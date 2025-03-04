import pathlib
import re
from typing import Any, Optional, Type

import appdirs
from loguru import logger

from commonwealth.settings.settings import BaseSettings, SettingsFromTheFuture


class Manager:
    SETTINGS_NAME_PREFIX = "settings-"

    def __init__(
        self,
        project_name: str,
        settings_type: Type[BaseSettings],
        config_folder: Optional[pathlib.Path] = None,
        load: bool = True,
    ) -> None:
        assert project_name, "project_name should be not empty"
        assert issubclass(settings_type, BaseSettings), "settings_type should use BaseSettings as subclass"

        self.project_name = project_name
        self.config_folder = (
            config_folder.joinpath(project_name)
            if config_folder
            else pathlib.Path(appdirs.user_config_dir(self.project_name))
        )
        self.config_folder.mkdir(parents=True, exist_ok=True)
        self.settings_type = settings_type
        self._settings = None
        logger.debug(
            f"Starting {project_name} settings with {settings_type.__name__}, configuration path: {config_folder}"
        )
        if load:
            self.load()

    @property
    def settings(self) -> Any:
        """Getter point for settings

        Returns:
            [Type[BaseSettings]]: The settings defined in the constructor
        """
        if not self._settings:
            self.load()

        return self._settings

    @settings.setter
    def settings(self, value: Any) -> None:
        """Setter point for settings. Save settings for every change

        Args:
            value ([Type[BaseSettings]]): The settings defined in the constructor
        """
        if not self._settings:
            self.load()

        self._settings = value
        self.save()

    def settings_file_path(self) -> pathlib.Path:
        """Return the settings file for the version specified in the constructor settings

        Returns:
            pathlib.Path: Path for the settings file
        """
        return self.config_folder.joinpath(f"{Manager.SETTINGS_NAME_PREFIX}{self.settings_type.VERSION}.json")

    @staticmethod
    def load_from_file(settings_type: Type[BaseSettings], file_path: pathlib.Path) -> Any:
        """Load settings from a generic location and settings type

        Args:
            settings_type (BaseSettings): Settings type that inherits from BaseSettings.
            file_path (pathlib.Path): Path for a valid settings file

        Returns:
            Any: The settings based on settings_type
        """
        assert issubclass(settings_type, BaseSettings), "settings_type should use BaseSettings as subclass"

        settings_data = settings_type()

        if file_path.exists():
            settings_data.load(file_path)
        else:
            settings_data.save(file_path)

        return settings_data

    def save(self) -> None:
        """Save settings"""
        self.settings.save(self.settings_file_path())

    def load(self) -> None:
        """Load settings"""

        def get_settings_version_from_filename(filename: pathlib.Path) -> int:
            result = re.search(f"{Manager.SETTINGS_NAME_PREFIX}(\\d+)", filename.name)
            assert result
            assert len(result.groups()) == 1
            return int(result.group(1))

        # Get all possible settings candidates and sort it by version
        valid_files = [
            possible_file
            for possible_file in self.config_folder.iterdir()
            if possible_file.name.startswith(Manager.SETTINGS_NAME_PREFIX)
        ]
        valid_files.sort(key=get_settings_version_from_filename, reverse=True)

        logger.debug(f"Found possible candidates for settings source: {valid_files}")
        for valid_file in valid_files:
            logger.debug(f"Checking {valid_file} for settings")
            try:
                self._settings = Manager.load_from_file(self.settings_type, valid_file)
                logger.debug(f"Using {valid_file} as settings source")
                return
            except SettingsFromTheFuture as exception:
                logger.debug("Invalid settings, going to try another file:", exception)

        self._settings = Manager.load_from_file(self.settings_type, self.settings_file_path())

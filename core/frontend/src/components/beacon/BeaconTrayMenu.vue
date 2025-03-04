<template>
  <v-menu
    v-if="is_connected_to_wifi"
    :close-on-content-click="false"
    nudge-left="150"
    nudge-bottom="25"
  >
    <template
      #activator="{ on, attrs }"
    >
      <v-card
        elevation="0"
        color="transparent"
        v-bind="attrs"
        v-on="on"
      >
        <v-icon
          v-tooltip="is_connected_to_wifi ?
            'Connected through a wireless connection, expect degraded performance'
            :
            'Connected through a wired connection'"
          class="px-1 white-shadow"
          :color="is_connected_to_wifi ? 'yellow' : 'white'"
        >
          mdi-ethernet-cable
        </v-icon>
      </v-card>
    </template>

    <v-card
      elevation="1"
      width="300"
    >
      <v-container>
        <div class="justify-center">
          It looks like you are reaching BlueOS via its wi-fi network. This can result in degraded performance.
          <span
            v-if="available_wired_domain()"
            class="mt-3"
            style="display: block;"
          >
            A wired connection is available:
            <v-btn
              small
              :href="`http://${available_wired_domain()}.local`"
            >
              Switch to {{ available_wired_domain() }}.local
            </v-btn>
          </span>
        </div>
      </v-container>
    </v-card>
  </v-menu>
</template>

<script lang="ts">
import Vue from 'vue'

import beacon from '@/store/beacon'
import { Domain, InterfaceType } from '@/types/beacon'
import { Dictionary } from '@/types/common'
import back_axios from '@/utils/api'

export default Vue.extend({
  name: 'BeaconTrayMenu',
  data() {
    return {
      probe_timer: 0,
      domains: {} as Dictionary<boolean>,
    }
  },
  computed: {
    wired_interface_domains(): Domain[] {
      return beacon.available_domains.filter((entry) => entry.interface_type === InterfaceType.WIRED)
    },
    wireless_interface_domains(): Domain[] {
      return beacon.available_domains.filter((entry) => entry.interface_type !== InterfaceType.WIRED)
    },
    is_connected_to_wifi(): boolean {
      return this.wireless_interface_domains.some((domain) => domain.ip === beacon.nginx_ip_address)
    },
  },
  mounted() {
    beacon.registerBeaconListener(this)
    this.probeDomains()
    this.probe_timer = setInterval(() => {
      this.probeDomains()
    }, 20000)
  },
  beforeDestroy() {
    clearInterval(this.probe_timer)
  },
  methods: {
    probeDomains() {
      // Probe beacon domains in an attempt to find a wired connection.
      if (!this.is_connected_to_wifi) {
        return
      }
      // GET errors cannot be suppressed in the console, so let's be transparent to the users about
      // why we are seeing them
      console.log('Trying to find a wired link to BlueOS...')
      for (const domain of this.wired_interface_domains) {
        back_axios({
          method: 'get',
          url: `http://${domain.ip}/status`,
          timeout: 1000,
        })
          .then(() => {
            this.domains[domain.hostname] = true
          })
          .catch(() => {
            this.domains[domain.hostname] = false
          })
      }
    },
    available_wired_domain(): string | null {
      for (const [domain, accessible] of Object.entries(this.domains)) {
        if (accessible) {
          return domain
        }
      }
      return null
    },
  },
})
</script>

<style>
.white-shadow {
  text-shadow: 0 0 3px #FFF;
}
</style>

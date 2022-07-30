<template>
  <div class="navigation-mobile">
    <v-row no-gutters class="text-center d-flex align-center justify-center">
      <v-col cols="4" @click="$router.push('/')" class="d-flex align-center justify-center" style="height: 60px">
        <v-icon size="32" class="ma-auto" color="white">mdi-home-outline</v-icon>
      </v-col>
      <v-col cols="4">
        <v-icon size="30" color="white">mdi-magnify</v-icon>
      </v-col>
      <v-col cols="4">
        <v-icon size="30" color="white">mdi-apps</v-icon>
      </v-col>
    </v-row>
  </div>
</template>
<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'NavigationMobile',
  data: () => ({}),
});
</script>

<style lang="scss">
.navigation-mobile {
  z-index: 1000;
  width: 100%;
  height: 60px;
  position: sticky;
  bottom: 0;
  background-color: #546e7a;
}
</style>

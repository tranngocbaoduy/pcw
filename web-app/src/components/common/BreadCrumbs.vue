<template>
  <v-breadcrumbs class="pa-0 ma-0" :items="breadcrumbs">
    <template v-slot:divider>
      <v-icon>mdi-chevron-right</v-icon>
    </template>
  </v-breadcrumbs>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  props: ['breadcrumbs'],
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
  },
});
</script>

<style lang="scss">
.v-breadcrumbs {
  .v-breadcrumbs__item {
    color: #1859db;
    font-size: 14px !important;
  }
  .v-breadcrumbs__item--disabled {
    color: #000000;
    font-weight: 700px !important;
    font-size: 14px !important;
  }
}
</style>

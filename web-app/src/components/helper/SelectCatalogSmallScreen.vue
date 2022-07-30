<template>
  <v-row class="mt-3 mb-0 pa-4">
    <v-col cols="6">
      <v-select :items="catalogItems" item-text="name" item-value="name" dense></v-select>
    </v-col>
    <v-col cols="6">
      <v-select :items="voteItems" item-text="name" item-value="name" dense></v-select>
    </v-col>
    <v-col cols="6">
      <v-select :items="brandItems" item-text="name" item-value="name" dense></v-select>
    </v-col>
    <v-col cols="6">
      <v-select :items="priceItems" item-text="name" item-value="name" dense></v-select>
    </v-col>
    <v-col cols="6">
      <v-select :items="agencyItems" item-text="name" item-value="name" dense></v-select>
    </v-col>
    <v-col cols="6">
      <v-select :items="shipItems" item-text="name" item-value="name" dense></v-select>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  props: ['catalogItems', 'voteItems', 'brandItems', 'priceItems', 'agencyItems', 'shipItems'],
  data: () => ({}),
});
</script>

<style lang="scss">
.background-list-title {
  position: inherit;
}
.header-title {
  position: sticky;
  z-index: 2;
  top: 0;
  color: white;
  background-color: #e8e9eb;
}
</style>

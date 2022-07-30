<template>
  <v-card :loading="loading" class="mx-auto pa-0 ma-0 rounded-0 elevation-4" max-width="374">
    <template slot="progress">
      <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
    </template>

    <v-img height="200" width="200" :src="require('../../assets/f201f0a8baee2ef5ee2adef6ac755c72.jpg')"></v-img>

    <v-card-title>Cafe Badilico</v-card-title>

    <v-card-text>
      <v-row align="center" class="mx-0">
        <v-rating :value="4.5" color="amber" dense half-increments readonly size="14"></v-rating>

        <div class="grey--text ml-4">4.5 (413)</div>
      </v-row>

      <div class="my-4 subtitle-1">$ • Italian, Cafe</div>

      <div>Small plates, salads & sandwiches - an intimate setting with 12 indoor seats plus patio seating.</div>
    </v-card-text>

    <v-divider class="mx-4"></v-divider>
    <!-- 
    <v-card-actions>
      <v-btn color="deep-purple lighten-2" text @click="reserve"> Reserve </v-btn>
    </v-card-actions> -->
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  data: () => ({
    loading: false,
    selection: 1,
  }),

  methods: {
    reserve() {
      this.loading = true;
      setTimeout(() => (this.loading = false), 2000);
    },
  },
});
</script>

<style scoped></style>

<template>
  <v-hover v-slot="{ hover }">
    <v-card class="rounded-xl pb-2 border-custom-4" :class="hover ? 'hover-custom-link elevation-12' : 'elevation-0'">
      <v-card-title class="font-weight-2 font-size-22 pa-5 pb-0" :class="hover ? 'primary-color-1 font-weight-3 ' : ''">
        {{ cards.title }}
      </v-card-title>
      <v-row no-gutters>
        <v-col class="d-flex child-flex pa-5" v-for="card in cards.Items" :key="card.subtitle" :cols="card.flex">
          <v-card class="border-custom-5">
            <v-img :src="card.src" aspect-ratio="1.2"></v-img>
          </v-card>
        </v-col>
      </v-row>
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  props: ['cards'],
});
</script>

<style lang="scss">
.v-img .v-responsive__sizer {
  padding-bottom: 0%;
}
</style>

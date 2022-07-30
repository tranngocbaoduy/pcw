<template>
  <div class="my-4">
    <v-row>
      <h3>Xu hướng tìm kiếm</h3>
      <v-col cols="12" class="font-color-1 d-inline-flex flex-wrap pa-4" justify="flex-start" align="space-around">
        <span class="py-2 px-4 font-size-14" v-for="(item, index) in trendingItems" :key="index"
          ><a href="#">{{ item }}</a></span
        >
      </v-col>
    </v-row>

    <v-row>
      <h3>{{ title }}</h3>
      <v-col cols="12" class="banner-content font-color-1 font-size-14"> {{ content }}</v-col>
      <!-- <template v-slot:actions>
        <v-btn text color="primary"> Dismiss </v-btn>
        <v-btn text color="primary"> Retry </v-btn>
      </template> -->
    </v-row>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  props: ['title', 'content', 'trendingItems'],
});
</script>

<style lang="scss">
.banner-content {
  font-size: 14px;
  line-height: 20px;
}
</style>

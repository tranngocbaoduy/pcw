<template>
  <div class="product-related">
    <div>
      <v-card-title class="pl-3 py-6">
        <span class="primary-color-3 font-size-26">{{ shopName }} </span>

        <v-spacer></v-spacer>
        <div
          class="item-expand-customer font-weight-2 font-size-14 float-right hover-custom-link"
          @click="$router.push(`/category/${categoryId}`)"
        >
          <span class="mr-3"> {{ $t('seeMore') }} </span>
          <v-icon size="24px">mdi-arrow-right-thin-circle-outline</v-icon>
        </div>
      </v-card-title>
    </div>

    <v-row no-gutters class="d-flex mb-6 px-0 align-start" align="start">
      <v-col lg="2" md="2" sm="4" xl="2" cols="6" v-for="item in relatedItems" :key="item.url">
        <router-link class="custom-link" :to="`/category/${categoryId}/product/${item['SK'].split('#').join('_')}`">
          <ProductRelated :item="item" />
          {{ item.brand }}item.brand
        </router-link>
      </v-col>
    </v-row>
    <v-divider class="mx-3"> </v-divider>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import ProductRelated from '@/components/product/ProductRelated.vue';

export default Vue.extend({
  components: {
    ProductRelated,
  },
  props: ['relatedItems', 'shopName', 'categoryId'],
  data: () => ({
    props: ['relatedProduct'],
  }),
});
</script>

<style lang="scss"></style>

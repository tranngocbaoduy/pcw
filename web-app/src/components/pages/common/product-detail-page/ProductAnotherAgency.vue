<template>
  <div class="product-related">
    <v-row no-gutters class="my-4">
      <v-col class="pa-0 ma-0" v-for="item in relatedItems" :key="item.url" cols="12">
        <ProductRelatedCard :item="item" />
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import ProductRelatedCard from '@/components/product/ProductRelatedCard.vue';
import { ProductItem } from '@/api/product.service';

export default Vue.extend({
  components: {
    ProductRelatedCard,
  },
  props: ['relatedItems', 'shopName'],
  data: () => ({
    props: ['relatedProduct'],
    sortItems: [] as ProductItem[],
  }),
  created() {},

  methods: {},
});
</script>

<style lang="scss">
</style>

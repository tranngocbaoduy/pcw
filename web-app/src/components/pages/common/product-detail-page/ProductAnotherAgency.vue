<template>
  <div class="product-related">
    <v-row no-gutters class="my-4">
      <v-col class="pa-0 ma-0" v-for="(item, index) in relatedItemsIsNew" :key="item.url" cols="12">
        <ProductRelatedCard :item="item" :class="isMobile && index % 2 == 0 ? 'bg-primary-color-6' : ''" />
      </v-col>
    </v-row>
    <v-row no-gutters class="my-4" v-if="relatedItemsIsUsed && relatedItemsIsUsed.length > 0">
      <v-col cols="12">
        <v-card-title class="primary-color-1 font-size-20 font-weight-3 pa-6">Sản phẩm đã qua sử dụng</v-card-title>
      </v-col>
      <v-col class="pa-0 ma-0" v-for="(item, index) in relatedItemsIsUsed" :key="item.url" cols="12">
        <ProductRelatedCard :item="item" :class="isMobile && index % 2 == 0 ? 'bg-primary-color-6' : ''" />
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
  computed: {
    relatedItemsIsUsed(): ProductItem[] {
      return this.relatedItems.filter((i: ProductItem) => i.isUsed);
    },
    relatedItemsIsNew(): ProductItem[] {
      return this.relatedItems.filter((i: ProductItem) => !i.isUsed);
    },
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
  },
  methods: {},
});
</script>

<style lang="scss"></style>

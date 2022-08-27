<template>
  <div class="product-related">
    <v-row no-gutters class="my-4">
      <v-col class="pa-0 ma-0" v-for="(item, index) in relatedItems" :key="item.url" cols="12">
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
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
  },
  methods: {},
});
</script>

<style lang="scss">
</style>

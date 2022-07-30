<template>
  <div class="product-related">
    <div>
      <v-card-title class="pl-3 py-6">
        <span class="primary-color-4 font-size-26">{{ shopName }} </span>

        <v-spacer></v-spacer>
      </v-card-title>
    </div>

    <v-row no-gutters class="d-flex mb-6 px-0 align-start" align="start">
      <v-col lg="3" md="3" sm="6" xl="2" cols="4" v-for="item in filterItems" :key="item.url">
        <a :href="item.url" class="custom-link" target="_blank">
          <ProductRelatedCard :item="item" />
        </a>
      </v-col>
      <v-col cols="12" class="d-flex justify-center align-center">
        <v-btn
          v-if="!isShowMore"
          class="white--text rounded-lg my-2"
          @click="isShowMore = true"
          color="#1859db"
          height="42px"
          width="144px"
          >{{ $t('See more') }}</v-btn
        >
        <v-btn
          v-if="isShowMore && !isShowAll"
          class="white--text rounded-lg my-2"
          @click="isShowAll = true"
          color="#1859db"
          height="42px"
          width="144px"
          >{{ $t('See all') }}</v-btn
        >
      </v-col>
    </v-row>
    <v-divider class="mx-3"> </v-divider>
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
    isShowMore: false,
    isShowAll: false,
    sortItems: [] as ProductItem[],
  }),
  created() {
    this.sortItems = JSON.parse(JSON.stringify(this.relatedItems));
    this.sortItems = this.sortItems.sort((itemA: ProductItem, itemB: ProductItem) => {
      if (itemA.price >= itemB.price) return 1;
      else return -1;
    }) as ProductItem[];
    console.log('this.sortItems', this.sortItems);
  },
  computed: {
    filterItems(): ProductItem[] {
      if (!this.isShowAll) {
        if (!this.isShowMore) {
          const items = [] as ProductItem[];
          const brands = [] as string[];
          for (const item of this.relatedItems) {
            if (!brands.includes(item.domain)) {
              items.push(item);
              brands.push(item.domain);
            }
          }
          console.log('brands', brands);
          return items;
        } else {
          const limit = 3;
          const brands = {} as any;
          const items = [] as ProductItem[];
          for (const item of this.relatedItems) {
            if (!(item.domain in brands)) {
              items.push(item);
              brands[item.domain] = 1;
            } else {
              if (brands[item.domain] < limit) {
                items.push(item);
                brands[item.domain] += 1;
              }
            }
          }
          return items;
        }
      }
      return this.sortItems;
    },
  },
});
</script>

<style lang="scss">
</style>

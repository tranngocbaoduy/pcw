<template>
  <div class="body-user-page pa-2" ref="body-user-page-ref">
    <Carousel />
    <RecommendProducts />
    <TrendingPromotion />
    <!-- <TrendingBrand /> -->
    <TrendingSearchProducts />
    <TrendingCategory :listItem="trendingCategoryItems" />
    <!-- <TrendingSearch></TrendingSearch> -->
    <!-- <Feature></Feature> -->
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Carousel from '@/components/common/CarouselCustom.vue';
import TrendingBrand from '@/components/pages/products/TrendingBrand.vue';
import TrendingPromotion from '@/components/pages/products/TrendingPromotion.vue';
import RecommendProducts from '@/components/pages/products/TrendingRecommendProducts.vue';
import TrendingSearchProducts from '@/components/pages/products/TrendingSearchProducts.vue';
import TrendingCategory from '@/components/pages/products/TrendingCategory.vue';
import { CategoryItem } from '@/api/category.service';

export default Vue.extend({
  name: 'Body',
  components: {
    Carousel,
    TrendingCategory,
    // TrendingBrand,
    TrendingPromotion,
    RecommendProducts,
    TrendingSearchProducts,
    // TrendingSearch,
    // Feature,
  },
  data: () => ({
    trendingCategoryItems: [] as CategoryItem[],
  }),
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    categoryItems(): CategoryItem[] {
      return this.$store.getters.categoryItems || [];
    },
  },
  created() {
    window.scrollTo({ top: 0, left: 0 });
    this.loadTrendingCategoryItems();
  },
  async mounted() {},
  watch: {
    async categoryItems() {
      if (this.categoryItems && this.categoryItems.length) {
        console.log('loadTrendingCategoryItems');
        this.loadTrendingCategoryItems();
      }
    },
  },
  methods: {
    loadTrendingCategoryItems() {
      this.trendingCategoryItems = [];
      for (const i of this.categoryItems) {
        try {
          i.image = require('@/assets/image/category/' + i.name.toLowerCase() + '.jpeg');
        } catch (err) {
          console.log('not jpeg');
          try {
            i.image = require('@/assets/image/category/' + i.name.toLowerCase() + '.png');
          } catch (err) {
            console.log('err');
          }
        }
        this.trendingCategoryItems.push(JSON.parse(JSON.stringify(i)));
      }
      // const catalog = [
      //   'Máy giặt',
      //   'Balo',
      //   'Sách nghệ thuật',
      //   'Kem chống nắng',
      //   'Tủ',
      //   'Sách tư duy',
      //   'Bàn ghế làm việc',
      // ].slice(0, 12);
      // for (const i of catalog) {
      //   this.trendingCategoryItems.push({
      //     PK: 'CATEGORY',
      //     SK: 'PHONE',
      //     name: 'phone',
      //     translateName: 'Phone',
      //     image: require('@/assets/image/category/phone.jpeg'),
      //     href: '/category/phone',
      //   });
      // }
    },
  },
});
</script>

<style lang="scss">
.body-user-page {
}
</style>

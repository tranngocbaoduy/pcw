<template>
  <div class="body-user-page pa-2" ref="body-user-page-ref">
    <Carousel />
    <RecommendProducts />
    <!-- <TrendingCategory></TrendingCategory> -->
    <TrendingPromotion />
    <!-- <TrendingBrand /> -->
    <TrendingSearchProducts />
    <TrendingCategory />
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
import TrendingSearchProducts from '@/components/pages/products/TrendingCategory.vue';
import TrendingCategory from '@/components/pages/products/TrendingSearchProducts.vue';

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
  data: () => ({}),
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
  },
  created() {
    window.scrollTo({ top: 0, left: 0 });
  },
});
</script>

<style lang="scss">
.body-user-page {
}
</style>

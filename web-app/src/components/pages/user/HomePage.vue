<template>
  <div class="body-user-page pa-2" ref="body-user-page-ref">
    <Carousel></Carousel>
    <TrendingCategory></TrendingCategory>
    <TrendingBrand></TrendingBrand>
    <TrendingPromotion class="my-4"></TrendingPromotion>
    <!-- <TrendingSearch></TrendingSearch> -->
    <Feature></Feature>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Carousel from '@/components/common/CarouselCustom.vue';
import TrendingCategory from '@/components/product/TrendingCategory.vue';
import TrendingBrand from '@/components/product/TrendingBrand.vue';
import TrendingPromotion from '@/components/product/TrendingPromotion.vue';
import TrendingSearch from '@/components/product/TrendingSearch.vue';
import Feature from '@/components/common/Feature.vue';

export default Vue.extend({
  name: 'Body',
  components: {
    Carousel,
    TrendingCategory,
    TrendingBrand,
    TrendingPromotion,
    // TrendingSearch,
    Feature,
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

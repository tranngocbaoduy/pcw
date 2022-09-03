<template>
  <div class="body-user-page pa-2" ref="body-user-page-ref" v-if="!isMobileAndHomePage">
    <Carousel />
    <RecommendProducts />
    <TrendingPromotion :promotionItems="promotionItems" />
    <!-- <TrendingBrand /> -->
    <TrendingCategory :listItem="trendingCategoryItems" />
    <!-- <TrendingSearchProducts /> -->
    <!-- <TrendingSearch></TrendingSearch> -->
    <!-- <Feature></Feature> -->
  </div>
  <div class="body-user-page-mobile pa-0" ref="body-user-page-ref" v-else>
    <SearchBar />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Carousel from '@/components/common/CarouselCustom.vue';
import SearchBar from '@/components/common/SearchBar.vue';
import TrendingPromotion from '@/components/pages/products/TrendingPromotion.vue';
import RecommendProducts from '@/components/pages/products/TrendingRecommendProducts.vue';
import TrendingCategory from '@/components/pages/products/TrendingCategory.vue';
import { CategoryItem } from '@/api/category.service';
import ProductService, { ProductItem } from '@/api/product.service';

export default Vue.extend({
  name: 'Body',
  components: {
    SearchBar,
    Carousel,
    TrendingCategory,
    // TrendingBrand,
    TrendingPromotion,
    RecommendProducts,
    // TrendingSearchProducts,
    // TrendingSearch,
    // Feature,
  },
  data: () => ({
    trendingCategoryItems: [] as CategoryItem[],
    promotionItems: [] as ProductItem[],
  }),
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    categoryItems(): CategoryItem[] {
      return this.$store.getters.categoryItems || [];
    },

    isMobileAndHomePage(): boolean {
      return this.isMobile && this.$route.path == '/';
    },
  },
  created() {
    window.scrollTo({ top: 0, left: 0 });
    this.loadTrendingCategoryItems();
    this.loadPromotionItems();
  },
  async mounted() {},
  watch: {
    async categoryItems() {
      if (this.categoryItems && this.categoryItems.length) {
        this.loadTrendingCategoryItems();
      }
    },
  },
  methods: {
    async loadPromotionItems() {
      this.promotionItems = await ProductService.queryPromotionItems({
        page: 1,
        limit: this.isMobile ? 8 : 21,
        discountRate: 2,
      });

      this.promotionItems = this.promotionItems.sort((itemA: ProductItem, itemB: ProductItem) => {
        const valueA = itemA.discountRate || 0;
        const valueB = itemB.discountRate || 0;
        // descending
        if (valueA < valueB) return 1;
        else return -1;
      });
    },
    async loadTrendingCategoryItems() {
      this.trendingCategoryItems = [];
      for (const i of this.categoryItems) {
        try {
          i.image = require('@/assets/image/category/' + i.name.toLowerCase() + '.jpeg');
        } catch (err) {
          // console.log('not jpeg');
          try {
            i.image = require('@/assets/image/category/' + i.name.toLowerCase() + '.png');
          } catch (err) {
            // console.log('err');
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
.body-user-page-mobile {
  overflow: hidden !important;
  position: relative !important;
  margin: 0 !important;
  padding: 0 !important;
}
</style>

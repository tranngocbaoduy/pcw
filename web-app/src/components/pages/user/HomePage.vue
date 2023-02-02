<template>
  <div class="body-user-page pa-2" ref="body-user-page-ref" v-if="!isMobileAndHomePage">
    <Carousel />
    <div v-if="categoryItems && categoryItems.length != 0">
      <RecommendProducts />
      <TrendingPromotion :promotionItems="promotionRow1Items" :category="categoryItems[0]" />
      <TrendingPromotion :promotionItems="promotionRow2Items" :category="categoryItems[1]" />
      <TrendingPromotion :promotionItems="promotionRow3Items" :category="categoryItems[2]" />
    </div>
    <!-- <TrendingBrand /> -->
    <!-- <TrendingCategory :listItem="trendingCategoryItems" /> -->
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
import { MetaInfo } from 'vue-meta';
import SeoService from '@/api/seo.service';

export default Vue.extend({
  name: 'Body',
  components: {
    SearchBar,
    Carousel,
    // TrendingCategory,
    // TrendingBrand,
    TrendingPromotion,
    RecommendProducts,
    // TrendingSearchProducts,
    // TrendingSearch,
    // Feature,
  },
  metaInfo(): MetaInfo {
    return SeoService.getMetaInfoHomePage();
  },
  data: () => ({
    trendingCategoryItems: [] as CategoryItem[],
    promotionRow1Items: [] as ProductItem[],
    promotionRow2Items: [] as ProductItem[],
    promotionRow3Items: [] as ProductItem[],
    randomCategory: {} as CategoryItem,
  }),
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    categoryItems(): CategoryItem[] {
      return this.$store.getters.categoryItems.filter((i: CategoryItem) => i.isLeaf) || [];
    },

    isMobileAndHomePage(): boolean {
      return this.isMobile && this.$route.path == '/';
    },
    categoryId(): string {
      return this.$route.params['idCate'] || '';
    },
  },
  created() {
    window.scrollTo({ top: 0, left: 0 });
  },
  async mounted() {},
  watch: {
    categoryItems() {
      const categoryItems = this.categoryItems;
      console.log('categoryItems', categoryItems);
      if (this.randomCategory && !this.randomCategory.id && categoryItems.length > 0) {
        this.randomCategory = categoryItems[Math.floor(Math.random() * categoryItems.length)];
        this.loadPromotionItems();
      }
    },
  },
  methods: {
    async loadPromotionItems() {
      this.promotionRow1Items = await ProductService.queryItemByTarget({
        categoryId: this.categoryItems[0].id,
        page: 1,
        limit: this.isMobile ? 8 : 21,
        discountRate: 30,
        isUsed: 'False',
      });
      this.promotionRow2Items = await ProductService.queryItemByTarget({
        categoryId: this.categoryItems[1].id,
        page: 1,
        limit: this.isMobile ? 8 : 21,
        discountRate: 30,
        isUsed: 'False',
      });
      this.promotionRow3Items = await ProductService.queryItemByTarget({
        categoryId: this.categoryItems[2].id,
        page: 1,
        limit: this.isMobile ? 8 : 21,
        discountRate: 30,
        isUsed: 'False',
      });
    },
    // async loadTrendingCategoryItems() {
    //   this.trendingCategoryItems = [];
    //   for (const i of this.categoryItems) {
    //     try {
    //       i.image = require('@/assets/image/category/' + i.name.toLowerCase() + '.jpeg');
    //     } catch (err) {
    //       // console.log('not jpeg');
    //       try {
    //         i.image = require('@/assets/image/category/' + i.name.toLowerCase() + '.png');
    //       } catch (err) {
    //         // console.log('err');
    //       }
    //     }
    //     this.trendingCategoryItems.push(JSON.parse(JSON.stringify(i)));
    //   }
    //   // const catalog = [
    //   //   'Máy giặt',
    //   //   'Balo',
    //   //   'Sách nghệ thuật',
    //   //   'Kem chống nắng',
    //   //   'Tủ',
    //   //   'Sách tư duy',
    //   //   'Bàn ghế làm việc',
    //   // ].slice(0, 12);
    //   // for (const i of catalog) {
    //   //   this.trendingCategoryItems.push({
    //   //     PK: 'CATEGORY',
    //   //     SK: 'PHONE',
    //   //     name: 'phone',
    //   //     translateName: 'Phone',
    //   //     image: require('@/assets/image/category/phone.jpeg'),
    //   //     href: '/category/phone',
    //   //   });
    //   // }
    // },
  },
});
</script>

<style lang="scss">
.body-user-page {
}
.body-user-page-mobile {
  // overflow: hidden !important;
  // position: relative !important;
  // margin: 0 !important;
  // padding: 0 !important;
}
</style>

<template>
  <div>
    <v-row class="category-page pt-0 mt-0" no-gutters :class="isMobile ? 'pa-0' : 'py-2 '">
      <div
        class="d-flex flex-column justify-center align-end"
        :class="isMobile ? 'transition-span-mobile' : 'transition-span'"
      >
        <v-btn
          @click="transitionToTopPage()"
          class="elevation-1 my-1 rounded-circle my-0"
          color="#1859db"
          style="background-color: white !important"
          icon
        >
          <v-icon size="20">mdi-arrow-up-bold</v-icon>
        </v-btn>
      </div>
      <v-col sm="12" md="12" cols="12" :class="isMobile ? 'py-0' : 'py-3'">
        <div class="mt-2 pa-0" :class="isMobile ? 'px-2' : 'px-0'">
          <BreadCrumbs :breadcrumbs="breadcrumbs" />
          <v-card-title class="product-page-name font-size-32 font-weight-3 px-0 mt-0 mx-0">{{
            categoryName
          }}</v-card-title>
        </div>
        <EnhancedFilter
          v-if="!isMobile"
          :brandItems="brandItems"
          :priceItems="priceItems"
          :agencyItems="agencyItems"
          @change-agency="changeAgency"
          @change-price="changePrice"
          @change-brand="changeBrand"
          class="ma-n2 pa-2 mx-0"
          @refresh-filter="refreshFilter"
        />
        <!-- :style="$vuetify.breakpoint.mdAndUp ? ' flex: 1 0 18%;' : ''" -->
        <div
          v-if="(filterProductItems && filterProductItems.length != 0) || !isLoading"
          class="mt-3"
          :class="isMobile ? 'px-2' : 'px-0'"
        >
          <v-row no-gutters>
            <v-col :key="item['SK']" v-for="item in filterProductItems" cols="6" md="2" xl="2" lg="2" sm="3">
              <router-link :to="`${getSlugId(item)}`">
                <Product :item="item" />
              </router-link>
            </v-col>
          </v-row>
        </div>
        <v-row v-else>
          <v-img :src="noItemImage" max-height="800" max-width="90%" height="400" class="ma-auto" />
        </v-row>

        <v-row no-gutters class="py-4">
          <v-col cols="12" class="d-flex justify-center align-center">
            <v-progress-circular v-if="isLoading" size="24" color="info" indeterminate></v-progress-circular>
            <v-btn
              v-else-if="!isLoading && isNextProduct"
              class="white--text rounded-lg my-2"
              @click="handleGetMoreProduct"
              color="#1859db"
              height="42px"
              width="144px"
              >{{ $t('See more') }}</v-btn
            >
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BreadCrumbs from '@/components/common/BreadCrumbs.vue';
import Product from '@/components/product/Product.vue';
import CategoryService from '@/api/category.service';
import ProductService, { ProductItem } from '@/api/product.service';

import EnhancedFilter from '@/components/search-filter/EnhancedFilter.vue';
import SeoService from '@/api/seo.service';
import { MetaInfo } from 'vue-meta';

export default Vue.extend({
  name: 'CategoryPage',
  props: [],
  components: {
    BreadCrumbs,
    Product,
    EnhancedFilter,
  },
  metaInfo(): MetaInfo {
    return SeoService.getMetaInfoCategoryPage(this.categoryName || '');
  },
  data: () => ({
    isLoading: false,
    isNextProduct: true,
    voteItems: [
      { name: '5-stars', rate: 5 },
      { name: '4-stars', rate: 4 },
      { name: '3-stars', rate: 3 },
      { name: '2-stars', rate: 2 },
      { name: '1-stars', rate: 1 },
    ],
    brandItems: [
      { name: 'Apple', selected: false },
      { name: 'Samsung', selected: false },
      { name: 'Xiaomi', selected: false },
      { name: 'OPPO', selected: false },
      { name: 'Huawei', selected: false },
      { name: 'Sony', selected: false },
    ],
    agencyItems: [
      { name: 'Tiki', selected: false, code: 'tiki' },
      // { name: 'Điện máy xanh', selected: false, code: 'dienmayxanh' },
      { name: 'Shopee', selected: false, code: 'shopee' },
      { name: 'Shopee Mall', selected: false, code: 'mall' },
      { name: 'Lazada Mall', selected: false, code: 'lazmall' },
      // { name: 'Lazada', selected: false },
      // { name: 'Sendo', selected: false },
      // { name: 'Nguyễn Kim', selected: false },
    ],
    shipItems: [
      { name: 'Nội địa: Giao hàng nhanh', selected: false },
      { name: 'Nội địa: Giao hàng thường', selected: false },
      { name: 'Quốc tế: Giao hàng nhanh', selected: false },
      { name: 'Quốc tế: Giao hàng thường', selected: false },
      { name: 'Miễn phí giao hàng', selected: false },
    ],
    noItemImage: require('@/assets/banner/no-product.png'),
    limit: 18,
    quantity: 18,
    page: 1,
    discountRate: 0,
    minMaxTuple: [0, 10000000] as number[],
    minMaxTupleDefault: [0, 10000000] as number[],
    productItems: [] as ProductItem[],
    priceItems: [] as any[],
  }),
  async created() {
    this.priceItems = [
      { id: 1, name: `${this.$t('Below')} 2 MIL VND`, selected: false, min: 0.3, max: 2 },
      { id: 2, name: `${this.$t('Range')} 2-4 MIL VND`, selected: false, min: 2, max: 4 },
      { id: 3, name: `${this.$t('Range')} 4-7 MIL VND`, selected: false, min: 4, max: 7 },
      { id: 4, name: `${this.$t('Range')} 7-13 MIL VND`, selected: false, min: 7, max: 13 },
      { id: 5, name: `${this.$t('Above')} 13 MIL VND`, selected: false, min: 13, max: 999 },
    ];
    this.page = 1;
    this.limit = this.isMobile ? 6 : 18;
    this.quantity = this.isMobile ? 6 : 18;
    await this.initialize();
    this.$store.commit('setState', { searchString: '' });
    this.$store.commit('setState', {
      searchFilter: {
        catalogItems: this.catalogItems,
        voteItems: this.voteItems,
        brandItems: this.brandItems,
        priceItems: this.priceItems,
        agencyItems: this.agencyItems,
        shipItems: this.shipItems,
      },
    });
  },
  mounted() {},
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    categoryName(): string {
      return CategoryService.upperCaseFirstLetter(CategoryService.code2category(this.categoryId))
        ? `${CategoryService.upperCaseFirstLetter(CategoryService.code2category(this.categoryId))}`
        : '';
    },
    categoryId(): string {
      return this.$route.params['idCate'] || '';
    },
    categoryItem(): any {
      return this.$store.getters.categoryItems.find((item: any) => item.SK == this.categoryId) || {};
    },
    catalogItems(): [] {
      return this.$store.getters.categoryItems.map((item: any) => ({
        name: CategoryService.code2category(item.SK),
        urlRoute: CategoryService.code2category(item.SK).split(' ').join('').toLowerCase(),
      }));
    },
    breadcrumbs(): any[] {
      return [
        {
          text: this.$t('home'),
          disabled: false,
          to: '/',
          exact: true,
        },
        {
          text: this.categoryName,
          to: `/category/${this.$route.params['idCate']}`,
          disabled: true,
          exact: true,
        },
      ];
    },

    filterProductItems() {
      const agencySelecting = this.agencyItems.filter((item: any) => item.selected).map((item: any) => item.code);
      const brandSelecting = this.brandItems
        .filter((item: any) => item.selected)
        .map((item: any) => CategoryService.upperCaseFirstLetter(item.name));
      return this.productItems.filter(
        (item: ProductItem) =>
          (agencySelecting.length == 0 || (agencySelecting && agencySelecting.includes(item.agency))) &&
          (brandSelecting.length == 0 ||
            (brandSelecting && brandSelecting.includes(CategoryService.upperCaseFirstLetter(item.brand)))) &&
          item.price > this.minMaxTuple[0] * 1000000 &&
          item.price < this.minMaxTuple[1] * 100000000
      );
    },

    brandItemsStore(): any {
      return this.$store.getters.brandItemsStore;
    },
  },

  watch: {
    async page() {
      if (this.page) {
        if (this.$route.query.page == this.page.toString()) {
          const query = { ...this.$route.query, page: this.page.toString() };
          this.$router.replace({ query: query || {} });
        }
      }
    },
    async categoryId() {
      await this.initialize();
    },
  },
  methods: {
    async initialize() {
      window.scrollTo({ top: 0, left: 0 });
      this.isLoading = true;

      console.log('Load item ...', this.categoryId);
      this.page = parseInt((this as any).$route.query.page || 1);
      this.$store.commit('setState', { searchString: this.$route.query.name });
      await this.loadBrandItems();
      await this.updateUrlQueryToData();
      this.isLoading = false;
    },
    async handleGetMoreProduct() {
      this.isLoading = true;
      this.isNextProduct = true;
      this.page += 1;
      const agencyItems = this.agencyItems.filter((item: any) => item.selected).map((item: any) => item.code);
      const brandItems = this.brandItems
        .filter((item: any) => item.selected)
        .map((item: any) => item.name.toLowerCase());
      const newItems = await ProductService.queryItemByTarget({
        category: this.categoryId.toUpperCase(),
        limit: this.limit,
        page: this.page,
        agencyItems: agencyItems,
        brandItems: brandItems,
        minPrice: this.minMaxTuple[0] * 1000000,
        maxPrice: this.minMaxTuple[1] * 1000000,
        isRep: true,
      });
      if (newItems && newItems.length == 0) this.isNextProduct = false;
      this.productItems = this.productItems.concat(newItems);
      this.isLoading = false;
    },
    async loadBrandItems() {
      const categoryId = this.categoryId.toUpperCase();
      if (
        !this.brandItemsStore ||
        (this.brandItemsStore && this.brandItemsStore.length == 0) ||
        !Object.keys(this.brandItemsStore).includes(categoryId)
      ) {
        this.brandItems = await CategoryService.queryBrandItems(categoryId);
        const brandItemsStore = this.brandItemsStore ? this.brandItemsStore : {};
        brandItemsStore[categoryId] = JSON.parse(JSON.stringify(this.brandItems));
        this.$store.commit('setState', { brandItemsStore: brandItemsStore });
      } else {
        this.brandItems = this.brandItemsStore[categoryId];
      }
    },
    async refreshFilter() {
      this.agencyItems = this.agencyItems.map((i) => ({
        ...i,
        selected: false,
      }));
      this.brandItems = this.brandItems.map((i) => ({
        ...i,
        selected: false,
      }));
      this.minMaxTuple = this.minMaxTupleDefault;
      await this.loadProductItemByTarget();
    },
    async changeAgency(agencyItems: any[]) {
      agencyItems.map((i) => {
        const agency = this.agencyItems.find((a) => i.code == a.code);
        if (agency && agency.selected.toString().length != 0) {
          agency.selected = !agency.selected;
        }
      });
      await this.loadProductItemByTarget();
    },
    async changeBrand(brandItems: any[]) {
      console.log(brandItems);
      brandItems.map((i) => {
        const brand = this.brandItems.find((a) => i.name == a.name);
        if (brand && brand.selected.toString().length != 0) {
          brand.selected = !brand.selected;
        }
      });
      await this.loadProductItemByTarget();
    },
    async changePrice({ min, max }: { min: number; max: number }) {
      this.minMaxTuple = [min, max];
      this.priceItems = this.priceItems.map((item: any) => ({
        ...item,
        selected:
          min != this.minMaxTupleDefault[0] && max != this.minMaxTupleDefault[1]
            ? item.min >= min && item.max <= max
            : false,
      }));
      await this.loadProductItemByTarget();
    },
    async updateUrlQueryToData(isRefresh?: false) {
      this.isLoading = true;
      const query = { ...this.$route.query };
      console.log('updateUrlQueryToData', query);
      const agencySelecting =
        !isRefresh && query && query.agencyItems && typeof query.agencyItems == 'string'
          ? query.agencyItems.split(',')
          : '';
      const brandSelecting =
        !isRefresh && query && query.brandItems && typeof query.brandItems == 'string'
          ? query.brandItems.split(',')
          : '';
      this.agencyItems = this.agencyItems.map((item: any) => ({
        ...item,
        selected: agencySelecting.includes(item.name),
      }));
      this.brandItems = this.brandItems.map((item: any) => ({
        ...item,
        selected: brandSelecting.includes(item.name),
      }));

      this.page = 1;
      await this.loadProductItemByTarget();

      this.isLoading = false;
    },

    async loadProductItemByTarget() {
      const agencyItems = this.agencyItems.filter((item: any) => item.selected).map((item: any) => item.code);
      const brandItems = this.brandItems
        .filter((item: any) => item.selected)
        .map((item: any) => item.name.toLowerCase());
      this.productItems = await ProductService.queryItemByTarget({
        category: this.categoryId.toUpperCase(),
        limit: this.limit,
        page: this.page,
        agencyItems: agencyItems,
        brandItems: brandItems,
        minPrice: this.minMaxTuple[0] * 1000000,
        maxPrice: this.minMaxTuple[1] * 1000000,
        discountRate: agencyItems.length != 0 || brandItems.length != 0 ? 0 : this.discountRate,
        isRep: true,
      });
      console.log('this.productItems', this.productItems);
    },
    getSlugId(item: ProductItem): string {
      return ProductService.getSlugId(item);
    },
    getIdProduct(item: ProductItem) {
      console.log('item', item);
      if (item['SK'].includes('REP')) return item['SK'].split('#').join('_');
      if (item['SK'].includes('CHILD')) {
        const newSK = item['SK']
          .split('#')
          .slice(0, item['SK'].split('#').length - 1)
          .join('_');
        return `${newSK.split('CHILD').join('REP')}_${item.relationshipID}`;
      }
      return '';
    },
    transitionToTopPage() {
      window.scrollTo({ top: -100, left: 0, behavior: 'smooth' });
    },
  },
});
</script>

<style lang="scss">
.category-page {
  width: 100%;
  .product-page-name {
    margin-bottom: 10px;
  }
  .product-page-result {
    align-items: center;
  }
  .product-page-quantity {
    width: 200px;
    height: 16px;
  }
  .product-page-filter {
    width: 261px;
    height: 48px;
    align-items: center;
    justify-content: flex-end;
  }
  .product-page-filter-title {
    width: 90px;
    height: 19px;
    margin-right: 15px;
  }
  .product-page-nav-left {
    width: 156px;
    height: 48px;
  }

  .transition-span {
    position: fixed;
    bottom: 30px;
    z-index: 100;
    right: 35px;
  }

  .transition-span-mobile {
    position: fixed;
    bottom: 90px;
    z-index: 100;
    right: 15px;
  }
}
</style>

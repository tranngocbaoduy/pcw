<template>
  <div>
    <v-row class="category-page pt-0 mt-0" no-gutters :class="isMobile ? 'pa-0' : 'py-2 '">
      <div
        class="d-flex flex-column justify-center align-end"
        :class="isMobile ? 'transition-span-mobile' : 'transition-span'"
      >
        <v-btn
          @click="toggleDetailMode()"
          class="elevation-1 my-1 rounded-circle my-0"
          color="#1859db"
          style="background-color: white !important"
          icon
        >
          <v-icon v-if="isDetailMode" size="20">mdi-image-filter-center-focus-strong</v-icon>
          <v-icon v-else size="20">mdi-image-filter-center-focus-weak</v-icon>
        </v-btn>
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
            selectedCategory ? selectedCategory.name : ''
          }}</v-card-title>
        </div>
        <EnhancedFilter
          v-if="!isMobile"
          :priceItems="priceItems"
          :agencyItems="agencyItemsByCategory"
          :filterSearchItems="filterSearchItems"
          :selectedIsUsedItems="isUsedItems"
          @change-agency="changeAgency"
          @change-price="changePrice"
          @change-filter="changeFilter"
          @change-selected-is-used="changeSelecetedIsUsed"
          @refresh-filter="refreshFilter"
          class="mx-0 py-2"
        />
        <!-- :style="$vuetify.breakpoint.mdAndUp ? ' flex: 1 0 18%;' : ''" -->
        <div
          v-if="(filterProductItems && filterProductItems.length != 0) || !isLoading"
          class="mt-3"
          :class="isMobile ? 'px-2' : 'px-0'"
        >
          <v-row no-gutters v-if="filterProductItemsByIsUsed(filterProductItems, false).length != 0">
            <v-col cols="12">
              <v-card-title
                class="product-page-name font-size-28 font-weight-3 px-0 mt-0 mx-0"
                v-if="selectedIsUsed == 'All'"
                >Sản phẩm mới</v-card-title
              ></v-col
            >
            <v-col
              :key="item['SK']"
              v-for="item in filterProductItemsByIsUsed(filterProductItems, false)"
              cols="6"
              md="2"
              xl="2"
              lg="2"
              sm="3"
            >
              <router-link :to="`${getSlugId(item)}`">
                <Product :item="item" />
              </router-link>
            </v-col>
          </v-row>
          <v-row no-gutters v-if="filterProductItemsByIsUsed(filterProductItems, true).length != 0">
            <v-col cols="12">
              <v-card-title class="product-page-name font-size-28 font-weight-3 px-0 mt-0 mx-0"
                >Sản phẩm đã qua sử dụng</v-card-title
              >
            </v-col>
            <v-col
              :key="item['SK']"
              v-for="item in filterProductItemsByIsUsed(filterProductItems, true)"
              cols="6"
              md="2"
              xl="2"
              lg="2"
              sm="3"
            >
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
import CategoryService, { CategoryItem } from '@/api/category.service';
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
    return SeoService.getMetaInfoCategoryPage(this.selectedCategory ? this.selectedCategory.name : '');
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
    agencyItems: CategoryService.agencyItems,
    isUsedItems: ['Sp Cũ', 'Tất cả'],
    selectedIsUsed: 'False',
    selectedAgency: '',
    shipItems: [
      { name: 'Nội địa: Giao hàng nhanh', selected: false },
      { name: 'Nội địa: Giao hàng thường', selected: false },
      { name: 'Quốc tế: Giao hàng nhanh', selected: false },
      { name: 'Quốc tế: Giao hàng thường', selected: false },
      { name: 'Miễn phí giao hàng', selected: false },
    ],
    noItemImage: require('@/assets/banner/no-product.png'),
    limit: 30,
    quantity: 30,
    page: 1,
    discountRate: 0,
    minMaxTuple: [0, 10000000] as number[],
    minMaxTupleDefault: [0, 10000000] as number[],
    productItems: [] as ProductItem[],
    filteredProductItems: [] as ProductItem[],
    priceItems: [] as any[],

    typeProducts: [] as string[],
    storageSizes: [] as string[],
    genProducts: [] as string[],
    screenSizes: [] as string[],
    yearProducts: [] as string[],
    ramProducts: [] as string[],
    coreNumProducts: [] as string[],
    networkSupportProducts: [] as string[],
    borderSizeProducts: [] as string[],
    filterSearchItems: [] as any[],
  }),
  async created() {
    this.priceItems = [
      { id: 1, name: `${this.$t('Below')} 10 MIL VND`, selected: false, min: 0.3, max: 10 },
      { id: 2, name: `${this.$t('Range')} 11 - 20 MIL VND`, selected: false, min: 11, max: 20 },
      { id: 3, name: `${this.$t('Range')} 21 - 30 MIL VND`, selected: false, min: 21, max: 30 },
      { id: 4, name: `${this.$t('Range')} 31 - 40 MIL VND`, selected: false, min: 31, max: 40 },
      { id: 5, name: `${this.$t('Above')} 40 MIL VND`, selected: false, min: 41, max: 999 },
    ];
    this.refreshPageNumber();
    await this.initialize();
    this.$store.commit('setState', { searchString: '' });
  },
  mounted() {},
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    isShowImageDetail(): boolean {
      return this.$store.getters.isShowImageDetail;
    },
    isDetailMode(): boolean {
      return this.$store.getters.isDetailMode;
    },
    selectedCategory(): CategoryItem {
      return this.$store.getters.selectedCategory;
    },
    categoryId(): string {
      return this.$route.params['idCate'] || '';
    },
    breadcrumbs(): any[] {
      const subBreadcrumbs = [] as any[];
      if (this.selectedCategory && this.selectedCategory.parents) {
        for (const category of this.selectedCategory.parents) {
          subBreadcrumbs.push({
            text: category ? category.name : '',
            to: `/category/${category.id}`,
            disabled: false,
            exact: true,
          });
        }
      }
      return [
        {
          text: this.$t('home'),
          disabled: false,
          to: '/',
          exact: true,
        },
        ...subBreadcrumbs,
        {
          text: this.selectedCategory ? this.selectedCategory.name : '',
          to: `/category/${this.$route.params['idCate']}`,
          disabled: true,
          exact: true,
        },
      ];
    },
    agencyItemsByCategory(): any[] {
      return this.selectedCategory ? CategoryService.agencyItemsByCategory(this.selectedCategory) : [];
    },

    filterProductItems() {
      return this.filteredProductItems && this.filteredProductItems.length > 0
        ? this.filteredProductItems
        : this.productItems;
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
    filterProductItemsByIsUsed(filteredProductItems: ProductItem[], isUsed = false) {
      return filteredProductItems.filter((i) => i.isUsed == isUsed);
    },
    toggleImage() {
      this.$store.commit('setState', { isShowImageDetail: !this.isShowImageDetail });
    },

    async toggleDetailMode() {
      console.log('set this.isDetailMode', !this.isDetailMode);
      this.$store.commit('setState', { isDetailMode: !this.isDetailMode });
      await this.loadProductItemByTarget();
    },
    async initialize() {
      window.scrollTo({ top: 0, left: 0 });
      this.isLoading = true;
      console.log('Load item ...', this.categoryId);
      this.page = parseInt((this as any).$route.query.page || 1);
      this.$store.commit('setState', { searchString: this.$route.query.name });
      await this.updateUrlQueryToData();
      this.isLoading = false;
      this.filterSearchItems = await ProductService.getFilterWareByKey({ categoryId: this.categoryId });
    },
    async handleGetMoreProduct() {
      this.isLoading = true;
      this.isNextProduct = true;
      this.page += 1;

      const newItems = await ProductService.queryItemByTarget({
        categoryId: this.categoryId.toUpperCase(),
        limit: this.limit,
        page: this.page,
        agencyItems: this.selectedAgency,
        minPrice: this.minMaxTuple[0] * 1000000,
        maxPrice: this.minMaxTuple[1] * 1000000,
        type: this.typeProducts && this.typeProducts.length > 0 ? this.typeProducts.join(',') : '',
        storageSize: this.storageSizes && this.storageSizes.length > 0 ? this.storageSizes.join(',') : '',
        screen: this.screenSizes && this.screenSizes.length > 0 ? this.screenSizes.join(',') : '',
        gen: this.genProducts && this.genProducts.length > 0 ? this.genProducts.join(',') : '',
        year: this.yearProducts && this.yearProducts.length > 0 ? this.yearProducts.join(',') : '',
        ram: this.ramProducts && this.ramProducts.length > 0 ? this.ramProducts.join(',') : '',
        coreNum: this.coreNumProducts && this.coreNumProducts.length > 0 ? this.coreNumProducts.join(',') : '',
        networkSupport:
          this.networkSupportProducts && this.networkSupportProducts.length > 0
            ? this.networkSupportProducts.join(',')
            : '',
        borderSize:
          this.borderSizeProducts && this.borderSizeProducts.length > 0 ? this.borderSizeProducts.join(',') : '',
        isUsed: this.selectedIsUsed,
        isUnique: !this.isDetailMode,
      });
      if (newItems && newItems.length == 0) this.isNextProduct = false;
      this.productItems = this.productItems.concat(newItems);
      this.isLoading = false;
    },
    async changeFilter(selectedFilters: any) {
      for (const key of Object.keys(selectedFilters)) {
        if (key == 'Type')
          this.typeProducts = selectedFilters[key].map((i: any) => i.toLocaleUpperCase().split(' ').join('_')).sort();
        if (key == 'Storage')
          this.storageSizes = selectedFilters[key].map((i: any) => i.toLocaleUpperCase().split(' ').join('_')).sort();
        if (key == 'Gen')
          this.genProducts = selectedFilters[key].map((i: any) => i.toLocaleUpperCase().split(' ').join('_')).sort();
        if (key == 'Year')
          this.yearProducts = selectedFilters[key].map((i: any) => i.toLocaleUpperCase().split(' ').join('_')).sort();
        if (key == 'Screen')
          this.screenSizes = selectedFilters[key].map((i: any) => i.toLocaleUpperCase().split(' ').join('_')).sort();
        if (key == 'Ram')
          this.ramProducts = selectedFilters[key].map((i: any) => i.toLocaleUpperCase().split(' ').join('_')).sort();
        if (key == 'Core')
          this.ramProducts = selectedFilters[key].map((i: any) => i.toLocaleUpperCase().split(' ').join('_')).sort();
        if (key == 'Network Support')
          this.networkSupportProducts = selectedFilters[key]
            .map((i: any) => i.toLocaleUpperCase().split(' ').join('_'))
            .sort();
        if (key == 'Border Size')
          this.borderSizeProducts = selectedFilters[key]
            .map((i: any) => i.toLocaleUpperCase().split(' ').join('_'))
            .sort();
      }

      this.refreshPageNumber();
      this.productItems = await ProductService.queryItemByTarget({
        categoryId: this.categoryId.toUpperCase(),
        limit: this.limit,
        page: this.page,
        agencyItems: this.selectedAgency,
        minPrice: this.minMaxTuple[0] * 1000000,
        maxPrice: this.minMaxTuple[1] * 1000000,
        type: this.typeProducts && this.typeProducts.length > 0 ? this.typeProducts.join(',') : '',
        storageSize: this.storageSizes && this.storageSizes.length > 0 ? this.storageSizes.join(',') : '',
        screen: this.screenSizes && this.screenSizes.length > 0 ? this.screenSizes.join(',') : '',
        gen: this.genProducts && this.genProducts.length > 0 ? this.genProducts.join(',') : '',
        year: this.yearProducts && this.yearProducts.length > 0 ? this.yearProducts.join(',') : '',
        ram: this.ramProducts && this.ramProducts.length > 0 ? this.ramProducts.join(',') : '',
        coreNum: this.coreNumProducts && this.coreNumProducts.length > 0 ? this.coreNumProducts.join(',') : '',
        networkSupport:
          this.networkSupportProducts && this.networkSupportProducts.length > 0
            ? this.networkSupportProducts.join(',')
            : '',
        borderSize:
          this.borderSizeProducts && this.borderSizeProducts.length > 0 ? this.borderSizeProducts.join(',') : '',
        isUsed: this.selectedIsUsed,
        isUnique: !this.isDetailMode,
      });
    },
    refreshPageNumber() {
      this.limit = this.isMobile ? 6 : 30;
      this.quantity = this.isMobile ? 6 : 30;
      this.page = 1;
    },
    async refreshFilter() {
      this.minMaxTuple = this.minMaxTupleDefault;
      this.selectedAgency = '';
      this.typeProducts = [];
      this.screenSizes = [];
      this.storageSizes = [];
      this.yearProducts = [];
      this.genProducts = [];
      this.screenSizes = [];
      this.ramProducts = [];
      this.coreNumProducts = [];
      this.selectedIsUsed = 'False';
      await this.loadProductItemByTarget();
    },
    async changeSelecetedIsUsed(selectedIsUsedItems: any) {
      if (selectedIsUsedItems.includes('Tất cả')) {
        this.selectedIsUsed = 'All';
      } else if (selectedIsUsedItems.includes('Sp Cũ')) {
        this.selectedIsUsed = 'True';
      } else {
        this.selectedIsUsed = 'False';
      }
      await this.loadProductItemByTarget();
    },
    async changeAgency(agencyItems: any[]) {
      this.selectedAgency = agencyItems.map((i) => i.code).join(',');
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
      const agencySelecting =
        !isRefresh && query && query.agencyItems && typeof query.agencyItems == 'string'
          ? query.agencyItems.split(',')
          : '';
      this.agencyItems = this.agencyItems.map((item: any) => ({
        ...item,
        selected: agencySelecting.includes(item.name),
      }));

      this.page = 1;
      await this.loadProductItemByTarget();

      this.isLoading = false;
    },

    async loadProductItemByTarget() {
      this.productItems = await ProductService.queryItemByTarget({
        categoryId: this.categoryId.toUpperCase(),
        limit: this.limit,
        page: this.page,
        agencyItems: this.selectedAgency,
        minPrice: this.minMaxTuple[0] * 1000000,
        maxPrice: this.minMaxTuple[1] * 1000000,
        type: this.typeProducts && this.typeProducts.length > 0 ? this.typeProducts.join(',') : '',
        storageSize: this.storageSizes && this.storageSizes.length > 0 ? this.storageSizes.join(',') : '',
        screen: this.screenSizes && this.screenSizes.length > 0 ? this.screenSizes.join(',') : '',
        gen: this.genProducts && this.genProducts.length > 0 ? this.genProducts.join(',') : '',
        year: this.yearProducts && this.yearProducts.length > 0 ? this.yearProducts.join(',') : '',
        ram: this.ramProducts && this.ramProducts.length > 0 ? this.ramProducts.join(',') : '',
        coreNum: this.coreNumProducts && this.coreNumProducts.length > 0 ? this.coreNumProducts.join(',') : '',
        networkSupport:
          this.networkSupportProducts && this.networkSupportProducts.length > 0
            ? this.networkSupportProducts.join(',')
            : '',
        borderSize:
          this.borderSizeProducts && this.borderSizeProducts.length > 0 ? this.borderSizeProducts.join(',') : '',
        discountRate: this.selectedAgency.split(',').length != 0 ? 0 : this.discountRate,
        isUsed: this.selectedIsUsed,
        isUnique: !this.isDetailMode,
      });
      // console.log('this.productItems', this.productItems);
    },
    getSlugId(item: ProductItem): string {
      return ProductService.getSlugId(item);
    },
    getIdProduct(item: ProductItem) {
      return item.id;
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

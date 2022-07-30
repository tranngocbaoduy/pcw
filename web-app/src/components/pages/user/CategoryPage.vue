<template>
  <v-row class="category-page pt-0 mt-0" no-gutters :class="isMobile ? 'pa-0' : 'pa-2 '">
    <v-col sm="12" md="2" cols="12" class="pa-0 pt-2 px-2">
      <SelectCatalogLargeScreen
        v-if="!isMobile"
        :catalogItems="catalogItems"
        :voteItems="voteItems"
        :brandItems="brandItems"
        :priceItems="priceItems"
        :agencyItems="agencyItems"
        :shipItems="shipItems"
        @handle-choose-price="handleChoosePrice"
        @handle-choose-price-custom="handleChoosePiceCustom"
      />
      <!-- <SelectCatalogSmallScreen
        v-else
        :catalogItems="catalogItems"
        :voteItems="voteItems"
        :brandItems="brandItems"
        :priceItems="priceItems"
        :agencyItems="agencyItems"
        :shipItems="shipItems"
      /> -->
    </v-col>
    <v-col sm="12" md="10" cols="12" :class="isMobile ? 'py-0' : 'py-3'">
      <div class="mt-2 pa-0">
        <BreadCrumbs :breadcrumbs="breadcrumbs" />
        <ProductLine :items="relatedItems"></ProductLine>
        <v-card-title class="product-page-name font-size-32 font-weight-3 px-4 mt-2 mx-0">{{
          categoryName
        }}</v-card-title>

        <!-- <v-row class="product-page-result pa-0 mb-4 mx-0">
        <v-card-text class="product-page-quantity font-size-14 font-weight-2 pa-0">1-48 trên 6000 kết quả</v-card-text>
        <v-row class="product-page-filter pa-0 ma-0">
          <v-card-text class="product-page-filter-title font-size-16 font-weight-2 pa-0">Ưu tiên xem</v-card-text>
          <div class="product-page-nav-left">
            <v-select label="Phổ biến nhất" hide-details solo></v-select>
          </div>
        </v-row>
      </v-row> -->
      </div>
      <div v-if="filterProductItems && filterProductItems.length != 0">
        <v-row class="mx-1 my-2"> </v-row>
        <v-row no-gutters>
          <!-- class="lg5-custom" -->
          <v-col lg="3" md="4" sm="4" xl="3" cols="6" v-for="item in filterProductItems" :key="item['SK']">
            <router-link class="custom-link" :to="`/category/${$route.params['idCate']}/product/${getIdProduct(item)}`"
              ><Product :item="item" />
            </router-link>
          </v-col>
        </v-row>
      </div>
      <v-row v-else>
        <v-img :src="noItemImage" max-height="800" max-width="90%" height="400" class="ma-auto" />
      </v-row>

      <v-row no-gutters class="pb-4">
        <v-col cols="12" class="d-flex justify-center align-center">
          <v-progress-circular v-if="isLoading" size="24" color="info" indeterminate></v-progress-circular>

          <v-btn
            v-else
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

    <!-- <AccountMenu :isShowMenu="isShowMenu" /> -->
  </v-row>
</template>

<script lang="ts">
import Vue from 'vue';

import SelectCatalogLargeScreen from '@/components/helper/SelectCatalogLargeScreen.vue';
// import SelectCatalogSmallScreen from '@/components/helper/SelectCatalogSmallScreen.vue';
import BreadCrumbs from '@/components/common/BreadCrumbs.vue';
import Product from '@/components/product/Product.vue';
import CategoryService from '@/api/category.service';
import ProductService, { ProductItem } from '@/api/product.service';
import ProductLine from '@/components/product/ProductLine.vue';

export default Vue.extend({
  name: 'CategoryPage',
  props: [],
  components: {
    BreadCrumbs,
    Product,
    // SelectCatalogSmallScreen,
    ProductLine,
    SelectCatalogLargeScreen,
  },
  data: () => ({
    isLoading: false,
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
      { name: 'Điện máy xanh', selected: false, code: 'dienmayxanh' },
      { name: 'Shopee', selected: false, code: 'shopee' },
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

    limit: 12,
    quantity: 12,
    page: 1,
    discountRate: 0,
    loader: {} as any,
    minMaxTuple: [0, 1000] as number[],
    productItems: [] as ProductItem[],
    relatedItems: [] as ProductItem[],
    rowsPerPage: 32,
    priceItems: [
      { id: 1, name: 'Below 2 MIL VND', selected: false, min: 0, max: 2 },
      { id: 2, name: 'Range 2-4 MIL VND', selected: false, min: 2, max: 4 },
      { id: 3, name: 'Range 4-7 MIL VND', selected: false, min: 4, max: 7 },
      { id: 4, name: 'Range 7-13 MIL VND', selected: false, min: 7, max: 13 },
      { id: 5, name: 'Above 13 MIL VND', selected: false, min: 13, max: 999 },
    ] as any[],
  }),
  async created() {
    this.page = 1;
    await this.initialize();
    this.$store.commit('setState', { searchString: '' });
  },
  mounted() {
    this.updateUrlQueryToData();
  },
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    categoryName(): string {
      return this.$t(
        `category.${CategoryService.upperCaseFirstLetter(CategoryService.code2category(this.categoryId))}`
      ).toString();
    },
    categoryId(): string {
      return this.$route.params['idCate'];
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
          text: this.$t(`category.${CategoryService.code2category(this.categoryId)}`),
          to: `/category/${this.$route.params['idCate']}`,
          disabled: true,
          exact: true,
        },
      ];
    },

    filterProductItems() {
      const agencySelecting = this.agencyItems
        .filter((item: any) => item.selected)
        .map((item: any) => CategoryService.upperCaseFirstLetter(item.name));
      const brandSelecting = this.brandItems
        .filter((item: any) => item.selected)
        .map((item: any) => CategoryService.upperCaseFirstLetter(item.name));
      return this.productItems.filter(
        (item: ProductItem) =>
          (agencySelecting.length == 0 ||
            (agencySelecting && agencySelecting.includes(CategoryService.upperCaseFirstLetter(item.domain)))) &&
          (brandSelecting.length == 0 ||
            (brandSelecting && brandSelecting.includes(CategoryService.upperCaseFirstLetter(item.brand)))) &&
          item.price > this.minMaxTuple[0] * 1000000 &&
          item.price < this.minMaxTuple[1] * 100000000
      );
    },

    brandItemsStore(): any {
      return this.$store.getters.brandItemsStore;
    },
    isCustomePrice(): boolean {
      return this.minMaxTuple[0] != 0 || this.minMaxTuple[1] != 1000;
    },
  },

  watch: {
    '$route.query'() {
      this.updateUrlQueryToData();
    },
    minMaxTuple() {
      if (this.minMaxTuple[0] != 0 && this.minMaxTuple[1] != 1000) {
        const query = {
          ...this.$route.query,
          minPrice: this.minMaxTuple[0],
          maxPrice: this.minMaxTuple[1],
        };
        this.$router.replace({ query: (query as any) || {} });
      }
    },
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
      const loading = this.$loading.show();

      console.log('Load item ...', this.categoryId);
      this.page = parseInt((this as any).$route.query.page || 1);
      this.$store.commit('setState', { searchString: this.$route.query.name });
      await this.loadBrandItems();
      await this.handleParamsOnUrl();
      await this.loadProductItemByTarget();
      // this.productItems = await ProductService.queryItemByCategoryId(this.categoryId.toUpperCase(), 10);
      this.relatedItems = await ProductService.queryItemByTarget({
        category: this.categoryId.toUpperCase(),
        limit: 16,
        page: 1,
        agencyItems: this.agencyItems.map((item: any) => item.code),
        brandItems: ['samsung'],
        minPrice: this.minMaxTuple[0] * 1000000,
        maxPrice: this.minMaxTuple[1] * 1000000,
      });
      loading.hide();
    },
    async handleGetMoreProduct() {
      this.isLoading = true;
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
        isRep: this.isCustomePrice ? false : true,
      });
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
    async handleParamsOnUrl() {
      const query = { ...this.$route.query };
      const agencySelecting =
        query && query.agencyItems && typeof query.agencyItems == 'string' ? query.agencyItems.split(',') : '';
      console.log('agencySelecting', agencySelecting);
      const brandSelecting =
        query && query.brandItems && typeof query.brandItems == 'string' ? query.brandItems.split(',') : '';
      console.log('brandSelecting', brandSelecting);
      this.agencyItems = this.agencyItems.map((item: any) => ({
        ...item,
        selected: agencySelecting.includes(item.name),
      }));
      this.brandItems = this.brandItems.map((item: any) => ({
        ...item,
        selected: brandSelecting.includes(item.name),
      }));
    },
    handleChoosePrice(item: any) {
      const id = item.id;
      const newPriceItems = [];
      for (const item of this.priceItems) {
        if (item.id == id) {
          item.selected = !item.selected;
        }
        newPriceItems.push({ ...item });
      }
      this.priceItems = [...newPriceItems];

      const filterItems = this.priceItems.filter((item: any) => item.selected);
      const minItems = filterItems.map((item: any) => item.min);
      const maxItems = filterItems.map((item: any) => item.max);
      if (Math.min(...minItems) == Infinity || Math.max(...maxItems) == Infinity) {
        this.minMaxTuple = [0, 1000];
      } else {
        this.minMaxTuple = [Math.min(...minItems), Math.max(...maxItems)];
        if (!this.minMaxTuple[0] || !this.minMaxTuple[1]) {
          this.minMaxTuple = [0, 1000];
        }
      }
    },
    handleChoosePiceCustom(min: number, max: number) {
      this.minMaxTuple = [min, max];
    },
    updateUrlQuery(name: string) {
      const urlParams = new URLSearchParams(window.location.search);
      urlParams.set('page', name);
      const queryUrl = urlParams.toString();
      history.replaceState({}, '', `${this.$route.path}?${queryUrl}`);
    },
    setValue(obj: any, path: string, value: any) {
      const a = path.split('.');
      let o = obj;
      while (a.length - 1) {
        const n: any = a.shift();
        if (!(n in o)) o[n] = {};
        o = o[n];
      }
      o[a[0]] = value;
    },

    getValue(obj: any, path: string) {
      path = path.replace(/\[(\w+)\]/g, '.$1');
      path = path.replace(/^\./, '');
      const a = path.split('.');
      let o = obj;
      while (a.length) {
        const n: any = a.shift();
        if (!(n in o)) return;
        o = o[n];
      }
      return o;
    },
    async updateUrlQueryToData() {
      const query = { ...this.$route.query };
      const agencySelecting =
        query && query.agencyItems && typeof query.agencyItems == 'string' ? query.agencyItems.split(',') : '';
      const brandSelecting =
        query && query.brandItems && typeof query.brandItems == 'string' ? query.brandItems.split(',') : '';
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
        isRep: this.isCustomePrice ? false : true,
      });
      console.log('this.productItems', this.productItems);
    },

    getIdProduct(item: ProductItem) {
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

  // @media (min-width: 1264px) and (max-width: 1903px) {
  //   .flex.lg5-custom {
  //     width: 20%;
  //     max-width: 20%;
  //     flex-basis: 20%;
  //   }
  // }
}
</style>

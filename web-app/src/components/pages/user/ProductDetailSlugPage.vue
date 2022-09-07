<template>
  <div class="product-detail-slug-page mt-3">
    <div
      class="d-flex flex-column justify-center align-end"
      :class="isMobile ? 'transition-span-mobile' : 'transition-span'"
    >
      <v-btn
        @click="transitionToCompare(0)"
        class="elevation-1 my-1 rounded-circle my-0"
        color="#1859db"
        style="background-color: white !important"
        icon
      >
        <v-icon size="20">mdi-store-search</v-icon>
      </v-btn>
      <v-btn
        @click="transitionToCompare(1)"
        class="elevation-1 my-1 rounded-circle my-0"
        color="#1859db"
        style="background-color: white !important"
        icon
      >
        <v-icon size="18">mdi-comment</v-icon>
      </v-btn>
      <!-- <v-btn
        @click="transitionToCompare(2)"
        class="elevation-1 my-1 rounded-circle my-0"
        color="#1859db"
        style="background-color: white !important"
        icon
      >
        <v-icon size="20">mdi-information</v-icon>
      </v-btn> -->

      <v-menu
        v-if="isMobile && tabModel == 0"
        :close-on-click="false"
        :close-on-content-click="true"
        bottom
        left
        nudge-bottom="40"
        z-index="2000"
        content-class="elevation-1 font-size-12"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            class="elevation-1 rounded-circle my-2"
            icon
            style="background-color: white !important"
            :color="isHasFilterBy ? '#1859db' : '#6e6e6e'"
            v-bind="attrs"
            retain-focus-on-click
            v-on="on"
          >
            <v-tooltip top>
              <template v-slot:activator="{ on: tooltip }">
                <v-icon :color="isHasFilterBy ? '#1859db' : '#6e6e6e'" v-bind="attrs" v-on="{ ...tooltip }" size="20"
                  >mdi-filter</v-icon
                >
              </template>
              <span>Filter By</span>
            </v-tooltip>
          </v-btn>
        </template>

        <v-list class="pa-0 py-0 ma-0 elevation-0 rounded-0 font-size-12">
          <v-list-item
            v-for="(item, index) in filterByProductAnotherAgency"
            :key="`${index}-filter-product`"
            class="hover-custom-link pa-0 ma-0 px-2 font-size-12"
            @click="handleChangeFilter(item)"
          >
            <v-checkbox class="font-size-12 py-0 mt-0" hide-details :label="item.name"></v-checkbox>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-btn
        @click="transitionToCompare(-1)"
        class="elevation-1 my-1 rounded-circle my-0"
        color="#1859db"
        style="background-color: white !important"
        icon
      >
        <v-icon size="20">mdi-arrow-up-bold</v-icon>
      </v-btn>
    </div>
    <div v-if="mainProduct && Object.keys(mainProduct).length != 0">
      <BreadCrumbs class="mt-4 px-2" :breadcrumbs="breadcrumbs" />
      <v-row class="mt-4 mb-8" no-gutters>
        <v-col sm="12" md="5" cols="12" class="pl-0" :class="isMobile ? 'pl-4 pr-4' : 'pr-4'" v-if="listPhotoItems">
          <ProductPhoto :listPhotoItems="listPhotoItems" />
        </v-col>
        <v-col sm="12" md="7" cols="12" class="px-2">
          <ProductInfo
            :item="mainProduct"
            :averagePrice="averagePrice"
            :subProductItems="subProductItems"
            :largestSaleOffItem="largestSaleOffItem"
            :domain="mainProduct.domain"
            :cheapestItem="cheapestItem"
          />
        </v-col>
      </v-row>
      <v-row no-gutters id="detail-rating-item">
        <v-col cols="12">
          <v-card class="elevation-0 rounded-sm" height="100%">
            <v-tabs v-model="tabModel" color="#1859db" left background-color="transparent">
              <v-tab :class="isMobile ? 'font-size-14' : 'font-size-14'">Các cửa hàng ({{ allProduct.length }})</v-tab>
              <v-tab :class="isMobile ? 'font-size-14' : 'font-size-14'">Đánh giá</v-tab>
              <v-tab
                :class="isMobile ? 'font-size-14' : 'font-size-14'"
                v-if="mainProduct && mainProduct.description && mainProduct.description.length != 0"
                >Thông tin</v-tab
              >
            </v-tabs>

            <v-tabs-items v-model="tabModel">
              <v-tab-item>
                <v-menu
                  :close-on-click="false"
                  :close-on-content-click="true"
                  bottom
                  left
                  nudge-bottom="40"
                  z-index="2000"
                  content-class="elevation-1 font-size-12"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      v-if="!isMobile"
                      class="filter-product-another-agency rounded-lg my-2"
                      icon
                      :color="isHasFilterBy ? '#1859db' : '#6e6e6e'"
                      v-bind="attrs"
                      retain-focus-on-click
                      v-on="on"
                    >
                      <v-tooltip top>
                        <template v-slot:activator="{ on: tooltip }">
                          <v-icon
                            :color="isHasFilterBy ? '#1859db' : '#6e6e6e'"
                            v-bind="attrs"
                            v-on="{ ...tooltip }"
                            size="20"
                            >mdi-filter</v-icon
                          >
                        </template>
                        <span>Filter By</span>
                      </v-tooltip>
                    </v-btn>
                  </template>

                  <v-list class="pa-0 py-2 ma-0 elevation-0 rounded-0 font-size-12">
                    <v-list-item
                      v-for="(item, index) in filterByProductAnotherAgency"
                      :key="`${index}-filter-product`"
                      class="hover-custom-link pa-0 ma-0 px-2 font-size-12"
                      @click="handleChangeFilter(item)"
                    >
                      <v-checkbox class="font-size-12 py-0 mt-0" hide-details :label="item.name"></v-checkbox>
                    </v-list-item>
                  </v-list>
                </v-menu>
                <v-menu
                  :close-on-click="true"
                  :close-on-content-click="true"
                  bottom
                  left
                  nudge-bottom="40"
                  z-index="2000"
                  content-class="elevation-1 font-size-12"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      class="rounded-lg my-2"
                      :class="isMobile ? 'sort-by-product-another-agency-mobile' : 'sort-by-product-another-agency'"
                      icon
                      :color="isHasSortBy ? '#1859db' : '#6e6e6e'"
                      v-bind="attrs"
                      retain-focus-on-click
                      v-on="on"
                    >
                      <v-tooltip top>
                        <template v-slot:activator="{ on: tooltip }">
                          <v-icon
                            :color="isHasSortBy ? '#1859db' : '#6e6e6e'"
                            v-bind="attrs"
                            v-on="{ ...tooltip }"
                            size="20"
                            >mdi-sort-descending</v-icon
                          >
                        </template>
                        <span>Sort by</span>
                      </v-tooltip>
                    </v-btn>
                  </template>

                  <v-list class="pa-0 py-2 ma-0 elevation-0 rounded-0">
                    <v-list-item
                      v-for="(item, index) in sortByProductAnotherAgency"
                      :key="`${index}-filter-product`"
                      class="hover-custom-link pa-0 ma-0 px-2 font-size-12"
                      @click="handleChangeSorter(item)"
                    >
                      <span class="font-size-12">{{ item.name }}</span>
                    </v-list-item>
                  </v-list>
                </v-menu>

                <ProductAnotherAgency
                  v-if="filterProductItems && filterProductItems.length != 0"
                  :relatedItems="filterProductItems"
                  :shopName="$t('anotherAgency')"
                />
              </v-tab-item>
              <v-tab-item>
                <DetailRatingItem :itemRating="mainProduct.itemRating" />
              </v-tab-item>
              <v-tab-item
                class="pa-4"
                v-if="mainProduct && mainProduct.description && mainProduct.description.length != 0"
                v-html="mainProduct && mainProduct.description ? mainProduct.description : ''"
              >
              </v-tab-item>
            </v-tabs-items> </v-card
        ></v-col>
      </v-row>
    </div>
    <v-row v-else>
      <v-img :src="noItemImage" max-height="800" max-width="90%" height="400" class="ma-auto" />
    </v-row>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BreadCrumbs from '@/components/common/BreadCrumbs.vue';
import ProductPhoto from '@/components/pages/common/product-detail-page/ProductPhoto.vue';
import ProductInfo from '@/components/pages/common/product-detail-page/ProductInfo.vue';
import ProductAnotherAgency from '@/components/pages/common/product-detail-page/ProductAnotherAgency.vue';
import CategoryService from '@/api/category.service';
import ProductService, { ProductItem } from '@/api/product.service';
import DetailRatingItem from '@/components/common/rating/DetailRatingItem.vue';
import SeoService from '@/api/seo.service';
import { MetaInfo } from 'vue-meta';

export default Vue.extend({
  name: 'Body',
  props: ['isShowMenu'],
  components: {
    BreadCrumbs,
    ProductPhoto,
    ProductInfo,
    ProductAnotherAgency,
    DetailRatingItem,
    // ListProductRelated,
  },
  metaInfo(): MetaInfo {
    const name = this.mainProduct ? this.mainProduct.cleanName || '' : '';
    const url = this.listPhotoItems && this.listPhotoItems.length != 0 ? this.listPhotoItems[0].url : '';
    return SeoService.getMetaInfoProductPage(name, url);
  },
  data: () => ({
    tabModel: null,
    noItemImage: require('@/assets/banner/no-product.png'),
    subProductItems: [] as ProductItem[],
    relatedProductItems: [] as ProductItem[],
    anotherProductItems: [] as ProductItem[],
    mainProduct: {} as ProductItem,
    allProduct: [] as ProductItem[],
    largestSaleOffItem: {} as ProductItem,
    cheapestItem: {} as ProductItem,
    listPhotoItems: [] as any[],
    averagePrice: 0 as number,
    anotherCategoryId: '' as string,
    isLoadedFinish: false,
    encodedSlugId: '',
    filterByProductAnotherAgency: [
      { id: 'discount', name: 'Giảm giá', isSelected: false },
      { id: 'review', name: 'Đánh giá', isSelected: false },
      { id: 'trusted', name: 'Store uy tín', isSelected: false },
    ],
    sortByProductAnotherAgency: [
      { id: 'discountRate', name: 'Giảm giá', isSelected: false },
      { id: 'price', name: 'Giá', isSelected: true },
      { id: 'countReview', name: 'Đánh giá', isSelected: false },
      { id: 'stock', name: 'Tồn kho', isSelected: false },
    ],
  }),
  computed: {
    isHasSortBy(): boolean {
      return this.sortByProductAnotherAgency.find((i) => i.isSelected) ? true : false;
    },
    isHasFilterBy(): boolean {
      return this.filterByProductAnotherAgency.find((i) => i.isSelected) ? true : false;
    },
    filterProductItems(): ProductItem[] {
      let productItems = this.allProduct;
      for (const i of this.filterByProductAnotherAgency) {
        if (i.id == 'discount' && i.isSelected) productItems = productItems.filter((item) => !!item.discountRate);
        if (i.id == 'review' && i.isSelected) productItems = productItems.filter((item) => !!item.countReview);
        if (i.id == 'trusted' && i.isSelected)
          productItems = productItems.filter((item) => !!item.shopItem && (item as any).shopItem.shop_is_official == 1);
      }
      console.log('productItems', productItems, this.filterByProductAnotherAgency);
      return productItems;
    },
    slugId(): string {
      return this.$route.params['slugId'];
    },
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    categoryId(): string {
      return this.mainProduct ? this.mainProduct.PK : '';
    },
    categoryItems(): any[] {
      return this.$store.getters.categoryItems;
    },
    getCategory(): any {
      return this.$store.getters.categoryItems.filter((item: any) => item.SK == this.categoryId)[0] || [];
    },
    getDomainItems(): any[] {
      return this.$store.getters.domainItems;
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
          text: this.categoryId ? `${CategoryService.code2category(this.categoryId)}` : '',
          to: `/category/${this.categoryId ? this.categoryId.toLowerCase() : ''}`,
          disabled: false,
          exact: true,
        },
        {
          text: CategoryService.upperCaseFirstLetter(`${(this as any).mainProduct.cleanName || ''}`),
          to: `#`,
          disabled: true,
          exact: true,
        },
      ];
    },
  },
  async created() {
    console.log('ProductDetailPage component is created');
    window.scrollTo({ top: 0, left: 0 });
    await this.initialize();
    this.allProduct = [this.mainProduct, ...this.subProductItems];
    this.handleChangeSorter(this.sortByProductAnotherAgency.find((i) => i.isSelected));
    this.cheapestItem = JSON.parse(JSON.stringify(this.allProduct[0]));
  },
  watch: {
    async slugId() {
      if (this.slugId) await this.initialize();
    },
    async categoryItems() {
      if (this.categoryItems && this.categoryItems.length != 0 && !this.isLoadedFinish) {
        this.isLoadedFinish = true;
      }
    },
  },
  methods: {
    transitionToCompare(tab: any) {
      if (tab == -1) {
        window.scrollTo({ top: -100, left: 0, behavior: 'smooth' });
      } else {
        this.tabModel = tab;
        (document as any)
          .getElementById('detail-rating-item')
          .scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
      }
    },
    handleChangeFilter(item: any) {
      const filter = this.filterByProductAnotherAgency.find((i) => item.id == i.id);
      if (filter) filter.isSelected = !filter.isSelected;
    },
    handleChangeSorter(item: any) {
      this.sortByProductAnotherAgency = this.sortByProductAnotherAgency.map((i) => ({
        ...i,
        isSelected: false,
      }));
      const filter = this.sortByProductAnotherAgency.find((i) => item.id == i.id);
      if (filter) {
        filter.isSelected = !filter.isSelected;

        this.allProduct = this.allProduct.sort((itemA: ProductItem, itemB: ProductItem) => {
          if (Object.keys(itemA).includes(filter.id) && Object.keys(itemB).includes(filter.id)) {
            const valueA = (itemA as any)[filter.id] || 0;
            const valueB = (itemB as any)[filter.id] || 0;
            if (['price'].includes(filter.id)) {
              // ascending
              if (valueA > valueB) return 1;
              else return -1;
            } else if (['discountRate', 'stock', 'countReview'].includes(filter.id)) {
              // descending
              if (valueA < valueB) return 1;
              else return -1;
            }
          }
          return 1;
        });
      }
    },
    filterConfidentItems(items: ProductItem[]): ProductItem[] {
      const allPrice = items.map((i) => i.price);
      const averagePrice = Math.round(
        (allPrice.reduce((a: number, b: number) => a + b, 0) / allPrice.length) as number
      );
      return items.filter((i: ProductItem) => i.price / averagePrice < 2);
    },
    async initialize() {
      const loading = this.$loading.show();
      try {
        const parts = this.slugId.split('.');
        const response = await ProductService.queryItemById({
          id: `${parts[parts.length - 2]}.${parts[parts.length - 1]}`,
          isHasChild: true,
        });
        if (response?.mainItem && response.childItems) {
          this.mainProduct = response.mainItem as ProductItem;
          this.subProductItems = JSON.parse(JSON.stringify(response.childItems)).sort(
            (itemA: ProductItem, itemB: ProductItem) => {
              if (itemA.price < itemB.price) return -1;
              else return 1;
            }
          );

          const allPrice = response.childItems
            .concat(response.mainItem)
            .map((item: ProductItem) => item.price) as number[];
          this.averagePrice = Math.round(
            (allPrice.reduce((a: number, b: number) => a + b, 0) / allPrice.length) as number
          );

          const listPhotoItems = Array.from(
            new Set(
              response.childItems
                .concat(response.mainItem)
                .map((item: ProductItem) => item.listImage)
                .flat(1)
            )
          );
          this.listPhotoItems = listPhotoItems.slice(0, 6).map((imageUrl: string) => ({
            name: imageUrl || '',
            url: imageUrl || '',
            selected: false,
          }));

          const saleOffSortedItems = JSON.parse(JSON.stringify(response.childItems.concat(response.mainItem))).sort(
            (itemA: ProductItem, itemB: ProductItem) => {
              if (itemA.discountRate < itemB.discountRate) return 1;
              else return -1;
            }
          );
          this.largestSaleOffItem = saleOffSortedItems[0] as ProductItem;
        }
      } catch (err) {
        console.log(err);
        this.$router.replace('/');
      }
      loading.hide();
    },
  },
});
</script>

<style lang="scss">
.product-detail-slug-page {
  .filter-product-another-agency {
    position: absolute;
    right: 68px;
    top: -55px;
    z-index: 10;
  }
  .sort-by-product-another-agency-mobile {
    position: absolute;
    right: 10px;
    top: -65px;
    z-index: 10;
  }

  .sort-by-product-another-agency {
    position: absolute;
    right: 20px;
    top: -55px;
    z-index: 10;
  }

  .transition-span {
    position: fixed;
    top: 170px;
    z-index: 100;
    right: 55px;
  }

  .transition-span-mobile {
    position: fixed;
    bottom: 90px;
    z-index: 300;
    right: 15px;
  }
  .v-label {
    font-size: 12px !important;
  }
}
</style>

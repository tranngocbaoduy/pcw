<template>
  <div class="product-user-page" v-if="mainProduct">
    <BreadCrumbs class="mt-4" :breadcrumbs="breadcrumbs" />
    <v-row class="mt-4 mb-8" no-gutters>
      <v-col sm="12" md="5" cols="12" class="px-4" v-if="listPhotoItems && !isMobile">
        <ProductPhoto :listPhotoItems="listPhotoItems" />
      </v-col>
      <v-col sm="12" md="7" cols="12" class="px-4">
        <ProductInfo
          :item="mainProduct"
          :averagePrice="averagePrice"
          :subProductItems="subProductItems"
          :largestSaleOffItem="largestSaleOffItem"
          :domain="mainProduct.domain"
        />
      </v-col>
      <v-col sm="12" md="12" cols="12" class="px-4">
        <v-card color="white" class="mt-5 rounded-0 px-3" elevation="0" v-if="mainProduct.content">
          <v-card-title class="pb-3">{{ $t('content') }}:</v-card-title>
          <v-card-text>{{ mainProduct.content }} </v-card-text>
        </v-card>
      </v-col>
      <v-col sm="12" md="12" cols="12" class="pa-4" v-if="listPhotoItems && isMobile">
        <ProductPhotoMobile :domain="mainProduct.domain" :listPhotoItems="listPhotoItems" />
      </v-col>
    </v-row>

    <v-divider> </v-divider>

    <ProductAnotherAgency
      v-if="subProductItems && subProductItems.length != 0"
      :relatedItems="subProductItems"
      :shopName="$t('anotherAgency')"
    />
    <!-- <ListProductRelated
      v-if="relatedProductItems && relatedProductItems.length != 0"
      :relatedItems="relatedProductItems"
      :categoryId="this.categoryId"
      :shopName="$t('similarProduct')"
    />
    <ListProductRelated
      v-if="anotherProductItems && anotherProductItems.length != 0"
      :relatedItems="anotherProductItems"
      :categoryId="this.anotherCategoryId"
      :shopName="$t('anotherProduct')"
    /> -->
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BreadCrumbs from '@/components/common/BreadCrumbs.vue';
import ProductPhoto from '@/components/pages/common/product-detail-page/ProductPhoto.vue';
import ProductPhotoMobile from '@/components/pages/common/product-detail-page/ProductPhotoMobile.vue';
import ProductInfo from '@/components/pages/common/product-detail-page/ProductInfo.vue';
import ProductAnotherAgency from '@/components/pages/common/product-detail-page/ProductAnotherAgency.vue';
// import ListProductRelated from '@/components/pages/common/product-detail-page/ListProductRelated.vue';

import base64url from 'base64url';
import CategoryService, { CategoryItem } from '@/api/category.service';
import ProductService, { ProductItem } from '@/api/product.service';

export default Vue.extend({
  name: 'Body',
  props: ['isShowMenu'],
  components: {
    BreadCrumbs,
    ProductPhoto,
    ProductPhotoMobile,
    ProductInfo,
    ProductAnotherAgency,
    // ListProductRelated,
  },
  data: () => ({
    subProductItems: [] as ProductItem[],
    relatedProductItems: [] as ProductItem[],
    anotherProductItems: [] as ProductItem[],
    mainProduct: {} as ProductItem,
    largestSaleOffItem: {} as ProductItem,
    listPhotoItems: [] as any[],
    averagePrice: 0 as number,
    anotherCategoryId: '' as string,
    isLoadedFinish: false,
    encodedSlugId: '',
  }),
  computed: {
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
          text: this.$t(`category.${CategoryService.code2category(this.categoryId)}`),
          to: `/category/${this.categoryId ? this.categoryId.toLowerCase() : ''}`,
          disabled: false,
          exact: true,
        },
        {
          text: CategoryService.upperCaseFirstLetter(`${(this as any).mainProduct.name || ''}`),
          to: `/${this.slugId}`,
          disabled: true,
          exact: true,
        },
      ];
    },
  },
  async created() {
    console.log('ProductDetailPage component is created', this.slugId);
    window.scrollTo({ top: 0, left: 0 });
    await this.initialize();
  },
  watch: {
    async slugId() {
      if (this.slugId) await this.initialize();
    },
    async categoryItems() {
      if (this.categoryItems && this.categoryItems.length != 0 && !this.isLoadedFinish) {
        await this.loadAnotherProductItems();
        this.isLoadedFinish = true;
      }
    },
  },
  methods: {
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
        this.encodedSlugId = base64url.encode(`/${this.slugId}`);
        const response = await ProductService.queryItemBySlugId({
          ENCODED_SLUG_ID: this.encodedSlugId,
          isHasChild: true,
        });

        this.mainProduct = response.mainItem as ProductItem;
        console.log('this.mainProduct', this.mainProduct);
        this.subProductItems = JSON.parse(JSON.stringify(response.childItems.concat(response.mainItem))).sort(
          (itemA: ProductItem, itemB: ProductItem) => {
            if (itemA.discountRate < itemB.discountRate) return 1;
            else return -1;
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
        // this.loadRelatedProductItems();
        // if (this.categoryItems && this.categoryItems.length != 0 && !this.isLoadedFinish) {
        //   await this.loadAnotherProductItems();
        //   this.isLoadedFinish = true;
        // }

        const saleOffSortedItems = JSON.parse(JSON.stringify(response.childItems.concat(response.mainItem))).sort(
          (itemA: ProductItem, itemB: ProductItem) => {
            if (itemA.discountRate < itemB.discountRate) return 1;
            else return -1;
          }
        );
        this.largestSaleOffItem = saleOffSortedItems[0] as ProductItem;
      } catch (err) {
        console.log(err);
      }
      loading.hide();
    },
    async loadRelatedProductItems() {
      this.relatedProductItems = (await ProductService.queryItemByCategoryId(
        this.categoryId.toUpperCase(),
        6
      )) as ProductItem[];
    },
    async loadAnotherProductItems() {
      console.log(this.categoryItems, this.categoryId);
      const category = this.categoryItems.find((item: CategoryItem) => item.SK != this.categoryId.toUpperCase());
      if (category) {
        this.anotherCategoryId = category.SK;
        this.anotherProductItems = (await ProductService.queryItemByCategoryId(category.SK, 6)) as ProductItem[];
      }
    },
  },
});
</script>

<style lang="scss"></style>

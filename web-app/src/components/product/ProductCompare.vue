<template>
  <div
    class="product-compare-item py-2"
    :class="isOdd ? 'white' : 'bg-primary-color-0'"
    style="flex-grow: 0 0 auto !important"
    v-if="mainProduct && Object.keys(mainProduct).length != 0"
  >
    <v-row class="ma-0 pa-0" no-gutters>
      <!-- <v-col
        sm="12"
        md="12"
        cols="12"
        class="pa-0"
        v-if="listPhotoItems && !isMobile"
        style="background-color: transparent"
      >
        <ProductPhotoMobile :domain="mainProduct.domain" :listPhotoItems="listPhotoItems" />
      </v-col> -->
      <v-col sm="12" md="12" cols="12" class="pa-0">
        <v-card elevation="0" class="rounded-0 px-4" style="background-color: transparent">
          <v-card-title class="font-size-14 title-product font-weight-2 mb-0 px-0 pb-0 line-height-28 d-inline-block">
            <span class="primary-color-2">{{ mainProduct.brand || '' }} </span> -
            <span>{{ mainProduct.name }}</span>
          </v-card-title>
          <v-card-text class="font-size-12 font-weight-2 pl-0 pb-4">
            <div class="d-flex justify-start align-center py-2">
              <RatingItem class="hover-custom-link py-1 pr-4" :itemRating="mainProduct.itemRating" :isDisplay="true" />

              <div class="my-0 px-0" v-if="mainProduct.voucherInfo">
                <div class="font-size-12 voucher-info">{{ mainProduct.voucherInfo.label }}</div>
              </div>
            </div>
            <div class="d-flex justify-start align-center">
              <div class="mr-3 ml-0">
                <span>Đánh giá: </span>
                <span class="font-weight-3 primary-color-2">{{
                  mainProduct.itemRating.rating_count.reduce((partialSum, a) => partialSum + a, 0) || ''
                }}</span>
              </div>
              <v-divider vertical style="width: 10px" class="my-2" />
              <div class="mx-3">
                <span>Đã bán: </span>
                <span class="font-weight-3 primary-color-2">{{ mainProduct.historicalSold || '' }}</span>
              </div>
              <v-divider vertical style="width: 10px" class="my-2" />
              <div class="mx-3">
                <span>Thích: </span>
                <span class="font-weight-3 primary-color-2">{{ mainProduct.likedCount || '' }}</span>
              </div>
            </div>
          </v-card-text>

          <div class="my-0 pl-2 pb-4">
            <v-row align="center" v-if="mainProduct.listPrice != mainProduct.price">
              <div class="font-size-14 font-weight-1 line-through pr-4 pl-0">
                {{ mainProduct.listPrice | formatPrice }}đ
              </div>
            </v-row>
            <v-row align="center">
              <div class="font-size-24 font-weight-3 mr-7 primary-color-1">{{ mainProduct.price | formatPrice }}đ</div>
              <div
                style="border: red 1px solid"
                v-if="mainProduct.listPrice != mainProduct.price"
                class="pa-1 rounded-sm rounded-0 font-size-12 font-weight-2 text-right ml-5 red white--text elevation-1 mr-2"
              >
                {{ mainProduct.discountRate }}% giảm
              </div>
              <span
                :class="mainProduct.domain ? mainProduct.domain.toLowerCase() : ''"
                class="rounded-md font-size-12 pa-1 py-0 font-weight-2 text-right elevation-1"
              >
                {{ mainProduct.domain }}
              </span>
            </v-row>
          </div>
          <v-card-actions class="pa-0">
            <v-btn
              @click="goToPlatform()"
              class="white--text rounded-lg my-0"
              color="#1859db"
              height="37px"
              width="100%"
              >{{ 'Mua' }}</v-btn
            >

            <span v-if="mainProduct.stock" class="font-size-12 ml-4"
              >Còn <span class="font-weight-bold">{{ mainProduct.stock }} </span>
            </span>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col sm="12" md="12" cols="12" class="px-4">
        <v-card color="white" class="mt-5 rounded-0 px-3" elevation="0" v-if="mainProduct.content">
          <v-card-title class="pb-3">{{ $t('content') }}:</v-card-title>
          <v-card-text>{{ mainProduct.content }} </v-card-text>
        </v-card>
      </v-col>
      <v-col sm="12" md="12" cols="12" class="pa-4" v-if="listPhotoItems && isMobile"> </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import ProductPhotoMobile from '@/components/pages/common/product-detail-page/ProductPhotoMobile.vue';
import RatingItem from '@/components/common/rating/RatingItem.vue';
import CategoryService from '@/api/category.service';

export default Vue.extend({
  name: 'ProductCompare',
  props: ['mainProduct', 'isOdd'],
  components: {
    // ProductPhotoMobile,
    RatingItem,
  },
  data: () => ({
    noItemImage: require('@/assets/banner/no-product.png'),
  }),
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    categoryId(): string {
      return this.mainProduct ? this.mainProduct.PK : '';
    },
    categoryItems(): any[] {
      return this.$store.getters.categoryItems;
    },
    listPhotoItems(): [] {
      return this.mainProduct.listImage;
    },
  },
  async created() {
    console.log('ProductDetailPage component is created');
    window.scrollTo({ top: 0, left: 0 });
    await this.initialize();
  },
  watch: {},
  methods: {
    async initialize() {},

    goToPlatform() {
      window.open(this.getURLAccessTrade(), '_blank');
    },
    getURLAccessTrade(): string {
      return `${process.env.VUE_APP_BASE_ACCESS_TRADE_URL}?url=${this.mainProduct.url}`;
    },
  },
  filters: {
    reduceText: function (text: string, max: number) {
      return CategoryService.upperCaseFirstLetter(text && text.length > max ? text.slice(0, max - 2) + '...' : text);
    },
    formatPrice(value: number) {
      // const val = (value / 1).toFixed(0).replace('.', ',');
      return value ? value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') : '';
    },
  },
});
</script>

<style lang="scss">
.product-compare-item {
  min-width: 340px !important;
  max-width: 340px !important;
  max-height: 540px !important;
  .voucher-info {
    border: 0.5px #ca3e29 solid;
    background-color: #f9f9f9;
    color: #ca3e29;
    border-radius: 2px;
    padding: 8px;
    margin: 0;
    display: inline;
  }
  .title-product {
    line-height: 2.5em;
    max-height: 97px;
    height: 2.5em; /* height is 2x line-height, so two lines will display */
    overflow: hidden; /* prevents extra lines from being visible */
    // text-overflow: ellipsis;
    // white-space: nowrap;
  }
}
</style>

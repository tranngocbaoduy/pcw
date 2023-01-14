<template>
  <div class="product-info" v-if="item">
    <v-card-title class="font-size-22 font-weight-2 mb-2 px-0 pb-0 line-height-30 d-inline-block">
      <span
        :class="domain ? domain.toLowerCase() : ''"
        style="border-radius: 2px !important"
        class="rounded-0 font-size-16 pa-1 mb-2 mr-3 font-weight-2 text-right elevation-0"
      >
        {{ item.representDomainName }}
      </span>
      <span class="primary-color-2 font-size-22">{{ item.brand || '' }} </span> -
      <span class="font-size-20">{{ item.name | reduceText(500) }}</span>
    </v-card-title>
    <!-- <v-card-text class="font-size-14 font-weight-2 pl-0 pb-4">
      <div class="d-flex justify-start align-center">
        <RatingItem class="hover-custom-link py-2 pr-4" :itemRating="item.itemRating" :isDisplay="true" />
        <v-divider vertical style="width: 10px" class="my-2" />
        <div :class="isMobile ? 'mx-2' : 'mx-3'">
          <span>Đánh giá: </span>
          <span class="font-weight-3 primary-color-2">{{
            item.itemRating.rating_count.reduce((partialSum, a) => partialSum + a, 0) || 0
          }}</span>
        </div>
        <v-divider vertical style="width: 10px" class="my-2" />
        <div :class="isMobile ? 'mx-2' : 'mx-3'">
          <span>Đã bán: </span>
          <span class="font-weight-3 primary-color-2">{{ item.historicalSold || 0 }}</span>
        </div>
        <v-divider vertical style="width: 10px" class="my-2" />
        <div :class="isMobile ? 'mx-2' : 'mx-3'">
          <span>Thích: </span>
          <span class="font-weight-3 primary-color-2">{{ item.likedCount || 0 }}</span>
        </div>
      </div>
    </v-card-text> -->

    <div class="my-0 pl-0 pb-4">
      <v-row align="center" no-gutters>
        <div class="font-size-16 font-weight-1 line-through pr-0 pl-1 mr-3" v-if="item.listPrice != item.price">
          {{ item.listPrice | formatPrice }}đ
        </div>
        <div class="font-size-28 font-weight-3 mr-2 primary-color-1">{{ item.price | formatPrice }}đ</div>
        <div
          v-if="item.listPrice != item.price"
          class="pa-1 rounded-md font-size-14 font-weight-2 text-right ml-5 elevation-0 mr-2 discount-rate"
        >
          {{ item.discountRate || 0 }}% giảm
        </div>
      </v-row>
    </div>
    <div class="my-0 px-0 pb-4 py-2" v-if="item.voucherInfo">
      <div class="font-size-14 voucher-info">{{ item.voucherInfo.label }}</div>
    </div>
    <div class="properties pt-5 px-4" v-show="isShowDetail">
      <div>
        <v-card-text class="font-size-12 font-weight-2" v-for="propertyItem in propertyItems" :key="propertyItem.name">
          <v-row align="center">
            <v-icon class="mr-2" size="25px"> mdi-{{ propertyItem.icon }} </v-icon>
            <div>{{ propertyItem.name | reduceText(50) }}</div>
          </v-row>
        </v-card-text>
      </div>
      <div class="font-weight-2 font-size-14 float-right">
        <span> {{ $t('information') }} </span>
        <v-icon size="24px">mdi-chevron-right</v-icon>
      </div>
    </div>
    <v-card-actions class="pa-0">
      <v-btn
        @click="goToPlatform(item)"
        class="white--text rounded-lg my-2 text-capitalize"
        color="#1859db"
        height="42px"
        width="100px"
        >{{ $t('buyNow') }}
      </v-btn>
      <span v-if="item.stock" class="font-size-14 ml-4">
        Kho: <span class="font-weight-bold">{{ item.stock }} </span> sản phẩm
      </span>
    </v-card-actions>
    <v-card color="white" class="mt-5 rounded-0 px-3" elevation="0">
      <v-card-title class="pb-3 d-flex justify-space-between align-center">
        <div class="hover-custom-link">{{ $t('note') }}:</div>
      </v-card-title>

      <v-card-text class="font-size-14 font-weight-1">
        <ul class="line-height-24 font-size-14 font-weight-2 mr-7" :class="isMobile ? ' pa-0' : ''">
          <li class="py-1">
            {{ $t('The cheapest product is on sale at') }}

            <span @click="goToPlatform(cheapestItem)" class="primary-color-1 hover-custom-link">{{
              cheapestItem && cheapestItem.domain ? cheapestItem.domain : ''
            }}</span>
          </li>
          <li class="py-1" v-if="largestSaleOffItem.discountRate != 0">
            {{ $t('The store with the most discounts is') }}
            <span @click="goToPlatform(largestSaleOffItem)" class="primary-color-1 hover-custom-link">
              <span class="primary-color-1">{{ largestSaleOffItem.domain }}</span>
            </span>
            {{ $t('up to') }}
            <span class="primary-color-2 discount-rate px-1"> {{ largestSaleOffItem.discountRate }}% </span>
            <span class="px-1">{{ ' với giá ưu đãi' }}</span>
            <span class="primary-color-1"> {{ largestSaleOffItem.price | formatPrice }}đ</span>
          </li>
          <li class="py-1">
            {{ $t('Average product price') }}
            <span class="primary-color-1">
              {{ averagePrice | formatPrice }}đ ~

              <v-icon v-if="isLargerThanAverage" class="mb-2 font-size-16 font-weight-bold" color="red"
                >mdi-arrow-top</v-icon
              >
              <v-icon v-else class="mb-1 mr-0 font-size-16 font-weight-bold" color="green">mdi-arrow-up</v-icon>
              {{ percentDiffPrice ? `${percentDiffPrice}%` : '0' }}
              <!-- <span class="primary-color-2"> {{ reviewDiffPrice }}</span> -->
            </span>
          </li>
        </ul>
      </v-card-text>
    </v-card>
  </div>
</template>

<script lang="ts">
import CategoryService from '@/api/category.service';
import RatingItem from '@/components/common/rating/RatingItem.vue';
import Vue from 'vue';
import { ProductItem } from '@/api/product.service';

export default Vue.extend({
  props: ['item', 'averagePrice', 'subProductItems', 'largestSaleOffItem', 'domain', 'cheapestItem'],
  // components: { RatingItem },
  data: () => ({
    isShowDetail: false,
    propertyItems: [
      { name: '6,7", Super Retina XDR, AMORLED, 2778 x 1284 Pixel', icon: 'cellphone' },
      { name: '12.0 MP + 12.0 MP + 12.0 MP', icon: 'opera' },
      { name: '12.0 MP', icon: 'camera' },
      { name: 'A14 Bionic', icon: 'presentation' },
      { name: '128GB', icon: 'inbox' },
    ],
  }),
  created() {},
  filters: {
    reduceText: function (text: string, max: number) {
      return CategoryService.upperCaseFirstLetter(text && text.length > max ? text.slice(0, max - 2) + '...' : text);
    },
    formatPrice(value: number) {
      // const val = (value / 1).toFixed(0).replace('.', ',');
      return value ? value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') : '';
    },
  },
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    isLargerThanAverage(): boolean {
      return parseInt(this.item.price) > parseInt(this.averagePrice);
    },
    percentDiffPrice(): number {
      return this.item.price < this.averagePrice
        ? 100 - Math.round((this.item.price / this.averagePrice) * 100)
        : 100 - Math.round((this.averagePrice / this.item.price) * 100);
    },
    reviewDiffPrice() {
      let res = '';
      if (this.percentDiffPrice > 20) res = this.$t('Huge price gap').toString();
      else if (this.percentDiffPrice > 10) res = this.$t('Significant price gap').toString();
      else if (this.percentDiffPrice > 1) res = this.$t('Need consider').toString();
      return res ? `- ${res}` : '';
    },
  },
  methods: {
    goToPlatform(item: ProductItem) {
      window.open(item.baseUrl, '_blank');
    },
    // getURLAccessTrade(item?: any): string {
    //   return `${process.env.VUE_APP_BASE_ACCESS_TRADE_URL}?url=${item && item.url ? item.url : this.item.url}`;
    // },
  },
});
</script>

<style lang="scss">
.product-info {
  .properties {
    height: 224px;
    background-color: #f9f9f9;
  }
  .voucher-info {
    border: 0.5px #ca3e29 solid;
    background-color: #f9f9f9;
    color: #ca3e29;
    border-radius: 2px;
    padding: 8px;
    margin: 0;
    display: inline;
  }

  .discount-rate {
    color: #ca3e29;
    z-index: 2;
    border: 1px solid #ca3e29;
    border-radius: 1px !important;
    line-height: 14px !important;
  }
}
</style>

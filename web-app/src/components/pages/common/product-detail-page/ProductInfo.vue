<template>
  <div class="product-info" v-if="item">
    <v-card-title class="font-size-22 font-weight-2 mb-3 px-0 pb-0 line-height-30">{{
      item.name | reduceText(500)
    }}</v-card-title>
    <v-card-text class="font-size-12 font-weight-2 pl-2">
      <v-row>
        <v-rating class="" :value="5" color="yellow" dense half-increments readonly size="15"></v-rating>
        <div class="mx-3">
          <span>{{ $t('brand') }}: </span>
          <span class="font-weight-3 primary-color-2">{{ item.brand || '' }}</span>
        </div>
      </v-row>
    </v-card-text>

    <v-card-text class="ma-0 pa-0 primary-color-4">
      <v-row align="center" no-gutters>
        <div class="mr-6">{{ $t('freeShip') }}</div>
        <div>{{ $t('genuine') }}</div>
      </v-row>
    </v-card-text>

    <v-card-text class="my-2 py-4 pl-2">
      <v-row align="center">
        <div class="font-size-30 font-weight-3 mr-7 primary-color-1">{{ item.price | formatPrice }}đ</div>
        <div class="font-size-16 font-weight-1 line-through">{{ item.listPrice | formatPrice }}đ</div>
        <div style="border: red 1px solid" class="px-2 rounded-lg font-size-14 font-weight-2 text-right ml-5 red--text">
          {{ item.discountRate }}%
        </div>
      </v-row>
    </v-card-text>
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
      <a :href="item.url" target="_blank">
        <v-btn class="white--text rounded-lg my-2" color="#1859db" height="42px" width="100%">{{ $t('buyNow') }}</v-btn>
      </a>
    </v-card-actions>
    <v-card color="white" class="mt-5 rounded-lg px-3">
      <v-card-title class="pb-3">{{ $t('note') }}:</v-card-title>

      <v-card-text class="font-size-14 font-weight-1">
        <ul class="font-size-14 font-weight-3 mr-7 line-height-24" :class="isMobile ? ' pa-0' : ''">
          <li class="py-1">
            {{ $t('The cheapest product is on sale at') }}
            <a :href="item.url" target="_blank">
              <span class="primary-color-1">{{ item && item.domain ? item.domain : '' }}</span>
            </a>
          </li>
          <li class="py-1" v-if="largestSaleOffItem.discountRate != 0">
            {{ $t('The store with the most discounts is') }}
            <a :href="largestSaleOffItem.url" target="_blank">
              <span class="primary-color-1">{{ largestSaleOffItem.domain }}</span>
            </a>
            {{ $t('up to') }}
            <span class="primary-color-2"> {{ largestSaleOffItem.discountRate }}% </span>-
            <span class="primary-color-1"> {{ largestSaleOffItem.price | formatPrice }}đ</span>
          </li>
          <li class="py-1">
            {{ $t('Sold in stores') }}: <span class="primary-color-1"> {{ subProductItems.length + 1 }} </span>
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
              <span class="primary-color-2"> {{ reviewDiffPrice }}</span>
            </span>
          </li>
        </ul>
      </v-card-text>
    </v-card>

    <v-card color="white" class="mt-5 rounded-lg px-3" v-if="item.content">
      <v-card-title class="pb-3">{{ $t('content') }}:</v-card-title>
      <v-card-text>{{ item.content }} </v-card-text>
    </v-card>
  </div>
</template>

<script lang="ts">
import CategoryService from '@/api/category.service';
import Vue from 'vue';

export default Vue.extend({
  props: ['item', 'averagePrice', 'subProductItems', 'largestSaleOffItem'],
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
  methods: {},
});
</script>

<style lang="scss">
.product-info {
  .properties {
    height: 224px;
    background-color: #f9f9f9;
  }
}
</style>

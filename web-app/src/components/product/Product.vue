<template>
  <v-hover v-slot="{ hover }">
    <v-card
      :elevation="hover ? 12 : 2"
      :loading="loading"
      class="product border-radius-8 box-sizing pb-5 mb-4 mx-2 py-auto"
      min-height="420"
      max-height="420"
    >
      <v-row class="px-2 pb-0 pt-8 ma-0 py-0">
        <span class="domain px-3 font-size-16 font-weight-2 text-right">
          {{ item.domain }}
        </span>
        <span v-if="item.listPrice != item.price" class="discount-rate px-3 font-size-16 font-weight-2 text-right">
          {{ item.discountRate }}%
        </span>

        <v-img
          class="product-img text-center ma-auto"
          min-height="220"
          :src="item.listImage[0] || require('../../assets/f201f0a8baee2ef5ee2adef6ac755c72.jpg')"
          :lazy-src="item.listImage[0] || require('../../assets/f201f0a8baee2ef5ee2adef6ac755c72.jpg')"
        >
        </v-img
      ></v-row>

      <v-card-title class="pa-0 mx-3 mt-0 mb-n3" style="">
        <v-row align="center">
          <v-col cols="9 pr-0">
            <div class="font-size-14 line-height-20">
              <span class="primary-color-2 font-weight-bold">{{ itemBrand }} </span>-
              {{ item.name | reduceText(40 - itemBrand.length - 3) }}
            </div>
          </v-col>
          <v-col cols="3 pr-2 pt-0">
            <v-btn class="float-right" icon>
              <v-icon size="16"> mdi-heart-outline </v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-title>

      <v-row class="pa-0 mx-3 mb-0 text-center py-0" align="center" no-gutters>
        <v-col cols="12" class="ma-0 pa-0 font-size-16 font-weight-3 text-left primary-color-1 line-height-26">
          {{ item.price | formatPrice }}đ
        </v-col>
      </v-row>
      <v-row class="pa-0 mx-3 my-0 text-center py-0" align="center" no-gutters v-if="item.listPrice != item.price">
        <v-col cols="9" class="ma-0 pa-0 primary-color-4 text-left font-size-12 font-weight-1 old-price line-height-22"
          >{{ item.listPrice | formatPrice }}đ
        </v-col>
      </v-row>

      <!-- <v-card-text class="mx-3 py-0 ma-0"> -->
      <v-row align="center" class="mx-3 pa-0 ma-0" no-gutters>
        <v-col cols="6" class="ma-0 pa-0">
          <v-rating
            class="product-rate ml-n1 line-height-18 pa-0"
            :value="getRatingAverage"
            color="#FFA200"
            dense
            half-increments
            readonly
            size="13"
          ></v-rating>
        </v-col>
      </v-row>
      <v-row align="center" class="mx-3 pa-0 ma-0" no-gutters>
        <v-col cols="12" class="ma-0 pa-0">
          <div class="font-size-12 font-weight-1 pa-0 ma-0 text-left line-height-20">
            <span class="font-weight-3 primary-color-3"> {{ `${item.listChildId.length} ${$t('in stores')}` }}</span
            ><br />
            <span class="line-height-20 font-size-12">{{ $t('freeShip') }}</span>
          </div>
        </v-col>
      </v-row>

      <!-- </v-card-text> -->
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import CategoryService from '@/api/category.service';
import Vue from 'vue';

export default Vue.extend({
  props: ['item'],
  data: () => ({
    loading: false,
    selection: 1,
  }),
  computed: {
    getRatingAverage(): number {
      return 5;
    },
    itemBrand(): string {
      return CategoryService.upperCaseFirstLetter(this.item.brand);
    },
  },

  filters: {
    reduceText: function (text: string, max: number) {
      return CategoryService.upperCaseFirstLetter(text && text.length > max ? text.slice(0, max - 2) + '...' : text);
    },
    formatPrice(value: string) {
      return value ? value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') : '';
    },
  },

  methods: {
    reserve() {
      this.loading = true;
      setTimeout(() => (this.loading = false), 2000);
    },
  },
});
</script>

<style lang="scss" scoped>
@import '@/assets/scss/Common.scss';
@import '@/assets/scss/LineHeight.scss';
@import '@/assets/scss/FontSize.scss';
.product {
  .domain {
    background: #1859db !important;
    border: #1859db 1px solid;
    color: white;
    position: absolute;
    left: 0px;
    top: 0px;
    z-index: 100;
    border-radius: 8px 0px 8px 0px !important;
  }
  .discount-rate {
    border: #ca3e29 1px solid;
    background-color: #ca3e29;
    color: white;
    position: absolute;
    right: 0px;
    top: 0px;
    z-index: 100;
    border-radius: 0px 8px 0px 8px !important;
  }

  .old-price {
    text-decoration: line-through !important;
    text-decoration-color: #607d8b !important;
    text-decoration-style: solid 1px !important;
  }
}
</style>

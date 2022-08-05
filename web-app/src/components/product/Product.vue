<template>
  <v-hover v-slot="{ hover }">
    <v-card :loading="loading" style="" class="product rounded-0 py-2 my-0">
      <v-row class="px-2 pb-0 pt-8 ma-0 py-0" style="height: 240px">
        <span :class="item.domain.toLowerCase()" class="domain px-3 font-size-16 font-weight-2 text-right">
          {{ item.domain }}
        </span>
        <v-img
          :class="hover ? 'mt-2' : 'mt-4'"
          class="product-img text-center"
          style="width: 191px; height: 191px"
          contain
          :style="hover ? 'z-index:4' : ''"
          :src="item.listImage[0] || require('../../assets/f201f0a8baee2ef5ee2adef6ac755c72.jpg')"
          :lazy-src="item.listImage[0] || require('../../assets/f201f0a8baee2ef5ee2adef6ac755c72.jpg')"
        >
        </v-img
      ></v-row>

      <v-card-title class="pa-0 mx-3 mt-0 mb-n3" style="">
        <v-row align="center">
          <v-col cols="9 pr-0">
            <div class="font-size-14 line-height-20 title-product">
              <span class="primary-color-2 font-weight-bold">{{ itemBrand }} </span>- {{ item.name }}
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
        <v-col cols="8" class="ma-0 pa-0 primary-color-4 text-left">
          <span class="font-size-12 font-weight-1 old-price line-height-22"> {{ item.listPrice | formatPrice }}đ</span>
          <span class="discount-rate px-1 font-size-14 font-weight-2 text-right"> {{ item.discountRate }}% </span>
        </v-col>

        <v-col cols="4" class="ma-0 pa-0">
          <div class="font-size-12 font-weight-1 pa-0 ma-0 text-right line-height-20">
            <span class="font-weight-3 primary-color-3"> {{ `${item.listChildId.length} ${$t('in stores')}` }}</span
            ><br />
          </div>
        </v-col>
      </v-row>
      <v-row class="pa-0 mx-3 my-0 text-center py-0" align="center" no-gutters>
        <v-col cols="7" class="ma-0 pa-0 font-size-16 font-weight-3 text-left primary-color-1 line-height-26">
          {{ item.price | formatPrice }}đ
        </v-col>
        <v-col cols="5" class="ma-0 pa-0 text-right">
          <v-rating
            class="product-rate line-height-18 pa-0"
            :value="getRatingAverage"
            color="#FFA200"
            dense
            half-increments
            readonly
            size="13"
          ></v-rating>
        </v-col>
      </v-row>

      <v-row align="center" class="mx-3 pa-0 ma-0" no-gutters> </v-row>
      <v-row align="center" class="mx-3 pa-0 ma-0" no-gutters> </v-row>
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
    attrs: {
      class: 'mb-6',
      boilerplate: true,
      elevation: 2,
    },
  }),
  computed: {
    getRatingAverage(): number {
      return 5;
    },
    itemBrand(): string {
      console.log(this.item);
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
  height: 100%;
  border: #cdcdcd 0.1px solid;
  box-shadow: none;
  .product-img {
    -webkit-transition: all 0.2s;
    -moz-transition: all 0.2s;
    -ms-transition: all 0.2s;
    -o-transition: all 0.2s;
    transition: all 0.2s;
  }
  .domain {
    position: absolute;
    left: 0px;
    top: 0px;
    z-index: 2;
    border-radius: 0px 0px 0px 0px !important;
  }
  .discount-rate {
    color: #ca3e29;
    z-index: 2;
  }

  .old-price {
    text-decoration: line-through !important;
    text-decoration-color: #607d8b !important;
    text-decoration-style: solid 1px !important;
  }
  .title-product {
    line-height: 1.5em;
    height: 3em; /* height is 2x line-height, so two lines will display */
    overflow: hidden; /* prevents extra lines from being visible */
    // text-overflow: ellipsis;
    // white-space: nowrap;
  }
}
</style>

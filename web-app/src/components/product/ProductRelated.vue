<template>
  <v-hover v-slot="{ hover }">
    <v-card
      :elevation="hover ? 12 : 2"
      max-width="250"
      :loading="loading"
      class="product border-radius-4 box-sizing pb-5 mb-4 mx-2"
    >
      <v-row class="px-2 pb-0 pt-3 ma-0">
        <span class="domain px-3 font-size-14 font-weight-2 text-right">
          {{ item.domain }}
        </span>
        <span v-if="item.listPrice != item.price" class="discount-rate px-3 font-size-14 font-weight-2 text-right">
          {{ item.discountRate }}%
        </span>

        <v-img
          class="product-img text-center"
          :src="item.listImage[0] || require('../../assets/f201f0a8baee2ef5ee2adef6ac755c72.jpg')"
          :lazy-src="item.listImage[0] || require('../../assets/f201f0a8baee2ef5ee2adef6ac755c72.jpg')"
          height="100%"
          width="100%"
        >
        </v-img
      ></v-row>

      <v-card-title class="pa-0 mx-3 mt-1 mb-n3" style="">
        <v-row align="center">
          <v-col cols="12">
            <div class="font-size-14 line-height-20">
              <span class="primary-color-2 font-weight-bold">{{ item.brand }} </span>- {{ item.name | reduceText(33) }}
            </div>
          </v-col>
        </v-row>
      </v-card-title>

      <v-row class="pa-0 mx-3 mb-0 text-center py-1" align="center">
        <v-col cols="12" class="ma-0 pa-0 font-size-16 font-weight-3 text-left primary-color-1 line-height-18">
          {{ item.price | formatPrice }}đ
        </v-col>
      </v-row>
      <v-row class="pa-0 mx-3 my-0 text-center py-0" align="center" v-if="item.listPrice != item.price">
        <v-col cols="9" class="ma-0 pa-0 primary-color-4 text-left font-size-12 font-weight-1 old-price line-height-18"
          >{{ item.listPrice | formatPrice }}đ
        </v-col>
      </v-row>

      <!-- <v-card-text class="mx-3 py-0 ma-0"> -->
      <v-row align="center" class="mx-3 pa-0 ma-0" no-gutters>
        <v-col cols="6" class="ma-0 pa-0">
          <v-rating
            class="product-rate ml-n1 pa-0 line-height-16"
            :value="getRatingAverage"
            color="#FFA200"
            dense
            half-increments
            readonly
            size="12"
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
    idProd(): string {
      return this.$route.params['idProd'];
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
  watch: {
    idProd() {
      window.scrollTo({ top: 0, left: 0 });
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

<style lang="scss">
@import '@/assets/scss/Common.scss';
@import '@/assets/scss/LineHeight.scss';
@import '@/assets/scss/FontSize.scss';
@import '@/assets/scss/PrimaryColor.scss';
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

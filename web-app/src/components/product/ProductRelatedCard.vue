<template>
  <v-hover v-slot="{ hover }">
    <v-card
      :elevation="hover ? 4 : 1"
      :loading="loading"
      class="product-related rounded-0 px-2 py-4"
      v-if="item"
      :style="hover ? 'z-index:4' : ''"
    >
      <v-card-title class="pa-0 ma-0">
        <span :class="item.domain.toLowerCase()" class="domain font-size-16 px-4">{{ item.domain }}</span>
      </v-card-title>

      <v-card-title class="pa-0 ma-0 mb-0 pt-7 pb-3" style="line-height: 23px">
        <v-row align="center" no-gutters>
          <v-col cols="12">
            <div class="font-size-14 font-weight-2 title-product">{{ item.name }}</div>
          </v-col>
        </v-row>
      </v-card-title>

      <v-row class="pa-0 mx-0 mb-0 text-center py-0" align="center" no-gutters>
        <v-col cols="6" class="ma-0 pa-0 primary-color-4 text-left">
          <span class="font-size-12 font-weight-1 old-price line-height-22"> {{ item.listPrice | formatPrice }}đ</span>
          <span class="discount-rate px-1 font-size-14 font-weight-2 text-right"> {{ item.discountRate }}% </span>
        </v-col>

        <v-col cols="6" class="ma-0 pa-0">
          <div class="font-size-10 font-weight-1 pa-0 ma-0 text-right line-height-20">
            <v-icon> mdi-heart-outline </v-icon>

            <!-- <span class="line-height-20 font-size-12">{{ $t('freeShip') }}</span> -->
          </div>
        </v-col>
      </v-row>
      <v-row class="pa-0 mx-0 my-0 text-center py-0" align="center" no-gutters>
        <v-col cols="6" class="ma-0 pa-0 font-size-16 font-weight-3 text-left primary-color-1 line-height-26">
          {{ item.price | formatPrice }}đ
        </v-col>
        <v-col cols="6" class="ma-0 pa-0 text-right">
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

  filters: {
    reduceText: function (text: string, max: number) {
      return CategoryService.upperCaseFirstLetter(text && text.length > max ? text.slice(0, max - 2) + '...' : text);
    },
    lowerText: function (text: string) {
      return text ? CategoryService.upperCaseFirstLetter(text) : text;
    },
    formatPrice(value: string) {
      // const val = (value / 1).toFixed(0).replace('.', ',');
      return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },
  },
  computed: {
    getRatingAverage(): number {
      if (this.item && this.item.ratingAverage) {
        return parseInt(this.item.ratingAverage.split('/')[0]) || 0;
      }
      return 5;
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
.product-related {
  height: 100%;
  .domain {
    position: absolute;
    left: 0px;
    top: 0px;
    z-index: 100;
    border-radius: 0px !important;
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
    height: 5em; /* height is 2x line-height, so two lines will display */
    overflow: hidden; /* prevents extra lines from being visible */
    // text-overflow: ellipsis;
    // white-space: nowrap;
  }
}
</style>

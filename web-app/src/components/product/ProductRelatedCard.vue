<template>
  <v-hover v-slot="{ hover }">
    <v-card
      :elevation="hover ? 12 : 2"
      :loading="loading"
      class="product-related rounded-lg box-sizing px-4 py-4 mb-4 mx-2"
      v-if="item"
    >
      <v-card-title class="pa-0 ma-0">
        <span class="domain font-size-16 px-4">{{ item.domain }}</span>
        <span class="discount-rate px-3 font-size-16 font-weight-2 text-right"> {{ item.discountRate }}% </span>
      </v-card-title>

      <v-card-title class="pa-0 ma-0 mb-0 pt-7" style="line-height: 23px">
        <v-row align="center">
          <v-col cols="10 pr-0 py-0" style="min-height: 55px">
            <div class="font-size-14 font-weight-2" v-if="hover">{{ item.name | lowerText }}</div>
            <div class="font-size-14 font-weight-2" v-else>{{ item.name | reduceText(55) }}</div>
          </v-col>
        </v-row>
      </v-card-title>

      <v-card-text align="left" class="pa-0 pt-2">
        <div class="font-size-18 font-weight-3 primary-color-1 py-1">{{ item.price | formatPrice }}đ</div>
        <div class="font-size-12 font-weight-1 py-0" v-if="item.listPrice != item.price">
          <span class="line-through">{{ item.listPrice | formatPrice }}đ</span>
        </div>
      </v-card-text>
      <v-card-text class="ma-0 pa-0">
        <v-row align="center" no-gutters>
          <v-rating :value="getRatingAverage" color="yellow" dense half-increments readonly size="14"></v-rating>
        </v-row>
        <v-row align="center" no-gutters>
          <div class="font-size-12 font-weight-1 pa-0 ma-0 float-right mr-4">{{ $t('freeShip') }}</div>
          <v-spacer />
          <v-btn icon>
            <v-icon> mdi-heart-outline </v-icon>
          </v-btn>
        </v-row>
      </v-card-text>
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
}
</style>

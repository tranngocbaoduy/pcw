<template>
  <v-hover v-slot="{ hover }">
    <v-card :loading="loading" style="" class="product rounded-0 py-2 my-0">
      <v-row class="px-2 pb-0 pt-8 ma-0 py-0" style="height: 220px">
        <span
          :class="[isMobile ? `domain-sub-left-mobile ${item.domain} ` : `domain-sub-left ${item.domain} `]"
          class="font-size-14 px-4"
        ></span>
        <span
          :class="[isMobile ? `domain-mobile ${item.domain}` : `domain ${item.domain}`, hover ? 'top-1px' : '']"
          class="font-size-14 px-4"
          >{{ item.domain }}</span
        >
        <v-img
          :class="hover ? 'mt-0' : 'mt-2'"
          class="product-img text-center"
          style="width: 181px; height: 181px"
          contain
          :style="hover ? 'z-index:4' : ''"
          :src="item.listImage[0] || require('@/assets/banner/no-product.png')"
          :lazy-src="item.listImage[0] || require('@/assets/banner/no-product.png')"
        >
        </v-img
      ></v-row>

      <v-card-title class="pa-0 mx-3 mt-0 mb-n2" style="">
        <v-row align="center">
          <v-col cols="12 pr-0">
            <div class="font-size-14 line-height-20 title-product">
              <!-- <span class="primary-color-2 font-weight-bold">{{ itemBrand }} </span>-  -->
              {{ item.name }}
            </div>
          </v-col>
          <!-- <v-col cols="3 pr-2 pt-0">
            <v-btn class="float-right" icon>
              <v-icon size="16"> mdi-heart-outline </v-icon>
            </v-btn>
          </v-col> -->
        </v-row>
      </v-card-title>

      <v-row class="pa-0 mx-3 my-0 mb-0 text-center py-0" align="center" no-gutters>
        <v-col cols="8" class="ma-0 pa-0 primary-color-4 text-left" v-if="item.listPrice != item.price">
          <span class="line-height-22 font-size-10 font-weight-1 old-price mr-2">
            {{ item.listPrice | formatPrice }}đ</span
          >
          <span class="discount-rate px-1 font-size-12 font-weight-2 text-right"> {{ item.discountRate }}% </span>
        </v-col>
        <v-col cols="8" v-else class="ma-0 pa-0 primary-color-4 text-left"></v-col>

        <v-col cols="4" class="ma-0 pa-0">
          <div class="font-size-10 font-weight-1 pr-0 pa-0 ma-0 text-right line-height-20">
            <span class="font-weight-3 primary-color-3" v-if="item.listChildId && item.listChildId.length != 0">
              {{ `${item.listChildId.length} ${$t('in stores')}` }}</span
            ><br />
          </div>
        </v-col>
      </v-row>
      <v-row class="pa-0 mx-3 my-0 text-center py-0" align="center" no-gutters>
        <v-col cols="7" class="line-height-22 ma-0 pa-0 font-size-14 font-weight-3 text-left primary-color-1">
          {{ item.price | formatPrice }}đ
        </v-col>
        <v-col cols="5" class="ma-0 pa-0 text-right" v-if="item.itemRating">
          <RatingItem :itemRating="item.itemRating" size="12" />
          <!-- <v-rating
            class="product-rate line-height-18 pa-0"
            :value="getRatingAverage"
            color="#FFA200"
            dense
            half-increments
            readonly
            size="13"
          ></v-rating> -->
        </v-col>
      </v-row>

      <v-row align="center" class="mx-3 pa-0 ma-0" no-gutters> </v-row>
      <v-row align="center" class="mx-3 pa-0 ma-0" no-gutters> </v-row>
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import CategoryService from '@/api/category.service';
import RatingItem from '@/components/common/rating/RatingItem.vue';
import Vue from 'vue';

export default Vue.extend({
  props: ['item'],
  components: { RatingItem },
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
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
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
@import '@/resources/scss/Common.scss';
@import '@/resources/scss/LineHeight.scss';
@import '@/resources/scss/FontSize.scss';
.product {
  height: 100%;
  border: #f2f2f2 0.1px solid;
  box-shadow: none;
  .product-img {
    -webkit-transition: all 0.2s;
    -moz-transition: all 0.2s;
    -ms-transition: all 0.2s;
    -o-transition: all 0.2s;
    transition: all 0.2s;
  }
  .top-1px {
    top: 1px !important;
  }
  .domain {
    position: absolute;
    right: 0px;
    top: 3px;
    z-index: 2;
    height: 24px;
    line-height: 24px;
    border-radius: 0px 0px 0px 4px !important;
  }
  .domain-sub-left {
    position: absolute;
    right: 0px;
    top: 0px;
    z-index: 2;
    border-radius: 4px 0px 4px 2px !important;
  }
  .domain-mobile {
    position: absolute;
    right: 0px;
    top: 3px;
    z-index: 2;
    height: 20px;
    line-height: 20px;
    border-radius: 0px 0px 0px 4px !important;
  }
  .domain-sub-left-mobile {
    position: absolute;
    right: 0px;
    top: 0px;
    z-index: 2;
    border-radius: 4px 0px 4px 2px !important;
  }
  .discount-rate {
    color: #ca3e29;
    z-index: 2;
    border: 1px solid #ca3e29;
    border-radius: 1px !important;
    line-height: 14px !important;
  }

  .old-price {
    text-decoration: line-through !important;
    text-decoration-color: #607d8b !important;
    text-decoration-style: solid 1px !important;
  }
}
</style>

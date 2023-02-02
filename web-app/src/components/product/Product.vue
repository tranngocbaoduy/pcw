<template>
  <v-hover v-slot="{ hover }">
    <v-card :loading="loading" style="" class="product rounded-0 py-2 my-0">
      <v-row class="px-2 pb-0 pt-0 ma-0 py-0">
        <span
          v-if="isDetailMode"
          :class="[isMobile ? `domain-sub-left-mobile ${item.domain} ` : `domain-sub-left ${item.domain} `]"
          class="font-size-10 px-4"
        ></span>
        <span
          v-if="isDetailMode"
          :class="[isMobile ? `domain-mobile ${item.domain}` : `domain ${item.domain}`, hover ? 'top-1px' : '']"
          class="font-size-10 px-2"
          >{{ item.representDomainName }}</span
        >
        <v-img
          :class="hover ? 'mt-0' : 'mt-2'"
          class="product-img text-center"
          contain
          :style="
            (hover ? 'z-index:1;' : '') +
            (isShowImageDetail ? 'width: 120px; height: 120px;' : 'width: 80px; height: 80px;')
          "
          :src="item.listImage[0] || require('@/assets/banner/no-product.png')"
          :lazy-src="item.listImage[0] || require('@/assets/banner/no-product.png')"
          :alt="item.name"
        >
        </v-img
      ></v-row>

      <v-card-title class="pa-0 mx-3 mt-0 mb-n3" style="">
        <v-row align="center">
          <v-col cols="12 pr-0">
            <div class="font-size-14 mb-2 line-height-20 title-product">
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

      <v-row class="pa-0 mx-3 my-0 mb-0 text-center py-0" align="center" no-gutters v-if="isDetailMode">
        <v-col cols="8" class="ma-0 pa-0 primary-color-4 text-left" v-if="item.listPrice != item.price">
          <span class="line-height-22 font-size-10 font-weight-1 old-price mr-2">
            {{ item.listPrice | formatPrice }}đ</span
          >
          <span class="discount-rate px-1 font-size-12 font-weight-2 text-right"> {{ item.discountRate }}% </span>
        </v-col>

        <v-col cols="8" v-else class="ma-0 pa-0 primary-color-4 text-left" style="height: 25px"> </v-col>

        <v-col cols="4" class="ma-0 pa-0 d-flex align-center justify-center"> </v-col>
      </v-row>
      <v-row class="pa-0 mx-3 my-0 text-center py-0" align="center" no-gutters>
        <v-col
          v-if="isDetailMode"
          cols="12"
          class="line-height-22 ma-0 pa-0 font-size-14 font-weight-3 text-left primary-color-1"
        >
          {{ item.price | formatPrice }}đ
        </v-col>
        <v-col
          v-else-if="item.smallestPrice != item.largestPrice"
          cols="12"
          class="line-height-22 ma-0 pa-0 font-size-12 font-weight-3 text-left primary-color-1"
        >
          {{ item.smallestPrice | formatPrice }} - {{ item.largestPrice | formatPrice }}đ
        </v-col>
        <v-col v-else cols="12" class="line-height-22 ma-0 pa-0 font-size-12 font-weight-3 text-left primary-color-1">
          {{ item.smallestPrice | formatPrice }}đ
        </v-col>
      </v-row>
      <v-row class="pa-2 px-3 py-0 ma-0">
        <div
          class="font-size-10 font-weight-1 pr-0 pa-0 my-1 ma-0 text-left line-height-20"
          style="max-height: 40px; min-height: 40px"
          v-if="!isDetailMode"
        >
          Có ở {{ item.stores.length }} cửa hàng
          <span class="font-size-10 font-weight-2 primary-color-2">{{ mappingStoreName.slice(0, 2).join(', ') }}</span>
          {{ mappingStoreName.length >= 2 ? '... và hơn thế nưa' : '' }}
        </div>
        <v-col
          cols="12"
          class="d-flex flex-wrap align-center justify-start pa-0 ma-0 my-0 py-1"
          v-if="item.initTags && item.initTags.length != 0"
        >
          <span
            class="sub-info flex-grow-0 pa-1 flex-shink-1 mr-1 mb-1 font-size-10 font-weight-2 text-left"
            v-for="tag in item.initTags.slice(0, item.initTags.length)"
            :key="tag"
          >
            {{ tag }}
          </span>
        </v-col>
        <v-col cols="6" class="pa-0 ma-0">
          <v-rating
            class="ma-0 pa-0 text-left"
            :value="getRatingAverage"
            color="#FFA200"
            dense
            half-increments
            readonly
            size="13"
          ></v-rating>
        </v-col>
        <v-col cols="6" class="pa-0 ma-0">
          <div class="font-size-10 font-weight-1 pr-0 pa-0 ma-0 text-right">
            {{ item.updatedAt | calTimeSince }}
          </div>
        </v-col>
      </v-row>
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import CategoryService from '@/api/category.service';
import Vue from 'vue';

export default Vue.extend({
  props: ['item', 'isDisplayGeneral'],
  // components: { RatingItem },
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
    mappingStoreName(): string[] {
      return this.item.stores.map((store: string) => CategoryService.agencyItems.find((i) => i.code == store)?.name);
    },
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    isDetailMode(): boolean {
      if (this.isDisplayGeneral) return false;
      return this.$store.getters.isDetailMode;
    },
    isShowImageDetail(): boolean {
      return this.$store.getters.isShowImageDetail;
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
    calTimeSince(fromDateString: string) {
      const fromDate: Date = new Date(fromDateString);
      const nowDate: Date = new Date();
      const seconds = Math.floor((nowDate.getTime() - fromDate.getTime()) / 1000);
      let interval = seconds / 31536000;

      if (interval > 1) {
        return Math.floor(interval) + 'y ago';
      }
      interval = seconds / 2592000;
      if (interval > 1) {
        return Math.floor(interval) + 'M ago';
      }
      interval = seconds / 86400;
      if (interval > 1) {
        return Math.floor(interval) + 'd ago';
      }
      interval = seconds / 3600;
      if (interval > 1) {
        return Math.floor(interval) + 'h ago';
      }
      interval = seconds / 60;
      if (interval < 1) {
        return 'Just now';
      }
      return Math.floor(interval) + 'm ago';
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
  @keyframes fadeOut {
    0% {
      opacity: 1;
    }
    99% {
      opacity: 0;
      z-index: 1;
    }
    100% {
      opacity: 0;
      display: none;
      z-index: -5;
    }
  }
  height: 100%;
  border: #f2f2f2 0.1px solid;
  box-shadow: none;
  transition: opacity 0.5s linear;
  -webkit-transition: opacity 0.5s linear;
  -moz-transition: opacity 0.5s linear;
  -o-transition: opacity 0.5s linear;
  -ms-transition: opacity 0.5s linear;
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
    z-index: 3 !important;
    border-radius: 4px 0px 4px 2px !important;
  }
  .domain-mobile {
    position: absolute;
    right: 0px;
    top: 3px;
    z-index: 3 !important;
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

  .sub-info {
    color: #777473;
    z-index: 2;
    border: 1px solid#c0bfbe;
    display: block;
    white-space: nowrap;
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

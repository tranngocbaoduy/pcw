<template>
  <v-hover v-slot="{ hover }">
    <v-card
      :elevation="hover ? 2 : 0"
      :loading="loading"
      class="
        product-related
        rounded-0
        px-2
        pb-3
        pt-1
        my-0
        d-flex d-flex-row
        flex-wrap
        justify-space-around
        align-center
      "
      :class="hover ? 'bg-primary-color-6' : ''"
      v-if="item"
      :style="hover ? 'z-index:4' : ''"
    >
      <div>
        <v-img
          contain
          transition="fade-transition"
          :width="isMobile ? 40 : 60"
          :height="isMobile ? 40 : 60"
          :src="item.listImage[0]"
          class="ma-auto"
        ></v-img>
      </div>
      <div class="pa-0 ma-0">
        <span
          :class="isMobile ? `domain-mobile ${item.domain.toLowerCase()}` : `domain ${item.domain.toLowerCase()}`"
          class="font-size-14 px-4"
          >{{ item.domain }}</span
        >
      </div>

      <div
        class="pa-0 ma-0 mb-0 pb-0 pt-4"
        :style="isMobile ? 'width: 320px' : 'width: 400px'"
        style="line-height: 23px"
      >
        <div class="font-size-14 font-weight-2">{{ item.name }}</div>
        <div class="d-flex justify-space-between align-center px-0 mx-0">
          <RatingItem class="hover-custom-link" :itemRating="item.itemRating" />
          <div class="font-size-14 font-weight-2 pt-1 pl-2">
            <v-icon small class="px-2 pr-1 pb-1">mdi-map-marker</v-icon>{{ item.shopLocation }}
          </div>
        </div>
      </div>
      <div class="mx-3 ml-0 font-size-14 text-right" :style="isMobile ? 'min-width: 50px' : 'min-width: 90px'">
        <div class="mb-n2">
          <span class="font-weight-bold">{{
            item.itemRating.rating_count.reduce((partialSum, a) => partialSum + a, 0) || 0
          }}</span
          ><span> review </span>
        </div>
        <a :href="getURLAccessTrade()" target="_blank" class="font-size-12 text-underline">Xem ngay</a>
      </div>

      <div class="mx-3 font-size-14 text-right" :style="isMobile ? 'min-width: 50px' : 'min-width: 90px'">
        <span class="font-weight-bold">{{ item.historicalSold || 0 }}</span> <span> đã bán</span>
      </div>
      <div class="ma-0 pa-0 primary-color-4 text-left" :style="isMobile ? 'min-width: 30px' : 'width: 40px'">
        <span class="discount-rate px-1 font-size-14 font-weight-2 text-right" v-if="item.listPrice != item.price">
          {{ item.discountRate }}%
        </span>
      </div>

      <div
        :style="isMobile ? 'width: 45px' : 'width: 80px'"
        class="ml-4"
        :class="isMobile ? 'font-size-14' : 'font-size-14'"
      >
        Kho: <span class="font-weight-bold">{{ item.stock || 0 }} </span>
      </div>
      <div class="text-right" :style="isMobile ? 'min-width: 60px' : 'min-width: 100px'">
        <div class="font-size-12 font-weight-1 old-price" v-if="item.listPrice != item.price">
          {{ item.listPrice | formatPrice }}đ
        </div>
        <div class="ma-0 pa-0 font-size-14 font-weight-3 text-right primary-color-1">
          {{ item.price | formatPrice }}đ
        </div>
      </div>

      <a :href="getURLAccessTrade()" target="_blank">
        <v-btn class="rounded-lg my-2" icon color="#1859db">
          <v-icon>mdi-shopping-outline</v-icon>
        </v-btn>
      </a>
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import RatingItem from '@/components/common/rating/RatingItem.vue';
import CategoryService from '@/api/category.service';
import Vue from 'vue';

export default Vue.extend({
  props: ['item'],
  data: () => ({
    loading: false,
    selection: 1,
  }),
  components: { RatingItem },

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

    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
  },

  methods: {
    reserve() {
      this.loading = true;
      setTimeout(() => (this.loading = false), 2000);
    },

    getURLAccessTrade(): string {
      return `${process.env.VUE_APP_BASE_ACCESS_TRADE_URL}?url=${this.item.url}`;
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
    bottom: 0px;
    z-index: 100;
    height: 24px;
    line-height: 24px;
    border-radius: 0px 4px 0px 0px !important;
  }
  .domain-mobile {
    position: absolute;
    left: 0px;
    top: 0px;
    z-index: 100;
    height: 20px;
    line-height: 20px;
    border-radius: 0px 0px 4px 0px !important;
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

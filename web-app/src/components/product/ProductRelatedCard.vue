<template>
  <v-hover v-slot="{ hover }">
    <v-card
      :elevation="hover ? 2 : 0"
      :loading="loading"
      class="product-related rounded-0 px-2 pb-3 pt-1 my-0 d-flex d-flex-row flex-wrap align-center"
      :class="(hover ? 'bg-primary-color-6' : '') + ' ' + (isMobile ? 'justify-space-around' : 'justify-space-around')"
      v-if="item"
      :style="hover ? 'z-index:4' : ''"
    >
      <!-- <div>
        <v-img
          contain
          transition="fade-transition"
          :width="isMobile ? 40 : 60"
          :height="isMobile ? 40 : 60"
          :src="item.listImage[0]"
          class="ma-auto"
        ></v-img>
      </div> -->
      <div
        class="pa-0 ma-0 mb-0 pb-0 pt-4 d-flex justify-start align-center"
        :style="isMobile ? `width: ${innerWidth}px` : 'min-width: 600px; width: 600px'"
        style="line-height: 23px"
      >
        <v-img
          contain
          transition="fade-transition"
          :width="isMobile ? 70 : 80"
          :height="isMobile ? 70 : 80"
          :max-width="isMobile ? 70 : 80"
          :max-height="isMobile ? 70 : 80"
          :src="item.listImage[0]"
          class="mx-4"
        ></v-img>

        <div style="flex: 1">
          <div class="font-size-14 font-weight-2">{{ item.name }}</div>
          <div class="d-flex justify-space-between align-center px-0 mx-0">
            <!-- <RatingItem class="hover-custom-link" :itemRating="item.itemRating" /> -->
            <div class="font-size-12 font-weight-2 primary-color-4">
              <v-icon
                @click="goToStore()"
                v-if="item.shopItem.store_level && item.shopItem.store_level == 'TRUSTED_STORE'"
                class="store font-size-20 mb-1 mr-1 primary-color-4"
                >mdi-store-check-outline</v-icon
              >
              <v-icon @click="goToStore()" v-else class="store font-size-20 mb-1 mr-1 primary-color-4"
                >mdi-store-outline</v-icon
              >

              <span @click="goToStore()" class="store" style="text-decoration: underline">{{
                item.shopItem.shop_name
              }}</span>
            </div>
            <div class="font-size-14 font-weight-2 pt-1 pl-2" v-if="item.shopLocation !== item.shopItem.shop_name">
              <v-icon small class="px-2 pr-1 pb-1">mdi-map-marker</v-icon>{{ item.shopLocation }}
            </div>
          </div>
        </div>
      </div>

      <div
        class="font-size-14 text-center"
        style="flex: 1"
        :style="isMobile ? 'width: 80px;' : 'width: 90px; padding-left:28px'"
      >
        <span> Review: </span>
        <span class="font-weight-bold">{{ item.countReview || 0 }}</span>
      </div>

      <!-- <div v-if="!isMobile" class="font-size-14 text-right" :style="isMobile ? 'min-width: 50px' : 'min-width: 90px'">
        <span class="font-weight-bold">{{ item.historicalSold || 0 }}</span> <span> đã bán</span>
      </div> -->
      <!-- 
      <div
        class="text-left"
        :style="isMobile ? 'width: 70px' : 'width: 80px'"
        :class="isMobile ? 'font-size-14' : 'font-size-14'"
      >
        Kho: <span class="font-weight-bold">{{ item.stock || 0 }} </span>
      </div> -->

      <div style="flex: 1" class="text-right" :style="isMobile ? 'min-width: 95px' : 'min-width: 120px'">
        <div
          class="ma-0 pa-0 font-size-16 font-weight-3 text-right primary-color-1"
          :class="item.listPrice != item.price ? 'pt-4 mb-n2' : ''"
        >
          {{ item.price | formatPrice }}đ
        </div>
        <span class="px-2 py-0 discount-rate font-size-12 font-weight-2 text-right" v-if="item.listPrice != item.price">
          {{ item.discountRate }}%
        </span>
      </div>

      <!-- <div
        class="ma-0 pa-0 primary-color-4 text-left d-flex align-center justify-center"
        :style="isMobile ? 'min-width: 50px' : 'width: 70px'"
      >
        <span class="px-2 py-0 discount-rate font-size-12 font-weight-2 text-right" v-if="item.listPrice != item.price">
          {{ item.discountRate }}%
        </span>
      </div> -->
      <div style="flex: 1" :class="isMobile ? 'text-right' : 'text-center'">
        <v-btn class="rounded-lg my-2" icon color="#1859db" @click="goToPlatform()">
          <v-icon>mdi-shopping-outline</v-icon>
        </v-btn>
      </div>

      <div class="pa-0 ma-0 absolute">
        <span
          :class="[
            isMobile
              ? `domain-sub-left-mobile ${item.domain.toLowerCase()}`
              : `domain-sub-left ${item.domain.toLowerCase()}`,
          ]"
          class="font-size-14 px-4"
        ></span>
        <span
          :class="[isMobile ? `domain-mobile ${item.domain.toLowerCase()}` : `domain ${item.domain.toLowerCase()}`]"
          class="font-size-14 px-4"
          >{{ item.agencyDisplay }}</span
        >
      </div>
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
  components: {
    // RatingItem
  },

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
    innerWidth(): number {
      return this.$store.getters.innerWidth;
    },
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
    goToPlatform() {
      window.open(this.getURLAccessTrade(), '_blank');
    },
    getURLAccessTrade(): string {
      return `${process.env.VUE_APP_BASE_ACCESS_TRADE_URL}?url=${this.item.url}`;
    },
    goToStore(): void {
      if (this.item.shopUrl) window.open(this.item.shopUrl, '_blank');
    },
  },
});
</script>

<style lang="scss">
.product-related {
  height: 100%;
  .domain {
    position: absolute;
    right: 0px;
    top: 3px;
    z-index: 100;
    height: 24px;
    line-height: 24px;
    border-radius: 0px 0px 0px 4px !important;
  }
  .domain-sub-left {
    position: absolute;
    right: 0px;
    top: 0px;
    z-index: 100;
    border-radius: 4px 0px 4px 2px !important;
  }
  .domain-mobile {
    position: absolute;
    left: 0px;
    top: 3px;
    z-index: 100;
    height: 20px;
    line-height: 20px;
    border-radius: 0px 0px 4px 0px !important;
  }
  .domain-sub-left-mobile {
    position: absolute;
    left: 0px;
    top: 0px;
    z-index: 100;
    border-radius: 4px 0px 4px 2px !important;
  }
  .discount-rate {
    color: #ca3e29;
    z-index: 2;
    border: 1px solid #ca3e29;
    border-radius: 1px !important;
    line-height: 14px !important;
  }
  .trusted {
    color: #ff2200;
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
  .title-product {
    line-height: 1.5em;
    height: 5em; /* height is 2x line-height, so two lines will display */
    overflow: hidden; /* prevents extra lines from being visible */
    // text-overflow: ellipsis;
    // white-space: nowrap;
  }
  .store:hover {
    cursor: pointer;
  }
}
</style>

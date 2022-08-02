<template>
  <v-col sm="12" md="12" cols="12" :class="isMobile ? 'py-0' : 'py-3'" class="trending-brand">
    <div class="mt-2 pa-0">
      <v-card-title class="trending-page-name font-size-32 font-weight-3 px-0 mt-2 mx-0">
        {{ $t('trendingPromotion') }}
        <v-spacer></v-spacer>
        <div
          v-if="!isMobile"
          class="font-weight-2 font-size-14 py-3 primary-color-1 float-right custom-link hover-custom-link"
        >
          <span class="py-1">{{ $t('seeMore') }}</span>
          <v-icon class="primary-color-1 pb-1" size="20px">mdi-chevron-right</v-icon>
        </div>
      </v-card-title>
      <v-carousel
        :show-arrows="false"
        light
        touchless
        :cycle="true"
        hide-delimiters
        hide-delimiter-background
        class="px-0"
        height="100%"
      >
        <template v-for="(item, index) in filterPromotionItems">
          <v-carousel-item
            v-if="(index + 1) % quantityItemsInCarousel === 1 || quantityItemsInCarousel === 1"
            :key="index"
          >
            <v-row class="pt-0 mx-0" no-gutters>
              <template v-for="(n, i) in quantityItemsInCarousel">
                <template v-if="+index + i < filterPromotionItems.length">
                  <v-col class="pa-2 px-0" :key="i">
                    <v-hover v-slot="{ hover }">
                      <v-card
                        :elevation="hover ? 3 : 1"
                        v-if="+index + i < filterPromotionItems.length"
                        class="border-custom-4 pa-4 py-4 mx-auto"
                      >
                        <span
                          v-if="item.listPrice != item.price"
                          class="discount-rate px-3 font-size-16 font-weight-2 text-right"
                        >
                          {{ filterPromotionItems[+index + i].sale }}%
                        </span>

                        <v-img
                          height="100%"
                          aspect-ratio="1.2"
                          class="my-2 rounded-0"
                          :src="filterPromotionItems[+index + i].img"
                        ></v-img>
                        <v-card-title class="font-size-16 font-weight-3 pa-2">
                          <v-row class="justify-center">
                            <div class="primary-color-2 mr-4">
                              {{ filterPromotionItems[+index + i].price | formatPrice }}đ
                            </div>
                          </v-row>
                        </v-card-title>
                      </v-card>
                    </v-hover>
                  </v-col>
                </template>
              </template>
            </v-row>
          </v-carousel-item>
        </template>
      </v-carousel>
    </div>
  </v-col>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  data() {
    return {
      promotions: [
        {
          name: 'Product1',
          sale: 18,
          price: '13000000',
          img: 'https://image.thanhnien.vn/1024/uploaded/nthanhluan/2020_10_14/1_foyn.jpg',
        },
        {
          name: 'Product2',
          sale: 18,
          price: '300000',
          img: 'https://cf.shopee.vn/file/e057297df1d99840c6ed44c936c7017f',
        },
        {
          name: 'Product3',
          sale: 18,
          price: '450000',
          img: 'https://cf.shopee.vn/file/1e38d6b16c9035cd9966a9551890b47b',
        },
        {
          name: 'Product4',
          sale: 30,
          price: '17000000',
          img: 'https://phucanhcdn.com/media/product/42432_nitro_series_an515_44_ha5.jpg',
        },
        {
          name: 'Product1',
          sale: 18,
          price: '13000000',
          img: 'https://image.thanhnien.vn/1024/uploaded/nthanhluan/2020_10_14/1_foyn.jpg',
        },
        {
          name: 'Product2',
          sale: 18,
          price: '300000',
          img: 'https://cf.shopee.vn/file/e057297df1d99840c6ed44c936c7017f',
        },
        {
          name: 'Product3',
          sale: 18,
          price: '450000',
          img: 'https://cf.shopee.vn/file/1e38d6b16c9035cd9966a9551890b47b',
        },
        {
          name: 'Product4',
          sale: 30,
          price: '17000000',
          img: 'https://phucanhcdn.com/media/product/42432_nitro_series_an515_44_ha5.jpg',
        },
        {
          name: 'Product2',
          sale: 18,
          price: '300000',
          img: 'https://cf.shopee.vn/file/e057297df1d99840c6ed44c936c7017f',
        },
        {
          name: 'Product3',
          sale: 18,
          price: '450000',
          img: 'https://cf.shopee.vn/file/1e38d6b16c9035cd9966a9551890b47b',
        },
      ],
    };
  },
  filters: {
    reduceText: function (text: string, max: number) {
      return text.length > max ? text.slice(0, max - 3) + '...' : text;
    },
    formatPrice(value: string) {
      // const val = (value / 1).toFixed(0).replace('.', ',');
      // return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    },
  },
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    heightScale(): number {
      return 350;
    },
    filterPromotionItems(): any[] {
      return this.promotions.slice(
        0,
        Math.floor(this.promotions.length / this.quantityItemsInCarousel) * this.quantityItemsInCarousel
      );
    },
    quantityItemsInCarousel(): number {
      if (this.$vuetify.breakpoint.xl) return 7;
      if (this.$vuetify.breakpoint.lg) return 7;
      if (this.$vuetify.breakpoint.md) return 7;
      if (this.$vuetify.breakpoint.sm) return 7;
      return 2;
    },
  },
});
</script>

<style lang="scss" scoped>
.trending-promotion {
  background: white;

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

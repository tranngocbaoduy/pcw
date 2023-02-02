<template>
  <v-col sm="12" md="12" cols="12" :class="isMobile ? 'py-0' : 'py-1'" class="trending-promotion px-0">
    <div class="my-0 pa-0">
      <v-card-title class="trending-page-name font-size-32 font-weight-3 px-0 ma-0">
        {{ $t('trendingPromotion') }} - {{ category.name }}
        <v-spacer></v-spacer>
        <div
          v-if="!isMobile"
          class="font-weight-2 font-size-14 py-3 primary-color-1 float-right custom-link hover-custom-link"
          @click="handleChangeToCategory"
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
        hide-delimiter-background
        class="px-0"
        height="100%"
      >
        <template v-for="(item, index) in filterPromotionItems">
          <v-carousel-item
            v-if="(index + 1) % quantityItemsInCarousel === 1 || quantityItemsInCarousel === 1"
            :key="`promotions-${index}`"
          >
            <v-row class="pt-0 mx-0" no-gutters>
              <template v-for="(n, i) in quantityItemsInCarousel">
                <template v-if="+index + i < filterPromotionItems.length">
                  <v-col class="py-2 px-0" :key="i">
                    <router-link :to="`${getSlugId(filterPromotionItems[+index + i])}`" :key="`${i}-${n}-s`">
                      <v-hover v-slot="{ hover }">
                        <v-card
                          :elevation="hover ? 3 : 1"
                          v-if="+index + i < filterPromotionItems.length"
                          class="border-custom-4 pa-2 py-4 mx-auto"
                        >
                          <v-img
                            contain
                            width="120"
                            height="120"
                            class="ma-auto mb-2 rounded-0"
                            :src="filterPromotionItems[+index + i].listImage[0]"
                          ></v-img>
                          <v-card-title class="font-size-16 font-weight-3 pa-0">
                            <div>
                              <!-- <div class="primary-color-2 mr-4">
                                {{ filterPromotionItems[+index + i].price | formatPrice }}đ
                              </div> -->

                              <div class="d-flex-col align-center justify-start line-height-18">
                                <div
                                  style="height: 50px"
                                  class="font-size-12 font-weight-2 line-height-22 title-product mb-2"
                                >
                                  {{ filterPromotionItems[+index + i].name }}
                                </div>
                                <v-col
                                  cols="12"
                                  class="d-flex flex-wrap align-center justify-start pa-0 ma-0"
                                  v-if="
                                    filterPromotionItems[+index + i].initTags &&
                                    filterPromotionItems[+index + i].initTags.length != 0
                                  "
                                >
                                  <span
                                    class="
                                      sub-info
                                      flex-grow-0
                                      pa-1
                                      flex-shink-1
                                      mr-1
                                      mb-1
                                      font-size-10 font-weight-2
                                      text-left
                                    "
                                    v-for="tag in filterPromotionItems[+index + i].initTags.slice(
                                      0,
                                      filterPromotionItems[+index + i].initTags.length
                                    )"
                                    :key="tag"
                                  >
                                    {{ tag }}
                                  </span>
                                </v-col>
                                <span
                                  class="mr-3 line-height-22 font-size-10 font-weight-1 old-price"
                                  v-if="
                                    filterPromotionItems[+index + i].listPrice != filterPromotionItems[+index + i].price
                                  "
                                >
                                  {{ filterPromotionItems[+index + i].listPrice | formatPrice }}đ
                                </span>
                                <div class="d-flex align-center justify-space-between">
                                  <span class="mr-3 font-weight-bold font-size-12 primary-color-2"
                                    >{{ filterPromotionItems[+index + i].price | formatPrice }}đ
                                  </span>
                                  <span
                                    class="discount-rate font-size-14 font-weight-2 elevation-0 bg-primary-color-7"
                                    v-if="
                                      filterPromotionItems[+index + i].listPrice !=
                                      filterPromotionItems[+index + i].price
                                    "
                                  >
                                    {{ filterPromotionItems[+index + i].discountRate }}%
                                  </span>
                                </div>
                              </div>
                            </div>
                          </v-card-title>
                        </v-card>
                      </v-hover>
                    </router-link>
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
import ProductService, { ProductItem } from '@/api/product.service';
import Vue from 'vue';

export default Vue.extend({
  props: ['promotionItems', 'category'],
  data() {
    return {
      promotions: [
        {
          name: 'Product1',
          sale: 18,
          price: '13000000',
          img: 'https://image.thanhnien.vn/1024/uploaded/nthanhluan/2020_10_14/1_foyn.jpg',
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
      return this.promotionItems.slice(
        0,
        Math.floor(this.promotionItems.length / this.quantityItemsInCarousel) * this.quantityItemsInCarousel
      );
    },
    quantityItemsInCarousel(): number {
      if (this.$vuetify.breakpoint.xl) return 7;
      if (this.$vuetify.breakpoint.lg) return 7;
      if (this.$vuetify.breakpoint.md) return 2;
      if (this.$vuetify.breakpoint.sm) return 3;
      return 2;
    },
  },
  methods: {
    getSlugId(item: ProductItem): string {
      return ProductService.getSlugId(item);
    },

    handleChangeToCategory() {
      this.$router.push(`/category/${this.category.id}`);
    },
  },
});
</script>

<style lang="scss" scoped>
.trending-promotion {
  background: transparent;

  .old-price {
    text-decoration: line-through !important;
    text-decoration-color: #607d8b !important;
    text-decoration-style: solid 1px !important;
  }

  .discount-rate {
    position: absolute;
    right: 0px;
    bottom: 20px;
    z-index: 2;
    width: 36px;
    color: white;
    height: 36px;
    padding-top: 4px;
    padding-bottom: 4px;
    text-align: center !important;
    border-radius: 0px 0px 0px 2px !important;
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
}
</style>

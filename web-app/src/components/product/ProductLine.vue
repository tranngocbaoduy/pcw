<template>
  <v-card
    class="product-line-card elevation-0 rounded-0 box-sizing my-6 pt-4 pa-0"
    min-height="406"
    v-if="items && items.length != 0"
  >
    <div class="ml-7 mt-1 mb-0 font-size-26 primary-color-2 font-weight-bold">
      <v-row no-gutters class="pa-0">
        <div>
          <v-img
            width="40px"
            height="40px"
            aspect-ratio="4.2"
            src="https://i.pinimg.com/736x/2a/ec/b9/2aecb93a75d08bbebec5800b1cfa59a3.jpg"
          ></v-img>
        </div>
        <div class="font-size-26 font-weight-3 pa-2">{{ $t('trendingSearch') }}</div>
        <v-spacer></v-spacer>
      </v-row>
    </div>
    <v-carousel
      show-arrows-on-hover
      hide-delimiters
      light
      height="100%"
      continuous
      :cycle="true"
      hide-delimiter-background
      class="pa-0"
      v-if="items && items.length != 0"
    >
      <template v-for="(item, index) in items">
        <v-carousel-item
          class="ml-3"
          v-if="(index + 1) % quantityItemsInCarousel === 1 || quantityItemsInCarousel === 1"
          :key="index"
        >
          <v-row class="mx-0 my-1">
            <template v-for="(n, i) in quantityItemsInCarousel">
              <template v-if="+index + i < items.length">
                <v-col :key="i" class="pt-2 px-0 d-flex align-center justify-center">
                  <v-hover v-slot="{ hover }">
                    <router-link
                      class="custom-link"
                      :to="`/category/${$route.params['idCate']}/product/${getIdProduct(item)}`"
                    >
                      <v-card
                        :elevation="hover ? 4 : 1"
                        :width="widthCardProductLine"
                        :loading="isLoading"
                        v-if="+index + i < items.length"
                        color="#fff"
                        class="rounded-lg pa-3"
                      >
                        <v-row no-gutters>
                          <v-col cols="12" class="py-4 pa-auto">
                            <v-img
                              width="80%"
                              height="176px"
                              class="ma-auto"
                              :src="items[+index + i].listImage[0]"
                            ></v-img
                          ></v-col>

                          <v-col cols="12" class="mt-3 pa-auto text-left">
                            <div class="ma-auto black--text text-left font-size-14 font-weight-bold">
                              <span class="primary-color-2 font-weight-bold">{{ items[+index + i].brand }} </span>-
                              <span class="font-weight-2">
                                {{ items[+index + i].name | reduceText(38 - items[+index + i].brand.length - 3) }}</span
                              >
                            </div>

                            <v-row class="pa-0 mb-0 text-center py-2" align="center" no-gutters>
                              <v-col
                                cols="12"
                                class="ma-0 pa-0 font-size-16 font-weight-3 text-left primary-color-1 line-height-18"
                              >
                                {{ item.price | formatPrice }}đ
                              </v-col>
                            </v-row>
                            <v-row
                              class="pa-0 my-0 text-center py-0"
                              align="center"
                              no-gutters
                              v-if="item.listPrice != item.price"
                            >
                              <v-col
                                cols="9"
                                class="
                                  ma-0
                                  pa-0
                                  primary-color-4
                                  text-left
                                  font-weight-1
                                  line-height-18
                                  old-price
                                  font-size-14
                                "
                                >{{ item.listPrice | formatPrice }}đ
                              </v-col>
                            </v-row>
                            <div class="text-left py-0 font-size-12 font-weight-3 primary-color-3">
                              {{ `${item.listChildId.length} ${$t('in stores')}` }}
                            </div>
                          </v-col>
                        </v-row>
                      </v-card>
                    </router-link>
                  </v-hover>
                </v-col>
              </template>
            </template>
          </v-row>
        </v-carousel-item>
      </template>
    </v-carousel>
  </v-card>
</template>

<script lang="ts">
import CategoryService from '@/api/category.service';
import { ProductItem } from '@/api/product.service';
import Vue from 'vue';

export default Vue.extend({
  props: ['items'],
  data: () => ({
    isLoading: true,
    selection: 1,
    widthCardProductLine: 0,
    quantityItemsInCarousel: 0,
  }),
  filters: {
    reduceText: function (text: string, max: number) {
      return CategoryService.upperCaseFirstLetter(text.length > max ? text.slice(0, max - 2) + '...' : text);
    },
    formatPrice(value: string) {
      return value ? value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') : '';
    },
  },
  watch: {
    items() {
      if (!this.items) {
        this.isLoading = true;
      } else {
        this.isLoading = false;
      }
    },
  },
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
  },
  created() {},

  mounted() {
    this.onResize();
    window.addEventListener('resize', this.onResize, { passive: true });
    window.addEventListener('resize', this.onResize, { passive: true });
  },
  methods: {
    reserve() {},
    onResize() {
      this.widthCardProductLine = this.getWidthCardProductLine();
      this.quantityItemsInCarousel = this.getQuantityItemsInCarousel();
    },
    getQuantityItemsInCarousel(): number {
      console.log('window.innerWidth', window.innerWidth, this.$vuetify.breakpoint.sm);
      if (this.$vuetify.breakpoint.xl) return 4;
      if (this.$vuetify.breakpoint.lg) return 4;
      if (this.$vuetify.breakpoint.md) return 4;
      if (this.$vuetify.breakpoint.sm) return 3;
      console.log('window.innerWidth', window.innerWidth, this.$vuetify.breakpoint.sm);

      if (window.innerWidth > 378) return 2;
      if (window.innerWidth > 300) return 1;
      return 2;
    },
    getWidthCardProductLine(): number {
      if (this.isMobile) {
        console.log('window.innerWidth', window.innerWidth);
        if (window.innerWidth > 378) return 170;
        if (window.innerWidth > 300) return 220;
        return 180;
      }
      return 200;
    },
    getIdProduct(item: ProductItem) {
      return item.id;
    },
  },
});
</script>

<style lang="scss">
@import '@/resources/scss/Common.scss';
@import '@/resources/scss/LineHeight.scss';
@import '@/resources/scss/FontSize.scss';
.product-line-card {
  width: 100%;
  background-color: gray;

  .old-price {
    text-decoration: line-through !important;
    text-decoration-color: #607d8b !important;
    text-decoration-style: solid 1px !important;
  }
}
</style>

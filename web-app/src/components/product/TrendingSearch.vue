<template>
  <v-card class="rounded-0 elevation-0 py-4 trending-search" height="265">
    <v-card-title class="pa-0 px-4">
      <v-row no-gutters class="pa-0">
        <div>
          <v-img
            width="40px"
            height="40px"
            aspect-ratio="4.2"
            src="https://i.pinimg.com/736x/2a/ec/b9/2aecb93a75d08bbebec5800b1cfa59a3.jpg"
          ></v-img>
        </div>
        <div class="font-size-24 font-weight-2 py-3">{{ $t('trendingSearch') }}</div>
        <v-spacer></v-spacer>
        <div
          v-if="!isMobile"
          class="font-weight-2 font-size-14 py-3 primary-color-1 float-right custom-link hover-custom-link"
        >
          <span class="py-1">{{ $t('seeMore') }}</span>
          <v-icon class="primary-color-1 pb-1" size="20px">mdi-chevron-right</v-icon>
        </div>
      </v-row>
    </v-card-title>

    <v-carousel
      :show-arrows="false"
      light
      touchless
      :cycle="true"
      hide-delimiters
      hide-delimiter-background
      height="270"
      class="px-3"
    >
      <template v-for="(item, index) in filterTrendingSearchItems">
        <v-carousel-item
          v-if="(index + 1) % quantityItemsInCarousel === 1 || quantityItemsInCarousel === 1"
          :key="index"
        >
          <v-row class="pt-3 mx-0">
            <template v-for="(n, i) in quantityItemsInCarousel">
              <template v-if="+index + i < filterTrendingSearchItems.length">
                <v-col class="pa-0" :key="i">
                  <v-card
                    height="150"
                    width="270"
                    v-if="+index + i < filterTrendingSearchItems.length"
                    class="border-custom-4 mx-auto"
                  >
                    <v-card-title>
                      <v-row align="center" class="mx-0 pt-3">
                        <v-col class="pa-0 ma-0">
                          <v-img
                            height="110px"
                            width="110px"
                            aspect-ratio="4.2"
                            class="mr-3"
                            :src="filterTrendingSearchItems[+index + i].img"
                          ></v-img>
                        </v-col>
                        <v-col class="pa-0">
                          <div class="font-size-16 font-weight-3" style="letter-spacing: normal !important">
                            {{ filterTrendingSearchItems[+index + i].name }}
                          </div>
                          <div class="font-size-12 font-weight-1">
                            {{ filterTrendingSearchItems[+index + i].qty }} sản phẩm
                          </div>
                        </v-col>
                      </v-row>
                    </v-card-title>
                  </v-card>
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
import Vue from 'vue';

export default Vue.extend({
  data() {
    return {
      trendings: [
        {
          name: 'Laptop',
          qty: 120,
          img: 'https://phucanhcdn.com/media/product/37180_inspiron_7490_ha2.jpg',
        },
        {
          name: 'Máy xay sinh tố',
          qty: '1220+',
          img: 'https://cdn01.dienmaycholon.vn/filewebdmclnew/public/picture/product/product16844/product_16844_1.png',
        },
        {
          name: 'Tủ lạnh, tủ đông',
          qty: 120,
          img: 'https://i.ytimg.com/vi/-BrUKtdmxHs/maxresdefault.jpg',
        },
        {
          name: 'Loa máy tính',
          qty: 120,
          img: 'https://cdn.nguyenkimmall.com/images/thumbnails/696/522/detailed/298/10023358-loa-vi-tinh-microlab-m-108-1.jpg',
        },
        {
          name: 'Tủ lạnh, tủ đông',
          qty: 120,
          img: 'https://i.ytimg.com/vi/-BrUKtdmxHs/maxresdefault.jpg',
        },
        {
          name: 'Loa máy tính',
          qty: 120,
          img: 'https://cdn.nguyenkimmall.com/images/thumbnails/696/522/detailed/298/10023358-loa-vi-tinh-microlab-m-108-1.jpg',
        },
      ],
    };
  },
  filters: {
    reduceText: function (text: string, max: number) {
      return text.length > max ? text.slice(0, max - 2) + '...' : text;
    },
  },
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    filterTrendingSearchItems(): any[] {
      console.log(
        this.trendings.length,
        this.quantityItemsInCarousel,
        this.trendings.length / this.quantityItemsInCarousel,
        Math.floor(this.trendings.length / this.quantityItemsInCarousel) * this.quantityItemsInCarousel
      );
      return this.trendings.slice(
        0,
        Math.floor(this.trendings.length / this.quantityItemsInCarousel) * this.quantityItemsInCarousel
      );
    },
    quantityItemsInCarousel(): number {
      if (this.$vuetify.breakpoint.xl) return 4;
      if (this.$vuetify.breakpoint.lg) return 4;
      if (this.$vuetify.breakpoint.md) return 3;
      if (this.$vuetify.breakpoint.sm) return 2;
      return 2;
    },
  },
});
</script>

<style lang="scss" scoped>
.trending-search {
  background: white;
  div {
    letter-spacing: normal !important;
  }
}
</style>

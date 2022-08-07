<template>
  <v-col sm="12" md="12" cols="12" :class="isMobile ? 'py-0' : 'py-3'" class="trending-brand">
    <div class="mt-2 pa-0">
      <v-card-title class="trending-page-name font-size-32 font-weight-3 px-0 mt-2 mx-0">
        {{ $t('searchProducts') }}
        <v-spacer></v-spacer>
        <div
          v-if="!isMobile"
          class="font-weight-2 font-size-14 py-3 primary-color-1 float-right custom-link hover-custom-link"
        >
          <span class="py-1">{{ $t('seeMore') }}</span>
          <v-icon class="primary-color-1 pb-1" size="20px">mdi-chevron-right</v-icon>
        </div>
      </v-card-title>
      <v-row class="mx-0" no-gutters>
        <v-col class="pa-0" :key="item.name" v-for="item in trendingSearchProductItems" :cols="columns">
          <v-hover v-slot="{ hover }">
            <router-link class="custom-link" :to="item.name">
              <v-card
                :elevation="hover ? 3 : 1"
                :style="hover ? 'z-index: 50' : ''"
                class="border-custom-6 pa-4 mx-0 rounded-0"
              >
                <v-img
                  contain
                  aspect-ratio="1.2"
                  min-height="80"
                  height="100%"
                  class="ma-auto rounded-0"
                  :src="item.image"
                ></v-img>
                <div class="title-trending-search font-size-14 font-weight-bold text-left">
                  {{ item.name }}
                </div>
                <div class="primary-color-4 font-size-12 font-weight-medium text-left">
                  {{ item.quantity }}
                </div>
              </v-card>
            </router-link>
          </v-hover>
        </v-col>
      </v-row>
    </div>
  </v-col>
</template>

<script lang="ts">
import { initial } from 'lodash';
import Vue from 'vue';

export default Vue.extend({
  data() {
    return {
      trendingSearchProductItems: [] as any[],
    };
  },
  async created() {
    await this.initialize();
  },
  methods: {
    async initialize() {
      this.trendingSearchProductItems = [
        {
          name: 'Son Kem Lì',
          quantity: '43.304+ sản phẩm',
          image: require('@/assets/image/brand/lenovo/brand.png'),
        },
        {
          name: 'Áo Thun Form Rộng Ngắn Tay Unisex',
          quantity: '68.689+ sản phẩm',
          image: require('@/assets/image/brand/lenovo/brand.png'),
        },
        {
          name: "Nước Tẩy Trang L'Oreal",
          quantity: '78.479+ sản phẩm',
          image: require('@/assets/image/brand/lenovo/brand.png'),
        },
        {
          name: 'Sữa Rửa Mặt',
          quantity: '53.867+ sản phẩm',
          image: require('@/assets/image/brand/lenovo/brand.png'),
        },
        {
          name: 'Mắt Kính Gọng Tròn',
          quantity: '46.893+ sản phẩm',
          image: require('@/assets/image/brand/lenovo/brand.png'),
        },
        {
          name: 'Ốp Lưng Iphone',
          quantity: '161.005+ sản phẩm',
          image: require('@/assets/image/brand/lenovo/brand.png'),
        },
        {
          name: 'Áo Sơmi Nam Ngắn Tay',
          quantity: '54.942+ sản phẩm',
          image: require('@/assets/image/brand/lenovo/brand.png'),
        },

        {
          name: 'Huyết thanh bình thường',
          quantity: '52.206+ sản phẩm',
          image: require('@/assets/image/brand/lenovo/brand.png'),
        },

        {
          name: 'Áo Thun Polo Nam Ngắn Tay',
          quantity: '72.371+ sản phẩm',
          image: require('@/assets/image/brand/lenovo/brand.png'),
        },

        {
          name: 'Quần Ống Rộng Nữ',
          quantity: '64.052+ sản phẩm',
          image: require('@/assets/image/brand/lenovo/brand.png'),
        },

        {
          name: 'Bông Tẩy Trang 3 Lớp Cotton Pads',
          quantity: '113.374+ sản phẩm',
          image: require('@/assets/image/brand/lenovo/brand.png'),
        },

        {
          name: 'Top bán chạy',
          quantity: '0+ sản phẩm',
          image: require('@/assets/image/brand/lenovo/brand.png'),
        },
      ];
    },
  },
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    columns(): number {
      if (this.$vuetify.breakpoint.xl) return 2;
      if (this.$vuetify.breakpoint.lg) return 2;
      if (this.$vuetify.breakpoint.md) return 2;
      if (this.$vuetify.breakpoint.sm) return 2;
      return 6;
    },
  },
});
</script>

<style lang="scss" scoped>
.trending-brand {
  width: 100%;
  .trending-page-name {
    margin-bottom: 10px;
  }
  .title-trending-search {
    line-height: 0.3em;
    height: 1.7em; /* height is 2x line-height, so two lines will display */
    overflow: hidden; /* prevents extra lines from being visible */
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}
</style>

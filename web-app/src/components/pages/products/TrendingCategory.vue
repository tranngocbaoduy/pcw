<template>
  <v-col sm="12" md="12" cols="12" :class="isMobile ? 'py-0' : 'py-3'" class="trending-brand">
    <div class="mt-2 pa-0">
      <v-card-title class="trending-page-name font-size-32 font-weight-3 px-0 mt-2 mx-0">
        {{ $t('trendingCategory') }}
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
        <v-col class="pa-0" :key="brand.href" v-for="brand in trendingCategoryItems" :cols="columns">
          <v-hover v-slot="{ hover }">
            <router-link class="custom-link" :to="brand.href">
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
                  :src="brand.img"
                ></v-img>
                <div class="text-center font-weight-bold">{{ brand.name }}</div>
              </v-card>
            </router-link>
          </v-hover>
        </v-col>
      </v-row>
    </div>
  </v-col>
</template>

<script lang="ts">
import Vue from 'vue';
import { CategoryItem } from '@/api/category.service';

export default Vue.extend({
  name: 'CategoryPage',
  props: [],
  components: {},
  data: () => ({
    trendingCategoryItems: [] as any[],
  }),
  async created() {
    this.initialize();
  },
  mounted() {},
  computed: {
    categoryItems(): CategoryItem[] {
      return this.$store.getters.categoryItems || [];
    },
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

  watch: {},
  methods: {
    async initialize() {
      this.trendingCategoryItems = [] as any[];
      const catalog = [
        'Điện thoại',
        'Truyện Tranh',
        'Tủ lạnh',
        'Tác phẩm kinh điển',
        'Tivi',
        'Máy giặt',
        'Balo',
        'Sách nghệ thuật',
        'Kem chống nắng',
        'Tủ',
        'Sách tư duy',
        'Bàn ghế làm việc',
      ];
      for (const i of catalog) {
        this.trendingCategoryItems.push({
          name: i,
          img: require('@/assets/brand/apple/brand.png'),
          logo: require('@/assets/brand/apple/logo.jpg'),
          href: '/category/television/?' + i,
        });
      }
    },
  },
});
</script>

<style lang="scss">
.category-page {
  width: 100%;
  .product-page-name {
    margin-bottom: 10px;
  }
  .product-page-result {
    align-items: center;
  }
  .product-page-quantity {
    width: 200px;
    height: 16px;
  }
  .product-page-filter {
    width: 261px;
    height: 48px;
    align-items: center;
    justify-content: flex-end;
  }
  .product-page-filter-title {
    width: 90px;
    height: 19px;
    margin-right: 15px;
  }
  .product-page-nav-left {
    width: 156px;
    height: 48px;
  }
}
</style>

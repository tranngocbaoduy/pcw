<template>
  <v-col sm="12" md="12" cols="12" :class="isMobile ? 'py-0' : 'py-3'" class="trending-brand">
    <div class="mt-2 pa-0">
      <v-card-title class="trending-page-name font-size-32 font-weight-3 px-0 mt-2 mx-0">
        {{ $t('featureBrand') }}
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
        <v-col class="pa-0" :key="brand.href + brand.name" v-for="brand in brands" :cols="columns">
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
                <v-img
                  height="56px"
                  width="160px"
                  aspect-ratio="4.2"
                  class="ma-auto rounded-0"
                  :src="brand.logo"
                ></v-img>
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

export default Vue.extend({
  data() {
    return {
      brands: [
        {
          name: 'Apple',
          img: require('@/assets/brand/apple/brand.png'),
          logo: require('@/assets/brand/apple/logo.jpg'),
          href: '/category/phone?brandItems=Iphone',
        },
        {
          name: 'Samsung',
          img: require('@/assets/brand/samsung/brand.jpeg'),
          logo: require('@/assets/brand/samsung/logo.png'),
          href: '/category/phone?brandItems=Samsung',
        },
        {
          name: 'LG',
          img: require('@/assets/brand/lg/brand.jpeg'),
          logo: require('@/assets/brand/lg/logo.png'),
          href: '/category/phone?brandItems=Lg',
        },
        {
          name: 'Lenovo',
          img: require('@/assets/brand/lenovo/brand.png'),
          logo: require('@/assets/brand/lenovo/logo.jpeg'),
          href: '/category/phone?brandItems=Lenovo',
        },
        {
          name: 'Apple',
          img: require('@/assets/brand/apple/brand.png'),
          logo: require('@/assets/brand/apple/logo.jpg'),
          href: '/category/phone?brandItems=Iphone',
        },
        {
          name: 'Samsung',
          img: require('@/assets/brand/samsung/brand.jpeg'),
          logo: require('@/assets/brand/samsung/logo.png'),
          href: '/category/phone?brandItems=Samsung',
        },
        {
          name: 'LG',
          img: require('@/assets/brand/lg/brand.jpeg'),
          logo: require('@/assets/brand/lg/logo.png'),
          href: '/category/phone?brandItems=Lg',
        },
        {
          name: 'Lenovo',
          img: require('@/assets/brand/lenovo/brand.png'),
          logo: require('@/assets/brand/lenovo/logo.jpeg'),
          href: '/category/phone?brandItems=Lenovo',
        },
        {
          name: 'Apple',
          img: require('@/assets/brand/apple/brand.png'),
          logo: require('@/assets/brand/apple/logo.jpg'),
          href: '/category/phone?brandItems=Iphone',
        },
        {
          name: 'Samsung',
          img: require('@/assets/brand/samsung/brand.jpeg'),
          logo: require('@/assets/brand/samsung/logo.png'),
          href: '/category/phone?brandItems=Samsung',
        },
        {
          name: 'LG',
          img: require('@/assets/brand/lg/brand.jpeg'),
          logo: require('@/assets/brand/lg/logo.png'),
          href: '/category/phone?brandItems=Lg',
        },
        {
          name: 'Lenovo',
          img: require('@/assets/brand/lenovo/brand.png'),
          logo: require('@/assets/brand/lenovo/logo.jpeg'),
          href: '/category/phone?brandItems=Lenovo',
        },
      ],
    };
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
}
</style>

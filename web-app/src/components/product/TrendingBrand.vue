<template>
  <v-card class="rounded-0 elevation-0 py-6 trending-brand">
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
        <div class="font-size-24 font-weight-2 py-3">{{ $t('featureBrand') }}</div>
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
    <v-row class="mx-0" no-gutters>
      <v-col class="pa-4" :key="brand.href" v-for="brand in brands" :cols="columns">
        <v-hover v-slot="{ hover }">
          <router-link class="custom-link" :to="brand.href">
            <v-card :elevation="hover ? 12 : 2" aspect-ratio="4.2" class="border-custom-4 pa-4 mx-auto">
              <v-img
                aspect-ratio="1.2"
                min-height="80"
                height="100%"
                class="ma-auto rounded-0"
                :src="brand.img"
              ></v-img>
              <v-img height="56px" width="160px" aspect-ratio="4.2" class="ma-auto rounded-0" :src="brand.logo"></v-img>
            </v-card>
          </router-link>
        </v-hover>
      </v-col>
    </v-row>
  </v-card>
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
          img: require('@/assets/brand/lg/brand.jpg'),
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
    filterBrandItems(): any[] {
      if (this.$vuetify.breakpoint.xl) return this.brands.slice(0, 3);
      if (this.$vuetify.breakpoint.lg) return this.brands.slice(0, 3);
      if (this.$vuetify.breakpoint.md) return this.brands.slice(0, 1);
      if (this.$vuetify.breakpoint.sm) return this.brands.slice(0, 1);
      return this.brands;
    },
    columns(): number {
      if (this.$vuetify.breakpoint.xl) return 3;
      if (this.$vuetify.breakpoint.lg) return 3;
      if (this.$vuetify.breakpoint.md) return 3;
      if (this.$vuetify.breakpoint.sm) return 3;
      return 6;
    },
  },
});
</script>

<style lang="scss" scoped>
.trending-brand {
  background: white;
}
</style>

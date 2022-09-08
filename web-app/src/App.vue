<template>
  <v-app style="min-height: 100vh !important">
    <router-view v-if="$route" :key="$route.fullPath" />
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';
import { MetaInfo } from 'vue-meta';
import SeoService from './api/seo.service';

export default Vue.extend({
  name: 'App',
  data: () => ({}),
  computed: {
    isMobile() {
      return this.$store.getters.isMobile;
    },
  },
  metaInfo(): MetaInfo {
    return SeoService.getMetaInfoHomePage();
  },
  async created() {
    console.log('App component is created');
  },
  mounted() {
    this.onResize();
    window.addEventListener('resize', this.onResize, { passive: true });
    window.addEventListener('scroll', this.onResize, { passive: true });
  },
  methods: {
    onResize() {
      const isMobile = !(this.$vuetify.breakpoint.lg || this.$vuetify.breakpoint.xl || this.$vuetify.breakpoint.md);
      if (this.isMobile != isMobile) {
        this.$store.dispatch('setIsMobile', { isMobile: isMobile });
      }
      this.$store.dispatch('setBoxDistance', {
        innerWidth: window.innerWidth,
        innerHeight: window.innerHeight,
        offsetHeight: window.pageYOffset,
      });
      // console.log(isMobile, window.innerWidth, window.pageYOffset);
    },
  },
  beforeDestroy() {
    if (typeof window !== 'undefined') {
      window.removeEventListener('resize', this.onResize, { passive: true } as any);
    }
  },
});
</script>

<style lang="scss">
@import '@/resources/scss/Common.scss';
@import '@/resources/scss/Border.scss';
@import '@/resources/scss/FontSize.scss';
@import '@/resources/scss/FontWeight.scss';
@import '@/resources/scss/LineHeight.scss';
@import '@/resources/scss/PrimaryColor.scss';
@import '@/resources/scss/BackgroundColor.scss';
@import '@/resources/scss/Platform.scss';
@import './App.scss';
</style>

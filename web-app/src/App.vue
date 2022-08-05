<template>
  <v-app>
    <router-view :key="$route.fullPath" />
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';

async function sleep(min: number, max: number) {
  return new Promise((res) => setTimeout(res, Math.floor(Math.random() * (max - min + 1)) + min));
}

export default Vue.extend({
  name: 'App',
  data: () => ({}),
  computed: {
    isMobile() {
      return this.$store.getters.isMobile;
    },
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
      this.$store.dispatch('setBoxDistance', { innerWidth: window.innerWidth, offsetHeight: window.pageYOffset });
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
@import '@/assets/scss/Common.scss';
@import '@/assets/scss/Border.scss';
@import '@/assets/scss/FontSize.scss';
@import '@/assets/scss/FontWeight.scss';
@import '@/assets/scss/LineHeight.scss';
@import '@/assets/scss/PrimaryColor.scss';
@import '@/assets/scss/BackgroundColor.scss';
@import '@/assets/scss/Platform.scss';
@import './App.scss';
</style>

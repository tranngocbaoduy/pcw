<template>
  <div class="home">
    <Header @handle-show-menu="handleShowMenu" :isShowMenu="isShowMenu"> </Header>
    <v-container f class="body-custom" :class="isMobile ? 'pa-0' : ''" :fluid="isFluid">
      <router-view />
    </v-container>
    <v-divider class="divider-custom"></v-divider>
    <Footer></Footer>
    <NavigationMobile v-if="isMobile"></NavigationMobile>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

import NavigationMobile from '@/components/common/NavigationMobile.vue';

import Header from '@/components/common/Header.vue';
import Footer from '@/components/common/Footer.vue';
import CategoryService from '@/api/category.service';

export default Vue.extend({
  name: 'Home',
  data: () => ({
    isShowMenu: false,
  }),
  components: {
    Header,
    NavigationMobile,
    Footer,
  },
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    isShowCarousel(): boolean {
      return this.$route.name == 'HomePage';
    },
    getCategoryItems(): any {
      return this.$store.getters.categoryItems;
    },

    isFluid(): boolean {
      if (this.$vuetify.breakpoint.xl) return false;
      if (this.$vuetify.breakpoint.lg) return false;
      if (this.$vuetify.breakpoint.md) return true;
      if (this.$vuetify.breakpoint.sm) return true;
      return true;
    },
  },
  async created() {
    console.log('Home component is created');
    await this.initialize();
  },
  methods: {
    async initialize() {
      const loading = this.$loading.show();
      let retryCount = 0;
      let categoryItems = null;
      if (!this.getCategoryItems || this.getCategoryItems.length == 0) {
        do {
          categoryItems = await CategoryService.queryAllCategory();
          console.log('categoryItems', categoryItems);
          this.$store.dispatch('setCategory', { categoryItems: await CategoryService.queryAllCategory() });
          await setTimeout(() => {}, 2000);
          retryCount += 1;
        } while (!categoryItems && retryCount < 3);
      }
      loading.hide();
    },
    handleShowMenu() {
      this.isShowMenu = !this.isShowMenu;
    },
  },
});
</script>
<style lang="scss">
.home {
  background-color: #f3f6f8 !important;
  .divider-custom {
    border: #546e7a 20px solid !important;
  }
}
</style>

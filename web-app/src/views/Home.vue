<template>
  <div
    class="home bg-primary-color-0 d-flex-column align-center justify-space-between"
    :style="`min-height: 100vh !important;`"
  >
    <Header @handle-show-menu="handleShowMenu" :isShowMenu="isShowMenu" v-if="!isMobileAndHomePage" />
    <v-container class="body-custom" :class="isMobile ? 'pa-0' : 'px-0'" :fluid="isFluid">
      <router-view />
    </v-container>
    <v-divider v-if="!isMobileAndHomePage" class="divider-custom"></v-divider>
    <Footer v-if="!isMobileAndHomePage" />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
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
    // NavigationMobile,
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
    innerHeight(): number {
      return this.$store.getters.innerHeight;
    },
    isFluid(): boolean {
      if (this.$vuetify.breakpoint.xl) return false;
      if (this.$vuetify.breakpoint.lg) return false;
      if (this.$vuetify.breakpoint.md) return true;
      if (this.$vuetify.breakpoint.sm) return true;
      return true;
    },
    isMobileAndHomePage(): boolean {
      return this.isMobile && this.$route.path == '/';
    },

    categoryIdInRoute(): string {
      return this.$route.params['idCate'] || '';
    },
  },
  async created() {
    console.log('Home component is created');
    await this.initialize();
  },
  methods: {
    async initialize() {
      const categoryItems = await CategoryService.queryAllCategory();
      console.log(
        this.categoryIdInRoute,
        categoryItems.find((c) => c.id == this.categoryIdInRoute)
      );
      this.$store.dispatch('setCategory', {
        categoryItems: categoryItems,
        selectedCategory: categoryItems.find((c) => c.id == this.categoryIdInRoute),
      });
    },
    handleShowMenu() {
      this.isShowMenu = !this.isShowMenu;
    },
  },
});
</script>
<style lang="scss">
.home {
  .divider-custom {
    border: #546e7a 20px solid !important;
  }
}
</style>

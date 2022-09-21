<template>
  <v-col sm="12" md="12" cols="12" :class="isMobile ? 'py-0' : 'py-3'" class="trending-category px-0">
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
      <v-row class="mx-0" no-gutters v-if="listItem && listItem.length">
        <v-col class="pa-0" :key="category.href" v-for="category in filterListItem" :cols="columns">
          <v-hover v-slot="{ hover }">
            <router-link class="custom-link" :to="category.href">
              <v-card
                :elevation="hover ? 3 : 1"
                :style="hover ? 'z-index: 50' : ''"
                class="border-custom-6 pa-1 py-4 mx-0 rounded-0"
              >
                <v-img
                  v-if="category.image"
                  :class="hover ? 'mt-2' : 'mt-4'"
                  style="width: 164px; height: 164px"
                  contain
                  class="ma-auto rounded-0"
                  :src="category.image"
                ></v-img>
                <div class="text-center font-weight-bold my-1">{{ categoryName(category.name) }}</div>
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
  name: 'CategoryPage',
  props: ['listItem'],
  components: {},
  data: () => ({}),
  async created() {},
  mounted() {},
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
    filterListItem(): any[] {
      return this.listItem.filter((i: any) => i.image);
    },
  },

  watch: {},
  methods: {
    categoryName(categoryId: string): string {
      return categoryId ? this.$t(`category.${categoryId}`).toString() : '';
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

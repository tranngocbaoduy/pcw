<template>
  <div>
    <v-row class="category-page pt-0 mt-0" no-gutters :class="isMobile ? 'pa-0' : 'pa-2 '">
      <v-col sm="12" md="12" cols="12" :class="isMobile ? 'py-0' : 'py-3'">
        <div class="mt-2 pa-0">
          <v-card-title class="product-page-name font-size-32 font-weight-3 px-0 mt-2 mx-0">
            {{ $t('recommendProducts') }}
            <v-spacer></v-spacer>
            <div
              v-if="!isMobile"
              class="font-weight-2 font-size-16 py-3 primary-color-1 float-right custom-link hover-custom-link"
              @click="handleChangeToCategory"
            >
              <span class="py-1">{{ $t('seeMore') }}</span>
              <v-icon class="primary-color-1 pb-1" size="20px">mdi-chevron-right</v-icon>
            </div>
          </v-card-title>
        </div>
        <div v-if="filterProductItems && filterProductItems.length != 0" class="mt-0">
          <v-row no-gutters>
            <v-col
              :key="item['SK']"
              v-for="item in filterProductItems"
              :style="$vuetify.breakpoint.mdAndUp ? ' flex: 1 0 18%;' : ''"
              cols="6"
              sm="3"
            >
              <router-link class="custom-link" :to="`${getSlugId(item)}`">
                <Product :item="item" />
              </router-link>
            </v-col>
          </v-row>
        </div>
        <v-row v-else>
          <v-img :src="noItemImage" max-height="800" max-width="90%" height="400" class="ma-auto" />
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Product from '@/components/product/Product.vue';
import ProductService, { ProductItem } from '@/api/product.service';
import { CategoryItem } from '@/api/category.service';

export default Vue.extend({
  name: 'CategoryPage',
  props: [],
  components: {
    Product,
  },
  data: () => ({
    noItemImage: require('@/assets/banner/no-product.png'),
    limit: 10,
    quantity: 10,
    page: 1,
    productItems: [] as ProductItem[],
    randomCategory: {} as CategoryItem,
    randomPathChangeTo: '',
    isLoading: true,
  }),
  async created() {
    this.page = 1;
    await this.initialize();
    this.isLoading = false;
  },
  mounted() {},
  computed: {
    categoryItems(): CategoryItem[] {
      return this.$store.getters.categoryItems || [];
    },
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    filterProductItems(): ProductItem[] {
      const number = parseInt((this.productItems.length / 5).toString());
      return this.productItems.slice(0, number * 5);
    },
  },

  watch: {
    async page() {
      if (this.page) {
        if (this.$route.query.page == this.page.toString()) {
          const query = { ...this.$route.query, page: this.page.toString() };
          this.$router.replace({ query: query || {} });
        }
      }
    },
    async categoryItems() {
      this.randomCategory = this.categoryItems[Math.floor(Math.random() * this.categoryItems.length)];
      this.randomPathChangeTo = `/category/${this.randomCategory.SK}`;
    },
  },
  methods: {
    async initialize() {
      window.scrollTo({ top: 0, left: 0 });
      this.page = parseInt((this as any).$route.query.page || 1);
      this.$store.commit('setState', { searchString: this.$route.query.name });
      await this.loadProductItemByTarget();
    },
    handleChangeToCategory() {
      if (this.randomPathChangeTo) this.$router.push(this.randomPathChangeTo);
    },
    async loadProductItemByTarget() {
      this.productItems = await ProductService.queryItemByTarget({
        category: '408011' || this.randomCategory.SK,
        limit: this.limit,
        page: this.page,
        agencyItems: [],
        brandItems: [],
        minPrice: 0,
        maxPrice: 1000000000,
      });
      console.log('this.productItems', this.productItems);
    },
    getSlugId(item: ProductItem): string {
      return ProductService.getSlugId(item);
    },
    getIdProduct(item: ProductItem) {
      if (item['SK'].includes('REP')) return item['SK'].split('#').join('_');
      if (item['SK'].includes('CHILD')) {
        const newSK = item['SK']
          .split('#')
          .slice(0, item['SK'].split('#').length - 1)
          .join('_');
        return `${newSK.split('CHILD').join('REP')}_${item.relationshipID}`;
      }
      return '';
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

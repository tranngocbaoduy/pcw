<template>
  <v-row class="py-8" no-gutters :style="marginGird">
    <v-col
      class="px-2"
      v-for="(item, index) in filterCategories"
      :key="index"
      :cols="columns"
      style="text-decoration: none"
    >
      <router-link :to="`/category/${filterCategories[+index]['id']}`">
        <v-hover v-slot="{ hover }">
          <v-card
            height="164"
            width="130"
            class="border-custom-4 py-3 mx-auto"
            :class="hover ? 'custom-background' : ''"
          >
            <v-img
              :height="isMobile ? 100 : 80"
              :width="isMobile ? 100 : 80"
              aspect-ratio="0.2"
              class="ma-auto"
              :src="hover ? item.imgOn : item.imgOff"
            ></v-img>
            <v-card-title
              class="justify-center font-size-16 text-center font-weight-3 py-0"
              style="text-decoration: none"
              >{{ item.name }}</v-card-title
            >
          </v-card>
        </v-hover>
      </router-link>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import CategoryService, { CategoryItem } from '@/api/category.service';
import Vue from 'vue';

export default Vue.extend({
  data() {
    return {
      categoryItems: [] as CategoryItem[],
    };
  },
  computed: {
    categories() {
      return [
        // {
        //   id: 'phone',
        //   name: this.$t('category.Phone'),
        //   imgOff: require('@/assets/icon/Blue/smartphone@2x.png'),
        //   imgOn: require('@/assets/icon/White/smartphone@2x.png'),
        // },
        // {
        //   id: 'television',
        //   name: this.$t('category.Television'),
        //   imgOff: require('@/assets/icon/Blue/television-screen@2x.png'),
        //   imgOn: require('@/assets/icon/White/television-screen@2x.png'),
        // },
        // {
        //   id: 'fridge',
        //   name: this.$t('category.Fridge'),
        //   imgOff: require('@/assets/icon/Blue/fridge@2x.png'),
        //   imgOn: require('@/assets/icon/White/fridge@2x.png'),
        // },
        // {
        //   id: 'washing',
        //   name: this.$t('category.Washing'),
        //   imgOff: require('@/assets/icon/Blue/washing-machine@2x.png'),
        //   imgOn: require('@/assets/icon/White/washing-machine@2x.png'),
        // },
      ];
    },
    filterCategories(): any[] {
      return this.isMobile ? this.categories.slice(0, 3) : this.categories;
    },
    isMobile() {
      return this.$store.getters.isMobile;
    },
    marginGird() {
      if (this.$vuetify.breakpoint.xl || this.$vuetify.breakpoint.lg) {
        return 'margin-left: 220px; margin-right: 220px';
      }
      if (this.$vuetify.breakpoint.md) {
        return 'margin-left: 110px; margin-right: 110px';
      }
      return '';
    },
    columns(): number {
      if (this.$vuetify.breakpoint.xl) return 4;
      if (this.$vuetify.breakpoint.lg) return 4;
      if (this.$vuetify.breakpoint.md) return 4;
      if (this.$vuetify.breakpoint.sm) return 4;
      return 4;
    },
  },

  async created() {
    await this.initialize();
  },

  filters: {
    reduceText: function (text: string, max: number) {
      return text.length > max ? text.slice(0, max - 2) + '...' : text;
    },
  },

  methods: {
    async initialize() {
      this.categoryItems = await CategoryService.queryAllCategory();
      this.$store.dispatch('setCategory', { categoryItems: this.categoryItems });
    },
  },
});
</script>

<style lang="scss">
.custom-background {
  background-color: #263238 !important;
  color: white !important;
  text-decoration: none;
  text-decoration-color: red;
}
</style>

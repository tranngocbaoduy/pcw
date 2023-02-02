<template>
  <div class="footer pt-9 pb-3">
    <v-container>
      <v-row no-gutters>
        <v-col cols="6" md="3" sm="4" class="pa-2">
          <v-card-title class="font-size-18 primary-color-1 font-weight-4 pa-0 mb-4">{{ $t('aboutUs') }}</v-card-title>
          <v-card-text class="font-size-14 font-weight-2 pa-0">{{ $t('aboutUsContent') }} </v-card-text>
        </v-col>
        <v-col cols="6" md="3" sm="2" class="pa-2" v-if="listCategoryName && listCategoryName.length != 0">
          <v-card-title class="font-size-18 primary-color-1 font-weight-4 pa-0 mb-4">{{ $t('catalog') }}</v-card-title>
          <router-link
            class="custom-link"
            :to="`/category/${category.id}`"
            v-for="category in listCategoryName"
            :key="category.id"
          >
            <v-card-text class="custom-link black--text font-size-14 font-weight-2 my-1 pa-0"
              >{{ category.name }}
            </v-card-text>
          </router-link>
        </v-col>

        <v-col cols="6" md="3" sm="4" class="pa-2">
          <v-card-title class="font-size-18 primary-color-1 font-weight-4 pa-0 mb-4">{{ $t('linking') }}</v-card-title>
          <v-card-text
            class="font-size-14 font-weight-2 pa-0 my-1"
            v-for="link in links"
            :key="link"
            @click="$router.push(`/category/phone?agencyItems=${link}`)"
          >
            {{ link }}
          </v-card-text>
        </v-col>
        <v-col cols="6" md="3" sm="2" class="pa-2">
          <v-card-title class="font-size-18 primary-color-1 font-weight-4 pa-0 mb-2">{{ $t('contact') }}</v-card-title>
          <v-card-text class="font-size-14 font-weight-2 pa-0">
            <div class="mb-2">Email: <span class="primary-color-1 font-weight-5">duytnb2608.work@gmail.com</span></div>
            <div class="mb-2">Phone: (+84) 79 333 5049</div>
            <div>
              <v-btn class="mr-3" v-for="icon in icons" :key="icon" icon>
                <v-icon size="24px">
                  {{ icon }}
                </v-icon>
              </v-btn>
            </div>
          </v-card-text>
        </v-col>
        <v-col cols="12" class="font-size-12 text-center pt-4">
          Giá cả hiển thị có thể cao hơn so với lần cập nhật gần nhất. Chúng tôi luôn cố gắng cập nhật giá mới nhất
          trong thời gian ngắn nhất.<br />
          © {{ new Date().getFullYear() }} PCW - Price Comparasion Website. <br />All rights reserved. <br />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script lang="ts">
import { CategoryItem } from '@/api/category.service';
import Vue from 'vue';

export default Vue.extend({
  name: 'Footer',
  data: () => ({
    links: ['Shopee', 'Tiki', 'Lazada'], //, 'Lazada', 'Điện máy xanh', 'FPT Shop', 'Nguyễn Kim'],
    icons: ['mdi-facebook', 'mdi-instagram'],
  }),
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    listCategoryName(): any[] {
      return this.$store.getters.categoryItems.filter((i: CategoryItem) => i.isLeaf).slice(0, 4);
    },
  },
  methods: {
    // categoryName(categoryId: string): string {
    //   return categoryId ? this.$t(`category.${categoryId}`).toString() : '';
    // },
  },
});
</script>

<style lang="scss">
@import '@/resources/scss/FontWeight.scss';
.footer {
  background-color: #f0f3f5 !important;
}
</style>

<template>
  <div class="header elevation-3">
    <v-toolbar class="py-3 toolbar-header" min-width="100%" :min-height="isMobile ? '80px' : '90px'">
      <router-link class="custom-link pa-2" :to="`/`">
        <v-img
          max-height="56"
          max-width="156"
          :height="isMobile ? 36 : 56"
          :width="isMobile ? 102 : 156"
          :src="require('@/assets/Light.png')"
          alt=""
        >
        </v-img>
      </router-link>
      <v-spacer></v-spacer>
      <v-autocomplete
        class="border-radius-8 elevation-0"
        single-line
        validate-on-blur
        full-width
        :items="productSearchItems"
        hide-details
        flat
        background-color="#eceff1"
        :placeholder="$t('search')"
        color="#ECEFF1"
        solo
        hide-selected
        allow-overflow
        v-model="value"
        item-text="name"
        item-value="code"
        :no-data-text="$t('No products found!!!')"
        hide-no-data
        hint
        :menu-props="{
          closeOnClick: false,
          closeOnContentClick: false,
          disableKeys: true,
          openOnClick: false,
          maxHeight: 400,
          minWidth: isMobile ? innerWidth : 440,
          maxWidth: isMobile ? innerWidth : 440,
          nudgeBottom: isMobile ? 12 : 0,
          offsetY: true,
          offsetOverflow: true,
          transition: false,
          overflowY: true,
        }"
        disable-lookup
        @keyup="searchProduct"
        :search-input.sync="searchCode"
      >
        <template v-slot:append>
          <v-fade-transition hide-on-leave>
            <v-progress-circular v-if="isLoading" size="24" color="info" indeterminate></v-progress-circular>
            <v-btn
              color="#1859db"
              v-else
              width="48"
              height="48"
              style="color: white"
              @click="searchProduct"
              class="border-radius-8 mr-n2"
            >
              <v-icon size="24">mdi-magnify</v-icon>
            </v-btn>
          </v-fade-transition>
        </template>
      </v-autocomplete>
      <v-spacer v-if="!isMobile"></v-spacer>

      <v-menu v-if="!isMobile" :close-on-click="true" bottom right nudge-bottom="40">
        <template v-slot:activator="{ on, attrs }">
          <v-btn color="white" tile elevation="0" light v-bind="attrs" retain-focus-on-click v-on="on">
            <v-avatar size="24">
              <img :src="localeLanguage.flag" :alt="localeLanguage.name" />
            </v-avatar>
            <span class="px-2"> {{ `${localeLanguage.code.toUpperCase()}` }}</span>
          </v-btn>
        </template>

        <v-list>
          <v-list-item
            v-for="(item, index) in localeLanguageItems"
            :key="index"
            @click="handleChangeLanguage(item)"
            class="hover-custom-link"
          >
            <v-avatar size="24">
              <img :src="item.flag" :alt="item.name" />
            </v-avatar>
            <v-list-item-title class="px-3">{{ item.name }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <!-- <v-btn icon>
        <v-icon size="24">mdi-apps</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon size="24">mdi-dots-vertical</v-icon>
      </v-btn> -->
    </v-toolbar>
  </div>
</template>

<script lang="ts">
async function sleep(min: number, max: number) {
  return new Promise((res) => setTimeout(res, Math.floor(Math.random() * (max - min + 1)) + min));
}
import Vue from 'vue';
import i18n from '@/i18n';
import { ProductSearchItem } from '@/api/product.service';

export default Vue.extend({
  name: 'Header',
  props: ['isShowMenu'],
  // components: { AccountMenu },
  data: () => ({
    isLoading: false,
    value: null,
    searchCode: '',
    cacheSearchCode: '',
    beforeCategory: '',
    localeLanguage: {} as any,

    debouncedQuery: Function,
  }),
  computed: {
    innerWidth(): number {
      return this.$store.getters.innerWidth;
    },
    localeLanguageItems() {
      return [
        {
          code: 'vn',
          name: this.$t('vn'),
          flag: require('@/assets/flag/vietnam.png'),
        },
        {
          code: 'en',
          name: this.$t('en'),
          flag: require('@/assets/flag/united-kingdom.png'),
        },
      ];
    },
    listCategoryName(): string[] {
      return [
        {
          PK: 'CATEGORY',
          SK: 'TatCa',
          NameVN: 'Tất cả',
        },
        ...this.$store.getters.categoryItems,
      ];
    },
    categoryId(): string {
      return this.$route.params['idCate'] || '';
    },
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    productSearchItems(): ProductSearchItem[] {
      return [
        {
          PK: 'a',
          SK: 'b',
          name: 'some thing 1',
        },
        {
          PK: 'a',
          SK: 'b',
          name: 'who is 3',
        },
        {
          PK: 'a',
          SK: 'b',
          name: 'this si',
        },
        {
          PK: 'a',
          SK: 'b',
          name: 'where are',
        },
      ];
    },
    // allProductName(): any[] {
    //   let items = this.$store.getters.allProductName as string[];

    //   if (this.selectedCategory && this.selectedCategory.SK && this.selectedCategory.SK != 'TatCa') {
    //     const mappingId = (this as any).mappingCategoryId[this.selectedCategory.SK];
    //     items = items.filter((item: string) => item.includes(mappingId));
    //   } else if (this.categoryId && !this.selectedCategory) {
    //     items = items.filter((item: string) => item.includes(this.categoryId));
    //   }

    //   return items.map((item: string) => {
    //     const ele = item.split('#');
    //     return {
    //       category: ele[0],
    //       code: ele[1],
    //       name: ele[2],
    //       wholeSent: item,
    //     };
    //   });
    // },
  },
  watch: {},
  methods: {
    handleShowMenu() {
      this.$emit('handle-show-menu');
    },
    handleChangeLanguage(item: any) {
      this.localeLanguage = item;
      if (this.localeLanguage != i18n.locale) i18n.locale = (this as any).localeLanguage.code as string;
      console.log('i18n.locale', i18n.locale);
    },
    async searchProduct(event: any) {
      this.isLoading = true;
      if (this.value) {
        const item = null as any;
        if (item) {
          const ele = item.split('#');
          const categoryId = ele[0];
          const code = ele[1];
          this.cacheSearchCode = code;
          this.$router.replace(`/category/${categoryId}/product/${code}`);
        }
      }
      if (event.code == 'Enter' && this.searchCode) {
        this.debouncedQuery();
        this.updateUrlQuery(this.searchCode);
      }
      await sleep(200, 200);
      this.isLoading = false;
    },
    searchItem() {
      if (this.searchCode) {
        this.value = null;
        console.log('value', this.searchCode);
        // const strFound = this.allProductName.find((item: any) => item.name.search(this.searchCode));
        // this.$store.commit('setState', { searchString: this.searchCode });
        // if (strFound && (this.$route.name != 'CategoryPage' || this.beforeCategory !== strFound.category)) {
        //   this.beforeCategory = strFound.category;
        //   this.$router.replace(`/category/${strFound.category}?name=${this.searchCode}`);
        // }
      }

      this.isLoading = false;
    },
    updateUrlQuery(query: string) {
      const urlParams = new URLSearchParams(window.location.search);
      urlParams.set('query', query);
      const queryUrl = urlParams.toString();
      history.replaceState({}, '', `${this.$route.path}?${queryUrl}`);
    },
    setValue(obj: any, path: string, value: any) {
      const a = path.split('.');
      let o = obj;
      while (a.length - 1) {
        const n: any = a.shift();
        if (!(n in o)) o[n] = {};
        o = o[n];
      }
      o[a[0]] = value;
    },

    getValue(obj: any, path: string) {
      path = path.replace(/\[(\w+)\]/g, '.$1');
      path = path.replace(/^\./, '');
      const a = path.split('.');
      let o = obj;
      while (a.length) {
        const n: any = a.shift();
        if (!(n in o)) return;
        o = o[n];
      }
      return o;
    },
  },
  created() {
    this.localeLanguage = this.localeLanguageItems[0] as any;
    this.debouncedQuery = (this as any)._.debounce(() => {
      this.searchItem();
    }, 500);
  },
});
</script>

<style lang="scss">
@import '@/assets/scss/Common.scss';
.header {
  .nav-left {
    width: 100px;
  }
  @include for_breakpoint(mobile tablet) {
    .v-toolbar__content {
      padding: 4px;
    }
  }

  .v-menu__content.v-autocomplete__content {
    left: 600px !important;
    min-width: 700px !important;
  }
  @include for_breakpoint(mobile tablet) {
    position: sticky;
    top: 0px;
    z-index: 1000;
  }
  .toolbar-header {
    padding: 0 80px;

    @include for_breakpoint(mobile tablet) {
      padding: 0px;
    }
  }
}
</style>

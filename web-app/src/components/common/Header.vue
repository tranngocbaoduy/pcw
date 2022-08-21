<template>
  <div class="elevation-0 header">
    <v-toolbar class="py-3 toolbar-header" min-width="100%" :min-height="isMobile ? '80px' : '90px'">
      <router-link class="custom-link pa-2" :to="`/`">
        <v-img
          max-height="56"
          max-width="156"
          :height="isMobile ? 36 : 56"
          :width="isMobile ? 102 : 156"
          :src="require('@/assets/image/logo/Light.png')"
          alt=""
        >
        </v-img>
      </router-link>
      <v-spacer></v-spacer>

      <div style="width: 700px" class="pb-0 pt-4">
        <v-autocomplete
          class="rounded-md elevation-1 mr-4"
          @blur="isFocus = false"
          @click="isFocus = true"
          style="box-shadow: none !important"
          :style="isFocus ? 'border: #1859db 1px solid;' : 'border: #ddd6d6 0.6px solid;'"
          validate-on-blur
          :items="productSearchItems"
          hide-details
          flat
          background-color="white"
          :placeholder="placeholder"
          color="#ECEFF1"
          solo
          allow-overflow
          item-value="cleanName"
          v-model="valueText"
          :no-data-text="$t('Let search somthing!')"
          :filter="filterItems"
          :menu-props="{
            closeOnClick: false,
            closeOnContentClick: false,
            disableKeys: true,
            openOnClick: false,
            maxHeight: 700,
            minWidth: widthMenu,
            maxWidth: widthMenu,
            nudgeBottom: isMobile ? 12 : 2,
            offsetY: true,
            elevation: 0,
            offsetOverflow: true,
            transition: false,
            overflowY: true,
          }"
          :disable-lookup="true"
          @keyup="searchProduct"
          :search-input.sync="searchCode"
        >
          <template v-slot:append>
            <v-fade-transition hide-on-leave>
              <v-progress-circular v-if="isLoading" size="24" color="info" indeterminate></v-progress-circular>
              <v-btn
                color="transparent"
                v-else
                width="48"
                height="32"
                style="color: white"
                @click="searchProduct"
                class="border-radius-0 elevation-0 mr-n6"
              >
                <v-icon color="#1859db" size="24">mdi-magnify</v-icon>
              </v-btn>
            </v-fade-transition>
          </template>
          <!-- <template v-slot:no-data>
            <v-list-item>
              <div class="d-flex-col align-center justify-center">
                <v-card elevation="0" class="rounded-0 pa-0" width="680">
                  <v-card-title class="pa-1 font-weight-bold font-size-18">Danh mục</v-card-title>
                  <v-card-text class="pa-1 font-size-12">
                    <v-chip-group
                      active-class="primary--text"
                      column
                      @click="
                        () => {
                          this.selectedCategory = [];
                        }
                      "
                      v-model="selectedCategory"
                    >
                      <v-chip
                        :draggable="false"
                        small
                        class="font-size-12 font-color-customer font-weight-bold bg-primary-color-0"
                        v-for="category in listCategoryName"
                        :key="`${category.name}-category-on-search`"
                        :to="`/category/${category.SK}`"
                      >
                        {{ categoryName(category.name) }}
                      </v-chip>
                    </v-chip-group>
                  </v-card-text>
                </v-card>
                <v-card elevation="0" class="rounded-0 pa-0">
                  <v-card-title class="pa-1 font-weight-bold font-size-18">Danh mục</v-card-title>
                  <v-card-text class="pa-1 font-size-12">
                    <v-chip-group
                      active-class="primary--text"
                      column
                      @click="
                        () => {
                          this.selectedCategory = [];
                        }
                      "
                      v-model="selectedCategory"
                    >
                      <v-chip
                        :draggable="false"
                        small
                        class="font-size-12 font-color-customer font-weight-bold bg-primary-color-0"
                        v-for="category in listCategoryName"
                        :key="`${category.name}-category-on-search`"
                        :to="`/category/${category.SK}`"
                      >
                        {{ categoryName(category.name) }}
                      </v-chip>
                    </v-chip-group>
                  </v-card-text>
                </v-card>
              </div>
            </v-list-item>
          </template> -->
          <template v-slot:prepend-item>
            <v-list-item>
              <div class="d-flex-col align-center justify-center">
                <v-card elevation="0" class="rounded-0 pa-0" :width="widthMenu">
                  <v-card-title class="pa-1 font-weight-bold font-size-18">Danh mục</v-card-title>
                  <v-card-text class="pa-1 font-size-12">
                    <v-chip-group
                      active-class="primary--text"
                      column
                      @click="
                        () => {
                          this.selectedCategory = [];
                        }
                      "
                      v-model="selectedCategory"
                    >
                      <v-chip
                        :draggable="false"
                        small
                        class="font-size-12 font-color-customer font-weight-bold bg-primary-color-0"
                        v-for="category in listCategoryName"
                        :key="`${category.name}-category-on-search`"
                        :to="`/category/${category.SK}`"
                      >
                        {{ categoryName(category.name) }}
                      </v-chip>
                    </v-chip-group>
                  </v-card-text>
                </v-card>
                <v-card elevation="0" class="rounded-0 pa-0" v-if="productSearchItems && productSearchItems.length > 0">
                  <v-card-title class="pa-1 font-weight-bold font-size-18">Sản phẩm gợi ý</v-card-title>
                </v-card>
              </div>
            </v-list-item>
          </template>
          <!-- <template v-slot:selection="{ attr, on, item, selected }">
            <v-chip v-bind="attr" :input-value="selected" color="blue-grey" class="white--text" v-on="on">
              <v-icon left> mdi-bitcoin </v-icon>
              dsa
              <span v-text="item.code"></span>
            </v-chip>
          </template> -->
          <template v-slot:item="{ item }">
            <router-link :to="`${getSlugId(item)}`">
              <v-hover v-slot="{ hover }">
                <v-list-item :class="hover ? ' bg-primary-color-0' : ''" style="padding: 0px !important">
                  <v-avatar tile size="32">
                    <img :src="item.listImage[0]" :alt="`small-image-${item.name}`" />
                  </v-avatar>
                  <v-list-item-title
                    class="px-3 font-size-12 d-flex-col align-center justify-start"
                    style="max-width: 600px"
                  >
                    <div
                      class="line-height-14"
                      style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 600px"
                    >
                      {{ item.cleanName }}
                    </div>
                    <div class="d-flex align-center justify-start line-height-18">
                      <span
                        class="mr-3 line-height-22 font-size-12 font-weight-1 old-price"
                        v-if="item.listPrice != item.price"
                      >
                        {{ item.listPrice | formatPrice }}đ
                      </span>
                      <span class="mr-3 font-weight-bold font-size-12">{{ item.price | formatPrice }} </span>
                      <span
                        class="discount-rate px-1 font-size-12 font-weight-2 text-right"
                        v-if="item.listPrice != item.price"
                      >
                        {{ item.discountRate }}%
                      </span>
                    </div>
                  </v-list-item-title>
                </v-list-item>
              </v-hover>
            </router-link>
          </template>
        </v-autocomplete>
        <div class="some-category-hot font-size-12 py-1" style="height: 35px">
          <div class="d-inline" v-for="i in listCategoryName.slice(0, 4)" :key="`${i.SK}-some-category-hot`">
            <v-hover v-slot="{ hover }">
              <router-link
                :to="`/category/${i.SK}`"
                class="pr-4 primary-color-1"
                :class="hover ? 'font-weight-bold' : 'font-weight-normal'"
              >
                {{ categoryName(i.name) }}
              </router-link>
            </v-hover>
          </div>
        </div>
      </div>
      <v-spacer v-if="!isMobile"></v-spacer>

      <!-- <v-menu v-if="!isMobile" :close-on-click="true" bottom right nudge-bottom="40" z-index="2000">
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
      </v-menu> -->
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
import ProductService, { ProductItem, ProductSearchItem } from '@/api/product.service';
import CategoryService from '@/api/category.service';

export default Vue.extend({
  name: 'Header',
  props: ['isShowMenu'],
  // components: { AccountMenu },
  data: () => ({
    selectedCategory: [],
    isLoading: false,
    valueText: null,
    isFocus: false,
    searchCode: '',
    cacheSearchCode: '',
    beforeCategory: '',
    localeLanguage: {} as any,
    debouncedQuery: Function,
    productSearchItems: [] as ProductItem[],
    placeholder: '',
    searchStringList: [] as string[],
  }),
  computed: {
    widthMenu(): number {
      const width = this.isMobile ? innerWidth : 680;
      return Math.min(width, 680);
    },
    productSearchItemsComputed() {
      return this.productSearchItems && this.productSearchItems.length == 0
        ? { PK: 'default' }
        : this.productSearchItems;
    },
    innerWidth(): number {
      return this.$store.getters.innerWidth;
    },
    localeLanguageItems() {
      return [
        {
          code: 'vn',
          name: this.$t('vn'),
          flag: require('@/assets/image/flag/vietnam.png'),
        },
        {
          code: 'en',
          name: this.$t('en'),
          flag: require('@/assets/image/flag/united-kingdom.png'),
        },
      ];
    },
    listCategoryName(): string[] {
      return this.isMobile ? this.$store.getters.categoryItems.slice(0, 7) : this.$store.getters.categoryItems;
    },
    categoryId(): string {
      return this.$route.params['idCate'] || '';
    },
    isMobile(): boolean {
      return this.$store.getters.isMobile;
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
  filters: {
    formatPrice(value: string) {
      return value ? value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') : '';
    },
  },
  methods: {
    filterItems(item: ProductItem, queryText: string, itemText: any): boolean {
      // if (item.SK.includes(queryText.split(' ').join('_'))) return true;
      // if (item.SK.includes(queryText)) return true;
      const a = item.SK.toLowerCase().trim().split(' ');
      const b = queryText.toLowerCase().trim().split(' ');
      const lastWordInQuery = b[b.length - 1];
      console.log('item', this.productSearchItems.length);
      if (a.length == 0 && b.length == 0) return false;
      const intersection = this._.intersection(a, b);
      console.log('intersection', intersection);
      const isIntersection = intersection && intersection.length != 0 && intersection.length == b.length ? true : false;
      if (isIntersection) return true;
      else return item.SK.toLowerCase().includes(lastWordInQuery);
    },
    handleShowMenu() {
      this.$emit('handle-show-menu');
    },
    handleChangeLanguage(item: any) {
      this.localeLanguage = item;
      if (this.localeLanguage != i18n.locale) i18n.locale = (this as any).localeLanguage.code as string;
      console.log('i18n.locale', i18n.locale);
    },
    async searchProduct(event: any) {
      if (this.valueText) {
        const item = null as any;
        if (item) {
          const ele = item.split('#');
          const categoryId = ele[0];
          const code = ele[1];
          this.cacheSearchCode = code;
          this.$router.replace(`/category/${categoryId}/product/${code}`);
        }
      }
      console.log('event.code', event.code);
      if (
        !this.isLoading &&
        // (event.code == 'Enter' || event.code == 'Space' || (this.searchCode && this.searchCode.length == 1)) &&
        this.searchCode
      ) {
        this.isLoading = true;
        this.debouncedQuery();
        this.updateUrlQuery(this.searchCode);
      }
      await sleep(1000, 1000);
      this.isLoading = false;
    },
    async searchItem() {
      this.valueText = null;
      if (this.searchCode && !this.searchStringList.includes(this.searchCode)) {
        this.searchStringList.push(this.searchCode);
        let listSearchItem = await ProductService.querySearchItems({ searchString: this.searchCode });
        listSearchItem = listSearchItem.map((i) => ({
          ...i,
        }));
        this.productSearchItems = this.productSearchItems.concat(listSearchItem);
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
    categoryName(categoryId: string): string {
      return categoryId ? this.$t(`category.${categoryId}`).toString() : '';
    },

    getSlugId(item: ProductItem): string {
      return ProductService.getSlugId(item);
    },
  },
  created() {
    console.log('Header component created');
    this.localeLanguage = this.localeLanguageItems[0] as any;
    this.placeholder = 'Siêu sale thỏa thích ...' || this.$t('search').toString();
    this.productSearchItems = this.$store.getters.productSearchItems || [];
    this.searchStringList = this.$store.getters.searchStringList || [];
    this.debouncedQuery = (this as any)._.debounce(() => {
      this.searchItem();
    }, 300);
  },
  beforeDestroy() {
    this.$store.commit('setState', {
      searchStringList: this.searchStringList,
      productSearchItems: this.productSearchItems,
    });
  },
});
</script>

<style lang="scss">
@import '@/resources/scss/Common.scss';
.header {
  box-shadow: 1px 6px 12px -10px rgba(0, 0, 0, 0.75) !important;
  -webkit-box-shadow: 1px 6px 12px -10px rgba(0, 0, 0, 0.75) !important;
  -moz-box-shadow: 1px 6px 12px -10px rgba(0, 0, 0, 0.75) !important;
  .nav-left {
    width: 100px;
  }
  @include for_breakpoint(mobile tablet) {
    .v-toolbar__content {
      padding: 4px;
    }
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
  .v-text-field.v-text-field--solo .v-input__control {
    min-height: 40px !important;
    height: 40px !important;
    font-size: 13px;
  }
}

.v-autocomplete__content {
  border-radius: 0px 0px 2px 2px !important;
  box-shadow: 1px 6px 12px -10px rgba(0, 0, 0, 0.75) !important;
  -webkit-box-shadow: 1px 6px 12px -10px rgba(0, 0, 0, 0.75) !important;
  -moz-box-shadow: 1px 6px 12px -10px rgba(0, 0, 0, 0.75) !important;
  .discount-rate {
    color: #ca3e29;
    z-index: 2;
  }

  .old-price {
    text-decoration: line-through !important;
    text-decoration-color: #607d8b !important;
    text-decoration-style: solid 1px !important;
  }
}
</style>

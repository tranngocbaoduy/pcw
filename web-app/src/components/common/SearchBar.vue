<template>
  <v-card
    height="100vh"
    width="100vw"
    class="elevation-0 bg-primary-color-0 d-flex flex-column justify-start align-center"
  >
    <div v-if="!isSelectedQR" style="width: 100%; height: 15%"></div>
    <router-link class="custom-link pa-2" :to="`/home`">
      <v-img :height="130" :width="270" contain :src="require('@/assets/image/logo/Light.png')" alt=""> </v-img>
    </router-link>
    <div class="d-flex align-center justify-center font-size-16 bg-primary-color-0">
      <div @click="isSelectedQR = false" class="hover-custom-link">Text</div>
      <span class="px-2">/</span>
      <div @click="isSelectedQR = true" class="hover-custom-link">QR Code</div>
    </div>
    <div style="width: 95%" class="pb-0 pt-4 bg-primary-color-0">
      <SearchQRBar
        v-if="isSelectedQR"
        @change-method-search-to-text="isSelectedQR = false"
        @change-method-search-to-qr-code="isSelectedQR = true"
      />
      <v-autocomplete
        v-else
        class="rounded-md elevation-1"
        @blur.prevent.stop="isFocus = false"
        @click.prevent.stop="isFocus = true"
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
        item-text="cleanName"
        v-model="valueText"
        :no-data-text="$t('Let search somthing!')"
        :filter="filterItems"
        :menu-props="{
          closeOnClick: false,
          closeOnContentClick: false,
          disableKeys: true,
          openOnClick: false,
          maxHeight: '40%',
          minWidth: widthMenu,
          maxWidth: widthMenu,
          nudgeBottom: isMobile ? 36 : 2,
          offsetY: true,
          elevation: 0,
          offsetOverflow: true,
          transition: false,
          overflowY: true,
        }"
        :disable-lookup="true"
        @keyup="searchProduct"
        :search-input.sync="searchCode"
        @input="searchCode = null"
      >
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
                        :to="`/category/${category.id}`"
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
                        :to="`/category/${category.id}`"
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
                      :to="`/category/${category.id}`"
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
        <template v-slot:item="{ item }" @click.prevent.stop>
          <v-hover v-slot="{ hover }">
            <v-list-item
              @click="goToItem(item)"
              :class="hover ? ' bg-primary-color-0' : ''"
              style="padding: 0px !important"
            >
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
        </template>
      </v-autocomplete>
      <div class="some-category-hot font-size-12 pb-1 my-1" style="height: 35px">
        <div class="d-inline" v-for="i in listCategoryName.slice(0, 4)" :key="`${i.id}-some-category-hot`">
          <v-hover v-slot="{ hover }">
            <router-link
              :to="`/category/${i.id}`"
              class="pr-4 primary-color-1"
              :class="hover ? 'font-weight-bold' : 'font-weight-normal'"
            >
              {{ categoryName(i.name) }}
            </router-link>
          </v-hover>
        </div>
      </div>
    </div>
  </v-card>
</template>

<script lang="ts">
async function sleep(min: number, max: number) {
  return new Promise((res) => setTimeout(res, Math.floor(Math.random() * (max - min + 1)) + min));
}
import Vue from 'vue';
import i18n from '@/i18n';
import ProductService, { ProductItem } from '@/api/product.service';
import AuthService from '@/api/auth.service';
import SearchQRBar from '@/components/common/SearchQRBar.vue';
export default Vue.extend({
  name: 'Header',
  props: ['isShowMenu'],
  components: { SearchQRBar },
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
    isSelectedQR: false,
  }),
  computed: {
    widthMenu(): number {
      const width = this.isMobile ? innerWidth : 400;
      return Math.min(width, 400);
    },
    productSearchItemsComputed() {
      return this.productSearchItems && this.productSearchItems.length == 0
        ? { PK: 'default' }
        : this.productSearchItems;
    },
    innerWidth(): number {
      return this.$store.getters.innerWidth;
    },
    innerHeight(): number {
      return this.$store.getters.innerHeight;
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
  },
  watch: {},
  filters: {
    formatPrice(value: string) {
      return value ? value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') : '';
    },
  },
  methods: {
    filterItems(item: ProductItem, queryText: string): boolean {
      // if (item.id.includes(queryText.split(' ').join('_'))) return true;
      // if (item.id.includes(queryText)) return true;
      const a = item.id.toLowerCase().trim().split(' ');
      const b = queryText.toLowerCase().trim().split(' ');
      const lastWordInQuery = b[b.length - 1];
      if (a.length == 0 && b.length == 0) return false;
      const intersection = this._.intersection(a, b);
      const isIntersection = intersection && intersection.length != 0 && intersection.length == b.length ? true : false;
      if (isIntersection) return true;
      else return item.id.toLowerCase().includes(lastWordInQuery);
    },
    handleShowMenu() {
      this.$emit('handle-show-menu');
    },
    handleChangeLanguage(item: any) {
      this.localeLanguage = item;
      if (this.localeLanguage != i18n.locale) i18n.locale = (this as any).localeLanguage.code as string;
    },
    async searchProduct() {
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
      if (this.searchCode.includes('http') && AuthService.isValidHttpUrl(this.searchCode)) {
        //    const searchURL =
        //   'https://shopee.vn/Dien-Thoai-OPPO-RENO7-4G-(8GB/128GB)---Hang-Chinh-Hang-i.25452983.16050088485?af_click_lookback=7d&af_reengagement_window=7d&af_siteid=an_17104620000&af_sub_siteid=1221547&af_viewthrough_lookback=1d&atnct1=5737c6ec2e0716f3d8a7a5c4e0de0d9a&atnct2=FUSYLJrC1liQE0y1dYWjRG2rp0zh7d4qSCEIKPOuNSaFeW0c&atnct3=BKec200063d00q6jv&c=322&is_retargeting=true&pid=affiliates&utm_campaign=&utm_content=1221547-FUSYLJrC1liQE0y1dYWjRG2rp0zh7d4qSCEIKPOuNSaFeW0c-x-pcw.store--&utm_medium=affiliates&utm_source=an_17104620000';
        let listSearchItem = await ProductService.querySearchItemsByUrl({ searchUrl: this.searchCode });
        if (listSearchItem.length != 0) {
          listSearchItem = listSearchItem.map((i) => ({
            ...i,
          }));
          this.productSearchItems = this.productSearchItems.concat(listSearchItem);
          this.searchCode = listSearchItem[0].name;
        }
      } else {
        if (this.searchCode && !this.searchStringList.includes(this.searchCode)) {
          this.searchStringList.push(this.searchCode);
          let listSearchItem = await ProductService.querySearchItems({ searchString: this.searchCode });
          listSearchItem = listSearchItem.map((i) => ({
            ...i,
          }));
          this.productSearchItems = this.productSearchItems.concat(listSearchItem);
        }
      }

      this.isLoading = false;
    },
    updateUrlQuery(query: string) {
      if (!AuthService.isValidHttpUrl(query)) {
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set('query', query);
        const queryUrl = urlParams.toString();
        history.replaceState({}, '', `${this.$route.path}?${queryUrl}`);
      }
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
    goToItem(item: ProductItem) {
      this.$router.push(this.getSlugId(item));
    },
    getSlugId(item: ProductItem): string {
      return ProductService.getSlugId(item);
    },
  },
  created() {
    console.log('Header component created', this.innerHeight);
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
    border: 1px solid #ca3e29;
    border-radius: 1px !important;
    line-height: 14px !important;
  }
  .old-price {
    text-decoration: line-through !important;
    text-decoration-color: #607d8b !important;
    text-decoration-style: solid 1px !important;
  }
}
</style>

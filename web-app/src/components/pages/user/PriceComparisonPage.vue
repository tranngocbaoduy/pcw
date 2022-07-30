<template>
  <div class="price-comparison-page">
    <BreadCrumbs class="mt-4" :breadcrumbs="breadcrumbs" />
    <template>
      <v-card-title class="font-size-22 font-weight-3 mt-2 mb-4 px-0">
        <div>So sánh giá</div>
        <v-spacer></v-spacer>
      </v-card-title>
    </template>
    <v-card class="border-custom-4 pa-9">
      <v-card-title class="font-size-22 font-weight-3 pa-0 mb-4">Sản phẩm cần so sánh</v-card-title>
      <v-row>
        <v-col cols="10">
          <v-autocomplete
            class="border-radius-8 elevation-0"
            single-line
            full-width
            hide-details
            flat
            :items="allProductName"
            background-color="#eceff1"
            placeholder="Hãy chọn 1 sản phẩm bất kỳ"
            color="#ECEFF1"
            item-text="name"
            item-value="code"
            solo
            return-object
            clearable
            v-model="selectedItem"
            :search-input.sync="searchQuery"
            @change="selectProduct($event)"
          >
            <template v-slot:append>
              <v-fade-transition hide-on-leave>
                <v-progress-circular v-if="isLoading" size="24" color="info" indeterminate></v-progress-circular>
                <!-- <v-btn
                  @click="selectProduct($event)"
                  color="#1859db"
                  v-else
                  width="48"
                  height="48"
                  style="color: white"
                  class="border-radius-8 mr-n2"
                >
                  <v-icon size="24">mdi-magnify</v-icon>
                </v-btn> -->
              </v-fade-transition>
            </template>
          </v-autocomplete></v-col
        >
        <v-col cols="2" class="pa-auto">
          <v-btn
            color="info"
            height="48"
            @click="refreshSearch"
            style="color: white"
            class="ma-auto my-1 border-radius-8 mr-n2"
          >
            Refresh
          </v-btn>
        </v-col>
      </v-row>

      <template>
        <v-chip-group column class="my-5" v-if="selectedItems && selectedItems.length != 0">
          <v-chip
            v-for="item in selectedItems"
            :key="item.name"
            class="font-size-16 font-weight-2 pa-4 rounded-0"
            color="orange"
            label
          >
            <strong>{{ item.name }}</strong>
          </v-chip>
        </v-chip-group>
      </template>

      <!-- <template>
        <v-card class="rounded-0 my-6 pa-5">
          <v-card-title class="font-size-16 font-weight-2 pa-0 mb-4">Gợi ý sản phẩm so sánh</v-card-title>
          <v-row>
            <v-col v-for="item in recommendations" :key="item.name">
              <v-card class="border-custom-4 mx-auto">
                <v-card-title class="font-size-16 font-weight-1 py-2">{{ item.name | reduceText(20) }}</v-card-title>
              </v-card>
            </v-col>
          </v-row>
        </v-card>
      </template> -->

      <v-card-title class="font-size-22 font-weight-3 pa-0" v-if="agencies && agencies.length != 0">
        Chọn đại lý
        <span class="font-size-16 font-weight-2 ml-1" v-if="!isSelectedAgencies"> (Chọn 1 đại lý để so sánh)</span>
      </v-card-title>

      <template>
        <v-chip-group column multiple class="mt-4 mb-8">
          <v-chip
            v-for="item in agencies"
            :key="item.name"
            class="font-size-16 font-weight-2 pa-4 rounded-0"
            v-model="item.selected"
            filter
            color="green"
            outlined
          >
            <strong>{{ item.name }}</strong>
          </v-chip>
        </v-chip-group>
      </template>

      <v-card-actions class="pa-0">
        <v-btn
          @click="handleComparasion"
          class="rounded-lg"
          height="50px"
          color="primary"
          :disabled="selectedItems.length == 0"
          >So sánh nhanh</v-btn
        >
      </v-card-actions>
    </v-card>

    <v-card-title class="font-size-22 font-weight-3 my-5 px-0">Kết quả</v-card-title>

    <template>
      <v-row no-gutters class="d-flex mb-6 px-0" v-if="comparisonItems.length != 0">
        <v-col
          lg="6"
          md="6"
          sm="12"
          xl="6"
          v-for="subComparisonItems in comparisonItems"
          :key="subComparisonItems.name"
        >
          <PriceComparisonCard :comparisonItems="subComparisonItems" />
        </v-col>
      </v-row>
      <v-row no-gutters class="d-flex mb-6 px-0" v-else>
        <v-img :src="noItemImage" max-height="800" max-width="100%" height="400" width="200" />
      </v-row>
    </template>
    <v-snackbar color="danger" v-model="isShowSnackbar" :timeout="2000">
      {{ textError }}
    </v-snackbar>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BreadCrumbs from '@/components/common/BreadCrumbs.vue';
import PriceComparisonCard from '@/components/product/PriceComparisonCard.vue';
import ProductService from '@/api/product.service';

export default Vue.extend({
  name: 'Body',
  props: ['isShowMenu'],
  components: { PriceComparisonCard, BreadCrumbs },
  data: () => ({
    searchQuery: '',
    isLoading: false,
    isShowSnackbar: false,
    textError: 'Không tìm thấy sản phẩm, vui lòng chọn sản phẩm khác.',

    recommendations: [
      { name: 'Product 1', selected: true },
      { name: 'Product 2', selected: true },
      { name: 'Product 3', selected: true },
      { name: 'Product 4', selected: true },
      { name: 'Product 5', selected: true },
    ],
    noItemImage: require('@/assets/banner/no-product.png'),

    mappingCategoryId: {
      tivi: 'tivi',
      'dien-thoai': 'DienThoai',
      'tu-lanh': 'TuLanh',
      'may-giat': 'MayGiat',
    },
    selectedItem: {} as any,
    selectedItems: [] as any[],
    agencies: [] as any[],
    comparisonItems: [] as any[],
    selectedFirstCategory: '',
    selectedProductNames: [] as string[],
    selectedProductId: [] as string[],
  }),
  filters: {
    reduceText: function (text: string, max: number) {
      return text.length > max ? text.slice(0, max - 2) + '...' : text;
    },
    formatPrice(value: string) {
      // const val = (value / 1).toFixed(0).replace('.', ',');
      return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },
  },
  created() {
    console.log('Price Comparasion Page component created');
    this.initialize();
  },
  computed: {
    breadcrumbs(): any[] {
      return [
        {
          text: 'Home',
          disabled: false,
          to: '/',
          exact: true,
        },
        {
          text: `So sánh nhanh`,
          to: ``,
          disabled: true,
          exact: true,
        },
      ];
    },
    isSelectedAgencies(): boolean {
      return this.agencies.filter((item: any) => item.selected).length != 0;
    },
    listCategoryName(): string[] {
      return [
        ...this.$store.getters.categoryItems,
        {
          PK: 'CATEGORY',
          SK: 'TatCa',
          NameVN: 'Tất cả',
        },
      ];
    },

    categoryId(): string {
      return this.$route.params['idCate'] || '';
    },
    allProductName(): any[] {
      let items = this.$store.getters.allProductName as string[];
      if (this.selectedFirstCategory && this.selectedFirstCategory != '') {
        items = items.filter((item: string) => item.includes(this.selectedFirstCategory));
      }
      if (this.selectedProductNames.length != 0) {
        items = items.filter((name: string) => !this.selectedProductNames.includes(name));
      }
      return items.map((item: string) => {
        const ele = item.split('#');
        return {
          category: ele[0],
          code: ele[1],
          name: ele[2],
          wholeSent: item,
          selected: false,
        };
      });
    },
  },
  methods: {
    refreshSearch() {
      this.selectedItem = {};
      this.selectedItems = [];
      this.agencies = [];
      this.comparisonItems = [];
      this.selectedFirstCategory = '';
      this.selectedProductNames = [];
      this.selectedProductId = [];
    },
    // async selectProduct(event: any) {
    //   this.isLoading = true;
    //   try {
    //     this.selectedItem.selected = true;
    //     const categoryId = (this as any).mappingCategoryId[this.selectedItem.category] || '';
    //     this.selectedFirstCategory = this.selectedItem.category;

    //     const productId = this.selectedItem.code;
    //     if (!this.selectedProductId.includes(productId)) {
    //       this.selectedProductId.push(productId);
    //       const productItem = {}; //await ProductService.queryItemByCode(categoryId, productId);
    //       for (const store of productItem.stores) {
    //         this.selectedProductNames.push(store.name);
    //         if (this.agencies.filter((item: any) => item.id == store.domainObj.id).length == 0) {
    //           this.agencies.push({
    //             ...JSON.parse(JSON.stringify(store.domainObj)),
    //             selected: false,
    //           });
    //         }
    //       }
    //       this.selectedItems.push({
    //         ...JSON.parse(JSON.stringify(this.selectedItem)),
    //         ...JSON.parse(JSON.stringify(productItem)),
    //       });
    //     } else {
    //       this.textError = 'Bạn đã chọn sản phẩm này rồi.';
    //       this.isShowSnackbar = true;
    //     }
    //   } catch (err) {
    //     console.log('err', err);
    //     this.textError = 'Không tìm thấy sản phẩm, vui lòng chọn sản phẩm khác.';
    //     this.isShowSnackbar = true;
    //     this.refreshSearch();
    //   }

    //   this.isLoading = false;
    // },
    handleComparasion() {
      this.comparisonItems = [] as any[];
      if (this.agencies.filter((item: any) => item.selected).length == 0) {
        this.textError = 'Chọn 1 đại lý để so sánh';
        this.isShowSnackbar = true;
      }
      for (const selectedItem of this.selectedItems) {
        const itemComparasion = {} as any;
        itemComparasion.stores = [];
        let name = '';
        let imageUrl = '';

        for (const store of selectedItem.stores) {
          const agency = this.agencies.find((item: any) => item.id == store.PK && item.selected);
          if (agency) {
            if (name == '') name = store.name || '';
            if (imageUrl == '') imageUrl = store.thumbnailUrl || '';
            const storeFound = itemComparasion.stores.find((item: any) => item.id == agency.id);
            if (storeFound) {
              storeFound.prices.push(store.price);
              storeFound.urlKeys.push(store.urlKey);
            } else {
              itemComparasion.stores.push({
                id: agency.id,
                name: agency.name,
                price: store.price,
                logoUrl: agency.logoUrl,
                prices: [store.price],
                urlKeys: [store.urlKey],
              });
            }
          }
        }
        itemComparasion.name = name;
        itemComparasion.img = imageUrl;
        if (itemComparasion.stores.length != 0) this.comparisonItems.push(itemComparasion);
      }
    },
    handleShowMenu() {
      this.$emit('handle-show-menu');
    },
    searchProduct() {
      this.isLoading = true;
      setTimeout(() => (this.isLoading = false), 2000);
    },
    handleCloseChipItem(removeItem: any) {
      if (this.selectedItems.length == 1) {
        this.selectedFirstCategory = '';
        this.agencies = [];
        this.selectedProductNames = [];
        this.selectedItems = [];
      } else {
        removeItem = this.selectedItems.find((item: any) => item.code == removeItem.code);

        this.selectedItems = this.selectedItems.splice(this.selectedItems.indexOf(removeItem), 1);
      }
      this.handleComparasion();
    },
    initialize() {},
  },
});
</script>

<style lang="scss"></style>

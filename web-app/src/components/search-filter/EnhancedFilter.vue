<template>
  <v-card class="enhanced-filter rounded-0 mx-0 elevation-0" :class="isSticky ? 'sticky' : 'n-sticky'">
    <!-- <template slot="progress">
      <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
    </template> -->

    <v-container
      :fluid="false"
      class="d-flex justify-start align-center pt-2 pb-0"
      style="height: 55px; flex-wrap: wrap"
      :class="isSticky ? '' : 'px-2'"
    >
      <!-- <div style="width: 100%" class="mb-4" :class="isSticky ? 'ml-4' : ''">
        <v-autocomplete
          class="rounded-sm elevation-0 mr-4"
          style="border: #6e6e6e 0.5px solid; box-shadow: none !important"
          validate-on-blur
          :items="productSearchItems"
          hide-details
          background-color="white"
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
        </v-autocomplete>
      </div> -->
      <div class="mr-4" :class="isSticky ? 'ml-4' : ''">
        <v-select
          v-model="selectedAgencies"
          hide-details
          class="font-size-14"
          style="width: 100px"
          :style="
            selectedAgencies && selectedAgencies.length == 0
              ? 'border: #6e6e6e 0.5px solid; box-shadow: none !important'
              : 'border: #1859db 1px solid'
          "
          :items="agencyItems"
          label=""
          solo
          flat
          :placeholder="$t('agency')"
          multiple
          item-text="name"
          return-object
          @change="handleChangeSelectedAgency"
        >
          <template v-slot:selection="{ index }">
            <span v-if="index === 0" style="color: #1859db" class="text-caption"> {{ $t('agency') }} </span>
          </template>
        </v-select>
      </div>
      <div class="mr-4">
        <v-select
          v-model="selectedPrices"
          hide-details
          style="width: 150px"
          :style="
            selectedPrices && selectedPrices.length == 0
              ? 'border: #6e6e6e 0.5px solid; box-shadow: none !important'
              : 'border: #1859db 1px solid'
          "
          :items="priceItems"
          label=""
          solo
          flat
          :placeholder="$t('range')"
          multiple
          item-text="name"
          return-object
          @change="handleChoosePrice"
        >
          <template v-slot:selection="{ index }">
            <span v-if="index === 0" style="color: #1859db" class="text-caption"> {{ $t('range') }} </span>
          </template>
        </v-select>
      </div>
      <v-btn
        class="rounded-md"
        color="#1859db"
        :style="isDisabledRefreshButton ? 'border: 0.5px #6e6e6e solid' : 'border: 1px #1859db solid'"
        :height="isDisabledRefreshButton ? 32 : 34"
        width="50"
        max-width="50"
        outlined
        :disabled="isDisabledRefreshButton"
        @click="refreshFilter"
      >
        <v-icon size="16"> mdi-refresh </v-icon>
      </v-btn>
      <!--  
      <v-card class="pa-0 mt-4 mb-4" color="#f3f6f8" flat>
        <v-card-title class="header-customer pa-0 mb-3 font-size-18"> {{ $t('range') }} </v-card-title>
        <div class="mt-5">
          <v-card-text
            v-for="item in priceItems"
            :key="item.name"
            class="item-customer pa-0 mt-2 ml-0 font-weight-2 hover-custom-link"
            @click="handleChoosePrice(item)"
            :class="item.selected ? 'font-weight-3 primary-color-1' : ''"
            >{{ $t(item.name) }}</v-card-text
          >
        </div>
        <v-card-text align="center" class="mb-0 mt-1 px-3 pb-1">
          <v-row class="my-n0 pa-0 d-inline-flex">
            <v-text-field
              class="rounded-lg mx-0"
              v-model="minPriceFilter"
              :value="minPriceFilter | formatVnd"
              flat
              dense
              label="MIN"
              type="number"
              single-line
              outlined
              hide-details
              solo
            ></v-text-field>
            <v-text-field
              class="rounded-lg mt-2 mx-0"
              v-model="maxPriceFilter"
              :value="maxPriceFilter | formatVnd"
              flat
              dense
              label="MAX"
              type="number"
              single-line
              outlined
              hide-details
              solo
            ></v-text-field>
          </v-row>
        </v-card-text>
        <v-card-actions class="px-0">
          <v-btn class="white--text mt-3 rounded-lg" color="#1859db" width="100%" @click="handleChoosePriceCustom"
            >OK</v-btn
          >
        </v-card-actions></v-card
      > -->
    </v-container>
  </v-card>
</template>

<script lang="ts">
import { ProductSearchItem } from '@/api/product.service';
import Vue from 'vue';

export default Vue.extend({
  props: ['agencyItems', 'priceItems'],
  data: () => ({
    selectedAgencies: [] as any[],
    selectedPrices: [] as any[],

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
    isSticky(): boolean {
      return this.offsetHeight > 260;
    },
    offsetHeight(): number {
      return this.$store.getters.offsetHeight;
    },
    catalogItems(): [] {
      return Object.keys(this.$store.getters.searchFilter).includes('catalogItems')
        ? this.$store.getters.searchFilter.catalogItems
        : [];
    },
    voteItems(): [] {
      return Object.keys(this.$store.getters.searchFilter).includes('voteItems')
        ? this.$store.getters.searchFilter.voteItems
        : [];
    },
    shipItems(): [] {
      return Object.keys(this.$store.getters.searchFilter).includes('shipItems')
        ? this.$store.getters.searchFilter.shipItems
        : [];
    },
    isDisabledRefreshButton(): boolean {
      return !(this.selectedPrices.length != 0 || this.selectedAgencies.length != 0);
    },
  },
  created() {},
  watch: {
    priceItems() {
      console.log('this.priceItems', this.priceItems, this.selectedPrices);
      if (this.priceItems && this.priceItems.length != 0) {
        // this.selectedPrices = this.priceItems.filter((i: any) => i.selected);
      } else {
        this.selectedPrices = [] as any[];
      }
    },
    agencyItems() {
      this.selectedAgencies = this.agencyItems.filter((i: any) => i.selected);
    },
  },
  methods: {
    refreshFilter() {
      this.selectedPrices = [] as any[];
      this.$emit('refresh-filter');
    },
    handleChoosePrice() {
      let minMaxTuple = [0, 1000];
      console.log('handleChoosePrice', this.selectedPrices);
      if (this.selectedPrices && this.selectedPrices.length != 0) {
        const minItems = this.selectedPrices.map((item: any) => item.min);
        const maxItems = this.selectedPrices.map((item: any) => item.max);
        if (Math.min(...minItems) == Infinity || Math.max(...maxItems) == Infinity) {
          minMaxTuple = [0, 1000];
        } else {
          minMaxTuple = [Math.min(...minItems), Math.max(...maxItems)];
          if ((!minMaxTuple[0] && minMaxTuple[0] != 0) || !minMaxTuple[1]) {
            minMaxTuple = [0, 1000];
          }
        }
        this.$emit('change-price', { min: minMaxTuple[0], max: minMaxTuple[1] });
      } else {
        this.$emit('change-price', { min: '', max: '' });
      }
    },
    updateUrlQuery(field: string, query: string) {
      const urlParams = new URLSearchParams(window.location.search);
      urlParams.set(field, query);
      const queryUrl = urlParams.toString();
      history.replaceState({}, '', `${this.$route.path}?${queryUrl}`);
    },
    handleChangeSelectedAgency() {
      this.$emit('change-agency', this.selectedAgencies);
      // if (this.selectedAgencies && this.selectedAgencies.length != 0) {
      //   this.updateUrlQuery('agencyItems', this.selectedAgencies.map((i: any) => i.name).join(','));
      //   this.$emit('refresh-filter');
      // } else {
      //   const query = { ...this.$route.query };
      //   delete query['agencyItems'];
      //   this.$router.replace({ path: this.$route.path, query: query || {} });
      //   this.$emit('refresh-filter');
      // }
    },
  },
  filters: {
    formatVnd(text: string) {
      return text + ',000,000 vnđ';
    },
  },
});
</script>

<style lang="scss">
.enhanced-filter.n-sticky {
  background: transparent;
}
.enhanced-filter.sticky {
  background: white;
  position: fixed;
  left: 0;
  top: 0;
  min-width: 100vw !important;
  z-index: 1000;
  box-shadow: 1px 6px 12px -10px rgba(0, 0, 0, 0.75) !important;
  -webkit-box-shadow: 1px 6px 12px -10px rgba(0, 0, 0, 0.75) !important;
  -moz-box-shadow: 1px 6px 12px -10px rgba(0, 0, 0, 0.75) !important;
}
.enhanced-filter {
  -webkit-transition: all 0.2s;
  -moz-transition: all 0.2s;
  -ms-transition: all 0.2s;
  -o-transition: all 0.2s;
  transition: all 0.2s;
  // background: transparent;
  // position: absolute;
  // left: 0;
  // top: 110;
  // width: 100vw;

  .v-text-field.v-text-field--solo .v-input__control {
    min-height: 32px !important;
    height: 32px !important;
    font-size: 13px;
  }
}
</style>

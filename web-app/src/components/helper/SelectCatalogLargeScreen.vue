<template>
  <div class="catalog-screen mt-3">
    <v-card class="pa-0 mt-0 mb-4" color="#f3f6f8" max-height="340px" flat>
      <v-card-title class="header-customer pa-0 mb-7 font-size-18"> {{ $t(`catalog`) }} </v-card-title>
      <div>
        <div v-for="item in catalogItems" :key="item.name">
          <v-hover v-slot="{ hover }">
            <router-link class="custom-link" :to="`/category/${item.urlRoute}`">
              <v-card-text
                class="item-customer font-size-14 font-weight-2 pa-0 my-2"
                :class="item.selected || hover ? 'primary-color-1' : 'black--text'"
                :elevation="hover ? 12 : 2"
                >{{ $t(`category.${item.name}`) }}</v-card-text
              >
            </router-link>
          </v-hover>
        </div>
      </div>
    </v-card>

    <!-- <v-card class="pa-0 mb-9" color="#f3f6f8" max-height="184px" flat>
      <v-card-title class="header-customer pa-0 mb-2"> Bình chọn </v-card-title>
      <div>
        <div v-for="item in voteItems" :key="item.name">
          <v-rating
            :value="item.rate"
            color="black"
            background-color="black"
            half-increments
            dense
            readonly
            size="24"
          ></v-rating>
        </div>
      </div>
    </v-card> -->

    <div class="pa-0 mb-4" flat>
      <v-card-title class="header-customer pa-0 ma-0 font-size-18">{{ $t('agency') }}</v-card-title>
      <div class="pl-3 mt-3">
        <div class="item-customer d-flex pa-0 mt-2" justify="center" v-for="item in agencyItems" :key="item.name">
          <v-checkbox
            @change="handleChangeSelectedAgency"
            class="item-checkbox-customer pa-0 my-0 font-weight-2"
            v-model="item.selected"
            style="font-color: #222b45 !important"
            :label="item.name"
            color="#1859db"
            light
            hide-details
          ></v-checkbox>
        </div>
      </div>
    </div>

    <v-card class="pa-0 mb-4" color="#f3f6f8" flat>
      <v-card-title class="header-customer pa-0 font-size-18">{{ $t('brand') }}</v-card-title>
      <div class="pl-3 mt-3 mb-7">
        <div class="item-customer d-flex pa-0 mt-2" justify="center" v-for="item in brandItems" :key="item.name">
          <v-checkbox
            @change="handleChangeSelectedBrand"
            class="item-checkbox-customer pa-0 my-0 font-weight-2"
            style="font-color: #222b45 !important"
            v-model="item.selected"
            :label="item.name"
            color="#1859db"
            light
            hide-details
          ></v-checkbox>
        </div>
      </div>
    </v-card>

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
      </v-card-actions>
    </v-card>

    <!--    

    <div class="pa-0 mb-8" max-height="197px" flat>
      <v-card-title class="header-customer pa-0 ma-0"> Giao hàng</v-card-title>
      <div class="mt-2 mb-4">
        <div class="item-customer d-flex pa-0 mt-2" justify="center" v-for="item in shipItems" :key="item.name">
          <v-checkbox
            class="item-checkbox-customer pa-0 ma-0"
            v-model="item.selected"
            :label="item.name"
            color="black"
            hide-details
          ></v-checkbox>
        </div>
      </div>
    </div> -->
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  props: ['catalogItems', 'voteItems', 'brandItems', 'priceItems', 'agencyItems', 'shipItems'],
  data: () => ({
    minPriceFilter: '',
    maxPriceFilter: '',
  }),
  created() {
    const query = { ...this.$route.query };
    if (query.minPrice && query.maxPrice) {
      this.minPriceFilter = query.minPrice as string;
      this.maxPriceFilter = query.maxPrice as string;
      this.$emit(
        'handle-choose-price-custom',
        parseInt(this.minPriceFilter || '0'),
        parseInt(this.maxPriceFilter || '999')
      );
    }
  },
  watch: {
    priceItems() {
      const filterItems = this.priceItems.filter((item: any) => item.selected);
      const minItems = filterItems.map((item: any) => item.min);
      const maxItems = filterItems.map((item: any) => item.max);
      this.minPriceFilter = Math.min(...minItems).toString();
      this.maxPriceFilter = Math.max(...maxItems).toString();
    },
  },
  methods: {
    handleChoosePrice(item: any) {
      this.$emit('handle-choose-price', item);
    },
    handleChoosePriceCustom() {
      this.$emit(
        'handle-choose-price-custom',
        parseInt(this.minPriceFilter || '0'),
        parseInt(this.maxPriceFilter || '999')
      );
    },
    handleChangeSelectedAgency() {
      const seletedItems = this.agencyItems.filter((i: any) => i.selected);
      if (seletedItems && seletedItems.length != 0) {
        const query = {
          ...this.$route.query,
          agencyItems: seletedItems.map((i: any) => i.name).join(','),
        };
        this.$router.replace({ query: query || {} });
      } else {
        const query = { ...this.$route.query };
        delete query['agencyItems'];
        this.$router.replace({ query: query || {} });
      }
    },
    handleChangeSelectedBrand() {
      const seletedItems = this.brandItems.filter((i: any) => i.selected);
      if (seletedItems && seletedItems.length != 0) {
        const query = {
          ...this.$route.query,
          brandItems: seletedItems.map((i: any) => i.name).join(','),
        };
        this.$router.replace({ query: query || {} });
      } else {
        const query = { ...this.$route.query };
        delete query['brandItems'];
        this.$router.replace({ query: query || {} });
      }
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
.catalog-screen {
  background-color: transparent;
  .header-customer {
    height: 21px;
    line-height: 21.09px;
    font-weight: bold;
    font-size: 16px;
  }

  .item-customer {
    height: 24px;
    margin-top: 2px;
    line-height: 14px;
    font-weight: 300px;
    font-size: 12px;
  }

  .item-checkbox-customer .v-label {
    line-height: 14px;
    font-weight: 300px;
    font-size: 12px;
    color: #000000;
  }
}
</style>

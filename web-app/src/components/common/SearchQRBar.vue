<template>
  <v-card
    :height="innerHeight"
    width="100vw"
    class="elevation-0 bg-primary-color-0 d-flex flex-column justify-start align-center"
  >
    <StreamBarcodeReader @decode="onDecode" @loaded="onLoaded"></StreamBarcodeReader>
    <v-card-text class="px-0" v-for="(item, index) in listSearchItem" :key="`${index}-search-item-qr-bar-${item.SK}`">
      <v-hover v-slot="{ hover }">
        <v-list-item
          @click="goToItem(item)"
          :class="hover ? ' bg-primary-color-0' : ''"
          style="padding: 0px !important"
        >
          <v-avatar tile size="32">
            <img :src="item.listImage[0]" :alt="`small-image-${item.name}`" />
          </v-avatar>
          <v-list-item-title class="px-3 font-size-12 d-flex-col align-center justify-start" style="max-width: 600px">
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
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { StreamBarcodeReader } from 'vue-barcode-reader';
import Vue from 'vue';
import AuthService from '@/api/auth.service';
import ProductService, { ProductItem } from '@/api/product.service';

export default Vue.extend({
  components: { StreamBarcodeReader },
  data: () => ({
    listSearchItem: [] as ProductItem[],
    listHasAlreadySearch: [] as string[],
  }),
  computed: {
    widthMenu(): number {
      const width = this.isMobile ? innerWidth : 400;
      return Math.min(width, 400);
    },
    innerWidth(): number {
      return this.$store.getters.innerWidth;
    },
    innerHeight(): number {
      return this.$store.getters.innerHeight;
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
    goToItem(item: ProductItem) {
      this.$router.push(ProductService.getSlugId(item));
    },
    async onDecode(text: string) {
      console.log(`Decode text from QR code is ${text}`);
      if (text.includes('http') && AuthService.isValidHttpUrl(text) && !this.listHasAlreadySearch.includes(text)) {
        const listSearchItemSK = this.listSearchItem.map((i: ProductItem) => i.SK);
        this.listHasAlreadySearch.push(text);
        const listSearchItem = await ProductService.querySearchItemsByUrl({ searchUrl: text });

        this.listSearchItem = this.listSearchItem.concat(
          listSearchItem.filter((i: ProductItem) => {
            return !listSearchItemSK.includes(i.SK);
          })
        );
        console.log('listSearchItem', listSearchItem);
      }
    },
    onLoaded() {
      console.log(`Ready to start scanning barcodes`);
    },
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

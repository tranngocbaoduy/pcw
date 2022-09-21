<template>
  <v-card width="100vw" class="elevation-0 bg-primary-color-0 d-flex flex-column justify-start align-center">
    <v-card-text
      class="pa-1 rounded-0"
      v-for="(item, index) in listSearchItem"
      :class="item.isDisplayHover ? 'bg-primary-color-8' : ''"
      :key="`${index}-search-item-qr-bar-${item.SK}`"
    >
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
    <StreamBarcodeReader v-if="!isPaused" @decode="onDecode" @loaded="onLoaded"></StreamBarcodeReader>
    <div
      v-else
      class="bg-primary-color-6 px-1"
      :style="`height:${innerWidth * 0.7}px; width:${innerWidth * 0.9}px;`"
    ></div>
    <v-snackbar :timeout="2000" color="primary" v-model="snackbar" :vertical="vertical">
      {{ text }}
    </v-snackbar>
  </v-card>
</template>

<script lang="ts">
async function sleep(min: number, max: number) {
  return new Promise((res) => setTimeout(res, Math.floor(Math.random() * (max - min + 1)) + min));
}
import { StreamBarcodeReader } from 'vue-barcode-reader';
import Vue from 'vue';
import AuthService from '@/api/auth.service';
import ProductService, { ProductItem } from '@/api/product.service';
import CategoryService from '@/api/category.service';

export default Vue.extend({
  components: { StreamBarcodeReader },
  data: () => ({
    listSearchItem: [] as ProductItem[],
    listHasAlreadySearch: {} as any,
    snackbar: false,
    text: 'Lorem ipsum dolor sit amet',
    vertical: true,
    isPaused: false,
    interval: {} as any,
    isSearch: false,
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
      clearTimeout(this.interval);
      if (
        text.includes('http') &&
        AuthService.isValidHttpUrl(text) &&
        !Object.keys(this.listHasAlreadySearch).includes(text) &&
        !this.isSearch
      ) {
        this.isSearch = true;
        const listSearchItemSK = this.listSearchItem.map((i: ProductItem) => i.SK);
        const listSearchItem = await ProductService.querySearchItemsByUrl({ searchUrl: text });
        const addItems = listSearchItem.filter((i: ProductItem) => {
          return !listSearchItemSK.includes(i.SK);
        });
        this.snackbar = true;
        if (addItems && addItems.length != 0) {
          this.listHasAlreadySearch[text] = addItems.map((i) => i.SK);
          this.listSearchItem = this.listSearchItem.concat(addItems);
          this.text = `Tìm được ${addItems.length} sản phẩm`;
          console.log('addItems', addItems);
        } else {
          this.text = `Không tìm thấy sản phẩm`;
        }
        this.isSearch = false;
      } else {
        this.snackbar = true;
        if (Object.keys(this.listHasAlreadySearch).includes(text)) {
          //
          const listSK = this.listHasAlreadySearch[text];
          const listItemFound = this.listSearchItem.filter((i: ProductItem) => listSK.includes(i.SK));
          for (const item of listItemFound) {
            item.isDisplayHover = true;
          }
          const timeout = setTimeout(() => {
            for (const item of listItemFound) {
              item.isDisplayHover = false;
            }
            clearTimeout(timeout);
          }, 2000);
          this.text = `Đã tìm thấy sản phẩm`;
        } else {
          this.text = `Không phải QR Code hợp lệ`;
        }
      }
      this.confirm();
    },

    async confirm() {
      this.interval = setTimeout(async () => {
        clearTimeout(this.interval);
        this.isPaused = true;
        await sleep(200, 200);
        const isConfirm = confirm('Tiếp tục quét QR?');
        if (isConfirm) {
          this.isPaused = false;
          await this.confirm();
        } else {
          this.$emit('change-method-search-to-text');
        }
      }, 1000 * 30);
    },
    onLoaded() {
      this.confirm();
      console.log(`Ready to start scanning barcodes`);
    },
  },
  beforeDestroy() {
    clearTimeout(this.interval);
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

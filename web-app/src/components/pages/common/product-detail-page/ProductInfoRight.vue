<template>
  <div class="product-info-right">
    <v-card>
      <v-row class="pa-0 ma-0">
        <v-col class="pa-0 my-2">
          <v-card-text class="pa-0 mx-3">
            <div class="font-size-16 font-weight-2 mb-2">{{ 'Shopee' | reduceText(6) }}</div>
            <div class="font-size-10 font-weight-1 line-height-16 mb-2">Cửa hàng thương mại điện tử</div>
            <v-row class="ma-0" align="center">
              <v-icon class="mr-2" size="16px"> mdi-web </v-icon>
              <div class="font-size-10 font-weight-1">Website</div>
            </v-row>
          </v-card-text>
        </v-col>
        <v-col class="pa-0 mt-3" align="center">
          <v-img
            class="border-custom-2"
            height="64"
            width="65"
            :src="require('@/assets/f201f0a8baee2ef5ee2adef6ac755c72.jpg')"
          ></v-img>
        </v-col>
      </v-row>
    </v-card>

    <v-card-text class="font-size-12 font-weight-2 pa-0 my-4"
      >Có 7 sản phẩm từ 6 nơi bán, giá từ 23.499.000 - 37.950.000</v-card-text
    >

    <v-card-actions class="pa-0 mb-5">
      <v-btn class="border-custom-1 box-shadow-1" height="44px" width="100%">So sánh giá</v-btn>
    </v-card-actions>

    <v-card height="281px">
      <v-card-title class="t font-size-12 font-weight-2 line-height-16 pt-3 pl-3 pb-1 ma-0">
        Ưu đãi liên quan
      </v-card-title>
      <div>
        <v-card-text class="font-size-10 font-weight-2 py-0" v-for="item in propmotionItems" :key="item.name">
          <v-row class="ma-0 py-2" align="center">
            <v-icon class="mr-2" size="20px"> mdi-{{ item.icon }} </v-icon>
            <div class="line-height-14">
              <div class="font-weight-3">{{ item.name }}</div>
              <div class="font-weight-1">{{ item.subname }}</div>
            </div>
          </v-row>
          <v-divider></v-divider>
        </v-card-text>
      </div>
    </v-card>
  </div>
</template>

<script lang="ts">
import CategoryService from '@/api/category.service';
import Vue from 'vue';
export default Vue.extend({
  data: () => ({
    propmotionItems: [
      { name: 'Bảo hành', subname: '12 Tháng', icon: 'shield-outline' },
      { name: 'Miễn phí giao hàng', subname: 'Cho Đơn Hàng Từ 800K', icon: 'car-estate' },
      { name: '100% hàng chính hãng', icon: 'check-decagram-outline' },
      { name: '15 ngày đổi trả', icon: 'repeat' },
      { name: 'Giảm giá và quà tặng', icon: 'gift' },
      { name: 'Trả góp chỉ từ', subname: '1.055.500đ/Tháng', icon: 'cash' },
    ],
  }),
  filters: {
    reduceText: function (text: string, max: number) {
      return CategoryService.upperCaseFirstLetter(text && text.length > max ? text.slice(0, max - 2) + '...' : text);
    },
  },
});
</script>

<style lang="scss"></style>

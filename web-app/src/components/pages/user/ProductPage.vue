<template>
  <div class="product-page mt-2 pa-0">
    <!-- <BreadCrumbs :breadcrumbs="breadcrumbs" />
    <v-row no-gutters class="d-flex align-center mt-5" align="center">
      <v-col lg="3" md="4" sm="6" xl="3" class="pa-auto ma-auto" v-for="i in product_quantity" :key="i">
        <Product />
      </v-col>
    </v-row>
    <div class="product-pagination font-weight-3 pa-0 mx-0 mb-10 mt-2 float-right">
      <v-pagination v-model="page" :length="5" circle color="black"></v-pagination>
    </div> -->
  </div>
</template>

//
<script lang="ts">
// import Vue from 'vue';
// import Product from '@/components/product/Product.vue';
// import BreadCrumbs from '@/components/common/BreadCrumbs.vue';

// export default Vue.extend({
//   name: 'Body',
//   props: ['isShowMenu'],
//   components: {
//     Product,
//     BreadCrumbs,
//   },
//   data: () => ({
//     page: 1,
//     product_quantity: 12,
//     isShowCatalog: false,
//     // clientWidth: window.innerWidth,
//   }),
//   computed: {
//     breadcrumbs() {
//       return [
//         {
//           text: 'Home',
//           disabled: false,
//           to: '/',
//           exact: true,
//         },
//         {
//           text: 'Điện thoại',
//           to: '/category/1',
//           disabled: false,
//           exact: true,
//         },
//         {
//           text: 'Iphone 12 ProMax',
//           to: '/product/1',
//           disabled: true,
//           exact: true,
//         },
//       ];
//     },
//   },
//   async created() {
//     await this.initialize();
//   },
//   methods: {
//     async initialize() {},
//   },
// });
//
</script>

//
<style lang="scss">
// .product-page {
//   .product-pagination {
//     width: 330px;
//     height: 32px;
//   }
// }
//
</style>

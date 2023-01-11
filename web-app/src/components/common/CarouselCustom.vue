<template>
  <v-carousel class="carousel rounded-lg mt-3" cycle height="400" hide-delimiter-background show-arrows-on-hover>
    <v-carousel-item class="item-carousel" v-for="(item, i) in items" :key="i" :src="item.src"></v-carousel-item>
  </v-carousel>
</template>

<script>
export default {
  data() {
    return {
      items: [
        {
          src: 'https://i0.wp.com/www.androidsage.com/wp-content/uploads/2018/09/Download-iPhone-XS-XS-Max-and-XR-Official-Stock-Wallpapers-min.jpg',
        },
        {
          src: require('@/assets/banner/Top-Banner.png'),
        },
        {
          src: 'https://i0.wp.com/www.androidsage.com/wp-content/uploads/2018/09/Download-iPhone-XS-XS-Max-and-XR-Official-Stock-Wallpapers-min.jpg',
        },
        {
          src: 'https://9to5mac.com/wp-content/uploads/sites/6/2021/06/MacBook-Pro-2020-Review-unboxed.jpg?quality=82&strip=all&w=1600',
        },
      ],
    };
  },
};
</script>
<style lang="scss">
.carousel {
  height: 512px;
  .carousel-item {
  }
}
</style>

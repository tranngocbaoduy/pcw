<template>
  <v-row class="pt-2 pa-0 ma-0">
    <v-col v-for="(item, index) in features" class="py-2 px-1" :key="index" :cols="columns">
      <FeatureCustom :cards="item"></FeatureCustom>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue from 'vue';
import FeatureCustom from '@/components/feature/FeatureCustom.vue';

export default Vue.extend({
  name: 'Body',
  components: {
    FeatureCustom,
  },
  data: () => ({}),
  computed: {
    features() {
      return {
        workstation: {
          title: this.$t('Workstation'),
          Items: [
            {
              subtitle: 'Màn hình',
              src: 'https://hanoicomputercdn.com/media/product/55868_s2421__4_.png',
              flex: 6,
            },
            { subtitle: 'Laptop', src: 'https://maytinhanphat.com.vn/img/image/m/workstation-vs-desktop.jpg', flex: 6 },
            {
              subtitle: 'Video Games',
              src: 'https://www.rollingstone.com/wp-content/uploads/2021/01/AdobeStock_274383137.jpeg?resize=1800,1200&w=450',
              flex: 6,
            },
            {
              subtitle: 'Máy tính',
              src: 'https://www.thurrott.com/wp-content/uploads/sites/2/2017/12/apple-patforms.jpg',
              flex: 6,
            },
          ],
        },

        kitchen: {
          title: this.$t('Kitchen'),
          Items: [
            {
              subtitle: '',
              src: 'https://www.hoteljob.vn/uploads/images/19-01-23-14/May-danh-trung-va-5-dieu-dau-bep-banh-can-biet-02.jpg',
              flex: 12,
            },
          ],
        },

        office: {
          title: this.$t('Office'),
          Items: [
            {
              subtitle: '',
              src: 'https://www.designyourway.net/blog/wp-content/uploads/2010/11/LaCie-Sphere-Hard-Drive-1024x747.jpg',
              flex: 12,
            },
          ],
        },

        health: {
          title: this.$t('Heath Care'),
          Items: [
            {
              subtitle: '',
              src: 'https://genk.mediacdn.vn/139269124445442048/2020/8/7/imgp2213-1596817885635819326205.jpg',
              flex: 12,
            },
          ],
        },

        house: {
          title: this.$t('Smart Home'),
          Items: [
            {
              subtitle: '',
              src: 'https://image.freepik.com/free-photo/digital-tablet-screen-with-smart-home-controller-wooden-table_53876-96317.jpg',
              flex: 12,
            },
          ],
        },

        corporation: {
          title: this.$t('Business Equipment'),
          Items: [
            { subtitle: 'Màn hình', src: 'https://cf.shopee.vn/file/1e38d6b16c9035cd9966a9551890b47b', flex: 6 },
            { subtitle: 'Thiết bị mạng', src: 'https://cf.shopee.vn/file/a4cd7aa2476d3d993174da7d3a598112', flex: 6 },
            {
              subtitle: 'Hội nghị',
              src: 'https://phucanhcdn.com/media/product/36477_panasonic_pt_lb305_ha2.jpg',
              flex: 6,
            },
            {
              subtitle: 'Thuyết trình',
              src: 'https://hanoicomputercdn.com/media/product/55868_s2421__4_.png',
              flex: 6,
            },
          ],
        },
      };
    },
    columns(): number {
      if (this.$vuetify.breakpoint.xl) return 4;
      if (this.$vuetify.breakpoint.lg) return 4;
      if (this.$vuetify.breakpoint.md) return 6;
      if (this.$vuetify.breakpoint.sm) return 6;
      return 12;
    },
  },
});
</script>

<style scoped>
</style>

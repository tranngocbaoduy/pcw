<template>
  <div class="my-4 detail-item-rating d-flex pa-4 rounded-sm" :class="isMobile ? 'flex-column' : ''">
    <div class="ma-auto">
      <v-progress-circular :rotate="270" :size="130" :width="15" :value="ratingScoreOnCircle" color="#1859db">
        <span class="font-size-20 font-weight-bold">{{ ratingScore }} </span>
        <span class="primary-color-4 font-size-14 font-weight-bold">/ 5</span>
      </v-progress-circular>
    </div>
    <div class="d-flex-column pa-2">
      <p class="font-weight-bold font-size-18 mb-2 font-color-customer">Đánh giá sản phẩm:</p>
      <div class="d-flex flex-row-reverse justify-start align-center font-size-14">
        <div
          v-for="(i, index) in numberRatingItems.slice(1, numberRatingItems.length)"
          :key="`${i}-star-${index}`"
          class="mr-2"
        >
          <div
            style="border: 0.5px #bbbbbb solid !important"
            class="white rounded-sm d-flex-block pa-2 block primary-color-3"
          >
            {{ index + 1 }} sao <span class="font-weight-bold primary-color-5"> ({{ i + 1 }})</span>
          </div>
        </div>
      </div>

      <div class="d-flex justify-start align-center mt-2 primary-color-3 font-size-14">
        <div style="border: 0.5px #bbbbbb solid !important" class="mr-2 white rounded-sm d-flex-block pa-2 block">
          Review hình ảnh/ video
          <span class="font-weight-bold primary-color-5"> ({{ itemRating.rcount_with_image }})</span>
        </div>
        <div style="border: 0.5px #bbbbbb solid !important" class="white rounded-sm d-flex-block pa-2 block">
          Review nội dung <span class="font-weight-bold primary-color-5"> ({{ itemRating.rcount_with_context }})</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  props: ['itemRating'],
  data: () => ({}),
  created() {},
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
    ratingScoreOnCircle(): number {
      return this.itemRating && this.itemRating.rating_star ? (this.itemRating.rating_star / 5) * 100 : 0;
    },
    ratingScore(): number | string {
      return this.itemRating && this.itemRating.rating_star ? parseFloat(this.itemRating.rating_star).toFixed(2) : 0;
    },
    numberRatingItems(): [] {
      return this.itemRating.rating_count;
    },
  },
  methods: {},
});
</script>

<style lang="scss">
.detail-rating-item {
}
</style>

<template>
  <div
    class="item-rating d-flex justify-start align-center pa-0 pl-0"
    @click="() => (isDisplay ? trasnsitionToDetailRatingItem() : '')"
  >
    <!-- <span class="primary-color-2 font-weight-bold pr-1 font-size-14" v-if="isDisplay">
      [{{ itemRating.rating_star }}]
    </span> -->
    <v-rating
      :value="itemRating.rating_star"
      :color="'#d0011b'"
      dense
      half-increments
      readonly
      :size="size ? size : 14"
    ></v-rating>
  </div>
</template>

<script lang="ts">
import CategoryService from '@/api/category.service';
import Vue from 'vue';

export default Vue.extend({
  props: ['itemRating', 'isDisplay', 'size'],
  data: () => ({}),
  created() {},
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
  },
  methods: {
    trasnsitionToDetailRatingItem() {
      (document as any).getElementById('detail-rating-item').scrollIntoView({ behavior: 'smooth' });
      this.$emit('choose-review');
    },
  },
});
</script>

<style lang="scss">
.item-rating {
}
</style>

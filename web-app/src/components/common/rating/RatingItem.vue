<template>
  <div
    class="item-rating d-flex justify-start align-center pa-0 pl-0"
    @click="() => (isDisplay ? trasnsitionToDetailRatingItem() : '')"
  >
    <!-- <span class="primary-color-2 font-weight-bold pr-1 font-size-14" v-if="isDisplay">
      [{{ itemRating.rating_star }}]
    </span> -->
    <v-rating :value="itemRating.rating_star" color="#FFA200" dense half-increments readonly size="14"></v-rating>
  </div>
</template>

<script lang="ts">
import CategoryService from '@/api/category.service';
import Vue from 'vue';

export default Vue.extend({
  props: ['itemRating', 'isDisplay'],
  data: () => ({}),
  created() {},
  computed: {
    isMobile(): boolean {
      return this.$store.getters.isMobile;
    },
  },
  methods: {
    trasnsitionToDetailRatingItem() {
      console.log('trasnsitionToDetailRatingItem');
      (document as any).getElementById('detail-rating-item').scrollIntoView({ behavior: 'smooth' });
    },
  },
});
</script>

<style lang="scss">
.item-rating {
}
</style>

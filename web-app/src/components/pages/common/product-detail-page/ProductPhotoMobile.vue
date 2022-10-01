<template>
  <div v-if="listPhotoItems && listPhotoItems.length != 0" style="background-color: transparent">
    <v-hover v-slot="{ hover }">
      <v-card
        class="rounded-0 d-flex align-center justify-center"
        height="276px"
        :elevation="0"
        style="background-color: transparent"
      >
        <v-img :class="hover ? 'pt-1' : 'pt-2'" contain width="270px" height="270px" :src="currentPhoto"></v-img>
      </v-card>
    </v-hover>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  props: ['listPhotoItems', 'domain'],
  data() {
    return {
      currentPhoto: {} as any,
      isLoadingImage: true,
    };
  },
  watch: {
    listPhotoItems() {
      if (this.listPhotoItems && this.listPhotoItems.length != 0) this.refreshImage();
    },
  },
  created() {
    this.refreshImage();
  },
  methods: {
    getMainImage(selectPhoto: any) {
      this.isLoadingImage = true;
      if (selectPhoto.selected == true) {
        selectPhoto.selected = false;
        this.refreshImage();
      } else {
        selectPhoto.selected = true;
      }
      this.currentPhoto = selectPhoto;
      this.isLoadingImage = false;
    },
    refreshImage() {
      this.currentPhoto = this.listPhotoItems[0] as any;
      this.isLoadingImage = false;
    },
  },

  computed: {
    currentPhotoUrl(): string {
      return '';
    },
    remainPhotos(): any {
      let remainPhotos = this.listPhotoItems.filter((i: any) => i.url != this.currentPhotoUrl);
      if (this.$vuetify.breakpoint.xl) remainPhotos = remainPhotos.slice(0, 4);
      if (this.$vuetify.breakpoint.lg) remainPhotos = remainPhotos.slice(0, 4);
      if (this.$vuetify.breakpoint.md) remainPhotos = remainPhotos.slice(0, 2);
      return remainPhotos.slice(0, 2);
    },
  },
});
</script>

<style lang="scss">
.product-photo {
}
</style>

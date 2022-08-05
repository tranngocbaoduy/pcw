<template>
  <div v-if="listPhotoItems && listPhotoItems.length != 0">
    <div class="d-flex justify-center align-center px-0 py-0">
      <div v-for="photo in remainPhotos" :key="photo.name" class="py-0 px-2">
        <v-hover v-slot="{ hover }">
          <v-card
            @click="getMainImage(photo)"
            :width="140"
            :height="140"
            :elevation="hover ? 12 : 2"
            :class="hover ? 'pa-2' : 'pa-3'"
          >
            <v-img class="" width="100%" height="100%" :src="photo.url"></v-img>
          </v-card>
        </v-hover>
      </div>
    </div>
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
  created() {},
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

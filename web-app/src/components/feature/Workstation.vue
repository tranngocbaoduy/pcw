<template>
  <v-card class="parent-workstation">
    <v-container fluid>
      <v-card-title class="parent-workstation-header"> Workstation </v-card-title>
      <div class="parent-workstation-content">
        <div>
          <v-row dense>
            <v-col v-for="card in cards" :key="card.title" :cols="card.flex">
              <v-card class="d-inline-flex">
                <v-img
                  :src="card.src"
                  class="white--text align-end"
                  font-size="18px"
                  gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                >
                  <v-card-title v-text="card.title"></v-card-title>
                </v-img>
              </v-card>
            </v-col>
          </v-row>
        </div>
        <div class="float-right">
          <span> Xem thêm </span>
          <v-icon size="20px">mdi-chevron-right</v-icon>
        </div>
      </div>
    </v-container>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    cards: [
      { title: 'Màn hình', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 6 },
      { title: 'Laptop', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 6 },
      { title: 'Video Games', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 6 },
      { title: 'Máy tính', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 6 },
    ],
  }),
};
</script>

<style scoped>
.parent-workstation {
  width: 430px;
  height: 444px;
  margin-right: 12px;
}
.parent-workstation-header {
  height: 29px;
  font-family: 'roboto';
  font-weight: 400px;
  font-size: 24px;
  margin-bottom: 30px;
}
.d-inline-flex {
  width: 189px;
  height: 152px;
}

.float-right {
  width: 88px;
  height: 24px;
  font-family: 'roboto';
  font-weight: 400px;
  font-size: 14px;
  margin-top: 10px;
}
</style>

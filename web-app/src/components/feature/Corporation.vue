<template>
  <v-card class="parent-corporation">
    <v-container fluid>
      <v-card-title class="parent-corporation-header"> Thiết bị doanh nghiệp </v-card-title>
      <div class="parent-corporation-content">
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
      { title: 'Thiết bị mạng', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 6 },
      { title: 'Hội nghị', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 6 },
      { title: 'Thuyết trình', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 6 },
    ],
  }),
};
</script>

<style lang="scss">
.parent-corporation {
  width: 430px;
  height: 444px;

  .parent-corporation-header {
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
}
</style>

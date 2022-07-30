<template>
  <v-card class="parent-office">
    <v-container fluid>
      <v-card-title class="parent-office-header"> Văn phòng </v-card-title>
      <div class="parent-office-content">
        <v-card>
          <v-img
            src="https://cdn.vuetifyjs.com/images/cards/house.jpg"
            gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
            height="320"
          ></v-img>
        </v-card>
      </div>
      <div class="float-right">
        <span> Xem thêm </span>
        <v-icon size="20px">mdi-chevron-right</v-icon>
      </div>
    </v-container>
  </v-card>
</template>

<script>
export default {
  data: () => ({}),
};
</script>

<style scoped>
.parent-office {
  width: 430px;
  height: 444px;
}
.parent-office-header {
  height: 29px;
  font-family: 'roboto';
  font-weight: 400px;
  font-size: 24px;
  margin-bottom: 30px;
}

.float-right {
  width: 88px;
  height: 24px;
  font-family: 'roboto';
  font-weight: 400px;
  font-size: 14px;
  margin-top: 15px;
}
</style>

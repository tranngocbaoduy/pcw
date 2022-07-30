<template>
  <v-hover v-slot="{ hover }">
    <v-card :elevation="hover ? 12 : 2" :loading="loading" class="rounded-lg box-sizing pa-4 mb-4 mx-2">
      <v-row>
        <v-col cols="6"> <v-img class="box-sizing rounded-0" :src="comparisonItems.img"></v-img></v-col>
        <v-col cols="6">
          <v-list>
            <!-- <v-list-item-group> -->
            <v-list-item flat elevation="0" v-for="(item, i) in comparisonItems.stores" :key="i">
              <v-list-item-content>
                <v-row class="mx-0 py-2" align="center">
                  <v-col
                    cols="4"
                    style="max-height: 20px !important; max-width: 20px !important"
                    class="font-size-14 font-weight-2 pa-0 my-0 mr-3 mt-1"
                  >
                    <v-img class="box-sizing ma-auto mt-1" :src="item.logoUrl"></v-img>
                  </v-col>
                  <v-col cols="8" class="font-size-14 font-weight-2 pa-0 pt-3"> {{ item.name }} </v-col>
                  <div
                    style="width: 100%"
                    class="my-0"
                    v-for="(price, index) in item.prices"
                    :key="index"
                    align="center"
                  >
                    <v-hover v-slot="{ hover }">
                      <a :href="item.urlKeys[index]" target="_blank">
                        <v-row
                          class="pa-0 mt-3 py-2"
                          :class="hover ? ' font-weight-3 font-size-16' : ''"
                          :elevation="hover ? 12 : 2"
                        >
                          <v-col
                            cols="9"
                            class="py-0 text-left font-size-14 my-0 primary-color-1 font-weight-2"
                            :class="hover ? ' font-weight-3 font-size-16' : ''"
                          >
                            {{ price | formatPrice }}đ
                          </v-col>
                          <v-col cols="3" class="pa-0 my-0"> <v-icon size="14"> mdi-arrow-right </v-icon></v-col>
                        </v-row>
                      </a>
                    </v-hover>
                  </div>
                </v-row>
              </v-list-item-content>
            </v-list-item>
            <!-- </v-list-item-group> -->
          </v-list></v-col
        >
      </v-row>

      <v-card-title class="font-size-22 font-weight-3" height="50">
        {{ comparisonItems.name | reduceText(100) }}
      </v-card-title>
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  props: ['comparisonItems'],
  data: () => ({
    loading: false,
    selection: 1,
  }),

  filters: {
    reduceText: function (text: string, max: number) {
      return text.length > max ? text.slice(0, max - 2) + '...' : text;
    },
    formatPrice(value: string) {
      // const val = (value / 1).toFixed(0).replace('.', ',');
      return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },
  },
  computed: {},

  methods: {},
});
</script>

<style lang="scss"></style>

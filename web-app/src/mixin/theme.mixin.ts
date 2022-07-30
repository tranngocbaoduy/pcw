import Vue from 'vue';

const MAIN_COLOR = {
  BLACK_THEME: ['1c2321', '7d98a1', '5e6572', 'a9b4c2', 'eef1ef'] as string[],
  WHITE_THEME: ['e5d4ed', '6d72c3', '5941a9', '514f59', '1d1128'] as string[],
  CUSTOM_THEME: ['f06543', 'e8e9eb', 'e0dfd5', '313638', 'f09d51'] as string[],
};

export interface MAIN_THEME {
  name?: 'BLACK_THEME' | 'WHITE_THEME';
}

const updateColorTheme = Vue.extend({
  data: () => {},
  created() {
    this.setColorTheme();
  },
  methods: {
    setColorTheme(): string[] {
      // return MAIN_COLOR[MAIN_THEME.name] || ;
      return [];
    },
  },
});

Vue.mixin(updateColorTheme);

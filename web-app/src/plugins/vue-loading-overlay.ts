import Vue from 'vue';

import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';
// define the plugin and pass object for config

Vue.use(Loading, {
  color: '#e5d4ed',
  loader: 'dots',
});

import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import i18n from './i18n';
import './plugins/vee-validate';
import VueLodash from 'vue-lodash';
import lodash from 'lodash';
//register component
import '@/mixin';
import './plugins/vue-loading-overlay';
import VueMeta from 'vue-meta';
import '@/vue-meta';
import './registerServiceWorker';

(function (original) {
  (console as any).enableLogging = function () {
    (console as any).log = original;
  };
  (console as any).disableLogging = function () {
    (console as any).log = function () {};
  };
})((console as any).log);

Vue.use(VueMeta, {
  // optional pluginOptions
  refreshOnceOnNavigation: true,
});
Vue.config.productionTip = false;
Vue.config.devtools = process.env.NODE_ENV === 'production' ? false : true;
process.env.NODE_ENV === 'production' ? (console as any).disableLogging() : (console as any).enableLogging();

Vue.use(VueLodash, { name: 'custom', lodash: lodash });

new Vue({
  router,
  store,
  vuetify,
  i18n,
  render: (h) => h(App),
}).$mount('#app');

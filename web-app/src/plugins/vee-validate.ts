import Vue from 'vue';
import { configure, ValidationObserver, ValidationProvider, setInteractionMode } from 'vee-validate';
// import { required, email, max, min, confirmed, min_value, max_value } from 'vee-validate/dist/rules';
import i18n from '@/i18n';

setInteractionMode('lazy');

configure({
  defaultMessage: (field: any, params: any) => {
    if (params && params._rule_) {
      params._field_ = i18n.t(`fields.${field}`);
      params._special_braces_ = ' {  } ';
      return i18n.t(`validation.${params._rule_}`, params).toString();
    }
    return i18n.t(field, params).toString();
  },
});

Vue.component('ValidationObserver', ValidationObserver);
Vue.component('ValidationProvider', ValidationProvider);

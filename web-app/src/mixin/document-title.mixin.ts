import Vue from 'vue';
import i18n from '@/i18n';

const updateDocumentTitleMixin = Vue.extend({
  data: () => ({
    documentTitle: undefined,
  }),

  created() {
    if (!this.documentTitle) return;

    if (this.documentTitle === 'default') {
      document.title = i18n.t(`documentTitles.${this.documentTitle}`).toString();
    } else {
      document.title =
        i18n.t(`documentTitles.${this.documentTitle}`).toString() + ' — ' + i18n.t(`documentTitles.default`).toString();
    }
  },
  methods: {},
});

Vue.mixin(updateDocumentTitleMixin);

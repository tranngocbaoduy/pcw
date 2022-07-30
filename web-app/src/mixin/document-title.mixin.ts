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
  methods: {
    code2category(code: any) {
      const categoryDict = {
        AIRCONDITION: 'Air Condition',
        FRIDGE: 'Fridge',
        LAPTOP: 'Laptop',
        PHONE: 'Phone',
        TELEVISION: 'Television',
        WASHING: 'Washing',
      } as any;
      return categoryDict[code.toUpperCase()];
    },
    category2code(category: any) {
      const categoryDict = {
        'Air Condition': 'AIRCONDITION',
        Fridge: 'FRIDGE',
        Laptop: 'LAPTOP',
        Phone: 'PHONE',
        Television: 'TELEVISION',
        Washing: 'WASHING',
      } as any;
      return categoryDict[category];
    },
  },
});

Vue.mixin(updateDocumentTitleMixin);

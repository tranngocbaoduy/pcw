import Vue from 'vue';
function setValue(obj: any, path: string, value: any) {
  const a = path.split('.');
  let o = obj;
  while (a.length - 1) {
    const n: any = a.shift();
    if (!(n in o)) o[n] = {};
    o = o[n];
  }
  o[a[0]] = value;
}

function getValue(obj: any, path: string) {
  path = path.replace(/\[(\w+)\]/g, '.$1');
  path = path.replace(/^\./, '');
  const a = path.split('.');
  let o = obj;
  while (a.length) {
    const n: any = a.shift();
    if (!(n in o)) return;
    o = o[n];
  }
  return o;
}

const urlQueryMixin = Vue.extend({
  data: () => ({
    urlQueryWatchers: [] as any,
    isInitUrlQuery: true,
  }),

  mounted() {
    if ((this as any).isWaitingLoadInit) {
      return;
    } else {
      this.setUrlQueryData();
    }
  },

  methods: {
    watchingData() {
      for (const item of this.urlQueryWatchers) {
        const { name, type } = item;
        this.$watch(`${name}`, () => this.updateUrlQuery(name, type), { deep: true });
      }
    },
    setUrlQueryData() {
      if (this.isInitUrlQuery) {
        this.isInitUrlQuery = false;
        this.watchingData();
      }
      const urlParams = new URLSearchParams(window.location.search);
      for (const item of this.urlQueryWatchers) {
        const { name, type } = item;
        try {
          if (urlParams.has(name)) {
            if (type === 'string') setValue(this, name, urlParams.get(name));
            else if (type === 'date') setValue(this, name, new Date(urlParams.get(name) as any));
            else setValue(this, name, JSON.parse(urlParams.get(name) as any));
          }
        } catch {
          // console.log(name, type);
        }
      }
    },
    updateUrlQuery(name: string, type: string) {
      const urlParams = new URLSearchParams(window.location.search);
      if (type === 'string' || type === 'date') urlParams.set(name, getValue(this, name));
      else urlParams.set(name, JSON.stringify(getValue(this, name)));

      const queryUrl = urlParams.toString();
      history.replaceState({}, '', `${this.$route.path}?${queryUrl}`);
    },
  },
});

Vue.mixin(urlQueryMixin);

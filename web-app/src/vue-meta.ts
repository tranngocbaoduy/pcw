import Vue, { ComponentOptions } from 'vue';
import { MetaInfo } from 'vue-meta';
import { MetaInfoComputed } from 'vue-meta/types/vue-meta';
declare module 'vue/types/options' {
  interface ComponentOptions<V extends Vue> {
    metaInfo?: MetaInfo | MetaInfoComputed | undefined;
  }
}

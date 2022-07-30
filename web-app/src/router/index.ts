import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import RouterHelper from './helper';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    component: () => import('@/views/Home.vue').catch(RouterHelper.handleAsyncComponentError),
    children: [
      {
        path: '',
        name: 'HomePage',
        component: () => import('@/components/pages/user/HomePage.vue').catch(RouterHelper.handleAsyncComponentError),
      },
      {
        path: '/category/:idCate',
        name: 'CategoryPage',
        component: () =>
          import('@/components/pages/user/CategoryPage.vue').catch(RouterHelper.handleAsyncComponentError),
      },
      {
        path: '/category/:idCate/product/:idProd',
        name: 'ProductDetailPage',
        component: () =>
          import('@/components/pages/user/ProductDetailPage.vue').catch(RouterHelper.handleAsyncComponentError),
      },
      {
        path: '/compare',
        name: 'ComparasionPage',
        component: () =>
          import('@/components/pages/user/PriceComparisonPage.vue').catch(RouterHelper.handleAsyncComponentError),
      },
    ],
  },
  {
    path: '/sys',
    name: 'sys',
    component: () => import('@/views/SysHome.vue').catch(RouterHelper.handleAsyncComponentError),
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ '@/views/About.vue').catch(RouterHelper.handleAsyncComponentError),
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;

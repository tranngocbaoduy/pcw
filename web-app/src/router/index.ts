import GoogleAuthService, { UserGoogleInfo } from '@/api/google-auth.service';
import store from '@/store';
import Vue from 'vue';
import VueRouter, { RawLocation, Route, RouteConfig } from 'vue-router';
import RouterHelper from './helper';
import moment from 'moment-timezone';
import SeoService from '@/api/seo.service';
import i18n from '@/i18n';
import CategoryService from '@/api/category.service';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    component: () => import('@/views/Home.vue').catch(RouterHelper.handleAsyncComponentError),
    children: [
      {
        path: '',
        name: '',
        component: () => import('@/components/pages/user/HomePage.vue').catch(RouterHelper.handleAsyncComponentError),
      },
      {
        path: '/home',
        name: 'HomePage',
        component: () => import('@/components/pages/user/HomePage.vue').catch(RouterHelper.handleAsyncComponentError),
      },
      {
        path: '/login',
        name: 'LoginPage',
        component: () =>
          import('@/components/pages/user/LoginAccount.vue').catch(RouterHelper.handleAsyncComponentError),
      },
      {
        path: '/category/:idCate',
        name: 'CategoryPage',
        component: () =>
          import('@/components/pages/user/CategoryPage.vue').catch(RouterHelper.handleAsyncComponentError),
      },
      {
        path: '/compare',
        name: 'ComparasionPage',
        component: () =>
          import('@/components/pages/user/PriceComparisonPage.vue').catch(RouterHelper.handleAsyncComponentError),
      },
      {
        path: ':slugId*',
        name: 'ProductDetailSlugPage',
        component: () =>
          import('@/components/pages/user/ProductDetailSlugPage.vue').catch(RouterHelper.handleAsyncComponentError),
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

function logout() {
  localStorage.setItem('google-auth', '');
  localStorage.removeItem('google-auth');
  store.dispatch('logout');
}
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  console.log(to);
  new Promise<RawLocation | undefined>((resolve) => {
    if (!store.getters.isAuthenticated) {
      let userGoogleInfo: any = localStorage.getItem('google-auth');
      if (userGoogleInfo) {
        userGoogleInfo = JSON.parse(userGoogleInfo);
        if (userGoogleInfo && userGoogleInfo.id) {
          GoogleAuthService.getUserInfo(userGoogleInfo.id).then(async (data: UserGoogleInfo) => {
            if (-1 * moment().diff(data.expriedAt, 'minute') < 0) {
              logout();
            } else {
              store.dispatch('login', { data });
              console.log('[FIRST INITIALIZED] =>', data);
            }
          });
        } else {
          logout();
        }
      }
    } else {
      console.log('[INITIALIZED] =>', store.getters.userGoogleInfo);
    }
    resolve(undefined);
  }).then((location) => {
    if (!to.fullPath.includes('/login') && to.fullPath.includes('%2F')) {
      next(decodeURIComponent(to.fullPath));
    }
    if (location) next(location);
    else if (to.path === from.path && to.fullPath.length < from.fullPath.length) {
      // Do nothing
    } else next();
  });
});

export default router;

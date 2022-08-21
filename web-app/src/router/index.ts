import Vue, { VueConstructor } from 'vue';
import VueRouter, { RawLocation, Route, RouteConfig } from 'vue-router';
import RouterHelper from './helper';

// export function register(Vue: VueConstructor) {
//   const routerPush = VueRouter.prototype.push;
//   const routerReplace = VueRouter.prototype.push;

//   const isNavigationDuplicated = (currentRoute: any, nextRoute: any) => {
//     const { name: nextName, params: nextParams = {}, query: nextQuery = {} } = nextRoute;
//     const { name, params, query } = currentRoute;

//     return equals(nextQuery, query) && equals(nextParams, params) && equals(nextName, name);
//   };

//   VueRouter.prototype.push = async function push(location: RawLocation): Promise<Route | any> {
//     if (!isNavigationDuplicated(this.currentRoute, location)) {
//       return await routerPush.call(this, location);
//     }
//   };

//   VueRouter.prototype.replace = async function replace(location: RawLocation): Promise<Route | any> {
//     if (!isNavigationDuplicated(this.currentRoute, location)) {
//       return await routerReplace.call(this, location);
//     }
//   };

//   Vue.use(VueRouter);
// }
// register(Vue);
Vue.use(VueRouter);

// const superPush = VueRouter.prototype.push;
// VueRouter.prototype.push = async function push(loc: RawLocation): Promise<Route> {
//   try {
//     return await superPush.bind(this)(loc);
//   } catch (e) {
//     if (e?.name === 'NavigationDuplicated') {
//       console.warn(e);
//       console.log(e);
//       return await superPush.bind(this)(loc);
//     } else {
//       throw e;
//     }
//   }
// };

// const superReplace = VueRouter.prototype.replace;
// VueRouter.prototype.replace = async function replace(loc: RawLocation): Promise<Route> {
//   try {
//     return await superReplace.bind(this)(loc);
//   } catch (e) {
//     if (e?.name === 'NavigationDuplicated') {
//       console.warn(e);
//       return await superReplace.bind(this)(loc);
//     } else {
//       throw e;
//     }
//   }
// };

// Vue.use(VueRouter);

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

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  console.log(to);
  new Promise<RawLocation | undefined>((resolve) => {
    resolve(undefined);
  }).then((location) => {
    if (to.fullPath.includes('%2F')) {
      next(decodeURIComponent(to.fullPath));
    }
    if (location) next(location);
    else if (to.path === from.path && to.fullPath.length < from.fullPath.length) {
      // Do nothing
    } else next();
  });
});

export default router;

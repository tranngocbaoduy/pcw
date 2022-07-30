import Vue from 'vue';
import Vuex from 'vuex';
import { CognitoUser } from '@aws-amplify/auth';
import { ProductItem } from '@/api/product.service';

Vue.use(Vuex);

interface RootState {
  userName: string;
  user: CognitoUser;
  categoryItems: any[];
  domainItems: any[];
  searchString: string;

  brandItemsStore: {};

  isMobile: boolean;
  innerWidth: number;
}

interface ProductItemByCategory {
  brandsItems?: any[] | [];
  productItems?: ProductItem[] | [];
  agencyItems?: any[] | [];
}

const state: RootState = {
  userName: '',
  user: {} as CognitoUser,
  categoryItems: [] as any[],
  searchString: '',
  brandItemsStore: {},
  isMobile: false,
  innerWidth: 0,

  domainItems: [
    {
      id: 'bmd1eWVua2ltLmNvbQ',
      name: 'Nguyễn Kim',
      url: 'nguyenkim.com',
      logoUrl: require('@/assets/shop-logo/nguyen-kim.png'),
      selected: false,
    },
    {
      id: 'bWV0YS52bg',
      name: 'Meta',
      url: 'meta.vn',
      logoUrl: require('@/assets/shop-logo/meta.png'),
      selected: false,
    },
    {
      id: 'dGlraS52bg',
      name: 'Tiki',
      url: 'tiki.vn',
      logoUrl: require('@/assets/shop-logo/tiki.png'),
      selected: false,
    },
    {
      id: 'dm9zby52bg',
      name: 'Vỏ sò',
      url: 'voso.vn',
      logoUrl: require('@/assets/shop-logo/vo-so.png'),
      selected: false,
    },
    {
      id: 'ZGllbm1heXhhbmguY29t',
      name: 'Điện máy xanh',
      url: 'dienmayxanh.com',
      logoUrl: require('@/assets/shop-logo/dien-may-xanh.png'),
      selected: false,
    },
    {
      id: 'bmhhbmhhdnVpLmNvbS52bg',
      name: 'Nhà Nhà Vui',
      url: 'nhanhavui.com.vn',
      logoUrl: require('@/assets/shop-logo/nhanhavui.png'),
      selected: false,
    },
    {
      id: 'aG5hbW1vYmlsZS5jb20',
      name: 'HNam Mobile',
      url: 'hnammobile.com',
      logoUrl: require('@/assets/shop-logo/hnammobile.jpg'),
      selected: false,
    },
    {
      id: 'ZGlkb25ndGhvbmdtaW5oLnZu',
      name: 'Di Động Thông Minh',
      url: 'didongthongminh.vn',
      logoUrl: require('@/assets/shop-logo/didongthongminh.png'),
      selected: false,
    },
    {
      id: 'aG9hbmdoYW1vYmlsZS5jb20',
      name: 'Hoàng Nam Mobile',
      url: 'hoanghamobile.com',
      logoUrl: require('@/assets/shop-logo/hoangnammobile.jpg'),
      selected: false,
    },
    {
      id: 'bWVkaWFtYXJ0LnZu',
      name: 'Media Mart',
      url: 'mediamart.vn',
      logoUrl: require('@/assets/shop-logo/mediamart.jpeg'),
      selected: false,
    },
    {
      id: 'c2lldXRoaWdpYWtoby5jb20',
      name: 'Siêu thị giá kho',
      url: 'sieuthigiakho.com',
      logoUrl: require('@/assets/shop-logo/sieuthigiakho.png'),
      selected: false,
    },
    {
      id: 'cGh1Y2FuaC52bg',
      name: 'Phú Cảnh',
      url: 'phucanh.vn',
      logoUrl: require('@/assets/shop-logo/dien-may-xanh.png'),
      selected: false,
    },
    {
      id: 'cGljby52bg',
      name: 'Pico',
      url: 'pico.vn',
      logoUrl: require('@/assets/shop-logo/pico.jpg'),
      selected: false,
    },
    {
      id: 'd3d3LnRoZWdpb2lkaWRvbmcuY29t',
      name: 'Thế giới di động',
      url: 'www.thegioididong.com',
      logoUrl: require('@/assets/shop-logo/tgdd.jpeg'),
      selected: false,
    },
    {
      id: 'Y2VsbHBob25lcy5jb20udm4',
      name: 'Cell Phone',
      url: 'cellphones.com.vn',
      logoUrl: require('@/assets/shop-logo/cellphoneS.png'),
      selected: false,
    },
    {
      id: 'ZWNvLW1hcnQudm4',
      name: 'Eco Mart',
      url: 'eco-mart.vn',
      logoUrl: require('@/assets/shop-logo/eco-mart.png'),
      selected: false,
    },
    {
      id: 'ZGllbm1heXBsdXMuY29t',
      name: 'Điện Máy Plus',
      url: 'dienmayplus.com',
      logoUrl: require('@/assets/shop-logo/dienmayplus.png'),
      selected: false,
    },
    {
      id: 'ZGlkb25nbWFuZ28uY29t',
      name: 'DD Mango',
      url: 'didongmango.com',
      logoUrl: require('@/assets/shop-logo/dien-may-xanh.png'),
      selected: false,
    },
    {
      id: 'ZGllbnRob2FpbW9pLnZu',
      name: 'Điện thoại mới',
      url: 'dienthoaimoi.vn',
      logoUrl: require('@/assets/shop-logo/dienthoaimoi.png'),
      selected: false,
    },
    {
      id: 'ZGllbm1heXRoYW5oLmNvbQ',
      name: 'Điện máy thanh',
      url: 'dienmaythanh.vn',
      logoUrl: require('@/assets/shop-logo/dienmaythanh.png'),
      selected: false,
    },
    {
      id: 'ZnB0c2hvcC5jb20udm4',
      name: 'FPT Shop',
      url: 'fptshop.com.vn',
      logoUrl: require('@/assets/shop-logo/fpt-shop.png'),
      selected: false,
    },
    {
      id: 'ZXNob3BzLnZu',
      name: 'E-shop',
      url: 'eshop.com.vn',
      logoUrl: require('@/assets/shop-logo/eshops.png'),
      selected: false,
    },
    {
      id: 'dmFuY2hpZW4uY29t',
      name: 'Văn Chiến',
      url: 'vanchien.com',
      logoUrl: require('@/assets/shop-logo/vanchien.png'),
      selected: false,
    },
    {
      id: 'ZGllbm1heXRpbnBoYXQuY29t',
      name: 'Điện máy tính phát',
      url: 'dienmaytinphat.com',
      logoUrl: require('@/assets/shop-logo/tinphat.png'),
      selected: false,
    },
  ],
};
export default new Vuex.Store({
  state,
  getters: {
    userName: (state) => state.userName,
    user: (state) => state.user,
    categoryItems: (state) => state.categoryItems,
    domainItems: (state) => state.domainItems,
    searchString: (state) => state.searchString,
    brandItemsStore: () => state.brandItemsStore,

    isMobile: (state) => state.isMobile,
    innerWidth: (state) => state.innerWidth,
  },
  mutations: {
    setState(state, nextState) {
      Object.keys(nextState).forEach((key) => ((state as any)[key as keyof RootState] = nextState[key]));
    },
  },
  actions: {
    signInDefault({ commit }, { user }) {
      commit('setState', { user });
    },
    setCategory({ commit }, { categoryItems }) {
      commit('setState', { categoryItems });
    },
    setIsMobile({ commit }, { isMobile }) {
      commit('setState', { isMobile: isMobile });
    },
    setInnerWidth({ commit }, { innerWidth }) {
      commit('setState', { innerWidth: innerWidth });
    },
  },
  modules: {},
});

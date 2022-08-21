import AuthService from '@/api/auth.service';
import { int } from 'aws-sdk/clients/datapipeline';

export interface ProductSearchItem {
  PK: string;
  SK: string;
  name: string;
}

export interface ProductItem {
  PK: string;
  SK: string;
  id: string;
  relationshipID: string;
  listChildId: string[];
  listImage: string[];
  content: string;
  createdDate?: string;
  domain: string;
  nameDomain: string;
  name: string;
  cleanName: string;
  price: number;
  listPrice: number;
  isAPI?: boolean;
  productCode: string;
  brand: string;
  url: string;
  discountRate: number;
  shopLocation?: string;
  historicalSold: string;
  likedCount: string;
  slugId: string;
  stock: number;
  subCategory: string;
  voucherInfo: {};
  itemRating: {};
  countReview: number;
}

export interface QueryProductItems {
  PK: string;
  SK: string;
  PRODUCTS: any[];
}

export default class ProductService {
  static async queryItemById({ id, isHasChild = false }: { id: string; isHasChild?: boolean }) {
    const url =
      process.env.VUE_APP_API_BASE_URL +
      `/${process.env.VUE_APP_ENV}/product?action=queryItemById&id=${id}&isHasChild=${isHasChild}`;
    try {
      const data = await AuthService.api
        .get(url)
        .then((response) => response.data)
        .then((res) => ({
          mainItem: ProductService.parseProductItem(res.data.mainItem),
          childItems: ProductService.parseListProductItem(res.data.childItems),
        }));
      return data;
    } catch (err) {
      return null;
    }
  }

  static async querySearchItems({ searchString }: { searchString: string }) {
    const url =
      process.env.VUE_APP_API_BASE_URL +
      `/${process.env.VUE_APP_ENV}/product?action=querySearchItems&searchString=${searchString}`;
    try {
      const data = await AuthService.api
        .get(url)
        .then((response) => ProductService.parseListProductItem(response.data.data));
      return data;
    } catch (err) {
      return [];
    }
  }

  static async queryItemByTarget({
    category,
    limit = 20,
    page = 1,
    agencyItems,
    brandItems,
    maxPrice,
    minPrice,
    discountRate,
    isRep = false,
  }: {
    category: string;
    limit: int;
    page: int;
    agencyItems: string[];
    brandItems: string[];
    maxPrice?: int;
    minPrice?: int;
    discountRate?: int;
    isRep?: boolean;
  }): Promise<ProductItem[]> {
    if (!category) return [];
    const params = {
      category: category,
      limit: limit,
      page: page,
      agencyItems: agencyItems,
      brandItems: brandItems,
      maxPrice: maxPrice,
      minPrice: minPrice,
      discountRate: discountRate,
      isRep: isRep,
    };
    const url = process.env.VUE_APP_API_BASE_URL + `/${process.env.VUE_APP_ENV}/product?action=queryItemByTarget`;
    const data = await AuthService.api
      .post(url, params)
      .then((response) => response.data)
      .then((res) => ProductService.parseListProductItem(res.data));
    return data;
  }

  static async queryPromotionItems({
    limit = 20,
    page = 1,
    discountRate,
  }: {
    limit: int;
    page: int;
    discountRate?: int;
  }): Promise<ProductItem[]> {
    const params = {
      limit: limit,
      page: page,
      discountRate: discountRate,
    };
    const url = process.env.VUE_APP_API_BASE_URL + `/${process.env.VUE_APP_ENV}/product?action=queryPromotionItems`;
    const data = await AuthService.api
      .post(url, params)
      .then((response) => response.data)
      .then((res) => ProductService.parseListProductItem(res.data));
    return data;
  }

  public static nameDomainShop = {
    'tiki.vn': 'Tiki',
    'dienmayxanh.com': 'Điện Máy Xanh',
    'shopee.vn': 'Shopee-Mall',
  } as any;

  static properText(text: string) {
    return text
      .split(' ')
      .map((t: string) => t.charAt(0).toUpperCase() + t.slice(1, t.length).toLowerCase())
      .join('');
  }

  static removeTextInSplash(text: string) {
    if (text.includes('(') && text.includes(')')) {
      const startIndex = text.indexOf('(');
      const endIndex = text.indexOf(')');
      if (endIndex > startIndex) text = text.split(text.slice(startIndex, endIndex + 1)).join('');
    }
    return text;
  }
  static removeTextInSquare(text: string) {
    if (text.includes('[') && text.includes(']')) {
      const startIndex = text.indexOf('[');
      const endIndex = text.indexOf(']');
      if (endIndex > startIndex) text = text.split(text.slice(startIndex, endIndex + 1)).join('');
    }
    return text;
  }
  static handleRemoveSub(text: string) {
    text = this.removeTextInSplash(text);
    text = this.removeTextInSplash(text);
    text = this.removeTextInSquare(text);
    text = this.removeTextInSquare(text);
    return text.trim();
  }

  static parseProductItem(item: any): ProductItem {
    return {
      PK: item.PK,
      SK: item.SK,
      brand: item.brand ? item.brand.toUpperCase() : item.brand,
      id: item.SK.split('#')[item.SK.split('#').length - 1],
      listChildId: item.child ? item.child : [],
      content: item.content,
      createdDate: item.created_date,
      domain: ProductService.nameDomainShop[item.domain],
      listImage: item.image,
      name: item.name,
      cleanName: this.handleRemoveSub(item.name),
      price: item.price > 200000000000 ? parseInt(item.price) / 100000 : parseInt(item.price),
      listPrice: item.list_price > 200000000000 ? parseInt(item.list_price) / 100000 : parseInt(item.list_price),
      discountRate: Math.round(100 - (parseInt(item.price) / parseInt(item.list_price)) * 100),
      isAPI: item.is_api,
      url: item.url,
      shopLocation: item.shop_location,
      slugId: item.slug_id ? item.slug_id : '',
      stock: item.stock ? parseInt(item.stock) : 0,
      subCategory: item.sub_category_code ? item.sub_category_code : '',
      voucherInfo: item.voucher_info ? item.voucher_info : '',
      historicalSold: item.historical_sold ? item.historical_sold : '',
      likedCount: item.liked_count ? item.liked_count : '',
      itemRating: item.item_rating ? item.item_rating : '',
      countReview: item.item_rating
        ? item.item_rating.rating_count.reduce((partialSum: number, a: number) => partialSum + a, 0)
        : 0,
    } as ProductItem;
  }

  static parseListProductItem(data: any[]): ProductItem[] {
    const items = [] as ProductItem[];
    for (const i of data) {
      items.push(ProductService.parseProductItem(i));
    }
    return items;
  }

  static getSlugId(item: ProductItem): string {
    if (item.slugId) {
      const preHandle = item.slugId
        .split('/')
        .filter((i) => !!i)
        .join('/')
        .replace('[', '(')
        .replace(']', ')');
      const encodeURIItem = encodeURI(encodeURI(preHandle));
      return '/' + (encodeURIItem.slice(0, 2) == '%2F' ? encodeURIItem.slice(2, encodeURIItem.length) : encodeURIItem);
    }
    return '';
  }
}

import AuthService from '@/api/auth.service';
import store from '@/store';

export interface ProductItem {
  guarantee?: string;
  images?: string[];
  domain?: string;
  price: string;
  listPrice?: string;
  discountRate?: string;
  category: string;
  ratingAverage?: string;
  SK?: string;
  PK?: string;
  name?: string;
  countBrand: number;
  thumbnailUrl?: string;
  isManyStore?: boolean;
  urlKey?: string;
  brand?: string;
  domainObj?: {};
}
export default class GoodsService {
  static async queryItemByCode(PK: string): Promise<any> {
    const url = process.env.VUE_APP_API_BASE_URL + `/${process.env.VUE_APP_ENV}/goods?action=queryItemByCode&pk=${PK}`;
    const data = await AuthService.api
      .get(url)
      .then((response) => response.data)
      .then((res) => GoodsService.convertProductItemsByCode(res.data));
    return data;
  }
  static async queryItemByCategoryId(category: string): Promise<ProductItem[]> {
    if (!category) return [] as ProductItem[];
    const url =
      process.env.VUE_APP_API_BASE_URL +
      `/${process.env.VUE_APP_ENV}/goods?action=queryItemByCategoryId&category=${category}`;
    const data = await AuthService.api
      .get(url)
      .then((response) => response.data)
      .then((res) => GoodsService.convertProductItemsByCategory(res.data));
    return data;
  }

  static isValidItem(item: any) {
    const allowed_attr_igorne = ['BRAND', 'RATING_AVERAGE', 'IS_MANY_STORE'];
    for (const key in item) {
      if (allowed_attr_igorne.includes(key)) continue;
      if (!item[key]) {
        return false;
      }
    }
    return true;
  }

  static getLowestPriceItem(productItems: any[]): ProductItem[] {
    return productItems
      .map((item) => {
        const domainObj = store.getters.domainItems.find((domainItem: any) => domainItem.id == item['DOMAIN']);
        return {
          guarantee: item['GUARANTEE'],
          images: item['IMAGES'],
          domain: item['DOMAIN'],
          price: item['PRICE'],
          listPrice: item['LIST_PRICE'],
          discountRate: item['DISCOUNT_RATE'],
          category: item['CATEGORY'],
          ratingAverage: item['RATING_AVERAGE'],
          SK: item['SK'],
          PK: item['PK'],
          name: item['NAME'],
          countBrand: item['COUNT_BRAND'] || 0,
          thumbnailUrl: item['THUMBNAIL_URL'],
          isManyStore: item['IS_MANY_STORE'],
          urlKey: item['URL_KEY'],
          brand: item['BRAND'],
          domainObj: domainObj,
        };
      })
      .sort((a: ProductItem, b: ProductItem) => {
        if (b.price == a.price) return 0;
        return b.price > a.price ? -1 : 1;
      });
  }

  static convertProductItemsByCode(items: any[]): ProductItem[] {
    const key = Object.keys(items)[0];
    return key ? GoodsService.getLowestPriceItem((items as any)[key] as ProductItem[]) : [];
  }

  static convertProductItemsByCategory(items: any[]): ProductItem[] {
    const listItem = [] as ProductItem[];
    for (const key in items) {
      for (const item of items[key]) {
        const countBrand = items[key].length;
        if (GoodsService.isValidItem(item)) {
          listItem.push({ ...item, COUNT_BRAND: countBrand } as ProductItem);
          break;
        }
      }
      if (listItem.length >= 48) break;
    }

    return listItem.map((item: any) => {
      const domainObj = store.getters.domainItems.find((domainItem: any) => domainItem.id == item['DOMAIN']);
      const newItem: ProductItem = {
        guarantee: item['GUARANTEE'],
        images: item['IMAGES'],
        domain: item['DOMAIN'],
        price: item['PRICE'],
        listPrice: item['LIST_PRICE'],
        discountRate: item['DISCOUNT_RATE'],
        category: item['CATEGORY'],
        ratingAverage: item['RATING_AVERAGE'],
        SK: item['SK'],
        PK: item['PK'],
        name: item['NAME'],
        countBrand: item['COUNT_BRAND'] || 0,
        thumbnailUrl: item['THUMBNAIL_URL'],
        isManyStore: item['IS_MANY_STORE'],
        urlKey: item['URL_KEY'],
        brand: item['BRAND'],
        domainObj: domainObj,
      };
      return newItem;
    });
  }
}

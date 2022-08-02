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
  baseEncodedURL: string;
  listChildId: string[];
  listImage: string[];
  content: string;
  createdDate: string;
  domain: string;
  nameDomain: string;
  name: string;
  price: number;
  listPrice: number;
  isAPI: boolean;
  productCode: string;
  brand: string;
  url: string;
  discountRate: number;
}

export interface QueryProductItems {
  PK: string;
  SK: string;
  PRODUCTS: any[];
}

export default class ProductService {
  static async queryItemBySlugId({
    ENCODED_SLUG_ID,
    isHasChild = false,
  }: {
    ENCODED_SLUG_ID: string;
    isHasChild?: boolean;
  }) {
    const url =
      process.env.VUE_APP_API_BASE_URL +
      `/${process.env.VUE_APP_ENV}/product?action=queryItemBySlugId&ENCODED_SLUG_ID=${ENCODED_SLUG_ID}&isHasChild=${isHasChild}`;
    const data = await AuthService.api
      .get(url)
      .then((response) => response.data)
      .then((res) => ({
        mainItem: ProductService.parseProductItem(res.data.mainItem),
        childItems: ProductService.parseListProductItem(res.data.childItems),
      }));
    return data;
  }

  static async queryChildItems({
    PK,
    RELATIONSHIP_ID,
  }: {
    PK: string;
    RELATIONSHIP_ID: string;
  }): Promise<ProductItem[]> {
    if (!PK || !RELATIONSHIP_ID) return [];
    RELATIONSHIP_ID = RELATIONSHIP_ID.split('#')[RELATIONSHIP_ID.split('#').length - 1];
    console.log('RELATIONSHIP_ID', RELATIONSHIP_ID);
    const url =
      process.env.VUE_APP_API_BASE_URL +
      `/${process.env.VUE_APP_ENV}/product?action=queryChildItem&PK=${PK}&RELATIONSHIP_ID=${RELATIONSHIP_ID.split(
        '#'
      ).join('_')}`;
    const data = await AuthService.api
      .get(url)
      .then((response) => response.data)
      .then((res) => ProductService.parseListProductItem(res.data))
      .then((items) =>
        items
          .sort((itemA: ProductItem, itemB: ProductItem) => {
            if (itemA.price >= itemB.price) return 1;
            else return -1;
          })
          .filter((item) => item.price)
      );
    return data;
  }

  static async queryItemByCategoryId(category: string, discountRate = 0, limit = 20, page = 1): Promise<ProductItem[]> {
    if (!category) return [];
    const url =
      process.env.VUE_APP_API_BASE_URL +
      `/${process.env.VUE_APP_ENV}/product?action=queryItemByCategoryId&category=${category}&limit=${limit}&page=${page}&discount_rate=${discountRate}`;
    const data = await AuthService.api
      .get(url)
      .then((response) => response.data)
      .then((res) => ProductService.parseListProductItem(res.data));
    return data;
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

  public static nameDomainShop = {
    'tiki.vn': 'Tiki',
    'dienmayxanh.com': 'Điện Máy Xanh',
    'shopee.vn': 'Shopee',
  } as any;

  static properText(text: string) {
    return text
      .split(' ')
      .map((t: string) => t.charAt(0).toUpperCase() + t.slice(1, t.length).toLowerCase())
      .join('');
  }

  static parseProductItem(item: any): ProductItem {
    return {
      PK: item.PK,
      SK: item.SK,
      brand: item.brand.toUpperCase(),
      id: item.SK.split('#')[item.SK.split('#').length - 1],
      relationshipID: item.RELATIONSHIP_ID,
      baseEncodedURL: item.base_encoded_url,
      listChildId: item.child ? item.child : [],
      content: item.content,
      createdDate: item.created_date,
      domain: ProductService.nameDomainShop[item.domain],
      listImage: item.image,
      name: item.name,
      price: item.price > 200000000000 ? parseInt(item.price) / 100000 : parseInt(item.price),
      listPrice: item.list_price > 200000000000 ? parseInt(item.list_price) / 100000 : parseInt(item.list_price),
      discountRate: Math.round(100 - (parseInt(item.price) / parseInt(item.list_price)) * 100),
      isAPI: item.is_api,
      productCode: item.product_code,
      url: item.url,
    } as ProductItem;
  }

  static parseListProductItem(data: any[]): ProductItem[] {
    const items = [] as ProductItem[];
    for (const i of data) {
      items.push(ProductService.parseProductItem(i));
    }
    return items;
  }
}

import AuthService from '@/api/auth.service';
import { int } from 'aws-sdk/clients/datapipeline';
import base64url from 'base64url';

export interface ProductSearchItem {
  PK: string;
  SK: string;
  name: string;
}

export interface ProductItem {
  id: string;
  name: string;
  baseUrl: string;
  encodedBaseUrl: string;
  categoryId: string;
  groupProductId: string;
  price: string;
  listPrice: string;
  updatedAt: string;
  discountRate: number;
  listImage: string[];
  slugId: string;
  representDomainName: string;
  // PK: string;
  // SK: string;
  // id: string;
  // relationshipID: string;
  // listChildId: string[];
  // agency: string;
  // agencyDisplay: string;
  // content: string;
  // createdDate?: string;
  // domain: string;
  // nameDomain: string;
  // name: string;
  // cleanName: string;
  // price: number;
  // listPrice: number;
  // isAPI?: boolean;
  // productCode: string;
  // brand: string;
  // url: string;
  // shopLocation?: string;
  // historicalSold: string;
  // likedCount: string;
  // stock: number;
  // subCategory: string;
  // voucherInfo: {};
  // itemRating: {};
  // countReview: number;
  // shopItem: {};
  // shopUrl: string;
  // description: [];
  // isDisplayHover?: boolean;
}

export interface IInfoGroup {
  id: string;
  name: string;
  description: string;
  listImage: string[];
  meta: {};
}

export default class ProductService {
  static async queryItemById({ groupProductId }: { groupProductId: string }) {
    const url = process.env.VUE_APP_API_BASE_URL + `groups/${groupProductId}?only_detail=True`;
    try {
      const data = await AuthService.api.get(url).then((res) => {
        return {
          infoGroup: ProductService.parseInfoGroupItem(res.data.group),
          items: ProductService.parseListProductItem(res.data.list_product),
        };
      });
      return data;
    } catch (err) {
      return null;
    }
  }

  static async querySearchItemsByUrl({ searchUrl }: { searchUrl: string }): Promise<ProductItem[]> {
    const url = process.env.VUE_APP_API_BASE_URL + `/${process.env.VUE_APP_ENV}/product?action=searchItemsByUrl`;
    const objURL = new URL(searchUrl);
    searchUrl = objURL.origin + objURL.pathname;
    if (searchUrl.includes('shopee.vn')) {
      let searchUrlSplit = '' as any;
      if (searchUrl.includes('shopee.vn/product/')) {
        searchUrlSplit = objURL.pathname.split('/');
      } else {
        searchUrlSplit = objURL.pathname.split('.');
      }
      searchUrl = `${searchUrlSplit[searchUrlSplit.length - 2]}.${searchUrlSplit[searchUrlSplit.length - 1]}`;
    } else {
      searchUrl = base64url.encode(searchUrl);
    }
    const params = {
      baseEncodedUrl: searchUrl,
    };

    try {
      const data = await AuthService.api
        .post(url, params)
        .then((response) => ProductService.parseListProductItem(response.data.products));
      return data;
    } catch (err) {
      return [];
    }
  }

  static async querySearchItems({
    querySearch,
    limit = 20,
    page = 1,
    agencyItems,
    maxPrice,
    minPrice,
    discountRate,
  }: {
    limit?: number;
    page?: number;
    querySearch: string;
    agencyItems?: string;
    maxPrice?: int;
    minPrice?: int;
    discountRate?: int;
  }): Promise<ProductItem[]> {
    const url =
      process.env.VUE_APP_API_BASE_URL +
      `products/search?&q=${querySearch}` +
      `${page ? `&page=${page}` : ''}` +
      `${limit ? `&limit=${limit}` : ''}` +
      `${agencyItems ? `&agency=${agencyItems}` : ''}` +
      `${minPrice ? `&min=${minPrice}` : ''}` +
      `${maxPrice ? `&max=${maxPrice}` : ''}` +
      `${discountRate && discountRate != 0 ? `&discount=${discountRate}` : ''}`;
    try {
      const data = await AuthService.api
        .get(url)
        .then((response) => ProductService.parseListProductItem(response.data.products));
      return data;
    } catch (err) {
      return [];
    }
  }

  static async queryItemByTarget({
    categoryId,
    querySearch,
    limit = 20,
    page = 1,
    agencyItems,
    maxPrice,
    minPrice,
    discountRate,
  }: {
    categoryId: string;
    limit: int;
    page: int;
    querySearch?: string;
    agencyItems?: string;
    maxPrice?: int;
    minPrice?: int;
    discountRate?: int;
  }): Promise<ProductItem[]> {
    if (!categoryId) return [];
    const url =
      process.env.VUE_APP_API_BASE_URL +
      `products/${categoryId}?` +
      `page=${page}` +
      `${limit ? `&limit=${limit}` : ''}` +
      `${querySearch ? `&query=${querySearch}` : ''}` +
      `${agencyItems ? `&agency=${agencyItems}` : ''}` +
      `${minPrice ? `&min=${minPrice}` : ''}` +
      `${maxPrice ? `&max=${maxPrice}` : ''}` +
      `${discountRate && discountRate != 0 ? `&discount=${discountRate}` : ''}`;

    const data = await AuthService.api
      .get(url)
      .then((response: any) => response.data.products)
      .then((data: any) => ProductService.parseListProductItem(data));
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
    tiki: 'Tiki',
    'dienmayxanh.com': 'Điện Máy Xanh',
    shopee: 'Shopee',
    mall: 'Mall',
    lazmall: 'LazMall',
    bachlongmobile: 'Bạch Long Mobile',
    topzone: 'TopZone',
    cellphones: 'Cellphones',
    didongviet: 'DiDongViet',
    shopdunk: 'Shopdunk',
    viettelstore: 'Viettel Store',
    nguyenkim: 'Nguyễn Kim',
    k24hstore: '24h Store',
  } as any;

  static parseListImage(list_image: string) {
    try {
      return JSON.parse(list_image);
    } catch {
      return [];
    }
  }

  static removeAccents(text: string) {
    return text
      ? text
          .normalize('NFD')
          .replace(/[\-|()/]/g, '')
          .replace(/[\u0300-\u036f]/g, '')
          .toLocaleLowerCase()
      : '';
  }

  static getSlugIdFromItem(item: any) {
    let slugId = `${ProductService.removeAccents(item.name).split(' ').join('-')}-${item.id}-${item.group_product}`;
    slugId = slugId.split('--').join('-');
    return slugId;
  }

  static getDomainFromURL(url: string) {
    try {
      const urlObj = new URL(url);
      if (urlObj.hostname.includes('www')) return urlObj.hostname.split('.')[1];
      const domain = urlObj.hostname.split('.')[0];
      return ['24hstore'].includes(domain) ? `k${domain}` : domain;
    } catch {
      // console.log('url', url);
      return '';
    }
  }

  static parseInfoGroupItem(item: any): IInfoGroup {
    return {
      id: item.id,
      name: item.name,
      description: item.description,
      listImage: item.list_image,
      meta: item.meta,
    } as IInfoGroup;
  }

  static parseProductItem(item: any): ProductItem {
    const domain = ProductService.getDomainFromURL(item.base_url);

    return {
      id: item.id, // '3hekq4s138bb',
      name: item.title, // 'iPhone 11 128GB Chính hãng - Đã kích hoạt bảo hành VN/A',
      // title: item.title, // 'iPhone 11 128GB đã kích hoạt - Giá rẻ nhất,đổi trả 30 ngày,bảo hành 12 tháng',
      baseUrl: item.base_url, // 'https://cellphones.com.vn/iphone-11-128gb-da-kich-hoat.html',
      encodedBaseUrl: item.encoded_base_url, // 'aHR0cHM6Ly9jZWxscGhvbmVzLmNvbS52bi9pcGhvbmUtMTEtMTI4Z2ItZGEta2ljaC1ob2F0Lmh0bWw',
      categoryId: item.category, // '3111010055',
      groupProductId: item.group_product, // 'si0abb2e7gbo',
      price: item.price, // '11190000.0',
      listPrice: item.list_price, // '16990000.0',
      updatedAt: item.updated_at, // '2023-01-08T15:04:37.862989Z',
      discountRate: item.discount_rate,
      listImage: ProductService.parseListImage(item.list_image),
      domain: domain,
      slugId: ProductService.getSlugIdFromItem(item),
      representDomainName: Object.keys(ProductService.nameDomainShop).includes(domain)
        ? ProductService.nameDomainShop[domain]
        : domain,
    } as ProductItem;
  }

  static handleDescription(description: string[]): string {
    const newDescription = [];
    if (description && description.length == 1) {
      if (description[0].includes('\n')) return description[0].split('\n').join('<br />');
      else return description[0];
    } else {
      for (const text of description) {
        if (text.includes('\n')) newDescription.push(text.split('\n').join('<br />'));
        else newDescription.push(text);
      }
      return newDescription.join('<br />');
    }
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
        .filter((i: string) => !!i)
        .join('/')
        .replace('[', '(')
        .replace(']', ')');
      const encodeURIItem = encodeURI(encodeURI(preHandle));
      return '/' + (encodeURIItem.slice(0, 2) == '%2F' ? encodeURIItem.slice(2, encodeURIItem.length) : encodeURIItem);
    }
    return '';
  }
}

import { MetaInfo } from 'vue-meta';

export default class SeoService {
  static getSeoInfoCommon(
    field:
      | 'title'
      | 'description'
      | 'keywords'
      | 'robots'
      | 'viewport'
      | 'og:type'
      | 'og:site_name'
      | 'og:url'
      | 'og:image'
      | 'og:image:width'
      | 'og:image:height'
  ): string {
    const BASE_URL = window.location.origin;
    const urlObj = new URL(BASE_URL);
    const seoInfo = {
      title: 'PCW - Trang web so sánh giá hàng đầu',
      description:
        'Tìm ra giá phù hợp cho tất cả sản phẩm mà bạn tìm kiếm - Hỗ trợ so sánh trên nhiều nền tảng bán hàng online',
      keywords: 'pcw, x-pcw, store, price compare, so sánh',
      robots: 'index, follow',
      viewport: 'width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=no',
      'og:type': 'website',
      'og:site_name': BASE_URL ? urlObj.host : 'x-pcw.store',
      'og:url': BASE_URL,
      'og:image': `${BASE_URL}/logo.png`,
      'og:image:width': '500',
      'og:image:height': '350',
    };

    return seoInfo[field];
  }

  static getMetaInfoHomePage(): MetaInfo {
    return {
      title: SeoService.getSeoInfoCommon('title'),
      htmlAttrs: {
        lang: 'vi',
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'keyword', content: SeoService.getSeoInfoCommon('keywords') },
        { name: 'description', content: SeoService.getSeoInfoCommon('description') },
        { name: 'robots', content: SeoService.getSeoInfoCommon('robots') },
        { name: 'viewport', content: SeoService.getSeoInfoCommon('viewport') },
        { name: 'og:type', content: SeoService.getSeoInfoCommon('og:type') },
        { name: 'og:site_name', content: SeoService.getSeoInfoCommon('og:site_name') },
        { name: 'og:url', content: SeoService.getSeoInfoCommon('og:url') },
        { name: 'og:image', content: SeoService.getSeoInfoCommon('og:image') },
        { name: 'og:image:width', content: SeoService.getSeoInfoCommon('og:image:width') },
        { name: 'og:image:height', content: SeoService.getSeoInfoCommon('og:image:height') },
      ],
    };
  }

  static getMetaInfoCategoryPage(categoryName: string): MetaInfo {
    return {
      title: `PCW ー ${categoryName}`,
      htmlAttrs: {
        lang: 'vi',
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'keyword', content: SeoService.getSeoInfoCommon('keywords') },
        { name: 'description', content: SeoService.getSeoInfoCommon('description') },
        { name: 'viewport', content: SeoService.getSeoInfoCommon('viewport') },
        { name: 'og:type', content: SeoService.getSeoInfoCommon('og:type') },
        { name: 'og:site_name', content: SeoService.getSeoInfoCommon('og:site_name') },
        { name: 'og:url', content: SeoService.getSeoInfoCommon('og:url') },
        { name: 'og:image', content: SeoService.getSeoInfoCommon('og:image') },
        { name: 'og:image:width', content: SeoService.getSeoInfoCommon('og:image:width') },
        { name: 'og:image:height', content: SeoService.getSeoInfoCommon('og:image:height') },
      ],
    };
  }

  static getMetaInfoProductPage(productName: string, imageURL: string): MetaInfo {
    const imageStrSplit = imageURL.split('.');
    const typeImage = imageStrSplit[imageStrSplit.length - 1];
    return {
      title: `PCW ー ${productName}`,
      htmlAttrs: {
        lang: 'vi',
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'keyword', content: SeoService.getSeoInfoCommon('keywords') },
        { name: 'description', content: `So sánh giá của ${productName}` },
        { name: 'viewport', content: SeoService.getSeoInfoCommon('viewport') },
        { name: 'og:type', content: SeoService.getSeoInfoCommon('og:type') },
        { name: 'og:site_name', content: SeoService.getSeoInfoCommon('og:site_name') },
        { name: 'og:url', content: SeoService.getSeoInfoCommon('og:url') },
        { name: 'og:image', content: imageURL },
        { name: 'og:image:url', content: imageURL },
        { name: 'og:image:type', content: `image/${typeImage == 'jpg' ? 'jpeg' : typeImage}` },
        { name: 'og:image:width', content: SeoService.getSeoInfoCommon('og:image:width') },
        { name: 'og:image:height', content: SeoService.getSeoInfoCommon('og:image:height') },
      ],
    };
  }
}

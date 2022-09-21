import { MetaInfo } from 'vue-meta';

export default class SeoService {
  static getSeoInfoCommon(
    field:
      | 'title'
      | 'description'
      | 'keywords'
      // | 'robots'
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
      keywords: 'pcw, so sánh giá, x-pcw, store, price compare, so sánh',
      robots: 'index, follow',
      viewport: 'width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=no',
      'og:type': 'website',
      'og:site_name': BASE_URL ? urlObj.host : 'x-pcw.store',
      'og:url': BASE_URL,
      'og:image': `${BASE_URL}/logo.png`,
      'og:image:width': '600',
      'og:image:height': '200',
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
        { vmid: 'keyword', property: 'keyword', name: 'keyword', content: SeoService.getSeoInfoCommon('keywords') },
        {
          vmid: 'description',
          property: 'description',
          name: 'description',
          content: SeoService.getSeoInfoCommon('description'),
        },
        // { vmid: 'robots', property: 'robots', name: 'robots', content: SeoService.getSeoInfoCommon('robots') },
        { vmid: 'viewport', property: 'viewport', name: 'viewport', content: SeoService.getSeoInfoCommon('viewport') },
        { vmid: 'og:type', property: 'og:type', name: 'og:type', content: SeoService.getSeoInfoCommon('og:type') },
        {
          vmid: 'og:site_name',
          property: 'og:site_name',
          name: 'og:site_name',
          content: SeoService.getSeoInfoCommon('og:site_name'),
        },
        { vmid: 'og:url', property: 'og:url', name: 'og:url', content: SeoService.getSeoInfoCommon('og:url') },
        { vmid: 'og:image', property: 'og:image', name: 'og:image', content: SeoService.getSeoInfoCommon('og:image') },
        {
          vmid: 'og:image:width',
          property: 'og:image:width',
          name: 'og:image:width',
          content: SeoService.getSeoInfoCommon('og:image:width'),
        },
        {
          vmid: 'og:image:height',
          property: 'og:image:height',
          name: 'og:image:height',
          content: SeoService.getSeoInfoCommon('og:image:height'),
        },
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
        { vmid: 'keyword', property: 'keyword', name: 'keyword', content: SeoService.getSeoInfoCommon('keywords') },
        {
          vmid: 'description',
          property: 'description',
          name: 'description',
          content: `Hàng ngàn mẫu mã ${categoryName} khác nhau`,
        },
        { vmid: 'viewport', property: 'viewport', name: 'viewport', content: SeoService.getSeoInfoCommon('viewport') },
        { vmid: 'og:type', property: 'og:type', name: 'og:type', content: SeoService.getSeoInfoCommon('og:type') },
        {
          vmid: 'og:site_name',
          property: 'og:site_name',
          name: 'og:site_name',
          content: SeoService.getSeoInfoCommon('og:site_name'),
        },
        { vmid: 'og:url', property: 'og:url', name: 'og:url', content: SeoService.getSeoInfoCommon('og:url') },
        { vmid: 'og:image', property: 'og:image', name: 'og:image', content: SeoService.getSeoInfoCommon('og:image') },
        {
          vmid: 'og:image:width',
          property: 'og:image:width',
          name: 'og:image:width',
          content: SeoService.getSeoInfoCommon('og:image:width'),
        },
        {
          vmid: 'og:image:height',
          property: 'og:image:height',
          name: 'og:image:height',
          content: SeoService.getSeoInfoCommon('og:image:height'),
        },
      ],
    };
  }

  static getMetaInfoProductPage(productName: string, imageURL: string, price: string): MetaInfo {
    const imageStrSplit = imageURL.split('.');
    const typeImage = imageStrSplit[imageStrSplit.length - 1];
    return {
      title: `PCW ー ${productName}`,
      htmlAttrs: {
        lang: 'vi',
      },
      meta: [
        { charset: 'utf-8' },
        {
          vmid: 'keyword',
          property: 'keyword',
          name: 'keyword',
          content: SeoService.getSeoInfoCommon('keywords') + ',' + productName.split(' ').join(', '),
        },
        { vmid: 'description', property: 'description', name: 'description', content: `${price} - ${productName}` },
        { vmid: 'viewport', property: 'viewport', name: 'viewport', content: SeoService.getSeoInfoCommon('viewport') },
        { vmid: 'og:type', property: 'og:type', name: 'og:type', content: SeoService.getSeoInfoCommon('og:type') },
        {
          vmid: 'og:site_name',
          property: 'og:site_name',
          name: 'og:site_name',
          content: SeoService.getSeoInfoCommon('og:site_name'),
        },
        { vmid: 'og:url', property: 'og:url', name: 'og:url', content: SeoService.getSeoInfoCommon('og:url') },
        { vmid: 'og:image', property: 'og:image', name: 'og:image', content: imageURL },
        { vmid: 'og:image:url', property: 'og:image:url', name: 'og:image:url', content: imageURL },
        {
          vmid: 'og:image:type',
          property: 'og:image:type',
          name: 'og:image:type',
          content: `image/${typeImage == 'jpg' ? 'jpeg' : typeImage}`,
        },
        {
          vmid: 'og:image:width',
          property: 'og:image:width',
          name: 'og:image:width',
          content: '500',
        },
        {
          vmid: 'og:image:height',
          property: 'og:image:height',
          name: 'og:image:height',
          content: '500',
        },
      ],
    };
  }
}

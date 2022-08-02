import AuthService from '@/api/auth.service';
import i18n from '@/i18n';
export interface CategoryItem {
  PK: string;
  SK: string;
  name: string;
  translateName: string;
}

export interface BrandItem {
  PK: string;
  SK: string;
  name: string;
  translateName: string;
  selected: boolean;
}

export default class CategoryService {
  static async queryAllCategory(): Promise<CategoryItem[]> {
    const url = process.env.VUE_APP_API_BASE_URL + `/${process.env.VUE_APP_ENV}/product?action=queryAllCategory`;
    const data = await AuthService.api
      .get(url)
      .then((response) => response.data)
      .then((res) => CategoryService.parseListCategoryItem(res.data));
    return data;
  }

  static async queryBrandItems(categoryId: string): Promise<BrandItem[]> {
    const url =
      process.env.VUE_APP_API_BASE_URL +
      `/${process.env.VUE_APP_ENV}/product?action=queryBrandItems&categoryId=${categoryId}`;
    const data = await AuthService.api
      .get(url)
      .then((response) => response.data)
      .then((res) => CategoryService.parseListBrandItems(res.data));
    return data;
  }

  static upperCaseFirstLetter(text: string) {
    if (!text) return text;
    const texts = text.split(' ') as string[];
    return texts.map((i: string) => i.charAt(0).toUpperCase() + i.slice(1, i.length).toLocaleLowerCase()).join(' ');
  }

  static parseCategoryItem(item: any): CategoryItem {
    return {
      PK: item.PK,
      SK: item.SK,
      name: CategoryService.upperCaseFirstLetter(item.SK),
      translateName: CategoryService.upperCaseFirstLetter(item.SK),
    } as CategoryItem;
  }

  static parseListCategoryItem(data: any[]): CategoryItem[] {
    const items = [] as CategoryItem[];
    for (const i of data) {
      items.push(CategoryService.parseCategoryItem(i));
    }
    return items;
  }

  static parseBrandItems(item: any): BrandItem {
    return {
      PK: item.PK,
      SK: item.SK,
      name: CategoryService.upperCaseFirstLetter(item.SK.split('#')[1]),
      translateName: CategoryService.upperCaseFirstLetter(item.SK.split('#')[1]),
      selected: false,
    } as BrandItem;
  }

  static parseListBrandItems(data: any[]): BrandItem[] {
    const items = [] as BrandItem[];
    for (const i of data) {
      items.push(CategoryService.parseBrandItems(i));
    }
    return items;
  }

  static code2category(code: string) {
    const categoryDict = {
      AIRCONDITION: 'Air Condition',
      FRIDGE: 'Fridge',
      LAPTOP: 'Laptop',
      PHONE: 'Phone',
      TELEVISION: 'Television',
      WASHING: 'Washing',
    } as any;
    if (!code) return '';
    return categoryDict[code.toUpperCase()];
  }

  static category2code(category: string) {
    const categoryDict = {
      'Air Condition': 'AIRCONDITION',
      Fridge: 'FRIDGE',
      Laptop: 'LAPTOP',
      Phone: 'PHONE',
      Television: 'TELEVISION',
      Washing: 'WASHING',
    } as any;
    return categoryDict[category];
  }
}

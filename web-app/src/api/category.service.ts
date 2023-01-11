import AuthService from '@/api/auth.service';
import store from '@/store';
import axios from 'axios';
export interface CategoryItem {
  id: string;
  name: string;
  href?: string;
  image?: string;
}
export default class CategoryService {
  static async queryAllCategory(): Promise<CategoryItem[]> {
    const url = process.env.VUE_APP_API_BASE_URL + `categories`;
    console.log(url);
    const data = await axios
      .get(url)
      .then((response) => response.data.categories)
      .then((data) => CategoryService.parseListCategoryItem(data));
    return data;
  }

  static async queryCategory(id: string): Promise<CategoryItem> {
    const url = process.env.VUE_APP_API_BASE_URL + `categories/${id}`;
    console.log(url);
    const data = await axios
      .get(url)
      .then((response) => response.data.categories)
      .then((data) => CategoryService.parseCategoryItem(data));
    return data;
  }

  static upperCaseFirstLetter(text: string) {
    if (!text) return text;
    const texts = text.split(' ') as string[];
    return texts.map((i: string) => i.charAt(0).toUpperCase() + i.slice(1, i.length).toLocaleLowerCase()).join(' ');
  }

  static parseCategoryItem(item: any): CategoryItem {
    return {
      id: item.id,
      name: item.name,
    } as CategoryItem;
  }

  static parseListCategoryItem(data: any[]): CategoryItem[] {
    const items = [] as CategoryItem[];
    for (const i of data) {
      items.push(CategoryService.parseCategoryItem(i));
    }
    return items;
  }

  static code2category(code: string) {
    if (!code) return '';
    if (code == 'undefined' || code == undefined) return '';
    const category = store.getters.categoryItems.find((i: CategoryItem) => i.id == code);
    if (category) return category.translateName;
    else return '';
    const categoryDict = {
      // AIRCONDITION: 'Air Condition',
      // MOTOR: 'Motor',
      // TABLET: 'Tablet',
      // FRIDGE: 'Fridge',
      // LAPTOP: 'Laptop',
      PHONE: 'Phone',
      // TELEVISION: 'Television',
      // WASHING: 'Washing',
    } as any;
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
      Shoes_man: 'Giày nam',
    } as any;
    return categoryDict[category];
  }
}

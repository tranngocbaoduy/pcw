import store from '@/store';
import axios from 'axios';
export interface CategoryItem {
  id: string;
  name: string;
  href?: string;
  image?: string;
  isLeaf?: boolean;
  parents?: CategoryItem[];
}
export default class CategoryService {
  static agencyItems = [
    { name: 'Điện máy xanh', code: 'www.dienmayxanh.com' },
    { name: 'TopZone', code: 'www.topzone.vn' },
    { name: 'DiĐộngViệt', code: 'didongviet.vn' },
    { name: 'ShopDunk', code: 'shopdunk.com' },
    { name: 'BạchLongMobile', code: 'bachlongmobile.com' },
    { name: 'Cellphones', code: 'cellphones.com.vn' },
    { name: '24h store', code: '24hstore.vn' },
    { name: 'ViettelStore', code: 'viettelstore.vn' },
    { name: 'Nguyễn Kim', code: 'www.nguyenkim.com' },
  ];

  static agencyItemsByCategory(selectedCategory: CategoryItem) {
    if (selectedCategory && selectedCategory.name == 'iPhone') {
      return CategoryService.agencyItems.filter((i) =>
        [
          'www.dienmayxanh.com',
          'www.topzone.vn',
          'didongviet.vn',
          'shopdunk.com',
          'bachlongmobile.com',
          'cellphones.com.vn',
          '24hstore.vn',
          'viettelstore.vn',
          'www.nguyenkim.com',
        ].includes(i.code)
      );
    } else if (selectedCategory && selectedCategory.name == 'Macbook') {
      return CategoryService.agencyItems.filter((i) =>
        ['www.topzone.vn', 'cellphones.com.vn', 'www.nguyenkim.com'].includes(i.code)
      );
    } else if (selectedCategory && selectedCategory.name == 'Apple Watch') {
      return CategoryService.agencyItems.filter((i) => ['www.topzone.vn'].includes(i.code));
    }
    return CategoryService.agencyItems;
  }

  static async queryAllCategory(): Promise<CategoryItem[]> {
    const url = process.env.VUE_APP_API_BASE_URL + `categories`;
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
      parents: item.parent_categories ? CategoryService.parseListCategoryItem(item.parent_categories) : [],
      isLeaf: item.is_leaf,
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

const dynamodbHelper = require("../helper/DynamodbHelper");

module.exports = async (event) => {
  const queryParams = event.queryStringParameters;
  let data = null;
  let res = null;
  console.log('Get metadata queryParams["action"]', queryParams["action"])
  if (!queryParams) {
    throw new Error("There's no query parameter");
  } else {
    switch (queryParams["action"]) {
      case "default":
        data = await getMetaDataDefault(event);
        break;
      case "category":
        data = await getMetaDataCategory(event);
        break;
      case "product":
        data = await getMetaDataProduct(event);
        break;
      default:
        data = [];
        break;
    }
    res = {
      message: "Successful",
      action: queryParams["action"],
      data: data,
    };

  }
  return res;
};

function titleCase(str) {
  var splitStr = str.toLowerCase().split(' ');
  for (var i = 0; i < splitStr.length; i++) {
    // You do not need to check if i is larger than splitStr length, as your for does that for you
    // Assign it back to the array
    splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);
  }
  // Directly return the joined string
  return splitStr.join(' ');
}

function formatPrice(value) {
  return value ? value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') + 'đ' : '';
}

async function getMetaDataProduct(event) {
  const idCategory = event.queryStringParameters["idCate"] || "";
  const idProduct = event.queryStringParameters["id"] || "";
  if (idProduct != '' && idCategory != '') {
    const params = {
      TableName: process.env.PRODUCT_TABLE_NAME,
      Key: {
        PK: idCategory,
        SK: idProduct,
      },
    };
    const result = await dynamodbHelper.getItem(params);
    if (result) {
      const BASE_HOST = 'x-pcw.store'
      const BASE_URL = 'https://x-pcw.store'
      const upperName = titleCase(result.clean_name)
      return {
        title: `PCW - ${upperName}`,
        description: `${formatPrice(result.price)} - ${upperName}`,
        keywords: 'pcw, x-pcw, price compare, store, ' + upperName.split(' ').join(', '),
        robots: 'index, follow',
        viewport: 'width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=no',
        'og:type': 'website',
        'og:site_name': BASE_HOST,
        'og:url': BASE_URL,
        'og:image': `${result.image && result.image.length != 0 ? result.image[0] : `${BASE_URL}/logo.png`}`,
        'og:image:width': '600',
        'og:image:height': '250',
      };
    }
  }
  return null;
}

async function getMetaDataCategory(event) {
  const idCategory = event.queryStringParameters["id"] || "";
  if (idCategory != '') {
    const params = {
      TableName: process.env.CATEGORY_TABLE_NAME,
      Key: {
        PK: 'CATEGORY',
        SK: idCategory,
      },
    };
    const result = await dynamodbHelper.getItem(params);
    if (result) {
      const BASE_HOST = 'x-pcw.store'
      const BASE_URL = 'https://x-pcw.store'
      return {
        title: `PCW - ${result.ViNAME}`,
        description: `Hàng ngàn mẫu mã ${result.ViNAME} khác nhau`,
        keywords: 'pcw, x-pcw, store, price compare, so sánh',
        robots: 'index, follow',
        viewport: 'width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=no',
        'og:type': 'website',
        'og:site_name': BASE_HOST,
        'og:url': BASE_URL,
        'og:image': `${BASE_URL}/logo.png`,
        'og:image:width': '600',
        'og:image:height': '250',
      };
    }
  }
  return null;
}

function getMetaDataDefault() {
  const BASE_HOST = 'x-pcw.store'
  const BASE_URL = 'https://x-pcw.store'
  return {
    title: 'PCW - Trang web so sánh giá hàng đầu',
    description:
      'Tìm ra giá phù hợp cho tất cả sản phẩm mà bạn tìm kiếm - Hỗ trợ so sánh trên nhiều nền tảng bán hàng online',
    keywords: 'pcw, x-pcw, store, price compare, so sánh',
    robots: 'index, follow',
    viewport: 'width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=no',
    'og:type': 'website',
    'og:site_name': BASE_HOST,
    'og:url': BASE_URL,
    'og:image': `${BASE_URL}/logo.png`,
    'og:image:width': '600',
    'og:image:height': '250',
  };
}

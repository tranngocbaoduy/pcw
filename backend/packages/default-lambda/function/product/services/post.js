const dynamodbHelper = require("../helper/DynamodbHelper");
const config = require("../helper/id_config");

function checkIsValidDomain(event) {
  const listDomainValid = ["https://x-pcw.store", "http://localhost:8080", "https://d3kxmkwimuhvhe.cloudfront.net"];
  if (listDomainValid.includes(event.headers.origin)) return true
  return false;
}

module.exports = async (event, context) => {

  const queryParams = event.queryStringParameters;
  console.log('[ACTION] =>', queryParams["action"])

  let result = null;
  let res = null;
  if (!queryParams) {
    throw new Error("There's no query parameter");
  } else {
    if (checkIsValidDomain(event)) {
      switch (queryParams["action"]) {
        case "queryItemByTarget":
          result = await queryItemByTarget(event);
          break;
        case "queryPromotionItems":
          result = await queryPromotionItems(event);
          break;
        case "searchItemsByUrl":
          result = await searchItemsByUrl(event);
          break;
        default:
          result = [];
          break;
      }
      res = {
        message: "Successful",
        action: queryParams["action"],
        data: await result,
      };
    } else {
      res = {
        message: "Failed",
        action: queryParams["action"],
        data: result,
      };
    }
  }
  return res;
};

function parseParams(body) {
  params = {};
  // {
  //   "category": "TELEVISION",
  //   "limit": 32,
  //   "agencyItems": ["tiki", "dienmayxanh", "shopee"],
  //   "brandItems": [
  //     "Aqua",
  //     "Asanzo",
  //     "Casper",
  //     "Darling",
  //     "Ffalcon",
  //     "Lg",
  //     "Samsung",
  //     "Sony",
  //     "Tcl"
  //   ],
  //   "maxPrice": 0,
  //   "minPrice": 10000
  // }
}
async function searchItemsByUrl(event) {
  const body = JSON.parse(event.body);
  const baseEncodedUrl = body["baseEncodedUrl"];
  if (Object.keys(config.IdConfig).includes(baseEncodedUrl)) {
    const id = config.IdConfig[baseEncodedUrl]
    const params = {
      TableName: process.env.PRODUCT_TABLE_NAME,
      IndexName: "SEARCH-INDEX",
      KeyConditionExpression: "#PRODUCT_KEY = :productKey and begins_with(#SK, :sk)",
      ExpressionAttributeNames: {
        "#PRODUCT_KEY": "PRODUCT_KEY",
        "#URL": "url",
        "#BRAND": "brand",
        "#DOMAIN": "domain",
        "#NAME": "name",
        "#IMAGE": "image",
        "#SK": "SK",
      },
      ExpressionAttributeValues: {
        ":productKey": "PRODUCT",
        ":sk": id
      },
      ProjectionExpression: 'PK, SK, #URL, price, voucher_info, slug_id, #BRAND, #DOMAIN, #NAME, #IMAGE, list_price, discount_rate, agency, description',
    };
    console.log('params', params)
    const data = await dynamodbHelper.queryItems(params);
    return data;
  } else {
    return []
  }
}

async function queryItemByTarget(event) {
  console.log("event", event);
  const body = JSON.parse(event.body);
  const PK = body["category"];
  const SK = body["SK"];
  const limit = body["limit"] ? parseInt(body["limit"]) : 16;
  const page = body["page"] ? parseInt(body["page"]) : 1;
  const agencyItems = body["agencyItems"].map((i) => i.toLowerCase());
  const brandItems = body["brandItems"].map((i) => i.toLowerCase());
  const minPrice = body["minPrice"] ? parseInt(body["minPrice"]) : 0;
  const maxPrice = body["maxPrice"] ? parseInt(body["maxPrice"]) : 10000000000;
  const discountRate = body["discountRate"] ? parseInt(body["discountRate"]) : 0;
  const isRep = body["isRep"] ? body["isRep"] : false;


  agencyValues = {};
  agencyFilterExpressionValues = [];
  agencyFilterExpressionNames = {};
  for (const agencyIndex in agencyItems) {
    agencyFilterExpressionValues.push(`begins_with(#AGENCY, :agency${agencyIndex})`);
    agencyValues[`:agency${agencyIndex}`] = agencyItems[agencyIndex];
    agencyFilterExpressionNames['#AGENCY'] = 'agency'
  }

  brandValues = {};
  brandFilterExpressionValues = [];
  brandFilterExpressionNames = {};
  for (const brandIndex in brandItems) {
    brandFilterExpressionValues.push(`begins_with(#BRAND, :brand${brandIndex})`);
    brandValues[`:brand${brandIndex}`] = brandItems[brandIndex]
    brandFilterExpressionNames['#BRAND'] = 'brand'
  };


  if (!PK) return [];
  const params = {
    TableName: process.env.PRODUCT_TABLE_NAME,
    KeyConditionExpression: isRep ? "#PK = :pk and begins_with(RBGI, :rbgi)" : "#PK = :pk",
    IndexName: 'RELATIONSHIP-BRAND-GROUP-INDEX',
    FilterExpression: `${brandFilterExpressionValues.length != 0
      ? `(${brandFilterExpressionValues.join(" OR ")}) AND`
      : ``
      } ${agencyFilterExpressionValues.length != 0
        ? `(${agencyFilterExpressionValues.join(" OR ")}) AND`
        : ``
      } (price BETWEEN :minPrice AND :maxPrice) and (discount_rate >= :discountRate)`,
    ExpressionAttributeNames: {
      "#PK": "PK",
      "#URL": "url",
      "#NAME": "name",
      "#AGENCY": "agency",
      "#DOMAIN": "domain",
      "#BRAND": "brand",
      "#IMAGE": "image",
      "#STOCK": "stock",
      ...agencyFilterExpressionNames,
      ...brandFilterExpressionNames
    },
    ProjectionExpression: 'PK, SK, #URL, price, voucher_info, slug_id, liked_count, #BRAND, #AGENCY,#DOMAIN, #NAME, shop_location, #IMAGE, list_price, item_rating, #STOCK, historical_sold, discount_rate, child, shop_item, description',
    ExpressionAttributeValues: {
      ":pk": PK,
      ":minPrice": minPrice,
      ":maxPrice": maxPrice,
      ":discountRate": discountRate,
      ...isRep ? { ":rbgi": "REP#" } : {},
      ...agencyValues,
      ...brandValues,
    },

  };
  console.log('params', params)
  const data = await dynamodbHelper.queryItems(params);
  console.log('data', data.length)
  return data.slice((page - 1) * limit, page * limit)
}


async function queryPromotionItems(event) {
  console.log("event", event);
  const body = JSON.parse(event.body);
  const limit = body["limit"] ? parseInt(body["limit"]) : 16;
  const page = body["page"] ? parseInt(body["page"]) : 1;
  const discountRate = body["discountRate"] ? parseInt(body["discountRate"]) : 0;

  const params = {
    TableName: process.env.PRODUCT_TABLE_NAME,
    IndexName: "SEARCH-INDEX",
    KeyConditionExpression: "#PRODUCT_KEY = :productKey",
    FilterExpression: `discount_rate >= :discountRate`,
    ExpressionAttributeNames: {
      "#PRODUCT_KEY": "PRODUCT_KEY",
      "#URL": "url",
      "#NAME": "name",
      "#AGENCY": "agency",
      "#DOMAIN": "domain",
      "#BRAND": "brand",
      "#IMAGE": "image",
      "#STOCK": "stock",
    },
    ProjectionExpression: 'PK, SK, #URL, price, voucher_info, slug_id, liked_count, #BRAND, #AGENCY, #DOMAIN, #NAME, shop_location, #IMAGE, list_price, #STOCK, discount_rate, child, shop_item, description',
    ExpressionAttributeValues: {
      ":productKey": 'PRODUCT',
      ":discountRate": discountRate,
    },

  };
  console.log('params', params)
  const data = await dynamodbHelper.queryAllItemsByLimit(params, limit);
  console.log('data', data.length)
  return data.slice((page - 1) * limit, page * limit)
}

const dynamodbHelper = require("../helper/DynamodbHelper");

function checkIsValidDomain(event) {
  const listDomainValid = ['https://x-pcw.com', 'http://localhost:8080']
  if (listDomainValid.includes(event.headers.origin)) return true
  return false;
}

module.exports = async (event, context) => {
  const queryParams = event.queryStringParameters;

  let result = null;
  let res = null;

  if (!queryParams) {
    throw new Error("There's no query parameter");
  } else {
    if (checkIsValidDomain(event)) {
      switch (queryParams["action"]) {
        case "queryChildItem":
          result = await queryChildItem(event);
          break;
        case "queryAllCategory":
          result = await queryAllCategory();
          break;
        case "queryBrandItems":
          result = await queryBrandItems(event);
          break;
        case "queryItemByCategoryId":
          result = await queryItemByCategoryId(event);
          break;
        default:
          result = [];
          break;
      }
      res = {
        message: "Successful",
        action: queryParams["action"],
        data: result,
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

async function getItemByCode(event) {
  const pk = event.queryStringParameters["pk"] || "";
  const sk = event.queryStringParameters["sk"] || "";

  const params = {
    TableName: process.env.PRODUCT_TABLE_NAME,
    Key: {
      PK: pk,
      SK: sk,
    },
  };

  result = await dynamodbHelper.getItem(params);
  return result.Item;
}

async function queryAllCategory() {
  const params = {
    TableName: process.env.CATEGORY_TABLE_NAME,
    KeyConditionExpression: "PK = :pk",
    ExpressionAttributeValues: {
      ":pk": "CATEGORY",
    },
  };
  return await dynamodbHelper.queryAllItems(params);
}

async function queryBrandItems(event) {
  const SK = event.queryStringParameters["categoryId"] || null;
  const params = {
    TableName: process.env.CATEGORY_TABLE_NAME,
    KeyConditionExpression: "PK = :pk and begins_with(SK, :sk)",
    ExpressionAttributeValues: {
      ":pk": "BRAND",
      ":sk": SK
    },
  };
  return await dynamodbHelper.queryAllItems(params);
}


async function queryChildItem(event) {
  const PK = event.queryStringParameters["PK"] || null;
  let RELATIONSHIP_ID = event.queryStringParameters["RELATIONSHIP_ID"] || null;
  if (!PK || !RELATIONSHIP_ID) return [];
  RELATIONSHIP_ID = RELATIONSHIP_ID.split('_').join('#')
  const params = {
    TableName: process.env.PRODUCT_TABLE_NAME,
    IndexName: 'RELATIONSHIP-INDEX',
    KeyConditionExpression: "#PK = :pk AND #RELATIONSHIP_ID = :relationshipId",
    ExpressionAttributeNames: {
      '#PK': 'PK',
      '#RELATIONSHIP_ID': 'RELATIONSHIP_ID',
    },
    ExpressionAttributeValues: {
      ":pk": PK,
      ":relationshipId": RELATIONSHIP_ID
    },
  };

  return await dynamodbHelper.queryItems(params)
}

async function queryItemByCategoryId(event) {
  const category = event.queryStringParameters["category"] || "";
  const limit = event.queryStringParameters["limit"] || 8;
  const page = event.queryStringParameters["page"] || 8;
  const PK = event.queryStringParameters["PK"] || null;
  const SK = event.queryStringParameters["SK"] || null;
  const discount_rate = event.queryStringParameters["discount_rate"] || 0;
  if (!category) return [];
  const params = {
    TableName: process.env.PRODUCT_TABLE_NAME,
    KeyConditionExpression: "PK = :pk AND begins_with(SK, :sk)",
    FilterExpression: "discount_rate >= :discount_rate",
    ExpressionAttributeValues: {
      ":pk": category,
      ":sk": 'REP',
      ":discount_rate": parseInt(discount_rate),
    },
    Limit: limit,
  };
  console.log('params', params)

  return await dynamodbHelper.queryAllItemsByLimit(params, parseInt(limit) * parseInt(page));
}

async function listAllItem() {
  const params = {
    TableName: process.env.PRODUCT_TABLE_NAME,
  };

  return await dynamodbHelper.scanAllItems(params);
}

function filterAllowedAttributesGoods(result) {
  const allowedAttributes = [
    "PK",
    "SK",
    "NAME",
    "CATEGORY",
    "GUARANTEE",
    "IMAGES",
    "DOMAIN",
    "PRICE",
    "LIST_PRICE",
    "DISCOUNT_RATE",
    "RATING_AVERAGE",
    "THUMBNAIL_URL",
    "IS_MANY_STORE",
    "URL_KEY",
    "BRAND",
  ];

  const resItems = result.map((item) => {
    let newItem = {};
    for (const key of Object.keys(item)) {
      if (allowedAttributes.includes(key)) {
        newItem[key] = item[key] || "";
      }
    }
    return newItem;
  });
  let listItems = {};
  let item = null;
  for (item of resItems) {
    listItems[item["PK"]] =
      !listItems[item["PK"]] || listItems[item["PK"]].length == 0
        ? [item]
        : [...listItems[item["PK"]], item];
  }
  return listItems;
}

const dynamodbHelper = require("../helper/DynamodbHelper");

function checkIsValidDomain(event) {
  const listDomainValid = ['https://x-pcw.com', 'http://localhost:8080']
  if (listDomainValid.includes(event.headers.origin)) return true
  return false;
}

module.exports = async (event) => {
  const queryParams = event.queryStringParameters;

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
    agencyFilterExpressionValues.push(`begins_with(#DOMAIN, :domain${agencyIndex})`);
    agencyValues[`:domain${agencyIndex}`] = agencyItems[agencyIndex];
    agencyFilterExpressionNames['#DOMAIN'] = 'domain'
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
    KeyConditionExpression: isRep ? "#PK = :pk and begins_with(SK, :sk)" : "#PK = :pk",
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
      ...agencyFilterExpressionNames,
      ...brandFilterExpressionNames
    },
    ExpressionAttributeValues: {
      ":pk": PK,
      ":minPrice": minPrice,
      ":maxPrice": maxPrice,
      ":discountRate": discountRate,
      ...isRep ? { ":sk": "REP#" } : {},
      ...agencyValues,
      ...brandValues,
    },
  };
  console.log('params', params)
  const data = await dynamodbHelper.queryItems(params);
  console.log('data', data.length)
  return data.slice((page - 1) * limit, page * limit)
}

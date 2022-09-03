const dynamodbHelper = require("../helper/DynamodbHelper");

function checkIsValidDomain(event) {
  const listDomainValid = ["https://x-pcw.store", "http://localhost:8080", "https://d3kxmkwimuhvhe.cloudfront.net"];
  if (event.headers && Object.keys(event.headers).includes('origin') && listDomainValid.includes(event.headers.origin)) return true;
  return false;
}

module.exports = async (event, context) => {
  const queryParams = event.queryStringParameters;
  let data = null;
  let res = null;
  console.log('queryParams["action"]', queryParams["action"])
  if (!queryParams) {
    throw new Error("There's no query parameter");
  } else {
    if (checkIsValidDomain(event)) {
      switch (queryParams["action"]) {
        case "getUserInfo":
          data = await queryUserInfo(event);
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
    } else {
      res = {
        message: "Failed",
        action: queryParams["action"],
        data: data,
      };
    }
  }
  return res;
};

async function queryUserInfo(event) {
  console.log('event', event)
  const id = event.queryStringParameters["id"] || "";
  if (!id) return null;
  const params = {
    TableName: process.env.USER_TABLE_NAME,
    Key: {
      PK: 'USER',
      SK: id,
    },
    ExpressionAttributeNames: {
      "#NAME": "name"
    },
    ProjectionExpression: 'PK, SK, email, #NAME, givenName, familyName, picture, locale',
  }
  return await dynamodbHelper.getItem(params);
}


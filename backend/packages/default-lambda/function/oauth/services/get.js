const dynamodbHelper = require("../helper/DynamodbHelper");

module.exports = async (event) => {
  const queryParams = event.queryStringParameters;
  let data = null;
  let res = null;
  console.log('queryParams["action"]', queryParams["action"])
  if (!queryParams) {
    throw new Error("There's no query parameter");
  } else {
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
    ProjectionExpression: 'PK, SK, email, #NAME, givenName, familyName, picture, locale, lastTimeLogin, lastTimeIP, expriedAt',
  }
  return await dynamodbHelper.getItem(params);
}


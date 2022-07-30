const AWS = require("aws-sdk");
const dynamodbClient = new AWS.DynamoDB.DocumentClient();

module.exports.getItem = function (params) {
  return dynamodbClient.get(params).promise();
};

/**
 * @param {AWS.DynamoDB.DocumentClient.ScanInput} params
 */
module.exports.scanAllItems = async function (params) {
  let result = null;
  const items = [];
  do {
    result = await dynamodbClient.scan(params).promise();
    items.push(...(result.Items || []));
    params = {
      ...params,
      ExclusiveStartKey: result.LastEvaluatedKey,
    };
  } while (result.LastEvaluatedKey);
  return items;
};

/**
 * @param {AWS.DynamoDB.DocumentClient.QueryInput} params
 */
        module.exports.queryAllItems = async function (params) {
        let result = null;
        const items = [];
    do {
        result = await dynamodbClient.query(params).promise();
        items.push(...(result.Items || []));
        params = {
      ...params,
      ExclusiveStartKey: result.LastEvaluatedKey,
    };
  } while (result.LastEvaluatedKey);
  return items;
};

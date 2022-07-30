const AWS = require("aws-sdk");
const dynamodbClient = new AWS.DynamoDB.DocumentClient();

/**
 * @param {AWS.DynamoDB.DocumentClient.GetInput} params
 */
module.exports.queryItem = function (params) {
  return dynamodbClient.get(params).promise();
};

module.exports.deleteItem = function (params) {
  return dynamodbClient.delete(params).promise();
};

module.exports.putItem = function (params) {
  return dynamodbClient.put(params).promise();
};

/**
 * @param {AWS.DynamoDB.DocumentClient.QueryInput} params
 */
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

/**
 * @param {AWS.DynamoDB.DocumentClient.QueryInput} params
 */
module.exports.queryAllItemsByLimit = async function (params, limit) {
  let result = null;
  const items = [];
  do {
    result = await dynamodbClient.query(params).promise();
    items.push(...(result.Items || []));
    params = {
      ...params,
      ExclusiveStartKey: result.LastEvaluatedKey,
    };

    if (items.length > limit) {
      return items.slice(0, limit)
    }
  } while (result.LastEvaluatedKey);
  return items;
};

/**
 * @param {AWS.DynamoDB.DocumentClient.QueryInput} params
 */
module.exports.queryItems = async function (params) {
  let result = null;
  result = await dynamodbClient.query(params).promise();
  return result.Items || [];
};

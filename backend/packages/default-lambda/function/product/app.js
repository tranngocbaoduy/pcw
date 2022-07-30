/**
 *
 * Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
 * @param {Object} event - API Gateway Lambda Proxy Input Format
 *
 * Context doc: https://docs.aws.amazon.com/lambda/latest/dg/nodejs-prog-model-context.html
 * @param {Object} context
 *
 * Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
 * @returns {Object} object - API Gateway Lambda Proxy Output Format
 *
 */

const get = require("./services/get");
const post = require("./services/post");

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "*",
  "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
};

exports.lambdaHandler = async (event, context) => {
  console.log(event);
  console.log(context);
  let response = {};
  try {
    if (event.httpMethod == "GET") {
      response = await get(event, context);
    }
    if (event.httpMethod == "POST") {
      response = await post(event, context);
    }
    response = {
      statusCode: 200,
      body: JSON.stringify(response),
      headers: {
        ...CORS_HEADERS,
      },
    };
  } catch (err) {
    console.log(err);
    return {
      statusCode: 400,
      body: JSON.stringify(err.message),
      headers: {
        ...CORS_HEADERS,
      },
    };
  }

  return response;
};

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

function checkIsValidDomain(event) {
  const listDomainValid = ["https://x-pcw.store", "http://localhost:8080", "https://d3kxmkwimuhvhe.cloudfront.net"];
  if (event.headers && Object.keys(event.headers).includes('origin') && listDomainValid.includes(event.headers.origin)) return true;
  return false;
}

const get = require("./services/get");
const post = require("./services/post");

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "*",
  "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
};

exports.lambdaHandler = async (event, context) => {
  context.callbackWaitsForEmptyEventLoop = false
  let response = {};
  try {
    if (checkIsValidDomain(event)) {
      if (event.httpMethod == "GET") {
        response = await get(event, context);
      }
      if (event.httpMethod == "POST") {
        response = await post(event, context);
      }
    } else {
      response = {
        message: "Failed",
        data: null,
      };
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

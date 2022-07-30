// const axios = require('axios')
// const url = 'http://checkip.amazonaws.com/';
let response;

let AWS = require("aws-sdk");
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

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "*",
  "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
};

exports.lambdaHandler = async (event, context) => {
  let data = null;
  try {
    const queryParams = event.queryStringParameters;
    if (!queryParams)
      return {
        statusCode: 400,
        body: "No found any service",
        headers: {
          ...CORS_HEADERS,
        },
      };

    switch (queryParams["service"]) {
      case "execute-api":
      default:
        data = await getCredentialsExecuteApi();
        break;
    }
  } catch (err) {
    console.log(err);
    return err;
  }

  return {
    statusCode: 200,
    body: JSON.stringify({
      data: data,
    }),
    headers: {
      ...CORS_HEADERS,
    },
  };
};

async function getCredentialsExecuteApi() {
  const sts = new AWS.STS();
  const params = {
    Policy: JSON.stringify({
      Version: "2012-10-17",
      Statement: [
        {
          Effect: "Allow",
          Action: ["execute-api:Invoke"],
          Resource: [
            `arn:aws:execute-api:${process.env.API_REGION}:*:${process.env.REST_API_ID}/*/*`,
          ],
        },
      ],
    }),
    RoleSessionName: `api-gateway-${process.env.ENV_NAME}`,
    RoleArn: process.env.DEFAULT_ROLE_ARN,
    DurationSeconds: 3600,
  };
  // async/await.
  let data = null;
  try {
    data = await sts.assumeRole(params).promise();
    // process data.
  } catch (error) {
    // error handling.
    console.log("error", error);
  }
  return data;
}

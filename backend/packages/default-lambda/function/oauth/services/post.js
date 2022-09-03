const axios = require('axios')
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
        case "authorize_code":
          data = await authorizationCode(event);
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

async function getUserInfo(accessToken) {
  const url = `https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=${accessToken}`;
  try {
    const data = await axios.get(url).then((response) => response.data);
    console.log('getUserInfo', data);
    return data;
  } catch (err) {
    return null;
  }
}

async function authorizationCode(event) {
  // Google's OAuth 2.0 endpoint for requesting an access token
  const body = JSON.parse(event.body);
  const code = body["code"];
  const redirect_uri = body["redirectURI"];
  const oauth2Endpoint = 'https://oauth2.googleapis.com/token';

  const params = {
    code: code,
    client_id: process.env.GOOGLE_CLIENT_ID,
    client_secret: process.env.GOOGLE_CLIENT_SECRET,
    redirect_uri: redirect_uri || process.env.GOOGLE_CLIENT_REDIRECT_URL,
    grant_type: 'authorization_code',
  };

  const res = await axios.post(oauth2Endpoint, params).then(async (res) => {
    // example
    // {
    //   "id": "102759011852820578273",
    //   "email": "duytnb2608.work@gmail.com",
    //   "verified_email": true,
    //   "name": "duy tnb",
    //   "given_name": "duy",
    //   "family_name": "tnb",
    //   "picture": "https://lh3.googleusercontent.com/a/AItbvml2Atcq7iLskhisia93ggRYbigYrfAbyMwu9Bc=s96-c",
    //   "locale": "en"
    // }
    let data = await getUserInfo(res.data.access_token);
    const params = {
      TableName: process.env.USER_TABLE_NAME,
      Key: {
        PK: 'USER',
        SK: data.id,
      },
      ExpressionAttributeNames: {
        "#NAME": "name"
      },
      ProjectionExpression: 'PK, SK, email, #NAME, givenName, familyName, picture, locale',
    }
    const userInfo = await dynamodbHelper.getItem(params)
    if (!userInfo) {
      console.log("[FIRST LOGIN] =>", data)
      const params = {
        TableName: process.env.USER_TABLE_NAME,
        Item: {
          PK: 'USER',
          SK: data.id,
          email: data.email,
          name: data.name,
          givenName: data.given_name,
          familyName: data.family_name,
          picture: data.picture,
          locale: data.locale,
          accessToken: res.data.access_token,
          refreshToken: res.data.refresh_token,
          expriedAt: new Date(new Date().getTime() + res.data.expires_in * 1000).toISOString(),
        }
      }
      await dynamodbHelper.putItem(params)
      data = {
        PK: 'USER',
        SK: data.id,
        email: data.email,
        name: data.name,
        givenName: data.given_name,
        familyName: data.family_name,
        picture: data.picture,
        locale: data.locale,
      }
    } else {
      data = userInfo;
      console.log("[LOGIN] =>", userInfo)
    }
    return data;
  }).catch(err => {
    console.log('[ERR] =>', err);
    throw err;
  });


  return res
}
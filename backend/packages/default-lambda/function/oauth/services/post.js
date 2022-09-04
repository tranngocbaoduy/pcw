const axios = require('axios')
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
  let userIP = ''
  try {
    userIP = event['requestContext']['identity']['sourceIp']
  } catch (err) {
    userIP = ''
  }
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
      ProjectionExpression: 'PK, SK, email, #NAME, givenName, familyName, picture, locale, lastTimeLogin, lastTimeIP, countLoginTime',
    }
    const userInfo = await dynamodbHelper.getItem(params)
    if (!userInfo) {
      console.log("[FIRST LOGIN] =>", data)
      const dummyIp = {}
      dummyIp[userIP] = [new Date().toISOString()]
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
          lastTimeLogin: new Date().toISOString(),
          lastTimeIP: dummyIp,
          countLoginTime: 0,
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

      const dummyLastTimeIP = userInfo.lastTimeIP;
      if (!Object.keys(dummyLastTimeIP).includes(userIP)) {
        dummyLastTimeIP[userIP] = [new Date().toISOString()]
      } else {
        dummyLastTimeIP[userIP].push(new Date().toISOString())
        dummyLastTimeIP[userIP] = dummyLastTimeIP[userIP].sort((a, b) => { if (a > b) return 1; return -1 })
      }
      const newUserInfo = {
        ...userInfo,
        lastTimeLogin: new Date().toISOString(),
        lastTimeIP: dummyLastTimeIP,
        accessToken: res.data.access_token,
        refreshToken: res.data.refresh_token,
        expriedAt: new Date(new Date().getTime() + res.data.expires_in * 1000).toISOString(),
        countLoginTime: userInfo.countLoginTime + 1
      }
      const params = {
        TableName: process.env.USER_TABLE_NAME,
        Item: newUserInfo
      }
      await dynamodbHelper.putItem(params)
      data = newUserInfo;
      delete data['countLoginTime']
      delete data['lastTimeIP']
      delete data['accessToken']
      delete data['refreshToken']
      console.log("[LOGIN] =>", userInfo)
    }
    return data;
  }).catch(err => {
    console.log('[ERR] =>', err);
    throw err;
  });


  return res
}
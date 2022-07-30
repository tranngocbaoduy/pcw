// const winston = require('winston');

// const tokenHelper = require('../helpers/token.helper');
var jwt = require('jsonwebtoken');
/**
 * @param {{
 *   body: string;
 *   pathParameters: {
 *     tenant_id: string;
 *     username: string;
 *   };
 *   requestContext: {
 *     identity: {
 *       cognitoIdentityId: string|null;
 *       cognitoAuthenticationProvider: string|null;
 *     }
 *   }
 * }} event
 */
exports.parseEvent = async function (event) {
  const jwtDecode = jwt.decode(event.headers['id-token']);
  console.log('jwtDecode', jwtDecode)
  const iss = jwtDecode.iss;
  const userPoolId = iss.split('com/')[1];
  const tenantId = event.pathParameters['tenant_id'];
  const targetUsername = event.pathParameters['username'];
  const groupId = jwtDecode['cognito:groups'] ? jwtDecode['cognito:groups'][0] : '';
  const tenantPreferredId = jwtDecode['custom:tenant_preferred_id'];
  const email = jwtDecode.email;
  const role = jwtDecode['custom:role'];
  const system_role = jwtDecode['custom:system_role'];
  const tenant_api_role = jwtDecode['custom:tenant_api_role'];

  return {
    userPoolId,
    tenantId,
    targetUsername,
    groupId,
    tenantPreferredId,
    email,
    role,
    system_role,
    tenant_api_role,
  };
};

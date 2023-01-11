import axios from 'axios';
import Auth, { CognitoUser } from '@aws-amplify/auth';
import { AuthOptions } from '@aws-amplify/auth/lib-esm/types';
import AWS from 'aws-sdk';
import AWS4 from 'aws4';

export interface CognitoUserCustom extends CognitoUser {
  name?: string;
}
export interface ICredentials {
  AccessKeyId: string;
  Expiration: string;
  SecretAccessKey: string;
  SessionToken: string;
}

export interface ICredentialsService {
  executeApi?: ICredentials | null;
  // dynamodb?: ICredentials | null;
}

axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
export default class AuthService {
  public static api = axios.create();
  private static config = {} as any;
  private static userCustom = {} as any;
  private static _currentCredentialsPromise = {
    executeApi: null as Promise<ICredentials | undefined | null> | null,
    // dynamodb: null as Promise<ICredentials | undefined | null> | null,
  };

  static async setCachedConfigure(): Promise<void> {
    AuthService.config = await Auth.configure({
      region: process.env.VUE_APP_AWS_REGION,
      authenticationFlowType: 'USER_SRP_AUTH',
      userPoolId: process.env.VUE_APP_SYSTEM_ADMIN_USER_POOL_ID,
      userPoolWebClientId: process.env.VUE_APP_SYSTEM_ADMIN_USER_POOL_WEB_CLIENT_ID,
      identityPoolId: process.env.VUE_APP_SYSTEM_ADMIN_IDENTITY_POOL_ID_1,
      storage: localStorage,
    } as AuthOptions);
  }

  static async signInDefault(): Promise<void> {
    AWS.config.region = process.env.VUE_APP_AWS_REGION; // Region
    AWS.config.credentials = new AWS.CognitoIdentityCredentials({
      IdentityPoolId: process.env.VUE_APP_SYSTEM_ADMIN_IDENTITY_POOL_ID_1 as string,
    });

    await AuthService.setCachedConfigure();
    try {
      await Auth.signIn({
        username: process.env.VUE_APP_AWS_SYSTEM_ADMIN_USER_DEFAULT || '',
        password: process.env.VUE_APP_AWS_SYSTEM_ADMIN_PASSWORD_DEFAULT || '',
      });
    } catch (err) {
      console.log(err);
    }
  }

  static setCachedConfigAuth(userName: string): void {
    localStorage.setItem(`AuthCognitoConfig.${userName}`, JSON.stringify(AuthService.config));
  }

  static getCachedConfigAuth(userName: string): any {
    const config = localStorage.getItem(`AuthCognitoConfig.${userName}`);
    return config != null && Object.keys(config).length != 0 ? JSON.parse(config) : false;
  }

  static async currentCredentials(
    service: keyof ICredentialsService = 'executeApi',
    opts = { bypassCache: false }
  ): Promise<any> {
    if (!service) service = 'executeApi';
    if (!AuthService._currentCredentialsPromise[service]) {
      AuthService._currentCredentialsPromise[service] = AuthService.__currentCredentials(service, opts);
    }

    return (AuthService._currentCredentialsPromise[service] as Promise<ICredentials>)
      .then((r) => {
        AuthService._currentCredentialsPromise[service] = null;
        return r;
      })
      .catch((r) => {
        console.log('eeeee', r);
        AuthService._currentCredentialsPromise[service] = null;
        throw r;
      });
  }

  static async __currentCredentials(
    service: keyof ICredentialsService = 'executeApi',
    opts = { bypassCache: true }
  ): Promise<any> {
    if (!AuthService.isAuthenticated()) {
      return null;
    }
    if (!opts.bypassCache) {
      return (AuthService.getCachedCredentials() as any)[service];
    }
    const token = await AuthService.getJwtToken();
    const data = await axios
      .get(
        `${process.env.VUE_APP_API_BASE_URL}/${process.env.VUE_APP_ENV}/credentials?service=${
          service == 'executeApi' ? 'execute-api' : service
        }`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      .then((response) => {
        return response.data.data;
      })
      .catch((err) => {
        console.log('err', err);
      });

    if (service == 'executeApi') {
      AuthService.clearCredentials(service);
      await AuthService.setCachedConfigure();
      AuthService.setCredentials(service, data.Credentials);
    }

    return await AuthService._currentCredentialsPromise[service];
  }

  static setCredentials(
    service: keyof ICredentialsService = 'executeApi',
    credentials: Promise<ICredentials | undefined | null> | null
  ) {
    AuthService._currentCredentialsPromise[service] = credentials;
  }
  static clearCredentials(service: keyof ICredentialsService = 'executeApi') {
    AuthService._currentCredentialsPromise[service] = null;
  }

  static async isAuthenticated(): Promise<boolean> {
    try {
      if (Object.keys(AuthService.config).length > 0) return true;
      await AuthService.signInDefault();
      return false;
    } catch {
      await AuthService.signInDefault();
      return false;
    }
  }

  static async getUserDefault(): Promise<any> {
    try {
      return (await Auth.currentAuthenticatedUser()) as CognitoUser;
    } catch {
      console.log('err user not exist');
      return (await Auth.currentAuthenticatedUser()) as CognitoUser;
    }
  }

  static async getJwtToken() {
    const user = await AuthService.getUserDefault();
    return (await user?.getSignInUserSession()?.getIdToken().getJwtToken()) || '';
  }

  static async getTimeLeftExpiration(): Promise<number> {
    const user = await AuthService.getUserDefault();
    return (await user?.getSignInUserSession()?.getIdToken().getExpiration()) || 0;
  }

  static setCachedCredentials(userName: string, credentialsService: ICredentialsService): any {
    if (credentialsService == null) localStorage.removeItem(`AuthCredentials.${userName}`);
    else localStorage.setItem(`AuthCredentials.${userName}`, JSON.stringify(credentialsService));
  }

  static async getCachedCredentials(): Promise<any> {
    const user = await this.getUserDefault();
    const credentialsRefresh: ICredentialsService = {
      // dynamodb: undefined,
    };

    let credentialsConfig: any = localStorage.getItem(`AuthCredentials.${user.getUsername()}`);
    credentialsConfig = credentialsConfig && credentialsConfig.length != 0 ? JSON.parse(credentialsConfig) : {};
    const configAuth: any = AuthService.getCachedConfigAuth(user.getUsername());
    return {
      ...credentialsRefresh,
      ...credentialsConfig,
      ...configAuth,
    };
  }

  static isValidHttpUrl(str: string): boolean {
    let url;
    try {
      url = new URL(str);
    } catch (_) {
      return false;
    }
    const validDomains = ['tiki.vn', 'shopee.vn', 'www.lazada.vn'];
    console.log(
      '[URL] =>',
      (url.protocol === 'http:' || url.protocol === 'https:') && validDomains.includes(url.hostname),
      str
    );
    return (url.protocol === 'http:' || url.protocol === 'https:') && validDomains.includes(url.hostname);
  }
}

//https://github.com/axios/axios
AuthService.api.interceptors.request.use(async (config) => {
  const credentials = await AuthService.currentCredentials('executeApi');
  if (!credentials) return config;
  const jwtToken = await AuthService.getJwtToken();
  const opts: any = {
    host: new URL(process.env.VUE_APP_API_BASE_URL || '').host,
    service: 'execute-api',
    region: process.env.VUE_APP_AWS_REGION,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Origin, X-Requested-With',
    },
    method: config.method?.toUpperCase(),
  };
  AWS4.sign(opts, {
    accessKey: credentials.accessKey,
    secretAccessKey: credentials.secretAccessKey,
    sessionToken: credentials.sessionToken,
  });

  delete opts.headers['Host'];
  delete opts.headers['Content-Length'];
  opts.headers['Authorization'] = 'Bearer ' + jwtToken;

  config.headers = {
    ...opts.headers,
    ...config.headers,
  };
  return config;
});

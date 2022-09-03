import store from '@/store';
import axios from 'axios';
import { uniqueId } from 'lodash';
import AuthService from './auth.service';

export interface UserGoogleInfo {
  id: string;
  email: string;
  name: string;
  givenName: string;
  familyName: string;
  picture: string;
  locale: string;
}

export default class GoogleAuthService {
  static getUserAuth(): UserGoogleInfo {
    return store.getters.userGoogleInfo;
  }

  static async logout() {
    localStorage.setItem('google-auth', '');
    localStorage.removeItem('google-auth');
    store.dispatch('logout');
  }

  static async getUserInfo(id: string): Promise<any> {
    const url = process.env.VUE_APP_API_BASE_URL + `/${process.env.VUE_APP_ENV}/oauth?action=getUserInfo&id=${id}`;
    try {
      const data = await AuthService.api
        .get(url)
        .then((response: any) => GoogleAuthService.parseGoogleUserInfo(response.data.data));
      return data;
    } catch (err) {
      return [];
    }
  }

  static async login() {
    // Google's OAuth 2.0 endpoint for requesting an access token
    const oauth2Endpoint = 'https://accounts.google.com/o/oauth2/v2/auth';

    // Create <form> element to submit parameters to OAuth 2.0 endpoint.
    const form = document.createElement('form');
    form.setAttribute('method', 'GET'); // Send as a GET request.
    form.setAttribute('action', oauth2Endpoint);

    // Parameters to pass to OAuth 2.0 endpoint.
    const params = {
      client_id: process.env.VUE_APP_GOOGLE_CLIENT_ID,
      redirect_uri: `${window.location.origin}/login`,
      response_type: 'code',
      scope: ['email', 'profile', 'openid'].join(' '),
      include_granted_scopes: 'false',
      state: uniqueId(),
      prompt: 'consent',
    } as any;
    console.log('params', params);

    // Add form parameters as hidden input values.
    for (const p in params) {
      const input = document.createElement('input');
      input.setAttribute('type', 'hidden');
      input.setAttribute('name', p);
      input.setAttribute('value', params[p]);
      form.appendChild(input);
    }

    // Add form to page and submit it to open the OAuth 2.0 endpoint.
    document.body.appendChild(form);
    form.submit();
  }

  static async authorizeCode({ scope, state, code }: { scope: string; state: string; code: string }) {
    const url = process.env.VUE_APP_API_BASE_URL + `/${process.env.VUE_APP_ENV}/oauth?action=authorize_code`;
    const params = { code: code, state: state, scope: scope };
    try {
      const data = await axios
        .post(url, params)
        .then((response: any) => {
          return GoogleAuthService.parseGoogleUserInfo(response.data.data);
        })
        .catch((err: any) => {
          console.log('[ERR] => ', err);
          return null;
        });
      return data;
    } catch (err) {
      return [];
    }
  }

  static parseGoogleUserInfo(data: any) {
    return {
      id: data.SK,
      email: data.email,
      name: data.name,
      givenName: data.givenName,
      familyName: data.familyName,
      picture: data.picture,
      locale: data.locale,
    };
  }
}

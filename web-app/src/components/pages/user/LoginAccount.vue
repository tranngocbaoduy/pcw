<template>
  <v-card
    elevation="0"
    width="400"
    height="200"
    class="pa-auto ma-auto rounded-0 d-flex-column justify-center align-center my-4 py-4"
  >
    <v-card-text class="d-flex justify-center align-center">
      <div class="text-center font-size-22">Login</div>
    </v-card-text>
    <v-card-actions class="d-flex align-center justify-center">
      <v-btn width="350" elevation="1" color="primary" class="text-capitalize" @click="login"
        >Sign in with Google</v-btn
      >
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import GoogleAuthService, { UserGoogleInfo } from '@/api/google-auth.service';
import Vue from 'vue';
export default Vue.extend({
  data() {
    return {
      noItemImage: require('@/assets/image/logo/Light.png'),
    };
  },
  computed: {
    isAuthenticated(): boolean {
      return this.$store.getters.isAuthenticated;
    },
  },
  async created() {
    console.log('this.isAuthenticated', this.isAuthenticated);

    if (!this.isAuthenticated) {
      await this.handleOauth();
    } else {
      this.$router.push('/');
    }
  },
  methods: {
    async login() {
      await GoogleAuthService.login();
    },
    async handleOauth(): Promise<void> {
      const loader = this.$loading.show();
      const res = {
        state: (this.$route?.query?.state as string) || '',
        code: (this.$route?.query?.code as string) || '',
        scope: (this.$route?.query?.scope as string) || '',
        userGoogleInfo: (this.$route?.query?.userGoogleInfo as string) || '',
        prompt: (this.$route?.query?.prompt as string) || '',
      };
      if (res.code && res.state && res.scope) {
        const data = (await GoogleAuthService.authorizeCode({
          state: res.state,
          scope: res.scope,
          code: res.code,
        })) as UserGoogleInfo;
        console.log('[LOGIN GOOGLE] => ', data);
        if (data) {
          localStorage.setItem('google-auth', JSON.stringify({ id: data.id }));
          this.$store.dispatch('login', { data });
          this.$router.push('/');
        } else {
          localStorage.setItem('google-auth', '');
          localStorage.removeItem('google-auth');
        }
      } else {
        localStorage.setItem('google-auth', '');
        localStorage.removeItem('google-auth');
        if (this.isAuthenticated) this.$router.push('/');
      }
      loader.hide();
    },
  },
});
</script>

<template lang="pug">
.d-flex.flex-row.justify-content-center.vh-100
  .d-flex.flex-column.col-md-4.gap-3.justify-content-center
      h2.text-center.fw-bold Sign in
      button.btn.btn-lg.btn-outline-secondary.social-btn-main-width-descriptor.text-center.text-nowrap(@click="SignInGauth") Log in with Google
      .row
          .col-5
              hr.or-line
          .col-2.text-center
              span.or-text or
          .col-5
              hr.or-line
      input.form-control.form-rounded(type="email" v-model="email" @input="onInput" placeholder="Enter email address")
      input.form-control.form-rounded(type="password" v-model="password" @input="onInput" placeholder="Password")
      .d-flex.flex-row.justify-content-center.w-100(v-if="typing")
        vue-recaptcha(:sitekey="recaptchaKey" @verify="onRecaptchaVerified" @expired="onRecaptchaExpired")
      button.btn.btn-lg.btn-dark.social-btn-email-width-descriptor(@click="SignIn") 
        .d-flex.flex-row.align-items-center.justify-content-center
          .text(v-if="!loading") Log in with Email
          .spinner-grow(v-else)
      .d-flex.flex-row.justify-content-center
        .me-2 Don't have an account?
        a(href="/sign-up") Sign up
      .d-flex.flex-row.justify-content-center
        a(href="/")
          img(:src="images.logo" alt="Splendy" width="75" height="23")
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import logo from '../assets/logo-transparents.svg'
import { useSignStore } from '@/stores/signStore'
import { useToasts } from '@/composables/useToasts'
import { VueRecaptcha } from 'vue-recaptcha';

export default defineComponent({
    name: 'LoginPage',
    components: { VueRecaptcha },
    setup() {
        
        const { addToast } = useToasts()
        return {
            addToast,
            recaptchaKey: import.meta.env.VITE_CAPTCHA_SITE_KEY_V2
        }
    },
    data() {
        return {
            email: '',
            password: '',
            loading: false,
            signStore: useSignStore(),
            recaptchaChecked: false,
            images: {
                logo,
            },
            typing: false
        }
    },
    methods: {
        SignInGauth() {
            this.addToast({ message: 'Signing in with Google is not currently available', type: 'warning' })
        },
        async SignIn() {
            try {
                if (!this.recaptchaChecked && import.meta.env.VITE_DEBUG !== 'true') {
                    this.addToast({ message: 'Please complete the reCAPTCHA verification', type: 'warning' });
                    return;
                }
                this.loading = true
                const result = await this.signStore.signIn(
                    this.email,
                    this.password
                )
                if (result.success) {
                    this.$router.push('/dashboard')
                }
            } finally {
                this.loading = false
            }
        },
        onRecaptchaVerified(_: any) {
            this.recaptchaChecked = true;
        },
        onRecaptchaExpired() {
            this.recaptchaChecked = false;
        },
        onInput() {
            this.typing = true;
        },
    },
})
</script>

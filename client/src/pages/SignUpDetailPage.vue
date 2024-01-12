<template lang="pug">
.d-flex.flex-row.justify-content-around.px-5.vh-100
    .d-flex.flex-column.col-md-4.gap-3.justify-content-center
        h2.text-center.fw-bold Account details
        .mail
            input.form-control.form-rounded(type="email" placeholder="Email address" v-model="v$.email.$model", :class="v$.email.$invalid && v$.email.$dirty ? 'is-invalid' : ''"  @input="typing=true")
            .invalid-feedback(v-if="v$.email.$invalid && v$.email.$dirty") Invalid email
        .d-flex.flex-row.gap-4
            input.form-control.form-rounded(type="text" placeholder="First name" v-model="v$.firstName.$model")
            input.form-control.form-rounded(type="text" placeholder="Last name" v-model="v$.lastName.$model")
        .password
            input.form-control.form-rounded(type="password" placeholder="Password" v-model="v$.password.$model", :class="v$.password.$invalid && v$.password.$dirty ? 'is-invalid' : ''")
            .invalid-feedback(v-if="v$.password.$invalid && v$.password.$dirty") Password should contain at least 8 characters, 1 number and 1 uppercase (or special) character
        //- .currency
        //-     select#currencyDropdown.form-control(v-model="currentCurrency" required)
        //-         option(:value="''" selected disabled) Choose your currency
        //-         option(v-for="curr in currencies" :key="curr" :value="curr" ) {{  curr }}
        .d-flex.flex-row.justify-content-center.w-100(v-if="typing")
            vue-recaptcha(:sitekey="recaptchaKey" @verify="onRecaptchaVerified" @expired="onRecaptchaExpired")
        button.btn.btn-lg.btn-dark.social-btn-email-width-descriptor(@click="signUp" :disabled="loading") 
            .d-flex.flex-row.align-items-center.justify-content-center
                .text(v-if="!loading") Sign up
                .spinner-grow(v-else)
        .d-flex.flex-row.justify-content-center
            .me-2 Already have an account?
            a(href="/login") Sign in
        .d-flex.flex-row.justify-content-center
            a(href="/")
                img(:src="images.logo" alt="Splendy" width="75" height="23")
</template>

<script lang="ts">
import { useSignStore } from '@/stores/signStore'
import useVuelidate from '@vuelidate/core'
import { required, email, minLength } from '@vuelidate/validators'
import { defineComponent } from 'vue'
import logo from '../assets/logo-transparents.svg'
import { VueRecaptcha } from 'vue-recaptcha'
import { useToasts } from '@/composables/useToasts'

export default defineComponent({
    name: 'SignUpDetailPage',
    components: { VueRecaptcha },
    setup() {
        const { addToast } = useToasts()
        // const currentCurrency = ref('')
        return {
            v$: useVuelidate(),
            signStore: useSignStore(),
            recaptchaKey: import.meta.env.VITE_CAPTCHA_SITE_KEY_V2,
            addToast,
            // currentCurrency,
        }
    },
    data() {
        return {
            //@ts-ignore
            email: this.signStore.storedEmail,
            firstName: '',
            lastName: '',
            password: '',
            loading: false,
            typing: false,
            recaptchaChecked: false,
            // currencies,
            images: {
                logo,
            },
        }
    },
    validations() {
        const mustBeCorrectPassword = (value: string) => {
            const containsNumber = /[0-9]/.test(value)
            const containsUppercase = /[A-Z]/.test(value)
            const containsSpecial = /[#?!@$%^&*-.]/.test(value)
            return containsNumber && (containsSpecial || containsUppercase)
        }
        return {
            email: { required, email },
            firstName: { required },
            lastName: { required },
            password: {
                required,
                minLength: minLength(8),
                mustBeCorrectPassword,
            },
        }
    },
    methods: {
        async signUp() {
            try {
                if (
                    !this.recaptchaChecked &&
                    import.meta.env.VITE_DEBUG !== 'true'
                ) {
                    this.addToast({
                        message: 'Please complete the reCAPTCHA verification',
                        type: 'warning',
                    })
                    return
                }

                this.loading = true
                const result = await this.signStore.signUp(
                    this.email,
                    this.firstName,
                    this.lastName,
                    this.password,
                )
                if (result.success) {
                    this.$router.push('/dashboard')
                }
            } finally {
                this.loading = false
            }
        },
        onRecaptchaVerified(_: any) {
            this.recaptchaChecked = true
        },
        onRecaptchaExpired() {
            this.recaptchaChecked = false
        },
    },
})
</script>

<style scoped lang="scss">
select:invalid {
  color: gray;
}


option {
  color: black;
}
</style>

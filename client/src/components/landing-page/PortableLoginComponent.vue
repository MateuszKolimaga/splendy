<template lang="pug">
.portable-login-item.card.p-5
    .d-flex.flex-column.gap-3
        h2.text-center.fw-bold Sign up
        button.btn.btn-lg.btn-outline-secondary.social-btn-main-width-descriptor.text-center.text-nowrap.overflow-hidden 
            span.px-4(@click="signUpGauth") Continue with Google
        .row.my-2
            .col-5
                hr.or-line
            .col-2.text-center
                span.or-text.text-nowrap or
            .col-5
                hr.or-line
        input.form-control.form-rounded(type="email" v-model="email" placeholder="Enter email address")
        button.btn.btn-lg.btn-dark.social-btn-email-width-descriptor(@click="signUp") Continue with Email
</template>

<script lang="ts">
import { useToasts } from '@/composables/useToasts';
import LoginPage from '@/pages/LoginPage.vue'
import { useSignStore } from '@/stores/signStore';
import { defineComponent, ref } from 'vue'

export default defineComponent({
    name: 'PortableLoginComponent',
    components: { LoginPage },
    setup() {
        const email = ref("")
        const signStore = useSignStore();
        const { addToast } = useToasts()
        return {
            email,
            signStore,
            addToast
        }
    },
    methods: {
        signUp() {
            this.signStore.setStoredEmail(this.email)
            this.$router.push({ name: 'SignUpDetail'})
        },
        signUpGauth() {
            this.addToast({ message: 'Signing up with Google is not currently available', type: 'warning' })
            this.signUp()
        }
    }
})
</script>

<style scoped lang="scss">
@import "@/styles/styles.scss";

.portable-login-item {
    border: 1px solid grey !important;
    transition: transform 0.3s ease-in-out;

    &:hover {
        transform: scale(1.02);
        // box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    &:not(:hover) {
        transition: transform 0.5s ease-in-out;
    }
}
</style>

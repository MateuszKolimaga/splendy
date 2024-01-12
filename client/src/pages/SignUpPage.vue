<template lang="pug">
.d-flex.flex-row.justify-content-center.vh-100
  .d-flex.flex-column.col-md-4.gap-3.justify-content-center
      h2.text-center.fw-bold Sign up
      button.btn.btn-lg.btn-outline-secondary.social-btn-main-width-descriptor.text-center.text-nowrap(@click="signUpGauth") Sign up with Google
      .row
          .col-5
              hr.or-line
          .col-2.text-center
              span.or-text or
          .col-5
              hr.or-line
      button.btn.btn-lg.btn-dark.social-btn-email-width-descriptor(@click="signUp") Sign up with Email
      .d-flex.flex-row.justify-content-center
        .me-2 Already have an account?
        a(href="/login") Sign in
      .d-flex.flex-row.justify-content-center
        a(href="/")
            img(:src="images.logo" alt="Splendy" width="75" height="23")
</template>

<script lang="ts">
import { defineComponent } from "vue";
import logo from "../assets/logo-transparents.svg";
import { useToasts } from "@/composables/useToasts";

export default defineComponent({
    name: "SignUpPage",
    setup() {
      const { addToast } = useToasts()
        return {
          addToast
        }
    },
    methods: {
        signUpGauth() {
            this.addToast({ message: 'Signing up with Google is not currently available', type: 'warning' })
            this.signUp()
        },
        signUp() {
            this.$router.push("/sign-up-detail")
        }
    },
    data() {
    return {
      images: {
        logo
      }
    }
    }
});
</script>

<style lang="scss" scoped>
@import "@/styles/styles.scss";


#email-input {
    border: 1px solid white;
    border-radius: 10px;
    background-color: $app-grey;
}
</style>
    
<template lang="pug">
.content.py-5
    .actual-content.flex-wrap.container-fluid
        .row.d-flex.flex-row.justify-content-around
            .card.mx-3.my-4.align-items-center.col-3.pb-1(@click="goLogin" style="cursor: pointer")
                img.invite-image.card-img-top(:src="images.friendsImage", alt="friendslImage" style="width: 23rem; height: 20rem")
                .card-body
                    h4.card-title.text-opacity-75.fw-bold Split bills with your friends
                    p.card-text.text-muted Manage shared expenses easily by splitting bills with friends. Keep track of who owes what.
            .card.mx-3.my-4.align-items-center.col-3.pb-1(@click="goLogin" style="cursor: pointer")
                img.invite-image.card-img-top(:src="images.personalImage", alt="personalImage" style="width: 23rem; height: 20rem")
                .card-body
                    h4.card-title.text-opacity-75.fw-bold Manage personal finances
                    p.card-text.text-muted Take control of your personal finances with our easy-to-use tools and insightful analytics.
            .card.mx-3.my-4.align-items-center.col-3.pb-1(@click="goLogin" style="cursor: pointer")
                img.invite-image.card-img-top(:src="images.mobileImage" alt="mobileImage" style="width: 23rem; height: 20rem")
                .card-body
                    h4.card-title.text-opacity-75.fw-bold Use on every device
                    p.card-text.text-muted Access your financial data seamlessly across all your devices, anytime, anywhere.
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import personalImage from '@/assets/content-landing/personal.svg'
import mobileImage from '@/assets/content-landing/mobile.svg'
import friendsImage from '@/assets/content-landing/friends.svg'

export default defineComponent({
    name: 'ContentComponent',
    //@ts-ignore
    data() {
        return {
            images: {
                personalImage,
                mobileImage,
                friendsImage,
            },
        }
    },
    methods: {
        goLogin() {
            this.$router.push('/sign-up')
        },
    },
})
</script>

<style scoped lang="scss">
@import "@/styles/styles.scss";

.card {
    min-width: 23rem;
    position: relative;
    transition: transform 0.3s ease-in-out;

    &:hover {
        transform: scale(1.04);
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    &:not(:hover) {
        transition: transform 0.5s ease-in-out;
    }
}

</style>

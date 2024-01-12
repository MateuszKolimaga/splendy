<template lang="pug">
.d-flex.px-4.w-100.align-items-center.justify-content-between.landing-footer.bg-light
    .d-flex.flex-row.w-100
        img(:src="images.logo" alt="Splendy" width="100" height="65")
    .d-flex.flex-row.flex-shrink-1.align-items-center
        .text-muted.flex-end Contact:
        a
            font-awesome-icon.ms-3(:icon="['far', 'envelope']" style="cursor: pointer" @click="openMail")
        a.d-flex.flex-row.align-items-center(href="https://github.com/MateuszKolimaga")
            img.ms-3(:src="images.githubLogo", alt="github", height="17")
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import logo from '../../assets/logo-transparents.svg'
import githubLogo from '../../assets/github-mark.svg'
export default defineComponent({
    name: 'FooterComponent',
    data() {
        return {
            images: {
                logo,
                githubLogo
            },
        }
    },
    methods: {
        openMail() {
            window.location.href = 'mailto:mateusz.kolimaga2@gmail.com';
        },
    },
})
</script>

<style scoped lang="scss">
a, font-awesome-icon {
    &:hover {
        transform: scale(1.1);
    }

    &:not(:hover) {
        transition: transform 0.3s ease-in-out;
    }
}
</style>

    
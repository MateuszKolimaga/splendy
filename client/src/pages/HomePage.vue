<template lang="pug">
main-content
wave-component
content-component
wave-component(:rotate-y="true", :rotate-x="true")
sign-up-row-component
wave-component#wave-footer(:rotate-y="false" :rotate-gradient="true")
footer-component

demo-dialog
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import MainHeaderComponent from '@/components/headers/MainHeaderComponent.vue'
import MainContent from '@/components/landing-page/MainContent.vue'
import WaveComponent from '@/components/landing-page/WaveComponent.vue'
import ContentComponent from '@/components/landing-page/ContentComponent.vue'
import PortableLoginComponent from '@/components/landing-page/PortableLoginComponent.vue'
import SignUpRowComponent from '@/components/landing-page/SignUpRowComponent.vue'
import FooterComponent from '@/components/landing-page/FooterComponent.vue'

export default defineComponent({
    name: 'HomePage',
    components: {
        MainHeaderComponent,
        MainContent,
        WaveComponent,
        ContentComponent,
        PortableLoginComponent,
        SignUpRowComponent,
        FooterComponent,
    },
    mounted() {
        document.body.style.overflow = 'visible'
    },
})
</script>


<style scoped lang="scss">
@import '@/styles/styles.scss';

#wave-footer {
    background-color: white;
}
</style>

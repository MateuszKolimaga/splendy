<template lang="pug">
div.base-image
    img(:src="images.base" alt="base")
    img(:src="images._1" alt="1" :style="getOverlayImageStyle(-9, 43)")
    img(:src="images._2" alt="2" :style="getOverlayImageStyle(5, 58)")
    img(:src="images._2_5" alt="2_5" :style="getOverlayImageStyle(8, 68)")
    img(:src="images._2_6" alt="2_6" :style="getOverlayImageStyle(39, 79)")
    img(:src="images._2_8" alt="2_8" :style="getOverlayImageStyle(42, 66)")
    img(:src="images._3" alt="3" :style="getOverlayImageStyle(50, 64)")
    img(:src="images._3_4" alt="3_4" :style="getOverlayImageStyle(61, 19)")
    img(:src="images._3_6" alt="3_6" :style="getOverlayImageStyle(43, 26)")
    img(:src="images._4" alt="4" :style="getOverlayImageStyle(50, 5)")
    img(:src="images._5" alt="5" :style="getOverlayImageStyle(-7, 14)")
    img(:src="images._6" alt="6" :style="getOverlayImageStyle(-8, 28)")
    img(:src="images._7" alt="7" :style="getOverlayImageStyle(24, 7)")
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import base from '../../assets/landing-reactive/new-0.svg'
import _1 from '../../assets/landing-reactive/1.svg'
import _2 from '../../assets/landing-reactive/2.svg'
import _2_5 from '../../assets/landing-reactive/2-5.svg'
import _2_6 from '../../assets/landing-reactive/2-6.svg'
import _2_8 from '../../assets/landing-reactive/2-8.svg'
import _3 from '../../assets/landing-reactive/3.svg'
import _3_4 from '../../assets/landing-reactive/3-4.svg'
import _3_6 from '../../assets/landing-reactive/3-6.svg'
import _4 from '../../assets/landing-reactive/4.svg'
import _5 from '../../assets/landing-reactive/5.svg'
import _6 from '../../assets/landing-reactive/6.svg'
import _7 from '../../assets/landing-reactive/7.svg'

export default defineComponent({
    name: "FloatingSvgComponent",
    data() {
        return {
            images: {
                base,
                _1, _2, _3, _4, _5, _6, _2_5, _2_6, _2_8, _3_4, _3_6, _7
            },
            mouseX: ref(0),
            mouseY: ref(0),
        }
    }, methods: {
        handleMouseMove(event: { clientX: number; clientY: number; }) {

            this.mouseX = event.clientX / window.innerWidth * 25;
            this.mouseY = event.clientY / window.innerHeight * 25;
        },
        getOverlayImageStyle(topOffset: any, leftOffset: any) {
            const sign = leftOffset % 3 == 1 ? '-' : '+'
            return {
                position: 'absolute',
                top: `calc(${topOffset}% ` + sign + ` ${this.mouseY}px)`,
                left: `calc(${leftOffset}% ` + sign + ` ${this.mouseX}px)`,
            };
        },
    }
});
</script>

<style scoped lang="scss">
@import "@/styles/styles.scss";

.base-image {
    position: relative;
}

</style>
    
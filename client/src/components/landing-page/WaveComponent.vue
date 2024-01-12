<template lang="pug">
div(v-if="!rotateGradient")
    svg(id="wave-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 150" :style="{ transform: `${rotateYStyle} ${rotateXStyle}` }")
        defs
            linearGradient(:id="gradientId" :x1="gradientX1" :x2="gradientX2" :y1="gradientY1" :y2="gradientY2")
                stop(offset="0%" :stop-color="gradientColor1")
                stop(offset="100%" :stop-color="gradientColor2")
        path(:fill="fill" :fill-opacity="fillOpacity" :d="wavePath")
div(v-else)
    svg(id="wave-svgs" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 150" :style="{ transform: `${rotateYStyle} ${rotateXStyle}` }")
        defs
            linearGradient(id="Gradient2")
                stop(offset="0%" :stop-color="gradientColor1")
                stop(offset="100%" :stop-color="gradientColor2")
        path(fill="url('#Gradient2')" :fill-opacity="2" :d="wavePath")
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "WaveComponent",
  props: {
    gradientId: {
      type: String,
      default: "Gradient1",
    },
    gradientX1: {
      type: String,
      default: "1",
    },
    gradientX2: {
      type: String,
      default: "0",
    },
    gradientY1: {
      type: String,
      default: "0",
    },
    gradientY2: {
      type: String,
      default: "0",
    },
    gradientColor1: {
      type: String,
      default: "rgba(203, 244, 227, 1)",
    },
    gradientColor2: {
      type: String,
      default: "rgba(255, 255, 255, 1)",
    },
    fill: {
      type: String,
      default: "url(#Gradient1)",
    },
    fillOpacity: {
      type: String,
      default: "1",
    },
    wavePath: {
      type: String,
      default: "M0,96L80,101.3C160,107,320,117,480,112C640,107,800,85,960,80C1120,75,1280,85,1360,90.7L1440,96L1440,0L1360,0C1280,0,1120,0,960,0C800,0,640,0,480,0C320,0,160,0,80,0L0,0Z",
    },
    rotateY: {
      type: Boolean,
      default: false,
    },
    rotateX: {
      type: Boolean,
      default: false,
    },
    rotateGradient: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    rotateYStyle(): string {
      return this.rotateY ? "rotateY(180deg)" : "";
    },
    rotateXStyle(): string {
      return this.rotateX ? "rotateX(180deg)" : "";
    },
  }
});
</script>

<style scoped>
#wave-svg {
  width: 100%;
  /* background-color: #ffe779; */
}
</style>
  
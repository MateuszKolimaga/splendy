<template lang="pug">
teleport(:to="target")
    #toasts.position-fixed.fixed-top.d-flex.row.row-cols-3
        .toasts-container.d-flex.flex-column.align-items-center(v-for="(toastsInPlacement, index) in toastsGroupedByPlacement" :key="index")
            toast-component(v-for="toast in toastsInPlacement" :key="toast.id" v-bind="{ ...toast }")
</template>

<script lang="ts" setup>
import { useToasts} from "../../composables/useToasts";
//@ts-ignore
import ToastComponent from './ToastComponent.vue'
import { computed } from "vue";

withDefaults(defineProps<{ target?: string }>(), {
    target: "body"
});

const { toasts } = useToasts();

//@ts-ignore
const toastsGroupedByPlacement = computed(() => {
    return [
        [...toasts.value.filter(toast => toast.position === "start")],
        [...toasts.value.filter(toast => toast.position === "center")],
        [...toasts.value.filter(toast => toast.position === "end")],
    ]
})
</script>

<style lang="scss" scoped>
div.position-fixed.fixed-top {
    height: 100%;
    width: 100%;
    pointer-events: none;
}
#toasts {
    z-index: 2000;
    padding: 0;
    margin: 0;
    .toasts-container {
        padding: 0;
        overflow: visible;
        max-height: 50%;
        height: 50%;
    }
}
</style>

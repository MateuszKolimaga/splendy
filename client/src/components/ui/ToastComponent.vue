<template lang="pug">
.toast.position-relative.align-items-center.text-white.border-0.mt-3.py-3.ps-3(ref="toastRef" :class="backgroundClass" role="alert" aria-atomic="true")
    .d-flex
        | {{ message }}
        button.btn-close.btn-close-white.me-2.m-auto(type="button" data-bs-dismiss="toast" aria-label="Close" )
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, PropType, ref } from "vue";
import { ToastData } from "../../composables/useToasts";
import { Toast } from "bootstrap";

export default defineComponent({
    name: "ToastComponent",
    props: {
        duration: {
            type: Number,
            default: 5000
        },
        message: {
            type: String,
            default: ""
        },
        dismiss: {
            type: Function as PropType<ToastData['dismiss']>,
            default: () => {}
        },
        type: {
            type: String as PropType<ToastData['type']>,
            default: "info"
        }
    },
    setup(props) {
        const toastRef = ref();

        const bootstrapToast = ref<Toast | null>(null)

        onMounted(() => {
            bootstrapToast.value = new Toast(toastRef.value, { delay: props.duration });
            toastRef.value.addEventListener('hidden.bs.toast', function () {
                handleDismiss()
            })
            bootstrapToast.value?.show();
        });

        const handleDismiss = () => {
            bootstrapToast.value?.dispose();
            props.dismiss();
        };

        const backgroundClass = computed(() => {
            return `bg-${props.type!}`;
        })

        return {
            backgroundClass,
            toastRef,
            handleDismiss
        };
    }
});
</script>
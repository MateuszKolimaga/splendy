<template lang="pug">
.modal.fade#showDemo(ref="showDemoRef")
    .modal-dialog.modal-dialog-centered.modal-lg
        .modal-content
            .modal-header
                h5.modal-title Demo
                button.btn-close.flex-shrink-1(type="button" data-bs-dismiss="modal" aria-label="Close")
            .modal-body.my-2
                .form-group.my-2
                    video(class="w-100" controls="controls" name="Video Name")
                        source(:src="demoMovie")
            .modal-footer
                button.btn.btn-md.btn-outline-secondary.mx-3(data-bs-dismiss="modal") Close
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { Modal } from 'bootstrap'
import demoMovie from '../../../assets/demo/splendy.mp4'

export default defineComponent({
    name: 'DemoDialog',
    data() {
        return {
            demoMovie
        }
    },
    setup() {
        const showDemo = ref<Modal>()
        const showDemoRef = ref()

        return {
           showDemo,
           showDemoRef,
        }
    },
    methods: {
        closeModal() {
            this.showDemo?.dispose()
            this.$emit('close')
        },
    },
    mounted() {
        this.showDemo = new Modal(this.showDemoRef)
        this.showDemoRef.addEventListener('hidden.bs.modal', () => {
            this.closeModal()
        })
        this.showDemo.show()
    },
})
</script>
        
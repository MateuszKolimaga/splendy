<template lang="pug">
.modal.fade#changeUser(ref="changeUserRef")
    .modal-dialog.modal-dialog-centered
        .modal-content
            .modal-header
                h5.modal-title Update your info
                button.btn-close.flex-shrink-1(@click="closeModal" type="button" aria-label="Close")
            .modal-body.my-2
                .form-group.my-2
                    label(for="firstNameInput") First name
                    input#firstNameInput.form-control(v-model="firstNameInput" type="text") 
                .form-group.my-2
                    label(for="lastNameInput") Second name
                    input#lastNameInput.form-control(v-model="lastNameInput" type="text") 
            .modal-footer
                button.btn.btn-md.btn-outline-secondary.mx-3(@click="closeModal") Cancel
                button.btn.btn-md.btn-primary(@click="executeModal" :disabled="updateButtonDisabled")
                    .text(v-if="!loading") Update
                    .spinner-border.spinner-border-sm(v-else)
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import { Modal } from 'bootstrap'
import { useUserStore } from '@/stores/userStore'

import { User } from '@/pages/split/types/user'
import { storeToRefs } from 'pinia'

export default defineComponent({
    name: 'ChangeUserDialog',
    data() {
        return {
            loading: false
        }
    },
    setup() {
        const changeUser = ref<Modal>()
        const changeUserRef = ref()
        const userStore = useUserStore()
        const { user } = storeToRefs(userStore)
        const firstNameInput = ref(user.value?.firstName)
        const lastNameInput = ref(user.value?.lastName)

        const updateButtonDisabled = computed(() => {
            return !firstNameInput.value?.trim() || !lastNameInput.value?.trim();
        });

        return {
            changeUser,
            changeUserRef,
            userStore,
            user,
            firstNameInput,
            lastNameInput,
            updateButtonDisabled
        }
    },
    methods: {
        async executeModal() {
            if (
                this.firstNameInput !== this.user?.firstName ||
                this.lastNameInput !== this.user?.lastName 
            ) {
                this.loading = true
                const newUser = User.copyWith(this.user!, {
                    firstName: this.firstNameInput,
                    lastName: this.lastNameInput,
                })
                await this.userStore.updateUser(newUser)
                this.loading = false
                this.$emit('execute', newUser)
                this.closeModal()
            } else {
                this.closeModal()
            }
        },
        closeModal() {
            this.changeUser?.dispose()
            this.$emit('close')
        },
    },
    mounted() {
        this.changeUser = new Modal(this.changeUserRef)
        this.changeUserRef.addEventListener('hidden.bs.modal', () => {
            this.closeModal()
        })
        this.changeUser.show()
    },
})
</script>
    
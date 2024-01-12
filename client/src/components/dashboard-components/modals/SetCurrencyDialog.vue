<template lang="pug">
.modal.fade#changeUser(ref="changeUserRef")
    .modal-dialog.modal-dialog-centered
        .modal-content
            .modal-header
                h5.modal-title Set your currency first
                button.btn-close.flex-shrink-1(@click="closeModal" type="button" aria-label="Close")
            .modal-body.my-2
                .form-group.my-2
                    label.my-1(for="currencyDropdown") Currency:
                    select.form-control(v-model="currentCurrency") 
                        option(v-for="curr in currencies" :key="curr" :value="curr") {{  curr }}
            .modal-footer
                button.btn.btn-md.btn-primary(@click="executeModal" :disabled="updateButtonDisabled")
                    .text(v-if="!loading") Update
                    .spinner-border.spinner-border-sm(v-else)
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import { Modal } from 'bootstrap'
import { useUserStore } from '@/stores/userStore'
import currencies from '@/pages/dashboard/models/currencies'
import { User } from '@/pages/split/types/user'
import { storeToRefs } from 'pinia'
import { useToasts } from '@/composables/useToasts'

export default defineComponent({
    name: 'SetCurrencyDialog',
    data() {
        return {
            currencies,
            loading: false
        }
    },
    setup() {
        const changeUser = ref<Modal>()
        const changeUserRef = ref()
        const userStore = useUserStore()
        const { user } = storeToRefs(userStore)
        const currentCurrency = ref(user.value?.currency)

        const updateButtonDisabled = computed(() => {
            return !currentCurrency.value?.trim();
        });
        const { addToast } = useToasts()

        return {
            changeUser,
            changeUserRef,
            userStore,
            user,
            currentCurrency,
            updateButtonDisabled,
            addToast
        }
    },
    methods: {
        async executeModal() {
            if (
                this.currentCurrency != this.user?.currency
            ) {
                this.loading = true
                const newUser = User.copyWith(this.user!, {
                    currency: this.currentCurrency,
                })
                await this.userStore.updateUser(newUser)
                this.loading = false
                this.$emit('execute', newUser)
                this.closeModal()
            } else {
                this.addToast({
                    message: 'Your currency is set to ' + this.currentCurrency,
                    type: 'info',
                })
                this.$emit('execute', this.user!)
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
        
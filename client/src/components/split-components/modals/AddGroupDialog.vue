<template lang="pug">
.modal#addGroup(ref="addGroupRef")
    .modal-dialog.modal-dialog-centered
     .modal-content
        .modal-header
            h5.modal-title Create a group
            button.btn-close.flex-shrink-1(@click="closeModal" type="button" aria-label="Close")
        .modal-body.my-3
            form
            .form-group.my-1
                label(for="category") Group name:
                input.form-control(v-model="form.name" type="text" id="description")
            .form-group.my-1
                    label(for="currencyDropdown") Group currency:
                    select#currencyDropdown.form-control(v-model="currentCurrency") 
                        option(v-for="curr in currencies" :key="curr" :value="curr") {{  curr }}
        .modal-footer
            button.btn.btn-md.btn-outline-secondary.mx-3(@click="closeModal") Cancel
            button.btn.btn-md.btn-primary(@click="createGroup")
                .text(v-if="!loading") Create
                span.spinner-border.spinner-border-sm(v-else, role="status", aria-hidden="true")
</template>


<script lang="ts">
//TODO: Add attachment to dialog
import { useSocialStore } from '@/stores/socialStore';
import { useUserStore } from '@/stores/userStore';
import { Modal } from 'bootstrap';
import { defineComponent, reactive, ref } from 'vue';
import currencies from '@/pages/dashboard/models/currencies'

export default defineComponent({
    name: "AddGroupDialog",
    setup() {
        const { user } = useUserStore()
        const socialStore = useSocialStore()
        const form = reactive({
            name: "",
            members: [
                user!.id
            ]
        });
        const addGroup = ref<Modal>()
        const addGroupRef = ref()
        const loading = ref(false)
        const currentCurrency = ref(user!.currency)

        return {
            form,
            addGroup,
            addGroupRef,
            socialStore,
            loading,
            currentCurrency,
            currencies
        }
    }, mounted() {
      this.addGroup = new Modal(this.addGroupRef)
      this.addGroupRef.addEventListener('hidden.bs.modal', () => {
          this.closeModal()
      })
      this.addGroup.show();
    },
    methods: {
            async createGroup() {
            this.loading = true
            const response = await this.socialStore.createTeam(this.form)
            this.$router.push({ name: 'SplitDashboard', params: { teamId: response.message.id } });
            this.loading = false
            this.$emit("close");
            this.addGroup?.dispose()
        },
        closeModal() {
            this.addGroup?.dispose()
            this.$emit("close");
        },
    },
    });
</script>

<style scoped>
.form-control {
    overflow-y: auto;
}
</style>
    
<template lang="pug">
.modal#addGroupExpense(ref="addGroupExpenseRef")
  .modal-dialog.modal-dialog-centered
      .modal-content
        .modal-header
          h5#operationDialogLabel.modal-title Add an expense
          button.btn-close.flex-shrink-1(@click="closeModal" type="button" aria-label="Close")
        .modal-body.mb-1
          form
            .form-group.my-2.d-flex.flex-column.gap-1
              label(for="amount") Amount:
              .amount-container
                .amount-question
                  input.form-control.mx-1(v-model="form.value" type="number" id="amount")
                  .currency-wrapper.d-flex.flex-column.justify-content-center
                      label.form-label(v-if="!currencyEditable", @click="currencyEditable = false") {{ form.currency }}
                      select(v-else, v-model="form.currency", @change="currencyEditable = false")
                        option(v-for="currency in currencies", :key="currency") {{ currency }}
            .form-group.my-2.d-flex.flex-column.gap-1
              label(for="category") Description:
              input.form-control(v-model="form.description" type="text" id="description")
            hr
            .form-group.my-2.d-flex.flex-column.gap-1.mt-3
                label Members:
                .member-checkboxes
                    input.form-check-input.me-2(type="checkbox" disabled="true" checked="true")
                    label.custom-member {{ user.firstName }} {{ user.lastName }}
                    template(v-for="(member, memberIndex) in membersWithoutUser" :key="member.id")
                        input.form-check-input.me-2(type="checkbox" v-model="form.to_users" :value="member.id")
                        label.custom-member {{ member.firstName }} {{ member.lastName }}
            .form-group.my-2.d-flex.flex-column.gap-1
                label(for="options") Options:
                .d-flex.flex-row
                  input.form-check-input.me-2(type="checkbox" id="splitEqually" disabled="true" checked="true") 
                  label.split-equally(for="splitEqually") Split equally
        .modal-footer
          button.btn.btn-md.btn-outline-secondary.mx-3(@click="closeModal") Cancel
          button.btn.btn-md.btn-primary(@click="saveOperation")
            .text(v-if="!loading") Save
            .spinner-border.spinner-border-sm(v-else)
</template>

<script lang="ts">
//TODO: Add attachment to dialog
import { PropType, defineComponent, reactive, ref } from 'vue'
import { Modal } from 'bootstrap'
import { User } from '@/pages/split/types/user'
import { useUserStore } from '@/stores/userStore'
import { storeToRefs } from 'pinia'
import { useTeamStore } from '@/stores/teamStore'
import currencies from '@/pages/dashboard/models/currencies'
import GroupOperation from '@/pages/split/models/groupOperations'
import { useToasts } from '@/composables/useToasts'

export default defineComponent({
    name: 'AddGroupExpenseDialog',
    props: {
        groupId: Number,
        members: Object as PropType<User[]>,
    },
    setup(props) {
        const currencyEditable = ref(false)
        const userStore = useUserStore()
        const teamStore = useTeamStore()
        const { user } = storeToRefs(userStore)
        const { currency, members } = storeToRefs(teamStore)
        const form = reactive(new GroupOperation(+user.value!.id, props.groupId!, currency.value))
        const addGroupExpense = ref<Modal>()
        const addGroupExpenseRef = ref()
        const loading = ref(false)
        const { addToast } = useToasts()
        return {
            currencyEditable,
            currencies: currencies,
            form,
            user,
            members,
            addGroupExpense,
            addGroupExpenseRef,
            teamStore,
            loading,
            addToast
        }
    },
    mounted() {
        this.addGroupExpense = new Modal(this.addGroupExpenseRef)
        this.addGroupExpenseRef.addEventListener('hidden.bs.modal', () => {
            this.closeModal()
        })
        this.addGroupExpense.show()
    },
    methods: {
        async saveOperation() {
          this.form!.date = new Date()
          if (this.form!.to_users.length == 0) {
            this.addToast({ message: 'You have to select at least one member', type: 'danger'})
            return
          } else if (this.form!.value == 0) {
            this.addToast({ message: 'You have to enter a proper value', type: 'danger'})
            return
          } else if (this.form!.description == "") {
            this.addToast({ message: 'You have to enter a description', type: 'danger'})
            return
          }
          this.form!.to_users.push(+this.user!.id)
          this.form!.users_settled.push(+this.user!.id)
          this.loading = true
          await this.teamStore.addExpense(this.form)
          this.loading = false
          this.$emit('execute')
          this.closeModal()
        },
        closeModal() {
            this.addGroupExpense?.dispose()
            this.$emit('close')
        },
    },
    computed: {
        membersWithoutUser() {
            //@ts-ignore
            return this.members.filter((member) => member.id !== this.user?.id)
        },
    },
})
</script>

<style scoped>
.custom-member {
    margin-right: 0.5rem;
}

.amount-question {
    display: flex;
    justify-content: space-between;
    margin-left: -3px;
}

.currency-wrapper {
    display: flex;
    justify-content: flex-start;
    align-items: flex-end;
    margin: 0px 10px 0px 5px;
}

.form-control {
    overflow-y: auto;
}

.split-equally {
    margin-right: 0.5rem;
}

hr {
    margin-top: 1rem;
    margin-bottom: 1rem;
    border: 0;
    border-top: 1px solid rgba(0, 0, 0, 0.5);
}
</style>

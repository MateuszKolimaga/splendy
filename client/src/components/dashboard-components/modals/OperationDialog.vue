<template lang="pug">
.modal.fade#showOperation(ref="showOperationRef")
  .modal-dialog.modal-dialog-centered(role="document")
      .modal-content
        .modal-header
          h5#operationDialogLabel.modal-title Add an {{ operationName }}
          button.btn-close.flex-shrink-1(@click="closeModal" type="button" aria-label="Close")
        .modal-body.my-2
          form
            .form-group.my-1
              label(for="amount") Amount:
              .amount-container
                .amount-question
                  input.form-control.mx-1(v-model="form.value" type="number" id="amount")
                  .currency-wrapper.d-flex.flex-column.justify-content-center
                      label.form-label(v-if="!currencyEditable", @click="currencyEditable = false") {{ form.currency }}
                      select(v-else, v-model="form.currency", @change="currencyEditable = false")
                        option(v-for="currency in currencies", :key="currency") {{ currency }}
            .form-group.my-1
              label(for="description") Description:
              input.form-control(v-model="form.description" type="text" id="description")
            .form-group.my-1
              label(for="category") Category:
              select.form-control(v-model="form.category" id="category")
                option(v-for="category in categories" :key="category") {{ category.charAt(0).toUpperCase() + category.slice(1) }}
            .form-group-my-1
              label(for="date") Date:
              Datepicker(id="date" v-model="form.date" :max-date="new Date()")
        .modal-footer
          button.btn.btn-md.btn-outline-secondary.mx-3(@click="closeModal") Cancel
          button.btn.btn-md.btn-primary( @click="saveOperation", :disabled="isLoading") 
            .text(v-if="!isLoading") Save
            span.spinner-border.spinner-border-sm(v-else, role="status", aria-hidden="true")
            
</template>


<script lang="ts">
import { Operation } from '@/pages/dashboard/models/operation';
import { expenseCategories, incomeCategories } from '@/pages/dashboard/models/operation-infos';
import { User } from '@/pages/split/types/user';
import { usePersonalStore } from '@/stores/personalStore';
import { Modal } from 'bootstrap';
import { PropType, defineComponent, ref } from 'vue';
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

export default defineComponent({
    name: "OperationDialog",
    components: {
      Datepicker
    },
    props: {
      user: Object as PropType<User>,
      currencies: Array<String>,
      operationName: String as PropType<"income" | "expense">
    },
    data() {
      return {
        isLoading: false
      }
    },
    setup(props) {
      const currencyEditable = ref(false);
      const showOperation = ref<Modal>()
      const showOperationRef = ref()
      const personalStore = usePersonalStore()
      const categories = props.operationName == 'expense' ? expenseCategories : incomeCategories;
      const form = ref(new Operation(props.user!.id.toString(), props.user!.currency.toString(), new Date()))
      return {
        currencyEditable,
        currencies: props.currencies,
        categories,
        showOperation,
        showOperationRef,
        form,
        personalStore
      }
    },
    methods: {
      async saveOperation() {
        this.form!.category = this.form!.category?.toLowerCase()
        this.isLoading = true
        const response = await this.personalStore.addTransaction(
                this.form,
                this.operationName?.valueOf() + 's' as "incomes" | "expenses"
        )
        this.isLoading = false
        if (response.success == true) {
          this.closeModal()
        }
      },
      closeModal() {
        this.showOperation?.dispose()
        this.$emit("close");
      },
    },
    mounted() {
      this.showOperation = new Modal(this.showOperationRef)
      this.showOperationRef.addEventListener('hidden.bs.modal', () => {
          this.closeModal()
      })
      this.showOperation.show();
    },
  });
</script>

<style scoped>
.operation-dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 25px;
  border: 1px solid grey;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  z-index: 1000;
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
</style>
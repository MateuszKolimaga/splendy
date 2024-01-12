<template lang="pug">
.dashboard.container-fluid.gx-0
  .row.d-flex.gx-0
    .operations-panel.fixed-h.col-5.bg-light.p-0.border-end.d-flex.flex-column
        .panel-header.px-4.pb-4.pt-2.bg-light.border.border-end-0
          .d-flex.align-items-center.p-2.justify-content-center.mb-1
              .date-choose-container(data-bs-toggle="dropdown")
                .dropdown#date-choose(style="cursor: pointer")
                  .w-100.fw-bold.me-1.d-flex.flex-row.align-items-center
                    .header(style="font-size: 1rem") {{ currentDateSpanCategory }}
                    font-awesome-icon.px-1(icon="chevron-down")
                .dropdown-menu#dropdown-menu-date
                    .dropdown-item.text-center.fw-bold(v-for="category in dateSpanCategories.filter(category => category != currentDateSpanCategory)", :key="category", @click="changeCurrentDateCategory(category)", style="cursor: pointer") 
                      | {{ category }}
          .d-flex.align-items-center
              .flex-grow-1.fw-bold
                .card.py-2.px-3.pointer(data-bs-toggle="dropdown")
                  .d-flex.dropdown
                    .w-100
                      | {{ IsIncome ? 'Incomes': 'Expenses' }}
                    .flex-shrink-1
                      font-awesome-icon(icon="chevron-down")
                  .dropdown-menu.w-100
                    .dropdown-item.fw-bold(@click="IsIncome = !IsIncome") {{ IsIncome ?  'Expenses' : 'Incomes' }}
              .ms-3
                button.btn.btn-primary(@click="openOperationDialog")
                  font-awesome-icon(icon="plus" style={'color': 'white'})
              .mx-3(title="Sort operations by value")
                font-awesome-icon(icon="sort", @click="sortOperations", style="cursor: pointer")
              .me-1(v-if="sortedClicked" @click="refreshSorting" style="cursor: pointer" title="Refresh sorting / Sort by date")
                font-awesome-icon(icon="refresh")
        .panel-body.overflow-y-auto.flex-grow-1.pt-3(v-if="showOperationsSpinner")
          .d-flex.flex-column.align-items-center.justify-content-center.h-100
            .spinner-border
        .panel-body.overflow-y-auto.flex-grow-1.py-2.ps-1(v-else)
          template(v-if="operations.length > 0" v-for="(operation, oIndex) in operations", :key="operation.id")
            OperationTile(:operation="operation" @delete-operation="deleteOperation")
            .operations-footer.ps-3.pe-4.my-2(v-if="nextOperationWithDifferentDate(operation, oIndex)")
                .d-flex.flex-row.justify-content-center.align-items-center
                    .w-100.border-top
          .d-flex.flex-column.align-items-center.justify-content-center.h-75(v-else)
            .text-muted No operations yet
            .text-muted.mt-2(@click="openOperationDialog" style="cursor: pointer") Add your first operation
    .central-panel.col-7.bg-light.fixed-h(v-if="!showOperationsSpinner")
        .row.border.border-start-0.border-bottom-0.gx-0.h-100.overflow-hidden
          .col-11.d-flex.flex-column.justify-content-between.h-100
            .d-flex.flex-column.justify-content-center.py-4.flex-fill
              .chart-area.h-100(v-if="legends.length > 0")
                doughnut-chart-component(v-if="showDoughnutChart" ref="doughnutChartComponent", :currency="user.currency", :data-type="IsIncome ? 'incomes': 'expenses'")
                template(v-if="!showDoughnutChart")
                  .d-flex.flex-row.justify-content-center
                    small.text-muted.transition-opacity(:style="showLineChartInstructions ? 'opacity: 1;' : 'opacity: 0;'") Hint: Click below on any category to add or remove it from the chart
                  line-chart-component(v-if="!showDoughnutChart" ref="lineChartComponent", :currency="user.currency", :data-type="IsIncome ? 'incomes': 'expenses'")
              .d-flex.flex-column.align-items-center.justify-content-center.h-100(v-else)
                font-awesome-icon.text-opacity-75.text-muted.mt-5(icon="magnifying-glass-chart" @click="openOperationDialog" style="cursor: pointer")
                .text-muted.mt-2(@click="openOperationDialog" style="cursor: pointer") Add operations to see the graph
            .legend.border-top.d-flex.flex-column.justify-content-center.flex-shrink-1.py-4.overflow-hidden(v-if="legends.length > 0")
              .d-flex.flex-row.justify-content-center.align-items-center.flex-wrap.gap-2
                .card.d-flex.flex-row.align-items-center.py-1.px-2.gap-2(v-for="legend in legends", :key="legend.category")
                  .div.fw-bold.rounded.px-1(:style="{'background-color': legend.color, 'color': 'white' }") {{ legend.percentage }}
                  .flex-grow-1.d-flex.flex-row.gap-2
                    .div {{ legend.category }} 
                    .fw-bold {{ legend.value }}
          .col-1.border-start.d-flex.flex-column.align-items-center
            a(href="#" @click="tryShowDoughnutChart").mt-4
              font-awesome-icon(icon="chart-pie", style={'color': 'grey'})
            a(href="#" @click="tryShowLineChart").mt-4
              font-awesome-icon(icon="chart-line", style={'color': 'grey'})
    .central-panel.col-7.bg-light.fixed-h(v-else)
      .row.border.border-start-0.border-bottom-0.gx-0.h-100.overflow-hidden
        .d-flex.flex-column.align-items-center.justify-content-center.h-100
          .spinner-border.mt-5

SetCurrencyDialog(v-if="isCurrencyDialogOpen && !isCurrencySet" :user="user" @execute="closeCurrencyDialog" @close="isCurrencyDialogOpen=false" ref="currencyDialogRef")
OperationDialog(v-if="isOperationDialogOpen" :user="user" :currencies="currencies" :operationName="IsIncome ? 'income': 'expense'" @close="isOperationDialogOpen = false" ref="operationDialogRef")
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue'
import DoughnutChartComponent from '@/components/chart/pie/ChartComponent.vue'
import LineChartComponent from '@/components/chart/line/ChartComponent.vue'
import { operationCategoryInfos } from './models/operation-infos'
import OperationTile from '@/components/dashboard-components/OperationTile.vue'
import OperationDialog from '@/components/dashboard-components/modals/OperationDialog.vue'
import SetCurrencyDialog from '@/components/dashboard-components/modals/SetCurrencyDialog.vue'
import currencies from './models/currencies'
import { useUserStore } from '@/stores/userStore'
import { storeToRefs } from 'pinia'
import { usePersonalStore } from '@/stores/personalStore'
import { Operation } from '@/pages/dashboard/models/operation'
import { dateSpanCategories } from '@/utils/const'
import { DateSpanCategoryType } from './types/operation.types'
import { useToasts } from '@/composables/useToasts'

export default defineComponent({
    name: 'MainDashboardPage',
    components: {
        DoughnutChartComponent,
        LineChartComponent,
        OperationTile,
        OperationDialog,
        SetCurrencyDialog,
    },
    setup() {
        const userStore = useUserStore()
        const { user } = storeToRefs(userStore)
        const personalStore = usePersonalStore()
        const { incomes, expenses, incomeLegends, expenseLegends } =
            storeToRefs(personalStore)
        const IsIncome = ref(false)
        const currentDateSpanCategory = 'All'
        const isCurrencySet = ref(false)
        const legends = computed(() => {
            if (IsIncome.value) return incomeLegends.value
            else return expenseLegends.value
        })
        const noData = IsIncome.value
            ? expenses.value.length == 0
            : incomes.value.length == 0
        const showOperationsSpinner = ref(noData)
        personalStore.fetchAll().then(() => {
            showOperationsSpinner.value = false
        })
        const isOperationDialogOpen = ref(false)
        const isCurrencyDialogOpen = ref(false)

        const currencyEditable = ref(false)
        const doughnutChartComponent = ref<InstanceType<
            typeof DoughnutChartComponent
        > | null>(null)
        const lineChartComponent = ref<InstanceType<
            typeof LineChartComponent
        > | null>(null)
        const showDoughnutChart = ref(true)
        const operationDialogRef = ref<InstanceType<
            typeof OperationDialog
        > | null>(null)
        const currencyDialogRef = ref<InstanceType<
            typeof SetCurrencyDialog
        > | null>(null)
        const operationsSorted = ref(false)
        const sortedClicked = ref(false)
        const showLineChartInstructions = ref(true)
        const { addToast } = useToasts()

        return {
            currencyEditable,
            currencies,
            IsIncome,
            doughnutChartComponent,
            lineChartComponent,
            operationCategoryInfos,
            isOperationDialogOpen,
            showOperationsSpinner,
            legends,
            operationDialogRef,
            user,
            personalStore,
            incomes,
            expenses,
            dateSpanCategories,
            currentDateSpanCategory,
            operationsSorted,
            sortedClicked,
            showDoughnutChart,
            showLineChartInstructions,
            currencyDialogRef,
            isCurrencyDialogOpen,
            isCurrencySet,
            addToast,
        }
    },
    methods: {
        deleteOperation(form: Operation) {
            this.personalStore.deleteOperation(
                form,
                this.IsIncome ? 'incomes' : 'expenses'
            )
        },
        closeCurrencyDialog() {
            this.isCurrencyDialogOpen = false
            this.isCurrencySet = true
            this.isOperationDialogOpen = true
        },
        openOperationDialog() {
            if (this.incomes.length == 0 && this.expenses.length == 0 && !this.isCurrencySet) {
                this.isCurrencyDialogOpen = true
                return
            }
            this.isOperationDialogOpen = true
        },
        closeOperationDialog() {
            this.isOperationDialogOpen = false
            this.operationDialogRef?.closeModal()
        },
        convertDateSpanCategoryToDays(category: DateSpanCategoryType) {
            switch (category) {
                case 'Last week':
                    return 7
                case 'Last month':
                    return 30
                case 'Last year':
                    return 365
                case 'All':
                    return 10000
            }
        },
        changeCurrentDateCategory(category: DateSpanCategoryType) {
            this.currentDateSpanCategory = category
            this.showOperationsSpinner = true
            this.personalStore
                .fetchAll(this.convertDateSpanCategoryToDays(category))
                .then(() => {
                    this.showOperationsSpinner = false
                })
        },
        sortOperations() {
            this.sortedClicked = true
            this.personalStore.sortOperations(this.operationsSorted)
            this.operationsSorted = !this.operationsSorted
        },
        refreshSorting() {
            this.sortedClicked = false
            const days = this.convertDateSpanCategoryToDays(
                this.currentDateSpanCategory as DateSpanCategoryType
            )
            this.personalStore.fetchAll(days).then(() => {
                this.showOperationsSpinner = false
            })
        },
        tryShowDoughnutChart() {
            this.showDoughnutChart = true
        },
        tryShowLineChart() {
            if (this.hasMultipleDays()) {
                this.showDoughnutChart = false
                setTimeout(() => {
                    this.showLineChartInstructions = false
                }, 6000)
            } else {
                this.addToast({
                    message:
                        'You have to have at least two operations in different days to see the line chart',
                    type: 'warning',
                })
            }
        },
        hasMultipleDays() {
            const uniqueDays = new Set()
            for (const operation of this.operations) {
                //@ts-ignore
                const date = new Date(operation.date)
                const day = date.getDate()
                uniqueDays.add(day)
                if (uniqueDays.size >= 2) {
                    return true
                }
            }
            return false
        },
        nextOperationWithDifferentDate(operation: any, oIndex: number) {
            if (oIndex == this.operations.length - 1) return false
            const nextOperation = this.operations[oIndex + 1]
            //@ts-ignore
            const operationDate = new Date(operation.date)
            //@ts-ignore
            const nextOperationDate = new Date(nextOperation.date)
            return (
                operationDate.getDate() != nextOperationDate.getDate() ||
                operationDate.getMonth() != nextOperationDate.getMonth() ||
                operationDate.getFullYear() != nextOperationDate.getFullYear()
            )
        },
    },
    computed: {
        operations() {
            if (this.IsIncome) return this.incomes
            else return this.expenses
        },
    },
})
</script>

<style scoped lang="scss">
.legend-tag {
    padding: 0.4rem;
}

#date-choose:hover {
    background-color: #e9ecef;
}

#dropdown-menu-date {
    margin-left: -2.7rem !important;
}

.transition-opacity {
    transition: opacity 1s ease;
}
</style>

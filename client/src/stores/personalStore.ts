//@ts-nocheck
import api from '@/common/api'
import {
    expenseOperationCategoryInfos,
    incomeOperationCategoryInfos,
} from '@/pages/dashboard/models/operation-infos'
import { groupBy } from 'lodash'
import { defineStore } from 'pinia'
import { useUserStore } from './userStore'
import { useToasts } from '@/composables/useToasts'

const { addToast } = useToasts()
export const usePersonalStore = defineStore('personal', {
    state: () => ({
        expenses: [],
        incomes: [],
        incomeLegends: [],
        expenseLegends: [],
    }),
    actions: {
        async fetchAll(days?: number) {
            await this.fetchExpenses(days)
            await this.fetchIncomes(days)
            this.fetchLegends()
        },
        async fetchExpenses(days?: number) {
            const endpoint = days ? `personal/expenses?days=${days}` : `personal/expenses`
            const response = await api.fetch(endpoint)
            this.expenses = response.data.results
            return { success: true }
        },
        async fetchIncomes(days?: number) {
            const endpoint = days ? `personal/incomes?days=${days}` : `personal/incomes`
            const response = await api.fetch(endpoint)
            this.incomes = response.data.results
            return { success: true }
        },
        fetchLegends() {
            const expensesByCategory = groupBy(this.expenses, 'category')
            const expensesAllCosts = this.expenses.reduce((total, op) => total + op.value, 0)
            const incomesByCategory = groupBy(this.incomes, 'category')
            const incomesAllCosts = this.incomes.reduce((total, op) => total + op.value, 0)
            const currency = useUserStore().user?.currency
            //@ts-ignore
            this.expenseLegends = Object.keys(expensesByCategory).map(
                (category) => {
                    const categoryValue = expensesByCategory[category].reduce(
                        //@ts-ignore
                        (total, op) => total + op.value,
                        0
                    )
                    return {
                        category:
                            category.charAt(0).toUpperCase() +
                            category.slice(1),
                        value:
                            categoryValue.toFixed(2) +
                            ' ' +
                            currency,
                        //@ts-ignore
                        color: expenseOperationCategoryInfos[category].color,
                        percentage: `${(100 * (categoryValue/expensesAllCosts)).toFixed(1)} %`
                    }
                }
            )
            //@ts-ignore
            this.incomeLegends = Object.keys(incomesByCategory).map(
                (category) => {
                    const categoryValue = incomesByCategory[category].reduce(
                        //@ts-ignore
                        (total, op) => total + op.value,
                        0
                    )
                    return {
                        category:
                            category.charAt(0).toUpperCase() +
                            category.slice(1),
                        value: categoryValue.toFixed(2) +
                        ' ' +
                        currency,
                        //@ts-ignore
                        color: incomeOperationCategoryInfos[category].color,
                        percentage: `${(100 * (categoryValue/incomesAllCosts)).toFixed(1)} %`
                    }
                }
            )
            this.expenseLegends.sort((a, b) => parseFloat(b.percentage) - parseFloat(a.percentage))
            this.incomeLegends.sort((a, b) => parseFloat(b.percentage) - parseFloat(a.percentage))
        },
        async unsetPersonal() {
            this.expenses = []
            this.incomes = []
            this.expenseLegends = []
            this.incomeLegends = []
        },
        async addTransaction(
            transaction: any,
            endpoint: 'expenses' | 'incomes'
        ) {
            const response = await api.fetch(`personal/${endpoint}`, {
                method: 'POST',
                body: JSON.stringify(transaction),
            })
            if (response.status == 201) {
                if (endpoint === 'expenses') {
                    await this.fetchExpenses()
                } else if (endpoint === 'incomes') {
                    await this.fetchIncomes()
                }
                this.fetchLegends()
                // addToast({ message: 'Operation added', type: 'success' })
                return {
                    success: true
                }
            }
            addToast({ message: 'Failed to add operation', type: 'danger' })
            return { success: false }
        },
        async deleteOperation(operation: any, endpoint: 'expenses' | 'incomes'){
            const response = await api.fetch(`personal/${endpoint}/${operation.id}`, {
                method: 'DELETE',
            })
            if (response.status == 204) {
                if (endpoint === 'expenses') {
                    await this.fetchExpenses()
                } else if (endpoint === 'incomes') {
                    await this.fetchIncomes()
                }
                this.fetchLegends()
                return {
                    success: true
                }
            }
            return { success: false }

        },
        sortOperations(undo: boolean) {
            if (undo) {
                this.expenses.sort((a, b) => b.value - a.value)
                this.incomes.sort((a, b) => b.value - a.value)
            } else {
                this.expenses.sort((a, b) => a.value - b.value)
                this.incomes.sort((a, b) => a.value - b.value)
            }
        }
    },
})

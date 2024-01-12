<template lang="pug">
Line.p-4.mt-4(:data="data" :options="options")
</template>

<script lang="ts">
import {
    Chart as ChartJS,
    LineElement,
    CategoryScale,
    registerables,
} from 'chart.js'
import { Line } from 'vue-chartjs'
import { PropType, computed, defineComponent } from 'vue'
import { convertOperationsToDatasetToChartData } from './lineUtils'
import { usePersonalStore } from '@/stores/personalStore'
import { storeToRefs } from 'pinia'

ChartJS.defaults.backgroundColor = '#FFA800'
ChartJS.register(CategoryScale, LineElement, ...registerables)

export default defineComponent({
    name: 'LineChartComponent',
    components: {
        Line,
    },
    props: {
        currency: String,
        dataType: String as PropType<'expenses' | 'incomes'>,
    },
    setup(props) {
        const dataType = computed(() => props.dataType)
        const personalStore = usePersonalStore()
        const { incomes, expenses } = storeToRefs(personalStore)
        const data = computed(() => {
            const operations =
                dataType.value == 'expenses' ? expenses.value : incomes.value
            return convertOperationsToDatasetToChartData(
                JSON.parse(JSON.stringify(operations)),
                dataType.value!
            )
        })
        const options = {
            elements: {
                line: {
                    borderWidth: 2,
                    tension: 0.3,
                },
                point: {
                    radius: 2,
                    hitRadius: 10,
                    hoverRadius: 4,
                },
            },
            scales: {
                x: {
                    grid: {
                        display: false,
                    },
                },
                y: {
                    grid: {
                        display: true,
                    },
                },
            },
            plugins: {
                legend: {
                    display: true,
                },
            },
        }

        return {
            data,
            options,
        }
    },
})
</script>

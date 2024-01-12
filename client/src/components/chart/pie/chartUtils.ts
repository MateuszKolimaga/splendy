import { groupBy, mapValues } from 'lodash'
import { ChartData } from 'chart.js'
import { OperationCategoryInfo } from '@/pages/dashboard/types/operation.types'
import {
    expenseOperationCategoryInfos,
    incomeOperationCategoryInfos,
} from '@/pages/dashboard/models/operation-infos'

export function convertOperationsToDatasetToChartData(
    operations: Array<{ category: string; value: number }>,
    category: 'incomes' | 'expenses',

) {
    const sums = processOperations(operations)
    const colorMap =
        category === 'incomes'
            ? incomeOperationCategoryInfos
            : expenseOperationCategoryInfos
    const chartData = createChartData(sums, colorMap)
    return chartData
}

function processOperations(
    operations: Array<{ category: string; value: number }>
) {
    const grouped = groupBy(operations, 'category')
    const sums = mapValues(grouped, (ops) =>
        ops.reduce((total, op) => total + Math.abs(op.value), 0)
    )
    return sums
}

function createChartData(
    sums: Record<string, number>,
    colorMap: Record<string, OperationCategoryInfo>
): ChartData<'doughnut', number[], unknown> {
    const labels = Object.keys(sums)
    const data = Object.values(sums)
    const backgroundColor = labels.map((label) => colorMap[label].color)
    return {
        labels,
        datasets: [
            {
                data,
                backgroundColor,
                borderWidth: 0.2,
            },
        ],
    }
}

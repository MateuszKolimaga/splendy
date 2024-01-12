//@ts-nocheck
import { expenseOperationCategoryInfos, incomeOperationCategoryInfos } from '@/pages/dashboard/models/operation-infos';
import { groupBy, mapValues } from 'lodash';

export function convertOperationsToDatasetToChartData(operations, dataType) {
    operations.sort((a, b) => new Date(a.date) - new Date(b.date));

    const operationsByCategory = groupBy(operations, 'category');

    const sortedOperationsByCategory = mapValues(operationsByCategory, operations => 
        operations.sort((a, b) => new Date(a.date) - new Date(b.date))
    );

    const xAxisLabels = Array.from(new Set(operations.map(operation => {
        const date = new Date(operation.date);
        return `${date.getDate()}/${date.getMonth()+1}`;
    })));

    const plotLabels = Object.keys(sortedOperationsByCategory)
    const colorMap = dataType === 'incomes' ? incomeOperationCategoryInfos : expenseOperationCategoryInfos

    const datasets = Object.entries(sortedOperationsByCategory).map(([category, operations]) => {
        const data = xAxisLabels.map(label => {
            const operation = operations.find(op => {
                const date = new Date(op.date);
                return `${date.getDate()}/${date.getMonth()+1}` === label;
            });
            return operation ? operation.value : 0;
        });

        return {
            label: category,
            backgroundColor: colorMap[category].plotColor,
            borderColor: colorMap[category].color,
            fill: true,
            data,
            // other dataset properties
        };
    });

    return {
        labels: xAxisLabels,
        datasets
    };
}
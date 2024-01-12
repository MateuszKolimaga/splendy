import { OperationCategoryInfo } from "../types/operation.types";

function createOperationCategoryInfos<
  T extends Record<string, OperationCategoryInfo>
>(obj: T) {
  return obj;
}

export const expenseOperationCategoryInfos = createOperationCategoryInfos({
  food: {
    color: "#FCD78D" ,
    plotColor: 'rgba(252, 215, 141, 0.5)'
  },
  transportation: {
    color: "#182248",
    plotColor: "rgba(24, 34, 72, 0.5)"
  },
  utilities: {
    color: "#D1495B",
    plotColor: "rgba(209, 73, 91, 0.5)"
  },
  entertainment: {
    color: "#EB9E2A",
    plotColor: "rgba(235, 158, 42, 0.5)"
  },
  other: {
    color: "#BA9B8D",
    plotColor: "rgba(186, 155, 141, 0.5)"
  },
});

export const incomeOperationCategoryInfos = createOperationCategoryInfos({
  salary: {
    color: "#488282",
    plotColor: "rgba(72, 130, 130, 0.5)"
  },
  bonus: {
    color: "#52AB90",
    plotColor: "rgba(82, 171, 144, 0.5)"
  },
  investment: {
    color: "#E6D5A1",
    plotColor: "rgba(230, 213, 161, 0.5)"
  },
  other: {
    color: "#BA9B8D",
    plotColor: "rgba(186, 155, 141, 0.5)"
  },
});

export const expenseCategories = Object.keys(expenseOperationCategoryInfos);
export const incomeCategories = Object.keys(incomeOperationCategoryInfos);

export const operationCategoryInfos = {
  ...expenseOperationCategoryInfos,
  ...incomeOperationCategoryInfos,
};

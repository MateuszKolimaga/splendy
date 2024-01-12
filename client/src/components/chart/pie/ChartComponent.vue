<template lang="pug">
Doughnut(:plugins="plugins" :data="data" :options="options")
</template>

<script lang="ts">
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Doughnut } from "vue-chartjs";
import { PropType, computed, defineComponent} from "vue";
import * as chartConfig from "./chartConfig";
import { convertOperationsToDatasetToChartData } from "./chartUtils";
import { usePersonalStore } from "@/stores/personalStore";
import { storeToRefs } from "pinia";
import { dougnutTextMiddle } from "./chartPlugins";

ChartJS.register(ArcElement, Tooltip, Legend);


export default defineComponent({
  name: "DoughnutChartComponent",
  components: {
    Doughnut,
  },
  props: {
    currency: String,
    dataType: String as PropType<"expenses" | "incomes">
  },
  setup(props) {
    const dataType = computed(() => props.dataType);
    const personalStore = usePersonalStore();
    const { incomes, expenses } = storeToRefs(personalStore)
    const data = computed(() => {
      const operations = dataType.value == "expenses" ? expenses.value : incomes.value
      return convertOperationsToDatasetToChartData(operations, dataType.value!)
    });
    
    const options = computed(() => {
      const operationsSum = data.value.datasets[0].data.reduce((a, b) => a + b, 0).toFixed(2).toString()
      return chartConfig.chartOptions(props.currency, operationsSum)
    });

    return {
      data,
      options,
      plugins: [dougnutTextMiddle]
    };
  },
});
</script>
./chartUtils
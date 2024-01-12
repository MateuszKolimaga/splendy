export const chartOptions = (currency: string | undefined, sum: string) => ({
  responsive: true,
  maintainAspectRatio: false,
  legend: {
    fontColor: "white",
  },
    elements: {
      center: {
        text: +sum > 0 ? sum + " " + currency : "", 
        sidePadding: 15, 
        minFontSize: 20,
        lineHeight: 15,
      }
    },
  plugins: {
    tooltip: {
      callbacks: {
        //@ts-ignore
        title: function (...args) {
          const label = args[0][0].label
          return label[0].toUpperCase() + label.slice(1)
        },
        //@ts-ignore
        label: function (context) {
          const label =
            " " +
            context.dataset.data[context.dataIndex].toFixed(2) +
            " " +
            (currency ?? ""); 
          return label;
        },
      },
    },
    legend: {
      display: false,
      position: "bottom",
      labels: {
        boxWidth: 15,
        boxHeight: 15,
        padding: 20,
        font: {
          size: 14,
          // weight: "bold"
        },
        //@ts-ignore
        generateLabels: (chart) => {
         //@ts-ignore
        const backgroundColors = chart.data.datasets.map(ds => ds.backgroundColor)
        return chart.data.labels.map((label: string, i: number) => (
        {
          datasetIndex: i,
          text: label[0].toUpperCase() + label.slice(1) + " " + chart.data.datasets[0].data[i] + " " + (currency ?? ""),
          fillStyle: backgroundColors[0][i],
          strokeStyle: backgroundColors[0][i]
        }))}
      },
    },}
});

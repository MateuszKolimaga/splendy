import { useUserStore } from "@/stores/userStore";

export const dougnutTextMiddle = {
  id: "dougnutTextMiddle",
  beforeDraw: function(chart: { config: { options: { elements: { center: any; }; }; }; ctx: any; innerRadius: number; chartArea: { left: any; right: any; top: any; bottom: any; }; }) {
    if (chart.config.options.elements.center) {
      var ctx = chart.ctx;
      var centerConfig = chart.config.options.elements.center;
      var fontStyle = centerConfig.fontStyle || 'Arial';
      var txt = centerConfig.text;

      var maxFontSize = centerConfig.maxFontSize || 75;
      var sidePadding = centerConfig.sidePadding || 20;
      var sidePaddingCalculated = (sidePadding / 100) * (chart.innerRadius * 2)
      ctx.font = "21px " + fontStyle;


      var stringWidth = ctx.measureText(txt).width;
      var elementWidth = (chart.innerRadius * 2) - sidePaddingCalculated;


      var widthRatio = elementWidth / stringWidth;
      var newFontSize = Math.floor(30 * widthRatio);
      var elementHeight = (chart.innerRadius * 2);


      var fontSizeToUse = Math.min(newFontSize, elementHeight, maxFontSize);
      var minFontSize = centerConfig.minFontSize;
      var lineHeight = centerConfig.lineHeight || 25;
      var wrapText = false;

      if (minFontSize === undefined) {
        minFontSize = 20;
      }

      if (minFontSize && fontSizeToUse < minFontSize) {
        fontSizeToUse = minFontSize;
        wrapText = true;
      }


      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      var centerX = ((chart.chartArea.left + chart.chartArea.right) / 2);
      var centerY = ((chart.chartArea.top + chart.chartArea.bottom) / 2);
      ctx.font = 'bold 20px sans-serif';

      if (!wrapText) {
        ctx.fillText(txt, centerX, centerY);
        return;
      }

      var words = txt.split(' ');
      var line = '';
      var lines = [];

      for (var n = 0; n < words.length; n++) {
        var testLine = line + words[n] + ' ';
        var metrics = ctx.measureText(testLine);
        var testWidth = metrics.width;
        if (testWidth > elementWidth && n > 0) {
          lines.push(line);
          line = words[n] + ' ';
        } else {
          line = testLine;
        }
      }

      centerY -= (lines.length / 2) * lineHeight;

      for (var n = 0; n < lines.length; n++) {
        ctx.fillText(lines[n], centerX, centerY);
        centerY += lineHeight;
      }
      ctx.fillText(line, centerX, centerY);
    }
  }
}
export const doughnutLabelsLine = {
    id: "doughnutLabelsLine",
    afterDraw(chart: { data?: any; getDatasetMeta?: any; ctx?: any; chartArea?: any; }) {
      const {
        ctx,
        chartArea: { width, height },
      } = chart;
      const userStore = useUserStore();
      const currency = userStore.user?.currency;

      chart.data.datasets.forEach((dataset: any, i: number) => {
        chart.getDatasetMeta(i).data.forEach((datapoint: { tooltipPosition: () => { x: any; y: any; }; options: { backgroundColor: any; }; }, index: number) => {
          const { x, y } = datapoint.tooltipPosition();

          const halfHeight = height / 2;
          const halfWidth = width / 2;

          const xLine = x >= halfWidth ? x + 55 : x - 55;
          const yLine = y >= halfHeight ? y + 55 : y - 55;
          const extraLine = x >= halfWidth ? 55 : -55;

          ctx.beginPath();
          ctx.moveTo(x, y);
          ctx.lineTo(xLine, yLine);
          ctx.lineTo(xLine + extraLine, yLine);
          ctx.strokeStyle = datapoint.options.backgroundColor;
          ctx.stroke();

          // const textWidth = ctx.measureText(dataset.data[index]).width;
          ctx.font = "18px Arial";

          const textXPosition = x >= halfWidth ? "left" : "right";
          const plusFivePx = x >= halfWidth ? 5 : -5;
          ctx.textAlign = textXPosition;
          ctx.textBaseline = "middle";
          ctx.fillStyle = 'rgb(91,91,91)';
          ctx.fillText(
            dataset.data[index].toFixed(2) + " " + (currency ?? ""),
            xLine + extraLine + plusFivePx,
            yLine
          );
        });
      });
    },
  };

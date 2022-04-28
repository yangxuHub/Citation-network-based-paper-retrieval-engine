import Vue from "vue";
import ECharts from "vue-echarts";
import { use } from "echarts/core";

// import ECharts modules manually to reduce bundle size
import { CanvasRenderer } from "echarts/renderers";
import { LineChart, ScatterChart, EffectScatterChart,GraphChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  GridComponent
} from "echarts/components";

use([
  CanvasRenderer,
  LineChart,
  GraphChart,
  ScatterChart,
  EffectScatterChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
]);

// register globally (or you can do it locally)
Vue.component("v-chart", ECharts);

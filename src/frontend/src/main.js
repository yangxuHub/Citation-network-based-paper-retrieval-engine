import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "./plugins/animate.js";
import "./plugins/axios.js";
import "./plugins/chart.js";
import "./plugins/cookies.js";
import "./plugins/element.js";
import "./plugins/video.js";
import tools from "./plugins/tools.js";
import { i18n } from "./plugins/i18n.js";
import { library } from "@fortawesome/fontawesome-svg-core";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { fab } from "@fortawesome/free-brands-svg-icons";
import { far } from "@fortawesome/free-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import vuescroll from 'vue-scroll'
 
Vue.use(vuescroll)
import * as echarts from "echarts"
Vue.prototype.$echarts = echarts
// FontAwesome Icon
library.add(fas, fab, far);
Vue.component("font-awesome-icon", FontAwesomeIcon);

// Tools
Vue.prototype.COMMON = tools;

Vue.config.productionTip = false;

// HTML Title
router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title =
      i18n.t("router.Base") + " - " + i18n.t("router." + to.meta.title);
  }
  next();
});

new Vue({
  i18n,
  router,
  store,
  render: h => h(App)
}).$mount("#app");

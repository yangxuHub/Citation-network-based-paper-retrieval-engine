<template>
  <div id="app">
    <el-backtop class="d-none d-sm-flex"></el-backtop>
    <header ref="nav">
      <Navbar />
    </header>
    <main :style="{ minHeight: mainHeight }">
      <keep-alive>
        <router-view v-if="$route.meta.keepAlive"></router-view>
      </keep-alive>
      <router-view v-if="!$route.meta.keepAlive"></router-view>
    </main>
    <footer ref="foot">
      <Infobar />
    </footer>
  </div>
</template>

<script>
import Infobar from "@/components/Infobar.vue";
import Navbar from "@/components/Navbar.vue";

export default {
  name: "app",
  components: { Infobar, Navbar},
  data: function() {
    return {
      mainHeight: "calc(100vh - 64px - 60.5px)"
    };
  },
  computed: {
    // Show
    //this.$store.state全局变量的调用，定义在store/index.js里面 初始默认值为false
    fChatShow: {
      get() {
        return this.$store.state.fChatShow;
      },
      set(value) {
        this.$store.commit("updateChatShow", value);
      }
    },
    // Maintain
    fHomeMaintain: function() {
      return this.$store.state.fHomeMaintain;
    }
  },
  mounted: function() {
    // Init
    this.localeInit();
    this.betaInit();
    this.ipInit();
    // Height
    this.$nextTick(() => {
      this.mainInit();
    });
    window.addEventListener("resize", () => {
      this.mainInit();
    });
  },
  methods: {
    // Init
    localeInit() {
      // if (this.$cookies.isKey("locale")) {
      //   const locale = this.$cookies.get("locale");
      //   if (!locale || !["chs", "cht", "eng", "jpa"].includes(locale)) {
      //     this.$cookies.remove("locale");
      //     return;
      //   }
      //   this.$i18n.locale = locale;
      // }
    },
    betaInit() {
      // if (this.fHomeMaintain) {
      //   this.$router.push({ path: "/sorry" });
      // }
      // const url = window.location.href;
      // if (
      //   url.indexOf("beta.hammerscholar.net") != -1 ||
      //   url.indexOf(":8077") != -1
      // ) {
      //   console.warn("You are viewing the beta version of Hammer Scholar");
      //   this.$message.warning(
      //     "You are viewing the beta version of Hammer Scholar"
      //   );
      // }
    },
    ipInit() {
      // this.axios
      //   .get("/ip")
      //   .then(response => {
      //     console.log("Welcome to Hammer Scholar, user of " + response.data.ip);
      //     const ip = response.data.ip ? response.data.ip : "";
      //     this.$store.commit("updateIPLocal", ip);
      //   })
      //   .catch(() => {});
    },
    mainInit() {
      this.mainHeight =
        "calc(100vh - " +
        this.getNavHeight() +
        "px - " +
        this.getInfoHeight() +
        "px)";
    },
    getNavHeight() {
      return this.$refs.nav && this.$refs.nav.offsetHeight
        ? this.$refs.nav.offsetHeight
        : 64;
    },
    getInfoHeight() {
      return this.$refs.foot && this.$refs.foot.offsetHeight
        ? this.$refs.foot.offsetHeight
        : 60.5;
    },
    // Export
    handleExport(data) {
      var jsonExport = JSON.stringify(data);
      var blob = new Blob([jsonExport], {
        type: "text/plain;charset=utf-8"
      });
      var time = new Date().Format("yyyy-MM-dd hh_mm_ss");
      var fileName = "Document results of Hammer Scholar " + time + ".json";
      var url = window.URL || window.webkitURL;
      var link = url.createObjectURL(blob);
      var a = document.createElement("a");
      a.download = fileName;
      a.href = link;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    },
    // Highlight
    subPosFind(sub, str) {
      var [a, i] = [[], -1];
      [sub, str] = [sub.toLowerCase(), str.toLowerCase()];
      while ((i = str.indexOf(sub, i + 1)) >= 0) a.push(i);
      return a;
    },
    subHighlight(sub, str) {
      const positions = this.subPosFind(sub, str);
      var html = "<span>";
      var index = 0;
      for (let i = 0; i < positions.length; i++) {
        let pos = positions[i];
        let fPos = i != positions.length && pos + sub.length > positions[i + 1];
        html += str.slice(index, pos);
        index = fPos ? positions[i + 1] : pos + sub.length;
        html +=
          '<strong class="stress-text">' + str.slice(pos, index) + "</strong>";
      }
      html += str.slice(index);
      return html + "</span>";
    },
    // Locale
    localeConvert(locale = "chs", msg = "语言已切换到简体中文。") {
      // Locale
      this.$i18n.locale = locale;
      // Title
      document.title =
        this.$t("router.Base")
      // Options
      this.$store.commit("updateLogicOptions");
      this.$store.commit("updateFieldOptions");
      this.$store.commit("updateListDocs");
      this.$store.commit("updateFilmOptions");
      // Cookie
      this.$cookies.remove("locale");
      this.$cookies.set("locale", locale, "1y");
      // Message
      if (msg) {
        this.$message.info(msg);
      }
    },
    debounce(fn, wait) {
      let timeout = null;
      return function() {
        if (timeout !== null) clearTimeout(timeout);
        timeout = setTimeout(fn, wait);
      };
    }
  }
};

Date.prototype.Format = function(fmt) {
  var o = {
    "M+": this.getMonth() + 1,
    "d+": this.getDate(),
    "h+": this.getHours(),
    "m+": this.getMinutes(),
    "s+": this.getSeconds(),
    "q+": Math.floor((this.getMonth() + 3) / 3),
    S: this.getMilliseconds()
  };
  if (/(y+)/.test(fmt))
    fmt = fmt.replace(
      RegExp.$1,
      (this.getFullYear() + "").substr(4 - RegExp.$1.length)
    );
  for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt))
      fmt = fmt.replace(
        RegExp.$1,
        RegExp.$1.length == 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length)
      );
  return fmt;
};
</script>

<style lang="scss">
/* Global */
::selection {
  color: #ffffff;
  background-color: #dc3545;
}
#app {
  font-family: -apple-system, Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.stress-text {
  color: #4aa7d8;
}
</style>

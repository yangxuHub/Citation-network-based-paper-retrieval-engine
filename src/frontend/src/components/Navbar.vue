<template>
  <div class="navbar py-1 py-sm-3">
    <div class="container-fluid">
      <div class="d-flex justify-content-between align-items-center w-100">
        <div class="flex-menu ml-0 ml-sm-3">
        </div>
        <div v-if="fLogoShow" class="flex-brand ml-3 d-none d-sm-block">
          <el-link :underline="false" @click="$router.push({ path: '/' })">
            <img src="@/assets/banner.png" height="28" />
          </el-link>
        </div>
        <div
          v-if="fSearchShow"
          class="flex-search text-center mx-4 w-100 d-none d-md-block"
        >
          <el-input
            v-model="searchInput"
            :placeholder="
              fFilmSelect
                ? $t('home.PleaseInputVideo')
                : $t('home.PleaseInputBasic')
            "
            @keypress.enter.native="handleQuery"
            class="w-100 input-with-select"
            size="small"
            clearable
          >
            <el-select
              v-if="fFilmSelect"
              v-model="filmField"
              :placeholder="$t('home.ChooseField')"
              slot="prepend"
            >
              <el-option
                v-for="film in filmOptions"
                :key="film.value"
                :label="film.label"
                :value="film.value"
              >
              </el-option>
            </el-select>
            <el-button slot="append" @click="handleQuery">
              <font-awesome-icon :icon="['fas', 'search']" size="sm" />
              <span class="ml-1 d-none d-lg-inline-block">{{
                $t("home.Search")
              }}</span>
            </el-button>
          </el-input>
        </div>
        <div
          class="flex-link text-right ml-auto mr-0 mr-sm-3"
          :style="{ minWidth: flexWidth + 'px' }"
        >
          <el-link
            v-if="fHomeShow"
            :underline="false"
            @click="$router.push({ path: '/' })"
          >
            <font-awesome-icon :icon="['fas', 'home']" />
            <span class="link-router">{{ $t("router.BackHome") }}</span>
          </el-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Navbar",
  data: function() {
    return {
      fFlexSmall: window.matchMedia("(max-width: 1200px)").matches
    };
  },
  computed: {
    // SHOW
    fLogoShow: function() {
      return !["/"].includes(this.$route.path);
    },
    fSearchShow: function() {
      return !["/", "/adv"].includes(this.$route.path);
    },
    fHomeShow: function() {
      return !["/"].includes(this.$route.fullPath);
    },
    fFilmShow: function() {
      return !["/?item=film"].includes(this.$route.fullPath);
    },
    // Menu
    fDrawerShow: {
      get() {
        return this.$store.state.fDrawerShow;
      },
      set(value) {
        this.$store.commit("updateDrawerShow", value);
      }
    },
    // Search
    searchInput: {
      get() {
        return this.$store.state.searchInput;
      },
      set(value) {
        this.$store.commit("updateInput", value);
      }
    },
    fFilmSelect: function() {
      return ["/film"].includes(this.$route.path);
    },
    filmField: {
      get() {
        return this.$store.state.selectFilm;
      },
      set(value) {
        this.$store.commit("updateFilm", value);
      }
    },
    filmOptions: function() {
      return this.$store.state.filmOptions;
    },
    // Lang
    langView: function() {
      return [
        {
          obj: "chs",
          link: "切换到简体中文",
          msg: "语言已切换到简体中文。",
          show: this.$i18n.locale == "chs"
        },
        {
          obj: "cht",
          link: "切換到正體中文",
          msg: "語言已切換到正體中文。",
          show: this.$i18n.locale == "cht"
        },
        {
          obj: "eng",
          link: "Switch to English",
          msg: "The language has been switched to English.",
          show: this.$i18n.locale == "eng"
        },
        {
          obj: "jpa",
          link: "日本語に切り替える",
          msg: "表示言語が日本語に切り替わりました。",
          show: this.$i18n.locale == "jpa"
        }
      ];
    },
    fENG: function() {
      return this.$i18n.locale == "eng";
    },
    // Flex
    flexWidth: function() {
      // All
      if (this.fFlexSmall) {
        switch (this.$i18n.locale) {
          case "chs":
          case "cht":
            return 185;
          case "eng":
            return 200;
          case "jpa":
            return 200;
          default:
            return 185;
        }
      } else {
        switch (this.$i18n.locale) {
          case "chs":
          case "cht":
            return 460;
          case "eng":
            return 495;
          case "jpa":
            return 520;
          default:
            return 460;
        }
      }
    }
  },
  mounted: function() {
    window.addEventListener("resize", () => {
      this.fFlexSmall = window.matchMedia("(max-width: 1200px)").matches;
    });
  },
  methods: {
    handleQuery() {
      this.$store.commit("handleQuery", {
        film: this.fFilmSelect,
        cap: this.filmField == "caption"
      });
    },
    localeConvert(locale, msg) {
      this.$parent.localeConvert(locale, msg);
    }
  }
};
</script>

<style scoped lang="scss">
.navbar {
  .flex-brand {
    height: 32px;
    line-height: 32px;
    // min-width: 180px;
    min-width: 216px;
  }
  .flex-search ::v-deep {
    .el-select {
      width: 110px;
    }
    .el-input-group__append {
      background-color: #77a7d8;
      border-color: #77a7d8;
      color: #ffffff;
    }
  }
  .flex-link {
    height: 32px;
    line-height: 32px;
    & > *:not(:first-child) {
      margin-left: 0.75rem;
    }
    .el-dropdown-link:hover {
      cursor: pointer;
      color: #77a7d8;
    }
    .link-router {
      font-size: 14px;
      margin-left: 0.25rem;
    }
  }
}
</style>

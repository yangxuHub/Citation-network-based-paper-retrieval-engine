<template>
  <div class="home container">
    <div class="px-3 home-container">
      <!-- Head -->
      <el-row class="row-head">
        <el-col :span="24" class="col-head text-center">
          <div class="d-flex justify-content-center">
            <img
              src="@/assets/logo.png"
              height="158"
              class="d-none d-md-block"
            />
            <img
              src="@/assets/logo.png"
              height="143"
              class="d-none d-sm-block d-md-none"
            />
            <img src="@/assets/logo.png" class="d-block d-sm-none w-100" />
          </div>
        </el-col>
      </el-row>
      <!-- Input -->
      <el-row class="row-input">
        <el-col :span="24" class="col-input mt-3 mb-2">
          <el-autocomplete
            v-model="searchInput"
            :placeholder="
              fFilm ? $t('home.PleaseInputVideo') : $t('home.PleaseInputBasic')
            "
            :fetch-suggestions="handleComplete"
            @keypress.enter.native="handleQuery"
            @select="handleSelect"
            class="inline-input w-100"
            clearable
          >
            <el-select
              v-if="fFilm"
              v-model="filmInput"
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
            <template slot-scope="{ item }">
              <div class="teal-text">{{ item.query }}</div>
            </template>
            <el-button slot="append" @click="handleQuery">
              <font-awesome-icon :icon="['fas', 'search']" size="sm" />
              <span class="ml-1">{{ $t("home.Search") }}</span>
            </el-button>
          </el-autocomplete>
        </el-col>
      </el-row>
      <!-- History -->
      <el-row v-if="historyTableData.length" class="row-history">
        <el-col :span="24" class="col-history">
          <div class="d-flex align-items-center">
            <span class="hist-intro">{{ $t("home.Histories") }}：</span>
            <ul class="list-unstyled m-0">
              <li
                v-for="(history, index) in historyTableData.slice(0, 2)"
                :key="index"
              >
                <el-link
                  :underline="false"
                  @click="handleHistory(history.query)"
                >
                  <span class="m-0">{{ history.query }}</span>
                </el-link>
              </li>
              <li
                v-for="(history, index) in historyTableData.slice(2, 5)"
                :key="index + 2"
                class="d-none d-md-inline-block"
              >
                <el-link
                  :underline="false"
                  @click="handleHistory(history.query)"
                >
                  <span class="m-0">{{ history.query }}</span>
                </el-link>
              </li>
            </ul>
          </div>
        </el-col>
      </el-row>
      <!-- Year -->
      <!-- <el-row v-if="fYear && !fFilm" class="row-year">
        <el-col :span="24" class="col-year mb-2">
          <el-divider class="mt-4 mb-3"></el-divider>
          <YearRange :from="''" :to="''" @year-range="getYearRange" />
        </el-col>
      </el-row> -->
      <!-- Tool -->
      <!-- <el-row class="row-tool">
        <el-col :span="24" class="col-tool d-flex mt-4">
          <el-button v-if="!fFilm" type="text" @click="handleYear">
            <font-awesome-icon :icon="['far', 'calendar-plus']" class="mr-2" />
            <span class="d-none d-sm-inline-block"
              ><span v-if="!fYear" v-html="$t('home.TimeAdd')"></span
              ><span v-else v-html="$t('home.TimeDelete')"></span></span
            ><span>{{ $t("home.Time") }}</span
            ><span
              v-html="$t('home.TimeRange')"
              class="d-none d-sm-inline-block"
            ></span>
          </el-button>
          <el-button type="text" @click="$router.push({ path: '/adv' })">
            <font-awesome-icon :icon="['fas', 'crown']" class="mr-2" />
            <span>{{ $t("home.Advanced") }}</span
            ><span
              v-html="$t('home.DocumentSearch')"
              class="d-none d-md-inline-block"
            ></span>
          </el-button>
          <el-button type="text" @click="handleReset">
            <font-awesome-icon :icon="['fas', 'undo-alt']" class="mr-2" />
            <span>{{ $t("home.Reset") }}</span>
          </el-button>
        </el-col>
      </el-row> -->
    </div>
  </div>
</template>

<script>
// import YearRange from "@/components/YearRange.vue";

export default {
  name: "Search",
  // components: { YearRange },
  data: function() {
    return {
      tabActive: "home",
      fYear: false
    };
  },
  computed: {
    fFilm: function() {
      return this.tabActive == "film";
    },
    yearFrom: {
      get() {
        return this.$store.state.yearFrom;
      },
      set(value) {
        this.$store.commit("updateYearFrom", value);
      }
    },
    yearTo: {
      get() {
        return this.$store.state.yearTo;
      },
      set(value) {
        this.$store.commit("updateYearTo", value);
      }
    },
    searchInput: {
      get() {
        return this.$store.state.searchInput;
      },
      set(value) {
        this.$store.commit("updateInput", value);
      }
    },
    filmInput: {
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
    historyTableData: function() {
      const historyKeys = this.$cookies
        .keys()
        .filter(e => e.substr(0, 8) == "history*");
      var historyData = [];
      historyKeys.forEach(function(key) {
        if (!key.match(/^history\*\$.+\$$/g)) {
          historyData.push(this.$cookies.get(key));
        }
      }, this);
      return historyData.reverse();
    }
  },
  watch: {
    $route() {
      this.routeCheck();
    }
  },
  mounted: function() {
    this.routeCheck();
  },
  methods: {
    routeCheck() {
      const item = this.$route.query.item;
      this.tabActive = item ? item : "home";
      this.fYear = false;
      [this.yearFrom, this.yearTo] = ["", ""];
    },
    handleComplete(queryString, cb) {
      var histories = this.historyTableData.slice(0, 50);
      var results = queryString
        ? histories.filter(this.historyFilter(queryString))
        : histories;
      cb(results);
    },
    historyFilter(queryString) {
      return history => {
        return (
          history.query.toLowerCase().indexOf(queryString.toLowerCase()) === 0
        );
      };
    },
    handleSelect(item) {
      this.searchInput = item.query;
      this.handleQuery();
    },
    handleHistory(query) {
      this.searchInput = query;
      this.handleQuery();
    },
    handleYear() {
      this.fYear = !this.fYear;
      if (!this.fYear) {
        [this.yearFrom, this.yearTo] = ["", ""];
      }
    },
    handleReset() {
      [this.searchInput, this.fYear] = ["", false];
      [this.yearFrom, this.yearTo] = ["", ""];
    },
    handleQuery() {
      this.$store.commit("handleQuery", {
        film: this.fFilm,
        cap: this.filmInput == "caption"
      });
    },
    getYearRange(range) {
      this.yearFrom = range.from;
      this.yearTo = range.to;
    }
  }
};
</script>

<style scoped lang="scss">
.home {
  .home-container {
    padding-top: 20vh;
    .row-input ::v-deep {
      .el-input__inner {
        height: 48px;
        line-height: 48px;
      }
      .el-select {
        width: 120px;
      }
      .el-input-group__append {
        background-color: #77a7d8;
        border-color: #77a7d8;
        color: #ffffff;
      }
    }
    .row-history {
      .hist-intro {
        font-size: 12px;
        color: #4f4f4f;
        margin-right: 0.125rem;
      }
      li {
        display: inline-block;
        color: #4f4f4f;
        margin-bottom: 0;
        .el-link {
          font-size: 12px;
          transform: translateY(-1px);
        }
        &:not(:first-child)::before {
          content: "\00A0•\00A0";
          font-size: 12px;
          padding: 0 0.25rem;
        }
      }
    }
    .el-divider {
      margin: 2.5rem 0 2rem;
    }
    .row-tool {
      .el-button {
        padding: 0.25rem 0;
        font-size: 1rem;
      }
    }
  }
}
</style>

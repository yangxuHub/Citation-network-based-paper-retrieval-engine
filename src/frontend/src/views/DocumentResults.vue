<template>
  <div class="documents container">
    <div class="px-3">
      <el-row class="row-head">
        <el-col :span="24" class="col-head">
          <ResultHead
            :load="fLoad"
            :found="fFound"
            :query="queryInput"
            :total="totalDoc"
          />
        </el-col>
      </el-row>
      <el-row class="row-filter">
        <el-col :span="24" class="col-filter mt-2 mb-3">
          <el-divider class="mb-2"></el-divider>
          <div class="d-flex flex-wrap flex-filter">
            <el-select
              v-model="sortBy"
              size="small"
              class="ml-auto mt-2 mt-lg-0"
              @change="filterSort"
            >
              <el-option
                v-for="sort in sortOptions"
                :key="sort.value"
                :label="sort.label"
                :value="sort.value"
              >
              </el-option>
            </el-select>
          </div>
          <el-divider class="mt-2 mb-3"></el-divider>
        </el-col>
      </el-row>
      <el-row :gutter="20" v-loading="fLoad" class="row-result">
        <el-col :span="24" v-if="!fLoad" class="col-none">
          <div v-if="!fFound" class="text-center mt-3">
            {{ $t("list.TryAnother") }}
          </div>
        </el-col>
        <el-col :xs="24" :sm="24" :md="16" v-if="!fLoad" class="col-list">
          <div v-if="!fMainFound" class="text-center">
            {{ $t("list.TryAnother") }}
          </div>
          <el-row class="row-docs">
            <el-col :span="24" class="col-docs">
              <ListDoc :docs="resultDoc" :highlight="keyHighlight" />
            </el-col>
          </el-row>
        </el-col>
      </el-row>
      <Page :total="totalDoc" class="mt-3 mt-sm-4 pb-0 pb-sm-3 mb-4" />
    </div>
  </div>
</template>

<script>
import ListDoc from "@/components/ListDoc.vue";
import Page from "@/components/Page.vue";
import ResultHead from "@/components/ResultHead.vue";

export default {
  name: "DocumentResults",
  components: { ListDoc, Page, ResultHead },
  data: function() {
    return {
      // Head
      fLoadDoc: true,
      isAdv: false,
      queryInput: "",
      totalDoc: 0,
      // Filter
      hasFilter: [],
      sortBy: "normal",
      // Result
      resultDoc: []
    };
  },
  computed: {
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
    sortOptions: function() {
      return [
        {
          value: "normal",
          label: "原始排序降序"
        },
        {
          value: "importance",
          label: "importance优化排序"
        }
      ];
    },
    fLoad: function() {
      return this.fLoadDoc;
    },
    fFoundDoc: function() {
      return this.resultDoc.length > 0;
    },
    fFound: function() {
      return this.fFoundDoc;
    },
    fMainFound: function() {
      return this.fFoundDoc;
    },
    hasPDF: function() {
      return this.hasFilter.includes("pdf");
    },
    hasCode: function() {
      return this.hasFilter.includes("code");
    },
    hasSource: function() {
      return this.hasFilter.includes("source");
    },
    hasVideo: function() {
      return this.hasFilter.includes("video");
    },
    hasSlide: function() {
      return this.hasFilter.includes("slide");
    },
    hasDataset: function() {
      return this.hasFilter.includes("dataset");
    },
    currentPage: {
      get() {
        return this.$store.state.currentPage;
      },
      set(value) {
        this.$store.commit("updatePage", value);
      }
    },
    ipLocal: function() {
      return this.$store.state.ipLocal;
    },
    fENG: function() {
      return this.$i18n.locale == "eng";
    },
    fJPA: function() {
      return this.$i18n.locale == "jpa";
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
      const routeQuery = this.$route.query;
      const query = routeQuery.query;
      if (!query) {
        console.log("Redirect to home.");
        this.$router.push({ path: "/" });
        return;
      }
      this.isAdv = !routeQuery.adv ? false : routeQuery.adv == "true";
      this.queryInput = query;
      this.$store.commit("updateInput", query);
      this.currentPage = 1;
      this.querySubmit();
    },
    querySubmit(pageFrom = 0) {
      console.log("Start searching...");
      this.fLoadDoc = true;
      this.resultDoc = [];
      try {
        this.docSubmit(pageFrom);
      } catch (e) {
        this.$message.error(this.$t("home.NotFormat"));
        this.$router.push({ path: "/" });
        return;
      }
    },
    //发送请求函数
    docSubmit(pageFrom) {
      var queryStr = "";
      queryStr = this.queryInput; //查询输入的关键词
      const prefix = "query?type=TITLE&";
      this.axios
        .get(
          prefix +
            "query=" +
            queryStr +
            "&from=" +
            pageFrom +
            "&size=" +
            "10" +
            "&filter_year=" +
            "false" +
            "&s_year=" +
            "2015" +
            "&e_year=" +
            "2022" +
            "&sort_by_incite=" +
            "false" +
            "&sort_by_outcite=" +
            "false" +
            "&sort_by_time=" +
            "false" +
            "&sort_by_importance=" +
            (this.sortBy == "importance")
        )
        .then(response => {
          // console.log(response.data);
          const responseData = this.COMMON.toJson(response.data);
          this.totalDoc = responseData.hits.total; //查询出的总结果数
          responseData.hits.hit.forEach(function(hit) {
            this.resultDoc.push(
              Object.assign({}, hit, {
                fExpandAbs: false,
                fBlogLoad: true,
                listBlog: []
              })
            );
          }, this);
          // console.log(this.resultDoc);
        })
        .catch(error => {
          console.error(error);
          // this.$message.error(this.$t("list.UnknownError"));
        })
        .finally(() => {
          this.fLoadDoc = false;
        });
    },
    filterYear(range) {
      this.yearFrom = range.from;
      this.yearTo = range.to;
      this.currentPage = 1;
      this.querySubmit();
    },
    filterExternal() {
      this.currentPage = 1;
      this.querySubmit();
    },
    filterSort() {
      this.currentPage = 1;
      this.querySubmit();
    },
    keyHighlight(str) {
      return this.$parent.subHighlight(this.queryInput, str);
    },
    handleChat() {
      this.$store.commit("updateChatShow", true);
    },
    handleLink(link) {
      window.open(link, "_blank");
    }
  }
};
</script>

<style scoped lang="scss">
.documents {
  .row-filter {
    @media (max-width: 576px) {
      .el-button,
      ::v-deep .el-checkbox-button__inner,
      ::v-deep .el-radio-button__inner {
        padding-left: 0.5rem;
        padding-right: 0.5rem;
      }
    }
  }
  .row-result {
    min-height: 40vh;
    .el-link {
      color: #77a7d8;
    }
    .col-draw {
      font-size: 0.75rem;
      .res-name {
        font-size: 0.8125rem;
      }
      .res-alias {
        color: #4f4f4f;
      }
      .res-orcid {
        color: #9e9e9e;
      }
    }
    .col-side {
      .res-bg {
        height: 2.25rem;
        line-height: 2.25rem;
        background: rgb(0, 105, 92);
        background: linear-gradient(
          90deg,
          rgba(0, 105, 92, 1) 0%,
          rgba(0, 150, 136, 1) 40%,
          rgba(0, 151, 167, 1) 100%
        );
        .el-link {
          width: 100%;
          &::after {
            display: none;
          }
          ::v-deep .el-link--inner {
            width: 100%;
            display: flex;
            align-items: center;
          }
        }
      }
      .res-full p {
        color: #4f4f4f;
        font-size: 14px;
        margin-bottom: 0;
      }
    }
  }
}
</style>

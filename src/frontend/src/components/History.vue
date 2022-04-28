<template>
  <div class="history">
    <el-row class="row-head">
      <el-col :xs="10" :sm="16" class="col-title">
        <h4 class="m-0">{{ $t("history.SearchHistory") }}</h4>
      </el-col>
      <el-col :xs="14" :sm="8" class="col-filter">
        <el-input
          v-model="historySearch"
          size="mini"
          :placeholder="$t('history.PleaseInput')"
        >
        </el-input>
      </el-col>
    </el-row>
    <el-row class="row-table">
      <el-col :span="24" class="col-table mt-3">
        <el-table
          :data="
            historyTableData.filter(
              data =>
                !historySearch ||
                data.query.toLowerCase().includes(historySearch.toLowerCase())
            )
          "
          :cell-style="{ padding: '0.375rem 0' }"
          :show-header="false"
          max-height="600"
          class=""
        >
          <el-table-column
            type="index"
            :index="indexMethod"
            width="40"
          ></el-table-column>
          <el-table-column prop="query" min-width="200"></el-table-column>
          <el-table-column
            prop="time"
            align="right"
            width="160"
            v-if="fTableTime"
          >
          </el-table-column>
          <el-table-column align="right" width="120">
            <template v-slot:default="scope">
              <el-button-group>
                <el-button size="mini" @click="handleSearch(scope.$index)">
                  <font-awesome-icon :icon="['fas', 'search']" />
                </el-button>
                <el-button
                  size="mini"
                  type="danger"
                  @click="handleDelete(scope.$index)"
                >
                  <font-awesome-icon :icon="['far', 'trash-alt']" />
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
    <el-row class="row-clear">
      <el-col :span="6" class="col-clear mt-3">
        <el-button
          type="text"
          v-if="!!historyTableData.length"
          @click="handleClear"
          class="ml-2"
        >
          <font-awesome-icon :icon="['fas', 'trash']" class="mr-2" />
          <span>{{ $t("history.ClearAll") }}</span>
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "History",
  props: ["histories"],
  data: function() {
    return {
      fTableTime: !window.matchMedia("(max-width: 992px)").matches,
      historySearch: "",
      historiesData: this.histories
    };
  },
  computed: {
    historyTableData: {
      get() {
        var tableData = [];
        this.historiesData.forEach(function(history) {
          tableData.push({
            query: history.query,
            time: history.time
          });
        }, this);
        return tableData;
      },
      set(value) {
        if (Number.isInteger(value)) {
          this.historiesData.splice(value, 1);
        } else if (Array.isArray(value)) {
          this.historiesData = [];
        }
      }
    }
  },
  mounted: function() {
    window.addEventListener("resize", () => {
      this.fTableTime = !window.matchMedia("(max-width: 992px)").matches;
    });
  },
  methods: {
    indexMethod(index) {
      return this.historyTableData.length - index;
    },
    handleSearch(index) {
      const history = this.historiesData[index];
      this.$store.commit("updateInput", history.query);
      this.$store.commit("handleQuery");
    },
    handleDelete(index) {
      this.$confirm(
        this.$t("history.DeleteConfirm"),
        this.$t("history.Warning"),
        {
          confirmButtonText: this.$t("history.OK"),
          cancelButtonText: this.$t("history.Cancel"),
          type: "warning"
        }
      )
        .then(() => {
          this.$cookies.remove("history*" + this.historyTableData[index].query);
          this.historyTableData = index;
          this.$message.success(this.$t("history.DeleteOK"));
        })
        .catch(() => {
          this.$message.info(this.$t("history.DeleteCancel"));
        });
    },
    handleClear() {
      this.$confirm(
        this.$t("history.ClearConfirm"),
        this.$t("history.Warning"),
        {
          confirmButtonText: this.$t("history.OK"),
          cancelButtonText: this.$t("history.Cancel"),
          type: "warning"
        }
      )
        .then(() => {
          const historyKeys = this.$cookies
            .keys()
            .filter(e => e.substr(0, 8) == "history*");
          historyKeys.forEach(function(key) {
            this.$cookies.remove(key);
          }, this);
          this.historyTableData = [];
          this.$message.success(this.$t("history.ClearOK"));
        })
        .catch(() => {
          this.$message.info(this.$t("history.ClearCancel"));
        });
    }
  }
};
</script>

<style scoped lang="scss">
.history {
  .row-table {
    max-height: 50vh;
    .el-button {
      padding: 0.25rem 0.75rem;
      font-size: 0.75rem;
    }
  }
}
</style>

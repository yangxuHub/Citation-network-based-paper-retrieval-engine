<template>
  <div class="page">
    <el-pagination
      small
      background
      @current-change="handlePageChange"
      :current-page.sync="currentPage"
      :total="total"
      :page-size="10"
      :pager-count="5"
      layout="prev, pager, next"
      class="text-center d-block d-sm-none"
      hide-on-single-page
    >
    </el-pagination>
    <el-pagination
      background
      @current-change="handlePageChange"
      :current-page.sync="currentPage"
      :total="total"
      :page-size="10"
      :pager-count="5"
      layout="prev, pager, next, jumper"
      class="text-center d-none d-sm-block"
      hide-on-single-page
    >
    </el-pagination>
  </div>
</template>

<script>
export default {
  name: "Page",
  props: ["total"],
  computed: {
    currentPage: {
      get() {
        return this.$store.state.currentPage;
      },
      set(value) {
        this.$store.commit("updatePage", value);
      }
    }
  },
  mounted: function() {
    this.currentPage = 1;
  },
  methods: {
    handlePageChange(val) {
      this.$parent.querySubmit(val - 1);
    }
  }
};
</script>

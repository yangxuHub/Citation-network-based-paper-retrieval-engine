<template>
  <div class="infobar container">
    <div class="px-3 pt-2 pb-2">
      <el-divider class="my-2"></el-divider>
      <div class="d-flex flex-wrap py-1">
        <div class="d-flex align-items-center flex-wrap mr-1">
          <span class="mr-1">Copyright &copy;</span>
          <span class="mr-1">Team 8</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Infobar"
};
</script>

<style scoped lang="scss">
.infobar {
  font-size: 13px;
  .el-link {
    font-size: 13px;
    ::v-deep .el-link--inner {
      display: flex;
      align-items: center;
    }
  }
}
</style>

<template>
  <div class="mistake container">
    <div class="px-3">
      <el-row class="row-error">
        <el-col :span="24" class="col-error">
          <h1 class="mt-5 m-0">
            <span class="mr-2">{{ $t("router.Mistake") }}</span>
            <font-awesome-icon :icon="['fas', 'exclamation-triangle']" />
          </h1>
          <el-card
            class="box-card border-danger mt-4"
            style="border-width: 0.125rem;"
          >
            <p class="mb-2">{{ $t("home.CheckURL") }}</p>
            <p class="mb-0">{{ $t("home.KeepContact") }}</p>
          </el-card>
          <el-button
            type="primary"
            class="mt-4"
            @click="$router.push({ path: '/' })"
            >{{ $t("home.Back2Home") }}</el-button
          >
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
export default {
  name: "Mistake"
};
</script>

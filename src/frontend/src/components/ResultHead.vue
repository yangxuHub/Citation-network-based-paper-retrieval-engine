<template>
  <div class="result-head">
    <h1 class="mt-4 pt-2 mb-0">
      <span v-if="load">{{ $t("list.Searching") }}</span>
      <span v-else-if="!found">
        <span v-if="$i18n.locale == 'jpa'">
          <span class="mr-1">{{ $t("list.QueryLeftQuote") }}</span>
          <span>{{ query }}</span>
          <span class="ml-1 mr-1">{{ $t("list.QueryRightQuote") }}</span>
          <span>{{ $t("list.SomeAbout") }}</span>
        </span>
        <span v-else>
          <span>{{ $t("list.NotFoundSome") }}</span>
          <span class="ml-3 mr-1">{{ $t("list.QueryLeftQuote") }}</span>
          <span>{{ query }}</span>
          <span class="ml-1 mr-3">{{ $t("list.QueryRightQuote") }}</span>
          <span>{{ $t("list.SomeAbout") }}</span>
        </span>
      </span>
      <span v-else>
        <span v-if="$i18n.locale == 'eng'">
          <span>{{ $t("list.QueryResult") }}</span>
          <span class="ml-3 mr-1">{{ $t("list.QueryLeftQuote") }}</span>
          <span>{{ query }}</span>
          <span class="ml-1">{{ $t("list.QueryRightQuote") }}</span>
        </span>
        <span v-else>
          <span class="mr-1">{{ $t("list.QueryLeftQuote") }}</span>
          <span>{{ query }}</span>
          <span class="mx-1">{{ $t("list.QueryRightQuote") }}</span>
          <span>{{ $t("list.QueryResult") }}</span>
        </span>
      </span>
    </h1>
    <p class="text-muted mt-4 mb-0">
      <span v-if="load">{{ $t("list.MayCost") }}</span>
      <span v-else-if="!found">{{ $t("list.ContactPlease") }}</span>
      <span v-else>
        <span class="mr-1">{{ $t("list.Approx") }}</span>
        <span>{{ total.toLocaleString() }}</span>
        <span v-if="total <= 1 && $i18n.locale == 'eng'" class="ml-1">{{
          $t("list.Total").slice(0, -1)
        }}</span>
        <span v-else class="ml-1">{{ $t("list.Total") }}</span>
      </span>
    </p>
  </div>
</template>

<script>
export default {
  name: "ResultHead",
  props: ["load", "found", "query", "total"]
};
</script>

<style scoped lang="scss"></style>

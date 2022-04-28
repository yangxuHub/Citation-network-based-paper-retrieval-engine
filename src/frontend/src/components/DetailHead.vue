<template>
  <div class="detail-head">
    <h1 class="mt-4 pt-2 mb-0">
      <span v-if="load">{{ $t("list.Searching") }}</span>
      <span v-else-if="!found">{{ $t("list.NotFound") }}</span>
    </h1>
    <p class="text-muted mt-4 mb-0">
      <span v-if="load">{{ $t("list.MayCost") }}</span>
      <span v-else-if="!found">{{ $t("list.ContactPlease") }}</span>
    </p>
  </div>
</template>

<script>
export default {
  name: "DetailHead",
  props: ["load", "found"],
  methods: {
    handleLink(link) {
      window.open(link, "_blank");
    }
  }
};
</script>

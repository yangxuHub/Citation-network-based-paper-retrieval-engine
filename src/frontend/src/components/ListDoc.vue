<template>
  <div class="list-doc">
    <div v-for="(doc, dIndex) in docs" :key="dIndex">
      <FeatDoc :doc="doc" :highlight="highlight" />
    </div>
  </div>
</template>

<script>
import FeatDoc from "@/components/FeatDoc.vue";

export default {
  name: "ListDoc",
  props: ["docs", "highlight"],
  components: { FeatDoc }
};
</script>

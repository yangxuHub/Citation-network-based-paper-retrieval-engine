<template>
  <div class="link-doc">
    <ul class="list-unstyled m-0">
      <li v-if="doc.inCitations > 0">
        <el-tooltip
          effect="dark"
          :content="$t('detail.CitedCount')"
          placement="top"
        >
          <div>
            <font-awesome-icon :icon="['fas', 'quote-left']" />
            <span class="icon-text">{{
              doc.inCitations.toLocaleString()
            }}</span>
          </div>
        </el-tooltip>
      </li>
      <li v-if="doc.pdf_url && doc.pdf_url.length">
        <el-link @click="handleLink(doc.pdf_url[0])">
          <font-awesome-icon :icon="['fas', 'file-pdf']" />
          <span class="icon-text">PDF</span>
        </el-link>
      </li>
      <li v-if="doc.code_url && doc.code_url.length">
        <el-popover placement="bottom" trigger="click">
          <div class="feat-code">
            <ul class="list-unstyled m-0">
              <li v-for="(item, cIndex) in doc.code_url" :key="cIndex">
                <el-link
                  :underline="false"
                  @click="handleLink(item.url)"
                  class="teal-text py-1"
                >
                  <font-awesome-icon :icon="['fas', 'code']" />
                  <span class="ml-2">{{ item.url }}</span>
                </el-link>
              </li>
            </ul>
          </div>
          <el-link slot="reference">
            <font-awesome-icon :icon="['fas', 'code']" />
            <span class="icon-text">{{ $t("detail.Code") }}</span>
          </el-link>
        </el-popover>
      </li>
      <li>
        <el-link v-if="doc.url" @click="handleLink(doc.url)">
          <font-awesome-icon :icon="['fas', 'dice-d6']" />
          <span class="icon-text">{{ $t("detail.Source") }}</span>
        </el-link>
      </li>
      <li v-if="!fFilm && doc.video_url && doc.video_url.length">
        <el-popover placement="bottom" trigger="click" width="400">
          <div class="feat-video">
            <ul class="list-unstyled m-0">
              <li v-for="(url, vIndex) in doc.video_url" :key="vIndex">
                <el-link
                  :underline="false"
                  @click="handleLink(url)"
                  class="teal-text py-1"
                >
                  <font-awesome-icon :icon="['fas', 'video']" />
                  <span class="ml-2">{{ url }}</span>
                </el-link>
              </li>
            </ul>
          </div>
          <el-link slot="reference">
            <font-awesome-icon :icon="['fas', 'video']" />
            <span class="icon-text">{{ $t("detail.Video") }}</span>
          </el-link>
        </el-popover>
      </li>
      <li v-if="doc.slide_url && doc.slide_url.length">
        <el-link @click="handleLink(doc.slide_url[0])">
          <font-awesome-icon :icon="['fas', 'file-powerpoint']" />
          <span class="icon-text">{{ $t("detail.Slide") }}</span>
        </el-link>
      </li>
      <li v-if="doc.dataset_url && doc.dataset_url.length">
        <el-link @click="handleLink(doc.dataset_url[0])">
          <font-awesome-icon :icon="['fas', 'database']" />
          <span class="icon-text">{{ $t("detail.Dataset") }}</span>
        </el-link>
      </li>
      <li v-if="doc.blog_urls && doc.blog_urls.length && !fBlog">
        <el-popover placement="bottom" trigger="click" width="350">
          <div v-loading="doc.fBlogLoad" class="feat-blog">
            <span v-if="doc.fBlogLoad" style="opacity: 0;">
              <p class="m-0">{{ $t("detail.NoBlog") }}</p>
              <p class="m-0">{{ $t("detail.NoBlog") }}</p>
            </span>
            <p v-else-if="!doc.listBlog.length" class="m-0">
              {{ $t("detail.NoBlog") }}
            </p>
            <ul v-else class="list-unstyled m-0">
              <li v-for="(item, bIndex) in doc.listBlog" :key="bIndex">
                <font-awesome-icon :icon="['fas', 'rss']" class="mr-2" />
                <el-tooltip :content="item.title" placement="top">
                  <el-link
                    @click="handleLink(item.url)"
                    :underline="false"
                    class="teal-text py-1"
                    style="transform: translateY(-1px);"
                  >
                    <span>{{ item.title.slice(0, dropMax) }}</span
                    ><span v-if="item.title.length > dropMax">...</span>
                  </el-link>
                </el-tooltip>
                <el-tag size="mini" type="info" effect="plain" class="ml-2">
                  {{ item.source }}
                </el-tag>
              </li>
            </ul>
          </div>
          <el-link slot="reference">
            <font-awesome-icon :icon="['fas', 'rss']" />
            <span class="icon-text">{{ $t("detail.Blog") }}</span>
          </el-link>
        </el-popover>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "LinkDoc",
  props: ["doc"],
  data: function() {
    return {
      dropMax: 23
    };
  },
  computed: {
    fFilm: function() {
      return ["/film", "/full"].includes(this.$route.path);
    },
    fBlog: function() {
      return ["/full"].includes(this.$route.path);
    },
    ipLocal: function() {
      return this.$store.state.ipLocal;
    }
  },
  mounted: function() {
    this.blogInit();
  },
  methods: {
    blogInit() {
      this.axios
        .get(
          "/blog?type=BLOG&paper_id=" +
            this.doc._id +
            "&user_ip=" +
            this.ipLocal
        )
        .then(response => {
          // console.log(response.data);
          this.doc.listBlog = response.data.hits;
        })
        .catch(error => {
          console.error(error);
          // this.$message.error(this.$t("list.UnknownError"));
        })
        .finally(() => {
          this.doc.fBlogLoad = false;
        });
    },
    handleLink(link) {
      window.open(link, "_blank");
    }
  }
};
</script>

<style scoped lang="scss">
.link-doc {
  .el-link {
    color: #77a7d8;
  }
  ul li {
    font-size: 14px;
    color: #4f4f4f;
    display: inline-block;
    .icon-text {
      margin-left: 0.375rem;
    }
    .el-link {
      font-size: 14px;
      color: #4f4f4f;
      transform: translateY(-1px);
    }
    &:not(:last-child) {
      margin-right: 0.875rem;
    }
  }
}
</style>

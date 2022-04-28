<template>
  <div class="document container">
    <div class="px-3">
      <el-row v-if="fLoad || !fFound" class="row-head">
        <el-col :span="24" class="col-head">
          <DetailHead :load="fLoad" :found="fFound" />
        </el-col>
      </el-row>
      <el-row v-loading="fLoad" class="row-detail">
        <!-- Title -->
        <el-col :span="24" class="col-title mt-3 mb-1">
          <p class="mb-2">
            <span v-if="!!detailDoc.importance"
              >重要性分数: {{ detailDoc.importance }}</span
            >
            <span v-if="!!detailDoc.importance && !!detailDoc.year">, </span>
            <span v-if="!!detailDoc.year"> 年份：{{ detailDoc.year }}</span>
          </p>
          <h1 v-if="!!detailDoc.title">{{ detailDoc.title }}</h1>
          <el-divider></el-divider>
        </el-col>
        <!--引文关系图展示-->
        <el-col v-if="!fLoad">
          <Show
            :load="fLoad"
          />
          <div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import DetailHead from "@/components/DetailHead.vue";
import Show from "@/components/Show.vue";

export default {
  name: "DocumentDetails",
  components: { DetailHead, Show },
  data: function() {
    return {
      fLoad: true,
      fFound: true,
      triadList: [],
      entityList: [],
      dataList:[],
      linkList:[],
      queryId: "",
      detailDoc: {},
      detailBlog: [],
      detailVideo: [],
      thumbHeight: "167px",
      posStartVideo: 0,
      blogMax: 4,
      fExpandBlog: false,
      radioVideo: 0,
      fFrameShow: false,
      fFrameLoad: false,
      timerFrame: null,
      cntFrame: 0
    };
  },
  computed: {
    searchInput: function() {
      return this.$store.state.searchInput;
    },
    videoURL: function() {
      return !!this.detailDoc.video_url && this.detailDoc.video_url.length
        ? this.detailDoc.video_url[this.radioVideo]
        : "";
    },
    videoID: function() {
      return !!this.detailDoc.video_url && this.detailDoc.video_url.length
        ? this.detailDoc.video_id[this.radioVideo]
        : "";
    },
    videoSource: function() {
      return !!this.detailDoc.video_url && this.detailDoc.video_url.length
        ? this.handleSource(this.videoURL)
        : "";
    },
    fYoutube: function() {
      return this.videoURL.indexOf("youtube") != -1;
    },
    fVimeo: function() {
      return this.videoURL.indexOf("vimeo") != -1;
    },
    fBilibili: function() {
      return this.videoURL.indexOf("bilibili") != -1;
    },
    videoPlayer() {
      return this.$refs.dialogFrame.player;
    },
    ipLocal: function() {
      return this.$store.state.ipLocal;
    }
  },
  mounted: function() {
    this.routeCheck();
    this.initTimer();
    window.addEventListener("resize", () => {
      this.thumbHeight =
        Math.floor(document.querySelectorAll(".frame-thumb")[0].offsetHeight) +
        "px";
    });
  },
  methods: {
    routeCheck() {
      const routeQuery = this.$route.query;
      const id = routeQuery.id;
      if (!id) {
        console.log("Redirect to home.");
        this.$router.push({ path: "/" });
        return;
      }
      this.queryId = id;
      this.querySubmit();
    },
    initTimer() {
      var timer = setInterval(() => {
        if (
          document.querySelectorAll(".frame-thumb") &&
          document.querySelectorAll(".frame-thumb").length
        ) {
          this.thumbHeight =
            Math.floor(
              document.querySelectorAll(".frame-thumb")[0].offsetHeight
            ) + "px";
          clearInterval(timer);
          timer = null;
        }
      }, 250);
    },
    querySubmit() {
      console.log("Start detailing...");
      [this.fLoad, this.fFound] = [true, true];
      this.detailDoc = [];
      this.docSubmit();
    },
    docSubmit() {
      this.axios
        .get(
          "/citations?type=CITATIONS&" +
            "sid=" +
            this.queryId +
            "&depth=1" +
            "&length=10"
        )
        .then(response => {
          const responseData = this.COMMON.toJson(response.data);
          this.detailDoc = responseData.hit;
        })
        .catch(error => {
          console.error(error);
          this.fFound = false;
          // this.$message.error(this.$t("list.UnknownError"));
        })
        .finally(() => {
          this.fLoad = false;
        });
    },
    submitVideo() {
      if (!this.searchInput) {
        return;
      }
      this.axios
        .get(
          "/single_video_location?type=SINGLE_VIDEO_LOCATION&query=" +
            this.searchInput +
            "&video_id=" +
            this.videoID +
            "&user_ip=" +
            this.ipLocal
        )
        .then(response => {
          // console.log(response.data);
          this.detailVideo = response.data.hits.hit;
        })
        .catch(error => {
          console.error(error);
          // this.$message.error(this.$t("list.UnknownError"));
        });
    },
    handleAuth(auth) {
      this.$router.push({
        path: "/auth",
        query: { id: auth.id, name: auth.name }
      });
    },
    handleVenue(affi) {
      this.$router.push({
        path: "/affi",
        query: { id: affi.venue_id, name: affi.venue }
      });
    },
    handleSource(url) {
      var src = "";
      if (this.fYoutube) {
        src = "https://youtu.be/" + this.getYoutubeId(url);
      } else if (this.fVimeo) {
        src = "https://vimeo.com/" + this.getVimeoId(url);
      } else if (this.fBilibili) {
        src = "https://www.bilibili.com/video/" + this.getBiliId(url);
      } else {
        src = url;
      }
      return src;
    },
    handlePos(pos) {
      const match = pos.time_start.match(/^.*(\d+):(\d+\.\d+).*/);
      const time = +match[1] * 60 + +match[2];
      // console.log(match, time);
      if (this.fYoutube) {
        this.videoPlayer.seekTo(time, true);
      } else if (this.fVimeo) {
        this.videoPlayer.setCurrentTime(time);
      } else if (this.fBilibili) {
        this.$message(this.$t("detail.NotSeek"));
      } else {
        this.$message(this.$t("detail.NotSeek"));
      }
    },
    handleVideo(url) {
      if (this.fYoutube) {
        return "https://www.youtube.com/embed/" + this.getYoutubeId(url);
      } else if (this.fVimeo) {
        return "https://player.vimeo.com/video/" + this.getVimeoId(url);
      } else if (this.fBilibili) {
        return (
          "https://player.bilibili.com/player.html?" +
          this.getBiliId(url) +
          "&high_quality=1&danmaku=0"
        );
      } else {
        return url;
      }
    },
    getVideoSourse(url) {
      if (!url) {
        return;
      }
      var matches = url.match(
        /^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:/\n?=]+)/im
      );
      return matches[1];
    },
    getYoutubeId(url) {
      const reg = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
      const match = url.match(reg);
      return match && match[2].length === 11 ? match[2] : null;
    },
    getVimeoId(url) {
      const reg = /^.*(vimeo.com\/|video\/)([^#&?]*).*/;
      const match = url.match(reg);
      return match && /^\d+$/.test(match[2]) ? match[2] : null;
    },
    getBiliId(url) {
      const reg = /^.*(video\/|\?aid=|&aid=|\?bvid=|&bvid=)([^#&?]*).*/;
      const match = url.match(reg);
      return match
        ? match[2].slice(0, 2) == "av"
          ? "aid=" + match[2].slice(2)
          : "bvid=" + match[2]
        : null;
    },
    dialogOpen(index) {
      // Init
      this.submitVideo();
      this.radioVideo = index;
      this.fFrameShow = true;
      this.fFrameLoad = true;
      if (this.timerFrame) {
        clearInterval(this.timerFrame);
        this.timerFrame = null;
      }
      // Timer
      this.cntFrame = 0;
      this.timerFrame = setInterval(() => {
        console.log("Start loading...");
        var htmlFrame = document.getElementsByClassName("dialog-frame")[0];
        this.cntFrame = this.cntFrame + 1;
        if (
          ((this.fBilibili || this.fVimeo || this.fYoutube) &&
            htmlFrame.innerHTML.length > 50) ||
          htmlFrame.contentWindow ||
          htmlFrame.contentDocument
        ) {
          clearInterval(this.timerFrame);
          this.timerFrame = null;
          setTimeout(() => {
            console.log("Load success");
            this.fFrameLoad = false;
          }, 500);
        }
        if (this.cntFrame >= 16) {
          this.$message({
            showClose: true,
            duration: 0,
            message: this.$t("detail.VideoLoadError"),
            type: "error"
          });
          clearInterval(this.timerFrame);
          this.timerFrame = null;
        }
      }, 500);
    },
    dialogClose() {
      this.fFrameShow = false;
      if (this.timerFrame) {
        clearInterval(this.timerFrame);
        this.timerFrame = null;
      }
    },
    handleLink(link) {
      window.open(link, "_blank");
    }
  }
};
</script>

<style scoped lang="scss">
.document {
  .row-detail {
    min-height: 40vh;
    .col-video {
      .frame-thumb {
        width: 100%;
        height: 0;
        padding-bottom: 56.25%;
        overflow: hidden;
        background-position: center center;
        background-repeat: no-repeat;
        background-size: cover;
        .image-slot {
          height: 100%;
          display: flex;
          justify-content: center;
          align-items: center;
        }
      }
      .frame-type {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        z-index: 1;
      }
      .frame-mask {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #00000066;
        opacity: 0;
        z-index: 1;
        &:hover {
          opacity: 1;
        }
      }
    }
    .col-blog {
      .blog-link {
        color: #212529;
        &:hover {
          color: #77a7d8;
        }
      }
    }
  }
  .video-dialog ::v-deep {
    .responsive-panel {
      min-height: 100%;
    }
    .dialog-frame {
      position: relative;
      padding-bottom: 56.25%;
      height: 0;
      overflow: hidden;
      min-width: 100%;
      iframe,
      object,
      embed {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
      }
    }
    .dialog-frame.other {
      padding-bottom: 0;
      height: 80vh;
    }
    .el-dialog.is-fullscreen {
      background: rgba(0, 0, 0, 0.8);
    }
    .el-dialog__headerbtn i {
      font-size: 2.5rem;
    }
  }
}
</style>

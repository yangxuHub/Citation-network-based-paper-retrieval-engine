<template>
  <div class="feat-doc">
    <p v-if="doc.title" class="doc-title mb-1">
      <el-link @click="handleDoc" :underline="false">
        <h6 v-html="highlight(doc.title)" class="m-0"></h6>
      </el-link>
    </p>
    <ul class="doc-attr list-unstyled mb-1">
      <li v-if="doc.inCitationsCount" class="text-capitalize">
        引用量：{{ doc.inCitationsCount }}
      </li>
      <li v-if="doc.outCitationsCount">参考量：{{ doc.outCitationsCount }}</li>
      <li v-if="doc.year">年份：{{ doc.year }}</li>
      <li v-if="doc.importance">重要性分数{{ doc.importance }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "FeatDoc",
  props: ["doc", "highlight"],
  data: function() {
    return {
      authMax: 4,
      absMax: 220,
      dropMax: 25,
      linkList: [],
      dataList: [],
      entityList: [],
      triadList: [],
      docList: []
    };
  },
  computed: {
    searchInput: function() {
      return this.$store.state.searchInput;
    },
    fFilm: function() {
      return ["/film"].includes(this.$route.path);
    },
    ipLocal: function() {
      return this.$store.state.ipLocal;
    }
  },
  methods: {
    //发送请求函数
    //在此发送请求获取引文关系信息
    handleDoc() {
      this.entityList = [];
      this.triadList = [];
      this.docList = [];
      this.axios
        .get(
          "/citations?type=CITATIONS&" +
            "sid=" +
            this.doc.Sid +
            "&depth=1" +
            "&length=10"
        )
        .then(response => {
          const responseData = this.COMMON.toJson(response.data);
          this.detailDoc = responseData.hit;
          // console.log(this.detailDoc.outCitations_shrink);
          //sid当节点，整理节点信息
          //把中心节点也就是本论文的节点放入
          //inCitations该论文被引用
          //outCitations该论文引用别人 即参考
          var center_entity =
            this.detailDoc.title.substring(0, 6) + this.detailDoc.year;
          if (this.entityList.indexOf(center_entity) <= -1) {
            this.entityList.push(center_entity);
            this.docList.push({
              title: this.detailDoc.title,
              year: this.detailDoc.year,
              importance: this.detailDoc.importance,
              inCitationsCount: this.detailDoc.inCitationsCount,
              outCitationsCount: this.detailDoc.outCitationsCount,
              sid: this.detailDoc.Sid
            });
          }
          this.detailDoc.outCitations_shrink.map((item, key) => {
            //遍历第一层shrink
            if (key <= 5) {
              if (
                this.entityList.indexOf(
                  item.title.substring(0, 6) + this.detailDoc.year
                ) <= -1
              ) {
                this.entityList.push(
                  item.title.substring(0, 6) + this.detailDoc.year
                );
                this.docList.push({
                  title: item.title,
                  year: item.year,
                  importance: item.importance,
                  inCitationsCount: item.inCitationsCount,
                  outCitationsCount: item.outCitationsCount,
                  sid: item.Sid
                });
              }
              this.triadList.push({
                entity_one: center_entity,
                entity_two: item.title.substring(0, 6) + this.detailDoc.year,
                relation: "outCitations"
              });
              //遍历第二层 out
              var second_shrink = item.outCitations_shrink;
              second_shrink.map((subitem, subkey) => {
                if (subkey <= 5) {
                  //判断sid是否已经存在
                  if (
                    this.entityList.indexOf(
                      subitem.title.substring(0, 6) + this.detailDoc.year
                    ) <= -1
                  ) {
                    //如果不存在，则加入到实体列表中
                    this.entityList.push(
                      subitem.title.substring(0, 6) + this.detailDoc.year
                    );
                    this.docList.push({
                      title: subitem.title,
                      year: subitem.year,
                      importance: subitem.importance,
                      inCitationsCount: subitem.inCitationsCount,
                      outCitationsCount: subitem.outCitationsCount,
                      sid: subitem.Sid
                    });
                  }
                  this.triadList.push({
                    entity_one:
                      item.title.substring(0, 6) + this.detailDoc.year,
                    entity_two:
                      subitem.title.substring(0, 6) + this.detailDoc.year,
                    relation: "outCitations"
                  });
                }
              });
              //遍历第二层in
              var second_in_shrink = item.inCitations_shrink;
              second_in_shrink.map((subitem, subkey) => {
                if (subkey <= 5) {
                  //判断sid是否已经存在
                  if (
                    this.entityList.indexOf(
                      subitem.title.substring(0, 6) + this.detailDoc.year
                    ) <= -1
                  ) {
                    //如果不存在，则加入到实体列表中
                    this.entityList.push(
                      subitem.title.substring(0, 6) + this.detailDoc.year
                    );
                    this.docList.push({
                      title: subitem.title,
                      year: subitem.year,
                      importance: subitem.importance,
                      inCitationsCount: subitem.inCitationsCount,
                      outCitationsCount: subitem.outCitationsCount,
                      sid: subitem.Sid
                    });
                  }
                  this.triadList.push({
                    entity_one:
                      subitem.title.substring(0, 6) + this.detailDoc.year,
                    entity_two:
                      item.title.substring(0, 6) + this.detailDoc.year,
                    relation: "inCitations"
                  });
                }
              });
            }
          });
          //添加incitations节点和边
          this.detailDoc.inCitations_shrink.map((item, key) => {
            //遍历第一层shrink
            if (key <= 5) {
              if (
                this.entityList.indexOf(
                  item.title.substring(0, 6) + this.detailDoc.year
                ) <= -1
              ) {
                this.entityList.push(
                  item.title.substring(0, 6) + this.detailDoc.year
                );
                this.docList.push({
                  title: item.title,
                  year: item.year,
                  importance: item.importance,
                  inCitationsCount: item.inCitationsCount,
                  outCitationsCount: item.outCitationsCount,
                  sid: item.Sid
                });
              }
              this.triadList.push({
                entity_one: item.title.substring(0, 6) + this.detailDoc.year,
                entity_two: center_entity,
                relation: "inCitations"
              });
              //遍历第二层 in
              var second_shrink = item.inCitations_shrink;
              second_shrink.map((subitem, subkey) => {
                if (subkey <= 5) {
                  //判断sid是否已经存在
                  if (
                    this.entityList.indexOf(
                      subitem.title.substring(0, 6) + this.detailDoc.year
                    ) <= -1
                  ) {
                    //如果不存在，则加入到实体列表中
                    this.entityList.push(
                      subitem.title.substring(0, 6) + this.detailDoc.year
                    );
                    this.docList.push({
                      title: subitem.title,
                      year: subitem.year,
                      importance: subitem.importance,
                      inCitationsCount: subitem.inCitationsCount,
                      outCitationsCount: subitem.outCitationsCount,
                      sid: subitem.Sid
                    });
                  }
                  this.triadList.push({
                    entity_one:
                      subitem.title.substring(0, 6) + this.detailDoc.year,
                    entity_two:
                      item.title.substring(0, 6) + this.detailDoc.year,
                    relation: "inCitations"
                  });
                }
              });
              //遍历第二层out
              var second_out_shrink = item.outCitations_shrink;
              second_out_shrink.map((subitem, subkey) => {
                if (subkey <= 5) {
                  //判断sid是否已经存在
                  if (
                    this.entityList.indexOf(
                      subitem.title.substring(0, 6) + this.detailDoc.year
                    ) <= -1
                  ) {
                    //如果不存在，则加入到实体列表中
                    this.entityList.push(
                      subitem.title.substring(0, 6) + this.detailDoc.year
                    );
                    this.docList.push({
                      title: subitem.title,
                      year: subitem.year,
                      importance: subitem.importance,
                      inCitationsCount: subitem.inCitationsCount,
                      outCitationsCount: subitem.outCitationsCount,
                      sid: subitem.Sid
                    });
                  }
                  this.triadList.push({
                    entity_one:
                      item.title.substring(0, 6) + this.detailDoc.year,
                    entity_two:
                      subitem.title.substring(0, 6) + this.detailDoc.year,
                    relation: "inCitations"
                  });
                }
              });
            }
          });
          //生成节点信息
          // console.log(this.entityList);
          // console.log(this.triadList);
          // console.log(this.docList);
          this.entityList.forEach(item => {
            let DataTemp = {
              // itemStyle : {
              //     color:colors[key%13],

              // },
              itemStyle: null,
              value: 20,
              symbolSize: 30,
              name: item
            };
            this.dataList.push(DataTemp);
          });

          //生成边信息
          this.triadList.forEach(item => {
            let LinkTemp = {
              source: item.entity_one,
              target: item.entity_two,
              //symbolSize: [5, 20],
              label: {
                normal: {
                  show: true,
                  formatter: ""
                  //这里用来设置关系边显示的内容
                }
              }
            };
            this.linkList.push(LinkTemp);
          });
          this.$store.commit("updateGraphData", {
            linkList: this.linkList,
            dataList: this.dataList,
            docList: this.docList
          });
        })
        .catch(error => {
          console.error(error);
          this.fFound = false;
          // this.$message.error(this.$t("list.UnknownError"));
        })
        .finally(() => {
          this.fLoad = false;
        });
      this.$router.push({
        path: "/full",
        query: { id: this.doc.Sid }
      });
    },
    handleAuth(auth) {
      this.$router.push({
        path: "/auth",
        query: { id: auth.id, name: auth.name }
      });
    }
  }
};
</script>

<style scoped lang="scss">
.feat-doc {
  .el-link {
    color: #77a7d8;
  }
  .doc-attr li {
    font-size: 13px;
    color: #4f4f4f;
    display: inline-block;
    .el-link {
      font-size: 13px;
      color: #4f4f4f;
      transform: translateY(-1px);
    }
    &:not(:first-child)::before {
      content: "\00A0•\00A0";
      font-size: 0.75rem;
      padding: 0 0.25rem;
    }
  }
  .doc-abs {
    font-size: 14px;
    color: #424242;
    margin-bottom: 0;
    .el-button {
      font-size: 11px;
      margin-left: 0.5rem;
      padding: 2px 6px;
    }
  }
}
</style>

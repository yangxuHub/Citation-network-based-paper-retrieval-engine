<template>
  <div>
    <el-col :span="16">
      <div id="myChart" :style="{ width: '100%', height: '500px' }"></div>
    </el-col>
    <!-- Blog -->
    <el-col
      v-if="docList.length"
      :span="8"
      class="col-blog mt-3"
      :style="{ overflow: 'auto', height: '450px' }"
    >
      <ul class="list-unstyled mb-2">
        <li
          v-for="(doc, Index) in docList.slice(0, docMax)"
          :key="Index"
          class="py-2 py-md-1"
          style="border-bottom: 1px solid #e9eeee"
        >
          <div class="d-flex justify-content-between">
            <div class="w-100">
              <el-link
                :underline="false"
                @click="handleLink(doc.url)"
                class="doc-link"
                style="margin-bottom: 2px;"
              >
                <p class="m-0" style="font-size: 15px;">{{ doc.title }}</p>
              </el-link>
              <p v-if="doc.year" class="grey-text m-0" style="font-size: 13px;">
                {{ doc.year }}
              </p>
            </div>
            <div
              class="d-flex justify-content-end align-items-end"
              style="min-width: 70px"
            >
              <el-tag
                size="mini"
                type="info"
                effect="plain"
                style="margin-bottom: 2px;"
              >
                {{ (doc.importance + "").substring(0, 5) }}
              </el-tag>
            </div>
          </div>
        </li>
      </ul>
    </el-col>
    <div v-if="docList.length > 5" class="text-center">
      <el-link
        @click="
          docMax = fExpandDoc ? 5 : docList.length;
          fExpandDoc = !fExpandDoc;
        "
        class="teal-text"
      >
        <span v-if="!fExpandDoc">展开</span><span v-else>收起</span>
      </el-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "Show",
  props: ["load"],
  data() {
    return {
      msg: "Welcome to Your Vue.js App",
      dataList: [],
      linkList: [],
      docList: [],
      option: {},
      docMax: 5,
      fExpandDoc: false
    };
  },
  mounted() {
    this.dataList = this.$store.state.dataList;
    this.linkList = this.$store.state.linkList;
    this.docList = this.$store.state.docList;
    this.drawLine();
  },
  methods: {
    drawLine() {
      // console.log(this.$store.state.dataList);
      // 基于准备好的dom，初始化echarts实例
      let myChart = this.$echarts.init(document.getElementById("myChart"));
      // 绘制图表
      this.option = {
        title: {
          text: "引文关系图"
        },
        tooltip: {
          trigger: "item",
          triggerOn: "mousemove",
          formatter: function(params) {
            if (params.data.sourse || params.data.target) {
              //这个内容就是提示时显示的内容。
              return params.data.label.formatter;
            } else {
              //在关系图里，能进到这里的数据项，应该只有节点和关系两种，所以不是关系就只能是节点……
              return params.name;
            }
          }
          //这里可以设置边关系的提示信息。
          //可以写一个函数，返回关系的名称
        },
        animationDuration: 1500,
        animationEasingUpdate: "quinticInOut",
        series: [
          {
            name: "引文关系图",
            type: "graph",
            layout: "force",
            data: this.$store.state.dataList, //存放节点信息
            links: this.$store.state.linkList, //存放边信息
            roam: true,
            //设置布局
            force: {
              initLayout: "circular", //初始布局
              repulsion: 500 //斥力大小
            },
            //设置是否可以放大或者移动
            focusNodeAdjacency: true,
            itemStyle: {
              normal: {
                borderColor: "#fff",
                borderWidth: 1,
                shadowBlur: 10,
                shadowColor: "rgba(0, 0, 0, 0.3)"
              }
            },
            label: {
              normal: {
                show: true
              }
            },
            edgeSymbol: ["circle", "arrow"],
            edgeSymbolSize: [4, 10],
            edgeLabel: {
              normal: {
                textStyle: {
                  fontSize: 6
                  //此处的fontsize是关系直接显示的文字的大小
                }
              }
            },
            lineStyle: {
              normal: {
                opacity: 0.9,
                width: 2
                //curveness: 0.2
              }
            },
            emphasis: {
              lineStyle: {
                width: 3
              }
            }
          }
        ]
      };
      myChart.setOption(this.option);
      // 点击node节点的事件
      myChart.on("click", function(param) {
        // console.log('node节点的数组---->', param.data);  // 打印出param, 可以看到里边有很多参数可以使用
        // let key = 'symbolSize'
        // let value = 80
        //
        // param.data[key] = value

        //获取节点点击的数组序号
        //var arrayIndex = param.dataIndex;
        // console.log('arrayIndex---->', arrayIndex);
        // console.log('name---->', param.name);
        if (param.dataType == "node") {
          // alert("点击了节点" + param.name)
        } else {
          // alert("点击了边" + param.value)
        }
      });
    }
  }
};
</script>

<template>
  <section>
    <el-row class="margin_bottom-medium">
      <div class="div-flex">
        <div style="text-align: left; flex-grow: 1; font-weight: bold;">{{ newsData.title }}</div>
        <el-radio-group
          size="mini"
          v-model="newsDataCategory"
          v-if="newsData.chooseItems.length > 1"
          @change="categoryChoosed(newsDataCategory)"
        >
          <el-radio-button
            :id="singleValue"
            :label="singleValue"
            v-for="singleValue in newsData.chooseItems"
            :key="singleValue"
          ></el-radio-button>
        </el-radio-group>
      </div>
    </el-row>
    <div style="text-align: left">
      <div
        class="scrollbar-div"
        style="height: 300px"
        v-if="newsDataShow.data.length > 0"
      >
        <div
          class="margin_bottom-mini margin_right-small"
          v-for="(link, i) in newsDataShow.data"
          :key="link"
        >
          <el-link
            type="primary"
            :href="link.url"
            style="color: #606266"
            target="_blank"
            :underline="false"
            >{{ i + 1 + "." + link.name }}
          </el-link>
          <br />
        </div>
      </div>
      <div
        class="better_font_style"
        v-if="newsDataShow.data.length == 0"
        style="
          margin-top: 15px;
          text-align: left;
          font-size: 14px;
          color: #606266;
        "
      >
        源站访问失败（宕机或限制），请稍后再试
      </div>
    </div>
    <div
      class="better_font_style"
      style="
        margin-top: 15px;
        text-align: right;
        font-size: 12px;
        color: #909399;
      "
    >
      {{ "更新时间：" + newsDataShow.time }}
    </div>
  </section>
</template>
<script>
import { deepClone } from "../../js/common";

export default {
  name: "newsModule",
  props: {
    newsData: {},
  },
  watch: {
    newsData(newVal, oldVal) {
      this.init();
    },
  },
  data() {
    return {
      newsDataCategory: [],
      newsDataShow: {
        data: [],
      },
    };
  },
  methods: {
    init() {
      this.newsDataCategory = this.newsData.choose;
      this.newsDataShow = deepClone(this.newsData.show);
      this.$emit("done");
    },
    categoryChoosed(newsDataCategory) {
      for (let x = 0; x < this.newsData.data.length; x++) {
        if (this.newsData.data[x].title == newsDataCategory) {
          this.newsDataShow = deepClone(this.newsData.data[x]);
          return;
        }
      }
    },
  },
  mounted() {
    this.init();
  },
};
</script>
</style>

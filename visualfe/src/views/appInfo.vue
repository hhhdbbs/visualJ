<template>
  <div>
    <userRouter />
    <div class="d-flex" style="padding:20px 10px">
      <h2 style="front-size:20px;font-weight:500">遥感图像处理</h2>
      <v-btn text color="primary" class="ml-auto" @click="saveApp">保存</v-btn>
    </div>
    <div
      class="d-flex"
      @mousedown="startOperator($event)"
      @mousemove="moveOperator($event)"
      @mouseup="endOperator($event)"
    >
      <v-card width="20%">
        <v-card-title>算子列表</v-card-title>
        <v-card-text>
          <v-list dense>
            <v-list-item-group v-model="selectedItem" color="primary">
              <v-list-item v-for="item in Images" :key="item.id">
                <v-list-item-content>
                  <v-list-item-title @mousedown="dragIt(item)">
                    {{ item.name }}
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-card-text>
      </v-card>
      <v-card class="flex-grow-1">
        <v-card-title>遥感图像任务编排</v-card-title>
        <v-card-text
          ><DAGBoard
            id="svgContent"
            :nodes="nodes"
            :lines="lines"
            @setInfo="setInfo"
        /></v-card-text>
      </v-card>
      <div width="20%" height="100%">
        <OperatorInfo
          :abledInfo="currentInfo.abledInfo"
          :disabledInfo="currentInfo.disabledInfo"
        />
      </div>

      <OPoint
        v-if="dragValue && dragValue.dragStatus"
        :pos_x="dragValue.pos_x"
        :pos_y="dragValue.pos_y"
        :taskID="dragValue.taskID"
        :opInformation="dragValue.opInformation"
      />
    </div>
  </div>
</template>
<script>
import userRouter from "../components/router/userRouter.vue"
import OPoint from "../components/app/OPoint.vue";
import DAGBoard from "../components/app/DAGBoard.vue";
import OperatorInfo from "../components/app/OperatorInfo.vue";
export default {
  name: "AppInfo",
  components: { OPoint, DAGBoard, OperatorInfo,userRouter },
  data() {
    return {
      currentInfo: { disabledInfo: [], abledInfo: [] },
      selectedItem: "",
      Images: [],
      dragValue: null,
      nodes: [],
      lines: [],
      Pos: {},
      appID: null
    };
  },
  mounted() {
    this.appID = this.$route.query.appId;
    document.getElementById("svgContent").oncontextmenu = function(e) {
      return false;
    };
    this.$axios.post("/app/view_operator_list/").then(res => {
      this.Images = res.data.operatorList;
    });
    this.$axios
      .get("/app/view_app/", { params: { appID: this.appID } })
      .then(res => {
        this.nodes = res.data.nodes;
        this.lines = res.data.lines;
      });
    // this.nodes = JSON.parse(
    //   '[{"pos_x":88,"pos_y":46,"taskID":9084,"opInformation":{"name":"预处理","id":1,"input_num":1,"output_num":1,"type":"Task","info":[{"name":"输入文件名","value":"input"},{"name":"输出文件名","value":"output"},{"name":"紫外线阈值","value":"op"}]}},{"pos_x":61,"pos_y":243,"taskID":2849,"opInformation":{"name":"彩色增强","id":2,"input_num":1,"output_num":2,"type":"Task","info":[{"name":"输入文件名","value":"input"},{"name":"输出文件名","value":"output"}]}},{"pos_x":304,"pos_y":154,"taskID":5490,"opInformation":{"name":"预处理","id":1,"input_num":1,"output_num":1,"type":"Task","info":[{"name":"输入文件名","value":"input"},{"name":"输出文件名","value":"output"},{"name":"紫外线阈值","value":"op"}]}}]'
    // );
    // this.lines = JSON.parse(
    //   '[{"from_node_circle":{"node":9084,"node_circle":3,"pos_x":132.08749389648438,"pos_y":111},"to_node_circle":{"node":2849,"node_circle":0,"pos_x":112.08749389648438,"pos_y":244}}]'
    // );
  },
  methods: {
    initPos() {
      let { left, top } = document
        .getElementById("svgContent")
        .getBoundingClientRect();
      this.Pos = { x: left, y: top };
    },
    dragIt(val) {
      this.dragValue = {
        dragStatus: true,
        opInformation: val,
        taskID: parseInt(Math.random() * 9000 + 1000, 10)
      };
    },
    startOperator(e) {
      if (this.dragValue && this.dragValue.dragStatus) {
        this.initPos();
        this.dragValue = {
          ...this.dragValue,
          pos_x: e.x,
          pos_y: e.y + 80
          // pos_x:e.x+this.Pos.x,
          // pos_y:e.y+this.Pos.y
        };
        // this.dragValue.pos_x=e.x
        // this.dragValue.pos_y=e.y
      }
    },
    moveOperator(e) {
      if (this.dragValue && this.dragValue.dragStatus) {
        this.initPos();
        this.dragValue = {
          ...this.dragValue,
          pos_x: e.x,
          pos_y: e.y
        };
        // this.dragValue.pos_x = e.x;
        // this.dragValue.pos_y = e.y;
      }
    },
    endOperator(e) {
      console.log(e.toElement.id);
      if (!this.dragValue) {
        return;
      }
      if (
        !this.dragValue.dragStatus &&
        (e.toElement.id != "sallite" || e.toElement.id != "earth")
      ) {
        this.dragValue.dragStatus = false;
        return;
      }

      var node_location = e.toElement.id;
      const { opInformation, taskID } = this.dragValue;
      const pos_x =
        (e.offsetX -90 - (sessionStorage["svg_left"] || 0)) /
        (sessionStorage["svgScale"] || 1); // 参数修正
      const pos_y =
        (e.offsetY -15 - (sessionStorage["svg_top"] || 0)) /
        (sessionStorage["svgScale"] || 1); // 参数修正
      var opInformation_clone = this.deepClone(opInformation);
      for (const index in opInformation_clone.info) {
        opInformation_clone.info[index].value = "";
        opInformation_clone.info[index].export = false;
      }

      const params = {
        pos_x,
        pos_y,
        taskID,
        node_location,
        opInformation: opInformation_clone,
        type: "task"
      };
      this.nodes.push(params);
      this.dragValue.dragStatus = false;
      this.setInfo(params);
    },
    setInfo(node) {
      const disabledInfo = [
        {
          name: "入度",
          value: node.opInformation.input_num
        },
        {
          name: "出度",
          value: node.opInformation.output_num
        }
      ];
      this.currentInfo = {
        disabledInfo,
        abledInfo: node.opInformation.info
      };
    },
    checkDAG() {
      //无环
      //只有一个起点
      console.log(this.nodes);
      console.log(this.lines);
      var m = new Map();
      var inputs = new Array(this.nodes.length);
      for (var item in this.nodes) {
        m.set(this.nodes[item].taskID, item);
        inputs[item] = 0;
      }
      for (var item in this.lines) {
        inputs[m.get(this.lines[item].to_node_circle.task)]++;
      }
      var flag = 0;
      console.log(inputs);
      for (var item in inputs) {
        if (inputs[item] == 0) {
          flag++;
        }
      }
      if (flag != 1) {
        this.$message.error(
          "存在0个或多余一个的起点，无法正确执行。请重新检查"
        );
        return false;
      }
      return true;
    },
    saveApp() {
      if(!this.checkDAG()){
        return
      }
      this.$axios
        .post(
          "/app/save_app/",
          this.qs.stringify({
            appID: this.appID,
            nodes: JSON.stringify(this.nodes),
            lines: JSON.stringify(this.lines)
          }),
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" }
          }
        )
        .then(res => {
          const { data } = res;
          if (data.status == 0) this.$router.push({ path: "/appList" });
          else {
            this.$message.error(data.msg);
          }
        });
    },
    isObject(o) {
      return (typeof o === "object" || typeof o === "function") && o !== null;
    },
    deepClone(obj) {
      if (!this.isObject(obj)) {
        throw new Error("obj 不是一个对象！");
      }

      let isArray = Array.isArray(obj);
      let cloneObj = isArray ? [...obj] : { ...obj };
      Reflect.ownKeys(cloneObj).forEach(key => {
        cloneObj[key] = this.isObject(obj[key])
          ? this.deepClone(obj[key])
          : obj[key];
      });

      return cloneObj;
    }
  }
};
</script>

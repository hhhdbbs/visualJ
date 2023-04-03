<template>
  <div>
    <userRouter />
    <svg width="100%" height="600px" id="TaskSvg">
      <g>
        <g
          v-for="item in containers"
          :key="`${item.containerID} ${item.pos_x}`"
          :transform="`translate(${item.pos_x}, ${item.pos_y})`"
        >
          <foreignObject width="90" height="60" style="overflow: visible">
            <div class="d-flex flex-column">
              <div>
                <svg
                  class="icon"
                  aria-hidden="true"
                  style="font-size:50px;transform:translateX(-50%)"
                >
                  <use xlink:href="#icon-rongqijiqun"></use>
                </svg>
              </div>
              <p style="transform:translateX(-50%);text-align:center">
                {{ item.containerName }}
              </p>
            </div>
          </foreignObject>
        </g>
        <g
          v-for="item in nodes"
          :key="`${item.taskID} ${item.pos_x}`"
          :transform="`translate(${item.pos_x}, ${item.pos_y})`"
        >
          <foreignObject width="200" height="60" style="overflow: visible;">
            <div class="d-flex flex-column" style="text-align:center">
              <div style="text-align:center">
                <svg class="icon" aria-hidden="true" style="font-size:50px;">
                  <use xlink:href="#icon-renwujincheng"></use>
                </svg>
              </div>
              <p style="text-align:center">
                {{ item.operatorName }}
                <span
                  :style="{
                    color: getStatusColor(item.status),
                    'font-weight': 800
                  }"
                  >{{ item.status }}</span
                >
              </p>
            </div>
          </foreignObject>
        </g>
        <g v-for="item in lines" :key="item.lineID">
          <path :class="'defaultLine'" :d="dragLinkPath(item)" />
        </g>
        <g
          v-for="item in circles"
          :key="`${item.taskID} ${item.pos_x}`"
          :transform="`translate(${item.pos_x}, ${item.pos_y})`"
        >
          <foreignObject width="90" height="60" style="overflow: visible;">
            <svg
              class="icon"
              aria-hidden="true"
              style="font-size:20px;color:red;transform:translateX(-50%)"
            >
              <use xlink:href="#icon-yuanquan"></use>
            </svg>
          </foreignObject>
        </g>
      </g>
    </svg>
  </div>
</template>
<script>
import userRouter from "../components/router/userRouter.vue"
export default {
  name: "TaskInfo",
  components:{userRouter},
  data() {
    return {
      containers: [
        // { containerID: 0, containerName: "虚拟机1", pos_x: 0, pos_y: 0 },
        // { containerID: 1, containerName: "虚拟机2", pos_x: 0, pos_y: 0 },
        // { containerID: 2, containerName: "虚拟机3", pos_x: 0, pos_y: 0 },
        // { containerID: 3, containerName: "虚拟机4", pos_x: 0, pos_y: 0 },
        // { containerID: 4, containerName: "虚拟机5", pos_x: 0, pos_y: 0 }
      ],
      containersMap: null,
      nodesMap: null,
      circles: [],
      nodes: [],
      lines_info: [],
      svgInfo: {},
      lines: [],
      Pos: {},
      taskID: null,
      timer: null
    };
  },
  async mounted() {
    const svg = document.getElementById("TaskSvg");
    const { width: svgWidth, height: svgHeight } = svg.getBoundingClientRect();
    this.svgInfo = {
      ...this.svgInfo,
      width: svgWidth,
      height: svgHeight
    };
    svg.oncontextmenu = function(e) {
      return false;
    };
    this.taskID = this.$route.query.taskId;
    await this.$axios.get("/app/container_list/").then(res => {
      var info = [];
      res.data.containerList.forEach(item => {
        info.push({
          ...item,
          pos_x: 0,
          pos_y: 0
        });
      });
      this.containers = info;
    });
    this.initContainersMap();
    this.computeContainersTranslate();
    this.timer = setInterval(async () => {
      await this.$axios
        .get("/app/view_task/", { params: { taskID: this.taskID } })
        .then(res => {
          var info;
          const {
            data: { nodes, lines, status }
          } = res;
          info = [];
          nodes.forEach(item => {
            info.push({
              ...item,
              pos_x: 0,
              pos_y: 0
            });
          });
          this.nodes = nodes;
          this.lines_info = lines;
          this.initNodesMap();
          this.computeNodeTranslate();
          this.computeCircleTranslate();
          this.initLines();
          if (status == "End") {
            clearInterval(this.timer);
            return;
          }
        });
    }, 1000);
  },
  methods: {
    getStatusColor(status) {
      switch (status) {
        case "Start":
          return "#311B92";
        case "Pause":
          return "#FF6F00";
        case "Run":
          return "#00695C";
        case "End":
          return "#E65100";
      }
    },
    initPos() {
      let { left, top } = document
        .getElementById("TaskSvg")
        .getBoundingClientRect();
      this.Pos = { pos_x: left, pos_y: top };
    },
    initContainersMap() {
      this.containersMap = new Map();
      for (const i in this.containers) {
        this.containersMap.set(this.containers[i].containerID, i);
      }
    },
    initNodesMap() {
      this.nodesMap = new Map();
      for (const i in this.nodes) {
        this.nodesMap.set(this.nodes[i].taskID, i);
      }
    },
    computeContainersTranslate() {
      const length = this.containers.length;
      const offsetX = this.svgInfo.width / length ;
      for (const index in this.containers) {
        this.containers[index].pos_x =
          (this.svgInfo.width * index) / (length+1) + offsetX;
        this.containers[index].pos_y = this.svgInfo.height / 10;
      }
    },
    computeNodeTranslate() {
      const length = this.nodes.length;
      const offsetX = this.svgInfo.width / this.containers.length / 5;
      const top = 150;
      for (const index in this.nodes) {
        this.nodes[index].pos_x = offsetX;
        this.nodes[index].pos_y =
          top + ((this.svgInfo.height - top) * index) / (length);
      }
    },
    computeCircleTranslate() {
      const circles = [];
      for (const i in this.nodes) {
        const { taskID, server,status } = this.nodes[i];
        if(status=="Run"||status=="End"){
          circles.push({
          status,
          taskID,
          server,
          pos_x: this.containers[this.containersMap.get(server)].pos_x,
          pos_y: this.nodes[this.nodesMap.get(taskID)].pos_y+20
        });
        }
        
      }
      this.circles = circles;
    },
    initLines() {
      this.initPos();
      const lines = [];
      const circleHeight = 10;
      console.log(this.circles)
      for (const item in this.lines_info) {
        const fromIndex = this.nodesMap.get(this.lines_info[item].from);
        const toIndex = this.nodesMap.get(this.lines_info[item].to);
        console.log("fr:",fromIndex," to:",toIndex)
        if(fromIndex!=null&&toIndex!=null&&fromIndex<this.circles.length&&toIndex<this.circles.length){
          console.log(1)
          lines.push({
          lineID: item,
          fromX: this.circles[fromIndex].pos_x,
          fromY: this.circles[fromIndex].pos_y + circleHeight,
          toX: this.circles[toIndex].pos_x,
          toY: this.circles[toIndex].pos_y + circleHeight
        });
        }
      }
      this.lines = lines;
    },
    dragLinkPath(dragLink) {
      const { fromX, fromY, toX, toY } = dragLink;
      return `M ${fromX} ${fromY} Q ${fromX + 30} ${fromY}  ${(toX + fromX) /
        2} ${(fromY + toY) / 2} T ${toX} ${toY}`;
    }
  }
};
</script>
<style scoped>
.defaultLine {
  stroke: #00c0ff;
  stroke-width: 2px;
  fill: transparent;
  cursor: pointer;
  stroke-dasharray: 5px;
  stroke-dashoffset: 1000px;
  animation: grown 40s infinite linear;
}
@keyframes grown {
  to {
    stroke-dashoffset: 0;
  }
}
</style>

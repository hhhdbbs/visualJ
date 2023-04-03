<template>
  <svg
    width="100%"
    height="600px"
    @mousedown="checkDownCurrentEvent"
    @mouseup="checkUpCurrentEvent"
    @mousemove="checkMoveCurrentEvent($event)"
  >
    <rect
      id="sallite"
      :width="halfSvg + 'px'"
      :height="heightSvg + 'px'"
      style="fill:rgba(255,255,255,0)"
    />
    <!-- <g :transform="`translate(${halfSvg/2-20}, 0)`">
      <foreignObject width="180" height="30" style="overflow: visible;">
        <span>卫星站</span>
      </foreignObject>
    </g> -->
    <rect
      id="earth"
      :width="halfSvg + 'px'"
      :height="heightSvg + 'px'"
      :transform="`translate(${halfSvg}, 0)`"
      style="fill:rgba(255,255,255,0)"
    />
    <!-- <g :transform="`translate(${halfSvg*1.5-20}, 0)`">
      <foreignObject width="180" height="30" style="overflow: visible;">
        <span>地面站</span>
      </foreignObject>
    </g> -->
    <g>
      <g
        v-for="(item, index) in nodes"
        :key="item.taskID"
        :transform="`translate(${item.pos_x}, ${item.pos_y})`"
        @mousedown="$emit('setInfo', item)"
      >
        <foreignObject width="180" height="30" style="overflow: visible;">
          <o-point-edit
            :opInformation="item.opInformation"
            :taskID="item.taskID"
            :index="index"
            @linkPre="linkPre"
            @linkEnd="linkEnd"
            @delTask="delTask"
          ></o-point-edit>
        </foreignObject>
      </g>
      <Lines :lines="lines" :menuInfo="menuInfo" @showMenu="showMenu"></Lines>
      <SimulateArrow
        v-if="currentEvent == EventType.DragLink"
        :dragLink="tempLineInfo"
      />
    </g>
  </svg>
</template>
<script>
import OPointEdit from "./OPointEdit.vue";
import SimulateArrow from "./SimulateArrow.vue";
import Lines from "./Lines.vue";
export default {
  name: "DAGBoard",
  components: { OPointEdit, SimulateArrow, Lines },
  props: {
    nodes: Array,
    lines: Array
  },
  data() {
    return {
      EventType: { DragLink: "DragLink" },
      currentEvent: null,
      tempLineInfo: null,
      Pos: {},
      menuInfo: { showMenu: false, menuPos: {} },
      halfSvg: "0",
      heightSvg: "0"
    };
  },
  mounted() {
    setTimeout(() => {
      this.halfSvg =
        document.getElementById("svgContent").width.animVal.value / 2;
      this.heightSvg = document.getElementById(
        "svgContent"
      ).height.animVal.value;
    }, 100);
  },
  methods: {
    getSvgHalfWidth() {
      return "1px";
    },
    checkDownCurrentEvent() {
      switch (this.currentEvent) {
      }
    },
    checkUpCurrentEvent() {
      this.menuInfo.showMenu = false;
      switch (this.currentEvent) {
        case this.EventType.DragLink:
          this.tempLineInfo = {};
          this.currentEvent = null;
      }
    },
    checkMoveCurrentEvent(e) {
      switch (this.currentEvent) {
        case this.EventType.DragLink:
          this.tempLineInfo.toX = e.x - this.Pos.x;
          this.tempLineInfo.toY = e.y - this.Pos.y;
      }
    },
    initPos() {
      let { left, top } = document
        .getElementById("svgContent")
        .getBoundingClientRect();
      this.Pos = { x: left, y: top };
    },
    linkPre(e, i, taskID, nodeID) {
      this.currentEvent = this.EventType.DragLink;
      this.initPos();
      const x = e.x - this.Pos.x;
      const y = e.y - this.Pos.y;
      //设置连线信息
      this.tempLineInfo = {
        from_node_task: taskID,
        from_node_circle: nodeID,
        from_output_num: this.nodes[i].opInformation.output_num,
        fromX: x,
        fromY: y,
        toX: x,
        toY: y
      };
      //检查出度不能过多
      const {
        from_node_task,
        from_node_circle,
        from_output_num
      } = this.tempLineInfo;
      var out = 1;
      this.lines.forEach(item => {
        if (item.from_node_circle.task == from_node_task) out++;
      });
      console.log(this.nodes[i]);
      console.log(out);
      console.log(from_output_num);
      if (out > from_output_num) {
        this.tempLineInfo = {};
        this.currentEvent = null;
        this.$message.error("错误：此镜像出度已满,需要删除多余的线");
      }
      //检查出度
    },
    linkEnd(e, i, taskID, nodeID) {
      if (this.currentEvent == this.EventType.DragLink) {
        //检查入度不能过多
        var in_port = 1;
        this.lines.forEach(item => {
          if (item.to_node_circle.task == taskID) in_port++;
        });
        console.log(this.nodes[i].opInformation.input_num);
        if (in_port > this.nodes[i].opInformation.input_num) {
          this.tempLineInfo = null;
          this.currentEvent = null;
          this.$message.error("错误：此镜像入度已满,需要删除多余的线");
          return;
        }
        //检查入度
        const LineInfo = {
          from_node_circle: {
            task: this.tempLineInfo.from_node_task,
            node_circle: this.tempLineInfo.from_node_circle,
            pos_x: this.tempLineInfo.fromX,
            pos_y: this.tempLineInfo.fromY
          },
          to_node_circle: {
            task: taskID,
            node_circle: nodeID,
            pos_x: this.tempLineInfo.toX,
            pos_y: this.tempLineInfo.toY
          }
        };
        // if (fromType == this.TaskType.End) {
        //   this.$message.error(" End 任务不可存在出度");
        // } else if (toType == this.TaskType.Start) {
        //   this.$message.error(" start 任务不可存在入度");
        // } else
        if (LineInfo.from_node_circle.task == LineInfo.to_node_circle.task) {
          this.$message.error("不可形成自环");
        } else if (this.checkHasCircle([...this.lines, LineInfo])) {
          this.$message.error("任务编排不可出现环状图，存在任务循环执行的风险");
        } else {
          this.lines.push(LineInfo);
        }
      }
      this.tempLineInfo = null;
      this.currentEvent = null;
    },
    delTask(index, taskID) {
      for (var i = 0; i < this.lines.length; i++) {
        if (
          this.lines[i].from_node_circle.task == taskID ||
          this.lines[i].to_node_circle.task == taskID
        ) {
          this.lines.splice(i, 1);
          i--;
        }
      }
      this.nodes.splice(index, 1);
    },
    checkHasCircle(tempLines) {
      var flag = false;
      var color = new Array(this.nodes.length);
      var taskToIndexMap = new Map();
      var vec = new Array(this.nodes.length);
      var dfs = x => {
        if (flag) {
          return;
        }
        color[x] = 0;
        for (var item in vec[x]) {
          var to = vec[x][item];
          if (color[to] == -1) {
            dfs(to);
          } else if (color[to] == 0) {
            flag = true;
          }
        }
        color[x] = 1;
      };
      for (var item in this.nodes) {
        color[item] = -1;
        vec[item] = [];
        taskToIndexMap.set(this.nodes[item].taskID, item);
      }
      for (var item in tempLines) {
        var from = taskToIndexMap.get(tempLines[item].from_node_circle.task);
        var to = taskToIndexMap.get(tempLines[item].to_node_circle.task);
        vec[from].push(to);
      }
      for (var item in color) {
        if (color[item] == -1) {
          dfs(item);
        }
        if (flag) {
          return true;
        }
      }
      console.log(flag);
      if (flag) {
        return true;
      } else {
        return false;
      }
    },
    showMenu(menuPos) {
      this.menuInfo.showMenu = true;
      this.menuInfo.menuPos = menuPos;
    }
  }
};
</script>

<template>
  <div>
    <v-card v-for="(item, index) in taskList" :key="item.taskID">
      <v-card-text class="d-flex">
        <h2 class="mr-auto">{{ item.taskName }}</h2>
        <v-btn
          text
          color="light-blue lighten-3"
          style="margin-right:10px"
          @click="watchStatus(index)"
        >
          查看
        </v-btn>
        <v-btn text :color="checkStatus(item.Status)">
          状态：{{ item.Status }}
        </v-btn>
        <v-btn
          v-if="item.Status == taskStatus.End"
          text
          color="purple darken-4"
        >
          获取结果
        </v-btn>
      </v-card-text>
    </v-card>
  </div>
</template>
<script>
export default {
  name: "TaskBoard",
  data() {
    return {
      taskStatus: { Start: "Start", Pause: "Pause", Run: "Run", End: "End" },
      taskList: [
        {
          taskID: 22,
          taskName: "任务1",
          appID: 22,
          Status: "Run",
          operators: [
            { operatorID: 12, operatorName: "预处理", pos_x: 0, pos_y: 0 },
            { operatorID: 23, operatorName: "灰度", pos_x: 0, pos_y: 0 },
            { operatorID: 234, operatorName: "强化特征", pos_x: 0, pos_y: 0 }
          ],
          nodes: [
            { nodeID: 44, operatorID: 12, containerID: 3, pos_x: 0, pos_y: 0 },
            { nodeID: 55, operatorID: 23, containerID: 2, pos_x: 0, pos_y: 0 },
            { nodeID: 66, operatorID: 234, containerID: 4, pos_x: 0, pos_y: 0 }
          ]
        },
        {
          taskID: 24,
          taskName: "应用图片强化特征",
          appID: 22,
          Status: "End",
          operators: [
            { operatorID: 12, operatorName: "预处理", pos_x: 0, pos_y: 0 },
            { operatorID: 23, operatorName: "灰度", pos_x: 0, pos_y: 0 }
          ],
          nodes: [
            { operatorID: 12, containerID: 3 },
            { operatorID: 23, containerID: 2 }
          ]
        },
        {
          taskID: 25,
          taskName: "针对应用灰度面向遥感图像处理",
          appID: 22,
          Status: "Start",
          operators: [
            { operatorID: 12, operatorName: "预处理", pos_x: 0, pos_y: 0 },
            { operatorID: 23, operatorName: "灰度", pos_x: 0, pos_y: 0 }
          ],
          nodes: [
            { operatorID: 12, containerID: 3 },
            { operatorID: 23, containerID: 2 }
          ]
        },
        {
          taskID: 26,
          taskName: "任务2",
          appID: 22,
          Status: "Pause",
          operators: [
            { operatorID: 23, operatorName: "预处理", pos_x: 0, pos_y: 0 },
            { operatorID: 12, operatorName: "灰度", pos_x: 0, pos_y: 0 }
          ],
          nodes: [
            { operatorID: 23, containerID: 2 },
            { operatorID: 12, containerID: 3 }
          ]
        }
      ]
    };
  },
  mounted() {},
  methods: {
    checkStatus(Status) {
      switch (Status) {
        case "Start":
          return "secondary";
        case "Pause":
          return "warning";
        case "Run":
          return "success";
        case "End":
          return "blue-grey";
      }
    },
    watchStatus(index) {
      const { operators, nodes } = this.taskList[index];
      this.$emit("watchStatus", operators, nodes);
    }
  }
};
</script>

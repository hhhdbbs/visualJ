<template>
  <div>
    <userRouter />
    <tubiao />
    <v-card v-for="item in taskList" :key="item.taskID">
      <v-card-text class="d-flex">
        <h2 class="mr-auto">{{ item.taskName }}</h2>
        <v-btn
          text
          color="light-blue lighten-3"
          style="margin-right:10px"
          @click="watchStatus(item.taskID)"
        >
          查看
        </v-btn>
        <v-btn text :color="checkStatus(item.Status)">
          状态：{{ item.Status }}
        </v-btn>
        <v-btn
          v-if="item.Status == taskStatus.End"
          text
          @click="getOutput(item.taskID)"
          color="purple darken-4"
        >
          获取结果
        </v-btn>
      </v-card-text>
    </v-card>
  </div>
</template>
<script>
import userRouter from "../components/router/userRouter.vue"
import tubiao from "./tubiao.vue"
export default {
  name: "TaskList",
  components:{userRouter,tubiao},
  data() {
    return {
      taskStatus: { Start: "Start", Pause: "Pause", Run: "Run", End: "End" },
      taskList: []
    };
  },
  mounted() {
    setInterval(()=>{
       this.$axios.get("/app/task_list/").then(res => {
      var list = [];
      for(var i=res.data.taskList.length-1;i>=0;i--){
        list.push(res.data.taskList[i])
      }
      this.taskList = list;
    });
    },1000)

    //  this.$axios.get("http://sat.act.buaa.edu.cn:8000/api/apps").then(res => {
    //   this.taskList = res.data.taskList;})
   
  },
  methods: {
    checkStatus(Status) {
      switch (Status) {
        case "Start":
          return "secondary";
        case "Fail":
          return "warning";
        case "Run":
          return "success";
        case "End":
          return "blue-grey";
      }
    },
    watchStatus(taskId) {
       this.$router.push({ path: "/taskInfo", query: { taskId } });
    },
    getOutput(taskID){
      this.$axios
      .get("/app/get_task_output_img/", { params: { taskID:taskID } })
      .then(res => {
        window.location.href ='http://192.168.1.202:8082/'+res.data.imgList[0].url
      })
    }
  }
};
</script>

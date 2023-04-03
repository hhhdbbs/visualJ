<template>
  <div>
    <adminRouter />
    <div>
      <p style="font-size:30px;font-weight:800;margin:20px 20px 0">
        服务器管理
      </p>
      <div class="d-flex">
        <v-btn
          color="primary"
          class="ml-auto"
          text
          @click="createServerDialog = true"
          >添加服务器</v-btn
        >
      </div>
      <v-divider r color="primary" />
      <div class="d-flex" style="padding:20px">
        <span style="width:20%;font-weight:800">服务器名称</span>
        <span style="width:20%;font-weight:800">ip:port</span>
        <span style="width:10%;font-weight:800">CPU</span>
        <span style="width:10%;font-weight:800">内存</span>
        <span
          style="width:15%;overflow:hidden;text-overflow:ellipsis;font-weight:800"
        >
          描述
        </span>
        <span style="width:10%;font-weight:800">状态</span>
        <span style="width:15%;font-weight:800">操作</span>
      </div>
      <v-divider />
      <div v-for="item in serverList" :key="item.id">
        <div class="d-flex" style="padding:20px">
          <span style="width:20%;">{{ item.name }}</span>
          <span style="width:20%;">{{ item.ip }}:{{ item.port }}</span>
          <span style="width:10%;">{{ item.CPU }}核</span>
          <span style="width:10%;">{{ item.capacity }}</span>
          <span style="width:15%;overflow:hidden;text-overflow:ellipsis">
            {{ item.description }}
          </span>
          <span style="width:10%;">
            <v-btn :color="item.status == '正常' ? 'primary' : 'error'">{{
              item.status
            }}</v-btn>
          </span>
          <span style="width:15%">
            <v-btn color="primary" text @click="del(item.id)">删除</v-btn>
            <v-btn color="primary" text @click="del(item.id)">编辑</v-btn>
          </span>
        </div>
      </div>
    </div>
    <v-dialog
      v-model="createServerDialog"
      max-width="70%"
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-card-title>添加服务器</v-card-title>
        <v-card-text>
          <v-form>
            <v-row>
              <v-col cols="12" class="padding-0">
                <v-text-field
                  label="服务器名称"
                  v-model="createForm.name"
                ></v-text-field>
              </v-col>
              <v-col cols="12" class="padding-0">
                <v-text-field label="ip" v-model="createForm.ip"></v-text-field>
              </v-col>
              <v-col cols="12" class="padding-0">
                <v-text-field
                  label="端口"
                  v-model="createForm.port"
                ></v-text-field>
              </v-col>
              <v-col cols="12" class="padding-0">
                <v-text-field
                  label="描述"
                  v-model="createForm.description"
                ></v-text-field>
              </v-col>
              <v-col cols="6" class="padding-0">
                <v-text-field
                  label="CPU"
                  v-model="createForm.CPU"
                ></v-text-field>
              </v-col>
              <v-col cols="6" class="padding-0">
                <v-text-field
                  label="内存"
                  v-model="createForm.capacity"
                ></v-text-field>
              </v-col>
              <v-col cols="6" class="padding-0">
                <v-text-field
                  label="账号名"
                  v-model="createForm.username"
                ></v-text-field>
              </v-col>
              <v-col cols="6" class="padding-0">
                <v-text-field
                  label="密码"
                  v-model="createForm.password"
                ></v-text-field>
              </v-col>
              <v-col cols="6" class="padding-0">
                <v-text-field
                  label="算子存放目录"
                  v-model="createForm.operatorDir"
                ></v-text-field>
              </v-col>
              <v-col cols="6" class="padding-0">
                <v-text-field
                  label="图像存放目录"
                  v-model="createForm.imgDir"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            text
            @click="
              createServerDialog = false;
              createForm = {};
            "
          >
            取消
          </v-btn>
          <v-btn color="green darken-1" text @click="createServer()" :loading="loading">
            新建
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import adminRouter from "../components/router/adminRouter.vue"
import moment from "moment";
export default {
  name: "OperatorList",
  components:{adminRouter},
  data() {
    return {
      createServerDialog: false,
      serverList: [],
      createForm: {},
      loading:false
    };
  },
  mounted() {
    this.initServerList();
  },
  methods: {
    getTime(value) {
      var date = moment(value).format("YYYY-MM-DD");
      return date;
    },
    initServerList() {
      this.$axios.get("/app/server_list/").then(res => {
        this.serverList = res.data.serverList;
      });
    },
    del(id) {
      this.$axios
        .post("/app/delete_server/", this.qs.stringify({ id }), {
          headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        .then(res => {
          this.initServerList();
        });
    },
    createServer() {
      this.loading=true
      setTimeout(()=>{
        this.$axios
        .post("/app/create_server/", this.qs.stringify(this.createForm), {
          headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        .then(res => {
          if (res.data.status == 0) {
            this.initServerList();
            this.createServerDialog = false;
            this.createForm = {};
          } else {
            this.$message.error(`${res.data.msg}`);
          }
        });
        this.loading=false
        },1000)
      
    }
  }
};
</script>
<style scoped>
.padding-0 {
  padding-top: 0;
  padding-bottom: 0;
}
.icon-middle-parent {
  position: relative;
}
.icon-middle-child {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>

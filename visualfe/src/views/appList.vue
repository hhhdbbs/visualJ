<template>
  <div>
    <userRouter />
  <div>
      <div cols="12">
        <v-card>
          <v-card-title id="bodyTitle">
            <h2>下午好,</h2>
            <h1>{{ author.name }}</h1>
          </v-card-title>
          <v-card-actions class="d-flex">
            <v-btn
              text
              color="primary"
              class="ml-auto"
              @click="createAppDialog = true"
            >
              新建应用
            </v-btn>
          </v-card-actions>
        </v-card>
      </div>
      <div cols="12">
        <v-card
          v-for="(item, index) in appList"
          :key="item.id"
          style="margin-bottom:1px"
        >
          <div class="d-flex" style="padding:10px">
            <h3>{{ item.name }}</h3>
            <v-btn
              text
              color="light-blue darken-3"
              @click="editApp(item.id)"
              class="ml-auto"
              >编辑</v-btn
            >
            <v-btn text color="light-blue darken-2" @click="applyApp(item)"
              >应用</v-btn
            >
            <v-btn
              text
              color="light-blue darken-1"
              @click="delApp(item.id, index)"
              >删除</v-btn
            >
          </div>
        </v-card>
      </div>
    <v-dialog
      v-model="applyDialog"
      max-width="50%"
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-card-title class="text-h5">
          应用：{{ checkItem.name }}
        </v-card-title>
        <v-card-text>
          <v-form>
            <v-row>
              <v-col cols="2">
                应用名
              </v-col>
              <v-col cols="10">
                <v-text-field v-model="applyForm.name" clearable></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="2">
                图片
              </v-col>
              <v-col cols="10">
                <v-file-input
                  accept="image/*"
                  v-model="applyForm.img"
                  clearable
                ></v-file-input>
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
              applyDialog = false;
              applyForm = {};
            "
          >
            取消
          </v-btn>
          <v-btn
            color="green darken-1"
            text
            @click="
              applyDialog = false;
              applyImg();
            "
          >
            应用
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="createAppDialog"
      max-width="50%"
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-card-title class="text-h5">
          新建应用
        </v-card-title>
        <v-card-text>
          <v-form>
            <v-row>
              <v-col cols="2">
                应用名
              </v-col>
              <v-col cols="10">
                <v-text-field
                  v-model="createForm.name"
                  clearable
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
              createAppDialog = false;
              createForm = {};
            "
          >
            取消
          </v-btn>
          <v-btn
            color="green darken-1"
            text
            @click="
              createAppDialog = false;
              createApp();
            "
          >
            新建应用
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
    </div>
</template>
<script>
import userRouter from "../components/router/userRouter.vue"
export default {
  name: "AppList",
  components:{userRouter},
  data() {
    return {
      author: { name: "张潇菡" },
      appList: [],
      applyDialog: false,
      createAppDialog: false,
      checkItem: {},
      applyForm: {},
      createForm: {}
    };
  },
  mounted() {
    //获取应用列表
    this.$axios.get("/app/app_list/").then(res => {
      this.appList = res.data.appList;
    });
  },
  methods: {
    editApp(appId) {
      this.$router.push({ path: "/appInfo", query: { appId } });
    },
    applyApp(item) {
      this.applyDialog = true;
      this.checkItem = item;
    },
    delApp(id, index) {
      this.$axios
        .post("/app/delete_app/", this.qs.stringify({ id }), {
          headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        .then(res => {
          const { data } = res;
          if (data.status == 0) this.appList.splice(index, 1);
          else {
            this.$message.error(data.msg);
          }
        });
    },
    applyImg() {
      var form = new FormData();
      form.append("id", this.checkItem.id);
      form.append("file", this.applyForm.img);
      form.append("name", this.applyForm.name);
      this.$axios.post("/app/create_task/", form).then(res => {
        if(res.data.status!=0){
          this.$message.error(`${res.data.msg}`)
        }
      });
    },
    createApp() {
      this.$axios
        .post("/app/create_app/", this.qs.stringify(this.createForm), {
          headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        .then(res => {
          this.createForm = {};
          const newApp = res.data.id;
          this.$router.push({ path: "/appInfo", query: { appId: newApp } });
        });
    }
  }
};
</script>

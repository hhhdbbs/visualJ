<template>
  <div>
    <adminRouter />
    <div>
      <p style="font-size:30px;font-weight:800;margin:20px 20px 0">
        用户管理
      </p>
      <div class="d-flex">
        <v-btn
          color="primary"
          class="ml-auto"
          text
          @click="createServerDialog = true"
          >新建用户</v-btn
        >
      </div>
      <v-divider r color="primary" />
      <div class="d-flex" style="padding:20px">
        <span style="width:20%;font-weight:800">账号名</span>
        <span style="width:20%;font-weight:800">密码</span>
        <span style="width:15%;font-weight:800">账号备注</span>
        <span style="width:10%;font-weight:800">权限</span>
        <span style="width:35%;font-weight:800">操作</span>
      </div>
      <v-divider />
      <div v-for="item in userList" :key="item.id">
        <div class="d-flex" style="padding:20px">
          <span style="width:20%;">{{ item.account }}</span>
          <span style="width:20%;">{{ item.password }}</span>
          <span style="width:15%;overflow:hidden;text-overflow:ellipsis">
            {{ item.description }}
          </span>
          <span style="width:10%;">
            <v-btn :color="item.isadmin ? 'error' : 'primary'">{{
              item.isadmin ? "管理员" : "普通用户"
            }}</v-btn>
          </span>
          <span style="width:35%">
            <v-btn color="primary" text @click="del(item.id)">删除</v-btn>
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
        <v-card-title>添加用户</v-card-title>
        <v-card-text>
          <v-form>
            <v-row>
              <v-col cols="12" class="padding-0">
                <v-text-field
                  label="账号名"
                  v-model="createForm.account"
                ></v-text-field>
              </v-col>
              <v-col cols="12" class="padding-0">
                <v-text-field
                  label="密码"
                  v-model="createForm.password"
                ></v-text-field>
              </v-col>
              <v-col cols="12" class="padding-0">
                <v-text-field
                  label="描述"
                  v-model="createForm.description"
                ></v-text-field>
              </v-col>
              <v-col cols="6" class="padding-0">
                <v-radio-group v-model="createForm.isadmin" row>
                  <v-radio label="管理员" value="1"></v-radio>
                  <v-radio label="普通用户" value="0"></v-radio>
                </v-radio-group>
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
          <v-btn
            color="green darken-1"
            text
            @click="createServer()"
            :loading="loading"
          >
            新建
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import adminRouter from "../components/router/adminRouter.vue";
import moment from "moment";
export default {
  name: "OperatorList",
  components: { adminRouter },
  data() {
    return {
      createServerDialog: false,
      userList: [],
      createForm: {},
      loading: false
    };
  },
  mounted() {
    this.initUserList();
  },
  methods: {
    getTime(value) {
      var date = moment(value).format("YYYY-MM-DD");
      return date;
    },
    initUserList() {
      this.$axios.get("/app/user_list/").then(res => {
        this.userList = res.data;
      });
    },
    del(id) {
      this.$axios
        .post("/app/delete_user/", this.qs.stringify({ id }), {
          headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        .then(res => {
          this.initUserList();
        });
    },
    createServer() {
      this.$axios
        .post("/app/create_user/", this.qs.stringify(this.createForm), {
          headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        .then(res => {
          if (res.data.result == 0) {
            this.initUserList();
            this.createServerDialog = false;
            this.createForm = {};
          } else {
            this.$message.error(`${res.data.msg}`);
          }
        });
      this.loading = false;
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

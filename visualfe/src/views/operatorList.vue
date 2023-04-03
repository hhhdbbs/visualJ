<template>
  <div>
    <userRouter />
    <div>
      <p style="font-size:30px;font-weight:800;margin:20px 20px 0">算子管理</p>
      <div class="d-flex">
        <v-btn color="primary" class="ml-auto" text @click="createOperatorDialog = true">添加算子</v-btn>
      </div>
      <v-divider r color="primary"/>
      <div class="d-flex" style="padding:20px">
            <span style="width:30%;font-weight:800">算子名称</span>
            <span style="width:20%;font-weight:800">创建时间</span>
            <span style="width:30%;overflow:hidden;text-overflow:ellipsis;font-weight:800">
               描述
            </span>
            <span style="width:10%;font-weight:800">操作</span>
            <span style="width:10%;font-weight:800">状态</span>
        </div>
     <v-divider />
      <div v-for="item in operatorList" :key="item.id">
        <div class="d-flex" style="padding:20px">
            <span style="width:30%;">{{ item.name }}</span>
            <span style="width:20%">{{ getTime(item.date) }}</span>
            <span style="width:30%;overflow:hidden;text-overflow:ellipsis">
                {{ item.description }}
            </span>
            <span style="width:20%"><v-btn color="primary" text @click="del(item.id)">删除</v-btn></span>
            <span style="width:10%;font-weight:800">
              <v-btn :color="item.loading ? 'error' : 'primary'">{{
              item.loading ? '加载' : '装载'
            }}</v-btn>
            </span>
        </div>
      </div>
    </div>
    <v-dialog
      v-model="createOperatorDialog"
      max-width="70%"
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-card-title>添加算子</v-card-title>
        <v-card-text>
          <v-form>
            <v-row>
              <v-col cols="12" class="padding-0">
                <v-text-field
                  label="算子名称"
                  v-model="createForm.name"
                ></v-text-field>
              </v-col>
              <v-col cols="12" class="padding-0">
                <v-text-field
                  label="算子描述"
                  v-model="createForm.description"
                ></v-text-field>
              </v-col>
              <v-col cols="12" class="padding-0">
                <v-text-field
                  label="运行脚本"
                  v-model="createForm.workFilename"
                ></v-text-field>
              </v-col>
              <v-col cols="12" class="padding-0">
                <v-text-field
                  label="输入文件目录"
                  v-model="createForm.inputDir"
                ></v-text-field>
              </v-col>
              <v-col cols="12" class="padding-0">
                <v-text-field
                  label="输出文件目录"
                  v-model="createForm.outputDir"
                ></v-text-field>
              </v-col>
            </v-row>
             <v-col cols="12" class="padding-0">
                 <v-file-input show-size truncate-length="24" v-model="createForm.file"></v-file-input>
             </v-col>
            <v-row v-for="(item, index) in createForm.paramters" :key="index">
              <v-col cols="1" class="padding-0 icon-middle-parent">
                <svg
                  @click="addP(index)"
                  class="icon icon-middle-child"
                  aria-hidden="true"
                  style="color:#2E7D32;"
                >
                  <use xlink:href="#icon-tianjia"></use>
                </svg>
              </v-col>
              <v-col cols="3" class="padding-0">
                <v-text-field
                  label="参数名称"
                  v-model="item.name"
                  hint="不可重复命名"
                ></v-text-field>
              </v-col>
              <v-col cols="3" class="padding-0">
                <v-text-field
                  label="参数描述"
                  v-model="item.description"
                ></v-text-field>
              </v-col>
              <v-col cols="3" class="padding-0">
                <v-select
                  :items="operatorType"
                  label="参数类型"
                  v-model="item.type"
                ></v-select>
              </v-col>
              <v-col cols="1" class="padding-0 icon-middle-parent">
                <svg
                  @click="delP(index)"
                  class="icon icon-middle-child"
                  aria-hidden="true"
                  style="color:#D84315"
                >
                  <use xlink:href="#icon-jianhao"></use>
                </svg>
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
              createOperatorDialog = false;
              createForm = { paramters: [{}] };
            "
          >
            取消
          </v-btn>
          <v-btn
            color="green darken-1"
            text
            @click="
              createOperator();
            "
          >
            新建
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import userRouter from "../components/router/userRouter.vue"
import moment from "moment";
export default {
  name: "OperatorList",
  components:{userRouter},
  data() {
    return {
      createOperatorDialog: false,
      operatorList: [],
      createForm: { paramters: [{}] },
      operatorType: [
        { text: "输入文件名", value: "input" },
        { text: "输出文件名", value: "output" },
        { text: "无", value: "none" }
      ]
    };
  },
  mounted(){
      this.initOperatorList()
  },
  methods: {
    getTime(value){
        var date = moment(value).format('YYYY-MM-DD');
        return date;
    },
    initOperatorList(){
        this.$axios.get("/app/edit_operator_list/").then(res => {
            this.operatorList=res.data.operatorList
        });
    },
    addP(index){
      this.createForm.paramters.splice(index+1,0,{})
    },
    delP(index){
      this.createForm.paramters.splice(index,1)
    },
    del(id) {
      this.$axios
        .post("/app/delete_operator/", this.qs.stringify({ id }), {
          headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        .then(res => {
          this.initOperatorList()
        });
    },
    createOperator() {
        var form = new FormData();
      form.append("name", this.createForm.name);
      form.append("file", this.createForm.file);
      form.append("inputDir", this.createForm.inputDir);
      form.append("outputDir", this.createForm.outputDir);
      form.append("description", this.createForm.description);
      form.append("paramters", JSON.stringify(this.createForm.paramters));
      form.append("workFilename", this.createForm.workFilename);
      this.$axios.post("/app/create_operator/", form).then(res => {
        this.initOperatorList()
        this.createForm={ paramters: [{}] }
        this.createOperatorDialog=false
      });
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

<template>
  <div>
    <el-menu class="el-menu-demo" mode="horizontal">
      <el-menu-item @click="jump('operatorList')" index="/operatorList">
        <i class="el-icon-s-home" style="margin-left: -4px"></i>
        <span> &nbsp;算子管理 </span>
      </el-menu-item>
      <el-menu-item @click="jump('appList')" index="/appList">
        <i class="el-icon-s-home" style="margin-left: -4px"></i>
        <span> &nbsp;应用中心 </span>
      </el-menu-item>
      <el-menu-item @click="jump('taskList')" index="/taskList">
        <i class="el-icon-s-home" style="margin-left: -4px"></i>
        <span> &nbsp;任务列表 </span>
      </el-menu-item>
      <el-menu-item @click="jump('login')" index="/userList">
        <i  style="margin-left: -4px"></i>
        <span> &nbsp;注销登录 </span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      activeIndex: "appList"
    };
  },
  methods: {
    jump(index) {
      this.$router.push({ path: index });
    }
  }
};
</script>

<style>
*::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}
*::-webkit-scrollbar-thumb {
  /*滚动条里面小方块*/
  border-radius: 15px;
  -webkit-box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
  /*background: #cce2f7;*/
  /* background: #999; */
}
*::-webkit-scrollbar-track {
  /*滚动条里面轨道*/
  -webkit-box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  background: #ededed;
}

*:-webkit-autofill {
  box-shadow: 0 0 0px 1000px #323451 inset !important;
  -webkit-box-shadow: 0 0 0px 1000px #323451 inset !important;
  border: 0px solid #ccc !important;
  -webkit-text-fill-color: #fff;
}
</style>

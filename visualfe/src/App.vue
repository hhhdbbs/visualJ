<template>
  <v-app>
    <router-view></router-view>
  </v-app>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      activeIndex: "appList"
    };
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

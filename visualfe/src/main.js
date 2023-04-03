// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import vuetify from './plugins/vuetify'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import './assets/css/all.css'
import './assets/iconfont/iconfont.js'
import axios from 'axios'
import qs from 'qs';
import moment from "moment"
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import '@mdi/font/css/materialdesignicons.css'
import * as echarts from "echarts"
Vue.prototype.$echarts = echarts
Vue.prototype.$moment = moment
moment.locale('zh-cn')
Vue.prototype.$axios = axios
axios.defaults.baseURL='http://127.0.0.1:8000/';//''http://192.168.1.202:8082/ http://127.0.0.1:8000/
Vue.config.productionTip = false
Vue.prototype.qs = qs;
Vue.use(ElementUI);
/* eslint-disable no-new */
new Vue({
  vuetify,
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect:'/login'
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/login')
    },
    {
      path: '/userList',
      name: 'UserList',
      component: () => import('@/views/userList')
    },
    {
      path: '/appList',
      name: 'AppList',
      component: () => import('@/views/appList')
    },
    {
      path: '/appInfo',
      name: 'AppInfo',
      component: () => import('@/views/appInfo')
    },
    {
      path: '/taskList',
      name: 'TaskList',
      component: () => import('@/views/taskList')
    },
    {
      path: '/operatorList',
      name: 'OperatorList',
      component: () => import('@/views/operatorList')
    },
    {
      path: '/taskInfo',
      name: 'TaskInfo',
      component: () => import('@/views/taskInfo')
    },
    {
      path: '/serverList',
      name: 'ServerList',
      component: () => import('@/views/serverList')
    },
    {
      path: '/tubiao',
      name: 'tubiao',
      component: () => import('@/views/tubiao')
    },
  ]
})

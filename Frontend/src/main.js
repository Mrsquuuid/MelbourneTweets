import Vue from 'vue'
import App from './App.vue'
import router from './router'
import echarts from 'echarts'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css'

Vue.use(Antd)
Vue.config.productionTip = false
Vue.prototype.$echarts = echarts

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'
import 'element-ui/lib/theme-chalk/index.css'
import VueTour from "vue-tour";
import app from "./App.vue";
require("vue-tour/dist/vue-tour.css");

Vue.use(ElementUI)
Vue.use(VueResource)
Vue.use(VueTour)

Vue.config.productionTip = true

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(app),
  components: { App },
  template: '<App/>'
}).$mount('#app')

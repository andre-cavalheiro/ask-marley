import Vue from 'vue'
import App from './App.vue'
import store from './store/store'
import router from './router/router'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: function (h) { return h(App) }
}).$mount('#app')

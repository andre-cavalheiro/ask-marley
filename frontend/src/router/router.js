import Vue from 'vue'
import Router from 'vue-router'
import home from '../views/Home.vue'
import results from '../views/Results.vue'
import about from '../views/About.vue'
import allDrugs from '../views/Drugs.vue'
//import drugInfo from '../views/DrugInfo.vue'
import drugInfo from '../components/SingleDrug.vue'
import admin from '../views/Admin.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  linkExactActiveClass: 'active',
  routes: [
    {
      path: '/',
      name: 'home',
      component: home
    },
    {
      path: '/',
      name: 'results',
      component: results
    },
    {
      path: '/about',
      name: 'about',
      component: about
    },
    {
      path: '/edit',
      name: 'admin',
      component: admin
    },
    {
      path: '/allDrugs',
      name: 'allDrugs',
      component: allDrugs,
      props: (route) => {
        return {
          fetchAll: true
        }
      }
    },{
      path: '/drugInfo',
      name: 'drugInfo',
      component: drugInfo,
      props: (route) => {
        return {
          drug: route.params.drug
        }
      }
    },

  ]
})

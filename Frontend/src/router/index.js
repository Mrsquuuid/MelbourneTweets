import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/1a',
    name: 'Page1A',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page1A.vue')
  },
  {
    path: '/1b',
    name: 'Page1B',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page1B.vue')
  },
  {
    path: '/1c',
    name: 'Page1C',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page1C.vue')
  },
  {
    path: '/1d',
    name: 'Page1D',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page1D.vue')
  },
  {
    path: '/1e',
    name: 'Page1E',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page1E.vue')
  },
  {
    path: '/1f',
    name: 'Page1F',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page1F.vue')
  },
  {
    path: '/1g',
    name: 'Page1G',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page1G.vue')
  },
  {
    path: '/1h',
    name: 'Page1H',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page1H.vue')
  },
  {
    path: '/2a',
    name: 'Page2A',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page2A.vue')
  },
  {
    path: '/2b',
    name: 'Page2B',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page2B.vue')
  },
  {
    path: '/2c',
    name: 'Page2C',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page2C.vue')
  },
  {
    path: '/2d',
    name: 'Page2D',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page2D.vue')
  },
  {
    path: '/2e',
    name: 'Page2E',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page2E.vue')
  },
  {
    path: '/2f',
    name: 'Page2F',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page2F.vue')
  },
  {
    path: '/3a',
    name: 'Page3A',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page3A.vue')
  },
  {
    path: '/3b',
    name: 'Page3B',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page3B.vue')
  },
  {
    path: '/3c',
    name: 'Page3C',
    component: () => import(/* webpackChunkName: "about" */ '../views/Page3C.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

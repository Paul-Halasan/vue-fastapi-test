import { createRouter, createWebHistory } from 'vue-router'
import ProductsPage from '../pages/ProductsPage.vue'
import MaterialsPage from '../pages/MaterialsPage.vue'

const routes = [
  {
    path: '/',
    redirect: '/products'
  },
  {
    path: '/products',
    name: 'products',
    component: ProductsPage
  },
  {
    path: '/materials',
    name: 'materials',
    component: MaterialsPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

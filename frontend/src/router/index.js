import { createRouter, createWebHistory } from 'vue-router'
import EmailInput from '@/views/EmailInput.vue'
import VerifyView from "@/views/VerifyView.vue";
import Index from "@/Index.vue";
import LoginView from "@/views/LoginView.vue";

const routes = [
  {
    path: '/',
    name: 'LoginView',
    component: LoginView
  },
  {
    path: '/email',
    name: 'EmailInput',
    component: EmailInput
  },
  {
    path: '/verify/:email',
    name: 'VerifyView',
    component: VerifyView
  },
  {
    path: '/index',
    name: 'Index',
    component: Index
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

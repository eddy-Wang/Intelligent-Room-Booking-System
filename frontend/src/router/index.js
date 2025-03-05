import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/LoginView.vue'
import EmailInput from '../pages/EmailInput.vue'
import LoginView from "@/pages/LoginView.vue";
import VerifyView from "@/pages/VerifyView.vue";

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
    path: '/verify',
    name: 'VerifyView',
    component: VerifyView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
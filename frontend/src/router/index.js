import { createRouter, createWebHistory } from 'vue-router'
import EmailInput from '@/views/EmailInput.vue'
import VerifyView from "@/views/VerifyView.vue";
import Index from "@/Index.vue";
import LoginView from "@/views/LoginView.vue";
import AdminIndex from "@/AdminIndex.vue";
import RoomManagementView from "@/views/RoomManagementView.vue";

const routes = [
  {
    path: '/',
    name: 'RoomManagement',
    component: RoomManagementView
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
  },
  {
    path:'/adminIndex',
    name:'AdminIndex',
    component: AdminIndex
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

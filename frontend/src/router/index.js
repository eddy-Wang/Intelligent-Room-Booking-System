import {createRouter, createWebHistory} from 'vue-router'
import EmailInput from '@/views/EmailInput.vue'
import VerifyView from "@/views/VerifyView.vue";
import Index from "@/Index.vue";
import IndexMobile from "@/IndexMobile.vue";
import LoginView from "@/views/LoginView.vue";
import AdminIndex from "@/AdminIndex.vue";
import AdminIndexMobile from "@/AdminIndexMobile.vue";
import AdminEnterPageMobile from "@/AdminEnterPageMobile.vue";


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
    },
    {
        path: '/indexMobile',
        name: 'IndexMobile',
        component: IndexMobile
    },
    {
        path: '/adminIndex',
        name: 'AdminIndex',
        component: AdminIndex
    },
    {
        path: '/adminIndexMobile',
        name: 'AdminIndexMobile',
        component: AdminIndexMobile
    },
    {
        path: '/adminEnterPageMobile',
        name: 'AdminEnterPageMobile',
        component: AdminEnterPageMobile
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router

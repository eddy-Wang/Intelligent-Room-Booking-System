import { createRouter, createWebHistory } from 'vue-router'
import TimeTable from '@/components/TimeTable.vue'
import MyReservation from '@/views/MyReservation.vue'
import RoomDetails from '@/views/RoomDetails.vue'
import RoomManagement from '@/views/RoomManagement.vue'
import Index from '@/Index.vue'


const routes = [
  { path: '/', name: 'Index', component: Index },
  { path: '/room/:id', name: 'RoomDetails', component: RoomDetails, props: true },
  { path: '/my-reservation', name: 'MyReservation', component: MyReservation },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
 
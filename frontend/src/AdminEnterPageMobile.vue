<template>
  <div class="admin-home-mobile-container">
    <div class="title-container">
      <h1><strong>DIICSU</strong></h1>
      <h2><strong>Room Booking System</strong></h2>
    </div>
    <div class="user-info-container">
      <div class="user-infor-header">
        User Information
      </div>
      <div class="user-avatar">
        <img
          :src="currentUser.avatar || 'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?q=80&w=2070&auto=format&fit=crop'"
          alt="User Avatar">
      </div>
      <div class="user-details">
        <div class="user-name">{{ currentUser.name || 'Unknown User' }}</div>
        <div class="user-email">{{ currentUser.email || 'No Email' }}</div>
        <div class="user-permission">{{ currentUser.permission || '' }}</div>
      </div>
    </div>
    <button class="enter-system-button" @click="goToUserSystem">
      User System
      <span class="arrow">→</span>
    </button>
    <button class="enter-system-button" @click="goToAdminSystem">
      Administrator System
      <span class="arrow">→</span>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, getCurrentInstance } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import IndexMobile from '@/IndexMobile.vue'
import AdminIndexMobile from '@/AdminIndexMobile.vue'

const instance = getCurrentInstance()
const router = useRouter()
const backendAddress = instance.appContext.config.globalProperties.$backendAddress
const currentUser = ref(instance.appContext.config.globalProperties.$user)
const users = ref([])

const fetchUsers = async () => {
  try {
    const response = await fetch(backendAddress + '/users')
    if (!response.ok) throw new Error('Failed to fetch users')
    const data = await response.json()
    users.value = data.data
  } catch (error) {
    console.error(error)
    ElMessage.error('Failed to load users')
  }
}

onMounted(() => {
  fetchUsers()
})

const goToUserSystem = () => {
  router.push({ name: 'IndexMobile' })
}

const goToAdminSystem = () => {
  router.push({ name: 'AdminIndexMobile' })
}
</script>

<style scoped>
.admin-home-mobile-container {
  font-family: 'Cambria', serif;
  display: flex;
  flex-direction: column;
  background-color: #eceef8;
  width: 100%;
  height: 100vh;
  padding: 20px;
  overflow: auto;
}

.title-container {
  margin-bottom: 0;
}

.title-container h1 {
  margin: 5px;
  font-size: 2.25rem;
  font-weight: bold;
}

.title-container h2 {
  margin: 5px;
  font-size: 2.25rem;
  color: #555;
}

.user-info-container {
  width: 100%;
  padding: 0 0 20px 0;
  background-color: white;
  border-radius: 20px;
  text-align: center;
  margin: 20px 0;
}

.user-infor-header {
  margin: 0 0 20px 0;
  font-weight: bolder;
  font-size: 1.25rem;
  background-color: #3155ef;
  color: white;
  height: 30px;
  width: 100%;
  line-height: 30px;
  text-align: center;
  border-radius: 20px 20px 0 0;
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}

.user-avatar img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.user-details {
  font-size: 1.1rem;
  color: #333;
}

.user-name {
  font-size: 1.2rem;
  font-weight: bold;
  margin-top: 10px;
}

.user-email {
  font-size: 1.1rem;
  margin-top: 10px;
}

.user-permission {
  font-size: 1.1rem;
  margin-top: 10px;
}

.enter-system-button {
  margin: 10px 0;
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1.1rem;
  transition: all 0.2s ease;
  background: #3155ef;
  color: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.arrow {
  font-size: 1.5rem;
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  pointer-events: none;
}
</style>

<template>
  <div class="reservation-management-mobile-container">
    <div class="title-container">
      <h1><strong>DRBS</strong></h1>
      <h2><strong>Reservation Management</strong></h2>
    </div>
    <div class="filter-controls">
      <!-- 搜索用户的控件保持单独一行 -->
      <el-autocomplete
          v-model="filters.userInput"
          :fetch-suggestions="queryUsers"
          clearable
          placeholder="Search by user"
          class="mobile-filter"
          @select="handleUserSelect"
      />
      <!-- 第一行：Rooms, Date, Time -->
      <div class="select-row">
        <el-select
            v-model="filters.room_id"
            multiple
            collapse-tags
            clearable
            placeholder="Rooms"
            class="mobile-filter"
        >
          <el-option
              v-for="room in rooms"
              :key="room.room_id"
              :label="room.name"
              :value="room.room_id"
          />
        </el-select>
        <el-select
            v-model="filters.date"
            multiple
            collapse-tags
            clearable
            placeholder="Date"
            class="mobile-filter"
        >
          <el-option
              v-for="date in sortedDates"
              :key="date"
              :label="formatDate(date)"
              :value="date"
          />
        </el-select>
        <el-select
            v-model="filters.time"
            multiple
            collapse-tags
            clearable
            placeholder="Time"
            class="mobile-filter"
        >
          <el-option
              v-for="timeSlot in timeSlots"
              :key="timeSlot"
              :label="timeSlot"
              :value="timeSlot"
          />
        </el-select>
      </div>
      <!-- 第二行：Processing State, Status -->
      <div class="select-row">
        <el-select
            v-model="filters.processing_state"
            multiple
            collapse-tags
            clearable
            placeholder="Processing State"
            class="mobile-filter"
        >
          <el-option
              v-for="state in processingStateOptions"
              :key="state"
              :label="state"
              :value="state"
          />
        </el-select>
        <el-select
            v-model="filters.status"
            multiple
            collapse-tags
            clearable
            placeholder="Status"
            class="mobile-filter"
        >
          <el-option
              v-for="status in statusOptions"
              :key="status"
              :label="status"
              :value="status"
          />
        </el-select>
      </div>
    </div>

    <div class="booking-list">
      <div
          v-for="booking in filteredBookings"
          :key="booking.booking_id"
          class="booking-card"
          :class="statusClass(booking.status)"
      >
        <div class="card-header">
          <div class="room-info">
            <div class="room-name">{{ getRoomName(booking.room_id) }}</div>
          </div>
          <div class="booking-status">
            <el-tag
                :type="statusTagType(booking.status)"
                size="mini"
                class="booking-status-tag"
                :data-status="booking.status"
            >
              {{ booking.status }}
            </el-tag>
          </div>
        </div>

        <div class="card-content">
          <div class="info-row">
            <el-icon class="info-icon">
              <User/>
            </el-icon>
            <span class="user-info">{{ getUserDisplay(booking.user_email) }}</span>
          </div>

          <div class="info-row">
            <el-icon class="info-icon">
              <Calendar/>
            </el-icon>
            <span class="user-info">{{ formatDate(booking.date) }}</span>
          </div>

          <div class="info-row">
            <el-icon class="info-icon">
              <Clock/>
            </el-icon>
            <div class="time-slots">
              <el-tag
                  v-for="(slot, index) in convertTimeStrToTimeSlots(booking.time).split('  ')"
                  :key="index"
                  size="mini"
                  class="time-tag"
              >
                {{ slot }}
              </el-tag>
            </div>
          </div>

          <div class="info-row">
            <el-icon class="info-icon">
              <Document/>
            </el-icon>
            <span class="purpose">{{ booking.purpose }}</span>
          </div>
        </div>

        <div class="card-actions">
          <template v-if="getProcessingState(booking.status) === 'processed'">
            <el-button size="mini" @click="modifyBooking(booking.booking_id, booking)" round>
              Edit
            </el-button>
            <el-button size="mini" @click="cancelBooking(booking.booking_id)" round>
              Cancel
            </el-button>
          </template>

          <template v-if="getProcessingState(booking.status) === 'unprocessed'">
            <el-button size="mini" @click="approveBooking(booking.booking_id)" round>
              Approve
            </el-button>
            <el-button size="mini" @click="rejectBooking(booking.booking_id)" round>
              Reject
            </el-button>
          </template>

          <el-button
              v-if="getProcessingState(booking.status) === 'completed'"
              size="mini"
              type="danger"
              @click="deleteBooking(booking.booking_id)"
              round
          >
            Delete
          </el-button>
        </div>

      </div>
    </div>

    <!-- 使用自定义模态框替换 Element Plus 的 Dialog -->
    <div v-if="modifyDialogVisible" class="modal" @click.self="modifyDialogVisible = false">
      <div class="modal-content">
        <h2>Modify Booking</h2>
        <form @submit.prevent="saveModifiedBooking">
          <label for="booking-user-email">User Email:</label>
          <input type="text" id="booking-user-email" v-model="currentBooking.user_email" disabled required/>

          <label for="booking-room">Room:</label>
          <select id="booking-room" v-model="currentBooking.room_id" required>
            <option v-for="room in rooms" :key="room.room_id" :value="room.room_id">
              {{ room.name }}
            </option>
          </select>

          <label for="booking-purpose">Purpose:</label>
          <input type="text" id="booking-purpose" v-model="currentBooking.purpose" required
                 placeholder="Meeting purpose"/>

          <label for="booking-date">Date:</label>
          <input type="date" id="booking-date" v-model="currentBooking.date" required/>

          <label for="booking-time">Time Slots:</label>
          <select id="booking-time" v-model="currentBooking.time" multiple required>
            <option v-for="(timeSlot, index) in timeSlots" :key="index" :value="index.toString()">
              {{ timeSlot }}
            </option>
          </select>

          <label for="booking-status">Status:</label>
          <select id="booking-status" v-model="currentBooking.status" required>
            <option value="Pending">Pending</option>
            <option value="Confirmed">Confirmed</option>
            <option value="Declined">Declined</option>
            <option value="Completed">Completed</option>
            <option value="Missed">Missed</option>
          </select>

          <div class="room-actions">
            <button type="submit" class="action-button">Save</button>
            <button type="button" @click="modifyDialogVisible = false" class="action-button">Cancel</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import {ref, computed, onMounted, getCurrentInstance, watch, onBeforeUnmount} from 'vue'
import {ElMessage} from 'element-plus'
import {User, Calendar, Clock, Document} from '@element-plus/icons-vue'

const instance = getCurrentInstance()
const backendAddress = instance.appContext.config.globalProperties.$backendAddress

// 响应式数据
const bookings = ref([])
const rooms = ref([])
const users = ref([])

// 编辑弹窗控制与当前预订数据
const modifyDialogVisible = ref(false)
const currentBooking = ref({})

// 过滤条件
const filters = ref({
  userInput: '',
  room_id: [],
  date: [],
  time: [],
  processing_state: [],
  status: []
})

// 常量定义
const statusOptions = ['Pending', 'Confirmed', 'Declined', 'Completed', 'Missed']
const processingStateOptions = ['unprocessed', 'processed', 'completed']
const reverseTimeSlotMap = {
  0: '08:00-08:45',
  1: '08:55-09:45',
  2: '10:00-10:45',
  3: '10:55-11:40',
  4: '12:00-12:45',
  5: '12:55-13:40',
  6: '14:00-14:45',
  7: '14:55-15:40',
  8: '16:00-16:45',
  9: '16:55-17:40',
  10: '19:00-19:45',
  11: '19:55-20:40'
}
const timeSlots = Object.values(reverseTimeSlotMap)

// 生成日期过滤项
const uniqueDates = computed(() => {
  return [...new Set(bookings.value.map(b => b.date))]
})
const sortedDates = computed(() => {
  return uniqueDates.value.sort((a, b) => new Date(a) - new Date(b))
})

// 过滤逻辑
const filteredBookings = computed(() => {
  if (!Array.isArray(bookings.value)) return []
  const result = bookings.value.filter(booking => {
    return Object.keys(filters.value).every(key => {
      const filterValue = filters.value[key]
      if (!filterValue || (Array.isArray(filterValue) && filterValue.length === 0) || (typeof filterValue === 'string' && filterValue.trim() === '')) {
        return true
      }
      if (key === 'userInput') {
        const user = users.value.find(u => u.email === booking.user_email)
        if (!user) return false
        return (
            user.name.toLowerCase().includes(filterValue.toLowerCase()) ||
            user.email.toLowerCase().includes(filterValue.toLowerCase()) ||
            user.permission.toLowerCase().includes(filterValue.toLowerCase())
        )
      }
      if (key === 'time') {
        const selectedTimeSlots = filterValue.map(time =>
            Object.keys(reverseTimeSlotMap).find(i => reverseTimeSlotMap[i] === time)
        )
        const bookingTimeSlots = booking.time.split(',').map(Number)
        return selectedTimeSlots.some(selectedTime => bookingTimeSlots.includes(Number(selectedTime)))
      }
      if (key === 'processing_state') {
        return filterValue.includes(getProcessingState(booking.status))
      }
      if (key === 'date') {
        return filterValue.includes(booking.date)
      }
      if (Array.isArray(booking[key])) {
        return booking[key].some(value => filterValue.includes(value))
      }
      return filterValue.includes(booking[key])
    })
  })
  return result.sort((a, b) => {
    const dateCompare = new Date(b.date) - new Date(a.date)
    if (dateCompare !== 0) return dateCompare
    const aMaxTime = Math.max(...a.time.split(',').map(Number))
    const bMaxTime = Math.max(...b.time.split(',').map(Number))
    return bMaxTime - aMaxTime
  })
})

// 用户搜索辅助函数
const queryUsers = (queryString, cb) => {
  const trimmedQuery = queryString.trim().toLowerCase()
  if (!trimmedQuery) {
    cb([])
    return
  }
  const results = users.value.filter(user => {
    const userName = user.name.replace(/\s+/g, '').toLowerCase()
    const userEmail = user.email.replace(/\s+/g, '').toLowerCase()
    const userPermission = user.permission.replace(/\s+/g, '').toLowerCase()
    return (
        userName.includes(trimmedQuery) ||
        userEmail.includes(trimmedQuery) ||
        userPermission.includes(trimmedQuery)
    )
  }).map(user => ({
    label: `${user.name} (${user.permission}) - ${user.email}`,
    value: `${user.name} (${user.permission}) - ${user.email}`,
    user
  }))
  cb(results)
}
const handleUserSelect = (selected) => {
  filters.value.userInput = selected.value.split(' (')[0]
}

// 获取房间名称
const getRoomName = (roomId) => {
  return rooms.value.find(r => r.room_id === roomId)?.name || 'Unknown Room'
}

// 映射处理状态
const getProcessingState = (status) => {
  const stateMap = {
    'Pending': 'unprocessed',
    'Confirmed': 'processed',
    'Declined': 'completed',
    'Completed': 'completed',
    'Missed': 'completed'
  }
  return stateMap[status] || 'unknown'
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-CA')
}

// 转换时间字符串为可读时间段
const convertTimeStrToTimeSlots = (timeStr) => {
  return timeStr.split(',')
      .map(Number)
      .map(index => reverseTimeSlotMap[index])
      .join('  ')
}

// 状态显示相关辅助方法
const statusClass = (status) => {
  const classMap = {
    'Pending': 'status-pending',
    'Confirmed': 'status-confirmed',
    'Declined': 'status-declined',
    'Completed': 'status-completed',
    'Missed': 'status-missed',
    'Banned': 'status-banned'
  }
  return classMap[status] || 'status-default'
}
const statusTagType = (status) => {
  const typeMap = {
    'Pending': 'warning',
    'Confirmed': 'success',
    'Declined': 'danger',
    'Completed': 'info',
    'Missed': 'info'
  }
  return typeMap[status] || 'info'
}
const getUserDisplay = (email) => {
  const user = users.value.find(u => u.email === email)
  return user ? `${user.name} (${user.permission})` : 'Unknown User'
}

// 数据请求
const fetchBookings = async () => {
  try {
    const response = await fetch(backendAddress + '/bookings')
    if (!response.ok) throw new Error('Failed to fetch bookings')
    const data = await response.json()
    bookings.value = data.data || []
  } catch (error) {
    ElMessage.error('Failed to load bookings')
  }
}
const fetchRooms = async () => {
  try {
    const response = await fetch(backendAddress + '/rooms_id_and_name')
    if (!response.ok) throw new Error('Failed to fetch rooms')
    const data = await response.json()
    rooms.value = data.data
  } catch (error) {
    ElMessage.error('Failed to load rooms')
  }
}
const fetchUsers = async () => {
  try {
    const response = await fetch(backendAddress + '/users')
    if (!response.ok) throw new Error('Failed to fetch users')
    const data = await response.json()
    users.value = data.data
  } catch (error) {
    ElMessage.error('Failed to load users')
  }
}

// 修改、保存、取消、审批、拒绝和删除预订
const modifyBooking = async (booking_id, newbooking) => {
  const booking = newbooking
  if (booking) {
    currentBooking.value = {
      ...booking,
      date: booking.date,             // 保持 YYYY-MM-DD 格式
      time: booking.time.split(',')   // 转为数组，便于多选
    }
    modifyDialogVisible.value = true
  }
}
const saveModifiedBooking = async () => {
  try {
    const payload = {
      ...currentBooking.value,
      time: currentBooking.value.time.sort().join(',')
    }
    const response = await fetch(backendAddress + '/modifyBooking', {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    })
    if (!response.ok) throw new Error('Update failed')
    ElMessage.success('Booking updated')
    modifyDialogVisible.value = false
    await fetchBookings()
  } catch (error) {
    ElMessage.error('Update failed')
  }
}
const cancelBooking = async (booking_id) => {
  try {
    const response = await fetch(backendAddress + `/bookings/${booking_id}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({status: 'Declined'})
    })
    if (!response.ok) throw new Error('Failed to cancel booking')
    ElMessage.success('Booking canceled successfully')
    fetchBookings()
  } catch (error) {
    ElMessage.error('Failed to cancel booking')
  }
}
const approveBooking = async (booking_id) => {
  try {
    const response = await fetch(backendAddress + `/bookings/${booking_id}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({status: 'Confirmed'})
    })
    if (!response.ok) throw new Error('Failed to approve booking')
    ElMessage.success('Booking approved successfully')
    fetchBookings()
  } catch (error) {
    ElMessage.error('Failed to approve booking')
  }
}
const rejectBooking = async (booking_id) => {
  try {
    const response = await fetch(backendAddress + `/bookings/${booking_id}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({status: 'Declined'})
    })
    if (!response.ok) throw new Error('Failed to reject booking')
    ElMessage.success('Booking rejected successfully')
    fetchBookings()
  } catch (error) {
    ElMessage.error('Failed to reject booking')
  }
}
const deleteBooking = async (booking_id) => {
  try {
    const response = await fetch(backendAddress + `/bookings/${booking_id}`, {
      method: 'DELETE'
    })
    if (!response.ok) throw new Error('Failed to delete booking')
    ElMessage.success('Booking deleted successfully')
    fetchBookings()
  } catch (error) {
    ElMessage.error('Failed to delete booking')
  }
}

// 锁定滚动的方案：记录当前滚动位置，并固定 body
let scrollPosition = 0
watch(modifyDialogVisible, (newVal) => {
  if (newVal) {
    // 记录当前滚动位置
    scrollPosition = window.pageYOffset || document.documentElement.scrollTop
    // 固定 body，并将 top 设置为负值
    document.body.style.position = 'fixed'
    document.body.style.top = `-${scrollPosition}px`
    document.body.style.left = '0'
    document.body.style.right = '0'
  } else {
    // 恢复 body 样式
    document.body.style.position = ''
    document.body.style.top = ''
    document.body.style.left = ''
    document.body.style.right = ''
    // 恢复滚动位置
    window.scrollTo(0, scrollPosition)
  }
})

// 组件卸载时清除设置
onBeforeUnmount(() => {
  document.body.style.position = ''
  document.body.style.top = ''
  document.body.style.left = ''
  document.body.style.right = ''
})

// 页面加载时获取数据
onMounted(async () => {
  await Promise.all([fetchBookings(), fetchRooms(), fetchUsers()])
})
</script>

<style scoped>
.reservation-management-mobile-container {
  font-family: 'Cambria', serif;
  display: flex;
  flex-direction: column;
  background-color: #eceef8;
  width: 100%;
  min-height: 100vh;
  padding: 20px;
  overflow: auto;
}

.title-container {
  margin-bottom: 1rem;
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

.filter-controls {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* select-row 用于将筛选组件排列成一行 */
.select-row {
  display: flex;
  flex-wrap: nowrap;
  gap: 0.5rem;
}

.booking-list {
  display: grid;
  gap: 1rem;
  margin-bottom: 2rem;
}

.booking-card {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.2rem;
  width: 100%;
  flex-wrap: nowrap;
}

.room-info {
  display: flex;
  align-items: center;
  gap: 0.2rem;
  min-width: 0;
}

.room-name {
  font-size: 1.1rem;
  font-weight: bold;
  word-break: break-word;
}

.room-name,
.booking-status {
  margin-top: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
}

.booking-status-tag {
  font-size: 1rem;
  font-weight: bold;
}

.booking-status-tag[data-status="Confirmed"] {
  background-color: #5ccb6a !important;
  border-color: #5ccb6a !important;
  color: #fff !important;
}

.booking-status-tag[data-status="Missed"] {
  background-color: #ff5757 !important;
  border-color: #ff5757 !important;
  color: #fff !important;
}

.booking-status-tag[data-status="Declined"] {
  background-color: #ffbd59 !important;
  border-color: #ffbd59 !important;
  color: #fff !important;
}

.booking-status-tag[data-status="Completed"] {
  background-color: #38b6ff !important;
  border-color: #38b6ff !important;
  color: #fff !important;
}

.booking-status-tag[data-status="Pending"] {
  background-color: #b58d54 !important;
  border-color: #b58d54 !important;
  color: #fff !important;
}

.booking-status-tag[data-status="Banned"] {
  background-color: #737373 !important;
  border-color: #737373 !important;
  color: #fff !important;
}

.card-content {
  display: grid;
  gap: 0.4rem;
  margin-top: 3%;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.info-icon {
  font-size: 1.2rem;
  color: #666;
}

.time-slots {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
}

.time-tag {
  font-size: 0.9rem;
  padding: 2px 6px;
}

.card-actions {
  margin: 1rem 10px auto 10px;
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
}

.card-actions .el-button {
  width: 45%;
  font-size: 1rem;
  height: 1.6rem;
}

/* 自定义模态框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  padding: 15px;
}

.modal-content {
  background: white;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  padding: 20px;
  margin: auto;
  border-radius: 12px;
}

.modal-content form {
  display: flex;
  flex-direction: column;
}

.modal-content label {
  margin: 8px 0 4px;
  font-weight: 500;
}

.modal-content input,
.modal-content select,
.modal-content textarea {
  width: 100%;
  padding: 12px;
  margin-bottom: 8px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
}

.room-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.action-button {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #3155ef;
  color: #FFFFFF;
}

.status-pending {
  border-left: 4px solid #b58d54;
}

.status-confirmed {
  border-left: 4px solid #5ccb6a;
}

.status-declined {
  border-left: 4px solid #ffbd59;
}

.status-completed {
  border-left: 4px solid #38b6ff;
}

.status-missed {
  border-left: 4px solid #ff5757;
}

.status-banned {
  border-left: 4px solid #737373;
}
</style>

<template>
  <div class="mobile-booking-management">
    <!-- Header Section -->
    <header class="app-header">
      <div class="app-title">
        <h1><strong>DRBS</strong></h1>
        <h2><strong>Reservation Management</strong></h2>
      </div>
    </header>

    <!-- Filter Panel -->
    <div class="filter-controls">
      <el-select
          v-model="filters.room_id"
          multiple
          collapse-tags
          placeholder="Filter Rooms"
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
          v-model="filters.status"
          multiple
          collapse-tags
          placeholder="Filter Status"
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

    <!-- Booking List -->
    <div class="booking-list">
      <div
          v-for="booking in filteredBookings"
          :key="booking.booking_id"
          class="booking-card"
          :class="statusClass(booking.status)"
      >
        <div class="card-header">
          <div class="room-info">
            <h3 class="room-name">{{ getRoomName(booking.room_id) }}</h3>
            <el-tag :type="statusTagType(booking.status)" size="mini">
              {{ booking.status }}
            </el-tag>
          </div>
          <span class="booking-date">{{ formatDate(booking.date) }}</span>
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

    <!-- Modify Dialog -->
    <el-dialog
        v-model="modifyDialogVisible"
        title="Modify Booking"
        fullscreen
        :before-close="handleCloseModifyDialog"
    >
      <el-form
          :model="currentBooking"
          label-position="top"
          class="mobile-form"
      >
        <!-- User Email -->
        <el-form-item label="User Email">
          <el-input
              v-model="currentBooking.user_email"
              disabled
              class="mobile-input"
          />
        </el-form-item>

        <!-- Room Selection -->
        <el-form-item label="Room">
          <el-select
              v-model="currentBooking.room_id"
              placeholder="Select Room"
              class="mobile-select"
          >
            <el-option
                v-for="room in rooms"
                :key="room.room_id"
                :label="room.name"
                :value="room.room_id"
            />
          </el-select>
        </el-form-item>

        <!-- Purpose -->
        <el-form-item label="Purpose">
          <el-input
              v-model="currentBooking.purpose"
              class="mobile-input"
              placeholder="Meeting purpose"
          />
        </el-form-item>

        <!-- Date Picker -->
        <el-form-item label="Date">
          <el-date-picker
              v-model="currentBooking.date"
              type="date"
              placeholder="Select date"
              value-format="YYYY-MM-DD"
              class="mobile-date-picker"
          />
        </el-form-item>

        <!-- Time Slots -->
        <el-form-item label="Time Slots">
          <el-select
              v-model="currentBooking.time"
              multiple
              placeholder="Select times"
              class="mobile-multi-select"
          >
            <el-option
                v-for="(timeSlot, index) in timeSlots"
                :key="index"
                :label="timeSlot"
                :value="index.toString()"
            />
          </el-select>
        </el-form-item>

        <!-- Status -->
        <el-form-item label="Status">
          <el-select
              v-model="currentBooking.status"
              placeholder="Select status"
              class="mobile-select"
          >
            <el-option label="Pending" value="Pending"/>
            <el-option label="Confirmed" value="Confirmed"/>
            <el-option label="Declined" value="Declined"/>
            <el-option label="Completed" value="Completed"/>
            <el-option label="Missed" value="Missed"/>
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer-mobile">
          <el-button
              class="footer-button"
              @click="modifyDialogVisible = false"
          >
            Cancel
          </el-button>
          <el-button
              type="primary"
              class="footer-button"
              @click="saveModifiedBooking"
          >
            Save
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue'
import {ElButton, ElMessage, ElOption, ElSelect} from 'element-plus'
import {User, Clock, Document} from '@element-plus/icons-vue'

// Reactive state
const bookings = ref([])
const rooms = ref([])
const users = ref([])
const modifyDialogVisible = ref(false)
const currentBooking = ref({})
const filters = ref({
  room_id: [],
  status: [],
  processing_state: []
})
const handleCloseModifyDialog = () => {
  modifyDialogVisible.value = false;
};
// Constants
const statusOptions = ['Pending', 'Confirmed', 'Declined', 'Completed', 'Missed']
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
const timeSlots = Object.values(reverseTimeSlotMap);
const filteredBookings = computed(() => {
  const filtered = bookings.value.filter(booking => {
    const roomMatch = filters.value.room_id.length === 0 ||
        filters.value.room_id.includes(booking.room_id)
    const statusMatch = filters.value.status.length === 0 ||
        filters.value.status.includes(booking.status)
    return roomMatch && statusMatch
  })
  return filtered.sort((a, b) => {
    const dateCompare = new Date(b.date) - new Date(a.date)
    if (dateCompare !== 0) return dateCompare

    const aMaxTime = Math.max(...a.time.split(',').map(Number))
    const bMaxTime = Math.max(...b.time.split(',').map(Number))
    return bMaxTime - aMaxTime
  })
})

// Methods
const statusClass = (status) => {
  const classMap = {
    'Pending': 'status-pending',
    'Confirmed': 'status-confirmed',
    'Declined': 'status-declined',
    'Completed': 'status-completed',
    'Missed': 'status-missed'
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
const handleDateChange = (date) => {
  console.log('Selected Date:', date);
  console.log('Current Booking Date:', currentBooking.value.date);
};

const getRoomName = (roomId) => {
  return rooms.value.find(r => r.room_id === roomId)?.name || 'Unknown Room'
}

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

const getUserDisplay = (email) => {
  const user = users.value.find(u => u.email === email)
  return user ? `${user.name} (${user.permission})` : 'Unknown User'
}

const convertTimeStrToTimeSlots = (timeStr) => {
  return timeStr.split(',')
      .map(Number)
      .map(index => reverseTimeSlotMap[index])
      .join('  ')
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-CA')
}

// Data fetching
const fetchBookings = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8080/bookings')
    if (!response.ok) throw new Error('Failed to fetch bookings')
    const data = await response.json()
    bookings.value = data.data || []
  } catch (error) {
    ElMessage.error('Failed to load bookings')
  }
}

const fetchRooms = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8080/rooms_id_and_name')
    if (!response.ok) throw new Error('Failed to fetch rooms')
    const data = await response.json()
    rooms.value = data.data
  } catch (error) {
    ElMessage.error('Failed to load rooms')
  }
}

const fetchUsers = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8080/users')
    if (!response.ok) throw new Error('Failed to fetch users')
    const data = await response.json()
    users.value = data.data
  } catch (error) {
    ElMessage.error('Failed to load users')
  }
}

const modifyBooking = async (booking_id, newbooking) => {
  const booking = newbooking;
  if (booking) {
    const formattedDate = formatDate(booking.date);
    currentBooking.value = {
      ...booking,
      date: formattedDate,
      time: booking.time.split(',')
    };
    console.log("Current Booking after initialization:", currentBooking.value);
    modifyDialogVisible.value = true;
  }
};

const saveModifiedBooking = async () => {
  try {
    const payload = {
      ...currentBooking.value,
      time: currentBooking.value.time.sort().join(',')
    }

    const response = await fetch('http://127.0.0.1:8080/modifyBooking', {
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
    const response = await fetch(`http://127.0.0.1:8080/bookings/${booking_id}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({status: 'Declined'})
    });
    if (!response.ok) throw new Error('Failed to cancel booking');
    ElMessage.success('Booking canceled successfully');
    fetchBookings(); // Refresh data
  } catch (error) {
    console.error('Error canceling booking:', error);
    ElMessage.error('Failed to cancel booking');
  }
};
// Function to approve a booking
const approveBooking = async (booking_id) => {
  try {
    const response = await fetch(`http://127.0.0.1:8080/bookings/${booking_id}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({status: 'Confirmed'})
    });
    if (!response.ok) throw new Error('Failed to approve booking');
    ElMessage.success('Booking approved successfully');
    fetchBookings(); // Refresh data
  } catch (error) {
    console.error('Error approving booking:', error);
    ElMessage.error('Failed to approve booking');
  }
};
// Function to reject a booking
const rejectBooking = async (booking_id) => {
  try {
    const response = await fetch(`http://127.0.0.1:8080/bookings/${booking_id}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({status: 'Declined'})
    });
    if (!response.ok) throw new Error('Failed to reject booking');
    ElMessage.success('Booking rejected successfully');
    fetchBookings(); // Refresh data
  } catch (error) {
    console.error('Error rejecting booking:', error);
    ElMessage.error('Failed to reject booking');
  }
};
// Function to delete a booking
const deleteBooking = async (booking_id) => {
  try {
    const response = await fetch(`http://127.0.0.1:8080/bookings/${booking_id}`, {
      method: 'DELETE'
    });
    if (!response.ok) throw new Error('Failed to delete booking');
    ElMessage.success('Booking deleted successfully');
    fetchBookings(); // Refresh data
  } catch (error) {
    console.error('Error deleting booking:', error);
    ElMessage.error('Failed to delete booking');
  }
};

// Lifecycle
onMounted(async () => {
  await Promise.all([fetchBookings(), fetchRooms(), fetchUsers()])
})
</script>

<style scoped>
.mobile-booking-management {
  padding: 1rem;
  background: #f8f9fa;
  min-height: 100vh;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.header-controls {
  display: flex;
  gap: 0.5rem;
}

.new-booking-button {
  width: 40px;
  height: 40px;
  font-size: 1.2rem;
}

.booking-list {
  display: grid;
  gap: 1rem;
  margin-bottom: 100px;
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
  gap: 0.5rem;
  width: 100%;
}

.room-info {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  min-width: 0;
}

.room-name {
  font-size: 1.1rem;
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 0;
}

.booking-date {
  font-size: 0.9rem;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 120px;
  margin-left: auto;
}

.card-content {
  display: grid;
  gap: 1rem;
  margin-top: 3%;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 0.8rem;
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
  font-size: 0.7rem;
  padding: 2px 6px;
}

.card-actions {
  margin-top: 1rem;
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-controls {
  z-index: 1000;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  padding: 1rem;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 0.5rem;
  margin-bottom: 50px;
  border-radius: 10px;
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.status-pending {
  border-left: 4px solid #e6a23c;
}

.status-confirmed {
  border-left: 4px solid #67c23a;
}

.status-declined {
  border-left: 4px solid #f56c6c;
}

.status-completed {
  border-left: 4px solid #909399;
}

.status-missed {
  border-left: 4px solid #909399;
}

.mobile-form {
  padding: 0 1rem;
}

.mobile-input,
.mobile-select,
.mobile-date-picker,
.mobile-multi-select {
  width: 100%;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #333;
}

/* Date Picker Mobile Optimization */
:deep(.el-date-editor.el-input) {
  width: 100%;
}

/* Multi-select Mobile Styling */
:deep(.el-select__tags) {
  flex-wrap: wrap;
  max-height: 80px;
  overflow-y: auto;
}

/* Footer Buttons */
.dialog-footer-mobile {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
}

.footer-button {
  flex: 1;
  padding: 1rem;
  font-size: 1.1rem;
}

@media (max-width: 480px) {
  .app-title {
    font-size: 1.2rem;
  }

  .booking-card {
    padding: 0.8rem;
  }

  .room-name {
    font-size: 1rem;
  }
}
</style>
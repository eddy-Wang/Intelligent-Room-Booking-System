<template>
  <div class="booking-management">
    <h2 class="page-title">Reservation Management</h2>
    <el-card class="custom-card">
      <el-table :data="filteredBookings" border stripe style="width: 100%" class="el-table">

        <!-- User Column -->
        <el-table-column class="el-table-column" label="User">
          <template #header>
            <div class="filter-header">
              <span>User</span>
              <el-autocomplete
                  v-model="filters.userInput"
                  :fetch-suggestions="queryUsers"
                  clearable
                  placeholder="Search by user"
                  @select="handleUserSelect"
              />
            </div>
          </template>
          <template #default="{ row }">
            {{ getUserDisplay(row.user_email) }}
          </template>
        </el-table-column>


        <!-- Room Name Column -->
        <el-table-column class="el-table-column" label="Room Name">
          <template #header>
            <div class="filter-header">
              <span>Room Name</span>
              <el-select v-model="filters.room_id" multiple clearable placeholder="Filter">
                <el-option v-for="value in uniqueValues('room_id')" :key="value" :label="getRoomName(value)"
                           :value="value"/>
              </el-select>
            </div>
          </template>
          <template #default="{ row }">
            {{ getRoomName(row.room_id) }} <!-- Displaying room name instead of room_id -->
          </template>
        </el-table-column>
        <!-- Purpose Column -->
        <el-table-column class="el-table-column" prop="purpose" label="Purpose">
        </el-table-column>

        <el-table-column class="el-table-column" prop="date" label="Date"
                         default-sort="{ prop: 'date', order: 'ascending' }">
          <template #header>
            <div class="filter-header">
              <span>Date</span>
              <el-select v-model="filters.date" multiple clearable placeholder="Filter">
                <!-- 调用方法对日期进行排序 -->
                <el-option
                    v-for="value in sortDates(uniqueValues('date'))"
                    :key="value"
                    :label="formatDate(value)"
                    :value="value"
                />
              </el-select>
            </div>
          </template>
          <template #default="{ row }">
            {{ formatDate(row.date) }} <!-- Converting time slots to human-readable format -->
          </template>
        </el-table-column>

        <!-- Time Column -->
        <el-table-column class="el-table-column" prop="time" label="Time">
          <template #header>
            <div class="filter-header">
              <span>Time</span>
              <el-select v-model="filters.time" multiple clearable placeholder="Filter">
                <el-option
                    v-for="(timeSlot, index) in timeSlots"
                    :key="index"
                    :label="timeSlot"
                    :value="timeSlot"/>
              </el-select>
            </div>
          </template>
          <template #default="{ row }">
            {{ convertTimeStrToTimeSlots(row.time) }} <!-- Converting time slots to human-readable format -->
          </template>
        </el-table-column>

        <!-- Processing State Column -->
        <el-table-column class="el-table-column" label="Processing State">
          <template #header>
            <div class="filter-header">
              <span>Processing State</span>
              <el-select v-model="filters.processing_state" multiple clearable placeholder="Filter">
                <el-option v-for="value in processingStateOptions" :key="value" :label="value" :value="value"/>
              </el-select>
            </div>
          </template>
          <template #default="{ row }">
            {{ getProcessingState(row.status) }} <!-- Displaying processing state based on status -->
          </template>
        </el-table-column>

        <!-- Status Column -->
        <el-table-column class="el-table-column" prop="status" label="Status">
          <template #header>
            <div class="filter-header">
              <span>Status</span>
              <el-select v-model="filters.status" multiple clearable placeholder="Filter">
                <el-option v-for="value in uniqueValues('status')" :key="value" :label="value" :value="value"/>
              </el-select>
            </div>
          </template>
        </el-table-column>

        <!-- Application Time Column (New) -->
        <el-table-column class="el-table-column" prop="application_time" label="Application Time" sortable>
          <template #default="{ row }">
            {{ timestampToTime(row.booking_id) }} <!-- Convert booking_id (timestamp) to application time -->
          </template>
        </el-table-column>

        <!-- Action Column (New) -->
        <el-table-column class="el-table-column" label="Actions" width="250">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button class="el-button"
                         v-if="getProcessingState(row.status) === 'processed'"
                         size="small"
                         @click="modifyBooking(row.booking_id,row)">
                Modify
              </el-button>
              <el-button class="el-button"
                         v-if="getProcessingState(row.status) === 'processed'"
                         size="small"
                         @click="cancelBooking(row.booking_id)">
                Cancel
              </el-button>

              <el-button class="el-button"
                         v-if="getProcessingState(row.status) === 'unprocessed'"
                         size="small"
                         @click="approveBooking(row.booking_id)">
                Approve
              </el-button>
              <el-button class="el-button"
                         v-if="getProcessingState(row.status) === 'unprocessed'"
                         size="small"
                         @click="rejectBooking(row.booking_id)">
                Reject
              </el-button>

              <el-button class="el-button"
                         v-if="getProcessingState(row.status) === 'completed'"
                         size="small"
                         @click="deleteBooking(row.booking_id)">
                Delete
              </el-button>
            </div>
          </template>
        </el-table-column>

      </el-table>
    </el-card>
    <!-- Modify Dialog -->
    <el-dialog
        v-model="modifyDialogVisible"
        title="Modify Booking"
        width="50%"
        :before-close="handleCloseModifyDialog"
    >
      <el-form :model="currentBooking" label-width="120px">
        <!-- User Email -->
        <el-form-item label="User Email">
          <el-input v-model="currentBooking.user_email" disabled/>
        </el-form-item>

        <!-- Room Name -->
        <el-form-item label="Room Name">
          <el-select v-model="currentBooking.room_id" placeholder="Select Room">
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
          <el-input v-model="currentBooking.purpose"/>
        </el-form-item>

        <!-- Date -->
        <el-form-item label="Date">
          <el-date-picker
              v-model="currentBooking.date"
              type="date"
              placeholder="Select Date"
              value-format="YYYY-MM-DD"
              @change="handleDateChange"
          />
        </el-form-item>

        <!-- Time Slots -->
        <el-form-item label="Time Slots">
          <el-select
              v-model="currentBooking.time"
              multiple
              placeholder="Select Time Slots"
          >
            <el-option
                v-for="(timeSlot, index) in timeSlots.sort()"
                :key="index"
                :label="timeSlot"
                :value="index.toString()"
            />
          </el-select>
        </el-form-item>

        <!-- Status -->
        <el-form-item label="Status">
          <el-select v-model="currentBooking.status" placeholder="Select Status">
            <el-option label="Pending" value="Pending"/>
            <el-option label="Confirmed" value="Confirmed"/>
            <el-option label="Declined" value="Declined"/>
            <el-option label="Completed" value="Completed"/>
            <el-option label="Missed" value="Missed"/>
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="modifyDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="saveModifiedBooking">Save</el-button>
      </template>
    </el-dialog>
  </div>

</template>
<script setup>
import {ref, computed, onMounted} from 'vue';

import {ElTable, ElTableColumn, ElSelect, ElOption, ElCard, ElButton, ElMessage} from 'element-plus';
import 'element-plus/dist/index.css';

// Define reactive data
const bookings = ref([]);
const rooms = ref([]);
const users = ref([]);
const filters = ref({
  user_email: [],
  room_id: [],
  date: [],
  time: [],
  status: [],
  permission: [],
  processing_state: []
});

// Time slots mapping
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
};
const timeSlots = Object.values(reverseTimeSlotMap);
const processingStateOptions = ['unprocessed', 'processed', 'completed'];

// Fetch rooms from backend API
const fetchRooms = async () => {
  try {
    const response = await fetch('http://172.20.10.3:8080/rooms_id_and_name');

    if (!response.ok) throw new Error('Failed to fetch rooms');
    const data = await response.json();
    rooms.value = data.data;
  } catch (error) {
    console.error('Error fetching rooms:', error);
  }
};
const fetchUsers = async () => {
  try {
    const response = await fetch('http://172.20.10.3:8080/users');
    if (!response.ok) throw new Error('Failed to fetch users');
    const data = await response.json();
    users.value = data.data;
  } catch (error) {
    console.error('Error fetching users:', error);
  }
};

const getUserDisplay = (email) => {
  const user = users.value.find(u => u.email === email);
  return user ? `${user.name} (${user.permission})` : 'Unknown User';
};

const sortDates = (dates) => {

  return dates.sort((a, b) => new Date(a) - new Date(b));
};
const queryUsers = (queryString, cb) => {
  const trimmedQuery = queryString.trim().toLowerCase().trim();

  if (!trimmedQuery) {
    cb([]);
    return;
  }

  const results = users.value
      .filter(user => {
        const userName = user.name.replace(/\s+/g, '').toLowerCase();
        const userEmail = user.email.replace(/\s+/g, '').toLowerCase();
        const userPermission = user.permission.replace(/\s+/g, '').toLowerCase();

        return (
            userName.includes(trimmedQuery) ||
            userEmail.includes(trimmedQuery) ||
            userPermission.includes(trimmedQuery) ||
            trimmedQuery.includes(userName) ||
            trimmedQuery.includes(userEmail) ||
            trimmedQuery.includes(userPermission)
        );
      })
      .map(user => ({
        label: `${user.name} (${user.permission}) - ${user.email}`,
        value: `${user.name} (${user.permission}) - ${user.email}`,
        user
      }));

  cb(results);
};
const modifyDialogVisible = ref(false);
const currentBooking = ref({});


const handleCloseModifyDialog = () => {
  modifyDialogVisible.value = false;
};


const saveModifiedBooking = async () => {
  try {
    console.log(currentBooking.value)
    const payload = {
      ...currentBooking.value,
      time: currentBooking.value.time.sort(),
    };
    console.log(3)
    const response = await fetch(`http://172.20.10.3:8080/modifyBooking`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload),
    });
    console.log(payload.date);
    if (!response.ok) throw new Error('Failed to update booking');
    ElMessage.success('Booking updated successfully');
    modifyDialogVisible.value = false;
    fetchBookings();
  } catch (error) {
    console.error('Error updating booking:', error);
    ElMessage.error('Failed to update booking');
  }
};
const handleUserSelect = (selected) => {
  filters.value.userInput = selected.value.split(' (')[0];
};
// Function to modify a booking
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
const handleDateChange = (date) => {
  console.log('Selected Date:', date);
  console.log('Current Booking Date:', currentBooking.value.date);
};
// Function to cancel a booking
const cancelBooking = async (booking_id) => {
  try {
    const response = await fetch(`http://172.20.10.3:8080/bookings/${booking_id}`, {
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
    const response = await fetch(`http://172.20.10.3:8080/bookings/${booking_id}`, {
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
    const response = await fetch(`http://172.20.10.3:8080/bookings/${booking_id}`, {
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
    const response = await fetch(`http://172.20.10.3:8080/bookings/${booking_id}`, {
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


// Fetch data on component mount
onMounted(() => {
  fetchBookings();
  fetchRooms();
  fetchUsers();
});

// Function to convert timestamp to a readable time format
const timestampToTime = (timestamp) => {
  const timestampInSeconds = timestamp / 1000;
  const time = new Date(timestampInSeconds * 1000);
  return time.toISOString().replace('T', ' ').slice(0, 19); // Format as 'YYYY-MM-DD HH:MM:SS'
};

// Function to get room name by room_id
const getRoomName = (room_id) => {
  const room = rooms.value.find(r => r.room_id === room_id);
  return room ? room.name : 'Unknown Room';
};

// Function to map status to processing state
const getProcessingState = (status) => {
  const processingStateMap = {
    'Pending': 'unprocessed',
    'Confirmed': 'processed',
    'Declined': 'completed',
    'Completed': 'completed',
    'Missed': 'completed'
  };
  return processingStateMap[status] || 'unknown';
};

// Function to get unique values for filters
const uniqueValues = (key) => [...new Set(bookings.value.map((item) => item[key]))];

// Function to convert time index to time slots
const convertTimeStrToTimeSlots = (timeStr) => {
  return timeStr.split(',')
      .map(Number)
      .map(index => reverseTimeSlotMap[index])
      .join('  ');
};
const fetchBookings = async () => {
  try {
    const response = await fetch('http://172.20.10.3:8080/bookings');
    if (!response.ok) throw new Error('Failed to fetch bookings');
    const booking = await response.json();
    const data = booking.data;
    console.log(data)
    if (Array.isArray(data)) {
      bookings.value = data;
    } else {
      console.error('Expected an array but got:', data);
      bookings.value = [];
    }
  } catch (error) {
    console.error('Error fetching bookings:', error);
  }
};
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-CA');
};

const filteredBookings = computed(() => {
  if (!Array.isArray(bookings.value)) {
    console.error('bookings.value is not an array:', bookings.value);
    return [];
  }

  return bookings.value.filter((booking) => {
    return Object.keys(filters.value).every((key) => {
      const filterValue = filters.value[key];

      if (!filterValue || filterValue.length === 0) {
        return true;
      }

      if (key === 'userInput') {
        const user = users.value.find(u => u.email === booking.user_email);
        if (!user) return false;
        return (
            user.name.toLowerCase().includes(filterValue.toLowerCase()) ||
            user.email.toLowerCase().includes(filterValue.toLowerCase()) ||
            user.permission.toLowerCase().includes(filterValue.toLowerCase())
        );
      }

      if (key === 'time') {
        const selectedTimeSlots = filterValue.map(time =>
            Object.keys(reverseTimeSlotMap).find(i => reverseTimeSlotMap[i] === time)
        );
        const bookingTimeSlots = booking.time.split(',').map(Number);
        return selectedTimeSlots.some(selectedTime => bookingTimeSlots.includes(Number(selectedTime)));
      }

      if (key === 'processing_state') {
        return filterValue.includes(getProcessingState(booking.status));
      }

      if (Array.isArray(booking[key])) {
        return booking[key].some(value => filterValue.includes(value));
      }

      return filterValue.includes(booking[key]);
    });
  });
});

</script>

<style scoped>

.page-title {
  font-size: 40px;
  font-weight: bold;
  margin-bottom: 20px;
  padding: 10px;
}

.el-table {
  height: 700px;
  width: 100%;
  overflow: auto;
}

.booking-management {
  font-family: 'Cambria', serif;
  width: 100%;
  padding: 20px;
  background-color: #f8f9fa;
  overflow: auto;
}

.custom-card {
  width: 100%;
  padding: 20px;
  border-radius: 12px;
  overflow: auto;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.filter-header {
  height: 100%;
  width: 100%;
  display: flow-root;
  justify-content: space-between;
  align-items: center;
}

.action-buttons {
  align-items: flex-start;
}

.el-button {
  width: 40%;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.1rem;
  background-color: #eceef8;
  color: #333;
  transition: background-color 0.2s ease;
}

.el-button:disabled {
  background-color: #a6a6a6;
  cursor: not-allowed;
}

.el-button:not(:disabled):hover {
  background-color: #3155ef;
  color: #fff;
}

.el-table-column {
  width: 5%;
}

</style>

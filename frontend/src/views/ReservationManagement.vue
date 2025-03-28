<!--
ReservationManagement.vue - Vue component for managing room reservations.

This component provides:
- Comprehensive reservation listing with filtering capabilities
- CRUD operations for reservations (create, read, update, delete)
- Approval/rejection workflow for pending reservations
- Excel export functionality
- Time slot management interface

Props: None
Events: None
Dependencies:
- Element Plus UI components
- XLSX library for Excel export
- Vue 3 Composition API
-->
<template>
  <div class="booking-management">
    <div class="header">
      <h2 class="page-title">Reservation Management</h2>
        <div class="button-group">
            <el-button class="new-button" type="primary" @click="openLimitUsageDialog">Limit usage time</el-button>
            <el-button class="export-button" type="success" @click="exportToExcel">Export to Excel</el-button>
        </div>
    </div>
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
    <!-- Limit Usage Time Dialog -->
    <el-dialog
        v-model="limitUsageDialogVisible"
        title="Limit Usage Time"
        width="50%"
        :before-close="handleCloseLimitUsageDialog"
    >
      <el-form :model="limitUsageForm" label-width="120px">
        <!-- Room Name -->
        <el-form-item label="Room Name">
          <el-select v-model="limitUsageForm.room_id" placeholder="Select Room">
            <el-option
                v-for="room in rooms"
                :key="room.room_id"
                :label="room.name"
                :value="room.room_id"
            />
          </el-select>
        </el-form-item>

        <!-- Date -->
        <el-form-item label="Date">
          <el-date-picker
              v-model="limitUsageForm.date"
              type="date"
              placeholder="Select Date"
              value-format="YYYY-MM-DD"
              :disabled-date="disabledDate"
          />
        </el-form-item>

        <!-- Time Slots -->
        <el-form-item label="Time Slots">
          <el-select
              v-model="limitUsageForm.time"
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
        <el-form-item label="Purpose">
          <el-input
              v-model="limitUsageForm.purpose"
              placeholder="Enter purpose"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="limitUsageDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="submitLimitUsage">Submit</el-button>
      </template>
    </el-dialog>
    <!-- Cancel Reason Dialog -->
    <el-dialog
        v-model="cancelDialogVisible"
        title="Cancel Booking"
        width="50%"
    >
      <el-form :model="cancelForm" label-width="120px">
        <el-form-item label="Reason">
          <el-input
              v-model="cancelForm.reason"
              type="textarea"
              :rows="2"
              placeholder="Please enter the reason for cancellation"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="cancelDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="confirmCancelBooking">Confirm</el-button>
      </template>
    </el-dialog>
    <!-- Reject Reason Dialog -->
    <el-dialog
        v-model="rejectDialogVisible"
        title="Reject Booking"
        width="50%"
    >
      <el-form :model="rejectForm" label-width="120px">
        <el-form-item label="Reason">
          <el-input
              v-model="rejectForm.reason"
              type="textarea"
              :rows="4"
              placeholder="Please enter the reason for rejection"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="rejectDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="confirmRejectBooking">Confirm</el-button>
      </template>
    </el-dialog>
  </div>

</template>
<script setup>
import {ref, computed, onMounted, getCurrentInstance} from 'vue';
import 'element-plus/dist/index.css';
import * as XLSX from 'xlsx';
import {ElMessage} from "element-plus";

/**
 * Exports filtered bookings to Excel
 */
const exportToExcel = () => {
    // Prepare the data for export
    const dataForExport = filteredBookings.value.map(booking => {
        return {
            'User': getUserDisplay(booking.user_email),
            'Room Name': getRoomName(booking.room_id),
            'Purpose': booking.purpose,
            'Date': formatDate(booking.date),
            'Time': convertTimeStrToTimeSlots(booking.time),
            'Processing State': getProcessingState(booking.status),
            'Status': booking.status,
            'Application Time': timestampToTime(booking.booking_id)
        };
    });

    // Create worksheet
    const ws = XLSX.utils.json_to_sheet(dataForExport);

    // Create workbook
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Reservations");

    // Generate file name with current date
    const dateStr = new Date().toISOString().slice(0, 10);
    const fileName = `Reservations_${dateStr}.xlsx`;

    // Export the file
    XLSX.writeFile(wb, fileName);
};
const instance = getCurrentInstance()
const backendAddress = instance.appContext.config.globalProperties.$backendAddress
const userEmail = ref("")
// Reject dialog related data
const rejectDialogVisible = ref(false);
const rejectForm = ref({
  booking_id: null,
  reason: ''
});
// Define reactive data
const bookings = ref([]);  // All booking records
const rooms = ref([]);     // Available rooms
const users = ref([]);     // System users
// Filter state
const filters = ref({
  user_email: [],
  room_id: [],
  date: [],
  time: [],
  status: [],
  permission: [],
  processing_state: []
});
// Cancel dialog related data
const cancelDialogVisible = ref(false);
const cancelForm = ref({
  booking_id: null,
  reason: ''
});// Time slots mapping
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

/**
 * Fetches room data from backend
 */
const fetchRooms = async () => {
  try {
    const response = await fetch(backendAddress + '/rooms_id_and_name');

    if (!response.ok) throw new Error('Failed to fetch rooms');
    const data = await response.json();
    rooms.value = data.data;
  } catch (error) {
    console.error('Error fetching rooms:', error);
  }
};
/**
 * Fetches user data from backend
 */
const fetchUsers = async () => {
  try {
    const response = await fetch(backendAddress + '/users');
    if (!response.ok) throw new Error('Failed to fetch users');
    const data = await response.json();
    users.value = data.data;
  } catch (error) {
    console.error('Error fetching users:', error);
  }
};
/**
 * Gets user display name with permission
 * @param {string} email - User email
 * @returns {string} Formatted user display
 */
const getUserDisplay = (email) => {
  const user = users.value.find(u => u.email === email);
  return user ? `${user.name} (${user.permission})` : 'Unknown User';
};
/**
 * Sorts date strings chronologically
 * @param {Array} dates - Array of date strings
 * @returns {Array} Sorted dates
 */
const sortDates = (dates) => {

  return dates.sort((a, b) => new Date(a) - new Date(b));
};
/**
 * Searches users for autocomplete
 * @param {string} queryString - Search query
 * @param {function} cb - Callback with results
 */
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
/**
 * Closes the modify booking dialog
 */
const handleCloseModifyDialog = () => {
  modifyDialogVisible.value = false;
};


/**
 * Saves modified booking
 */
const saveModifiedBooking = async () => {
  try {
    console.log(currentBooking.value);
    const payload = {
      ...currentBooking.value,
      time: currentBooking.value.time.sort(),
    };
    console.log(3);
    const response = await fetch(backendAddress + `/modifyBooking`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload),
    });

    const responseData = await response.json();

    if (responseData.code !== '001') {
      throw new Error(responseData.message);
    }

    ElMessage.success('Booking updated successfully');
    modifyDialogVisible.value = false;
    fetchBookings();
  } catch (error) {
    console.error('Error updating booking:', error);
    ElMessage.error(error.message || 'Failed to update booking');
  }
};
/**
 * Handles user selection from autocomplete
 * @param {Object} selected - Selected user
 */
const handleUserSelect = (selected) => {
  filters.value.userInput = selected.value.split(' (')[0];
};
/**
 * Opens modify dialog for a booking
 * @param {number} booking_id - Booking ID
 * @param {Object} newbooking - Booking data
 */
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
/**
 * Handles date selection changes in the booking modification form
 */
const handleDateChange = (date) => {
  console.log('Selected Date:', date);
  console.log('Current Booking Date:', currentBooking.value.date);
};
/**
 * Initiates booking cancellation
 * @param {number} booking_id - Booking ID
 */
const cancelBooking = async (booking_id) => {
  cancelForm.value = {
    booking_id: booking_id,
    reason: ''
  };
  cancelDialogVisible.value = true;
};
/**
 * Confirms booking cancellation
 */
const confirmCancelBooking = async () => {
  try {
    const response = await fetch(backendAddress + `/bookings/${cancelForm.value.booking_id}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        status: 'Declined',
        cancel_reason: cancelForm.value.reason
      })
    });
    console.log(cancelForm.value.reason)
    if (!response.ok) throw new Error('Failed to cancel booking');

    ElMessage.success('Booking canceled successfully');
    cancelDialogVisible.value = false;
    fetchBookings(); // Refresh data
  } catch (error) {
    console.error('Error canceling booking:', error);
    ElMessage.error(error.message || 'Failed to cancel booking');
  }
};
/**
 * Approves a pending booking
 * @param {number} booking_id - Booking ID
 */
const approveBooking = async (booking_id) => {
  try {
    const response = await fetch(backendAddress + `/bookings/${booking_id}`, {
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

/**
 * Initiates booking rejection
 * @param {number} booking_id - Booking ID
 */
const rejectBooking = async (booking_id) => {
  rejectForm.value = {
    booking_id: booking_id,
    reason: ''
  };
  rejectDialogVisible.value = true;
};
/**
 * Confirms booking rejection
 */
const confirmRejectBooking = async () => {
  try {
    const response = await fetch(backendAddress + `/bookings/${rejectForm.value.booking_id}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        status: 'Declined',
        cancel_reason: rejectForm.value.reason
      })
    });

    if (!response.ok) throw new Error('Failed to reject booking');

    ElMessage.success('Booking rejected successfully');
    rejectDialogVisible.value = false;
    fetchBookings(); // Refresh data
  } catch (error) {
    console.error('Error rejecting booking:', error);
    ElMessage.error(error.message || 'Failed to reject booking');
  }
};

/**
 * Deletes a completed booking
 * @param {number} booking_id - Booking ID
 */
const deleteBooking = async (booking_id) => {
  try {
    const response = await fetch(backendAddress + `/bookings/${booking_id}`, {
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


/**
 * Component mounted lifecycle hook
 * - Fetches current user information
 * - Initializes booking, room, and user data
 * - Sets the current user's email for form submissions
 */
onMounted(async () => {
  let me = await instance.appContext.config.globalProperties.$me()
  let user = me.data
  userEmail.value = user.email
  console.log(userEmail.value)
  await fetchBookings();
  await fetchRooms();
  await fetchUsers();
});

/**
 * Converts timestamp to readable time format
 * @param {number} timestamp - Unix timestamp
 * @returns {string} Formatted time string
 */
const timestampToTime = (timestamp) => {
  const timestampInSeconds = timestamp / 1000;
  const time = new Date(timestampInSeconds * 1000);

  const chinaOffset = 8 * 60 * 60 * 1000;
  const chinaTime = new Date(time.getTime() + chinaOffset);

  return chinaTime.toISOString().replace('T', ' ').slice(0, 19);
};

/**
 * Gets room name by ID
 * @param {number} room_id - Room ID
 * @returns {string} Room name
 */
const getRoomName = (room_id) => {
  const room = rooms.value.find(r => r.room_id === room_id);
  return room ? room.name : 'Unknown Room';
};

/**
 * Maps status to processing state
 * @param {string} status - Booking status
 * @returns {string} Processing state
 */
const getProcessingState = (status) => {
  const processingStateMap = {
    'Pending': 'unprocessed',
    'Confirmed': 'processed',
    'Declined': 'completed',
    'Completed': 'completed',
    'Missed': 'completed',
    'Banned': 'completed'
  };
  return processingStateMap[status] || 'unknown';
};

/**
 * Gets unique values for a given booking property
 * @param {string} key - Property name
 * @returns {Array} Unique values
 */
const uniqueValues = (key) => [...new Set(bookings.value.map((item) => item[key]))];

/**
 * Converts time string to human-readable slots
 * @param {string} timeStr - Comma-separated time indexes
 * @returns {string} Formatted time slots
 */
const convertTimeStrToTimeSlots = (timeStr) => {
  return timeStr.split(',')
      .map(Number)
      .map(index => reverseTimeSlotMap[index])
      .join('  ');
};
/**
 * Fetches all bookings from backend
 */
const fetchBookings = async () => {
  try {
    const response = await fetch(backendAddress + '/bookings');
    if (!response.ok) throw new Error('Failed to fetch bookings');
    const booking = await response.json();
    const data = booking.data;
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
/**
 * Formats date string to localized format
 * @param {string} dateString - Date string to format
 * @returns {string} Formatted date
 */
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-CA');
};
/**
 * Computes filtered bookings based on current filters
 * @returns {Array} Filtered booking records
 */
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
// Limit Usage Time Dialog
const limitUsageDialogVisible = ref(false);
const limitUsageForm = ref({
      room_id: '',
      date: '',
      time: [],
      user_email: '',
      purpose: ''
    })
;
/**
 * Opens time limit dialog
 */
const openLimitUsageDialog = () => {
  limitUsageDialogVisible.value = true;
};

const handleCloseLimitUsageDialog = () => {
  limitUsageDialogVisible.value = false;
};

/**
 * Disables dates before today in date picker
 * @param {Date} time - Date to check
 * @returns {boolean} True if date should be disabled
 */
const disabledDate = (time) => {
  return time.getTime() < Date.now() - 8.64e7;
}
/**
 * Submits time limit restrictions
 */
const submitLimitUsage = async () => {
  try {
    limitUsageForm.value.user_email = userEmail.value
    const payload = {
      ...limitUsageForm.value,
    };
    console.log('p='+payload);
    const response = await fetch(backendAddress + '/ban', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload),
    });

    if (!response.ok) throw new Error('Failed to limit usage time');

    const result = await response.json();

    if (result.code === '200') {
      ElMessage.success(`Prohibited time slots are set successfully, affecting ${result.data.conflict_count} reservation`);
      await fetchBookings();
      limitUsageDialogVisible.value = false;
    } else {
      ElMessage.error(result.message);
    }
  } catch (error) {
    console.error('Error limiting usage time:', error);
    ElMessage.error('Failed to limit usage time');
  }
};
</script>

<style scoped>
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2%;
    width: 100%;
}

.page-title {
    font-size: 40px;
    font-weight: bold;
    padding: 10px;
    margin: 0;
}

.button-group {
    display: flex;
    gap: 30px;
}

.new-button, .export-button {
    width: 30px;
    min-width: 10%;
    height: 50%;
    padding: 10px;
    margin: 0;
}

.el-button.el-button--success.export-button{
  width: 100%;
  margin-top: 10%;
  height: 43px;
}

.el-button.el-button--primary.new-button{
  width: 120%;
  margin-top: 10%;
  height: 43px;
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
}

.custom-card {
  width: 100%;
  padding: 20px;
  border-radius: 12px;
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

.el-table-column {
  width: 5%;
}

.el-dialog__footer {
    box-sizing: border-box;
    padding-top: var(--el-dialog-padding-primary);
    text-align: center;
}

</style>

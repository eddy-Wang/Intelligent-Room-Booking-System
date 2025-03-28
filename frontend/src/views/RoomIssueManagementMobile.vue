<!--
RoomIssueManagementMobile.vue - Mobile-optimized component for managing room repair issues.

This component provides:
- Mobile-friendly interface for viewing and managing room issues
- Filtering capabilities by room and status
- Report submission form with validation
- Status-based actions (approve, reject, complete, delete)
- Responsive card-based layout optimized for mobile devices

Props: None
Events: None
Dependencies: Element Plus UI components
-->
<template>
  <div class="room-issue-management-container">
    <!-- Title section -->
    <div class="title-container">
      <h1><strong>DRBS</strong></h1>
      <h2><strong>Room Issue Management</strong></h2>
    </div>
    <!-- New Issue button -->
    <button @click="showReportDialog" class="new-issue-button">New Issue</button>
    <!-- Filter controls -->
    <div class="filter-controls">
      <el-select
          v-model="filters.room_id"
          multiple
          collapse-tags
          clearable
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
          clearable
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
    <!-- Report Issue Modal Dialog -->
    <div v-if="dialogVisible" class="modal" @click.self="dialogVisible = false">
      <div class="modal-content">
        <h2>Report Issue</h2>
        <form @submit.prevent="submitNewReport">
          <label for="issue-room">Room:</label>
          <select id="issue-room" v-model="newReportForm.room_id" required>
            <option value="" disabled>Select Room</option>
            <option
                v-for="room in rooms"
                :key="room.room_id"
                :value="room.room_id"
            >
              {{ room.name }}
            </option>
          </select>
          <!-- User email input -->
          <label for="issue-email">Your Email:</label>
          <input
              type="email"
              id="issue-email"
              v-model="newReportForm.user_email"
              placeholder="email@example.com"
              required
          />
          <!-- Issue details textarea -->
          <label for="issue-details">Issue Details:</label>
          <textarea
              id="issue-details"
              v-model="newReportForm.reportInfo"
              placeholder="Describe the problem..."
              rows="4"
          ></textarea>
          <!-- Form actions -->
          <div class="room-actions">
            <button type="submit" class="action-button">Submit</button>
            <button type="button" class="action-button" @click="dialogVisible = false">Cancel</button>
          </div>
        </form>
      </div>
    </div>
    <!-- Issues list -->
    <div class="issues-list">
      <!-- Issue card for each report -->
      <div
          v-for="report in filteredReports"
          :key="report.timestamp"
          class="issue-card"
          :class="statusClass(report.reviewed)"
      >
        <!-- Card header with room name and status -->
        <div class="card-header">
          <span class="room-name">{{ getRoomName(report.room_id) }}</span>
          <el-tag class="booking-status-tag" :data-status="report.reviewed" size="small">
            {{ report.reviewed }}
          </el-tag>
        </div>
        <!-- Card content with issue details -->
        <div class="card-content">
          <p class="issue-description">{{ report.reportInfo }}</p>
          <p class="user-email">{{ report.user_email }}</p>
        </div>
        <!-- Card actions based on status -->
        <div class="card-actions">
          <template v-if="report.reviewed === 'Unreviewed'">
            <el-button size="small" @click="approveReport(report)" round>
              Approve
            </el-button>
            <el-button size="small" @click="rejectReport(report)" round>
              Reject
            </el-button>
          </template>
          <!-- Approved: Show Complete button -->
          <el-button
              v-if="report.reviewed === 'Approved'"
              size="small"
              @click="completeReport(report)"
              round
          >
            Complete
          </el-button>
          <!-- Rejected or Completed: Show Delete button -->
          <el-button
              v-if="['Rejected', 'Completed'].includes(report.reviewed)"
              size="small"
              @click="deleteReport(report)"
              round
          >
            Delete
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, getCurrentInstance, watch, onBeforeUnmount } from 'vue'
import { ElMessage } from 'element-plus'

// Initialize backend address from global properties
const instance = getCurrentInstance()
const backendAddress = instance.appContext.config.globalProperties.$backendAddress

// Reactive state
const reports = ref([])          // List of all issue reports
const rooms = ref([])            // List of all rooms
const filters = ref({            // Current filter values
  room_id: [],                   // Selected room IDs
  status: []                     // Selected statuses
})
const dialogVisible = ref(false) // Controls report dialog visibility
const newReportForm = ref({      // Form data for new reports
  room_id: '',                   // Selected room ID
  user_email: '',                // Reporter email
  reportInfo: ''                 // Issue description
})
const statusOptions = ['Unreviewed', 'Approved', 'Rejected', 'Completed']

// Data fetching
onMounted(async () => {
  await fetchRooms()
  await fetchReports()
})
/**
 * Fetches room list from backend
 * @async
 */
async function fetchRooms() {
  try {
    const response = await fetch(backendAddress + '/rooms_id_and_name')
    rooms.value = (await response.json()).data
  } catch (error) {
    ElMessage.error('Failed to load rooms')
  }
}

/**
 * Fetches issue reports from backend
 * @async
 */
async function fetchReports() {
  try {
    const response = await fetch(backendAddress + '/room_issue_reports')
    reports.value = (await response.json()).data || []
  } catch (error) {
    ElMessage.error('Failed to load reports')
  }
}

/**
 * Computed property for filtered reports based on current filters
 * @returns {Array} Filtered list of reports
 */
const filteredReports = computed(() => {
  return reports.value.filter(report => {
    const roomMatch =
      filters.value.room_id.length === 0 ||
      filters.value.room_id.includes(report.room_id)
    const statusMatch =
      filters.value.status.length === 0 ||
      filters.value.status.includes(report.reviewed)
    return roomMatch && statusMatch
  })
})

/**
 * Gets room name by room ID
 * @param {string} roomId - Room ID to look up
 * @returns {string} Room name or 'Unknown Room'
 */
function getRoomName(roomId) {
  return rooms.value.find(r => r.room_id === roomId)?.name || 'Unknown Room'
}
/**
 * Returns CSS class based on report status
 * @param {string} status - Report status
 * @returns {string} CSS class name
 */
function statusClass(status) {
  return `status-${status.toLowerCase()}`
}

/**
 * Updates report status in backend
 * @async
 * @param {Object} report - Report to update
 * @param {string} status - New status
 */
async function updateReportStatus(report, status) {
  try {
    await fetch(backendAddress + `/room_issue_reports/${report.timestamp}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ reviewed: status })
    })
    ElMessage.success(`Report ${status.toLowerCase()}`)
    await fetchReports()
  } catch (error) {
    ElMessage.error('Action failed')
  }
}
/**
 * Deletes a report from backend
 * @async
 * @param {Object} report - Report to delete
 */
async function deleteReport(report) {
  try {
    await fetch(backendAddress + `/room_issue_reports/${report.timestamp}`, {
      method: 'DELETE'
    })
    ElMessage.success('Report deleted')
    await fetchReports()
  } catch (error) {
    ElMessage.error('Deletion failed')
  }
}
/**
 * Submits a new report to backend
 * @async
 */
async function submitNewReport() {
  try {
    await fetch(backendAddress + '/room_issue_reports', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        ...newReportForm.value,
        timestamp: new Date().toISOString(),
        reviewed: 'Approved'
      })
    })
    ElMessage.success('Report submitted')
    dialogVisible.value = false
    await fetchReports()
  } catch (error) {
    ElMessage.error('Submission failed')
  }
}

// Action shortcuts
const approveReport = (report) => updateReportStatus(report, 'Approved')
const rejectReport = (report) => updateReportStatus(report, 'Rejected')
const completeReport = (report) => updateReportStatus(report, 'Completed')
/**
 * Shows the report dialog and resets form
 */
const showReportDialog = () => {
  newReportForm.value = { room_id: '', user_email: '', reportInfo: '' }
  dialogVisible.value = true
}

let scrollPosition = 0
// Manage scroll position when modal is open/closed
watch(dialogVisible, (newVal) => {
  if (newVal) {
    scrollPosition = window.pageYOffset || document.documentElement.scrollTop
    document.body.style.position = 'fixed'
    document.body.style.top = `-${scrollPosition}px`
    document.body.style.left = '0'
    document.body.style.right = '0'
  } else {
    document.body.style.position = ''
    document.body.style.top = ''
    document.body.style.left = ''
    document.body.style.right = ''
    window.scrollTo(0, scrollPosition)
  }
})
// Clean up scroll position on unmount
onBeforeUnmount(() => {
  document.body.style.position = ''
  document.body.style.top = ''
  document.body.style.left = ''
  document.body.style.right = ''
})
</script>


<style scoped>
/* Main container styling */
.room-issue-management-container {
  font-family: 'Cambria', serif;
  display: flex;
  flex-direction: column;
  background-color: #eceef8;
  width: 100%;
  height: 100vh;
  padding: 20px;
  overflow: auto;
}
/* Title section styling */
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
/* New Issue button styling */
.new-issue-button {
  margin: 20px 0 0 0;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: #3155ef;
  color: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}
/* Filter controls styling */
.filter-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 1rem 0;
  padding: 0.5rem;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.mobile-filter {
  flex: 1;
}
/* Issues list styling */
.issues-list {
  display: grid;
  gap: 1rem;
  margin-bottom: 50px;
}
/* Individual issue card styling */
.issue-card {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
/* Card header styling */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
}

.room-name {
  font-size: 1.1rem;
  font-weight: bold;
}

.booking-status-tag {
  font-size: 1rem;
  font-weight: bold;
}
/* Status-specific tag colors */
.booking-status-tag[data-status="Approved"] {
  background-color: #5ccb6a !important;
  border-color: #5ccb6a !important;
  color: #fff !important;
}

.booking-status-tag[data-status="Unreviewed"] {
  background-color: #b58d54 !important;
  border-color: #b58d54 !important;
  color: #fff !important;
}

.booking-status-tag[data-status="Rejected"] {
  background-color: #ff5757 !important;
  border-color: #ff5757 !important;
  color: #fff !important;
}

.booking-status-tag[data-status="Completed"] {
  background-color: #38b6ff !important;
  border-color: #38b6ff !important;
  color: #fff !important;
}
/* Card content styling */
.card-content {
  margin-bottom: 1rem;
}

.issue-description {
  color: #7f8c8d;
  margin: 0.5rem 0;
}

.user-email {
  color: #566c94;
  font-size: 0.9rem;
  margin: 0;
}
/* Card actions styling */
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
  background-color: #eceef8;
  border: none;
}
/* Status-based border colors */
.status-unreviewed {
  border-left: 4px solid #ffbd59;
}

.status-approved {
  border-left: 4px solid #5ccb6a;
}

.status-rejected {
  border-left: 4px solid #ff5757;
}

.status-completed {
  border-left: 4px solid #38b6ff;
}
/* Modal dialog styling */
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
/* Form styling */
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
/* Form actions styling */
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
/* Button transition effect */
.el-button {
  transition: all 0.2s ease;
}
</style>

<template>
  <div class="mobile-repair-container">
    <!-- Header Section -->
    <header class="app-header">
      <div class="app-title">
        <h1><strong>DRBS</strong></h1>
        <h2><strong>Room Issue Management</strong></h2>
      </div>
      <el-button
          class="new-issue-button"
          type="primary"
          @click="showReportDialog"
      >
        + New Issue
      </el-button>
    </header>

    <!-- New Issue Dialog -->
    <el-dialog
        v-model="dialogVisible"
        title="Report Issue"
        fullscreen
    >
      <el-form :model="newReportForm">
        <el-form-item label="Room">
          <el-select
              v-model="newReportForm.room_id"
              placeholder="Select Room"
              size="large"
          >
            <el-option
                v-for="room in rooms"
                :key="room.room_id"
                :label="room.name"
                :value="room.room_id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="Your Email">
          <el-input
              v-model="newReportForm.user_email"
              placeholder="email@example.com"
              type="email"
              size="large"
          />
        </el-form-item>

        <el-form-item label="Issue Details">
          <el-input
              v-model="newReportForm.reportInfo"
              type="textarea"
              placeholder="Describe the problem..."
              rows="4"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false" round>Cancel</el-button>
          <el-button type="primary" @click="submitNewReport" round>Submit</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- Issues List -->
    <div class="issues-list">
      <div
          v-for="report in filteredReports"
          :key="report.timestamp"
          class="issue-card"
          :class="statusClass(report.reviewed)"
      >
        <div class="card-header">
          <span class="room-name">{{ getRoomName(report.room_id) }}</span>
          <el-tag :type="statusTagType(report.reviewed)" size="small">
            {{ report.reviewed }}
          </el-tag>
        </div>

        <div class="card-content">
          <p class="issue-description">{{ report.reportInfo }}</p>
          <p class="user-email">{{ report.user_email }}</p>
        </div>

        <div class="card-actions">
          <template v-if="report.reviewed === 'Unreviewed'">
            <el-button size="small" @click="approveReport(report)" round>
              Approve
            </el-button>
            <el-button size="small" @click="rejectReport(report)" round>
              Reject
            </el-button>
          </template>

          <el-button
              v-if="report.reviewed === 'Approved'"
              size="small"
              @click="completeReport(report)"
              round
          >
            Complete
          </el-button>

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

    <!-- Filter Controls -->
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
  </div>
</template>

<script setup>
import {ref, computed, onMounted, getCurrentInstance} from 'vue'
import {ElMessage} from 'element-plus'

const instance = getCurrentInstance()
const backendAddress = instance.appContext.config.globalProperties.$backendAddress

// Reactive state
const reports = ref([])
const rooms = ref([])
const filters = ref({
  room_id: [],
  status: []
})
const dialogVisible = ref(false)
const newReportForm = ref({
  room_id: '',
  user_email: '',
  reportInfo: ''
})
const statusOptions = ['Unreviewed', 'Approved', 'Rejected', 'Completed']

// Data fetching
onMounted(async () => {
  await fetchRooms()
  await fetchReports()
})

async function fetchRooms() {
  try {
    const response = await fetch(backendAddress+'/rooms_id_and_name')
    rooms.value = (await response.json()).data
  } catch (error) {
    ElMessage.error('Failed to load rooms')
  }
}

async function fetchReports() {
  try {
    const response = await fetch(backendAddress+'/room_issue_reports')
    reports.value = (await response.json()).data || []
  } catch (error) {
    ElMessage.error('Failed to load reports')
  }
}

// Computed properties
const filteredReports = computed(() => {
  return reports.value.filter(report => {
    const roomMatch = filters.value.room_id.length === 0 ||
        filters.value.room_id.includes(report.room_id)
    const statusMatch = filters.value.status.length === 0 ||
        filters.value.status.includes(report.reviewed)
    return roomMatch && statusMatch
  })
})

// Helper methods
function getRoomName(roomId) {
  return rooms.value.find(r => r.room_id === roomId)?.name || 'Unknown Room'
}

function statusTagType(status) {
  const types = {
    Unreviewed: 'warning',
    Approved: 'success',
    Rejected: 'danger',
    Completed: 'info'
  }
  return types[status] || 'info'
}

function statusClass(status) {
  return `status-${status.toLowerCase()}`
}

// Report actions
async function updateReportStatus(report, status) {
  try {
    await fetch(backendAddress+`/room_issue_reports/${report.timestamp}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({reviewed: status})
    })
    ElMessage.success(`Report ${status.toLowerCase()}`)
    await fetchReports()
  } catch (error) {
    ElMessage.error('Action failed')
  }
}

async function deleteReport(report) {
  try {
    await fetch(backendAddress+`/room_issue_reports/${report.timestamp}`, {
      method: 'DELETE'
    })
    ElMessage.success('Report deleted')
    await fetchReports()
  } catch (error) {
    ElMessage.error('Deletion failed')
  }
}

async function submitNewReport() {
  try {
    await fetch(backendAddress+'/room_issue_reports', {
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
const showReportDialog = () => {
  newReportForm.value = {room_id: '', user_email: '', reportInfo: ''}
  dialogVisible.value = true
}
</script>

<style scoped>
.mobile-repair-container {
  padding: 1rem;
  max-width: 100%;
  min-height: 100vh;
  background: #f5f7fa;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.app-title {
  font-size: 1.5rem;
  color: #2c3e50;
  margin: 0;
}

.new-issue-button {
  font-size: 2rem;
  padding: 0.75rem 1.5rem;
  color: white;
  background: #3f63fd;
  height: 40px;
  width: 50%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-radius: 15px;
}

.issues-list {
  display: grid;
  gap: 1rem;
  margin-bottom: 100px;
}

.issue-card {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.room-name {
  font-weight: 600;
  color: #34495e;
}

.card-content {
  margin-bottom: 1rem;
}

.issue-description {
  color: #7f8c8d;
  margin: 0.5rem 0;
}

.user-email {
  color: #3498db;
  font-size: 0.9rem;
  margin: 0;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-controls {
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

.mobile-filter {
  flex: 1;
}

.status-unreviewed {
  border-left: 4px solid #e67e22;
}

.status-approved {
  border-left: 4px solid #2ecc71;
}

.status-rejected {
  border-left: 4px solid #e74c3c;
}

.status-completed {
  border-left: 4px solid #3498db;
}

.el-button {
  transition: all 0.2s ease;
}

.el-button:hover {
  transform: translateY(-1px);
}

@media (max-width: 480px) {
  .app-title {
    font-size: 1.2rem;
  }

  .new-issue-button {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
}
</style>
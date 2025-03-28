<!--
RoomIssueManagement.vue - Component for managing room repair reports.

This component provides:
- Interface for viewing and managing room repair reports
- Filtering capabilities for reports by room, user, and status
- Functionality to approve, reject, complete, and delete reports
- Export to Excel with additional analysis of frequent issues
- Form for submitting new repair reports

Props: None
Events: None
Dependencies: Element Plus UI components, xlsx library for Excel export
-->
<template>
  <div class="room-repair-handling">
    <!-- Header section with title and action buttons -->
      <div class="header">
          <h2 class="page-title">Room Repair Handling</h2>
          <div class="button-group">
              <el-button class="new-button" type="primary" @click="dialogVisible = true">Report New Issue</el-button>
              <el-button class="export-button" type="success" @click="exportToExcel">Export to Excel</el-button>
          </div>
      </div>
    <!-- Dialog for reporting new issues -->
    <el-dialog v-model="dialogVisible" title="Report New Issue" width="30%">
      <el-form :model="newReportForm" label-width="120px">
        <el-form-item label="Room Name">
          <el-select v-model="newReportForm.room_id" placeholder="Select Room">
            <el-option
                v-for="room in rooms"
                :key="room.room_id"
                :label="room.name"
                :value="room.room_id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="User Email">
          <el-input v-model="newReportForm.user_email" placeholder="Enter your email"/>
        </el-form-item>
        <el-form-item label="Report Info">
          <el-input
              v-model="newReportForm.reportInfo"
              type="textarea"
              placeholder="Describe the issue"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="submitNewReport">Submit</el-button>
      </template>
    </el-dialog>
    <!-- Main card containing reports table -->
    <el-card class="custom-card">
      <el-table :data="filteredReports" border stripe style="width: 100%" class="el-table">
        <!-- Room Name Column with filter -->
        <el-table-column class="el-table-column" label="Room Name">
          <template #header>
            <div class="filter-header">
              <span>Room Name</span>
              <el-select v-model="filters.room_id" multiple clearable placeholder="Filter">
                <el-option
                    v-for="room in rooms"
                    :key="room.room_id"
                    :label="room.name"
                    :value="room.room_id"
                />
              </el-select>
            </div>
          </template>
          <template #default="{ row }">
            {{ getRoomName(row.room_id) }}
          </template>
        </el-table-column>

        <!-- User Email Column -->
        <el-table-column class="el-table-column" label="User Email">
          <template #header>
            <div class="filter-header">
              <span>User Email</span>
              <el-autocomplete
                  v-model="filters.user_email"
                  :fetch-suggestions="queryUsers"
                  clearable
                  placeholder="Search by user email"
                  @select="handleUserSelect"
              />
            </div>
          </template>
          <template #default="{ row }">
            {{ row.user_email }}
          </template>
        </el-table-column>

        <!-- Report Info Column -->
        <el-table-column class="el-table-column" label="Report Info">
          <template #default="{ row }">
            {{ row.reportInfo }}
          </template>
        </el-table-column>

        <!-- Status Column -->
        <el-table-column class="el-table-column" label="Status">
          <template #header>
            <div class="filter-header">
              <span>Status</span>
              <el-select v-model="filters.status" multiple clearable placeholder="Filter">
                <el-option
                    v-for="status in statusOptions"
                    :key="status"
                    :label="status"
                    :value="status"
                />
              </el-select>
            </div>
          </template>
          <template #default="{ row }">
            {{ row.reviewed }}
          </template>
        </el-table-column>

        <!-- Actions Column -->
        <el-table-column class="el-table-column" label="Actions" width="250">
          <template #default="{ row }">
            <div class="action-buttons">
              <!-- Unreviewed: Show Approve and Reject buttons -->
              <el-button
                  v-if="row.reviewed === 'Unreviewed'"
                  size="small"
                  @click="approveReport(row)"
              >
                Approve
              </el-button>
              <el-button
                  v-if="row.reviewed === 'Unreviewed'"
                  size="small"
                  @click="rejectReport(row)"
              >
                Reject
              </el-button>

              <!-- Approved: Show Complete buttons -->
              <el-button
                  v-if="row.reviewed === 'Approved'"
                  size="small"
                  @click="completeReport(row)"
              >
                Complete
              </el-button>

              <!-- Rejected or Completed: Show Delete button -->
              <el-button
                  v-if="row.reviewed === 'Rejected' || row.reviewed === 'Completed'"
                  size="small"
                  @click="deleteReport(row)"
              >
                Delete
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import {ref, computed, onMounted, getCurrentInstance} from 'vue';
import {ElTable, ElTableColumn, ElSelect, ElOption, ElCard, ElButton, ElMessage, ElAutocomplete} from 'element-plus';
import 'element-plus/dist/index.css';
import * as XLSX from 'xlsx';
/**
 * Converts timestamp to formatted time string (China timezone)
 * @param {number} timestamp - Unix timestamp in milliseconds
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
 * Exports reports data to Excel with additional analysis
 */
const exportToExcel = () => {
    // Prepare main reports data for export
  const roomNameMap = {};
    rooms.value.forEach(room => {
        roomNameMap[room.room_id] = room.name;
    });
    const dataForExport = filteredReports.value.map(report => {
        return {
            'Room Name': getRoomName(report.room_id),
            'User Email': report.user_email,
            'Report Info': report.reportInfo,
            'Status': report.reviewed,
            'Report time': timestampToTime(report.timestamp)
        };
    });

    // Create worksheet for main reports
    const ws = XLSX.utils.json_to_sheet(dataForExport);

    // Calculate frequently reported rooms
    const roomIssueCounts = {};
    reports.value.forEach(report => {
        if (report.reviewed === 'Completed' || report.reviewed === 'Approved') {
            if (!roomIssueCounts[report.room_id]) {
                roomIssueCounts[report.room_id] = 0;
            }
            roomIssueCounts[report.room_id]++;
        }
    });

    // Filter rooms with 5+ issues and prepare data
    const frequentIssuesData = Object.entries(roomIssueCounts)
        .filter(([_, count]) => count >= 5)
        .map(([room_id, count]) => ({
            'Room Name': roomNameMap[room_id] || 'Unknown Room',
            'Issue Count': count
        }));
    // Create worksheet for frequent issues
    const frequentIssuesWs = XLSX.utils.json_to_sheet(frequentIssuesData);

    // Create workbook with both sheets
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Repair Reports");
    XLSX.utils.book_append_sheet(wb, frequentIssuesWs, "Frequent Issues Rooms");
    // Generate filename with current date
    const dateStr = new Date().toISOString().slice(0, 10);
    const fileName = `Repair_Reports_${dateStr}.xlsx`;
    // Trigger download
    XLSX.writeFile(wb, fileName);
};
// Initialize backend address
const instance = getCurrentInstance()
const backendAddress = instance.appContext.config.globalProperties.$backendAddress

// Reactive data
const reports = ref([]);          // List of all repair reports
const rooms = ref([]);            // List of all rooms
const users = ref([]);            // List of all users
const filters = ref({             // Current filter values
  room_id: [],                    // Selected room IDs
  user_email: '',                 // Filter by user email
  status: [],                     // Selected statuses
});
const dialogVisible = ref(false); // Controls new report dialog visibility
const newReportForm = ref({       // Form data for new reports
  room_id: '',                    // Selected room ID
  user_email: '',                 // Reporter email
  reportInfo: '',                 // Report description
});

// Status options
const statusOptions = ['Unreviewed', 'Approved', 'Rejected', 'Completed'];

/**
 * Fetches room list from backend
 * @async
 */
const fetchRooms = async () => {
  try {
    const response = await fetch(backendAddress+'/rooms_id_and_name');
    if (!response.ok) throw new Error('Failed to fetch rooms');
    const data = await response.json();
    rooms.value = data.data;
  } catch (error) {
    console.error('Error fetching rooms:', error);
  }
};

/**
 * Fetches user list from backend
 * @async
 */
const fetchUsers = async () => {
  try {
    const response = await fetch(backendAddress+'/users');
    if (!response.ok) throw new Error('Failed to fetch users');
    const data = await response.json();
    users.value = data.data;
  } catch (error) {
    console.error('Error fetching users:', error);
  }
};

/**
 * Fetches repair reports from backend
 * @async
 */
const fetchReports = async () => {
  try {
    const response = await fetch(backendAddress+'/room_issue_reports');
    if (!response.ok) throw new Error('Failed to fetch reports');
    const data = await response.json();
    console.log('Fetched reports:', data);
    reports.value = Array.isArray(data.data) ? data.data : [];
  } catch (error) {
    console.error('Error fetching reports:', error);
    reports.value = [];
  }
};

/**
 * Gets room name by room ID
 * @param {string} room_id - Room ID to look up
 * @returns {string} Room name or 'Unknown Room'
 */
const getRoomName = (room_id) => {
  const room = rooms.value.find((r) => r.room_id === room_id);
  return room ? room.name : 'Unknown Room';
};

/**
 * Handles user selection in autocomplete
 * @param {Object} selected - Selected user object
 */
const handleUserSelect = (selected) => {
  filters.value.user_email = selected.value.split(' ')[0];
};

/**
 * Provides autocomplete suggestions for user email filter
 * @param {string} queryString - Current search query
 * @param {function} cb - Callback to return results
 */
const queryUsers = (queryString, cb) => {
  const results = users.value
      .filter((user) => user.email.toLowerCase().includes(queryString.toLowerCase()))
      .map((user) => ({value: user.email, label: user.email}));
  cb(results);
};

/**
 * Computed property for filtered reports based on current filters
 * @returns {Array} Filtered list of reports
 */
const filteredReports = computed(() => {
  return reports.value.filter((report) => {
    return (
        (filters.value.room_id.length === 0 || filters.value.room_id.includes(report.room_id)) &&
        (filters.value.user_email === '' || report.user_email.includes(filters.value.user_email)) &&
        (filters.value.status.length === 0 || filters.value.status.includes(report.reviewed))
    );
  });
});

/**
 * Approves a repair report
 * @async
 * @param {Object} report - Report to approve
 */
const approveReport = async (report) => {
  try {
    const response = await fetch(backendAddress+`/room_issue_reports/${report.timestamp}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({reviewed: 'Approved'}),
    });
    if (!response.ok) throw new Error('Failed to approve report');
    ElMessage.success('Report approved successfully');
    fetchReports();
  } catch (error) {
    console.error('Error approving report:', error);
    ElMessage.error('Failed to approve report');
  }
};

/**
 * Rejects a repair report
 * @async
 * @param {Object} report - Report to reject
 */
const rejectReport = async (report) => {
  try {
    const response = await fetch(backendAddress+`/room_issue_reports/${report.timestamp}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({reviewed: 'Rejected'}),
    });
    if (!response.ok) throw new Error('Failed to reject report');
    ElMessage.success('Report rejected successfully');
    fetchReports();
  } catch (error) {
    console.error('Error rejecting report:', error);
    ElMessage.error('Failed to reject report');
  }
};


/**
 * Marks a report as completed
 * @async
 * @param {Object} report - Report to complete
 */
const completeReport = async (report) => {
  try {
    const response = await fetch(backendAddress+`/room_issue_reports/${report.timestamp}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({reviewed: 'Completed'}),
    });
    if (!response.ok) throw new Error('Failed to complete report');
    ElMessage.success('Report completed successfully');
    fetchReports();
  } catch (error) {
    console.error('Error completing report:', error);
    ElMessage.error('Failed to complete report');
  }
};

/**
 * Deletes a report
 * @async
 * @param {Object} report - Report to delete
 */
const deleteReport = async (report) => {
  try {
    const response = await fetch(backendAddress+`/room_issue_reports/${report.timestamp}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete report');
    ElMessage.success('Report deleted successfully');
    fetchReports();
  } catch (error) {
    console.error('Error deleting report:', error);
    ElMessage.error('Failed to delete report');
  }
};

/**
 * Submits a new repair report
 * @async
 */
const submitNewReport = async () => {
  try {
    const response = await fetch(backendAddress+'/room_issue_reports', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        timestamp: new Date().toISOString(),
        room_id: newReportForm.value.room_id,
        user_email: newReportForm.value.user_email,
        reportInfo: newReportForm.value.reportInfo,
        reviewed: 'Approved',
      }),
    });
    if (!response.ok) throw new Error('Failed to submit report');
    ElMessage.success('Report submitted successfully');
    dialogVisible.value = false;
    fetchReports();
  } catch (error) {
    console.error('Error submitting report:', error);
    ElMessage.error('Failed to submit report');
  }
};

// Fetch data on component mount
onMounted(() => {
  fetchRooms();
  fetchUsers();
  fetchReports();
});
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1%;
  width: 100%;
}

.page-title {
  font-size: 40px;
  font-weight: bold;
  margin-bottom: 20px;
  padding: 10px;
}
/* Button group styling */
.button-group {
    display: flex;
    gap: 30px;
}
/* Export button styling */
.export-button {
    width: 100%;
    background-color: #28a745;
    color: white;
}

.export-button:hover {
    background-color: #218838;
}
/* New report button styling */
.new-button {
    min-width: 10%;
    height: 50%;
    padding: 10px;
    margin: 0;
}

.export-button {
    min-width: 10%;
    height: 50%;
    padding: 10px;
    margin: 0;
}
/* Specific button overrides */
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
/* Table styling */
.el-table {
  height: 700px;
  width: 100%;
  overflow: auto;
}

/* Main container styling */
.room-repair-handling {
  font-family: 'Cambria', serif;
  width: 100%;
  height: 100%;
  padding: 20px;
  background-color: #f8f9fa;
}

/* Card styling */
.custom-card {
  width: 100%;
  padding: 20px;
  border-radius: 12px;
  overflow: auto;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* Filter header styling */
.filter-header {
  height: 100%;
  width: 100%;
  display: flow-root;
  justify-content: space-between;
  align-items: center;
}
/* Action buttons styling */
.action-buttons {
  align-items: flex-start;
}
/* Button styling */
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
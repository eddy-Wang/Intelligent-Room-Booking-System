<template>
    <div class="room-repair-handling">
        <h2 class="page-title">Room Repair Handling</h2>
        <el-card class="custom-card">
            <el-table :data="filteredReports" border stripe style="width: 100%" class="el-table">
                <!-- Room Name Column -->
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
                            <!-- Pending: Show Approve and Reject buttons -->
                            <el-button
                                    v-if="row.reviewed === 'Pending'"
                                    size="small"
                                    @click="approveReport(row)"
                            >
                                Approve
                            </el-button>
                            <el-button
                                    v-if="row.reviewed === 'Pending'"
                                    size="small"
                                    @click="rejectReport(row)"
                            >
                                Reject
                            </el-button>

                            <!-- Approved: Show Complete and Modify buttons -->
                            <el-button
                                    v-if="row.reviewed === 'Approved'"
                                    size="small"
                                    @click="completeReport(row)"
                            >
                                Complete
                            </el-button>
                            <el-button
                                    v-if="row.reviewed === 'Approved'"
                                    size="small"
                                    @click="modifyReport(row)"
                            >
                                Modify
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
import { ref, computed, onMounted } from 'vue';
import { ElTable, ElTableColumn, ElSelect, ElOption, ElCard, ElButton, ElMessage, ElAutocomplete } from 'element-plus';
import 'element-plus/dist/index.css';

// Define reactive data
const reports = ref([]);
const rooms = ref([]);
const users = ref([]);
const filters = ref({
    room_id: [],
    user_email: '',
    status: [],
});

// Status options
const statusOptions = ['Pending', 'Approved', 'Rejected', 'Completed'];

// Fetch rooms from backend API
const fetchRooms = async () => {
    try {
        const response = await fetch('http://192.168.110.54:8080/rooms');
        if (!response.ok) throw new Error('Failed to fetch rooms');
        const data = await response.json();
        rooms.value = data.data;
    } catch (error) {
        console.error('Error fetching rooms:', error);
    }
};

// Fetch users from backend API
const fetchUsers = async () => {
    try {
        const response = await fetch('http://192.168.110.54:8080/users');
        if (!response.ok) throw new Error('Failed to fetch users');
        const data = await response.json();
        users.value = data.data;
    } catch (error) {
        console.error('Error fetching users:', error);
    }
};

// Fetch reports from backend API
const fetchReports = async () => {
    try {
        const response = await fetch('http://192.168.110.54:8080/room_issue_reports');
        if (!response.ok) throw new Error('Failed to fetch reports');
        const data = await response.json();
        reports.value = data.data;
    } catch (error) {
        console.error('Error fetching reports:', error);
    }
};

// Get room name by room_id
const getRoomName = (room_id) => {
    const room = rooms.value.find((r) => r.room_id === room_id);
    return room ? room.name : 'Unknown Room';
};

// Handle user selection in autocomplete
const handleUserSelect = (selected) => {
    filters.value.user_email = selected.value.split(' ')[0];
};

// Query users for autocomplete
const queryUsers = (queryString, cb) => {
    const results = users.value
        .filter((user) => user.email.toLowerCase().includes(queryString.toLowerCase()))
        .map((user) => ({ value: user.email, label: user.email }));
    cb(results);
};

// Filtered reports based on filters
const filteredReports = computed(() => {
    return reports.value.filter((report) => {
        return (
            (filters.value.room_id.length === 0 || filters.value.room_id.includes(report.room_id)) &&
            (filters.value.user_email === '' || report.user_email.includes(filters.value.user_email)) &&
            (filters.value.status.length === 0 || filters.value.status.includes(report.reviewed))
        );
    });
});

// Approve report
const approveReport = async (report) => {
    try {
        const response = await fetch(`http://192.168.110.54:8080/room_issue_reports/${report.timestamp}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reviewed: 'Approved' }),
        });
        if (!response.ok) throw new Error('Failed to approve report');
        ElMessage.success('Report approved successfully');
        fetchReports();
    } catch (error) {
        console.error('Error approving report:', error);
        ElMessage.error('Failed to approve report');
    }
};

// Reject report
const rejectReport = async (report) => {
    try {
        const response = await fetch(`http://192.168.110.54:8080/room_issue_reports/${report.timestamp}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reviewed: 'Rejected' }),
        });
        if (!response.ok) throw new Error('Failed to reject report');
        ElMessage.success('Report rejected successfully');
        fetchReports();
    } catch (error) {
        console.error('Error rejecting report:', error);
        ElMessage.error('Failed to reject report');
    }
};

// Complete report
const completeReport = async (report) => {
    try {
        const response = await fetch(`http://192.168.110.54:8080/room_issue_reports/${report.timestamp}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reviewed: 'Completed' }),
        });
        if (!response.ok) throw new Error('Failed to complete report');
        ElMessage.success('Report completed successfully');
        fetchReports();
    } catch (error) {
        console.error('Error completing report:', error);
        ElMessage.error('Failed to complete report');
    }
};

// Delete report
const deleteReport = async (report) => {
    try {
        const response = await fetch(`http://192.168.110.54:8080/room_issue_reports/${report.timestamp}`, {
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

// Fetch data on component mount
onMounted(() => {
    fetchRooms();
    fetchUsers();
    fetchReports();
});
</script>

<style>
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

.room-repair-handling {
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
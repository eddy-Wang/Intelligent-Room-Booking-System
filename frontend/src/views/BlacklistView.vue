<template>
  <div class="room-repair-handling">
    <div class="header">
      <h2 class="page-title">User Black List</h2>
    </div>

    <el-card class="custom-card">
      <el-table :data="filteredUsers" border stripe style="width: 100%" class="el-table">
        <!-- User Email Column -->
        <el-table-column class="el-table-column" label="User Email">
          <template #header>
            <div class="filter-header">
              <span>User Email</span>
              <el-autocomplete
                  v-model="filters.user_email"
                  :fetch-suggestions="queryUsers"
                  clearable
                  placeholder="Search by email"
              />
            </div>
          </template>
          <template #default="{ row }">
            {{ row.user_email }}
          </template>
        </el-table-column>

        <!-- User Name Column -->
        <el-table-column class="el-table-column" label="User Name">
          <template #header>
            <div class="filter-header">
              <span>User Name</span>
              <el-autocomplete
                  v-model="filters.user_name"
                  :fetch-suggestions="queryUserNames"
                  clearable
                  placeholder="Search by name"
              />
            </div>
          </template>
          <template #default="{ row }">
            {{ row.user_name }}
          </template>
        </el-table-column>

        <!-- Violation Count Column -->
        <el-table-column class="el-table-column" label="remarks" prop="violation_count" sortable>
          <template #header>
            <div class="filter-header">
              <span class="header-label">Remarks</span>
              <el-select v-model="filters.violation_count" placeholder="Filter" clearable>
                <el-option label="≥3" value="3"/>
                <el-option label="≥5" value="5"/>
                <el-option label="≥10" value="10"/>
              </el-select>
            </div>
          </template>
        </el-table-column>

        <!-- Ban Start Time -->
        <el-table-column class="el-table-column" label="Ban Start Date" prop="ban_start" sortable/>

        <!-- Ban End Time -->
        <el-table-column class="el-table-column" label="Ban End Date" prop="ban_end" sortable/>

        <!-- Actions Column -->
        <el-table-column class="el-table-column" label="Actions" width="180">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button
                  size="small"
                  @click="handleUnban(row)"
              >
                Release
              </el-button>
              <el-button
                  size="small"
                  type="danger"
                  @click="handleDelete(row)"
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
import {ref, computed} from 'vue';

//TODO:static data for test
const testUsers = ref([
  {
    user_email: 'user1@example.com',
    user_name: 'AAA',
    violation_count: 3,
    ban_start: '2024-03-01',
    ban_end: '2024-06-01'
  },
  {
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  },
  {
    user_email: 'user3@example.com',
    user_name: 'CCC',
    violation_count: 2,
    ban_start: '2024-04-01',
    ban_end: '2024-07-01'
  },
  {
    user_email: 'tech@example.com',
    user_name: 'DDD',
    violation_count: 7,
    ban_start: '2024-01-10',
    ban_end: '2024-04-10'
  },
  {
    user_email: 'support@example.com',
    user_name: 'EEE',
    violation_count: 4,
    ban_start: '2024-03-20',
    ban_end: '2024-06-20'
  },
  {
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  }, {
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  }, {
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  }, {
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  }, {
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  }, {
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  }, {
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  },{
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  },{
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  },{
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  },{
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  },{
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  },{
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  },{
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  },{
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  },{
    user_email: 'user2@example.com',
    user_name: 'BBB',
    violation_count: 5,
    ban_start: '2024-02-15',
    ban_end: '2024-05-15'
  },

]);

const filters = ref({
  user_email: '',
  user_name: '',
  violation_count: null
});


const filteredUsers = computed(() => {
  return testUsers.value.filter(user => {
    const emailMatch = user.user_email.toLowerCase().includes(filters.value.user_email.toLowerCase());
    const nameMatch = user.user_name.toLowerCase().includes(filters.value.user_name.toLowerCase());
    const countMatch = !filters.value.violation_count ||
        user.violation_count >= parseInt(filters.value.violation_count);

    return emailMatch && nameMatch && countMatch;
  });
});


const queryUsers = (queryString, cb) => {
  const results = testUsers.value
      .filter(user => user.user_email.toLowerCase().includes(queryString.toLowerCase()))
      .map(user => ({value: user.user_email}));
  cb(results);
};

const queryUserNames = (queryString, cb) => {
  const results = testUsers.value
      .filter(user => user.user_name.toLowerCase().includes(queryString.toLowerCase()))
      .map(user => ({value: user.user_name}));
  cb(results);
};


const handleUnban = (row) => {
  console.log('Unban user:', row);
};

const handleDelete = (row) => {
  console.log('Delete record:', row);
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

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
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-label {
  white-space: nowrap;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.header-content {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
}


.el-table .caret-wrapper {
  display: inline-flex;
  align-items: center;
  height: auto;
}

.el-table .sort-caret {
  position: static;
  margin-left: 4px;
}

.el-table-column {
  width: auto;
  min-width: 120px;
}
</style>
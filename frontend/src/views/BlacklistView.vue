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
        <el-table-column class="el-table-column" label="Missed Time" prop="missed_time" sortable>
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
                  @click="handleRelease(row)"
              >
                Release
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import {getCurrentInstance} from 'vue'

export default {
  name: 'BlacklistView',
  setup() {
    const instance = getCurrentInstance()
    const backendAddress = instance.appContext.config.globalProperties.$backendAddress
    return {backendAddress}
  },
  data() {
    return {
      users: [],
      filters: {
        user_email: '',
        user_name: '',
      },
      loading: false,
      error: null
    }
  },
  computed: {
    filteredUsers() {
      return this.users.filter(user => {
        const emailMatch = user.user_email.toLowerCase().includes(this.filters.user_email.toLowerCase())
        const nameMatch = user.user_name.toLowerCase().includes(this.filters.user_name.toLowerCase())
        return emailMatch && nameMatch
      })
    }
  },
  methods: {
    convertTime(gmtTimeString, addDays = 0) {
      if (!gmtTimeString) return '';

      const gmtDate = new Date(gmtTimeString);
      if (isNaN(gmtDate.getTime())) {
        console.error('invalid date :', gmtTimeString);
        return 'invalid date';
      }

      // Add days if specified
      if (addDays > 0) {
        gmtDate.setDate(gmtDate.getDate() + addDays);
      }

      return new Intl.DateTimeFormat('zh-CN', {
        timeZone: 'Asia/Shanghai',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false,
      }).format(gmtDate);
    },


    async fetchBadUsers() {
      this.loading = true
      try {
        const resp = await fetch(`${this.backendAddress}/bad_users`)
        const result = await resp.json()
        if (result.code === '000') {
          this.users = (result.data || []).map(row => ({
            user_email: row.user_email || '',
            user_name: row.user_name || '',
            missed_time: row.missed_time ?? 0,
            ban_start: this.convertTime(row.added_at) || '',
            ban_end: this.convertTime(row.added_at, 30) || '' // Add 30 days here
          }))
        } else {
          throw new Error(result.message || 'Unknown error')
        }
      } catch (err) {
        this.error = err.message
        console.error('Fetch bad users error:', err)
      } finally {
        this.loading = false
      }
    },
    queryUsers(queryString, cb) {
      const results = this.users
          .filter(u => u.user_email.toLowerCase().includes(queryString.toLowerCase()))
          .map(u => ({value: u.user_email}))
      cb(results)
    },
    queryUserNames(queryString, cb) {
      const results = this.users
          .filter(u => u.user_name.toLowerCase().includes(queryString.toLowerCase()))
          .map(u => ({value: u.user_name}))
      cb(results)
    },
    async handleRelease(row) {
      try {
        // Confirm with the user before releasing
        const confirmResult = await this.$confirm(
            `Are you sure you want to release ${row.user_email} from the blacklist?`,
            'Confirm Release',
            {
              confirmButtonText: 'Release',
              cancelButtonText: 'Cancel',
              type: 'warning'
            }
        ).catch(() => {
          // User clicked cancel
          return false;
        });

        if (!confirmResult) return;

        // Show loading
        const loadingInstance = this.$loading({
          lock: true,
          text: 'Releasing user...',
          background: 'rgba(0, 0, 0, 0.7)'
        });

        // Call the API
        const response = await fetch(
            `${this.backendAddress}/reset_missed_times/${encodeURIComponent(row.user_email)}`,
            {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json'
              }
            }
        );

        const result = await response.json();

        if (result.code === '000') {
          this.$message({
            message: 'User released successfully!',
            type: 'success'
          });
          // Refresh the list
          await this.fetchBadUsers();
        } else {
          throw new Error(result.message || 'Failed to release user');
        }
      } catch (error) {
        this.$message({
          message: error.message || 'An error occurred while releasing the user',
          type: 'error'
        });
        console.error('Release error:', error);
      } finally {
        // Hide loading
        this.$loading().close();
      }
    }
  },
  mounted() {
    this.fetchBadUsers()
  }
}
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
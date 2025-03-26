<template>
  <div class="blacklist-management-mobile-container">
    <div class="title-container">
      <h1><strong>DRBS</strong></h1>
      <h2><strong>User Blacklist Management</strong></h2>
    </div>
    <div class="filter-controls">
      <el-autocomplete
          v-model="filters.user_email"
          :fetch-suggestions="queryUsers"
          clearable
          placeholder="Search by email"
          class="mobile-filter"
      />
      <el-autocomplete
          v-model="filters.user_name"
          :fetch-suggestions="queryUserNames"
          clearable
          placeholder="Search by name"
          class="mobile-filter"
      />
    </div>
    <div class="user-list">
      <div
          v-for="(user, index) in filteredUsers"
          :key="index"
          class="user-card"
      >
        <div class="card-header">
          <div class="user-info">
            <div class="user-name">{{ user.user_name }}</div>
            <div class="user-email">{{ user.user_email }}</div>
          </div>
        </div>
        <div class="card-content">
          <div class="card-body">
            <div class="info-row">
              <span class="label">Missed Time: </span>
              <span> {{ user.missed_time }}</span>
            </div>
            <div class="info-row">
              <span class="label">Ban Start: </span>
              <span> {{ user.ban_start }}</span>
            </div>
            <div class="info-row">
              <span class="label">Ban End: </span>
              <span> {{ user.ban_end }}</span>
            </div>
          </div>
          <div class="card-actions">
            <el-button size="small" type="primary" @click="handleRelease(user)">
              Release
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {getCurrentInstance} from 'vue'

export default {
  name: 'BlacklistViewMobile',
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
      if (!gmtTimeString) return ''
      const gmtDate = new Date(gmtTimeString)
      if (isNaN(gmtDate.getTime())) {
        console.error('invalid date :', gmtTimeString)
        return 'invalid date'
      }
      if (addDays > 0) {
        gmtDate.setDate(gmtDate.getDate() + addDays)
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
      }).format(gmtDate)
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
            ban_end: this.convertTime(row.added_at, 30) || ''
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
    async handleRelease(user) {
      try {
        const confirmResult = await this.$confirm(
            `Are you sure you want to release ${user.user_email} from the blacklist?`,
            'Confirm Release',
            {
              confirmButtonText: 'Release',
              cancelButtonText: 'Cancel',
              type: 'warning'
            }
        ).catch(() => {
          return false
        })
        if (!confirmResult) return

        const loadingInstance = this.$loading({
          lock: true,
          text: 'Releasing user...',
          background: 'rgba(0, 0, 0, 0.7)'
        })

        const response = await fetch(
            `${this.backendAddress}/reset_missed_times/${encodeURIComponent(user.user_email)}`,
            {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json'
              }
            }
        )
        const result = await response.json()
        if (result.code === '000') {
          this.$message({
            message: 'User released successfully!',
            type: 'success'
          })
          await this.fetchBadUsers()
        } else {
          throw new Error(result.message || 'Failed to release user')
        }
      } catch (error) {
        this.$message({
          message: error.message || 'An error occurred while releasing the user',
          type: 'error'
        })
        console.error('Release error:', error)
      } finally {
        this.$loading().close()
      }
    }
  },
  mounted() {
    this.fetchBadUsers()
  }
}
</script>

<style scoped>
.blacklist-management-mobile-container {
  font-family: 'Cambria', serif;
  display: flex;
  flex-direction: column;
  background-color: #eceef8;
  width: 100%;
  height: 100vh;
  padding: 20px;
  overflow: auto;
}

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

.filter-controls {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin: 20px 0;
  padding: 0.5rem;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.mobile-filter {
  width: 100%;
}

.user-list {
  display: grid;
  gap: 1rem;
}

.user-card {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
}

.user-email {
  font-size: 1rem;
  color: #555;
}

.card-content {
  display: flex;
}

.card-body {
  flex: 0 0 60%;
}

.card-actions {
  margin-bottom: 30px;;
  flex: 0 0 53%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-body .info-row {
  justify-content: space-between;
  font-size: 1rem;
  margin-bottom: 0.3rem;
}

</style>

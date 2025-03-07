<template>
  <v-container fluid>
    <v-row justify="space-between" align="stretch">
      <!-- 日历和时间表并列 -->
      <v-col cols="12" md="6">
        <v-card style="background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
          <v-row>
            <v-col cols="12" md="6" class="d-flex justify-center align-center">
              <v-date-picker
                v-model="selectedDate"
                show-adjacent-months
                @input="handleDateSelection"
                flat
                no-title
                prev-icon="mdi-chevron-left"
                next-icon="mdi-chevron-right"
              ></v-date-picker>
            </v-col>
            <v-col cols="12" md="6">
              <v-row>
                <v-col v-for="(slot, index) in timeSlots" :key="index" cols="6">
                  <v-btn
                    :style="getButtonStyle(slot)"
                    :disabled="slot.status === 0"
                    block
                    class="ma-1"
                    depressed
                    @click="toggleSlot(index)"
                  >
                    {{ formatTime(slot.start) }} - {{ formatTime(slot.end) }}
                  </v-btn>
                </v-col>
              </v-row>
            </v-col>
            <!-- Room Status 标签 -->
            <v-col cols="12" style="background-color: #3155ef; border-radius: 0 0 8px 8px;">
              <div class="d-flex justify-center align-center" style="height: 40px; line-height: 40px; color: white;">
                Room Status
              </div>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      selectedDate: null,
      bookings: {
        '2025-03-07': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], // 全灰色（已预订）
        '2025-03-08': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], // 全灰色（已预定）
        '2025-03-09': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        '2025-03-15': [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
      },
      timeSlots: [
        { start: '08:00', end: '08:45', status: 1 },
        { start: '08:55', end: '09:40', status: 1 },
        { start: '10:00', end: '10:45', status: 1 },
        { start: '10:55', end: '11:40', status: 1 },
        { start: '12:00', end: '12:45', status: 1 },
        { start: '12:55', end: '13:40', status: 1 },
        { start: '14:00', end: '14:45', status: 1 },
        { start: '14:55', end: '15:40', status: 1 },
        { start: '16:00', end: '16:45', status: 1 },
        { start: '16:55', end: '17:40', status: 1 },
        { start: '19:00', end: '19:45', status: 1 },
        { start: '19:55', end: '20:40', status: 1 }
      ]
    };
  },
  methods: {
    handleDateSelection(date) {
      if (!date) {
        // 如果没有选择日期，所有时间段为灰色（不可选）
        this.timeSlots = this.timeSlots.map(slot => ({ ...slot, status: 0 }));
        return;
      }

      const localDate = new Date(date);
      const dateKey = [
        localDate.getFullYear(),
        String(localDate.getMonth() + 1).padStart(2, '0'),
        String(localDate.getDate()).padStart(2, '0')
      ].join('-');

      if (this.bookings[dateKey]) {
        this.timeSlots = this.timeSlots.map((slot, index) => ({
          ...slot,
          status: this.bookings[dateKey][index]
        }));
      } else {
        // 初始化新日期为全可预订状态
        this.timeSlots = this.timeSlots.map(slot => ({ ...slot, status: 1 }));
      }
    },

    toggleSlot(index) {
      if (this.timeSlots[index].status === 1) {
        this.timeSlots[index].status = 2;
      } else if (this.timeSlots[index].status === 2) {
        this.timeSlots[index].status = 1;
      }
      this.updateBookings();
    },

    updateBookings() {
      if (this.selectedDate) {
        const dateKey = this.selectedDate.toISOString().split('T')[0];
        this.$set(this.bookings, dateKey, this.timeSlots.map(slot => slot.status));
      }
    },

    getButtonStyle(slot) {
      if (!this.selectedDate) {
        return { backgroundColor: '#a6a6a6', color: 'white' };
      }
      switch (slot.status) {
        case 0: return { backgroundColor: '#a6a6a6', color: 'white' };
        case 1: return { backgroundColor: '#eceef8', color: 'black' };
        case 2: return { backgroundColor: '#3155ef', color: 'white' };
        default: return { backgroundColor: '#a6a6a6', color: 'white' };
      }
    },

    formatTime(time) {
      return time.substring(0, 5);
    }
  }
};
</script>

<style>
.v-date-picker-table--date .v-btn {
  background: transparent !important;
  color: rgba(0, 0, 0, 0.87) !important;
  font-weight: 400;
  border: none !important;
}

.v-btn {
  border: none !important;
  transition: all 0.2s;
}

.v-btn[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 隐藏默认头部 */
.v-date-picker-header {
  display: none;
}

/* 大背景框样式 */
.v-card {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 1050px; /* 固定宽度 */
  margin: 0 auto; /* 居中 */
}

/* Room Status 标签样式 */
.room-status-label {
  background-color: #3155ef;
  color: white;
  width: 100%;
  text-align: center;
  padding: 10px 0;
  margin-top: 20px;
}
</style>
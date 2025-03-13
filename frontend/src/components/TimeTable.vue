<template>
  <div class="container">
    <div class="card">
      <div class="card-content">
        <!-- 日历部分 -->
        <div class="calendar-container">
          <div class="calendar-header">
            <button @click="prevMonth" class="nav-button">‹</button>
            <span class="month-year">{{ currentMonth }} {{ currentYear }}</span>
            <button @click="nextMonth" class="nav-button">›</button>
          </div>

          <div class="calendar-grid">
            <div class="calendar-weekday" v-for="day in weekdays" :key="day">{{ day }}</div>
            <div
                v-for="day in daysInMonth"
                :key="day.date"
                :class="['calendar-day', {
    'selected': isSelected(day.date),
    'disabled': !day.isCurrentMonth || day.isPastDate
  }]"
                @click="!day.isPastDate && selectDate(day.date)"
            >
              {{ day.day }}
            </div>
          </div>
        </div>

        <!-- 时间槽部分 -->
        <div class="time-slots-container">
          <div class="time-slots-grid">
            <button
                v-for="(slot, index) in timeSlots"
                :key="index"
                :disabled="slot.status === 0"
                :class="['time-slot-button', { 'selected': slot.status === 2 }]"
                @click="toggleSlot(index)"
            >
              {{ formatTime(slot.start) }} - {{ formatTime(slot.end) }}
            </button>
          </div>
        </div>
      </div>
      <div class="room-status-label">
        Room Status
      </div>
    </div>
  </div>
</template>

<script>
import {inject} from "vue";

export default {
  emits: ['time-selected'],
  setup() {
    // 注入父组件提供的数据
    const childData = inject('childData');
    const roomSelected = inject('roomSelected')

    return {
      childData, roomSelected
    };
  },
  watch: {
    childData(newVal, oldVal) {
      console.log("old:", oldVal);
      console.log("new:", newVal);
      this.updateBookings(newVal);
      this.handleDateSelection(); // 更新时间槽状态
    },
    roomSelected(newVal, oldVal) {
      if (newVal === 0) {
        this.timeSlots.forEach((timeSlot) => {
          timeSlot.status = 0
        });
      }
    }
  },
  data() {
    return {
      selectedDate: null,
      currentDate: new Date(), // 当前显示的月份
      bookings: {}, // 初始化为空对象，等待 childData 注入
      timeSlots: Array(12).fill().map((_, index) => ({
        start: ['08:00', '08:55', '10:00', '10:55', '12:00', '12:55', '14:00', '14:55', '16:00', '16:55', '19:00', '19:55'][index],
        end: ['08:45', '09:40', '10:45', '11:40', '12:45', '13:40', '14:45', '15:40', '16:45', '17:40', '19:45', '20:40'][index],
        status: 0
      })),
      weekdays: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] // 英文星期缩写
    };
  },

  computed: {
    // 当前月份和年份
    currentMonth() {
      return this.currentDate.toLocaleString('en-US', {month: 'long'}); // 英文月份
    },
    currentYear() {
      return this.currentDate.getFullYear();
    },
    // 生成当前月份的日期
    daysInMonth() {
      const year = this.currentDate.getFullYear();
      const month = this.currentDate.getMonth();
      const firstDay = new Date(year, month, 1);
      const lastDay = new Date(year, month + 1, 0);
      const days = [];

      const today = new Date();
      today.setHours(0, 0, 0, 0);

      // 填充上个月的日期
      for (let i = firstDay.getDay(); i > 0; i--) {
        const date = new Date(year, month, -i + 1);
        days.push({
          day: date.getDate(), date: this.formatDate(date), isCurrentMonth: false,
          isPastDate: date < today
        });
      }

      // 填充当前月的日期
      for (let i = 1; i <= lastDay.getDate(); i++) {
        const date = new Date(year, month, i);
        days.push({
          day: i, date: this.formatDate(date), isCurrentMonth: true,
          isPastDate: date < today
        });
      }

      // 填充下个月的日期
      const nextMonthDays = 7 - (days.length % 7);
      for (let i = 1; i <= nextMonthDays; i++) {
        const date = new Date(year, month + 1, i);
        days.push({
          day: date.getDate(), date: this.formatDate(date), isCurrentMonth: false,
          isPastDate: date < today
        });
      }

      return days;
    }
  },

  methods: {
    // 上个月
    prevMonth() {
      this.currentDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() - 1, 1);
    },
    // 下个月
    nextMonth() {
      this.currentDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 1);
    },
    // 选择日期
    selectDate(date) {
      const selectedDate = new Date(date);
      const today = new Date();
      today.setHours(0, 0, 0, 0);

      if (selectedDate < today) {
        return;
      }

      this.selectedDate = selectedDate;
      this.handleDateSelection();
    },
    // 判断日期是否被选中
    isSelected(date) {
      return this.selectedDate && this.formatDate(this.selectedDate) === date;
    },
    // 处理日期选择
    handleDateSelection() {
      if (!this.selectedDate) {
        this.timeSlots = this.timeSlots.map(slot => ({...slot, status: 1}));
        return;
      }

      const dateKey = this.formatDate(this.selectedDate);

      if (this.bookings[dateKey]) {
        this.timeSlots = this.timeSlots.map((slot, index) => ({
          ...slot,
          status: this.bookings[dateKey][index]
        }));
      } else {
        this.timeSlots = this.timeSlots.map(slot => ({...slot, status: 1}));
      }

      this.emitSelection();
    },
    // 切换时间槽状态
    toggleSlot(index) {
      if (!this.selectedDate) return;

      const dateKey = this.formatDate(this.selectedDate);

      if (!this.bookings[dateKey]) {
        this.bookings[dateKey] = new Array(12).fill(1);
      }

      if (this.timeSlots[index].status === 1) {
        this.timeSlots[index].status = 2;
      } else if (this.timeSlots[index].status === 2) {
        this.timeSlots[index].status = 1;
      }

      this.emitSelection();
    },
    // 触发事件
    emitSelection() {
      const selectedSlots = this.timeSlots
          .map((slot, idx) => ({...slot, index: idx}))
          .filter(slot => slot.status === 2);
      this.$emit('time-selected', this.selectedDate, selectedSlots);
    },
    // 格式化时间
    formatTime(time) {
      const [hours, minutes] = time.split(':');
      return `${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}`;
    },
    // 格式化日期
    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    // 将 childData 转换为 bookings 对象
    updateBookings(bookingsArray) {
      this.bookings = {}; // 清空旧的 bookings

      bookingsArray.forEach(booking => {
        const date = new Date(booking.date);
        const timeSlots = booking.time; // 例如 [3, 7]

        const dateKey = this.formatDate(date);

        // 初始化当前日期的时间槽，默认全部可用
        if (!this.bookings[dateKey]) {
          this.bookings[dateKey] = new Array(12).fill(1); // 默认全部可用
        }

        // 标记不可用的时间槽
        timeSlots.forEach(slot => {
          if (slot >= 0 && slot < 12) {
            this.bookings[dateKey][slot] = 0; // 标记为不可用
          }
        });
      });
    },
  }
};
</script>

<style scoped>
/* 全局字体 */
body {
  font-family: 'Cambria', serif;
}

.container {
  min-height: 100%;
  width: 100%;
  padding: 10px;
}

.card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.card-content {
  display: flex;
  flex-grow: 1;
  height: 100%;
}

/* 日历部分 */
.calendar-container {
  max-height: 95%;
  margin-top: 2%;
  width: 50%;
  padding: 10px;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.nav-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.month-year {
  font-size: 1.2rem;
  font-weight: bold;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.calendar-weekday {
  text-align: center;
  font-weight: bold;
}

.calendar-day {
  text-align: center;
  padding: 8px;
  cursor: pointer;
  border-radius: 4px;
}

.calendar-day.selected {
  background-color: #3155ef;
  color: white;
}

.calendar-day.disabled {
  color: #ccc;
  cursor: not-allowed;
  pointer-events: none;
}


/* 时间槽部分 */
.time-slots-container {
  margin-top: 8%;
  width: 50%;
  height: 100%;
  overflow-y: auto;
  padding: 12px;
}

.time-slots-grid {
  display: grid;
  grid-template-columns: repeat(2, 2fr);
  gap: 15px;
}

.time-slot-button {
  width: 100%;
  padding: 8px;
  font-size: 0.8rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.time-slot-button:disabled {
  background-color: #a6a6a6;
  color: white;
  cursor: not-allowed;
}

.time-slot-button:not(:disabled) {
  background-color: #eceef8;
  color: black;
}

.time-slot-button.selected {
  background-color: #3155ef;
  color: white;
}

.room-status-label {
  font-weight: bolder;
  font-size: 25px;
  background-color: #3155ef;
  color: white;
  height: 20%;
  line-height: 40px;
  text-align: center;
  border-radius: 0 0 8px 8px;
}
</style>
<!--
TimeTable.vue - Interactive calendar for room booking with time slot selection.

Features:
- Monthly calendar view with navigation
- Time slot selection grid
- Disabled dates/slots for past times
- Visual indication of booked/selected slots
- Responsive layout

Props: None
Events:
- time-selected: Emitted when time slots are selected (date, slots)

Dependencies:
- None (pure Vue implementation)
-->
<template>
  <div class="container">
    <div class="card">
      <div class="card-content">
        <!-- Calendar section -->
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
                @click="!day.isPastDate && roomSelected !== 0 && selectDate(day.date)"
            >
              {{ day.day }}
            </div>
          </div>
        </div>

        <!-- Time slots section -->
        <div class="time-slots-container">
          <div class="time-slots-grid">
            <button
                v-for="(slot, index) in timeSlots"
                :disabled="slot.status === 0 || isSlotDisabled(slot, index)"
                :class="['time-slot-button', {
      'selected': slot.status === 2,
      'disabled': slot.status === 0 || isSlotDisabled(slot, index)
    }]"
                @click="toggleSlot(index)"
            >
              {{ formatTime(slot.start) }} - {{ formatTime(slot.end) }}
            </button>
          </div>
        </div>
      </div>
      <!-- Footer label -->
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
    // Inject shared state from parent
    const childData = inject('childData'); // Existing bookings
    const lessonData = inject('lessonData'); // Scheduled lessons
    const roomSelected = inject('roomSelected'); // Currently selected room

    return {
      childData, lessonData, roomSelected
    };
  },
  watch: {
    /**
     * Watches for changes in booking data and updates calendar
     */
    childData(newVal, oldVal) {
      console.log("old:", oldVal);
      console.log("new:", newVal);

      const combinedData = [...newVal, ...this.lessonData];
      console.log("combined:", combinedData)
      this.updateBookings(combinedData);

      this.handleDateSelection();

    },
    /**
     * Watches for room selection changes
     */
    roomSelected(newVal, oldVal) {
      console.log("newVal:", newVal)
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
      currentDate: new Date(),
      bookings: {},
      timeSlots: Array(12).fill().map((_, index) => ({
        start: ['08:00', '08:55', '10:00', '10:55', '12:00', '12:55', '14:00', '14:55', '16:00', '16:55', '19:00', '19:55'][index],
        end: ['08:45', '09:40', '10:45', '11:40', '12:45', '13:40', '14:45', '15:40', '16:45', '17:40', '19:45', '20:40'][index],
        status: 0
      })),
      weekdays: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    };
  },

  computed: {
    /**
     * Returns current month name
     * @returns {string} Current month
     */
    currentMonth() {
      return this.currentDate.toLocaleString('en-US', {month: 'long'});
    },
    /**
     * Returns current year
     * @returns {number} Current year
     */
    currentYear() {
      return this.currentDate.getFullYear();
    },
    /**
     * Generates array of days for current month view
     * @returns {Array} Days for calendar display
     */
    daysInMonth() {
      const year = this.currentDate.getFullYear();
      const month = this.currentDate.getMonth();
      const firstDay = new Date(year, month, 1);
      const lastDay = new Date(year, month + 1, 0);
      const days = [];

      const today = new Date();
      today.setHours(0, 0, 0, 0);

      for (let i = firstDay.getDay(); i > 0; i--) {
        const date = new Date(year, month, -i + 1);
        days.push({
          day: date.getDate(), date: this.formatDate(date), isCurrentMonth: false,
          isPastDate: date < today
        });
      }

      for (let i = 1; i <= lastDay.getDate(); i++) {
        const date = new Date(year, month, i);
        days.push({
          day: i, date: this.formatDate(date), isCurrentMonth: true,
          isPastDate: date < today
        });
      }

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
    /**
     * Navigates to previous month
     */
    prevMonth() {
      this.currentDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() - 1, 1);
    },
    /**
     * Navigates to next month
     */
    nextMonth() {
      this.currentDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 1);
    },
    /**
     * Selects a date and updates time slots
     * @param {string} date - Date string in YYYY-MM-DD format
     */
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
    /**
     * Checks if a date is currently selected
     * @param {string} date - Date string to check
     * @returns {boolean} True if date is selected
     */
    isSelected(date) {
      return this.selectedDate && this.formatDate(this.selectedDate) === date;
    },
    /**
     * Updates time slots based on selected date
     */
    handleDateSelection() {
      if (!this.selectedDate) {
        this.timeSlots = this.timeSlots.map(slot => ({...slot, status: 1}));
        return;
      }

      const dateKey = this.formatDate(this.selectedDate);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const selectedDate = new Date(this.selectedDate);
      selectedDate.setHours(0, 0, 0, 0);

      if (this.bookings[dateKey]) {
        this.timeSlots = this.timeSlots.map((slot, index) => {
          const isPast = selectedDate.getTime() === today.getTime() &&
              this.isSlotDisabled(slot, index);

          return {
            ...slot,
            status: isPast ? 0 : this.bookings[dateKey][index]
          };
        });
      } else {
        this.timeSlots = this.timeSlots.map((slot, index) => {
          const isPast = selectedDate.getTime() === today.getTime() &&
              this.isSlotDisabled(slot, index);

          return {
            ...slot,
            status: isPast ? 0 : 1
          };
        });
      }

      this.emitSelection();
    },
    /**
     * Toggles a time slot's selection state
     * @param {number} index - Index of time slot to toggle
     */
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
    /**
     * Emits selected time slots to parent
     */
    emitSelection() {
      const selectedSlots = this.timeSlots
          .map((slot, idx) => ({...slot, index: idx}))
          .filter(slot => slot.status === 2);
      this.$emit('time-selected', this.selectedDate, selectedSlots);
    },
    /**
     * Formats time string (HH:MM)
     * @param {string} time - Time string to format
     * @returns {string} Formatted time
     */
    formatTime(time) {
      const [hours, minutes] = time.split(':');
      return `${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}`;
    },
    /**
     * Formats date as YYYY-MM-DD
     * @param {Date} date - Date to format
     * @returns {string} Formatted date string
     */
    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    /**
     * Updates bookings data structure
     * @param {Array} bookingsArray - Array of booking objects
     */
    updateBookings(bookingsArray) {
      this.bookings = {};

      bookingsArray.forEach(booking => {
        const date = new Date(booking.date);
        const timeSlots = booking.time;

        const dateKey = this.formatDate(date);

        if (!this.bookings[dateKey]) {
          this.bookings[dateKey] = new Array(12).fill(1);
        }

        timeSlots.forEach(slot => {
          if (slot >= 0 && slot < 12) {
            this.bookings[dateKey][slot] = 0;
          }
        });
      });
    },
     /**
     * Checks if a time slot should be disabled
     * @param {Object} slot - Time slot object
     * @param {number} index - Slot index
     * @returns {boolean} True if slot should be disabled
     */
    isSlotDisabled(slot, index) {
      if (!this.selectedDate) return true;

      const today = new Date();
      today.setHours(0, 0, 0, 0);  // 00:00:00

      const selectedDate = new Date(this.selectedDate);
      selectedDate.setHours(0, 0, 0, 0);


      if (selectedDate < today) return true;

      if (selectedDate > today) return false;


      const now = new Date();
      console.log("now",now)
      const [hours, minutes] = slot.start.split(':');
      const slotTime = new Date();
      slotTime.setHours(parseInt(hours), parseInt(minutes), 0, 0);

      return slotTime < now;
    }
  }
};
</script>

<style scoped>
body {
  font-family: 'Cambria', serif;
}

.container {
  height: 100%;
  width: 100%;
  overflow: hidden;
}

.card {
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.card-content {
  display: flex;
  flex-grow: 1;
  height: 90%;
}

.calendar-container {
  max-height: 95%;
  margin-top: 2%;
  width: 50%;
  padding: 12px;
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
  height: 10%;
  line-height: 40px;
  text-align: center;
  border-radius: 0 0 20px 20px;
}
</style>
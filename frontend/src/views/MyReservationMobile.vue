<!--
MyReservationMobile.vue - Mobile-optimized reservation management component.

This component provides:
- Mobile-friendly view of user reservations with filtering capabilities
- Status-based styling for different reservation states
- Check-in and cancellation functionality
- Responsive card-based layout optimized for mobile devices

Props: None
Events: None
Dependencies: Element Plus UI components
-->
<template>
  <div class="reservation-container">
    <!-- Title section -->
    <div class="title-container">
      <h1><strong>DRBS</strong></h1>
      <h2><strong>My Reservation</strong></h2>
    </div>
    <!-- Filter controls section -->
    <div class="filter-container">
      <div class="filter-row">
        <el-select v-model="filters.date" multiple clearable placeholder="Date">
          <el-option v-for="value in uniqueDates" :key="value" :label="value" :value="value"/>
        </el-select>
        <el-select v-model="filters.time" multiple clearable placeholder="Time">
          <el-option v-for="timeSlot in timeSlots" :key="timeSlot" :label="timeSlot" :value="timeSlot"/>
        </el-select>
      </div>
      <div class="filter-row">
        <el-select v-model="filters.name" multiple clearable placeholder="Room">
          <el-option v-for="value in uniqueRooms" :key="value" :label="value" :value="value"/>
        </el-select>
        <el-select v-model="filters.status" multiple clearable placeholder="Status">
          <el-option v-for="value in uniqueStatusValues" :key="value" :label="value" :value="value"/>
        </el-select>
      </div>
    </div>
    <!-- Reservation list -->
    <div class="content-wrapper">
      <div class="reservation-list">
        <!-- Reservation card for each booking -->
        <el-card
            v-for="(reservation, index) in filteredReservations"
            :key="index"
            :class="['reservation-item', statusClass(reservation.status)]"
            shadow="hover"
        >
          <!-- Card header with room info and status -->
          <div class="card-header">
            <div class="room-info">
              <div class="room-name">{{ reservation.name }}</div>
            </div>
            <div class="booking-status">
              <el-tag
                  :type="statusTagType(reservation.status)"
                  size="mini"
                  class="booking-status-tag"
                  :data-status="reservation.status"
              >
                {{ reservation.status }}
              </el-tag>
            </div>
          </div>
          <!-- Reservation details -->
          <div class="reservation-content">
            <div class="reservation-info">
              <div class="reservation-time">
                <strong>Date:</strong> {{ reservation.date.split('00:00:00')[0] }}
              </div>
              <div class="reservation-time">
                <strong>Time:</strong> {{ convertTimeStrToTimeSlots(reservation.time) }}
              </div>
              <div class="reservation-capacity">
                <strong>Capacity:</strong> {{ reservation.capacity }}
              </div>
              <div class="reservation-purpose">
                <strong>Purpose:</strong> {{ reservation.purpose }}
              </div>
            </div>
          </div>
          <!-- Action buttons for confirmed reservations -->
          <div class="reservation-actions" v-if="reservation.status.toString() === 'Confirmed'">
            <button @click="checkIn(index)" class="action-button">Check In</button>
            <button @click="cancelReservation(index)" class="action-button">Cancel</button>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import {getCurrentInstance} from "vue";
import {ElCard, ElMessage, ElTag} from "element-plus";

export default {
  name: "MyReservationMobile",
  components: {
    ElCard,
    ElTag
  },
  setup() {
    // Initialize backend address from global properties
    const instance = getCurrentInstance();
    const backendAddress = instance.appContext.config.globalProperties.$backendAddress;
    return {backendAddress};
  },
  data() {
    return {
      user: [],// Current user data
      reservations: [],// List of user reservations
      reverseTimeSlotMap: {
        0: "08:00-08:45",
        1: "08:55-09:45",
        2: "10:00-10:45",
        3: "10:55-11:40",
        4: "12:00-12:45",
        5: "12:55-13:40",
        6: "14:00-14:45",
        7: "14:55-15:40",
        8: "16:00-16:45",
        9: "16:55-17:40",
        10: "19:00-19:45",
        11: "19:55-20:40"
      },// Mapping of time slot indexes to human-readable time ranges
      timeSlots: [
        "08:00-08:45",
        "08:55-09:45",
        "10:00-10:45",
        "10:55-11:40",
        "12:00-12:45",
        "12:55-13:40",
        "14:00-14:45",
        "14:55-15:40",
        "16:00-16:45",
        "16:55-17:40",
        "19:00-19:45",
        "19:55-20:40"
      ],// Array of all possible time slots for filtering
      filters: {
        date: [],
        time: [],
        name: [],
        status: []
      }// Current filter values
    };
  },
  computed: {
    /**
     * Computed property for unique dates from reservations
     * @returns {Array} List of unique dates
     */
    uniqueDates() {
      return [...new Set(this.reservations.map(item => item.date.split("00:00:00")[0]))];
    },
    /**
     * Computed property for unique room names from reservations
     * @returns {Array} List of unique room names
     */
    uniqueRooms() {
      return [...new Set(this.reservations.map(item => item.name))];
    },
    /**
     * Computed property for unique status values from reservations
     * @returns {Array} List of unique status values
     */
    uniqueStatusValues() {
      return [...new Set(this.reservations.map(item => item.status))];
    },
    /**
     * Computed property for filtered reservations based on current filters
     * @returns {Array} Filtered list of reservations
     */
    filteredReservations() {
      return this.reservations.filter(reservation => {
        // Filter by date if any dates are selected
        if (this.filters.date && this.filters.date.length > 0) {
          const resDate = reservation.date.split("00:00:00")[0];
          if (!this.filters.date.includes(resDate)) {
            return false;
          }
        }
        // Filter by time if any time slots are selected
        if (this.filters.time && this.filters.time.length > 0) {
          const resTimeArr = reservation.time
              .split(",")
              .map(Number)
              .map(index => this.reverseTimeSlotMap[index]);
          const match = this.filters.time.some(selectedTime => resTimeArr.includes(selectedTime));
          if (!match) {
            return false;
          }
        }
        // Filter by room name if any names are selected
        if (this.filters.name && this.filters.name.length > 0) {
          if (!this.filters.name.includes(reservation.name)) {
            return false;
          }
        }
        // Filter by status if any statuses are selected
        if (this.filters.status && this.filters.status.length > 0) {
          if (!this.filters.status.includes(reservation.status)) {
            return false;
          }
        }
        return true;
      });
    },
  },
  methods: {
    /**
     * Returns CSS class based on reservation status
     * @param {string} status - Reservation status
     * @returns {string} CSS class name
     */
    statusClass(status) {
      const classMap = {
        Pending: "status-pending",
        Confirmed: "status-confirmed",
        Declined: "status-declined",
        Completed: "status-completed",
        Missed: "status-missed",
        Banned: "status-banned"
      };
      return classMap[status] || "status-default";
    },
    /**
     * Returns Element Plus tag type based on reservation status
     * @param {string} status - Reservation status
     * @returns {string} Tag type
     */
    statusTagType(status) {
      const typeMap = {
        Pending: "warning",
        Confirmed: "success",
        Declined: "danger",
        Completed: "info",
        Missed: "info",
        Banned: "info"
      };
      return typeMap[status] || "info";
    },
    /**
     * Fetches user reservations from backend
     * @async
     */
    async fetchReservations() {
      try {
        const response = await fetch(this.backendAddress + "/get-reservations", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({email: this.user.email})
        });
        const data = await response.json();
        if (data.code === "000") {
          // Sort reservations by date (newest first)
          this.reservations = data.data.sort((a, b) => new Date(b.date) - new Date(a.date));
        } else {
          ElMessage.error(data.message);
        }
      } catch (error) {
        console.error("Error fetching reservations:", error);
      }
    },
    /**
     * Cancels a reservation
     * @async
     * @param {number} index - Index of reservation in filtered array
     */
    async cancelReservation(index) {
      const bookingId = this.reservations[index].booking_id;
      try {
        const response = await fetch(this.backendAddress + "/cancel-reservation", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({booking_id: bookingId})
        });
        const data = await response.json();
        if (data.code === '000') {
          ElMessage.success('Reservation cancelled successfully!');
          await this.fetchReservations();
        } else {
          ElMessage.error(data.message);
        }
      } catch (error) {
        console.error("Error cancelling reservation:", error);
      }
    },
    /**
     * Handles check-in for a reservation
     * @async
     * @param {number} index - Index of reservation in filtered array
     */
    async checkIn(index) {
      const bookingId = this.reservations[index].booking_id;
      try {
        const response = await fetch(this.backendAddress + "/booking_check_in/" + bookingId, {
          method: "GET"
        });
        const data = await response.json();
        if (data.code === '000') {
          ElMessage.success('Check-in successfully!');
          await this.fetchReservations();
        } else {
          ElMessage.error(data.message);
        }
      } catch (error) {
        console.error("Error:", error);
      }
    },
    /**
     * Converts time slot string to human-readable format
     * @param {string} timeStr - Comma-separated time slot indexes
     * @returns {string} Formatted time ranges
     */
    convertTimeStrToTimeSlots(timeStr) {
      return timeStr
          .split(",")
          .map(Number)
          .map(index => this.reverseTimeSlotMap[index])
          .join(" ");
    }
  },
  /**
 * Vue lifecycle hook - called after the component is mounted to the DOM
 * @async
 */
  async mounted() {
    const instance = getCurrentInstance();
    if (instance) {
      let me = await instance.appContext.config.globalProperties.$me()
      this.user = me.data
    }
    this.fetchReservations();
  }
};
</script>

<style scoped>
/* Base styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
/* Main container styling */
.reservation-container {
  font-family: "Cambria", serif;
  display: flex;
  flex-direction: column;
  background-color: #eceef8;
  width: 100%;
  min-height: 200vh;
  height: 100%;
  padding: 20px;
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
/* Filter controls styling */
.filter-container {
  margin: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.5rem;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.filter-row {
  display: flex;
  gap: 10px;
}
/* Main content layout */
.content-wrapper {
  display: flex;
  flex-direction: column;
  margin-bottom: 50px;
}
/* Reservation list styling */
.reservation-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
/* Individual reservation card styling */
.reservation-item {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
}
/* Status-based border colors */
.status-pending {
  border-left: 4px solid #b58d54;
}

.status-confirmed {
  border-left: 4px solid #5ccb6a;
}

.status-declined {
  border-left: 4px solid #ffbd59;
}

.status-completed {
  border-left: 4px solid #38b6ff;
}

.status-missed {
  border-left: 4px solid #ff5757;
}

.status-banned {
  border-left: 4px solid #737373;
}
/* Card header styling */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.2rem;
  width: 100%;
  flex-wrap: nowrap;
}

.room-info {
  display: flex;
  align-items: center;
  gap: 0.2rem;
  min-width: 0;
}

.room-name {
  font-size: 1.2rem;
  font-weight: bold;
  word-break: break-word;
}

/* Status tag styling */
.booking-status {
  margin-top: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
}

.booking-status-tag {
  font-size: 1rem;
  font-weight: bold;
}
/* Status-specific tag colors */
.booking-status-tag[data-status="Confirmed"] {
  background-color: #5ccb6a !important;
  border-color: #5ccb6a !important;
  color: #fff !important;
}

.booking-status-tag[data-status="Missed"] {
  background-color: #ff5757 !important;
  border-color: #ff5757 !important;
  color: #fff !important;
}

.booking-status-tag[data-status="Declined"] {
  background-color: #ffbd59 !important;
  border-color: #ffbd59 !important;
  color: #fff !important;
}

.booking-status-tag[data-status="Completed"] {
  background-color: #38b6ff !important;
  border-color: #38b6ff !important;
  color: #fff !important;
}

.booking-status-tag[data-status="Pending"] {
  background-color: #b58d54 !important;
  border-color: #b58d54 !important;
  color: #fff !important;
}

.booking-status-tag[data-status="Banned"] {
  background-color: #737373 !important;
  border-color: #737373 !important;
  color: #fff !important;
}
/* Reservation details styling */
.reservation-content {
  color: #545454;
  display: flex;
  flex-direction: column;
  font-size: 1rem;
}

.reservation-info {
  flex: 1;
}

.reservation-time,
.reservation-capacity,
.reservation-purpose {
  margin-top: 0.1rem;
}
/* Action buttons styling */
.reservation-actions {
  margin: 8px 10px auto 10px;
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
}

.action-button {
  width: 45%;
  font-size: 1rem;
  height: 1.6rem;
  background-color: #eceef8;
  border: none;
  border-radius: 10px;
}

/* Override Element Plus card padding */
:deep(.el-card__body) {
  padding: 0 !important;
}
</style>

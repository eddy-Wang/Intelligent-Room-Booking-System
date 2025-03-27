<template>
  <div class="reservation-container">
    <div class="title-container">
      <h1><strong>DRBS</strong></h1>
      <h2><strong>My Reservation</strong></h2>
    </div>
    <div class="filter-container">
      <div class="filter-row">
        <el-select v-model="filters.date" multiple clearable placeholder="Filter by Date">
          <el-option v-for="value in uniqueDates" :key="value" :label="value" :value="value"/>
        </el-select>
        <el-select v-model="filters.time" multiple clearable placeholder="Filter by Time">
          <el-option v-for="timeSlot in timeSlots" :key="timeSlot" :label="timeSlot" :value="timeSlot"/>
        </el-select>
      </div>
      <div class="filter-row">
        <el-select v-model="filters.name" multiple clearable placeholder="Filter by Room">
          <el-option v-for="value in uniqueRooms" :key="value" :label="value" :value="value"/>
        </el-select>
        <el-select v-model="filters.status" multiple clearable placeholder="Filter by Status">
          <el-option v-for="value in uniqueStatusValues" :key="value" :label="value" :value="value"/>
        </el-select>
      </div>
    </div>
    <div class="content-wrapper">
      <div class="reservation-list">
        <el-card
            v-for="(reservation, index) in filteredReservations"
            :key="index"
            :class="['reservation-item', statusClass(reservation.status)]"
            shadow="hover"
        >
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
import {ElCard, ElTag} from "element-plus";

export default {
  name: "MyReservationMobile",
  components: {
    ElCard,
    ElTag
  },
  setup() {
    const instance = getCurrentInstance();
    const backendAddress = instance.appContext.config.globalProperties.$backendAddress;
    return {backendAddress};
  },
  data() {
    return {
      user: [],
      reservations: [],
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
      },
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
      ],
      filters: {
        date: [],
        time: [],
        name: [],
        status: []
      }
    };
  },
  computed: {
    uniqueDates() {
      return [...new Set(this.reservations.map(item => item.date.split("00:00:00")[0]))];
    },
    uniqueRooms() {
      return [...new Set(this.reservations.map(item => item.name))];
    },
    uniqueStatusValues() {
      return [...new Set(this.reservations.map(item => item.status))];
    },
    filteredReservations() {
      return this.reservations.filter(reservation => {
        if (this.filters.date && this.filters.date.length > 0) {
          const resDate = reservation.date.split("00:00:00")[0];
          if (!this.filters.date.includes(resDate)) {
            return false;
          }
        }
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
        if (this.filters.name && this.filters.name.length > 0) {
          if (!this.filters.name.includes(reservation.room)) {
            return false;
          }
        }
        if (this.filters.status && this.filters.status.length > 0) {
          if (!this.filters.status.includes(reservation.status)) {
            return false;
          }
        }
        return true;
      });
    },
    userAvatar() {
      return this.user.permission === "student"
          ? "https://images.unsplash.com/photo-1609561505734-7c42d1bbafc9?w=500&auto=format&fit=crop&q=60"
          : "https://images.unsplash.com/photo-1507679799987-c73779587cc?w=500&auto=format&fit=crop&q=60";
    }
  },
  methods: {
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
    generateICSContent() {
      let icsData =
          "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//DIICSU Room Booking System//Reservation Calendar//EN\n";
      this.reservations.forEach(reservation => {
        let startDate = new Date(reservation.date)
            .toISOString()
            .replace(/[-:]/g, "")
            .split("T")[0];
        let timeSlots = reservation.time
            .split(",")
            .map(Number)
            .map(index => this.reverseTimeSlotMap[index]);
        timeSlots.forEach(timeSlot => {
          let [start, end] = timeSlot.split("-");
          let startDateTime = `${startDate}T${start.replace(":", "")}00Z`;
          let endDateTime = `${startDate}T${end.replace(":", "")}00Z`;
          icsData += `BEGIN:VEVENT UID:${reservation.name}-${startDateTime} DTSTAMP:${new Date()
              .toISOString()
              .replace(/[-:]/g, "")
              .split(".")[0]}Z DTSTART:${startDateTime} DTEND:${endDateTime} SUMMARY:${reservation.name} DESCRIPTION:Purpose: ${reservation.purpose} LOCATION:Capacity: ${reservation.room ||
          reservation.name} STATUS:${reservation.status} END:VEVENT `;
        });
      });
      icsData += "END:VCALENDAR";
      return icsData;
    },
    downloadCalendar() {
      try {
        const icsContent = this.generateICSContent();
        const blob = new Blob([icsContent], {type: "text/calendar"});
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${this.user.name}_my_reservation.ics`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        alert(
            'Calendar file downloaded!\n\n' +
            'To import the calendar:\n' +
            '1. Open your calendar app (e.g., Outlook, Google Calendar, Apple Calendar).\n' +
            '2. Find the "Import" or "Subscribe" option.\n' +
            '3. Select the downloaded .ics file.\n' +
            '4. Follow the prompts to complete the import.'
        );
      } catch (error) {
        console.error("Error generating calendar:", error);
        alert("Failed to generate calendar.");
      }
    },
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
          this.reservations = data.data.sort((a, b) => new Date(b.date) - new Date(a.date));
        } else {
          alert(data.message);
        }
      } catch (error) {
        console.error("Error fetching reservations:", error);
      }
    },
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
        if (data.code === "000") {
          alert("Reservation cancelled successfully!");
          await this.fetchReservations();
        } else {
          alert(data.message);
        }
      } catch (error) {
        console.error("Error cancelling reservation:", error);
      }
    },
    async checkIn(index) {
      const bookingId = this.reservations[index].booking_id;
      try {
        const response = await fetch(this.backendAddress + "/booking_check_in/" + bookingId, {
          method: "GET"
        });
        const data = await response.json();
        if (data.code === "000") {
          alert("Check-in successfully!");
          await this.fetchReservations();
        } else {
          alert(data.message);
        }
      } catch (error) {
        console.error("Error:", error);
      }
    },
    convertTimeStrToTimeSlots(timeStr) {
      return timeStr
          .split(",")
          .map(Number)
          .map(index => this.reverseTimeSlotMap[index])
          .join(" ");
    }
  },
  mounted() {
    const instance = getCurrentInstance();
    if (instance) {
      this.user = instance.appContext.config.globalProperties.$user;
    }
    this.fetchReservations();
  }
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

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

.filter-container {
  margin: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.filter-row {
  display: flex;
  gap: 10px;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  margin-bottom: 50px;
}

.reservation-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.reservation-item {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

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

.reservation-actions {
  margin-top: 1rem;
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.action-button {
  padding: 6px 12px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: bold;
  background-color: #eceef8;
  color: #333;
}

:deep(.el-card__body) {
  padding: 0 !important;
}
</style>

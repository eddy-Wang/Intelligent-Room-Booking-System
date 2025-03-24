<template>
  <div class="reservation-container">
    <div class="title-container">
      <h1><strong>DRBS</strong></h1>
      <h2><strong>My Reservation</strong></h2>
    </div>
    <div class="content-wrapper">
      <div class="reservation-list">
        <div
            v-for="(reservation, index) in reservations"
            :key="index"
            class="reservation-item">
          <div
              class="top-rectangle"
              :style="{ backgroundColor: getStatusColor(reservation.status) }">
            <span class="rectangle-text">{{ reservation.status }}</span>
          </div>
          <div
              class="status-rectangle"
              :style="{ backgroundColor: getStatusColor(reservation.status) }">
          </div>
          <div class="reservation-content">
            <div class="reservation-info">
              <div class="reservation-name">{{ reservation.name }}</div>
              <div class="reservation-time">
                <strong>Data:</strong> {{ reservation.date.split('00:00:00')[0] }}
              </div>
              <div class="reservation-time">
                <strong>Time:</strong> {{ convertTimeStrToTimeSlots(reservation.time) }}
              </div>
              <div class="reservation-capacity"><strong>Capacity:</strong> {{ reservation.capacity }}</div>
              <div class="reservation-purpose"><strong>Purpose:</strong> {{ reservation.purpose }}</div>
            </div>
          </div>
          <div class="reservation-actions" v-if="reservation.status.toString() === 'Confirmed'">
            <button @click="cancelReservation(index)" class="action-button">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {getCurrentInstance} from "vue";

const reverseTimeSlotMap = {
  0: '08:00-08:45',
  1: '08:55-09:45',
  2: '10:00-10:45',
  3: '10:55-11:40',
  4: '12:00-12:45',
  5: '12:55-13:40',
  6: '14:00-14:45',
  7: '14:55-15:40',
  8: '16:00-16:45',
  9: '16:55-17:40',
  10: '19:00-19:45',
  11: '19:55-20:40'
};

export default {
  name: 'MyReservationMobile',
  setup() {
    const instance = getCurrentInstance()
    const backendAddress = instance.appContext.config.globalProperties.$backendAddress

    return {backendAddress}
  },
  data() {
    return {
      user: [],
      reservations: [],
      reverseTimeSlotMap,
    };
  },
  computed: {
    userAvatar() {
      return this.user.permission === 'student'
          ? "https://images.unsplash.com/photo-1609561505734-7c42d1bbafc9?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDJ8fHxlbnwwfHx8fHw%3D"
          : "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fHN0YWZmfGVufDB8fDB8fHww";
    },
  },
  methods: {
    getStatusColor(status) {
      const statusColors = {
        'Confirmed': '#5ccb6a',
        'Missed': '#ff5757',
        'Declined': '#ffbd59',
        'Completed': '#38b6ff',
        'Pending': '#b58d54'
      };
      return statusColors[status] || '#000';
    },
    generateICSContent() {
      let icsData = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//DIICSU Room Booking System//Reservation Calendar//EN\n";

      this.reservations.forEach(reservation => {
        let startDate = new Date(reservation.date).toISOString().replace(/[-:]/g, '').split('T')[0];
        let timeSlots = reservation.time.split(',').map(Number).map(index => this.reverseTimeSlotMap[index]);

        timeSlots.forEach(timeSlot => {
          let [start, end] = timeSlot.split('-');
          let startDateTime = `${startDate}T${start.replace(':', '')}00Z`;
          let endDateTime = `${startDate}T${end.replace(':', '')}00Z`;

          icsData +=
              `BEGIN:VEVENT
UID:${reservation.name}-${startDateTime}
DTSTAMP:${new Date().toISOString().replace(/[-:]/g, '').split('.')[0]}Z
DTSTART:${startDateTime}
DTEND:${endDateTime}
SUMMARY:${reservation.name}
DESCRIPTION:Purpose: ${reservation.purpose}
LOCATION:Capacity: ${reservation.name}
STATUS:${reservation.status}
END:VEVENT
`;
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
        const response = await fetch(this.backendAddress+'/get-reservations', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({email: this.user.email}),
        });
        const data = await response.json();
        if (data.code === '000') {
          this.reservations = data.data.sort((a, b) => new Date(b.date) - new Date(a.date));
        } else {
          alert(data.message);
        }
      } catch (error) {
        console.error('Error fetching reservations:', error);
      }
    },
    async cancelReservation(index) {
      const bookingId = this.reservations[index].booking_id;
      try {
        const response = await fetch(this.backendAddress+'/cancel-reservation', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({booking_id: bookingId}),
        });
        const data = await response.json();
        if (data.code === '000') {
          alert('Reservation cancelled successfully!');
          await this.fetchReservations();
        } else {
          alert(data.message);
        }
      } catch (error) {
        console.error('Error cancelling reservation:', error);
      }
    },
    convertTimeStrToTimeSlots(timeStr) {
      return timeStr.split(',')
          .map(Number)
          .map(index => this.reverseTimeSlotMap[index])
          .join('  ');
    }
  },
  mounted() {
    const instance = getCurrentInstance();
    if (instance) {
      this.user = instance.appContext.config.globalProperties.$user;
    }
    this.fetchReservations();
  },
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.reservation-container {
  font-family: 'Cambria', serif;
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

.content-wrapper {
  display: flex;
  flex-direction: column;
}

.reservation-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.reservation-item {
  position: relative;
  flex-wrap: wrap;
  background-color: #ffffff;
  border-radius: 20px;
  padding: 0;
  display: flex;
  align-items: stretch;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.top-rectangle {
  position: absolute;
  top: 0;
  left: 76%;
  width: 18%;
  height: 30px;
  border-radius: 0 0 10px 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: bold;
  color: #fff;
}

.status-rectangle {
  width: 4.5%;
  border-radius: 20px 0 0 20px;
}

.reservation-content {
  color: #545454;
  flex: 1;
  display: flex;
  flex-direction: column;
  margin: 20px 25% 20px 20px;
  font-size: 1rem;
}

.reservation-info {
  flex: 1;
}

.reservation-name {
  color: black;
  font-size: 1.2rem;
  font-weight: bold;
}

.reservation-actions {
  border-radius: 10px;
  position: absolute;
  top: 50%;
  left: 78%;
  transform: translateY(-50%);
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
</style>

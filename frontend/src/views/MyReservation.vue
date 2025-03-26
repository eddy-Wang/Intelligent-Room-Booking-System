<template>
    <div class="panel">
        <div class="container">
            <h1>My Reservation</h1>

            <!-- Filter Dropdowns -->
            <div class="filter-container">
                <el-select v-model="roomFilter" placeholder="Filter by Room" clearable>
                    <el-option
                            v-for="room in uniqueRooms"
                            :key="room"
                            :label="room"
                            :value="room"
                    />
                </el-select>

                <el-select v-model="dateFilter" placeholder="Filter by Date" clearable>
                    <el-option
                            v-for="date in uniqueDates"
                            :key="date"
                            :label="date"
                            :value="date"
                    />
                </el-select>

                <el-select v-model="statusFilter" placeholder="Filter by Status" clearable>
                    <el-option
                            v-for="status in uniqueStatuses"
                            :key="status"
                            :label="status"
                            :value="status"
                    />
                </el-select>
            </div>

            <div class="content-wrapper">
                <div class="reservation-list">
                    <div
                            v-for="(reservation, index) in paginatedReservations"
                            :key="index"
                            class="reservation-item"
                    >
                        <div class="reservation-info">
                            <div class="reservation-name">{{ reservation.name }}</div>
                            <div class="reservation-time">
                                {{ reservation.date.split('00:00:00')[0] + convertTimeStrToTimeSlots(reservation.time) }}
                            </div>
                            <div class="reservation-capacity">Capacity: {{ reservation.capacity }}</div>
                            <div class="reservation-purpose">{{ reservation.purpose }}</div>
                        </div>
                        <div class="status-and-actions">
                            <div class="reservation-status">{{ reservation.status }}</div>
                            <div class="reservation-actions" v-if="reservation.status.toString() === 'Confirmed'">
                                <button @click="checkIn(index)" class="action-button">Check In</button>
                                <button @click="cancelReservation(index)" class="action-button">Cancel</button>
                            </div>
                        </div>
                    </div>
                    <div class="pagination">
                        <button @click="prevPage" :disabled="currentPage === 1" class="pagination-button">Previous</button>
                        <button @click="nextPage" :disabled="currentPage === totalPages" class="pagination-button">Next</button>
                    </div>
                </div>

                <div class="user-info">
                    <div class="user-avatar">
                        <img :src="userAvatar" alt="User Avatar"/>
                    </div>
                    <div class="user-email">{{ user.name }}</div>
                    <div class="user-email">{{ user.email }}</div>
                    <div class="user-role">{{ user.permission }}</div>
                    <button @click="downloadCalendar" class="download-button">Subscribe to Calendar</button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { getCurrentInstance } from "vue";

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
    name: 'MyReservation',
    setup() {
        const instance = getCurrentInstance();
        const backendAddress = instance.appContext.config.globalProperties.$backendAddress;
        return { backendAddress };
    },
    data() {
        return {
            user: [],
            reservations: [],
            currentPage: 1,
            reverseTimeSlotMap,
            itemsPerPage: 3,
            roomFilter: '',
            dateFilter: '',
            statusFilter: '',
        };
    },
    computed: {
        uniqueRooms() {
            return [...new Set(this.reservations.map(reservation => reservation.name))];
        },
        uniqueDates() {
            return [...new Set(this.reservations.map(reservation => reservation.date.split('00:00:00')[0]))];
        },
        uniqueStatuses() {
            return [...new Set(this.reservations.map(reservation => reservation.status))];
        },
        filteredReservations() {
            return this.reservations.filter(reservation => {
                return (
                    (this.roomFilter ? reservation.name === this.roomFilter : true) &&
                    (this.dateFilter ? reservation.date.split('00:00:00')[0] === this.dateFilter : true) &&
                    (this.statusFilter ? reservation.status === this.statusFilter : true)
                );
            });
        },
        totalPages() {
            return Math.ceil(this.filteredReservations.length / this.itemsPerPage);
        },
        paginatedReservations() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.filteredReservations.slice(start, end);
        },
        userAvatar() {
            return this.user.permission === 'student'
                ? "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                : "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";
        },
    },
    methods: {
        generateICSContent() {
            let icsData = `BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//DIICSU Room Booking System//Reservation Calendar//EN\n`;
            this.reservations.forEach(reservation => {
                let startDate = new Date(reservation.date).toISOString().replace(/[-:]/g, '').split('T')[0];
                let timeSlots = reservation.time.split(',').map(Number).map(index => this.reverseTimeSlotMap[index]);
                timeSlots.forEach(timeSlot => {
                    let [start, end] = timeSlot.split('-');
                    let startDateTime = `${startDate}T${start.replace(':', '')}00Z`;
                    let endDateTime = `${startDate}T${end.replace(':', '')}00Z`;
                    icsData += `
BEGIN:VEVENT
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
            icsData += `END:VCALENDAR`;
            return icsData;
        },
        downloadCalendar() {
            try {
                const icsContent = this.generateICSContent();
                const blob = new Blob([icsContent], { type: "text/calendar" });
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
                const response = await fetch(this.backendAddress + '/get-reservations', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email: this.user.email }),
                });
                const data = await response.json();
                if (data.code === '000') {
                    this.reservations = data.data.sort((a, b) => {
                        return new Date(b.date) - new Date(a.date);
                    });
                } else {
                    alert(data.message);
                }
            } catch (error) {
                console.error('Error fetching reservations:', error);
            }
        },
        async cancelReservation(index) {
            const bookingId = this.reservations[(this.currentPage - 1) * this.itemsPerPage + index].booking_id;
            try {
                const response = await fetch(this.backendAddress + '/cancel-reservation', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        booking_id: bookingId,
                    }),
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
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },
        convertTimeStrToTimeSlots(timeStr) {
            return timeStr.split(',')
                .map(Number)
                .map(index => this.reverseTimeSlotMap[index])
                .join('  ');
        },
        async checkIn(index) {
          const bookingId = this.reservations[(this.currentPage - 1) * this.itemsPerPage + index].booking_id
          try {
            const response = await fetch(this.backendAddress + '/booking_check_in/'+bookingId, {
              method: 'GET'
            });
            const data = await response.json();
            if (data.code === '000') {
              alert('Check-in successfully!');
              await this.fetchReservations();
            } else {
              alert(data.message);
            }
          } catch (error) {
            console.error('Error:', error);
          }
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

.panel {
    background: #eceef8;
    display: flex;
    justify-content: space-between;
    min-height: 100vh;
}

body {
    font-family: 'Segoe UI', Arial, sans-serif;
    background-color: #f5f7fa;
    color: #333;
    line-height: 1.6;
}

.container {
    font-family: 'Cambria', serif;
    width: 100%;
    height: 80%;
    max-width: 1750px;
    margin: 20px auto;
    padding: 20px;
    background-color: #eceef8;
    border-radius: 12px;
}

h1 {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 20px;
    font-size: 3.5rem;
}

.filter-container {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

.content-wrapper {
    display: flex;
    gap: 20px;
}

.reservation-list {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.reservation-item {
    height:80%;
    width:100%;
    background-color: #ffffff;
    border-radius: 20px;
    padding: 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.reservation-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.reservation-info {
    flex: 1;
}

.reservation-name {
    font-size: 1.5rem;
    font-weight: bold;
    color: #34495e;
}

.reservation-time {
    font-size: 1.2rem;
    color: #555;
    margin-top: 5px;
}

.reservation-purpose {
    font-size: 1.0rem;
    color: #777;
    margin-top: 5px;
}

.reservation-capacity {
    font-size: 1.0rem;
    color: #777;
    margin-top: 5px;
}

.reservation-status {
    font-size: 2.5rem;
    color: #34495e;
    font-weight: bold;
    margin-right: 20px;
}

.status-and-actions {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 10px;
}

.reservation-actions {
    width: 105%;
    display: flex;
    flex-direction: row;
    gap: 5px;
}

.action-button {
    height:20%;
    width: 100%;
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1.1rem;
    background-color: #eceef8;
    color: #333;
    transition: background-color 0.2s ease;
}

.action-button:disabled {
    background-color: #a6a6a6;
    cursor: not-allowed;
}

.action-button:not(:disabled):hover {
    background-color: #3155ef;
    color: #fff;
}

.user-info {
    width: 30%;
    height: 20%;
    padding: 80px;
    background-color: #eceef8;
    border-radius: 12px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.user-avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
}

.user-avatar img {
    width: 300px;
    height: 300px;
    border-radius: 50%;
    object-fit: cover;
}

.user-email {
    font-size: 1.2rem;
    color: #333;
    margin-top: 10px;
}

.user-role {
    font-size: 1rem;
    color: #777;
    margin-top: 5px;
}

.pagination {
    display: flex;
    justify-content: center;
    margin-top: 10px;
    gap: 10px;
}

.pagination-button {
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    background-color: #ffffff;
    color: #333;
    font-size: 1rem;
    transition: background-color 0.2s ease;
}

.pagination-button:disabled {
    background-color: #a6a6a6;
    cursor: not-allowed;
}

.pagination-button:not(:disabled):hover {
    background-color: #3155ef;
    color: #fff;
}

.download-button {
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1.1rem;
    background-color: #d3dafb;
    color: #333;
    transition: background-color 0.2s ease;
    margin-top: 20px;
}

.download-button:disabled {
    background-color: #a6a6a6;
    cursor: not-allowed;
}

.download-button:not(:disabled):hover {
    background-color: #3155ef;
    color: #fff;
}

.el-select{
    border-radius: 10px;
    width:22.5%;
    height:15%;
}
</style>
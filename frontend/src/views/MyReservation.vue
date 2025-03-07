<template>
    <div class="panel">
        <div class="container">
            <h1>My Reservation</h1>
            <div class="content-wrapper">
                <div class="reservation-list">
                    <div
                        v-for="(reservation, index) in paginatedReservations"
                        :key="index"
                        class="reservation-item"
                    >
                        <div class="reservation-info">
                            <div class="reservation-name">{{ reservation.name }}</div>
                            <div class="reservation-time">{{ reservation.time }}</div>
                            <div class="reservation-capacity">Capacity: {{ reservation.capacity }}</div>
                            <div class="reservation-purpose">{{ reservation.purpose }}</div>
                        </div>
                        <div class="status-and-actions">
                            <div class="reservation-status">{{ getStatusText(reservation.status) }}</div>
                            <div class="reservation-actions" v-if="reservation.status === 0">
                                <button @click="modifyReservation(index)" class="action-button">Modify</button>
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
                        <img :src="userAvatar" alt="User Avatar" />
                    </div>
                    <div class="user-email">{{ user.email }}</div>
                    <div class="user-role">{{ user.role === 0 ? 'Student' : 'Staff' }}</div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
export default {
    name: 'MyReservation',
    data() {
        return {
            reservations: [
                { name: "Room A", time: "10:00 AM - 12:00 PM", purpose: "Meeting", capacity: 10, status: 0 },
                { name: "Room B", time: "1:00 PM - 3:00 PM", purpose: "Interview", capacity: 5, status: 1 },
                { name: "Room C", time: "4:00 PM - 6:00 PM", purpose: "Workshop", capacity: 20, status: 2 },
                { name: "Room D", time: "7:00 PM - 9:00 PM", purpose: "Training", capacity: 15, status: 3 },
                { name: "Room E", time: "10:00 PM - 12:00 AM", purpose: "Event", capacity: 30, status: 4 },
            ],
            currentPage: 1,
            itemsPerPage: 3,
            user: {
                email: "user@example.com",
                role: 0, // 0 for Student, 1 for Staff
            },
            avatarUrls: {
                student: "https://images.unsplash.com/photo-1609561505734-7c42d1bbafc9?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDJ8fHxlbnwwfHx8fHw%3D", // Student 头像
                staff: "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fHN0YWZmfGVufDB8fDB8fHww", // Staff 头像
            },
        };
    },
    computed: {
        totalPages() {
            return Math.ceil(this.reservations.length / this.itemsPerPage);
        },
        paginatedReservations() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.reservations.slice(start, end);
        },
        userAvatar() {
            return this.user.role === 0 ? this.avatarUrls.student : this.avatarUrls.staff;
        },
    },
    methods: {
        getStatusText(status) {
            const statusMap = {
                0: "Booked",
                1: "Done",
                2: "Reviewing",
                3: "Declined",
                4: "Missed",
            };
            return statusMap[status];
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
        modifyReservation(index) {
            alert(`Modify reservation: ${this.reservations[index].name}`);
        },
        cancelReservation(index) {
            alert(`Cancel reservation: ${this.reservations[index].name}`);
        },
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

.content-wrapper {
    display: flex;
    gap: 20px; /* 列表和用户信息之间的间距 */
}

.reservation-list {
    flex: 1; /* 占据剩余空间 */
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.reservation-item {
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
    display: flex;
    flex-direction: row;
    gap: 5px;
}

.action-button {
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
    width: 450px; /* 用户信息区域宽度 */
    height: 660px; /* 确保容器高度占满父容器 */
    padding: 20px;
    background-color: #eceef8;
    border-radius: 12px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center; /* 水平居中 */
    justify-content: center; /* 垂直居中 */
}
.user-avatar {
    display: flex;
    align-items: center; /* 垂直居中 */
    justify-content: center; /* 水平居中 */
    margin-bottom: 10px; /* 头像和邮箱之间的间距 */
}

.user-avatar img {
    width: 300px;
    height: 300px;
    border-radius: 50%; /* 圆形头像 */
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
</style>

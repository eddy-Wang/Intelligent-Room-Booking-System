<template>
  <div class="panel">
    <div class="container">
      <h1>Room Management</h1>
      <div class="content-wrapper">
        <div class="admin-actions">
          <button @click="showAddRoomModal = true" class="add-button">Add Room</button>
        </div>
        <div class="room-list">
          <div
              v-for="(room, index) in paginatedRooms"
              :key="index"
              class="room-item"
          >
            <div class="room-image">
              <img :src="room.image" alt="Room Image" class="room-img" />
            </div>
            <div class="room-info">
              <div class="room-name">{{ room.name }}</div>
              <div class="room-capacity">Capacity: {{ room.capacity }}</div>
              <div class="room-location">Location: {{ room.location }}</div>
              <div class="room-equipment">Equipment: {{ room.equipment.join(', ') }}</div>
            </div>
            <div class="status-and-actions">
              <div class="room-actions">
                <button @click="modifyRoom(index)" class="action-button">Modify</button>
                <button @click="deleteRoom(index)" class="action-button">Delete</button>
              </div>
            </div>
          </div>
          <div class="pagination">
            <button @click="prevPage" :disabled="currentPage === 1" class="pagination-button">Previous</button>
            <button @click="nextPage" :disabled="currentPage === totalPages" class="pagination-button">Next</button>
          </div>
        </div>



        <!-- 弹窗：增加房间 -->
        <div v-if="showAddRoomModal" class="modal">
          <div class="modal-content">
            <h2>Add Room</h2>
            <form @submit.prevent="addRoom">
              <label for="room-name">Room Name:</label>
              <input type="text" id="room-name" v-model="newRoom.name" required />

              <label for="room-capacity">Capacity:</label>
              <input type="number" id="room-capacity" v-model="newRoom.capacity" required />

              <label for="room-location">Location:</label>
              <input type="text" id="room-location" v-model="newRoom.location" required />

              <label for="room-equipment">Equipment (comma separated):</label>
              <input type="text" id="room-equipment" v-model="newRoom.equipmentInput" required />

              <button type="submit" class="action-button">Add</button>
              <button @click="showAddRoomModal = false" class="action-button">Cancel</button>
            </form>
          </div>
        </div>

        <!-- 弹窗：修改房间 -->
        <div v-if="showModifyRoomModal" class="modal">
          <div class="modal-content">
            <h2>Modify Room</h2>
            <form @submit.prevent="saveModifiedRoom">
              <label for="modify-room-name">Room Name:</label>
              <input type="text" id="modify-room-name" v-model="modifiedRoom.name" required />

              <label for="modify-room-capacity">Capacity:</label>
              <input type="number" id="modify-room-capacity" v-model="modifiedRoom.capacity" required />

              <label for="modify-room-location">Location:</label>
              <input type="text" id="modify-room-location" v-model="modifiedRoom.location" required />

              <label for="modify-room-equipment">Equipment (comma separated):</label>
              <input type="text" id="modify-room-equipment" v-model="modifiedRoom.equipmentInput" required />

              <button type="submit" class="action-button">Save</button>
              <button @click="showModifyRoomModal = false" class="action-button">Cancel</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import roomAImage from '@/assets/room1.png';
export default {
  name: 'RoomManagement',
  data() {
    return {
      rooms: [
        {
          name: "Room A",
          capacity: 10,
          location: "Building 1, Floor 2",
          equipment: ["Projector", "Whiteboard"],
          status: true,
          image: roomAImage
        },
        {
          name: "Room B",
          capacity: 5,
          location: "Building 2, Floor 1",
          equipment: ["TV", "Conference Phone"],
          status: false,
          image: roomAImage
        },
        {
          name: "Room C",
          capacity: 20,
          location: "Building 3, Floor 3",
          equipment: ["Projector", "Microphone"],
          status: true,
          image: roomAImage
        },
      ],
      currentPage: 1,
      itemsPerPage: 3,
      showAddRoomModal: false,
      showModifyRoomModal: false,
      newRoom: {
        name: "",
        capacity: 0,
        location: "",
        equipmentInput: "",
      },
      modifiedRoom: {
        index: null,
        name: "",
        capacity: 0,
        location: "",
        equipmentInput: "",
      },
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.rooms.length / this.itemsPerPage);
    },
    paginatedRooms() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.rooms.slice(start, end);
    },
  },
  methods: {
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
    addRoom() {
      const equipment = this.newRoom.equipmentInput.split(',').map(item => item.trim());
      this.rooms.push({
        name: this.newRoom.name,
        capacity: this.newRoom.capacity,
        location: this.newRoom.location,
        equipment: equipment,
        status: true,
      });
      this.showAddRoomModal = false;
      this.resetNewRoom();
    },
    modifyRoom(index) {
      this.modifiedRoom = {
        index: index,
        name: this.rooms[index].name,
        capacity: this.rooms[index].capacity,
        location: this.rooms[index].location,
        equipmentInput: this.rooms[index].equipment.join(', '),
      };
      this.showModifyRoomModal = true;
    },
    saveModifiedRoom() {
      const equipment = this.modifiedRoom.equipmentInput.split(',').map(item => item.trim());
      this.rooms[this.modifiedRoom.index] = {
        name: this.modifiedRoom.name,
        capacity: this.modifiedRoom.capacity,
        location: this.modifiedRoom.location,
        equipment: equipment,
        status: this.rooms[this.modifiedRoom.index].status,
      };
      this.showModifyRoomModal = false;
    },
    deleteRoom(index) {
      if (confirm("Are you sure you want to delete this room?")) {
        this.rooms.splice(index, 1);
      }
    },
    resetNewRoom() {
      this.newRoom = {
        name: "",
        capacity: 0,
        location: "",
        equipmentInput: "",
      };
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
  font-size: 3.5rem;
}

.content-wrapper {
  display: grid;
  gap: 20px; /* 列表和用户信息之间的间距 */
}

.room-list {
  flex: 1; /* 占据剩余空间 */
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.room-item {
  background-color: #ffffff;
  border-radius: 20px;
  //padding: 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.room-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.room-info {
  padding: 40px 0 40px 40px;
  flex: 1;
}

.room-name {
  font-size: 1.5rem;
  font-weight: bold;
  color: #34495e;
}

.room-capacity {
  font-size: 1.0rem;
  color: #777;
  margin-top: 5px;
}

.status-and-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
}

.room-actions {
  display: flex;
  flex-direction: row;
  gap: 5px;
}
.add-button{
  margin-left: 50%;
  padding: 8px 16px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1.1rem;
  background-color: #ffffff;
  color: #333;
  transition: background-color 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.add-button:disabled {
  background-color: #a6a6a6;
  cursor: not-allowed;
}

.add-button:not(:disabled):hover {
  background-color: #3155ef;
  color: #fff;
}

.action-button {
  padding: 8px 16px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1.1rem;
  background-color: #ffffff;
  color: #333;
  transition: background-color 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.action-button:disabled {
  background-color: #a6a6a6;
  cursor: not-allowed;
}

.action-button:not(:disabled):hover {
  background-color: #3155ef;
  color: #fff;
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
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  width: 400px;
}

.modal-content form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.modal-content label {
  font-weight: bold;
}

.modal-content input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.admin-actions {
  margin-top: 20px;
  text-align: center;
}

.room-item {
  display: flex;
  align-items: center; /* 确保图片和内容垂直居中 */
  gap: 20px; /* 图片和内容之间的间距 */
}

.room-image {
  min-width: 100px; /* 图片宽度 */
  height: 200px; /* 图片高度 */
  border-radius: 10px 0 0 10px; /* 左上角和左下角圆角，右上角和右下角直角 */
  overflow: hidden; /* 确保图片不会超出容器 */
}

.room-img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 确保图片填充整个容器 */
}

</style>
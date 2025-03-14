<template>
  <div class="panel">
    <div class="container">
      <h1>Room Management</h1>
      <div class="content-wrapper">
        <div class="admin-actions">
          <button @click="showAddRoomModal = true" class="add-button">Add Room</button>
        </div>
        <div class="room-list">
          <!-- 房间项容器（带滚动条） -->
          <div class="room-items-container">
            <div
                v-for="(room, index) in paginatedRooms"
                :key="index"
                class="room-item"
            >
              <div class="room-image">
                <img :src="room.image" alt="Room Image" class="room-img"/>
              </div>
              <div class="room-info">
                <div class="room-name">{{ room.name }}</div>
                <div class="room-capacity">Capacity: {{ room.capacity }}</div>
                <div class="room-location">Location: {{ room.location }}</div>
                <div class="room-equipment">Equipment: {{ room.equipment.join(', ') }}</div>
                <div class="room-access">Access: {{ room.access }}</div>
                <div class="room-information">Information: {{ room.information || 'N/A' }}</div>
              </div>

              <div class="room-actions">
                <button @click="modifyRoom(index)" class="action-button">Modify</button>
                <button @click="deleteRoom(index)" class="action-button">Delete</button>
              </div>
            </div>
          </div>
          <div class="pagination">
            <button
                @click="prevPage"
                :disabled="currentPage === 1"
                class="pagination-button"
            >
              Previous
            </button>
            <button
                @click="nextPage"
                :disabled="currentPage === totalPages"
                class="pagination-button"
            >
              Next
            </button>
          </div>
        </div>


        <!-- 弹窗：增加房间 -->
        <div v-if="showAddRoomModal" class="modal">
          <div class="modal-content">
            <h2>Add Room</h2>
            <form @submit.prevent="addRoom">
              <label for="room-name">Room Name:</label>
              <input type="text" id="room-name" v-model="newRoom.name" required/>

              <label for="room-capacity">Capacity:</label>
              <input type="number" id="room-capacity" v-model="newRoom.capacity" required/>

              <label for="room-location">Location:</label>
              <input type="text" id="room-location" v-model="newRoom.location" required/>

              <label for="room-equipment">Equipment (comma separated):</label>
              <input type="text" id="room-equipment" v-model="newRoom.equipmentInput" required/>

              <label for="room-access">Access:</label>
              <select id="room-access" v-model="newRoom.access" required>
                <option value="All">All</option>
                <option value="Staff Only">Staff Only</option>
                <option value="Selected Staff Only">Selected Staff Only</option>
              </select>
              <label for="room-image">Image:</label>
              <input
                  type="file"
                  id="room-image"
                  @change="handleAddImageUpload"
                  accept="image/*"
                  required
                  title="Select room image"
                  class="custom-file-input"
              >

              <label for="room-information">Information (optional):</label>
              <textarea id="room-information" v-model="newRoom.information"></textarea>

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
              <input type="text" id="modify-room-name" v-model="modifiedRoom.name" required/>

              <label for="modify-room-capacity">Capacity:</label>
              <input type="number" id="modify-room-capacity" v-model="modifiedRoom.capacity" required/>

              <label for="modify-room-location">Location:</label>
              <input type="text" id="modify-room-location" v-model="modifiedRoom.location" required/>

              <label for="modify-room-equipment">Equipment (comma separated):</label>
              <input type="text" id="modify-room-equipment" v-model="modifiedRoom.equipmentInput" required/>

              <label for="modify-room-access">Access:</label>
              <select id="modify-room-access" v-model="modifiedRoom.access" required>
                <option value="All">All</option>
                <option value="Staff Only">Staff Only</option>
                <option value="Selected Staff Only">Selected Staff Only</option>
              </select>
              <label for="modify-room-image">Image:</label>
              <input
                  type="file"
                  id="modify-room-image"
                  @change="handleModifyImageUpload"
                  accept="image/*"
                  title="Select room image"
                  class="custom-file-input"
              >
              <!-- 显示当前图片 -->
              <div v-if="modifiedRoom.image" class="image-preview">
                <img :src="modifiedRoom.image" alt="Current Image" class="preview-img">
              </div>
              <label for="modify-room-information">Information (optional):</label>
              <textarea id="modify-room-information" v-model="modifiedRoom.information"></textarea>

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
import SeminarRoom from '@/assets/622---seminar-room.png';
import PartyCommitee from '@/assets/634---party-committee-meeting-room.png';
import MultipurposeTeachingRoom from '@/assets/635---multipurpose-teaching-room.png';
import EnglishRoom from '@/assets/english-room.png';
import FormalMeetingRoom from '@/assets/formal-meeting-room.png';
import InformMeetingRoom from '@/assets/informal-meeting-room.png';


export default {
  name: 'RoomManagement',
  data() {
    return {
      rooms: [
        {
          name: "622-Seminar Room",
          capacity: 50,
          location: "DIICSU Sixth Floor",
          equipment: ["Projector", "Whiteboard", "Microphone", "Power Outlets", "Wi-Fi"],
          access: "All",
          image: SeminarRoom
        },
        {
          name: "634-Party Committee Meeting Room",
          capacity: 10,
          location: "DIICSU Sixth Floor",
          equipment: ["Projector", "Wi-Fi"],
          access: "Selected Staff Only",
          image: PartyCommitee
        },
        {
          name: "635-Multipurpose Teaching Room",
          capacity: 20,
          location: "Building 3, Floor 3",
          equipment: ["Projector", "Microphone", "Computer", "Power Outlets", "Wi-Fi"],
          access: "All",
          image: MultipurposeTeachingRoom
        },
        {
          name: "English Room 101",
          capacity: 30,
          location: "DIICSU Groud Floor",
          equipment: ["Projector", "Microphone", "Computer", "Wi-Fi"],
          access: "All",
          image: EnglishRoom,
        },
        {
          name: "English Room 102",
          capacity: 30,
          location: "DIICSU Groud Floor",
          equipment: ["Projector", "Microphone", "Computer", "Wi-Fi"],
          access: "All",
          image: EnglishRoom,
        },
        {
          name: "English Room 103",
          capacity: 30,
          location: "DIICSU Groud Floor",
          equipment: ["Projector", "Microphone", "Computer", "Wi-Fi"],
          access: "All",
          image: EnglishRoom,
        }, {
          name: "English Room 104",
          capacity: 30,
          location: "DIICSU Groud Floor",
          equipment: ["Projector", "Microphone", "Computer", "Wi-Fi"],
          access: "All",
          image: EnglishRoom,
        }, {
          name: "English Room 105",
          capacity: 30,
          location: "DIICSU Groud Floor",
          equipment: ["Projector", "Microphone", "Computer", "Wi-Fi"],
          access: "All",
          image: EnglishRoom,
        }, {
          name: "English Room 106",
          capacity: 30,
          location: "DIICSU Groud Floor",
          equipment: ["Projector", "Microphone", "Computer", "Wi-Fi"],
          access: "All",
          image: EnglishRoom,
        }, {
          name: "English Room 107",
          capacity: 30,
          location: "DIICSU Groud Floor",
          equipment: ["Projector", "Microphone", "Computer", "Wi-Fi"],
          access: "All",
          image: EnglishRoom,
        }, {
          name: "English Room 108",
          capacity: 30,
          location: "DIICSU Groud Floor",
          equipment: ["Projector", "Microphone", "Computer", "Wi-Fi"],
          access: "All",
          image: EnglishRoom,
        },
        {
          name: "English Room 116",
          capacity: 30,
          location: "DIICSU Groud Floor",
          equipment: ["Projector", "Microphone", "Computer", "Wi-Fi"],
          access: "All",
          image: EnglishRoom,
        }, {
          name: "English Room 117",
          capacity: 30,
          location: "DIICSU Groud Floor",
          equipment: ["Projector", "Microphone", "Computer", "Wi-Fi"],
          access: "All",
          image: EnglishRoom,
        }, {
          name: "English Room 118",
          capacity: 30,
          location: "DIICSU Groud Floor",
          equipment: ["Projector", "Microphone", "Computer", "Wi-Fi"],
          access: "All",
          image: EnglishRoom,
        }, {
          name: "English Room 119",
          capacity: 30,
          location: "DIICSU Groud Floor",
          equipment: ["Projector", "Microphone", "Computer", "Wi-Fi"],
          access: "All",
          image: EnglishRoom,
        },
        {
          name: "Formal Meeting Room",
          capacity: 14,
          location: "DIICSU Groud Floor",
          equipment: ["Power Outlets", "Wi-Fi"],
          access: "Staff Only",
          image: FormalMeetingRoom,
        }, {
          name: "Informal Meeting Room",
          capacity: 14,
          location: "DIICSU Groud Floor",
          equipment: ["Wi-Fi"],
          access: "Staff Only",
          image: InformMeetingRoom,
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
        image: null
      },
      modifiedRoom: {
        index: null,
        name: "",
        capacity: 0,
        location: "",
        equipmentInput: "",
        image: null
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

    handleAddImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.newRoom.image = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },

    handleModifyImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.modifiedRoom.image = e.target.result;
        };
        reader.readAsDataURL(file);
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
    addRoom() {
      const equipment = this.newRoom.equipmentInput.split(',').map(item => item.trim());
      this.rooms.push({
        name: this.newRoom.name,
        capacity: this.newRoom.capacity,
        location: this.newRoom.location,
        equipment: equipment,
        access: this.newRoom.access,
        image: this.newRoom.image || roomAImage,
        information: this.newRoom.information
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
        access: this.rooms[index].access,
        image: this.rooms[index].image,
        information: this.rooms[index].information
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
        access: this.modifiedRoom.access,
        image: this.modifiedRoom.image,
        information: this.modifiedRoom.information
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
  height: 100vh;
  display: flex;
}

.container {
  flex: 1;
  display: flex;
  flex-direction: column;
  max-width: 1750px;
  margin: 20px auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #2c3e50;
  font-size: 3.5rem;
  margin-bottom: 10px;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 180px);
}

.admin-actions {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-end;
  padding-right: 20px;
}

.room-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 20px;
}

.room-items-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #eceef8;
  box-shadow: none;
}

.room-item {
  display: flex;
  height: 200px;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  overflow: hidden;
}

.room-image {
  height: 100%;
  width: 300px;
  flex-shrink: 0;
  border-radius: 20px 0 0 20px;
}

.room-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: inherit;
}

.room-info {
  flex: 1;
  padding: 15px 25px;
  min-width: 0;
}

.room-info > div {
  margin: 2px 0;
  line-height: 1.3;
}

.room-name {
  font-size: 1.5rem;
  font-weight: bold;
  color: #34495e;
  margin-bottom: 4px;
}

.room-information {
  font-size: 0.95rem;
  color: #666;
  margin-top: 6px;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 3.6em;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.room-actions {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0 20px;
  gap: 15px;
  flex-shrink: 0;
}


.add-button {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: #fff;
  color: #333;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.action-button,
.pagination-button {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: #fff;
  color: #333;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.add-button:hover:not(:disabled),
.action-button:hover:not(:disabled),
.pagination-button:hover:not(:disabled) {
  background: #3155ef;
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(49, 85, 239, 0.3);
}

.add-button:active:not(:disabled),
.action-button:active:not(:disabled),
.pagination-button:active:not(:disabled) {
  transform: translateY(0);
}

.pagination {
  position: sticky;
  bottom: 0;
  display: flex;
  justify-content: center;
  gap: 15px;
  padding: 15px 0;
  background: linear-gradient(to bottom,
  rgba(236, 238, 248, 0) 0%,
  rgba(236, 238, 248, 0.9) 30%,
  rgba(236, 238, 248, 1) 100%
  );
  z-index: 2;
}

.pagination-button {
  min-width: 100px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  padding: 30px;
  width: 450px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.modal-content label {
  font-weight: 600;
  color: #444;
}

.modal-content input,
.modal-content select,
.modal-content textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  width: 100%;
}

.modal-content textarea {
  height: 80px;
  resize: vertical;
}

/* disabled status */
button:disabled {
  background: #e0e0e0 !important;
  color: #a0a0a0 !important;
  cursor: not-allowed;
  box-shadow: none !important;
}

.image-preview {
  margin: 10px 0;
}

.preview-img {
  max-width: 200px;
  max-height: 150px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

input[type="file"] {
  padding: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #f8f9fa;
}
</style>
<template>
  <div class="panel">
    <div class="container">
      <h1>Room Management</h1>
      <div class="content-wrapper">
        <div class="admin-actions">
          <button @click="showAddRoomModal = true" class="add-button-container">Add Room</button>
        </div>
        <div class="room-list-container">
          <div class="room-items-container">
            <div
                v-for="(room, index) in paginatedRooms"
                :key="index"
                class="room-item"
            >
              <div class="room-image">
                <img :src="room.image_url" alt="Room Image" class="room-img"/>
              </div>
              <div class="room-info">
                <div class="room-name">{{ room.name }}</div>
                <div class="room-capacity">Capacity: {{ room.capacity }}</div>
                <div class="room-location">Location: {{ room.location }}</div>
                <div class="room-equipment">Equipment: {{ formatEquipment(room.equipment) }}</div>
                <div class="room-access">Access: {{ accessMap[room.access] }}</div>
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

        <!-- Add Room Modal -->
        <div v-if="showAddRoomModal" class="modal">
          <div class="modal-content">
            <h2>Add Room</h2>
            <form @submit.prevent="addRoom">
              <label for="room-name">Room Name:</label>
              <input type="text" id="room-name" v-model="newRoom.name" required/>

              <label for="room-capacity">Capacity:</label>
              <input type="number" id="room-capacity" v-model="newRoom.capacity" required min="0"/>

              <label for="room-location">Location:</label>
              <input type="text" id="room-location" v-model="newRoom.location" required/>

              <label>Equipment:</label>
              <div class="equipment-checkboxes">
                <label><input type="checkbox" v-model="newRoom.equipment.Projector"> Projector</label>
                <label><input type="checkbox" v-model="newRoom.equipment.Whiteboard"> Whiteboard</label>
                <label><input type="checkbox" v-model="newRoom.equipment.Microphone"> Microphone</label>
                <label><input type="checkbox" v-model="newRoom.equipment.Computer"> Computer</label>
                <label><input type="checkbox" v-model="newRoom.equipment.PowerOutlets"> Power Outlets</label>
                <label><input type="checkbox" v-model="newRoom.equipment.WiFi"> Wi-Fi</label>
              </div>

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
                  @change="handleImageUpload"
                  accept="image/*"
                  required
                  title="Select room image"
                  class="custom-file-input"
              >
              <div v-if="newRoom.image_url" class="image-preview">
                <img :src="newRoom.image_url" alt="Current Image" class="preview-img">
              </div>

              <label for="room-information">Information (optional):</label>
              <textarea id="room-information" v-model="newRoom.information"></textarea>
              <button type="submit" class="action-button">Add</button>
              <button @click="showAddRoomModal = false" class="action-button">Cancel</button>
            </form>
          </div>
        </div>

        <!-- Modify Room Modal -->
        <div v-if="showModifyRoomModal" class="modal">
          <div class="modal-content">
            <h2>Modify Room</h2>
            <form @submit.prevent="saveModifiedRoom">
              <label for="modify-room-name">Room Name:</label>
              <input type="text" id="modify-room-name" v-model="modifiedRoom.name" required/>

              <label for="modify-room-capacity">Capacity:</label>
              <input type="number" id="modify-room-capacity" v-model="modifiedRoom.capacity" required min="0"/>

              <label for="modify-room-location">Location:</label>
              <input type="text" id="modify-room-location" v-model="modifiedRoom.location" required/>

              <label>Equipment:</label>
              <div class="equipment-checkboxes">
                <label><input type="checkbox" v-model="modifiedRoom.equipment.Projector"> Projector</label>
                <label><input type="checkbox" v-model="modifiedRoom.equipment.Whiteboard"> Whiteboard</label>
                <label><input type="checkbox" v-model="modifiedRoom.equipment.Microphone"> Microphone</label>
                <label><input type="checkbox" v-model="modifiedRoom.equipment.Computer"> Computer</label>
                <label><input type="checkbox" v-model="modifiedRoom.equipment.PowerOutlets"> Power Outlets</label>
                <label><input type="checkbox" v-model="modifiedRoom.equipment.WiFi"> Wi-Fi</label>
              </div>

              <label for="modify-room-access">Access:</label>
              <select id="modify-room-access" v-model="modifiedRoom.access" required>
                <option value="0">All</option>
                <option value="1">Staff Only</option>
                <option value="2">Selected Staff Only</option>
              </select>

              <label for="modify-room-image">Image:</label>
              <input
                  type="file"
                  id="modify-room-image"
                  @change="handleImageUpload"
                  accept="image/*"
                  title="Select room image"
                  class="custom-file-input"
              >
              <div v-if="modifiedRoom.image_url" class="image-preview">
                <img :src="modifiedRoom.image_url" alt="Current Image" class="preview-img">
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
import {getCurrentInstance} from "vue";
import {ElMessage} from "element-plus";

export default {
  name: 'RoomManagement',
  setup() {
    const instance = getCurrentInstance()
    const backendAddress = instance.appContext.config.globalProperties.$backendAddress

    return {backendAddress}
  },
  data() {
    return {
      isModifying: false,
      accessMap: {
        0: "All",
        1: "Staff Only",
        2: "Selected Staff"
      },
      rooms: [],
      currentPage: 1,
      itemsPerPage: 3,
      showAddRoomModal: false,
      showModifyRoomModal: false,
      newRoom: {
        name: "",
        capacity: 0,
        location: "",
        equipment: {
          Projector: false,
          Whiteboard: false,
          Microphone: false,
          Computer: false,
          PowerOutlets: false,
          WiFi: false
        },
        image_url: null,
        access: "All",
        information: null,
      },

      //modifiedRoom
      modifiedRoom: {
        index: null,
        name: "",
        capacity: 0,
        location: "",
        equipment: {
          Projector: false,
          Whiteboard: false,
          Microphone: false,
          Computer: false,
          PowerOutlets: false,
          WiFi: false
        },
        image_url: null,
        access: "All",
        information: null,
      }
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
    }
  },
  methods: {
    formatEquipment(equipment) {
      if (typeof equipment === 'string') {
        const cleanedString = equipment.replace(/[{}]/g, '').replace(/'/g, '"');
        try {
          return JSON.parse(`[${cleanedString}]`).join(', ');
        } catch (error) {
          console.error('Failed to parse equipment:', error);
          return 'No equipment';
        }
      } else if (Array.isArray(equipment)) {
        return equipment.join(', ');
      } else {
        return 'No equipment';
      }
    },
    async fetchRoomData() {
      try {
        const response = await fetch(this.backendAddress + '/getRooms');
        const data = await response.json();
        this.rooms = data.data;
      } catch (error) {
        console.error('Error fetching room data:', error);
      }
    },
    async addRoom() {
      const equipment = Object.keys(this.newRoom.equipment)
          .filter(key => this.newRoom.equipment[key])
          .map(key => key.replace(/([A-Z])/g, ' $1').trim());


      const information = this.newRoom.information ? this.newRoom.information : null;
      const image_url = this.newRoom.image_url ? this.newRoom.image_url : null;
      const room = {
        name: this.newRoom.name,
        capacity: this.newRoom.capacity,
        location: this.newRoom.location,
        equipment: equipment,
        access: this.newRoom.access,
        image_url: image_url,
        information: information
      };

      try {
        const response = await fetch(this.backendAddress + '/rooms', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(room),
        });
        const data = await response.json();
        if (data.code === '000') {
          this.rooms.push(room);
          this.showAddRoomModal = false;
          this.resetNewRoom();
        }
      } catch (error) {
        console.error('Failed to add room:', error);
      }
      this.isModifying = false;
    },


    async modifyRoom(index) {
      const room = this.paginatedRooms[index];
      this.modifiedRoom = {
        id: room.id,
        name: room.name,
        capacity: room.capacity,
        location: room.location,
        equipment: {
          Projector: room.equipment.includes("Projector"),
          Whiteboard: room.equipment.includes("Whiteboard"),
          Microphone: room.equipment.includes("Microphone"),
          Computer: room.equipment.includes("Computer"),
          PowerOutlets: room.equipment.includes("Power Outlets"),
          WiFi: room.equipment.includes("Wi-Fi")
        },
        access: room.access,
        image_url: room.image_url,
        information: room.information
      };
      this.isModifying = true;
      this.showModifyRoomModal = true;
    },
    async saveModifiedRoom() {
      const equipment = Object.keys(this.modifiedRoom.equipment)
          .filter(key => this.modifiedRoom.equipment[key])
          .map(key => key.replace(/([A-Z])/g, ' $1').trim());

      const room = {
        name: this.modifiedRoom.name,
        capacity: this.modifiedRoom.capacity,
        location: this.modifiedRoom.location,
        equipment: equipment,
        access: this.modifiedRoom.access,
        image_url: this.modifiedRoom.image_url,
        information: this.modifiedRoom.information || null
      };
      console.log(this.modifiedRoom.id)
      try {
        const response = await fetch(this.backendAddress + `/rooms/${this.modifiedRoom.id}`, {
          method: 'PUT',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(room)
        });

        const data = await response.json();
        if (data.code === '000') {
          const index = this.rooms.findIndex(r => r.id === this.modifiedRoom.id);
          if (index !== -1) {
            this.rooms.splice(index, 1, {...this.rooms[index], ...room});
          }
          this.showModifyRoomModal = false;
          this.resetNewRoom();
        }
      } catch (error) {
        console.error('Failed to modify room:', error);
      }
    },


    async deleteRoom(index) {
      const room = this.paginatedRooms[index];

      if (confirm("Are you sure you want to delete this room?")) {
        const roomId = room.id;

        try {
          const response = await fetch(this.backendAddress + `/rooms/${roomId}`, {
            method: 'DELETE',
          });
          const data = await response.json();
          if (data.code === '000') {
            const roomIndex = this.rooms.findIndex(r => r.id === roomId);
            if (roomIndex !== -1) {
              this.rooms.splice(roomIndex, 1);
            }
            if (this.paginatedRooms.length === 0 && this.currentPage > 1) {
              this.currentPage--;
            }
          }
        } catch (error) {
          console.error('Failed to delete room:', error);
        }
      }
    },
    async handleImageUpload(event) {
      const file = event.target.files[0];
      if (!file) {
        ElMessage.info("Please select an image to upload");
        return;
      }
      const maxFileSize = 5 * 1024 * 1024;
      if (file.size > maxFileSize) {
        ElMessage.info("The max size is 5MB");
        return;
      }
      const creds = [
        {uid: "af7c509daf8264c6f539e62ad1a63fbd", token: "0ee94f5bd8b1a55cddf0e1a5d5436785"},
        {uid: "88ebf0e92847f83dc9689aea7dfe9d1c", token: "805d0aaaed73724e435a7a727743090e"},
        {uid: "a5d81acf270ad077b4f29d855f9354d4", token: "4d832654bdb2b770d86dda48224cfe7f"},
        {uid: "7a55ae3d265f33da6ec8efbf90759e71", token: "02a6e7d8831ace26ec97bb66a2df5968"},
        {uid: "4fd9e5610b0e525238740a52d529a0ab", token: "8672bd62f6f14e80dd95e536b7ccea04"}
      ];
      for (let i = 0; i < creds.length; i++) {
        const formData = new FormData();
        formData.append("uid", creds[i].uid);
        formData.append("token", creds[i].token);
        formData.append("file", file);

        try {
          // post request
          const response = await fetch("https://www.imgurl.org/api/v2/upload", {
            method: "POST",
            body: formData,
          });

          // response handling
          const result = await response.json();

          console.log(result);
          console.log(result.code);

          if (result.code === 200) {
            const image_url = result.data.url;
            if (this.isModifying) {
              this.modifiedRoom.image_url = image_url;
            } else {
              this.newRoom.image_url = image_url;
            }
            ElMessage.success("Upload successful!");
            console.log("Image URL:", image_url);
            return; // stop once it succeeds
          }

          // '今日上传数量上限！' means that an account has reached its maximum number of uploads
          // As the API is from a Chinese website, so the return message must be used in Chinese in the code.
          if (result.code === -1000 && result.msg === '今日上传数量上限！') {
            console.log(`Account ${i + 1} limit reached — switching credentials`);
            continue;
          }
          ElMessage.error(`Error uploading image: ${result.msg || "Unknown error"}`);
          return;
        } catch (error) {
          ElMessage.error("Upload failed, please check network connection");
          return;
        }
      }
      ElMessage.info("All accounts have reached today's upload limit.");
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
    resetNewRoom() {
      this.newRoom = {
        name: "",
        capacity: 0,
        location: "",
        equipment: {
          Projector: false,
          Whiteboard: false,
          Microphone: false,
          Computer: false,
          PowerOutlets: false,
          WiFi: false
        },
        image_url: null,
        access: "All",
        information: null,
      };
    },
  },
  mounted() {
    this.fetchRoomData();
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
  font-family: 'Cambria', serif;
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
  margin-bottom: 10px;
  display: flex;
  justify-content: flex-end;
  padding-right: 20px;
}

.room-list-container {
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


.add-button-container {
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

.add-button-container:hover:not(:disabled),
.action-button:hover:not(:disabled),
.pagination-button:hover:not(:disabled) {
  background: #3155ef;
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(49, 85, 239, 0.3);
}

.add-button-container:active:not(:disabled),
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
  background: #eceef8;
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

.equipment-checkboxes {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: flex-start;
  margin-bottom: 15px;
}

.equipment-checkboxes label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.95rem;
  color: #444;
  white-space: nowrap;
}

</style>
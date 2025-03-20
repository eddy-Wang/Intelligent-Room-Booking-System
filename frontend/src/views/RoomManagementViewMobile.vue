<template>
  <div class="mobile-panel">
    <div class="container">
      <div class="title-container">
      <h1><strong>DRBS</strong></h1>
      <h2><strong>Room Management</strong></h2>
    </div>
      <div class="content-wrapper">
        <button @click="showAddRoomModal = true" class="add-button">Add Room</button>

        <div class="room-list">
          <div
            v-for="(room, index) in rooms"
            :key="index"
            class="room-item"
          >
            <div class="room-image">
              <img :src="room.image_url" alt="Room" class="room-img"/>
            </div>

            <div class="room-info">
              <div class="room-name">{{ room.name }}</div>
              <div class="room-meta">
                <div>Capacity: {{ room.capacity }}</div>
                <div>Location: {{ room.location }}</div>
                <div>Access: {{ accessMap[room.access] }}</div>
              </div>
              <div class="room-equipment">Equipment: {{ formatEquipment(room.equipment) }}</div>
              <div class="room-information">{{ room.information || 'No additional info' }}</div>
            </div>

            <div class="room-actions">
              <button @click="modifyRoom(index)" class="action-button">Edit</button>
              <button @click="deleteRoom(index)" class="action-button delete">Delete</button>
            </div>
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
              <input type="number" id="room-capacity" v-model="newRoom.capacity" required/>

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
              <div class="room-actions">
                <button type="submit" class="action-button">Add</button>
                <button @click="showAddRoomModal = false" class="action-button">Cancel</button>
          
              </div>
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
              <input type="number" id="modify-room-capacity" v-model="modifiedRoom.capacity" required/>

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
              <div class="room-actions">
                <button type="submit" class="action-button">Save</button>
                <button @click="showModifyRoomModal = false" class="action-button">Cancel</button>
            
              </div>
              </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MobileRoomManagement',
  data() {
    return {
      rooms: [],
      isModifying: false,
      showAddRoomModal: false,
      showModifyRoomModal: false,
      accessMap: {
        0: "All",
        1: "Staff Only",
        2: "Selected Staff"
      },
      newRoom: {
        name: "",
        capacity: "",
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
        const response = await fetch('http://127.0.0.1:8080/getRooms');
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
        const response = await fetch('http://127.0.0.1:8080/rooms', {
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
      const room = this.rooms[index];
      console.log(room)
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
        const response = await fetch(`http://127.0.0.1:8080/rooms/${this.modifiedRoom.id}`, {
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
      const room = this.rooms[index];

      if (confirm("Are you sure you want to delete this room?")) {
        const roomId = room.id;

        try {
          const response = await fetch(`http://127.0.0.1:8080/rooms/${roomId}`, {
            method: 'DELETE',
          });
          const data = await response.json();
          if (data.code === '000') {
            const roomIndex = this.rooms.findIndex(r => r.id === roomId);
            if (roomIndex !== -1) {
              this.rooms.splice(roomIndex, 1);
            }
            alert("Room deleted successfully")
          }
        } catch (error) {
          console.error('Failed to delete room:', error);
        }
      }
    },
    async handleImageUpload(event) {
      const file = event.target.files[0];
      if (!file) {
        alert("Please select an image to upload");
        return;
      }
      const maxFileSize = 5 * 1024 * 1024;
      if (file.size > maxFileSize) {
        alert("The max size is 5MB");
        return;
      }

      const formData = new FormData();
      formData.append("uid", "af7c509daf8264c6f539e62ad1a63fbd"); // UID
      formData.append("token", "0ee94f5bd8b1a55cddf0e1a5d5436785"); // Token
      formData.append("file", file); // image file

      try {
        // post request
        const response = await fetch("https://www.imgurl.org/api/v2/upload", {
          method: "POST",
          body: formData,
        });

        // response handling
        const result = await response.json();
        console.log(result)
        console.log(result.code)
        if (result.code === 200) {
          const image_url = result.data.url;
          if (this.isModifying) {
            this.modifiedRoom.image_url = image_url;
          } else {
            this.newRoom.image_url = image_url;
          }
          alert("upload successfully");
          this.newRoom.image_url = image_url;
          console.log(this.newRoom.image_url)
          alert("upload successfully");
        } else {
          alert(`error：${result.message || "unknown error"}`);
        }
      } catch (error) {
        alert("Upload failed, please check network connection");
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
  }
};
</script>

<style scoped>
.mobile-panel {
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

.add-button {
  margin: 20px 0;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: #3155ef;
  color: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.action-button {
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
.action-button:hover:not(:disabled){
  background: #3155ef;
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(49, 85, 239, 0.3);
}

.add-button:active:not(:disabled),
.action-button:active:not(:disabled) {
  transform: translateY(0);
}


.content-wrapper {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

body {
  font-family: 'Cambria', serif;
}

.room-list {
  display: grid;
  gap: 15px;
  margin-bottom: 50px;
}

.room-item {
  background: #fff;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.room-image {
  width: 100%;
  height: 200px;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 12px;
}

.room-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.room-info > div {
  margin: 6px 0;
  font-size: 14px;
}

.room-name {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.room-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  color: #666;
}

.room-equipment {
  color: #4a5568;
  font-size: 13px;
}

.room-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.action-button {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
}

.delete {
  background: #fef2f2;
  color: #dc2626;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  padding: 15px;
}

.modal-content {
  background: white;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 20px;
  border-radius: 12px;
}

input, select, textarea {
  width: 100%;
  padding: 12px;
  margin: 8px 0;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
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

.equipment-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin: 10px 0;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.confirm, .cancel {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-weight: 500;
}

.confirm {
  background: #3b82f6;
  color: white;
}

.cancel {
  background: #f1f5f9;
  color: #64748b;
}

.image-upload input {
  padding: 0;
  border: none;
}

.image-preview img {
  width: 100%;
  max-height: 150px;
  object-fit: cover;
  border-radius: 8px;
  margin-top: 10px;
}
</style>
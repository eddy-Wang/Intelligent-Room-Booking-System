<!--
RoomRepair.vue - Component for reporting equipment issues in rooms.

Features:
- Displays list of rooms with images
- Allows users to report equipment issues
- Modal form for submitting repair requests
- Responsive grid layout
- User authentication integration

Props: None
Events: None
Dependencies:
- Element Plus for notifications
- Vue 3 Composition API
-->
<template>
  <!-- Main container -->
  <div class="container">
    <h1 class="title">Room Equipment Repair</h1>

    <div class="room-list-container">
      <div v-for="room in rooms" :key="room.id" class="room-card">
        <img :src="room.image_url" alt="Room Image" class="room-image">
        <h2 class="room-name">{{ room.name }}</h2>
        <div class="button-container">
          <button @click="openRepairDialog(room)" class="report-button">Report Issue</button>
        </div>

      </div>
    </div>
    <!-- Repair report modal dialog -->
    <div v-if="showDialog" class="modal-overlay">
      <div class="modal">
        <h2 class="modal-title">Report Issue for {{ selectedRoom?.name }}</h2>
        <label class="input-label">Issue Description:</label>
        <textarea v-model="reportInfo" class="input-field textarea" placeholder="Describe the issue here"></textarea>

        <div class="button-group">
          <button @click="showDialog = false" class="cancel-button">Cancel</button>
          <button @click="submitRepair" class="save-button">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {getCurrentInstance, onMounted, ref} from "vue";
import {ElMessage} from "element-plus";
/**
 * Component initialization
 */
const instance = getCurrentInstance()
const backendAddress = instance.appContext.config.globalProperties.$backendAddress

// Reactive data properties
const rooms = ref([]); // Array to store room data
const showDialog = ref(false); // Controls modal visibility
const selectedRoom = ref(null); // Currently selected room for reporting
const reportInfo = ref(""); // User's issue description
const userEmail = ref(""); // Logged-in user's email
const userPermission = ref(""); // User's permission level

/**
 * Fetches room data from backend API
 * @async
 */
const fetchRoomData = async () => {
  try {
    const response = await fetch(backendAddress+"/getRooms");
    const data = await response.json();
    rooms.value = data.data;
  } catch (error) {
    console.error("Error fetching room data:", error);
  }
};
/**
 * Opens the repair dialog for a specific room
 * @param {Object} room - The room to report issues for
 */
const openRepairDialog = (room) => {
  selectedRoom.value = room;
  showDialog.value = true;
  reportInfo.value = "";
};
/**
 * Submits a repair request to the backend
 * @async
 */
const submitRepair = async () => {
      if (!reportInfo.value) {
        alert("Please fill in report information!");
        return;
      }

      const repairData = {
        room_id: selectedRoom.value.id,
        user_email: userEmail.value,
        report_info: reportInfo.value,
        user_permission: userPermission.value,
      };

      console.log("Repair data:", repairData);
      try {
        const response = await fetch(backendAddress+"/room_issue", {
          method: "PUT",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify(repairData),
        });
        if (response.ok) {
          const data = await response.json();
          if (data.code === "000") {
            ElMessage.success("Repair request submitted successfully!");
            showDialog.value = false;
          } else {
            ElMessage.error("Failed to submit repair request: " , data.message);
          }
        } else {
          ElMessage.error("There is a problem with the network, please try again.");
        }
      } catch (error) {
        console.error("Error submitting repair:", error);
        ElMessage.error("Error submitting repair:", error);
      }
    }
;
/**
 * Component mounted lifecycle hook
 * Fetches initial data and user information
 */
onMounted(async () => {
  let me = await instance.appContext.config.globalProperties.$me()
  let user = me.data
  userEmail.value = user.email
  userPermission.value = user.permission
  await fetchRoomData()
});
</script>

<style scoped>
/* Main container styling */
.container {
  font-family: 'Cambria', serif;
  padding: 20px;
  background-color: #F5F6FA;
  height: 100vh;
}
/* Page title styling */
.title {
  font-size: 58px;
  font-weight: bold;
  text-align: left;
  color: #222;
  height: 12%;
}

/* Responsive room grid container */
.room-list-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 50px;
  height: 88%;
  overflow-y: auto;
  padding-right: 20px;
  margin: 30px;
}
/* Individual room card styling */
.room-card {
  background-color: #ECEEF8;
  border-radius: 30px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease-in-out;
  min-height: 500px;
  min-width: 270px;
  display: flex;
  flex-direction: column;
}

.room-card:hover {
  transform: translateY(-5px);
}

.room-image {
  flex-grow: 1;
  height: 60%;
  width: 100%;
  object-fit: cover;
}

.room-name {
  margin: 15px 0 0 0;
  font-size: 20px;
  font-weight: bold;
  color: #333;
  width: 100%;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.button-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 16%;
}

.report-button {
  width: 110px;
  font-size: 16px;
  background-color: #4064fd;
  color: white;
  padding: 6px;
  border-radius: 10px;
  cursor: pointer;
  border: none;
  transition: background 0.2s;
}

.report-button:hover {
  background-color: #3155ef;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: white;
  padding: 24px;
  border-radius: 10px;
  width: 400px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.modal-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #222;
}

.input-label {
  display: block;
  font-size: 14px;
  margin-bottom: 5px;
  color: #666;
}

.input-field {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  margin-bottom: 15px;
}

.textarea {
  height: 80px;
  resize: none;
}

/* 按钮组 */
.button-group {
  display: flex;
  justify-content: space-between;
}

.cancel-button {
  background: #bbb;
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

.cancel-button:hover {
  background: #999;
}

.save-button {
  background: #2D6EF7;
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

.save-button:hover {
  background: #1A52D8;
}
</style>
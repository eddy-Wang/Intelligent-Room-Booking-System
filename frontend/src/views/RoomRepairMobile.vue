<template>
  <div class="home-container">
    <div class="title-container">
      <h1><strong>DRBS</strong></h1>
      <h2><strong>Room Equipment Repair</strong></h2>
    </div>

    <div class="search-container">
      <input type="text" v-model="searchQuery" placeholder="Search a room..."/>
    </div>

    <div class="rooms-container">
      <div
          v-for="room in filteredRooms"
          :key="room.id"
          class="room-card"
          :class="{ selected: selectedRoom && selectedRoom.id === room.id }"
      >
        <div class="room-image">
          <img :src="room.image" :alt="room.name"/>
        </div>
        <div class="room-details">
          {{ room.name }}
        </div>
        <button class="repair-button" @click.stop="openRepairDialog(room)">Report</button>
      </div>
    </div>

    <div v-if="showRepairDialog" class="modal-overlay" @click="closeRepairDialog">
      <div class="modal-container" @click.stop>
        <h3>Repair: {{ selectedRoom ? selectedRoom.name : '' }}</h3>
        <input
            type="text"
            v-model="repairDescription"
            placeholder="Repair equipment description"
            class="repair-input"
        />
        <button
            :class="{ active: repairDescription.trim().length > 0 }"
            class="submit-repair-button"
            @click="submitRepair"
        >
          Submit
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, computed, getCurrentInstance} from 'vue';
import axios from 'axios';
import {ElMessage} from "element-plus";

const instance = getCurrentInstance()
const backendAddress = instance.appContext.config.globalProperties.$backendAddress

const selectedRoom = ref(null);
const roomsData = ref([]);
const searchQuery = ref('');
const showRepairDialog = ref(false);
const repairDescription = ref('');

const filteredRooms = computed(() => {
  const query = searchQuery.value.toLowerCase().replace(/\s+/g, '');
  return roomsData.value.filter(room => {
    const roomName = room.name.toLowerCase().replace(/\s+/g, '');
    return roomName.includes(query);
  });
});

onMounted(async () => {
  try {
    const response = await axios.get(backendAddress+'/allRoom', {
      params: {permission: instance.appContext.config.globalProperties.$user.permission}
    });
    if (response.data.code === '001') {
      roomsData.value = response.data.data.map(room => ({
        ...room,
        image: getRoomImage(room)
      }));
    } else {
      console.error(response.data.message);
    }
  } catch (error) {
    console.error('Error fetching rooms:', error);
  }
});

function getRoomImage(room) {
  switch (room.id) {
    case 1:
      return new URL('@/assets/622---seminar-room.png', import.meta.url).href;
    case 2:
      return new URL('@/assets/room1.png', import.meta.url).href;
    case 3:
      return new URL('@/assets/635---multipurpose-teaching-room.png', import.meta.url).href;
    case 16:
      return new URL('@/assets/formal-meeting-room.png', import.meta.url).href;
    case 17:
      return new URL('@/assets/informal-meeting-room.png', import.meta.url).href;
    default:
      return new URL('@/assets/english-room.png', import.meta.url).href;
  }
}

function openRepairDialog(room) {
  selectedRoom.value = room;
  repairDescription.value = ''; // 每次打开时重置输入内容
  showRepairDialog.value = true;
}

function closeRepairDialog() {
  showRepairDialog.value = false;
}

async function submitRepair() {
  if (repairDescription.value.trim().length === 0) {
    ElMessage.info("Please enter repair description.");
    return;
  }

  const repairData = {
    room_id: selectedRoom.value.id,
    user_email: instance.appContext.config.globalProperties.$user.email,
    report_info: repairDescription.value,
    user_permission: instance.appContext.config.globalProperties.$user.permission
  };

  try {
    const response = await axios.put(backendAddress+'/room_issue', repairData, {
      headers: {'Content-Type': 'application/json'}
    });

    if (response.data.code === "000") {
      ElMessage.success("Repair request submitted successfully!");
      showRepairDialog.value = false;
    } else {
      ElMessage.error(response.data.message);
    }
  } catch (error) {
    console.error("Error submitting repair:", error);
    ElMessage.error("Error submitting repair.");
  }
}
</script>

<style scoped>
.home-container {
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

.search-container {
  width: 100%;
  background-color: #fff;
  border-radius: 20px;
  height: 30px;
  display: flex;
  align-items: center;
  padding: 0 10px;
  margin: 16px 0;
}

.search-container input {
  border: none;
  outline: none;
  width: 100%;
  font-size: 14px;
}

.rooms-container {
  background: #eceef8;
  width: 100%;
  margin: 0 auto 50px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.room-card {
  position: relative;
  height: 240px;
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
}

.room-image {
  height: 60%;
  background-color: #eceef8;
}

.room-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.room-details {
  min-height: 2.4em;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.9rem;
  color: #333;
  margin: 10px 5px 8px 5px;
  text-align: center;
}

.repair-button {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  border: none;
  border-radius: 10px;
  background-color: #3155ef;
  color: #fff;
  padding: 5px 10px;
  cursor: pointer;
  font-size: 0.9rem;
  width: 50%;
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
  z-index: 1000;
}

.modal-container {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.repair-input {
  background-color: #fdf8f6;
  border: 1px solid #ccc;
  padding: 8px;
  border-radius: 5px;
  width: 100%;
  font-size: 0.9rem;
}

.submit-repair-button {
  border: none;
  border-radius: 5px;
  padding: 10px;
  font-size: 0.9rem;
  color: #fff;
  background-color: #a6a6a6;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-repair-button.active {
  background-color: #3155ef;
}
</style>

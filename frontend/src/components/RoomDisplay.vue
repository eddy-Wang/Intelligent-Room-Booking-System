<template>
  <div class="room-display" @mousemove="handleMouseMove" @mouseleave="stopAutoScroll">
    <div class="rooms-container" :style="{ transform: `translateX(${scrollPosition}%)` }">
      <template v-if="filteredRooms.length > 0">
        <div
            v-for="room in filteredRooms"
            :key="room.id"
            class="room-card"
            :class="{ 'selected': selectedRoom && selectedRoom.id === room.id }"
            @click="handleRoomClick(room)"
        >
          <div class="room-image">
            <img :src="room.image_url" :alt="room.name"/>
          </div>
          <div class="room-name"><strong>{{ room.name }}</strong></div>
        </div>
      </template>
      <div v-else class="placeholder">
        No rooms available.
      </div>
    </div>

    <transition name="slide">
      <div
          v-if="selectedRoom"
          class="room-info"
          @click.stop
      >
        <div class="room-header">
          <h2 class="room-title">{{ selectedRoom.name }}</h2>
          <button class="close-btn" @click="resetSelection">×</button>
        </div>

        <div class="room-details">
          <div class="detail-item">
            <span class="label">Capacity: </span>
            <span class="value">{{ selectedRoom.capacity }}</span>
          </div>

          <div class="detail-item">
            <span class="label">Equipment: </span>
            <div class="equipment-list">
              <div
                  class="equipment-item"
                  v-for="equipment in parsedEquipment"
                  :key="equipment"
              >
                <span class="equipment-icon">{{ getEquipmentIcon(equipment) }}</span>
                <span class="equipment-name">{{ equipment }}</span>
              </div>
            </div>
          </div>

          <div class="detail-item">
            <span class="label">Access: </span>
            <span class="value">{{ accessMap[selectedRoom.access] }}</span>
          </div>
        </div>

        <div
            v-if="selectedRoom.report && selectedRoom.report.length > 0"
            class="warning-container"
        >
          <div class="warning-item">
            <span class="warning-title">⚠️ Warnings:  </span>
            <span class="warning-message">{{ selectedRoom.report[0] }}</span>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import {ref, computed, watch, inject} from 'vue'

const props = defineProps({
  roomIds: {
    type: Array,
    required: true,
    default: () => []
  },
  rooms: {
    type: Array,
    required: true,
    default: () => []
  }
})
const getEquipmentIcon = (equipment) => {
  const icons = {
    'Power Outlets': '🔌',
    'Projector': '📽️',
    'Microphone': '🎤',
    'Computer': '💻',
    'Whiteboard': '📝',
    'Wi-Fi': '📶'
  };
  return icons[equipment] || '✨';
}
const parsedEquipment = computed(() => {
  if (!selectedRoom.value || !selectedRoom.value.equipment) {
    return [];
  }
  return selectedRoom.value.equipment
      .replace(/[{}']/g, '')
      .split(',')
      .map(item => item.trim())
      .filter(item => item);
});

const accessMap = ref({
  0: "All",
  1: "Staff Only",
  2: "Selected Staff"
});
const filteredRooms = computed(() => {
  return props.rooms.filter(room => props.roomIds.includes(room.id))
})
const shouldScroll = computed(() => {
  return filteredRooms.value.length > 3
})

const scrollPosition = ref(0)
const isScrolling = ref(false)
const scrollSpeed = ref(0)
const selectedRoom = ref(null)

const emit = defineEmits(['roomSelected'])

const handleRoomClick = (room) => {
  const index = filteredRooms.value.findIndex(r => r.id === room.id)

  scrollPosition.value = -index * 38;
  selectedRoom.value = room

  isScrolling.value = false
  emit('roomSelected', room)
}

const handleMouseMove = (e) => {
  if (selectedRoom.value || !shouldScroll.value) return;

  const container = e.currentTarget;
  const containerRect = container.getBoundingClientRect();
  const mouseX = e.clientX - containerRect.left;
  const containerCenter = containerRect.width / 2;

  const distanceRatio = (mouseX - containerCenter) / containerCenter;

  const sensitivity = 0.1;
  const maxScrollSpeed = 0.2;

  scrollSpeed.value = -distanceRatio * sensitivity * maxScrollSpeed;

  if (Math.abs(distanceRatio) > 0.8) {
    isScrolling.value = true;
    updateScroll();
  } else {
    isScrolling.value = false;
  }
};

const updateScroll = () => {
  if (!isScrolling.value) return

  scrollPosition.value += scrollSpeed.value
  const cardWidthPercent = 37.2;
  const totalCardsWidthPercent = filteredRooms.value.length * (cardWidthPercent)
  const maxScrollPercent = 100 - totalCardsWidthPercent;

  scrollPosition.value = Math.max(Math.min(0, scrollPosition.value), maxScrollPercent);

  if (isScrolling.value) {
    requestAnimationFrame(updateScroll)
  }
}
const resetSelection = () => {
  selectedRoom.value = null
  scrollPosition.value = 0
  emit('room-unselected')
}

const stopAutoScroll = () => {
  if (selectedRoom.value) return
  isScrolling.value = false
  scrollPosition.value = 0
}
watch(filteredRooms, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    resetSelection()
  }
})
</script>

<style scoped>
.room-info {
  position: absolute;
  left: 33.5%;
  width: 66.5%;
  height: 88%;
  background: white;
  border-radius: 12px;
  padding-left: 20px;
  padding-top: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.room-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.room-title {
  color: #2c3e50;
  font-size: 1.3rem;
  margin: 0;
  font-weight: 600;
}

.close-btn {
  position: absolute;
  top: 43%;
  right: 15px;
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
}

.close-btn:hover {
  color: #e74c3c;
  transform: scale(1.2);
}

.room-details {
  flex: 1;
}

.detail-item {
  margin-bottom: 8px;
  display: flex;
  flex-wrap: wrap;
}

.label {
  font-weight: 600;
  color: #34495e;
  min-width: 80px;
  align-content: center;
}

.value {
  color: #2c3e50;
}

.equipment-list {
  display: flex;
  flex-direction: row;
  gap: 8px;
  margin-left: 16px;
}

.equipment-item {
  display: flex;
  background-color: #f8f9fa;
  padding: 6px 7px;
  border-radius: 8px;
  font-size: 1rem;
}

.equipment-icon {
  margin-right: 7px;
  font-size: 1rem;
}

.equipment-name {
  color: #34495e;
  align-content: center;
}

.warning-container {
  background-color: #fff8e1;
  border-left: 4px solid #f39c12;
  padding-left: 16px;
  border-radius: 8px;
  width: 90%;
  margin-bottom: 10px;
}

.warning-item {
  display: flex;
  margin-top: 12px;
  margin-bottom: 12px;
  align-items: baseline;
}

.warning-title {
  font-weight: 600;
  min-width: 110px;
  color: #34495e;
}

.warning-message {
  color: #e67e22;
  flex: 1;
}

.room-display {
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
  display: flex;
  padding: 16px 0 16px 0;
}

.rooms-container {
  background: #eceef8;
  width: 100%;
  height: 100%;
  max-width: 89%;
  margin: auto 0;
  display: flex;
  gap: 2%;
  position: relative;
  transition: transform 0.3s ease-out;
}

.room-card {
  width: 36%;
  height: 100%;
  flex-shrink: 0;
  border-radius: 12px;
  overflow: hidden;
  background: #eceef8;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease;
}

.room-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.room-image {
  width: 100%;
  height: 80%;
  overflow: hidden;
}

.room-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.room-name {
  padding: 10px;
  height: 100%;
  text-align: center;
  font-size: 16px;
  color: #333;
  font-weight: 500;
  background: #d5ddff;
}

.placeholder {
  width: 100%;
  height: 100%;
  text-align: center;
  font-size: 18px;
  color: #666;
  padding: 108px;
  background: #eceef8;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

</style>
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
        <h2>{{ selectedRoom.name }}</h2>
        <p>Capacity: {{ selectedRoom.capacity }}</p>
        <p>Equipment: {{ selectedRoom.equipment }}</p>
        <p>Access: {{  accessMap[selectedRoom.access] }}</p>
        <div v-if="selectedRoom.report && selectedRoom.report.length > 0" class="warning-messages">
          <div class="warning-message" v-for="(warning, index) in selectedRoom.report" :key="index">
            Warning {{ index + 1 }}: {{ warning }}
          </div>
        </div>
        <button class="close-btn" @click="resetSelection">×</button>
      </div>
    </transition>
  </div>
</template>

<script setup>
import {ref, computed, watch} from 'vue'

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

.room-info {
  position: absolute;
  left: 33.5%;
  width: 66.5%;
  height: 90%;
  background: white;
  border-radius: 12px;
  padding: 10px 20px 10px 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 2;
  overflow-y: auto;
}

.warning-message {
  color: red;
  background-color: #ffe6e6;
  padding: 10px;
  border: 1px solid red;
  border-radius: 5px;
  margin-top: 0.8%;
  height: 20%;
  max-width: 90%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.room-display {
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
  background: #eceef8;
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


@media (max-width: 768px) {
  .room-card {
    min-width: 280px;
  }
}

</style>
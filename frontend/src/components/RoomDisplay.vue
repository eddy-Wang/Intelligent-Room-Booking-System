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
            <img :src="getImagePath(room.name)" :alt="room.name" />
          </div>
          <div class="room-name"><strong>{{ room.name }}</strong></div>
        </div>
      </template>
      <div v-else class="placeholder" >
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
        <p>Access: {{ selectedRoom.access }}</p>
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
const getImagePath = (name) => {
  if (name.startsWith("English Room")) {
    return new URL(`../assets/english-room.png`, import.meta.url).href;
  } else {
    const fileName = name.toLowerCase().replace(/\s+/g, '-');
    return new URL(`../assets/${fileName}.png`, import.meta.url).href;
  }
}
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
  top: 100px;
  right: 15px;
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
}

.room-info {
  position: absolute;
  left: 34.5%;
  width: 65%;
  height: 90%;
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 2;
}

.room-display {
  width: 100%;
  height: 100% ;
  overflow: hidden;
  position: relative;
  background: #eceef8;
  display: flex;
  padding: 16px;
}

.rooms-container {
  background: #eceef8;
  width: 100%;
  height: 100%;
  max-width: 90%;
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
  height: 200px;
  overflow: hidden;
}

.room-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.room-name {
  padding: 10px;
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
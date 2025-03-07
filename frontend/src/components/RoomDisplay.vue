<template>
  <div class="room-display" @mousemove="handleMouseMove" @mouseleave="stopAutoScroll">
    <div class="edge-mask left"></div>
    <div class="edge-mask right"></div>

    <div class="rooms-container" :style="{ transform: `translateX(${scrollPosition}px)` }">
      <div
          v-for="room in filteredRooms"
          :key="room.id"
          class="room-card"
          :class="{ 'selected': selectedRoom && selectedRoom.id === room.id }"
          @click="handleRoomClick(room)"
      >
        <div class="room-image">
          <img :src="room.image" :alt="room.name">
        </div>
        <div class="room-name">{{ room.name }}</div>
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
        <p>Equipment: {{ selectedRoom.equipment.join(', ') }}</p>
        <p>Access: {{ selectedRoom.access }}</p>
        <button class="close-btn" @click="resetSelection">×</button>
      </div>
    </transition>

  </div>
</template>

<script setup>
import {ref, onMounted, computed} from 'vue'

const props = defineProps({
  roomIds: {
    type: Array,
    required: true,
    default: () => []
  }
})

const filteredRooms = computed(() => {
  return rooms.value.filter(room => props.roomIds.includes(room.id))
})

const rooms = ref([
  {
    id: 1,
    name: 'Informal Meeting Room',
    image: new URL('@/assets/room1.png', import.meta.url).href,
    capacity: '15-30',
    equipment: ['Projector', 'Whiteboard', 'Power Outlets', 'Wi-Fi'],
    access: 'All'
  },
  {
    id: 2,
    name: 'Formal Meeting Room',
    image: new URL('@/assets/room1.png', import.meta.url).href,
    capacity: '30-45',
    equipment: ['Projector', 'Whiteboard', 'Computers', 'Wi-Fi'],
    access: 'Staff Only'
  },
  {
    id: 3,
    name: '635',
    image: new URL('@/assets/2.png', import.meta.url).href,
    capacity: '15-30',
    equipment: ['Whiteboard', 'Power Outlets', 'Wi-Fi'],
    access: 'All'
  },
  {
    id: 4,
    name: 'English Corridor',
    image: new URL('@/assets/room1.png', import.meta.url).href,
    capacity: '15-30',
    equipment: ['Whiteboard', 'Power Outlets', 'Wi-Fi'],
    access: 'All'
  }, {
    id: 5,
    name: 'Seminar Room',
    image: new URL('@/assets/room1.png', import.meta.url).href,
    capacity: '15-30',
    equipment: ['Whiteboard', 'Power Outlets', 'Wi-Fi'],
    access: 'All'
  }
])

const scrollPosition = ref(0)
const isScrolling = ref(false)
const scrollSpeed = ref(0)
const selectedRoom = ref(null)

const emit = defineEmits(['roomSelected'])

const handleRoomClick = (room) => {
  const index = filteredRooms.value.findIndex(r => r.id === room.id)
  scrollPosition.value = -index * 340
  selectedRoom.value = room

  isScrolling.value = false
  emit('roomSelected', room)
}
const handleMouseMove = (e) => {
  if (selectedRoom.value) return
  const container = e.currentTarget
  const containerRect = container.getBoundingClientRect()
  const mouseX = e.clientX - containerRect.left
  const containerCenter = containerRect.width / 2

  const distance = mouseX - containerCenter

  if (Math.abs(distance) > 150) {
    scrollSpeed.value = -(distance / containerRect.width) * 8
    isScrolling.value = true
    updateScroll()
  } else {
    isScrolling.value = false
  }
}

const updateScroll = () => {
  if (!isScrolling.value) return

  scrollPosition.value += scrollSpeed.value
  const maxScroll = -((rooms.value.length - 3) * 340)
  scrollPosition.value = Math.max(Math.min(0, scrollPosition.value), maxScroll)

  if (isScrolling.value) {
    requestAnimationFrame(updateScroll)
  }
}

const resetSelection = () => {
  selectedRoom.value = null
  scrollPosition.value = 0
}

const stopAutoScroll = () => {
  if (selectedRoom.value) return
  isScrolling.value = false
  scrollPosition.value = 0
}
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
  top: 20px;
  left: 340px;
  width: 660px;;
  height: 240px;
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 2;
}

.room-display {
  width: 1020px;
  height: 280px;
  overflow: hidden;
  position: relative;
  background: #eceef8;
  padding: 20px 0;
  display: flex;
  justify-content: center;
}

.rooms-container {
  width: 1020px;
  max-width: 1020px;
  margin: auto auto;
  display: flex;
  gap: 20px;
  position: relative;
  transition: transform 0.3s ease-out;
}

.room-card {
  width: 320px;
  min-width: 320px;
  max-width: 320px;
  height: 240px;
  flex-shrink: 0;
  border-radius: 12px;
  overflow: hidden;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease,opacity 0.3s ease;
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

.edge-mask {
  position: absolute;
  top: 0;
  bottom: 0;
  width: calc((100% - 1020px) / 2);
  background: #f8f9fa;
  z-index: 1;
  pointer-events: none;
}

@media (max-width: 768px) {
  .room-card {
    min-width: 280px;
  }
}

.edge-mask {
  position: absolute;
  top: 0;
  bottom: 0;
  width: calc((100% - 1020px) / 2);
  background: #f8f9fa;
  z-index: 1;
  pointer-events: none;
}

.edge-mask.left {
  left: 0;
}

.edge-mask.right {
  right: 0;
}
</style>
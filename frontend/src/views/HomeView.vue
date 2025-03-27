<template>
  <div class="home-container">
    <main class="middle-column">
      <div class="top-row">
        <h1><strong>DIICSU</strong></h1>
        <h2><strong>Room Booking System</strong></h2>
      </div>
      <div class="middle-row">
        <room-display
            :room-ids="roomIds"
            :rooms="roomsData"
            @room-selected="handleRoomSelected"
            @room-unselected="handleRoomUnselected"
        />
      </div>
      <div class="bottom-row">
        <time-table
            @time-selected="handleTimeSelection"
        />
      </div>

    </main>

    <div class="right-column">
      <room-search
          @filters-updated="handleFilters"
          :selected-room="selectedRoom"
          :book-date="bookDate"
          :selected-date="selectedDate"
          :selected-slots="selectedSlots"
      />
    </div>
  </div>
</template>

<script setup>
import {getCurrentInstance, nextTick, onMounted, provide, ref} from "vue";
import RoomSearch from "@/components/RoomSearch.vue";
import TimeTable from '@/components/TimeTable.vue';
import RoomDisplay from '@/components/RoomDisplay.vue';

const instance = getCurrentInstance()
const backendAddress = instance.appContext.config.globalProperties.$backendAddress
const roomIds = ref([])
const bookDate = ref(null)
const selectedRoom = ref(null)
const selectedDate = ref(null)
const selectedSlots = ref([])
const bookTimeSlots = ref([])
const roomsData = ref([])
const childData = ref([])
const lessonData = ref([])
const roomSelected = ref(0)
provide('childData', childData)
provide('lessonData', lessonData)

provide('roomSelected', roomSelected)

provide('bookDate', bookDate)
provide('bookTimeSlots', bookTimeSlots)

const fetchData = async () => {
  try {
    const instance = getCurrentInstance();
    const user = instance.appContext.config.globalProperties.$me()
    const url = backendAddress + `/allRoom`;
    const response = await fetch(url, {
      credentials: 'include'
    });
    const data = await response.json();
    roomsData.value = data.data;
    roomIds.value = roomsData.value
        .filter(room => Number.isInteger(room.id))
        .map(room => room.id)
        .sort((a, b) => a - b);
    console.log('Fetched data:', roomsData.value);
  } catch (err) {
    console.error('Failed to fetch data:', err);
  }
};
onMounted(() => {
  fetchData()
})

const handleFilters = (filters) => {
  const filteredRooms = roomsData.value.filter(room => {
    return filters.every(filter => {
      switch (filter.type) {
        case 'access':
          if (filter.value === 'all') {
            return true;
          } else {
            return room.access === 1;
          }
        case 'capacity':
          switch (filter.value) {
            case '1-15':
              return room.capacity >= 1 && room.capacity <= 15
            case '16-30':
              return room.capacity >= 16 && room.capacity <= 30
            case '31-45':
              return room.capacity >= 31 && room.capacity <= 45
            case '46-60':
              return room.capacity >= 46 && room.capacity <= 60
            default:
              return true
          }
        case 'equipment':
          if (filter.value.length === 0) return true;

          return filter.value.every(equip => {
            const roomEquipments = room.equipment || [];
            return roomEquipments.includes(equip);
          });
        case 'date-time':
          if (!filter.value.date || filter.value.slots.length === 0) return true;
          console.log("test filter date", filter.value.date)
          console.log("slots", filter.value.slots)
          const selectedDate = formatDate(filter.value.date);

          console.log("filter date after format:", selectedDate)
          console.log("booking", room.booking)
          // Check for booking conflicts
          const hasBookingConflict = room.booking.some(booking => {
            if (formatDate(booking.date) === selectedDate) {
              return booking.time.some(bookedSlot => filter.value.slots.includes(bookedSlot));
            }
            return false;
          });

          // Check for lesson conflicts (if lessons exist)
          const hasLessonConflict = room.lesson && room.lesson.some(lesson => {
            if (formatDate(lesson.date) === selectedDate) {
              return lesson.time.some(lessonSlot => filter.value.slots.includes(lessonSlot));
            }
            return false;
          });

          const hasConflict = hasBookingConflict || hasLessonConflict;

          console.log("conflict", hasConflict)
          return !hasConflict;
        default:
          return true
      }
    })
  })

  roomIds.value = filteredRooms.map(room => room.id)
}

function formatDate(date) {
  if (!date) return '';
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

const handleRoomSelected = async (room) => {
  selectedRoom.value = room;
  roomSelected.value = 1
  try {
    const response = await fetch(backendAddress + `/requestRoomDetails?roomId=${room.id}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    childData.value = data.data.booking;
    lessonData.value = data.data.lesson;
    console.log("Received room details:", childData.value);
    console.log("Received lesson details:", lessonData.value);

  } catch (error) {
    console.error("Error fetching room details:", error);
    childData.value = null;
    lessonData.value = null;
  }
};

const handleRoomUnselected = () => {
  bookDate.value = null;
  selectedRoom.value = null;
  selectedDate.value = null;
  selectedSlots.value = [];
  bookTimeSlots.value = [];
  roomSelected.value = 0
};

const handleTimeSelection = (date, slots) => {
  bookDate.value = date;
  bookTimeSlots.value = slots;
  console.log(date, slots)
};
</script>

<style scoped>
body {
  font-family: 'Cambria', serif;
}

.home-container {
  display: flex;
  width: 100%;
  height: 100%;
  overflow: auto;
}


.middle-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #eceef8;
  padding: 10px 20px 10px 20px;
}

.top-row {
  height: 17%;
  margin-bottom: 0;
}

.top-row h1 {
  margin: 0 0 0 0;
  font-size: 48px;
  font-weight: bold;
}

.top-row h2 {
  margin: 0 0 5px;
  font-size: 48px;
  color: #555;
}

.middle-row {
  height: 29%;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.bottom-row {
  height: 54%;
  display: block;
  width: 100%;
  gap: 20px;
}

.right-column {
  background-color: #eceef8;
  padding: 10px;
  width: 28%;
  height: 100%;
}

.middle-column, .right-column {
  min-height: 100%;
}

html, body {
  height: 100%;
  overflow: auto;
}

</style>
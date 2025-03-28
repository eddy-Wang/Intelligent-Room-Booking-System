<!--
HomeView.vue - Main view component for DIICSU Room Booking System.

This component provides:
- Room display grid with selection capabilities
- Interactive timetable for time slot selection
- Comprehensive room search and filtering functionality
- Booking management interface

Props: None
Events:
- @room-selected: Emitted when a room is selected
- @room-unselected: Emitted when a room is unselected
- @time-selected: Emitted when time slots are selected
- @filters-updated: Emitted when search filters are changed

Dependencies:
- RoomDisplay.vue - For displaying room information
- TimeTable.vue - For time slot selection
- RoomSearch.vue - For search and filtering
-->
<template>
  <!-- Main container with flex layout -->
  <div class="home-container">
     <!-- Middle column containing room display and timetable -->
    <main class="middle-column">
      <!-- Header section -->
      <div class="top-row">
        <h1><strong>DIICSU</strong></h1>
        <h2><strong>Room Booking System</strong></h2>
      </div>

      <!-- Room display section -->
      <div class="middle-row">
        <room-display
            :room-ids="roomIds"
            :rooms="roomsData"
            @room-selected="handleRoomSelected"
            @room-unselected="handleRoomUnselected"
        />
      </div>

      <!-- Timetable section -->
      <div class="bottom-row">
        <time-table
            @time-selected="handleTimeSelection"
        />
      </div>

    </main>

    <!-- Right column for search and filters -->
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
/**
 * Room Booking System - Main View Component
 * Handles room display, selection, time slot management and filtering
 */
import {getCurrentInstance, nextTick, onMounted, provide, ref} from "vue";
import RoomSearch from "@/components/RoomSearch.vue";
import TimeTable from '@/components/TimeTable.vue';
import RoomDisplay from '@/components/RoomDisplay.vue';
// Component instance and backend configuration
const instance = getCurrentInstance()
const backendAddress = instance.appContext.config.globalProperties.$backendAddress
// Reactive state variables
const roomIds = ref([])               // List of room IDs to display
const bookDate = ref(null)            // Selected booking date
const selectedRoom = ref(null)        // Currently selected room
const selectedDate = ref(null)        // Selected date for booking
const selectedSlots = ref([])         // Selected time slots
const bookTimeSlots = ref([])         // Time slots for booking
const roomsData = ref([])             // Full room data from backend
const childData = ref([])             // Booking data for selected room
const lessonData = ref([])            // Lesson data for selected room
const roomSelected = ref(0)           // Flag indicating if room is selected

// Provide data to child components
provide('childData', childData)
provide('lessonData', lessonData)

provide('roomSelected', roomSelected)

provide('bookDate', bookDate)
provide('bookTimeSlots', bookTimeSlots)

/**
 * Fetches all room data from backend
 * @async
 */
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
    // Extract and sort room IDs
    roomIds.value = roomsData.value
        .filter(room => Number.isInteger(room.id))
        .map(room => room.id)
        .sort((a, b) => a - b);
    console.log('Fetched data:', roomsData.value);
  } catch (err) {
    console.error('Failed to fetch data:', err);
  }
};
// Fetch data when component mounts
onMounted(() => {
  fetchData()
})
/**
 * Handles filter updates from RoomSearch component
 * @param {Array} filters - Array of filter objects
 */
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
  // Update displayed room IDs based on filters
  roomIds.value = filteredRooms.map(room => room.id)
}

/**
 * Formats date to YYYY-MM-DD string
 * @param {Date|string} date - Date to format
 * @returns {string} Formatted date string
 */
function formatDate(date) {
  if (!date) return '';
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * Handles room selection event
 * @param {Object} room - Selected room object
 */
const handleRoomSelected = async (room) => {
  selectedRoom.value = room;
  roomSelected.value = 1
  try {
    // Fetch details for selected room
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

/**
 * Handles room unselection event
 * Resets all related state
 */
const handleRoomUnselected = () => {
  bookDate.value = null;
  selectedRoom.value = null;
  selectedDate.value = null;
  selectedSlots.value = [];
  bookTimeSlots.value = [];
  roomSelected.value = 0
};

/**
 * Handles time slot selection from timetable
 * @param {Date} date - Selected date
 * @param {Array} slots - Array of selected time slots
 */
const handleTimeSelection = (date, slots) => {
  bookDate.value = date;
  bookTimeSlots.value = slots;
  console.log(date, slots)
};
</script>

<style scoped>
/* Main container styles */
body {
  font-family: 'Cambria', serif;
}
/* Flex layout for main container */
.home-container {
  display: flex;
  width: 100%;
  height: 100%;
  overflow: auto;
}

/* Middle column styles */
.middle-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #eceef8;
  padding: 10px 20px 10px 20px;
}
/* Header row styles */
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
/* Room display grid styles */
.middle-row {
  height: 29%;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

/* Timetable styles */
.bottom-row {
  height: 54%;
  display: block;
  width: 100%;
  gap: 20px;
}
/* Right column (search) styles */
.right-column {
  background-color: #eceef8;
  padding: 10px;
  width: 28%;
  height: 100%;
}
/* Full height styles for columns */
.middle-column, .right-column {
  min-height: 100%;
}

/* Full page height styles */
html, body {
  height: 100%;
  overflow: auto;
}

</style>
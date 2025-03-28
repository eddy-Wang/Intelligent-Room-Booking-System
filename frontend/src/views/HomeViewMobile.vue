<!--
HomeViewMobile.vue - Main view component for DIICSU Room Booking System.

This component provides:
- Interactive room display with filtering capabilities
- Calendar and time slot selection interface
- Booking management functionality
- Real-time availability checking

Props: None
Events:
- @room-selected: Emitted when a room is selected
- @room-unselected: Emitted when a room is unselected
- @time-selected: Emitted when time slots are selected
- @filters-updated: Emitted when search filters are changed

Dependencies:
- Vue3Datepicker - For date selection
- Element Plus - For UI components and messaging
- Axios - For HTTP requests
-->
<template>
  <!-- Main Container -->
  <div class="home-container">
    <!-- Title Section -->
    <div class="title-container">
      <h1><strong>DIICSU</strong></h1>
      <h2><strong>Room Booking System</strong></h2>
    </div>

    <!-- Filter Section -->
    <div class="filter-container">
      <div class="filter-header">
        Filter
      </div>
      <div class="filter-content">
        <!-- Capacity Filter -->
        <div class="filter-section">
          <h2 id="first-section">Capacity</h2>
          <div class="button-filters">
            <button
                v-for="(filter, index) in capacityFilters"
                :key="index"
                :class="{ 'active-filter': activeCapacityFilter === filter.value }"
                @click="handleCapacityFilter(filter.value)"
            >
              {{ filter.label }}
            </button>
          </div>
        </div>
        <!-- Equipment Filter -->
        <div class="filter-section">
          <h2>Available Equipment</h2>
          <div class="button-filters">
            <button
                v-for="(filter, index) in equipmentFilters"
                :key="index"
                :class="{ 'active-filter': activeEquipmentFilters.includes(filter.value) }"
                @click="handleEquipmentFilter(filter.value)"
            >
              {{ filter.label }}
            </button>
          </div>
        </div>
        <!-- Date and Time Filter -->
        <div class="filter-section">
          <h2>Date and Time</h2>
          <div class="date-picker">
            <div class="date-picker-toggle">
              <Vue3Datepicker
                  placeholder="Select a date"
                  v-model="selectedDate"
                  :language="'en'"
                  :format="'yyyy-MM-dd'"
                  :disabledDate="disabledDate"
                  :clearable="true"
              />
            </div>
          </div>
          <div class="time-picker">
            <input
                type="text"
                id="time-picker-toggle"
                class="time-picker-toggle"
                readonly
                placeholder="Select time slots"
                :value="selectedTimeDisplay"
                @click="toggleTimePicker"
            />
            <div class="time-picker-dropdown" v-if="isTimePickerOpen">
              <label v-for="(slot, index) in filterTimeSlots" :key="index">
                <input
                    type="checkbox"
                    :value="index"
                    :checked="selectedTimeSlotMaps.includes(filterTimeSlotMap[slot])"
                    @change="toggleFilterSlot(index)"
                />
                {{ slot }}
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Rooms List Section -->
    <div class="rooms-container">
      <template v-if="filteredRooms.length > 0">
        <div
            v-for="room in filteredRooms"
            :key="room.id"
            class="room-card"
            :class="{ selected: selectedRoom && selectedRoom.id === room.id }"
            @click="() => { selectRoom(room); handleRoomSelected(room) }"
        >
          <div class="room-card-content">
            <div class="room-image">
              <img :src="room.image_url" :alt="room.name"/>
            </div>
            <div class="room-details">
              <h2>{{ room.name }}</h2>
              <p>Capacity: {{ room.capacity }}</p>
              <p>Equipment: {{ room.equipment.join(', ') }}</p>
              <p>Location: {{ room.location }}</p>
            </div>
          </div>
        </div>
      </template>
      <div v-else class="placeholder">
        No rooms available.
      </div>
    </div>

    <!-- Time Table Section -->
    <div class="time-table-container" @time-selected="handleTimeSelection">
      <div class="time-table-header">
        Time
      </div>
      <div class="time-table-content">
        <!-- Calendar -->
        <div class="calendar-container">
          <div class="calendar-header">
            <button @click="prevMonth" class="calendar-nav-button">‹</button>
            <span class="month-year">{{ currentMonth }} {{ currentYear }}</span>
            <button @click="nextMonth" class="calendar-nav-button">›</button>
          </div>
          <div class="calendar-grid">
            <div class="calendar-weekday" v-for="day in weekdays" :key="day">
              {{ day }}
            </div>
            <div
                v-for="day in daysInMonth"
                :key="day.date"
                :class="[
                'calendar-day',
                { selected: isSelected(day.date), disabled: !day.isCurrentMonth || day.isPastDate }
              ]"
                @click="!day.isPastDate && selectDate(day.date)"
            >
              {{ day.day }}
            </div>
          </div>
        </div>
        <!-- Time Slots -->
        <div class="time-slots-container">
          <div class="time-slots-grid">
            <button
                v-for="(slot, index) in timeSlots"
                :key="index"
                :disabled="slot.status === 0"
                :class="['time-slot-button', {
      'selected': slot.status === 2,
      'disabled': slot.status === 0 || isSlotDisabled(slot, index)
    }]"
                @click="toggleSlot(index)"
            >
              {{ formatTime(slot.start) }} - {{ formatTime(slot.end) }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <hr class="divider-line"/>

    <!-- Booking Information Section -->
    <div class="book-information-container">
      <div class="book-information-content">
        <h2>Book Information</h2>
        <div class="result-box scrollable">
          <div v-if="selectedRoom" class="booking-info">
            <p>Room: {{ selectedRoom.name }}</p>
            <p v-if="bookDate">Date: {{ formatDate(bookDate) }}</p>
            <div v-if="selectedSlots.length > 0">
              <p>Selected Time Slots:</p>
              <ul>
                <li v-for="(slot, index) in selectedSlots" :key="index">
                  {{ formatTime(slot.start) }} - {{ formatTime(slot.end) }}
                </li>
              </ul>
            </div>
            <div v-else>
              No time slots selected
            </div>
          </div>
          <div v-else>
            Please select a room, date, and time slots
          </div>
        </div>
      </div>
      <div class="book-information-content">
        <h2>Purpose</h2>
        <textarea
            class="input-box"
            placeholder="Enter purpose..."
            rows="3"
            style="max-height: 60px; overflow-y: auto;"
            v-model="bookingPurpose"
        ></textarea>
      </div>
    </div>

    <!-- Book Button -->
    <button
        class="book-button"
        :class="{ enabled: isBookable }"
        :disabled="!isBookable"
        @click="handleBook"
    >
      Book
    </button>
  </div>
</template>

<script setup>
/* ===== Imports ===== */
import {ref, computed, watch, onMounted, onBeforeUnmount, getCurrentInstance} from 'vue';
import Vue3Datepicker from 'vue3-datepicker';
import axios from 'axios';
import {ElMessage} from 'element-plus';
import * as today from "date-fns";

/* ===== Global Variables ===== */
const instance = getCurrentInstance();
const backendAddress = instance.appContext.config.globalProperties.$backendAddress;
const user = ref({})
/* ===== Reactive Data ===== */
const roomIds = ref([]);
const roomsData = ref([]);

const childData = ref([]);
const lessonData = ref([]);
const combinedData = ref([]);

const selectedRoom = ref(null);
const selectedDate = ref(null);
const bookDate = ref(null);
const selectedSlots = ref([]);
const bookingPurpose = ref('');
const currentDate = ref(new Date());
const bookings = ref({});

/* ===== Computed Properties ===== */
// Current month and year for calendar header
const currentMonth = computed(() =>
    currentDate.value.toLocaleString('en-US', {month: 'long'})
);
const currentYear = computed(() => currentDate.value.getFullYear());

// Generate days for current month (including adjacent days for full weeks)
const daysInMonth = computed(() => {
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.getMonth();
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const days = [];
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Days from previous month
  for (let i = firstDay.getDay(); i > 0; i--) {
    const date = new Date(year, month, -i + 1);
    days.push({
      day: date.getDate(),
      date: formatDate(date),
      isCurrentMonth: false,
      isPastDate: date < today
    });
  }
  // Days in current month
  for (let i = 1; i <= lastDay.getDate(); i++) {
    const date = new Date(year, month, i);
    days.push({
      day: i,
      date: formatDate(date),
      isCurrentMonth: true,
      isPastDate: date < today
    });
  }
  // Days from next month to fill grid
  const nextMonthDays = 7 - (days.length % 7);
  for (let i = 1; i <= nextMonthDays; i++) {
    const date = new Date(year, month + 1, i);
    days.push({
      day: date.getDate(),
      date: formatDate(date),
      isCurrentMonth: false,
      isPastDate: date < today
    });
  }
  return days;
});

// Display selected time slots or default placeholder text
const selectedTimeSlots = ref([]);
const selectedTimeSlotMaps = ref([]);
const selectedTimeDisplay = computed(() => {
  return selectedTimeSlots.value.join(', ') || 'Select time slots';
});

// Filter configurations
const capacityFilters = ref([
  {label: '1 - 15', value: '1-15'},
  {label: '16 - 30', value: '16-30'},
  {label: '31 - 45', value: '31-45'},
  {label: '46 - 60', value: '46-60'}
]);
const activeCapacityFilter = ref('');
const roomSelected = ref(0)
const equipmentFilters = ref([
  {label: 'Projector', value: 'Projector'},
  {label: 'Whiteboard', value: 'Whiteboard'},
  {label: 'Microphone', value: 'Microphone'},
  {label: 'Computer', value: 'Computer'},
  {label: 'Power Outlets', value: 'Power Outlets'},
  {label: 'Wi-Fi', value: 'Wi-Fi'}
]);
const activeEquipmentFilters = ref([]);

// Time picker related data
const isTimePickerOpen = ref(false);
const filterTimeSlots = ref([
  '08:00-08:45',
  '09:00-09:45',
  '10:00-10:45',
  '10:55-11:40',
  '12:00-12:45',
  '12:55-13:40',
  '14:00-14:45',
  '14:55-15:40',
  '16:00-16:45',
  '16:55-17:40',
  '19:00-19:45',
  '19:55-20:40'
]);
const filterTimeSlotMap = {
  '08:00-08:45': 0,
  '09:00-09:45': 1,
  '10:00-10:45': 2,
  '10:55-11:40': 3,
  '12:00-12:45': 4,
  '12:55-13:40': 5,
  '14:00-14:45': 6,
  '14:55-15:40': 7,
  '16:00-16:45': 8,
  '16:55-17:40': 9,
  '19:00-19:45': 10,
  '19:55-20:40': 11
};

/* ===== Helper Functions ===== */
/**
 * Formats time string to ensure two digits for hours/minutes
 * @param {string} time - Time string to format (HH:MM)
 * @returns {string} Formatted time string
 */
function formatTime(time) {
  const parts = time.split(':');
  return `${parts[0].padStart(2, '0')}:${parts[1].padStart(2, '0')}`;
}

/**
 * Formats date object to 'yyyy-MM-dd' string
 * @param {Date} date - Date to format
 * @returns {string} Formatted date string
 */
function formatDate(date) {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * Watches for changes in selectedRoom and resets date/time selections
 * when a new room with bookings is selected
 */
watch(selectedRoom, (newRoom) => {
  if (newRoom && newRoom.booking) {
    console.log("999")
    selectedDate.value = ""
    timeSlots.value = timeSlots.value.map(slot => ({...slot, status: 0}));
  }
});

/**
 * Updates bookings data structure
 * @param {Array} bookingsArray - Array of booking objects
 */
const updateBookings = (bookingsArray) => {
  let tmp = {}
  console.log(4)
  bookingsArray.forEach(booking => {
    console.log(3)
    const date = new Date(booking.date);
    const timeSlots = booking.time;
    console.log(2)
    const dateKey = formatDate(date);
    console.log("dateKey ", dateKey)

    if (!tmp[dateKey]) {
      tmp[dateKey] = new Array(12).fill(1);
    }

    timeSlots.forEach(slot => {
      if (slot >= 0 && slot < 12) {
        tmp[dateKey][slot] = 0;
      }
    });
  });

  bookings.value = tmp
  console.log(bookings)
}

/**
 * Handles room selection and fetches room details
 * @param {Object} room - Selected room object
 */
const handleRoomSelected = async (room) => {
  console.log("start handleRoomSelected")
  selectedRoom.value = room;
  roomSelected.value = 1;

  try {
    const response = await fetch(`${backendAddress}/requestRoomDetails?roomId=${room.id}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    childData.value = data.data.booking;
    lessonData.value = data.data.lesson;
    console.log("Received room details:", childData.value);
    console.log("Received lesson details:", lessonData.value);
    combinedData.value = [
      ...childData.value,
      ...lessonData.value
    ];
    console.log("Combined data:", combinedData.value);
    console.log(1)
    updateBookings(combinedData.value)
  } catch (error) {
    //console.error("Error fetching room details:", error);
    childData.value = null;
    lessonData.value = null;
    combinedData.value = null;
  }
};

/**
 * Parses equipment string to array
 * @param {string} equipStr - Equipment string to parse
 * @returns {Array} Array of equipment items
 */
function parseEquipment(equipStr) {
  return equipStr.replace(/{|}|'/g, '').split(',').map(item => item.trim());
}

/* ===== Date and Calendar Functions ===== */
/**
 * Navigates to previous month in calendar
 */
function prevMonth() {
  currentDate.value = new Date(
      currentDate.value.getFullYear(),
      currentDate.value.getMonth() - 1,
      1
  );
}

/**
 * Navigates to next month in calendar
 */
function nextMonth() {
  currentDate.value = new Date(
      currentDate.value.getFullYear(),
      currentDate.value.getMonth() + 1,
      1
  );
}

/**
 * Handles date selection from calendar
 * @param {string} date - Selected date string
 */
function selectDate(date) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const selected = new Date(date);
  if (selected < today) return;
  selectedDate.value = selected;
  handleDateSelection();
}


/**
 * Checks if a date is selected
 * @param {string} date - Date to check
 * @returns {boolean} True if date is selected
 */
function isSelected(date) {
  return selectedDate.value && formatDate(selectedDate.value) === date;
}

/**
 * Updates time slots based on selected date
 */
const handleDateSelection = () => {
  if (!selectedRoom.value || !selectedDate.value) {
    timeSlots.value = timeSlots.value.map(slot => ({...slot, status: 0}));
    return;
  }

  const key = formatDate(selectedDate.value);
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  timeSlots.value = timeSlots.value.map((slot, index) => {
    const isBooked = bookings.value[key]?.[index] === 0;
    const isPastSlot = isSlotDisabled(slot, index);
    return {
      ...slot,
      status: (isBooked || isPastSlot) ? 0 : 1
    };
  });

  emitSelection();
};


/* ===== Time Slot Functions ===== */
/**
 * Toggles time slot selection
 * @param {number} index - Index of time slot to toggle
 */
const timeSlots = ref(
    Array(12)
        .fill()
        .map((_, index) => ({
          start: [
            '08:00', '08:55', '10:00', '10:55', '12:00', '12:55',
            '14:00', '14:55', '16:00', '16:55', '19:00', '19:55'
          ][index],
          end: [
            '08:45', '09:40', '10:45', '11:40', '12:45', '13:40',
            '14:45', '15:40', '16:45', '17:40', '19:45', '20:40'
          ][index],
          status: 0 // 0: disabled, 1: available, 2: selected
        }))
);

// Toggle a time slot (select/unselect)
/**
 * Toggles time slot selection
 * @param {number} index - Index of time slot to toggle
 */
function toggleSlot(index) {
  if (!selectedDate.value) return;
  if (timeSlots.value[index].status === 0) return;
  timeSlots.value[index].status = timeSlots.value[index].status === 1 ? 2 : 1;
  emitSelection();
}


/**
 * Emits current selected time slots
 */
function emitSelection() {
  const selectedSlotsArr = timeSlots.value
      .map((slot, idx) => ({...slot, index: idx}))
      .filter(slot => slot.status === 2);
  // Update booking date and selected slots
  handleTimeSelection(selectedDate.value, selectedSlotsArr);
}


/**
 * Handles time slot selection
 * @param {Date} date - Selected date
 * @param {Array} slots - Array of selected slots
 */
function handleTimeSelection(date, slots) {
  bookDate.value = date;
  selectedSlots.value = slots;
}

/* ===== Filter Functions ===== */
/**
 * Computes combined filters from capacity, equipment and date-time selections
 * @returns {Array} Array of filter objects to apply
 */
const combinedFilters = computed(() => {
  const filters = [];
  if (activeCapacityFilter.value) {
    filters.push({type: 'capacity', value: activeCapacityFilter.value});
  }
  if (activeEquipmentFilters.value.length > 0) {
    filters.push({type: 'equipment', value: activeEquipmentFilters.value.slice()});
  }
  if (selectedDate.value && selectedTimeSlotMaps.value.length > 0) {
    filters.push({
      type: 'date-time',
      value: {
        date: selectedDate.value,
        slots: selectedTimeSlotMaps.value
      }
    });
  }
  return filters;
});

/**
 * Applies filters to room data
 * @param {Array} filters - Array of filter objects
 */
function handleFilters(filters) {
  const filteredRooms = roomsData.value.filter(room => {
    return filters.every(filter => {
      switch (filter.type) {
        case 'capacity':
          switch (filter.value) {
            case '1-15':
              return room.capacity >= 1 && room.capacity <= 15;
            case '16-30':
              return room.capacity >= 16 && room.capacity <= 30;
            case '31-45':
              return room.capacity >= 31 && room.capacity <= 45;
            case '46-60':
              return room.capacity >= 46 && room.capacity <= 60;
            default:
              return true;
          }
        case 'equipment':
          if (filter.value.length === 0) return true;
          return filter.value.every(equip => room.equipment.includes(equip));
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
          return true;
      }
    });
  });
  roomIds.value = filteredRooms.map(room => room.id);
}

/**
 * Watches for changes in combined filters and applies them
 */
watch(combinedFilters, (newFilters) => {
  handleFilters(newFilters);
});

/* ===== Filter UI Handlers ===== */
/**
 * Toggles capacity filter
 * @param {string} filterValue - Capacity filter value
 */
function handleCapacityFilter(filterValue) {
  activeCapacityFilter.value = activeCapacityFilter.value === filterValue ? '' : filterValue;
}

/**
 * Toggles equipment filter
 * @param {string} filterValue - Equipment filter value
 */
function handleEquipmentFilter(filterValue) {
  if (activeEquipmentFilters.value.includes(filterValue)) {
    activeEquipmentFilters.value = activeEquipmentFilters.value.filter(v => v !== filterValue);
  } else {
    activeEquipmentFilters.value.push(filterValue);
  }
}

/* ===== Time Picker Handlers ===== */
/**
 * Toggles time picker dropdown
 */
function toggleTimePicker() {
  selectedTimeSlots.value = [];
  selectedTimeSlotMaps.value = [];
  isTimePickerOpen.value = !isTimePickerOpen.value;
}

/**
 * Toggles time slot in filter
 * @param {number} index - Index of time slot to toggle
 */
function toggleFilterSlot(index) {
  const slot = filterTimeSlots.value[index];
  const slotValue = filterTimeSlotMap[slot];
  if (selectedTimeSlots.value.includes(slot)) {
    selectedTimeSlots.value = selectedTimeSlots.value.filter(s => s !== slot);
    selectedTimeSlotMaps.value = selectedTimeSlotMaps.value.filter(v => v !== slotValue);
  } else {
    selectedTimeSlots.value.push(slot);
    selectedTimeSlotMaps.value.push(slotValue);
  }
}

/* ===== Date Picker Helper ===== */
/**
 * Disables dates before today in date picker
 * @param {Date} date - Date to check
 * @returns {boolean} True if date should be disabled
 */
function disabledDate(date) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const target = new Date(date);
  target.setHours(0, 0, 0, 0);
  return target.getTime() < today.getTime();
}

/* ===== Room Selection and Booking ===== */
/**
 * Computes filtered rooms based on current roomIds filter
 * @returns {Array} Filtered list of rooms
 */
const filteredRooms = computed(() => {
  return roomsData.value.filter(room => roomIds.value.includes(room.id));
});

/**
 * Selects or deselects a room
 * @param {Object} room - Room object to select/deselect
 */
function selectRoom(room) {
  if (selectedRoom.value && selectedRoom.value.id === room.id) {
    // Deselect room and reset booking data
    selectedRoom.value = null;
    bookings.value = {};
    selectedDate.value = null;
    bookDate.value = null;
  } else {
    selectedRoom.value = room;
    // Process room bookings if available
    if (room.booking && room.booking.length > 0) {
      room.booking.forEach(booking => {
        if (booking.status === 'Confirmed') {
          if (!bookings.value[booking.date]) {
            bookings.value[booking.date] = new Array(12).fill(1);
          }
          booking.time.forEach(slotIndex => {
            bookings.value[booking.date][slotIndex] = 0;
          });
        }
      });
    } else {
      bookings.value = {};
    }
  }
}

/**
 * Determines if booking can be submitted
 * @returns {boolean} True if all required booking fields are filled
 */
const isBookable = computed(() => {
  return (
      selectedRoom.value &&
      bookDate.value &&
      selectedSlots.value.length > 0 &&
      bookingPurpose.value.trim() !== ''
  );
});

/**
 * Handles booking submission
 */
async function handleBook() {
  if (!isBookable.value) {
    alert('Please select a room, date, time slots, and enter purpose.');
    return;
  }
  const bookingData = {
    roomId: selectedRoom.value.id,
    roomName: selectedRoom.value.name,
    date: formatDate(bookDate.value),
    timeSlots: selectedSlots.value.map(slot => slot.index),
    purpose: bookingPurpose.value,
    user_email: user.value.email
  };
  try {
    const response = await axios.post(backendAddress + '/bookRoom', bookingData, {
      headers: {'Content-Type': 'application/json'}
    });
    if (response.data.code === '000') {
      ElMessage.success('Booking successful!');
      selectedRoom.value = null;
      selectedDate.value = null;
      bookDate.value = null;
      selectedSlots.value = [];
      bookingPurpose.value = '';
    } else if (response.data.code === '007') {
      ElMessage.info('You are currently on the blacklist and cannot make bookings.');
    } else {
      ElMessage.error('Booking failed: ' + response.data.message);
    }
  } catch (error) {
    console.error('Error booking room:', error);
    ElMessage.error('An error occurred while booking the room, please try again later');
  }
}

/* ===== Global Event Handlers ===== */
/**
 * Handles clicks outside time picker to close it
 * @param {Event} event - Click event
 */
function handleClickOutside(event) {
  if (!event.target.closest('.time-picker')) {
    isTimePickerOpen.value = false;
  }
}

/**
 * Checks if a time slot should be disabled
 * @param {Object} slot - Time slot object
 * @param {number} index - Slot index
 * @returns {boolean} True if slot should be disabled
 */
function isSlotDisabled(slot, index) {
  // No date selected ⇒ all slots disabled
  if (!selectedDate.value) return true;

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const sel = new Date(selectedDate.value);
  sel.setHours(0, 0, 0, 0);


  // Selected date is in past ⇒ disabled
  if (sel < today) return true;

  // Selected date is in future ⇒ enabled
  if (sel > today) return false;

  // Selected date is today ⇒ check if slot time has passed
  const now = new Date();
  const [h, m] = slot.start.split(':').map(Number);
  const slotTime = new Date(sel);
  slotTime.setHours(h, m, 0, 0);

  return slotTime < now;
}


/* ===== Lifecycle Hooks ===== */
/**
 * Component mounted lifecycle hook
 * - Fetches current user data
 * - Loads room data from backend
 * - Sets up click outside handler
 */
onMounted(async () => {
  let me = await instance.appContext.config.globalProperties.$me()
  user.value = me.data
  // Fetch room data from backend
  try {
    const response = await axios.get(backendAddress + '/allRoom', {
      withCredentials: true
    });
    if (response.data.code === '001') {
      roomsData.value = response.data.data.map(room => {
        const newRoom = {...room};
        newRoom.equipment = parseEquipment(room.equipment);
        newRoom.image = room.image_url;
        return newRoom;
      });
      roomIds.value = roomsData.value.map(room => room.id);
    } else {
      console.error(response.data.message);
    }
  } catch (error) {
    console.error('Error fetching rooms:', error);
  }
  // Add event listener for closing time picker
  document.addEventListener('click', handleClickOutside);
});


/**
 * Component beforeUnmount lifecycle hook
 * - Cleans up click outside handler
 */
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});


</script>

<style scoped>
/* ===== Global Styles ===== */
body {
  font-family: Cambria, serif;
  font-size: 0.9rem;
  line-height: 1.2;
}

/* ===== Main Container ===== */
.home-container {
  font-family: 'Cambria', serif;
  display: flex;
  flex-direction: column;
  background-color: #eceef8;
  width: 100%;
  height: 100%;
  padding: 20px;
  overflow: auto;
}

/* ===== Title Section ===== */
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

/* ===== Filter Section ===== */
.filter-container {
  min-height: 100%;
  width: 100%;
  padding: 0;
  background-color: white;
  border-radius: 20px;
  margin-top: 16px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.filter-header {
  margin: 0;
  font-weight: bolder;
  font-size: 1.25rem;
  background-color: #3155ef;
  color: white;
  height: 30px;
  width: 100%;
  line-height: 30px;
  text-align: center;
  border-radius: 20px 20px 0 0;
}

.filter-content {
  border: none;
  padding: 15px;
  flex-grow: 1;
}

.filter-section h2 {
  margin-left: 5%;
  margin-top: 12px;
  margin-bottom: 6px;
  font-size: 1.1rem;
  font-weight: bold;
  color: #333;
}

#first-section {
  margin-top: 0;
}

/* Button Filters */
.button-filters {
  width: 90%;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 5px;
  align-items: stretch;
}

.button-filters button {
  width: 100%;
  height: 35px;
  padding: 9px;
  font-size: 0.9rem;
  border-radius: 10px;
  background-color: #eceef8;
  color: #333;
  border: none;
  transition: all 0.3s ease-in-out;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.button-filters button.active-filter {
  background-color: #3155ef;
  color: white;
}

/* Date Picker */
.date-picker {
  margin-left: 5%;
  position: relative;
  display: inline-block;
  width: 90%;
}

.date-picker-toggle {
  height: 35px;
  margin-bottom: 10px;
  width: 100%;
  padding: 8px 16px;
  background-color: #eceef8;
  border: 1px solid #ccc;
  cursor: pointer;
  border-radius: 10px;
}

.vue3-datepicker .disabled,
.vue3-datepicker .datepicker__cell--disabled {
  color: #ccc;
  pointer-events: none;
}

/* Time Picker */
.time-picker {
  margin-left: 5%;
  position: relative;
  display: inline-block;
  width: 90%;
}

.time-picker-toggle {
  height: 35px;
  margin-bottom: 10px;
  width: 100%;
  padding: 8px 16px;
  background-color: #eceef8;
  border: 1px solid #ccc;
  cursor: pointer;
  border-radius: 10px;
}

.time-picker-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 10px;
  z-index: 1000;
  width: 100%;
  box-shadow: 0 4px 8px rgb(255, 255, 255);
  max-height: 200px;
  overflow-y: auto;
}

.time-picker-dropdown label {
  display: block;
  margin: 5px 0;
}

.time-picker-dropdown input[type="checkbox"] {
  margin-right: 8px;
}

/* ===== Time Table Section ===== */
.time-table-container {
  min-height: 100%;
  width: 100%;
  padding: 0;
  background-color: white;
  border-radius: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.time-table-header {
  margin: 0;
  font-weight: bold;
  font-size: 1.25rem;
  background-color: #3155ef;
  color: white;
  height: 30px;
  width: 100%;
  line-height: 30px;
  text-align: center;
  border-radius: 20px 20px 0 0;
}

.time-table-content {
  width: 95%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  height: 100%;
}

/* Calendar Styles */
.calendar-container {
  width: 100%;
  margin-top: 2%;
  padding: 5px;
  flex: 1;
  line-height: 1.2;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.calendar-nav-button {
  background: none;
  border: none;
}

.month-year {
  font-size: 1.2rem;
  font-weight: bold;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
}

.calendar-weekday {
  text-align: center;
  font-weight: bold;
  padding: 6px;
}

.calendar-day {
  text-align: center;
  padding: 4px;
  border-radius: 4px;
  font-weight: bold;
}

.calendar-day.selected {
  background-color: #3155ef;
  color: white;
  border-radius: 100%;
}

.calendar-day.disabled {
  color: #ccc;
  cursor: not-allowed;
  pointer-events: none;
}

/* Time Slots */
.time-slots-container {
  width: 100%;
  margin-bottom: 10px;
  padding: 5px;
  overflow-y: auto;
  flex: 1;
  line-height: 1;
}

.time-slots-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.time-slot-button {
  width: 100%;
  padding: 9px;
  font-size: 0.9rem;
  border: none;
  border-radius: 10px;
  transition: background-color 0.2s;
  font-weight: bold;
}

.time-slot-button:disabled {
  background-color: #a6a6a6;
  color: white;
  cursor: not-allowed;
}

.time-slot-button:not(:disabled) {
  background-color: #eceef8;
  color: black;
}

.time-slot-button.selected {
  background-color: #3155ef;
  color: white;
}

/* ===== Rooms Section ===== */
.rooms-container {
  background: #eceef8;
  width: 100%;
  margin: 0 auto 20px auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: relative;
}

.room-card {
  min-height: 140px;
  width: 100%;
  border-radius: 20px;
  overflow: hidden;
  background: #fff;
  cursor: pointer;
  display: flex;
  align-items: stretch;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.room-card.selected {
  box-shadow: 0 0 10px 3px rgba(0, 123, 255, 0.8);
  transform: scale(1.02);
}

.room-card-content {
  display: flex;
  flex-direction: row;
}


.room-image {
  width: 140px;
  height: 100%;
  overflow: hidden;
  flex-shrink: 0;
}

.room-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.room-details {
  flex: 1;
  padding: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.room-details h2 {
  margin: 0 0 5px;
  font-size: 1.1rem;
  color: #333;
}

.room-details p {
  margin: 1px 0;
  font-size: 0.9rem;
  color: #666;
}

.placeholder {
  width: 100%;
  text-align: center;
  font-size: 18px;
  color: #666;
  padding: 108px;
  background: #eceef8;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}


/* ===== Booking Information ===== */
.book-information-container {
  width: 100%;
  padding: 10px 20px;
}

.book-information-content {
  display: flex;
  flex-direction: column;
  margin-bottom: 12px;
}

.book-information-content h2 {
  font-size: 22px;
  margin-bottom: 10px;
}

.result-box {
  background-color: #fdf8f6;
  border-left: 5px solid #3155ef;
  border-radius: 0 10px 10px 0;
  padding: 12px;
  margin-left: 3px;
}

.booking-info {
  font-size: 14px;
  line-height: 1.5;
}

.booking-info ul {
  margin: 5px 0;
  padding-left: 20px;
}

.booking-info li {
  margin: 3px 0;
}

.scrollable {
  max-height: 120px;
  overflow-y: auto;
  padding-right: 10px;
}

.book-information-content textarea {
  background-color: #fdf8f6;
  border-radius: 10px;
  padding: 5px 10px;
}

/* ===== Book Button ===== */
.book-button {
  display: block;
  margin: 0 20px 50px auto;
  background-color: #7e7c7c;
  color: white;
  padding: 5px 30px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.book-button.enabled {
  background-color: #3155ef;
  color: white;
}

.book-button:disabled {
  cursor: not-allowed;
}

.book-button:active {
  transform: translateY(0);
}

/* ===== Media Queries ===== */
@media (max-width: 390px) {
  .room-card-content {
    flex-direction: column;
  }

  .room-image {
    width: 100%;
    height: auto;
  }
}
</style>

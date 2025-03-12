<template>
  <div class="home-container">
    <!-- 标题部分 -->
    <div class="title-container">
      <h1><strong>DIICSU</strong></h1>
      <h2><strong>Room Booking System</strong></h2>
    </div>
    <!-- filter部分 -->
    <div class="filter-container">
      <div class="filter-header">
        Filter
      </div>
      <div class="filter-content">
        <div class="filter-section">
          <h2 id="first-section">Capacity</h2>
          <div class="button-filters">
            <button
                v-for="(filter, index) in capacityFilters"
                :key="index"
                :class="{ 'active-filter': activeCapacityFilter === filter.value }"
                @click="handleCapacityFilter(filter.value)">
              {{ filter.label }}
            </button>
          </div>
        </div>
        <div class="filter-section">
          <h2>Available Equipment</h2>
          <div class="button-filters">
            <button
                v-for="(filter, index) in equipmentFilters"
                :key="index"
                :class="{ 'active-filter': activeEquipmentFilters.includes(filter.value) }"
                @click="handleEquipmentFilter(filter.value)">
              {{ filter.label }}
            </button>
          </div>
        </div>
        <div class="filter-section">
          <h2>Date and Time</h2>
          <div class="date-picker">
            <div class="date-picker-toggle">
              <Vue3Datepicker
                  placeholder="Select a date"
                  v-model="selectedDate"
                  :language="'en'"
                  :format="'yyyy-MM-dd'"
                  @change="updateDateDisplay"
                  :disabled-date="disabledDate"
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
    <!-- 房间&信息部分 -->
    <div class="rooms-container">
      <template v-if="filteredRooms.length > 0">
        <div
            v-for="room in filteredRooms"
            :key="room.id"
            class="room-card"
            :class="{ selected: selectedRoom && selectedRoom.id === room.id }"
            @click="selectRoom(room)">
          <div class="room-card-content">
            <div class="room-image">
              <img :src="room.image" :alt="room.name"/>
            </div>
            <div class="room-details">
              <h2>{{ room.name }}</h2>
              <p>Capacity: {{ room.capacity }}</p>
              <p>Equipment: {{ room.equipment.join(', ') }}</p>
              <p>Access: {{ room.access }}</p>
            </div>
          </div>
        </div>
      </template>
      <div v-else class="placeholder">
        No rooms available.
      </div>
    </div>
    <!-- time table部分 -->
    <div class="time-table-container" @time-selected="handleTimeSelection">
      <div class="time-table-header">
        Time
      </div>
      <div class="time-table-content">
        <!-- 日历部分 -->
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
                :class="['calendar-day', { 'selected': isSelected(day.date), 'disabled': !day.isCurrentMonth || day.isPastDate }]"
                @click="!day.isPastDate && selectDate(day.date)">
              {{ day.day }}
            </div>
          </div>
        </div>
        <!-- 时间槽部分 -->
        <div class="time-slots-container">
          <div class="time-slots-grid">
            <button
                v-for="(slot, index) in timeSlots"
                :key="index"
                :disabled="slot.status === 0"
                :class="['time-slot-button', { 'selected': slot.status === 2 }]"
                @click="toggleSlot(index)">
              {{ formatTime(slot.start) }} - {{ formatTime(slot.end) }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <hr class="divider-line">
    <!-- 预定信息部分 -->
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
        ></textarea>
      </div>
    </div>
    <button class="book-button" @click="handleBook">Book</button>
  </div>
</template>

<script setup>
import {ref, computed, watch, onMounted, onBeforeUnmount} from 'vue';
import Vue3Datepicker from 'vue3-datepicker';
import axios from 'axios';

// 定义响应式数据
const roomIds = ref([1, 2, 3, 4, 5]);
const bookDate = ref(null);
const selectedRoom = ref(null);
const selectedDate = ref(null);
const selectedSlots = ref([]);

// 模拟房间数据
const roomsData = [
  {
    id: 1,
    capacity: 20,
    equipment: "{'projector', 'whiteboard', 'powerOutlets', 'wifi'}",
    access: 1,
    location: "DIICSU Sixth Floor",
    info: "",
    booking: [
      {
        booking_id: "1",
        user_email: "2542762@dundee.ac.uk",
        room_id: 1,
        date: "2025-03-19",
        time: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        purpose: "test1",
        status: "Confirmed"
      },
      {
        booking_id: "2",
        user_email: "2542762@dundee.ac.uk",
        room_id: 1,
        date: "2025-03-14",
        time: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        purpose: "test2",
        status: "Missed"
      }
    ]
  },
  {
    id: 2,
    capacity: 10,
    equipment: "{'projector', 'whiteboard', 'computers', 'wifi'}",
    access: 1,
    location: "DIICSU Sixth Floor",
    info: "",
    booking: [
      {
        booking_id: "1",
        user_email: "2542762@dundee.ac.uk",
        room_id: 1,
        date: "2025-03-19",
        time: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        purpose: "test1",
        status: "Confirmed"
      },
      {
        booking_id: "2",
        user_email: "2542762@dundee.ac.uk",
        room_id: 1,
        date: "2025-03-13",
        time: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        purpose: "test2",
        status: "Missed"
      }
    ]
  },
  {
    id: 3,
    capacity: 60,
    equipment: "{'whiteboard', 'powerOutlets', 'wifi'}",
    access: 1,
    location: "DIICSU Sixth Floor",
    info: "",
    booking: []
  },
  {
    id: 4,
    capacity: 15,
    equipment: "{'whiteboard', 'outlets', 'wifi'}",
    access: 1,
    location: "DIICSU Sixth Floor",
    info: "",
    booking: []
  },
  {
    id: 5,
    capacity: 28,
    equipment: "{'whiteboard', 'powerOutlets', 'wifi'}",
    access: 1,
    location: "DIICSU Sixth Floor",
    info: "",
    booking: []
  }
];

// 根据筛选条件过滤房间
const handleFilters = (filters) => {
  console.log("Current filters:", filters);
  const filteredRooms = roomsData.filter(room => {
    return filters.every(filter => {
      switch (filter.type) {
        case 'access':
          return filter.value === 'all' ? true : room.access === filter.value;
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
          return filter.value.every(equip => {
            const roomEquipments = room.equipment || [];
            return roomEquipments.includes(equip);
          });
        case 'date-time':
          if (!filter.value.date || filter.value.slots.length === 0) return true;
          const selectedDateStr = formatDate(new Date(filter.value.date));
          const hasConflict = room.booking.some(booking => {
            if (booking.date === selectedDateStr) {
              return booking.time.some(bookedSlot => filter.value.slots.includes(bookedSlot));
            }
            return false;
          });
          return !hasConflict;
        default:
          return true;
      }
    });
  });
  roomIds.value = filteredRooms.map(room => room.id);
};

// 房间选择及时间选择处理
const handleRoomSelected = (room) => {
  selectedRoom.value = room;
};
const handleRoomUnselected = () => {
  selectedRoom.value = null;
  selectedDate.value = null;
  selectedSlots.value = [];
};
const handleTimeSelection = (date, slots) => {
  bookDate.value = date;
  selectedSlots.value = slots;
};

// 日历和时间表逻辑
const currentDate = ref(new Date());
const bookings = ref({
  '2025-03-07': new Array(12).fill(0),
  '2025-03-08': new Array(12).fill(0),
  '2025-03-09': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
  '2025-03-10': new Array(12).fill(1),
  '2025-03-11': [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
  '2025-03-12': new Array(12).fill(1),
  '2025-03-13': new Array(12).fill(1),
  '2025-03-14': new Array(12).fill(1),
  '2025-03-15': new Array(12).fill(1),
});
const timeSlots = ref(
    Array(12)
        .fill()
        .map((_, index) => ({
          start: ['08:00', '08:55', '10:00', '10:55', '12:00', '12:55', '14:00', '14:55', '16:00', '16:55', '19:00', '19:55'][index],
          end: ['08:45', '09:40', '10:45', '11:40', '12:45', '13:40', '14:45', '15:40', '16:45', '17:40', '19:45', '20:40'][index],
          status: 0
        }))
);
const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const currentMonth = computed(() =>
    currentDate.value.toLocaleString('en-US', {month: 'long'})
);
const currentYear = computed(() => currentDate.value.getFullYear());
const daysInMonth = computed(() => {
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.getMonth();
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const days = [];
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  // 上个月日期
  for (let i = firstDay.getDay(); i > 0; i--) {
    const date = new Date(year, month, -i + 1);
    days.push({
      day: date.getDate(),
      date: formatDate(date),
      isCurrentMonth: false,
      isPastDate: date < today
    });
  }
  // 当前月
  for (let i = 1; i <= lastDay.getDate(); i++) {
    const date = new Date(year, month, i);
    days.push({
      day: i,
      date: formatDate(date),
      isCurrentMonth: true,
      isPastDate: date < today
    });
  }
  // 下个月日期
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

function prevMonth() {
  currentDate.value = new Date(
      currentDate.value.getFullYear(),
      currentDate.value.getMonth() - 1,
      1
  );
}

function nextMonth() {
  currentDate.value = new Date(
      currentDate.value.getFullYear(),
      currentDate.value.getMonth() + 1,
      1
  );
}

function selectDate(date) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const selected = new Date(date);
  if (selected < today) return;
  selectedDate.value = selected;
  handleDateSelection();
}

function isSelected(date) {
  return selectedDate.value && formatDate(selectedDate.value) === date;
}

function handleDateSelection() {
  if (!selectedDate.value) {
    timeSlots.value = timeSlots.value.map(slot => ({...slot, status: 0}));
    return;
  }
  const dateKey = formatDate(selectedDate.value);
  if (bookings.value[dateKey]) {
    timeSlots.value = timeSlots.value.map((slot, index) => ({
      ...slot,
      status: bookings.value[dateKey][index]
    }));
  } else {
    timeSlots.value = timeSlots.value.map(slot => ({...slot, status: 0}));
  }
  emitSelection();
}

function toggleSlot(index) {
  if (!selectedDate.value) return;
  const dateKey = formatDate(selectedDate.value);
  if (!bookings.value[dateKey]) {
    bookings.value[dateKey] = new Array(12).fill(0);
  }
  if (timeSlots.value[index].status === 1) {
    timeSlots.value[index].status = 2;
  } else if (timeSlots.value[index].status === 2) {
    timeSlots.value[index].status = 1;
  }
  emitSelection();
}

function emitSelection() {
  const selectedSlotsArr = timeSlots.value
      .map((slot, idx) => ({...slot, index: idx}))
      .filter(slot => slot.status === 2);
  handleTimeSelection(selectedDate.value, selectedSlotsArr);
}

function formatTime(time) {
  const parts = time.split(':');
  return `${parts[0].padStart(2, '0')}:${parts[1].padStart(2, '0')}`;
}

function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

const capacityFilters = ref([
  {label: '1 - 15', value: '1-15'},
  {label: '16 - 30', value: '16-30'},
  {label: '31 - 45', value: '31-45'},
  {label: '46 - 60', value: '46-60'}
]);
const activeCapacityFilter = ref('');
const activeAccessFilter = ref('all');
const equipmentFilters = ref([
  {label: 'Projector', value: 'Projector'},
  {label: 'Whiteboard', value: 'Whiteboard'},
  {label: 'Microphone', value: 'Microphone'},
  {label: 'Computer', value: 'Computer'},
  {label: 'Power Outlets', value: 'Power Outlets'},
  {label: 'Wi-Fi', value: 'Wi-Fi'}
]);
const activeEquipmentFilters = ref([]);
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
const selectedTimeSlots = ref([]);
const selectedTimeSlotMaps = ref([]);
const selectedTimeDisplay = computed(() => {
  return selectedTimeSlots.value.join(', ') || 'Select time slots';
});

function handleCapacityFilter(filterValue) {
  activeCapacityFilter.value = activeCapacityFilter.value === filterValue ? '' : filterValue;
}

function handleEquipmentFilter(filterValue) {
  if (activeEquipmentFilters.value.includes(filterValue)) {
    activeEquipmentFilters.value = activeEquipmentFilters.value.filter(v => v !== filterValue);
  } else {
    activeEquipmentFilters.value.push(filterValue);
  }
}

function toggleTimePicker() {
  selectedTimeSlots.value = [];
  selectedTimeSlotMaps.value = [];
  isTimePickerOpen.value = !isTimePickerOpen.value;
}

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

function updateDateDisplay() {
}

function disabledDate(date) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return date < today;
}

const combinedFilters = computed(() => {
  const filters = [];
  if (activeAccessFilter.value !== 'all') {
    filters.push({type: 'access', value: activeAccessFilter.value});
  }
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
    console.log("selected date:", selectedDate.value);
  }
  return filters;
});
watch(combinedFilters, (newFilters) => {
  handleFilters(newFilters);
  // selectedRoom.value = null;
});

function handleClickOutside(event) {
  if (!event.target.closest('.time-picker')) {
    isTimePickerOpen.value = false;
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
const displayRooms = ref([
  {
    id: 1,
    name: 'Informal Meeting Room',
    image: new URL('@/assets/informal-meeting.png', import.meta.url).href,
    capacity: '15-30',
    equipment: ['Projector', 'Whiteboard', 'Power Outlets', 'Wi-Fi'],
    access: 'All'
  },
  {
    id: 2,
    name: 'Formal Meeting Room',
    image: new URL('@/assets/formal-meeting.png', import.meta.url).href,
    capacity: '30-45',
    equipment: ['Projector', 'Whiteboard', 'Computers', 'Wi-Fi'],
    access: 'Staff Only'
  },
  {
    id: 3,
    name: 'Room 635',
    image: new URL('@/assets/635.png', import.meta.url).href,
    capacity: '15-30',
    equipment: ['Whiteboard', 'Power Outlets', 'Wi-Fi'],
    access: 'All'
  },
  {
    id: 4,
    name: 'English Corridor',
    image: new URL('@/assets/corridor.png', import.meta.url).href,
    capacity: '15-30',
    equipment: ['Whiteboard', 'Power Outlets', 'Wi-Fi'],
    access: 'All'
  },
  {
    id: 5,
    name: 'Seminar Room',
    image: new URL('@/assets/seminar-room.png', import.meta.url).href,
    capacity: '15-30',
    equipment: ['Whiteboard', 'Power Outlets', 'Wi-Fi'],
    access: 'All'
  }
]);
const filteredRooms = computed(() => {
  return displayRooms.value.filter(room => roomIds.value.includes(room.id));
});

function selectRoom(room) {
  if (selectedRoom.value && selectedRoom.value.id === room.id) {
    selectedRoom.value = null;
  } else {
    selectedRoom.value = room;
  }
}

async function handleBook() {
  if (!selectedRoom.value || !bookDate.value || selectedSlots.value.length === 0) {
    alert('Please select a room, date, and time slots.');
    return;
  }
  const bookingData = {
    roomId: selectedRoom.value.id,
    roomName: selectedRoom.value.name,
    date: formatDate(bookDate.value),
    timeSlots: selectedSlots.value
  };
  try {
    const response = await axios.post('https://your-backend-api.com/bookings', bookingData);
    if (response.data.success) {
      alert('Booking successful!');
    } else {
      alert('Booking failed: ' + response.data.message);
    }
  } catch (error) {
    console.error('Error booking room:', error);
    alert('An error occurred while booking the room.');
  }
}
</script>

<style>
body {
  font-family: Cambria, serif;
  font-size: 0.9rem;
  line-height: 1.2;
}

.home-container {
  display: flex;
  flex-direction: column;
  background-color: #eceef8;
  width: 100%;
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

.time-table-container {
  min-height: 100%;
  width: 100%;
  padding: 0;
  background-color: white;
  border-radius: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
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

.filter-container {
  min-height: 100%;
  width: 100%;
  padding: 0;
  background-color: white;
  border-radius: 20px;
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

/* 房间展示样式 */
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
  height: 140px;
  width: 100%;
  border-radius: 20px;
  overflow: hidden;
  background: #fff;
  cursor: pointer;
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
  height: 140px;
  overflow: hidden;
  flex-shrink: 0;
}

.room-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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

.divider-line {
  border: none;
  height: 1px;
  background-color: #ddd;
  margin: 10px;
}

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

.book-button:active {
  transform: translateY(0);
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

.input-box {
  background-color: #fdf8f6;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  color: #333;
  padding: 12px 16px;
  outline: none;
  resize: vertical;
  width: 100%;
  max-height: 150px;
  overflow-y: auto;
}

.input-box:focus {
  background-color: #f8eae4;
}

@media (max-width: 200px) {
  .room-card-content {
    flex-direction: column;
  }

  .room-image {
    width: 100%;
    height: auto;
  }
}
</style>

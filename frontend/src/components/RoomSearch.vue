<template>
  <div class="room-search-container">
    <!-- 第一个 Panel：筛选条件 -->
    <div class="panel1">
      <div class="panel-content">
        <!-- Capacity  -->
        <div class="filter-section">
          <h2>Capacity</h2>
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

        <!-- Available Equipment  -->
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

        <!-- Date/Time  -->
        <div class="filter-section">
          <h2>Date and Time</h2>
          <div class="date-picker">
            <div class="date-picker-toggle">
              <vue3-datepicker
                  placeholder="Select a date"
                  v-model="selectedDate"
                  :language="'en'"
                  :format="'yyyy-MM-dd'"
                  @change="updateDateDisplay"
                  :disabled-date="disabledDate"
              />
            </div>
          </div>
          <!-- time picker -->
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
              <label v-for="(slot, index) in timeSlots" :key="index">
                <input
                    type="checkbox"
                    :value="index"
                    :checked="selectedTimeSlots.includes(index)"
                    @change="toggleSlot(index)"
                />
                {{ slot }}
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- 第一个 Panel 的蓝色底边 -->
      <div class="panel-footer">
        Room Search
      </div>
    </div>

    <!-- 第二个 Panel：预订信息 -->
    <div class="panel2">
      <div class="panel-content">
        <div class="input-section">
          <h2>Book Information</h2>
          <div class="result-box scrollable">
            <div v-if="selectedRoom" class="booking-info">
              <p>Room: {{ selectedRoom.name }}</p>
              <p v-if="bookDate">Date: {{ formatDate(bookDate) }}</p>
              <div v-if="bookTimeSlots.length > 0">
                <p>Selected Time Slots:</p>
                <ul>
                  <li v-for="(slot, index) in bookTimeSlots" :key="index">
                    {{ formatTime(slot.start) }} - {{ formatTime(slot.end) }}
                  </li>
                </ul>
              </div>
              <div v-else>
                No time slots selected
              </div>
              <p v-else>No time slots selected</p>
            </div>
            <div v-else>
              Please select a room, date and time slots
            </div>
          </div>
        </div>
        <div class="input-section">
          <h2>Purpose</h2>
          <textarea
              class="input-box"
              placeholder="Enter purpose..."
              rows="2"
              style="max-height: 10%; overflow-y: auto;"
              v-model="bookingPurpose"
          ></textarea>
        </div>
        <button class="book-button" @click="handleBook">Book</button>
      </div>

      <!-- 第二个 Panel 的蓝色底边 -->
      <div class="panel-footer">
        Booking Details
      </div>
    </div>
  </div>
</template>
<script>
import Vue3Datepicker from 'vue3-datepicker';
import axios from 'axios';
import {getCurrentInstance, inject} from "vue";

export default {
  name: 'RoomSearch',
  components: {
    Vue3Datepicker
  },

  setup() {
    let instance = getCurrentInstance()
    const user_email = instance.appContext.config.globalProperties.$user.email
    // 注入父组件提供的数据
    const bookDate = inject('bookDate');
    const bookTimeSlots = inject('bookTimeSlots')

    return {
      bookDate, bookTimeSlots, user_email
    };
  },
  watch: {
    combinedFilters(newFilters) {
      this.$emit('filters-updated', newFilters);
    },
    selectedDate(newDate) {
      this.$emit('date-selected', newDate); // 将 selectedDate 传递给父组件
    },

    bookDate(newVal, oldVal) {
      console.log("bookDate old:", oldVal);
      console.log("bookDate new:", newVal);
    },
    bookTimeSlots(newVal, oldVal) {
      console.log("bookDate old:", oldVal);
      console.log("bookDate new:", newVal);
    }
  },

  data() {
    return {
      accessFilters: [
        {label: 'All', value: 'all'},
        {label: 'Staff Only', value: 'staff'}
      ],
      activeAccessFilter: 'all',
      bookingPurpose: "",

      // Capacity
      capacityFilters: [
        {label: '1 - 15', value: '1-15'},
        {label: '16 - 30', value: '16-30'},
        {label: '31 - 45', value: '31-45'},
        {label: '46 - 60', value: '46-60'}
      ],
      activeCapacityFilter: '',

      // Available Equipment
      equipmentFilters: [
        {label: 'Projector', value: 'Projector'},
        {label: 'Whiteboard', value: 'Whiteboard'},
        {label: 'Microphone', value: 'Microphone'},
        {label: 'Computer', value: 'Computer'},
        {label: 'Power Outlets', value: 'Power Outlets'},
        {label: 'Wi-Fi', value: 'Wi-Fi'}
      ],
      activeEquipmentFilters: [],


      isTimePickerOpen: false,
      timeSlots: [
        '08:00-08:45',
        '08:55-09:40',
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
      ],
      timeSlotMap: {
        '08:00-08:45': 0,
        '08:55-09:40': 1,
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
      },
      bookDate: null,
      selectedDate: null,
      selectedTimeSlots: [],
      selectedTimeSlotMaps: [],
      selectedTimeDisplay: '',
      isDatePickerOpen: false,
      selectedDateDisplay: '',
    };
  },

  computed: {
    combinedFilters() {
      const filters = [];

      if (this.activeAccessFilter !== 'all') {
        filters.push({type: 'access', value: this.activeAccessFilter});
      }

      if (this.activeCapacityFilter) {
        filters.push({type: 'capacity', value: this.activeCapacityFilter});
      }

      if (this.activeEquipmentFilters.length > 0) {
        filters.push({type: 'equipment', value: [...this.activeEquipmentFilters]});
      }

      if (this.selectedDate && this.selectedTimeSlotMaps.length > 0) {
        filters.push({
          type: 'date-time',
          value: {
            date: this.selectedDate,
            slots: this.selectedTimeSlotMaps
          }
        });
        console.log("aaa", this.selectedDate)
      }

      return filters;
    },


    selectedTimeDisplay() {
      return this.selectedTimeSlots.join(', ') || 'Select time slots';
    },
    updateDateDisplay() {
      this.selectedDateDisplay = this.selectedDate ? this.selectedDate.toLocaleDateString() : '';
      this.$emit('date-selected', this.selectedDate); // 如果需要传递给父组件
    }

  },

  methods: {
    handleAccessFilter(filterValue) {
      this.activeAccessFilter = filterValue;
    }
    ,
    handleCapacityFilter(filterValue) {
      this.activeCapacityFilter =
          this.activeCapacityFilter === filterValue ? '' : filterValue;
    }
    ,
    handleEquipmentFilter(filterValue) {
      if (this.activeEquipmentFilters.includes(filterValue)) {
        this.activeEquipmentFilters = this.activeEquipmentFilters.filter(
            v => v !== filterValue
        );
      } else {
        this.activeEquipmentFilters.push(filterValue);
      }
    },
    formatDate(date) {
      if (!date) return '';
      const d = new Date(date);
      return d.toISOString().split('T')[0];
    },
    formatTime(timeStr) {
      return timeStr.slice(0, 5)
    },

    toggleTimePicker() {
      this.selectedTimeSlots = [];
      this.selectedTimeSlotMaps = [];

      this.isTimePickerOpen = !this.isTimePickerOpen;
    },
    toggleSlot(index) {
      const slotKey = this.timeSlots[index]; //  '08:00-08:45'
      const slotValue = this.timeSlotMap[slotKey]; // 0

      if (this.selectedTimeSlots.includes(slotKey)) {
        this.selectedTimeSlots = this.selectedTimeSlots.filter(s => s !== slotKey);
        this.selectedTimeSlotMaps = this.selectedTimeSlotMaps.filter(v => v !== slotValue);
      } else {
        this.selectedTimeSlots.push(slotKey);
        this.selectedTimeSlotMaps.push(slotValue);
      }
    },


    handleClickOutside(event) {
      if (!this.$el.contains(event.target)) {
        this.isTimePickerOpen = false;
      }
    },

    async handleBook() {
      if (!this.selectedRoom || !this.bookDate || this.bookTimeSlots.length === 0) {
        alert('Please select a room, date, and time slots.');
        return;
      }
      console.log(this.selectedRoom, this.bookDate, this.bookTimeSlots)
      const bookingData = {
        roomId: this.selectedRoom.id,
        roomName: this.selectedRoom.name,
        date: this.bookDate,
        timeSlots: this.bookTimeSlots.map(slot => slot.index),
        purpose: this.bookingPurpose,
        user_email: this.user_email
      };
      try {
        const response = await axios.post('http://127.0.0.1:8080/bookRoom', bookingData, {
          headers: {'Content-Type': 'application/json'}
        });
        if (response.data.code === '000') {
          alert('Booking successful!');
        } else {
          alert('Booking failed: ' + response.data.message);
        }
      } catch (error) {
        console.error('Error booking room:', error);
        alert('An error occurred while booking the room.');
      }
    }
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside);
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleClickOutside);
  },

  props: {
    selectedRoom: Object,
    bookDate: String,
    selectedSlots:
    Array
  },
}

</script>
<style scoped>
* {
  font-family: 'Cambria', serif;
}

.room-search-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
}

.panel1, .panel2 {
  font-family: 'Cambridge', sans-serif;
  border: none;
  border-radius: 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 400px;
  margin-bottom: 20px;
}

.panel-footer {
  border: none;
  height: 20%;
  background-color: #3155ef;
  color: white;
  text-align: center;
  font-size: 25px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0 0 20px 20px;
  width: 100%;
}

.panel-content {
  border: none;
  padding: 15px;
  flex-grow: 1;
}

.filter-section h2 {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 6px;
}

.button-filters {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  align-items: stretch;
}

.button-filters button {
  width: 100%;
  height: 35px;
  font-size: 18px;
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

.input-section {
  display: flex;
  flex-direction: column;
}

.input-section h2 {
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

.book-button {
  display: block;
  margin-left: auto;
  margin-top: 10px;
  background-color: #7e7c7c;
  color: white;
  padding: 10px 25px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.book-button:hover {
  background-color: #404040;
  transform: translateY(-1px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
}

.book-button:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
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

.time-picker {
  position: relative;
  display: inline-block;
  width: 100%;
}

.time-picker-toggle {
  width: 100%;
  padding: 8px 16px;
  background-color: #eceef8;
  border: 1px solid #ccc;
  cursor: pointer;
  font-size: 16px;
  border-radius: 4px;
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
  font-size: 14px;
}

.time-picker-dropdown input[type="checkbox"] {
  margin-right: 8px;
}

.scrollable {
  max-height: 100px;
  overflow-y: auto;
  padding-right: 10px;
}

.time-picker-toggle {
  height: 35px;
  margin-bottom: 10px;
  width: 100%;
  padding: 8px 16px;
  background-color: #eceef8;
  border: 1px solid #ccc;
  cursor: pointer;
  font-size: 16px;
  border-radius: 10px;
}

.date-picker {
  position: relative;
  display: inline-block;
  width: 100%;
}

.date-picker-toggle {
  height: 35px;
  margin-bottom: 10px;
  width: 100%;
  padding: 8px 16px;
  background-color: #eceef8;
  border: 1px solid #ccc;
  cursor: pointer;
  font-size: 16px;
  border-radius: 10px;
}
</style>
<!--<style scoped>-->
<!--* {-->
<!--  font-family: 'Cambria', serif;-->
<!--}-->
<!--.panel1 {-->
<!--  font-family: 'Cambridge', sans-serif;-->
<!--  border: none;-->
<!--  border-radius: 20px;-->
<!--  background-color: #fff;-->
<!--  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);-->
<!--  overflow: hidden;-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--  max-height: 55%;-->
<!--  width: 400px;-->
<!--  margin-bottom: 20px; /* 两个 Panel 之间的间距 */-->
<!--}-->
<!--.panel2 {-->
<!--  font-family: 'Cambridge', sans-serif;-->
<!--  border: none;-->
<!--  border-radius: 20px;-->
<!--  background-color: #fff;-->
<!--  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);-->
<!--  overflow: hidden;-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--  max-height:55%;-->
<!--  width: 400px;-->
<!--  margin-bottom: 20px; /* 两个 Panel 之间的间距 */-->
<!--}-->

<!--.panel-footer {-->
<!--  border: none;-->
<!--  height: 18%;-->
<!--  background-color: #3155ef;-->
<!--  color: white;-->
<!--  text-align: center;-->
<!--  font-size: 25px;-->
<!--  font-weight: bold;-->
<!--  display: flex;-->
<!--  align-items: center;-->
<!--  justify-content: center;-->
<!--  border-radius: 0 0 20px 20px;-->
<!--  width: 100%;-->
<!--}-->

<!--.panel-content {-->
<!--  border: none;-->
<!--  padding: 15px;-->
<!--  flex-grow: 1;-->
<!--}-->
<!--.filter-section h2 {-->
<!--  font-size: 20px;-->
<!--  font-weight: bold;-->
<!--  color: #333;-->
<!--  margin-bottom: 6px;-->
<!--}-->


<!--.button-filters {-->
<!--  display: grid;-->
<!--  grid-template-columns: repeat(2, 1fr);-->
<!--  gap: 10px;-->
<!--  align-items: stretch;-->
<!--}-->


<!--.button-filters button {-->
<!--  width: 100%;-->
<!--  height: 40px;-->
<!--  font-size: 18px;-->
<!--  border-radius: 10px;-->
<!--  background-color: #eceef8;-->
<!--  color: #333;-->
<!--  border: none;-->
<!--  transition: all 0.3s ease-in-out;-->
<!--  display: flex;-->
<!--  align-items: center;-->
<!--  justify-content: center;-->
<!--  cursor: pointer;-->
<!--}-->

<!--.button-filters button.active-filter {-->
<!--  background-color: #3155ef;-->
<!--  color: white;-->
<!--}-->

<!--.input-section {-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--}-->

<!--.input-section h2 {-->
<!--  font-size: 22px;-->
<!--  margin-bottom: 10px;-->
<!--}-->

<!--.result-box {-->
<!--  background-color: #fdf8f6;-->
<!--  border-left: 5px solid #3155ef;-->
<!--  border-radius: 0 10px 10px 0;-->
<!--  padding: 12px;-->
<!--  margin-left: 3px;-->
<!--}-->

<!--.input-box {-->
<!--  background-color: #fdf8f6;-->
<!--  border: none;-->
<!--  border-radius: 10px;-->
<!--  font-size: 16px;-->
<!--  color: #333;-->
<!--  padding: 12px 16px;-->
<!--  outline: none;-->
<!--  resize: vertical; /* 允许用户垂直调整大小 */-->
<!--  width: 100%; /* 确保宽度占满父容器 */-->
<!--  max-height: 150px; /* 设置最大高度 */-->
<!--  overflow-y: auto; /* 超过高度时显示滚动条 */-->
<!--}-->

<!--.input-box:focus {-->
<!--  background-color: #f8eae4;-->
<!--}-->

<!--.book-button {-->
<!--  display: block;-->
<!--  margin-left: auto;-->
<!--  margin-top: 10px;-->
<!--  background-color: #7e7c7c;-->
<!--  color: white;-->
<!--  padding: 10px 25px;-->
<!--  border: none;-->
<!--  border-radius: 8px;-->
<!--  font-size: 16px;-->
<!--  font-weight: 500;-->
<!--  cursor: pointer;-->
<!--  transition: all 0.2s ease;-->
<!--  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);-->
<!--}-->

<!--.book-button:hover {-->
<!--  background-color: #404040;-->
<!--  transform: translateY(-1px);-->
<!--  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);-->
<!--}-->

<!--.book-button:active {-->
<!--  transform: translateY(0);-->
<!--  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);-->
<!--}-->

<!--.booking-info {-->
<!--  font-size: 14px;-->
<!--  line-height: 1.5;-->
<!--}-->

<!--.booking-info ul {-->
<!--  margin: 5px 0;-->
<!--  padding-left: 20px;-->
<!--}-->

<!--.booking-info li {-->
<!--  margin: 3px 0;-->
<!--}-->


<!--.time-picker {-->
<!--  position: relative;-->
<!--  display: inline-block;-->
<!--  width: 100%;-->
<!--}-->

<!--.time-picker-toggle {-->
<!--  width: 100%;-->
<!--  padding: 8px 16px;-->
<!--  background-color: #eceef8;-->
<!--  border: 1px solid #ccc;-->
<!--  cursor: pointer;-->
<!--  font-size: 16px;-->
<!--  border-radius: 4px;-->
<!--}-->

<!--.time-picker-dropdown {-->
<!--  position: absolute;-->
<!--  top: 100%;-->
<!--  left: 0;-->
<!--  background-color: #fff;-->
<!--  border: 1px solid #ccc;-->
<!--  padding: 10px;-->
<!--  z-index: 1000;-->
<!--  width: 100%;-->
<!--  box-shadow: 0 4px 8px rgb(255, 255, 255);-->
<!--  max-height: 200px;-->
<!--  overflow-y: auto;-->
<!--}-->

<!--.time-picker-dropdown label {-->
<!--  display: block;-->
<!--  margin: 5px 0;-->
<!--  font-size: 14px;-->
<!--}-->

<!--.time-picker-dropdown input[type="checkbox"] {-->
<!--  margin-right: 8px;-->
<!--}-->

<!--.scrollable {-->
<!--  max-height: 100px; /* 设置一个固定高度 */-->
<!--  overflow-y: auto; /* 允许垂直滚动 */-->
<!--  padding-right: 10px; /* 为滚动条留出空间 */-->
<!--}-->

<!--.time-picker-toggle {-->
<!--  height: 35px;-->
<!--  margin-bottom: 10px;-->
<!--  width: 100%;-->
<!--  padding: 8px 16px;-->
<!--  background-color: #eceef8;-->
<!--  border: 1px solid #ccc;-->
<!--  cursor: pointer;-->
<!--  font-size: 16px;-->
<!--  border-radius: 10px;-->
<!--}-->

<!--.date-picker {-->
<!--  position: relative;-->
<!--  display: inline-block;-->
<!--  width: 100%;-->
<!--}-->

<!--.date-picker-toggle {-->
<!--  height: 35px;-->
<!--  margin-bottom: 10px;-->
<!--  width: 100%;-->
<!--  padding: 8px 16px;-->
<!--  background-color: #eceef8;-->
<!--  border: 1px solid #ccc;-->
<!--  cursor: pointer;-->
<!--  font-size: 16px;-->
<!--  border-radius: 10px;-->
<!--}-->


<!--</style>-->
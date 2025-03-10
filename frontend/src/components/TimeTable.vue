<template>
  <v-container fluid>
    <v-row no-gutters>
      <v-col cols="12">
        <v-card class="d-flex flex-column" style="background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); height: 410px;">
          <v-row no-gutters class="flex-grow-1" style="height: 350px;">
            <v-col cols="6" class="d-flex justify-center align-center" style="height: 100%; overflow-y: auto;">
              <v-date-picker v-model="selectedDate" show-adjacent-months @update:modelValue="handleDateSelection" flat no-title
                             prev-icon="mdi-chevron-left" next-icon="mdi-chevron-right" class="flex-grow-1" style="font-size: 0.8rem; max-width: 90%; height: 120%"></v-date-picker>
            </v-col>
            <v-col cols="6" style="height: 105%; overflow-y: auto;">
              <v-row no-gutters class="flex-grow-1" style="height: 100%;">
                <v-col v-for="(slot, index) in timeSlots" :key="index" cols="6" class="pb-2">
                  <v-btn :style="getButtonStyle(slot)" :disabled="slot.status === 0" block depressed class="ma-80"
                         @click="toggleSlot(index)" :class="{ 'mb-4': index !== timeSlots.length - 1 }" style="font-size: 0.8rem;">
                    {{ formatTime(slot.start) }} - {{ formatTime(slot.end) }}
                  </v-btn>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
          <div class="d-flex justify-center align-center"
               style="background-color: #3155ef; color: white; height: 40px; line-height: 40px;">
            Room Status
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  emits: ['time-selected'],

  data() {
    return {
      selectedDate: null,
      bookings: {
        '2025-03-07': new Array(12).fill(0),
        '2025-03-08': new Array(12).fill(0),
        '2025-03-09': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        '2025-03-10': new Array(12).fill(1),
        '2025-03-11': new Array(12).fill(1),
        '2025-03-12': new Array(12).fill(1),
        '2025-03-13': new Array(12).fill(1),
        '2025-03-14': new Array(12).fill(1),
        '2025-03-15': new Array(12).fill(1),
      },
      timeSlots: Array(12).fill().map((_, index) => ({
        start: ['08:00', '08:55', '10:00', '10:55', '12:00', '12:55', '14:00', '14:55', '16:00', '16:55', '19:00', '19:55'][index],
        end: ['08:45', '09:40', '10:45', '11:40', '12:45', '13:40', '14:45', '15:40', '16:45', '17:40', '19:45', '20:40'][index],
        status: 0
      }))
    };
  },

  methods: {
    handleDateSelection(date) {
      if (!date) {
        this.timeSlots = this.timeSlots.map(slot => ({...slot, status: 0}));
        return;
      }

      this.selectedDate = date;
      const dateKey = this.formatDate(this.selectedDate);

      if (this.bookings[dateKey]) {
        this.timeSlots = this.timeSlots.map((slot, index) => ({
          ...slot,
          status: this.bookings[dateKey][index]
        }));
      } else {
        this.timeSlots = this.timeSlots.map(slot => ({...slot, status: 0}));
      }

      this.emitSelection();
    },

    toggleSlot(index) {
      if (!this.selectedDate) return;

      const dateKey = this.formatDate(this.selectedDate);

      if (!this.bookings[dateKey]) {
        this.bookings[dateKey] = new Array(12).fill(0);
      }

      if (this.timeSlots[index].status === 1) {
        this.timeSlots[index].status = 2;
        this.bookings[dateKey][index] = 1;
      } else if (this.timeSlots[index].status === 2) {
        this.timeSlots[index].status = 1;
        this.bookings[dateKey][index] = 0;
      }

      this.emitSelection();
    },

    emitSelection() {
      const selectedSlots = this.timeSlots
          .map((slot, idx) => ({...slot, index: idx}))
          .filter(slot => slot.status === 2);
      this.$emit('time-selected', this.selectedDate, selectedSlots);
    },

    getButtonStyle(slot) {
      if (!this.selectedDate) {
        return {backgroundColor: '#a6a6a6', color: 'white'};
      }
      switch (slot.status) {
        case 0:
          return {backgroundColor: '#a6a6a6', color: 'white'};
        case 1:
          return {backgroundColor: '#eceef8', color: 'black'};
        case 2:
          return {backgroundColor: '#3155ef', color: 'white'};
        default:
          return {backgroundColor: '#a6a6a6', color: 'white'};
      }
    },

    formatTime(time) {
      const [hours, minutes] = time.split(':');
      return `${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}`;
    },

    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    }
  }
};
</script>

<style>
.v-date-picker-table--date .v-btn {
  background: transparent !important;
  color: rgba(0, 0, 0, 0.87) !important;
  font-weight: 400;
  border: none !important;
}

.v-btn {
  border: none !important;
  transition: all 0.2s;
}

.v-btn[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}

.v-date-picker-header {
  display: none;
}

.v-card {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  height: 80%;
  margin: 0;
  display: flex;
  flex-direction: column;
}

.room-status-label {
  background-color: #3155ef;
  color: white;
  width: 100%;
  text-align: center;
  padding: 10px 0;
  margin-top: auto;
  border-radius: 0 0 8px 8px;
}
</style>

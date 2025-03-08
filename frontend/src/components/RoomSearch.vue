<template>
  <div class="panel">
    <div class="panel-content">
      <div class="filter-section">
        <h2>Room Access</h2>
        <div class="button-filters">
          <button
              v-for="(filter, index) in accessFilters"
              :key="index"
              :class="{ 'active-filter': activeAccessFilter === filter.value }"
              @click="handleAccessFilter(filter.value)"
          >
            {{ filter.label }}
          </button>
        </div>
      </div>

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

      <hr class="divider-line">

      <div class="input-section">
        <h2>Book Information</h2>
        <div class="result-box">Detailed Room Information</div>
      </div>
      <div class="input-section">
        <h2>Purpose</h2>
        <input type="text" class="input-box">

      </div>
      <button class="book-button">Book</button>
    </div>

    <!-- **Room Search & Booking** -->
    <div class="panel-footer">
      Room Search & Booking
    </div>
  </div>
</template>

<script>
export default {
  name: 'RoomSearch',
  data() {
    return {
      accessFilters: [
        {label: 'All', value: 'all'},
        {label: 'Staff Only', value: 'staff'}
      ],
      activeAccessFilter: 'all',

      // Capacity 过滤条件
      capacityFilters: [
        {label: '0 - 15', value: '0-15'},
        {label: '15 - 30', value: '15-30'},
        {label: '30 - 45', value: '30-45'},
        {label: '45 - 60', value: '45-60'}
      ],
      activeCapacityFilter: '',

      // Available Equipment 过滤条件
      equipmentFilters: [
        {label: 'Projector', value: 'projector'},
        {label: 'Whiteboard', value: 'whiteboard'},
        {label: 'Microphone', value: 'microphone'},
        {label: 'Computers', value: 'computers'},
        {label: 'Power Outlets', value: 'powerOutlets'},
        {label: 'Wi-Fi', value: 'wifi'}
      ],
      activeEquipmentFilters: [],
    };
  },

  computed: {
    combinedFilters() {
      const filters = [];
      // 添加Access過濾條件（排除默認的'all'）
      if (this.activeAccessFilter !== 'all') {
        filters.push({ type: 'access', value: this.activeAccessFilter });
      }
      // 添加Capacity過濾條件
      if (this.activeCapacityFilter) {
        filters.push({ type: 'capacity', value: this.activeCapacityFilter });
      }
      // 添加Equipment過濾條件（僅當有選中時）
      if (this.activeEquipmentFilters.length > 0) {
        filters.push({ type: 'equipment', value: [...this.activeEquipmentFilters] });
      }
      return filters;
    }
  },
  watch: {
    combinedFilters(newFilters) {
      this.$emit('filters-updated', newFilters); // 觸發事件傳遞數組
    }
  },
  methods: {
    handleAccessFilter(filterValue) {
      this.activeAccessFilter = filterValue;
    },
    handleCapacityFilter(filterValue) {
      this.activeCapacityFilter =
          this.activeCapacityFilter === filterValue ? '' : filterValue;
    },
    handleEquipmentFilter(filterValue) {
      if (this.activeEquipmentFilters.includes(filterValue)) {
        this.activeEquipmentFilters = this.activeEquipmentFilters.filter(
            v => v !== filterValue
        );
      } else {
        this.activeEquipmentFilters.push(filterValue);
      }
    }
  }
};
//   methods: {
//     handleAccessFilter(filterValue) {
//       this.activeAccessFilter = filterValue;
//       this.$emit('filter-access', filterValue);
//     },
//
//     handleCapacityFilter(filterValue) {
//       if (this.activeCapacityFilter === filterValue) {
//         this.activeCapacityFilter = '';
//       } else {
//         this.activeCapacityFilter = filterValue;
//       }
//       this.$emit('filter-capacity', this.activeCapacityFilter);
//     },
//
//     handleEquipmentFilter(filterValue) {
//       if (this.activeEquipmentFilters.includes(filterValue)) {
//         this.activeEquipmentFilters = this.activeEquipmentFilters.filter(
//             value => value !== filterValue
//         );
//       } else {
//         this.activeEquipmentFilters.push(filterValue);
//       }
//       this.$emit('filter-equipment', this.activeEquipmentFilters);
//     }
//   }
// };
</script>

<style scoped>
* {
  font-family: 'Cambria', serif;
}

.panel {
  font-family: 'Cambridge', sans-serif;
  border: none;
  border-radius: 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.panel-content {
  border: none;
  padding: 12px;
  flex-grow: 1;
}

.panel-footer {
  border: none;
  height: 50px;
  background-color: #3155ef;
  color: white;
  text-align: center;
  font-size: 25px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0 0 20px 20px;
}


.filter-section h2 {
  font-size: 22px;
  font-weight: bold;
  color: #333;
  margin-bottom: 12px;
}


.button-filters {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  align-items: stretch;
}


.button-filters button {
  width: 100%;
  height: 50px;
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
  height: 50px;
  border: none;
  border-radius: 10px;
  font-size: 22px;
  color: #333;
  padding: 12px 16px;
  outline: none;
}

.input-box:focus {
  background-color: #f8eae4;
}

.divider-line {
  border: none;
  height: 1px;
  background-color: #ddd;
  margin-top: 20px;
}
.book-button {
  display: block;
  margin-left: auto;
  margin-top: 20px;
  background-color: #7e7c7c;
  color: white;
  padding: 10px 25px;
  border: none;
  border-radius: 8px;
  font-size: 18px;
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

</style>

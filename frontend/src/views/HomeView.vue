<template>
  <div class="home-container">
    <main class="middle-column">
      <!-- 上排：标题 + 房间分类按钮 -->
      <div class="top-row">
        <h1><strong>DIICSU</strong></h1>
        <h2><strong>Room Booking System</strong></h2>
      </div>
      <!-- 下排：房间卡片 + 底部“Rooms”栏 -->
      <div class="middle-row">
        <!-- 房间卡片 -->
        <!--        <room-display :room-ids="roomIds"/>-->
        <room-display
            :room-ids="roomIds"
            :rooms="roomsData"
            @room-selected="handleRoomSelected"
            @room-unselected="handleRoomUnselected"
        />
      </div>
      <div class="bottom-row">
        <!--        <time-table/>-->
        <time-table
            @time-selected="handleTimeSelection"
        />
      </div>

    </main>

    <!-- 右侧区域（第三列） -->
    <div class="right-column">
      <!--      <room-search @filters-updated="handleFilters"/>-->
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
import {getCurrentInstance, onMounted, provide, ref} from "vue";
import RoomSearch from "@/components/RoomSearch.vue";
import TimeTable from '@/components/TimeTable.vue';
import RoomDisplay from '@/components/RoomDisplay.vue';


const roomIds = ref([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
//room status
const bookDate = ref(null)
const selectedRoom = ref(null)
const selectedDate = ref(null)
const selectedSlots = ref([])
const bookTimeSlots = ref([])
const roomsData = ref([])
const childData = ref([])
const roomSelected = ref(0)
provide('childData', childData)
provide('roomSelected', roomSelected)

provide('bookDate', bookDate)
provide('bookTimeSlots',bookTimeSlots)

const fetchData = async () => {
  try {
    const instance = getCurrentInstance();
    const userPermission = instance.appContext.config.globalProperties.$user.permission;
    const url = `http://127.0.0.1:8080/allRoom?permission=`+userPermission;
    const response = await fetch(url);
    const data = await response.json();
    roomsData.value = data.data;
    console.log('Fetched data:', roomsData.value);
  } catch (err) {
    console.error('Failed to fetch data:', err);
  }
};
onMounted(() => {
  fetchData()
})

const handleFilters = (filters) => {
  console.log("当前过滤条件：", filters);

  // 执行过滤
  const filteredRooms = roomsData.value.filter(room => {
    // 检查所有过滤器是否都满足
    return filters.every(filter => {
      switch (filter.type) {
        case 'access':
          if (filter.value === 'all') {
            return true; // 显示全部房间
          } else {
            return room.access === 1; // 严格匹配 access 值
          }
          // 容量过滤
        case 'capacity':
          // 处理不同范围值
          switch (filter.value) {
            case '1-15':
              return room.capacity >= 1 && room.capacity <= 15
            case '16-30': // 你关注的案例
              return room.capacity >= 16 && room.capacity <= 30
            case '31-45':
              return room.capacity >= 31 && room.capacity <= 45
            case '46-60':
              return room.capacity >= 46 && room.capacity <= 60
            default:
              return true
          }
        case 'equipment':
          // 当没有选择任何设备时不进行过滤
          if (filter.value.length === 0) return true;

          // 房间必须包含所有选中的设备（使用every）
          return filter.value.every(equip => {
            const roomEquipments = room.equipment || [];
            return roomEquipments.includes(equip);
          });
        case 'date-time':
          // 如果没有选择日期或时间段则不过滤
          if (!filter.value.date || filter.value.slots.length === 0) return true;
          console.log(filter.value.date)
          console.log(filter.value.slots)
          // 将用户选择的日期转换为YYYY-MM-DD格式
          const selectedDate = formatDate(filter.value.date);

          console.log("date:", selectedDate)
          // 检查该房间在选定日期的预订情况
          const hasConflict = room.booking.some(booking => {
            console.log("当前过滤条件：", filters);
            // 检查日期是否匹配
            if (booking.date === selectedDate) {
              // 检查用户选择的时间段是否与预订时间段有重叠
              //TODO:class timetable filter
              return booking.time.some(bookedSlot => filter.value.slots.includes(bookedSlot));
            }
            return false;
          });

          // 如果有冲突，过滤掉该房间
          return !hasConflict;


        default:
          return true
      }
    })
  })

  // 提取过滤后的ID
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

// 从RoomDisplay接收选中的房间
const handleRoomSelected = async (room) => {
  selectedRoom.value = room;
  roomSelected.value = 1
  try {
    // 发送GET请求，假设后端需要room.id作为参数
    const response = await fetch(`http://127.0.0.1:8080/requestRoomDetails?roomId=${room.id}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    childData.value = data.data.booking; // 将获取的数据存入响应式变量
    console.log("Received room details:", childData.value);

  } catch (error) {
    console.error("Error fetching room details:", error);
    // 可以选择重置数据或显示错误信息
    childData.value = null;
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

// 从TimeTable接收日期和时间段
const handleTimeSelection = (date, slots) => {
  bookDate.value = date;
  bookTimeSlots.value = slots;
  console.log(date,slots)
};
</script>

<style>
body {
  font-family: 'Cambria', serif;
}

.home-container {
  display: flex;
  align-items: start;
  width: 100%;
  height: 100%;
}

/* ========== 中间列：上下两排 ========== */
.middle-column {
  flex: 1;
  display: grid;
  grid-template-rows: auto 1fr auto;
  background-color: #eceef8;
  padding: 20px;
}

/* ----- 上排：标题 + Tab ----- */
.top-row {
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

/* ----- 中间（房间卡片）----- */
.middle-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

/* ----- 下排（TimeTable）----- */
.bottom-row {
  display: block;
  width: 100%;
  gap: 20px;
}

/* ========== 右侧列 ========== */
.right-column {
  background-color: #eceef8;
  padding: 10px;
  width: 28%;
  height: 100%;
}
</style>
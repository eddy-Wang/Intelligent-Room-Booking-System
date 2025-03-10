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
            @room-selected="handleRoomSelected"
            @room-unselected="handleRoomUnselected"
        />
      </div>
      <div class="bottom-row">
        <!--        <time-table/>-->
        <time-table
            @time-selected="handleTimeSelection"
            :selected-room="selectedRoom"
            :is-enabled="isTableEnabled"
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
import axios from "axios";
import {ref, computed} from "vue";
import RoomSearch from "@/components/RoomSearch.vue";
import TimeTable from '@/components/TimeTable.vue';
import RoomDisplay from '@/components/RoomDisplay.vue';


const roomIds = ref([1, 2, 3, 4, 5])
const isTableEnabled = ref(false);
//room status
const bookDate = ref(null)
const selectedRoom = ref(null)
const selectedDate = ref(null)
const selectedSlots = ref([])


//TODO: test data. can be deleted after connecting to the back end
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


const handleFilters = (filters) => {
  console.log("当前过滤条件：", filters);

  // 执行过滤
  const filteredRooms = roomsData.filter(room => {
    // 检查所有过滤器是否都满足
    return filters.every(filter => {
      switch (filter.type) {
        case 'access':
          if (filter.value === 'all') {
            return true; // 显示全部房间
          } else {
            return room.access === filter.value; // 严格匹配 access 值
          }
          // 容量过滤
        case 'capacity':
          console.log("111");
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
          console.log(filter.value.slots.length)
          // 将用户选择的日期转换为YYYY-MM-DD格式
          const selectedDate = formatDate(filter.value.date);

        function formatDate(date) {
          if (!date) return '';
          const d = new Date(date);
          const year = d.getFullYear();
          const month = String(d.getMonth() + 1).padStart(2, '0');
          const day = String(d.getDate()).padStart(2, '0');
          return `${year}-${month}-${day}`;
        }

          console.log(selectedDate)
          // 检查该房间在选定日期的预订情况
          const hasConflict = room.booking.some(booking => {
            // 检查日期是否匹配
            if (booking.date === selectedDate) {
              // 检查用户选择的时间段是否与预订时间段有重叠
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


// 从RoomDisplay接收选中的房间
const handleRoomSelected = (room) => {
  selectedRoom.value = room;
  isTableEnabled.value = true; // 启用 TimeTable
};

const handleRoomUnselected = () => {
  selectedRoom.value = null;
  selectedDate.value = null;
  selectedSlots.value = [];
  isTableEnabled.value = false; // 禁用 TimeTable
};

// 从TimeTable接收日期和时间段
const handleTimeSelection = (date, slots) => {
  bookDate.value = date;
  selectedSlots.value = slots;
};


// TODO: connect to back end
// const fetchRoomData = async () => {
//   try {
//     const response = await axios.get('https://backend-api.com/rooms');
//     roomsData.value = response.data; // 将获取的数据存储到 roomsData 中
//   } catch (error) {
//     console.error("获取房间信息失败:", error);
//   }
// };
//
// // 在组件挂载时调用 fetchRoomData
// onMounted(() => {
//   fetchRoomData();
// });
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
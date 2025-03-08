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
        <room-display :room-ids="roomIds"/>

      </div>
      <div class="bottom-row">
        <time-table/>
      </div>

    </main>

    <!-- 右侧区域（第三列） -->
    <div class="right-column">
      <room-search @filters-updated="handleFilters"/>
    </div>
  </div>
</template>

<script setup>
import {ref, computed} from "vue";
import RoomSearch from "@/components/RoomSearch.vue";
import TimeTable from '@/components/TimeTable.vue';

const roomIds = ref([1, 2, 3, 4, 5])
import RoomDisplay from '@/components/RoomDisplay.vue';
// 处理过滤器变化的回调
//TODO: get from backend
const roomsData = [
  {id: 1, capacity: 20, equipment: ['projector', 'whiteboard','powerOutlets', 'wifi']},
  {id: 2, capacity: 10, equipment: ['projector','whiteboard','computers','wifi'], access: 'staff'},
  {id: 3, capacity: 60, equipment: ['whiteboard','powerOutlets','wifi']},
  {id: 4, capacity: 15, equipment: ['whiteboard','outlets','wifi']},
  {id: 5, capacity: 28, equipment: ['whiteboard','powerOutlets','wifi']}
]


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
          // 处理不同范围值
          switch (filter.value) {
            case '0-15':
              return room.capacity >= 0 && room.capacity <= 15
            case '15-30': // 你关注的案例
              return room.capacity >= 15 && room.capacity <= 30
            case '30-45':
              return room.capacity >= 30 && room.capacity <= 45
            case '45-60':
              return room.capacity >= 45 && room.capacity <= 60
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

        default:
          return true
      }
    })
  })

  // 提取过滤后的ID
  roomIds.value = filteredRooms.map(room => room.id)
}
</script>

<style>
.home-container {
  display: flex; /* 关键：横向排列子元素 */
  align-items: start; /* 可选：让它们顶对齐 */
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
  padding: 20px;
  width: 450px;

}
</style>
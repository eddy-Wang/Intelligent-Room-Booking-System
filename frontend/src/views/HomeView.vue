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
            <room-display />

        </div>
        <div class="bottom-row">
          <time-table />
        </div>
                   
        </main>

        <!-- 右侧区域（第三列） -->
        <div class="right-column">
        <room-search />
        </div>
    </div>
</template>

<script setup>
  import RoomDisplay from '@/components/RoomDisplay.vue';
  import RoomSearch from "@/components/RoomSearch.vue";
  import TimeTable from '@/components/TimeTable.vue';
</script>

<style>
.home-container {
  display: flex;      /* 关键：横向排列子元素 */
  align-items: start; /* 可选：让它们顶对齐 */
  width: 100%;
  height: 100%;
  align-items: stretch; 
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
  margin-bottom: 0px;
  
}

.top-row h1 {
  margin: 80px 0 8px 0;
  font-size: 48px;
  font-weight: bold;
}

.top-row h2 {
  margin: 0 0 50px;
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
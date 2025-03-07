<template>
    <div class="home-container">
        <main class="middle-column">
        <!-- 上排：标题 + 房间分类按钮 -->
        <div class="top-row">
            <h1><strong>DIICSU</strong></h1>
            <h2><strong>Room Booking System</strong></h2>
        </div>
        <div>
          
        </div>
        <!-- 下排：房间卡片 + 底部“Rooms”栏 -->
        <div class="bottom-row">
            <!-- 房间卡片 -->
            <room-display :room-ids="roomIds"/>
        </div>
        </main>

        <!-- 右侧区域（第三列） -->
        <aside class="right-column">
        <h2>My Reservations</h2>
        <router-view name=""></router-view>
        </aside>
    </div>
</template>

<script setup>
import {ref} from "vue";

//TODO filter给数组
const roomIds = ref([1, 3, 5])
import RoomDisplay from '@/components/RoomDisplay.vue';
</script>

<style>
.home-container {
  display: flex;      /* 关键：横向排列子元素 */
  align-items: start; /* 可选：让它们顶对齐 */
  /* 如果想让中间列自适应、右侧固定宽度，可以在这里加 flex: 1; 或宽度 */
}
/* ========== 中间列：上下两排 ========== */
.middle-column {
  display: grid;
  grid-template-rows: auto 1fr;
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

.tab-bar .el-button {
  /* 基础样式 */
  border-radius: 8px !important;  /* 圆角 */
  padding: 12px 20px !important;
  font-weight: 500;
  
  /* 未选中状态（颜色可自定义） */
  background-color: var(--tab-inactive-bg, #F0ECE6) !important; /* 默认白色 */
  border: 1px solid var(--tab-inactive-border, #F0ECE6) !important; 
  color: #000 !important; /* 强制黑色字体 */
}

/* 选中状态（颜色可自定义） */
.tab-bar .active-tab {
  background-color: var(--tab-active-bg, #b29775) !important; /* 默认浅灰 */
  border-color: var(--tab-active-border, #b29775) !important; /* 默认深灰边框 */
}

/* ----- 下排：房间卡片 + 底部“Rooms”栏 ----- */
.bottom-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

/* ========== 右侧列 ========== */
.right-column {
  background-color: #eceef8;
  padding: 20px;
}
</style>
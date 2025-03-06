<template>
  <div class="index-container">
    <!-- 左侧导航栏（第一列） -->
    <aside class="left-column">
      <div class="top-icon"></div>
      <div class="nav-item" @mouseover="hoverNavItem" @mouseleave="leaveNavItem">
        <el-icon><House /></el-icon>
      </div>
      <div class="nav-item" @mouseover="hoverNavItem" @mouseleave="leaveNavItem">
        <el-icon><Bell /></el-icon>
      </div>
      <!-- 底部圆形图标 -->
      <div class="bottom-icon"><el-icon><RefreshRight /></el-icon></div>
      <div class="bottom-icon"><el-icon><Setting /></el-icon></div>
    </aside>

    <!-- 中间主体（第二列，分为上下两排） -->
    <main class="middle-column">
      <!-- 上排：标题 + 房间分类按钮 -->
      <div class="top-row">
        <h1><strong>DIICSU</strong></h1>
        <h2><strong>Room Booking System</strong></h2>

        <!-- 房间分类按钮（Tab） -->
        <div class="tab-bar">
          <el-button
            v-for="(tab, index) in tabs"
            :key="index"
            :class="{ 'active-tab': activeTab === index }"
            @click="activeTab = index"
          >
            {{ tab }}
          </el-button>
        </div>
      </div>

      <!-- 下排：房间卡片 + 底部"Rooms"栏 -->
      <div class="bottom-row">
        <!-- 房间卡片 -->
        <router-view name="roomDetails"></router-view>
      </div>
    </main>

    <!-- 右侧区域（第三列） -->
    <aside class="right-column">
      <h2>My Reservations</h2>
      <router-view name="myReservation"></router-view>
    </aside>
  </div>
</template>

<script>
import { House, Bell, RefreshRight, Setting } from '@element-plus/icons-vue'

export default {
  name: 'Index',
  components: {
    House,
    Bell,
    RefreshRight,
    Setting
  },
  data() {
    return {
      tabs: ['English Rooms', 'Formal Meeting Room', 'Informal Meeting Room', '622', '634', '635'],
      activeTab: 1, // 默认选中第二个 Tab
    };
  },
  methods: {
    hoverNavItem(event) {
      event.target.style.backgroundColor = '#87aade';
      event.target.style.color = '#fff';
    },
    leaveNavItem(event) {
      event.target.style.backgroundColor = '#fff';
      event.target.style.color = '#000';
    },
  },
};
</script>

<style scoped>
/* CSS 变量 */
:root {
  --primary-color: #87aade;
  --secondary-color: #f0f0f0;
  --font-size-large: 48px;
  --font-size-medium: 16px;
}

/* 整体布局 */
.index-container {
  display: grid;
  grid-template-columns: 80px 1fr 300px; /* 左 80px，中间自适应，右 300px */
  height: 100vh;
  background-color: var(--secondary-color);
  overflow: hidden;
}

/* ========== 左侧导航栏 ========== */
.left-column {
  background-color: #F0ECE6;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 0;
  gap: 20px;
  border-right: 1px solid #ddd;
}

.top-icon,
.bottom-icon {
  margin: 20px;
  width: 40px;
  height: 40px;
  background-color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-item {
  width: 40px;
  height: 40px;
  background-color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* ========== 中间列：上下两排 ========== */
.middle-column {
  display: grid;
  grid-template-rows: auto 1fr;
  background-color: #fcf8f6;
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

/* ----- 下排：房间卡片 + 底部"Rooms"栏 ----- */
.bottom-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

/* ========== 右侧列 ========== */
.right-column {
  background-color: #fcf8f6;
  padding: 20px;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .index-container {
    grid-template-columns: 60px 1fr; /* 在小屏幕上隐藏右侧栏 */
  }
  .right-column {
    display: none;
  }
}
</style>
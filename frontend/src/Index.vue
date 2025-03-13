<template>
  <div class="index-container">
    <!-- 左侧导航栏（第一列） -->
    <aside class="left-column">
      <div class="top-icon"></div>

      <div class="nav-items-container">
        <div 
          v-for="(item, index) in navItems" 
          :key="index" 
          class="nav-item"
          :class="{ active: activeNav === index }" 
          @click="setActiveNav(index)"
        >
          <!-- <el-icon><component :is="item.icon" /></el-icon> -->
          <svg-icon type="mdi" :path="$mdi[item.icon]"></svg-icon>
        </div>
      </div>
      <!-- 底部圆形图标 -->
      <div class="bottom-icon"><svg-icon type="mdi" :path="$mdi.mdiExitToApp"></svg-icon></div>
    </aside>
    <component :is="activeComponent" />
  </div>
</template>

<script>
import HomeView from '@/views/HomeView.vue';
import MyReservation from '@/views/MyReservation.vue';
import NotificationView from '@/views/NotificationView.vue';
import SettingsView from '@/views/SettingsView.vue';
export default {
  name: 'Index',
  components:{
    HomeView,
    MyReservation,
    NotificationView,
    SettingsView,
  },
  data() {
    return {
      activeTab: 1, // 默认选中第二个 Tab
      activeNav: 0, // 默认选中第一个导航项
      navItems: [
        { icon: 'mdiHomeOutline',  component: 'HomeView' },
        { icon: 'mdiBellOutline',  component: 'NotificationView'},
        { icon: 'mdiAccountOutline', component: 'MyReservation'},
        { icon: 'mdiCogOutline', component: 'SettingsView'}
      ]
    };
  },
  computed: {
    // 根据 activeNav 动态获取要显示的组件名
    activeComponent() {
      return this.navItems[this.activeNav].component
    }
  },
  methods: {
    setActiveNav(index) {
      this.activeNav = index;
    }
  },
};
</script>

<style scoped>
/* 整体布局 */
.index-container {
  display: grid;
  grid-template-columns: 80px 1fr;  /* 左 80px，中间自适应，右 300px */
  height: 100vh;
  background-color: #eceef8;
  overflow: hidden;
}

/* ========== 左侧导航栏 ========== */
.left-column {
  background-color: #3155ef;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 0;
  height: 100vh;
  border-right: 1px solid #ddd;
  position: relative;
}

.top-icon {
  margin: 20px;
  width: 40px;
  height: 40px;
  background-color: #eceef8;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-items-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 25px;
}

.bottom-icon {
  margin: 20px;
  width: 40px;
  height: 40px;
  background-color: #3155ef;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff
}

.nav-item {
  width: 40px;
  height: 40px;
  background-color: #3155ef;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.nav-item svg {
  color: #fff; /* 如果你的图标库基于 currentColor，图标就会显示为白色 */
}

/* 活跃状态样式 */
.nav-item.active {
  border-radius: 50% 0 0 50%;
  background-color: #eceef8;
}

.nav-item.active svg {
  color: #000;
}

/* 使用伪元素创建向右延伸的连接部分 */
.nav-item.active::after {
  content: "";
  position: absolute;
  width: 20px;  /* 向右延伸的宽度 */
  height: 40px;
  background-color: #eceef8;
  right: -20px;
  z-index: 1;
}

</style>
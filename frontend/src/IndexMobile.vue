<template>
  <div class="index-container">
    <component :is="activeComponent"/>
    <div class="nav-container">
      <nav class="bottom-nav">
        <div
          v-for="(item, index) in navItems"
          :key="index"
          class="nav-item"
          :class="{ active: activeNav === index }"
          @click="setActiveNav(index)">
          <svg-icon type="mdi" :path="$mdi[item.icon]"></svg-icon>
        </div>
      </nav>
    </div>
  </div>
</template>

<script>
import HomeViewMobile from './views/HomeViewMobile.vue';
import MyReservationMobile from './views/MyReservation.vue';
import NotificationViewMobile from './views/NotificationView.vue';
import SettingsViewMobile from './views/SettingsView.vue';

export default {
  name: 'IndexMobile',
  components: {
    HomeViewMobile,
    MyReservationMobile,
    NotificationViewMobile,
    SettingsViewMobile,
  },
  data() {
    return {
      activeNav: 0,
      navItems: [
        { icon: 'mdiHomeOutline', component: 'HomeViewMobile' },
        { icon: 'mdiBellOutline', component: 'NotificationViewMobile' },
        { icon: 'mdiAccountOutline', component: 'MyReservationMobile' },
        { icon: 'mdiCogOutline', component: 'SettingsViewMobile' }
      ]
    };
  },
  computed: {
    activeComponent() {
      return this.navItems[this.activeNav].component;
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
.index-container {
  background-color: #eceef8;
  overflow: hidden;
  position: relative;
}

.nav-container {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 50px;
  background-color: #eceef8;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* 底部导航栏样式 */
.bottom-nav {
  width: 100%;
  height: 50px;
  background-color: #3155ef;
  border-radius: 10px 10px 0 0;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

/* 导航项 */
.nav-item {
  height: 100%;
  width: 25%;
  flex: 1;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

/* 图标大小等比缩放 */
.nav-item svg {
  padding-top: 10px;
  padding-bottom: 10px;
  height: 100%;
  width: 100%;
  color: #fff;
}

/* 活跃状态 */
.nav-item.active svg {
  color: #000;
  background: url('assets/nav-icon-selected.svg') no-repeat center bottom;
  background-size: 90% 90%;
}
</style>

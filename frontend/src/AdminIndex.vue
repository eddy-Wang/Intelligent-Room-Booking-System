<template>
  <div class="index-container">
    <!-- left column -->
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
          <svg-icon type="mdi" :path="$mdi[item.icon]"></svg-icon>
        </div>
      </div>
      <!-- botton icon -->
      <div class="bottom-icon"><svg-icon type="mdi" :path="$mdi.mdiExitToApp"></svg-icon></div>
    </aside>
    <component :is="activeComponent" />
  </div>
</template>

<script>
import AdminHomeView from "@/views/AdminHomeView.vue";
import MyReservation from '@/views/MyReservation.vue';
import ReservationManagement from '@/views/ReservationManagement.vue';
import RoomManagementView from '@/views/RoomManagementView.vue';
export default {
  name: 'Index',
  components:{
    AdminHomeView,
    MyReservation,
    ReservationManagement,
    RoomManagementView,
  },
  data() {
    return {
      activeTab: 1,
      activeNav: 0,
      navItems: [
        { icon: 'mdiHomeOutline',  component: 'AdminHomeView' },
        { icon: 'mdiApplicationEditOutline',  component: 'ReservationManagement'},
        { icon: 'mdiClipboardTextOutline', component: 'RoomManagementView'},
        { icon: 'mdiBookAccountOutline', component: 'MyReservation'},

      ]
    };
  },
  computed: {
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
  grid-template-columns: 80px 1fr;
  height: 100vh;
  background-color: #eceef8;
  overflow: hidden;
}

/* ========== left navigator========== */
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
  color: #fff;
}

.nav-item.active {
  border-radius: 50% 0 0 50%;
  background-color: #eceef8;
}

.nav-item.active svg {
  color: #000;
}


.nav-item.active::after {
  content: "";
  position: absolute;
  width: 20px;
  height: 40px;
  background-color: #eceef8;
  right: -20px;
  z-index: 1;
}

</style>

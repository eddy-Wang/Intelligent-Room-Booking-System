<template>
  <div class="index-container">
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
      <div class="bottom-icon">
        <svg-icon type="mdi" :path="$mdi.mdiExitToApp"></svg-icon>
      </div>
    </aside>
    <component :is="activeComponent"/>
  </div>
</template>

<script>
import HomeView from '@/views/HomeView.vue';
import MyReservation from '@/views/MyReservation.vue';
import * as $mdi from "@mdi/js";
import RoomRepair from "@/views/RoomRepair.vue";

export default {
  name: 'Index',
  components: {
    HomeView,
    MyReservation,
    RoomRepair,
  },
  data() {
    return {
      activeTab: 1,
      activeNav: 0,
      navItems: [
        {icon: 'mdiHomeOutline', component: 'HomeView'},
        {icon: 'mdiAccountOutline', component: 'MyReservation'},
        {icon: 'mdiTools', component: 'RoomRepair'},
      ]
    };
  },
  computed: {
    $mdi() {
      return $mdi
    },
    activeComponent() {
      return this.navItems[this.activeNav].component
    }
  },
  methods: {
    setActiveNav(index) {
      this.activeNav = index;
      console.log(index)
    }
  },
};
</script>

<style scoped>

.index-container {
  font-family: 'Cambria', serif;
  display: grid;
  grid-template-columns: 80px 1fr;
  height: 100vh;
  background-color: #eceef8;
}

.left-column {
  background-color: #3155ef;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 20px;
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
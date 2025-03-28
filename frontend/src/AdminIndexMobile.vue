<!--
AdminIndexMobile.vue - Mobile admin dashboard with bottom navigation bar.

Features:
- Bottom navigation for mobile devices
- Dynamic component loading
- Back navigation functionality
- Responsive design optimized for mobile

Props: None
Events: None
Dependencies:
- Vue Router for navigation
- @mdi/js for Material Design icons
- Custom SvgIcon component
- Mobile view components for each section
-->
<template>
  <div class="index-container">
    <!-- Dynamic component area -->
    <component :is="activeComponent"/>
    <!-- Bottom navigation bar -->
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
import RoomManagementViewMobile from "@/views/RoomManagementViewMobile.vue";
import RoomIssueManagementMobile from "@/views/RoomIssueManagementMobile.vue";
import ReservationManagementMobile from "@/views/ReservationManagementMobile.vue";
import BlacklistViewMobile from "@/views/BlacklistViewMobile.vue";

export default {
  name: 'IndexMobile',
  components: {
    RoomManagementViewMobile,
    RoomIssueManagementMobile,
    ReservationManagementMobile,
    BlacklistViewMobile,
  },
  data() {
    return {
      activeNav: 1,
      navItems: [
        {icon: 'mdiArrowLeft'},
        {icon: 'mdiApplicationEditOutline', component: 'ReservationManagementMobile'},
        {icon: 'mdiTools', component: 'RoomIssueManagementMobile'},
        {icon: 'mdiClipboardTextOutline', component: 'RoomManagementViewMobile'},
        {icon: 'mdiFileCancelOutline', component: 'BlacklistViewMobile'}
      ]
    };
  },
  computed: {
    /**
     * Returns the currently active component based on navigation selection
     * @returns {Component} The active component
     */
    activeComponent() {
      return this.navItems[this.activeNav].component;
    }
  },
  methods: {
    /**
     * Sets the active navigation item or handles back navigation
     * @param {number} index - Index of the navigation item
     */
    setActiveNav(index) {
      if (index === 0) {
        this.$router.back();
      } else {
        this.activeNav = index;
      }
    }
  },
};
</script>

<style scoped>
.index-container {
  background-color: #eceef8;
  position: relative;
  font-family: 'Cambria', serif;
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

.bottom-nav {
  width: 100%;
  height: 50px;
  background-color: #3155ef;
  border-radius: 10px 10px 0 0;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.nav-item {
  height: 100%;
  width: 25%;
  flex: 1;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-item svg {
  padding-top: 10px;
  padding-bottom: 10px;
  height: 100%;
  width: 100%;
  color: #fff;
}

.nav-item.active svg {
  color: #000;
  background: url('assets/nav-icon-selected.svg') no-repeat center bottom;
  background-size: 90% 90%;
}
</style>

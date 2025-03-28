<!--
IndexMobile.vue - Mobile application with bottom navigation bar and role-based UI.

Features:
- Bottom navigation optimized for mobile devices
- Dynamic component loading based on navigation selection
- Role-based navigation items (Admin vs Student)
- Back navigation functionality for Admin users
- Logout functionality for Student users
- Responsive design for mobile screens

Props: None
Events: None
Dependencies:
- Vue Router for navigation
- @mdi/js for Material Design icons
- Custom SvgIcon component
- Mobile view components for each section
- User permission system ($user)
-->
<template>
  <div class="index-container">
    <!-- Dynamic component area - shows current view -->
    <component :is="activeComponent"/>
    <!-- Bottom navigation bar -->
    <div class="nav-container">
      <nav class="bottom-nav">
        <!-- Navigation items loop -->
        <div
            v-for="(item, index) in navItems"
            :key="index"
            class="nav-item"
            :class="{ active: activeNav === index }"
            @click="setActiveNav(index)">
          <!-- Navigation icon -->
          <svg-icon type="mdi" :path="$mdi[item.icon]"></svg-icon>
        </div>
        <!-- Logout button (only shown for Student users) -->
        <div
            v-if="permission === 'Student'"
            class="nav-item logout-item"
            @click="handleLogout">
          <svg-icon type="mdi" :path="$mdi.mdiExitToApp"></svg-icon>
        </div>
      </nav>
    </div>
  </div>
</template>

<script>
import HomeViewMobile from '@/views/HomeViewMobile.vue';
import MyReservationMobile from '@/views/MyReservationMobile.vue';
import RoomRepairMobile from '@/views/RoomRepairMobile.vue';

export default {
  name: 'IndexMobile',
  components: {
    HomeViewMobile,
    MyReservationMobile,
    RoomRepairMobile,
  },
  data() {
    return {
      activeNav: this.$user && this.$user.permission === 'Admin' ? 1 : 0,
      adminNavItems: [
        {icon: 'mdiArrowLeft'},
        {icon: 'mdiHomeOutline', component: 'HomeViewMobile'},
        {icon: 'mdiAccountOutline', component: 'MyReservationMobile'},
        {icon: 'mdiTools', component: 'RoomRepairMobile'}
      ],
      userNavItems: [
        {icon: 'mdiHomeOutline', component: 'HomeViewMobile'},
        {icon: 'mdiAccountOutline', component: 'MyReservationMobile'},
        {icon: 'mdiTools', component: 'RoomRepairMobile'}
      ]
    };
  },
  computed: {
    /**
     * Returns current user permission level
     * @returns {string} User permission ('Admin' or 'Student')
     */
    permission() {
      return this.$user ? this.$user.permission : 'Student';
    },
    /**
     * Returns navigation items based on user role
     * @returns {Array} Appropriate navigation items array
     */
    navItems() {
      return this.permission === 'Admin' ? this.adminNavItems : this.userNavItems;
    },
    /**
     * Returns the currently active component
     * @returns {Component} The active component based on navigation
     */
    activeComponent() {
      return this.navItems[this.activeNav].component;
    }
  },
  methods: {
    /**
     * Sets active navigation or handles back navigation for Admin
     * @param {number} index - Index of the navigation item
     */
    setActiveNav(index) {
      if (this.permission === 'Admin' && index === 0) {
        this.$router.back();
      } else {
        this.activeNav = index;
      }
    },
    /**
     * Handles logout confirmation and redirects to login page
     */
    handleLogout() {
      if (confirm('Are you sure you want to logout?')) {
        this.$user = null;
        this.$router.push({name: 'LoginView'});
        console.log('User logged out');
      }
    }
  }
};
</script>

<style scoped>
.index-container {
  font-family: 'Cambria', serif;
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

.logout-item {
  height: 100%;
  width: 25%;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-item svg {
  padding-top: 10px;
  padding-bottom: 10px;
  height: 100%;
  width: 100%;
  color: #fff;
}
</style>

<!--
Index.vue - Desktop admin dashboard with left navigation sidebar.

Features:
- Fixed left navigation sidebar with icons
- Dynamic component loading
- Hover tooltips for navigation items
- Smooth transitions and animations
- Responsive design optimized for desktop
- Logout functionality

Props: None
Events: None
Dependencies:
- Vue Router for navigation
- @mdi/js for Material Design icons
- Custom SvgIcon component
- View components for each section
-->
<template>
  <div class="index-container">
    <!-- Left navigation sidebar -->
    <aside
        class="left-column"
        role="navigation"
        aria-label="Main navigation"
    >
      <!-- Home/Logo button at top -->
      <router-link
          to="/index"
          class="top-icon"
          aria-label="Return to homepage"
      >
        <img
            src="../src/assets/diiLogo.png"
            alt="Company Logo"
            class="logo-image"
            @click="setActiveNav(0)"
        >
      </router-link>

      <!-- Navigation items container -->
      <nav class="nav-items-container">
        <button
            v-for="(item, index) in navItems"
            :key="index"
            class="nav-item"
            role="menuitem"
            :class="{
            active: activeNav === index,
          }"
            @click="setActiveNav(index)"
            @mouseenter="hoverIndex = index"
            @mouseleave="hoverIndex = null"
            :data-index="index"
            :aria-label="item.label"
            :aria-current="activeNav === index ? 'page' : null"
        >
          <svg-icon
              type="mdi"
              :path="$mdi[item.icon]"
              class="nav-icon"
          ></svg-icon>

          <span
              v-if="hoverIndex === index"
              class="tooltip"
          >
            {{ item.label }}
          </span>
        </button>
      </nav>
      <!-- Logout button at bottom -->
      <button
          class="bottom-icon"
          @click="handleLogout"
          aria-label="Logout"
      >
        <svg-icon
            type="mdi"
            :path="$mdi.mdiExitToApp"
            class="logout-icon"
        ></svg-icon>
      </button>
    </aside>
    <!-- Main content area -->
    <main class="main-content">
      <component :is="activeComponent"/>
    </main>
  </div>
</template>

<script>
import HomeView from "@/views/HomeView.vue";
import MyReservation from '@/views/MyReservation.vue';
import router from "@/router/index.js";
import RoomRepair from "@/views/RoomRepair.vue";

export default {
  name: 'Index',
  components: {
    HomeView,
    MyReservation,
    RoomRepair
  },
  data() {
    return {
      activeNav: 0, // Currently active navigation index
      hoverIndex: null, // Index of hovered navigation item
      navItems: [
        {
          icon: 'mdiHomeOutline',
          component: 'HomeView',
          label: 'Home',
        },
        {
          icon: 'mdiAccountOutline',
          component: 'MyReservation',
          label: 'My Reservations',
        },
        {
          icon: 'mdiTools',
          component: 'RoomRepair',
          label: 'Report Room Issue',
        },
      ]
    };
  },
  computed: {
    /**
     * Returns the currently active component based on navigation selection
     * @returns {Component} The active component
     */
    activeComponent() {
      return this.navItems[this.activeNav].component
    }
  },
  methods: {
    /**
     * Sets the active navigation item
     * @param {number} index - Index of the navigation item
     */
    setActiveNav(index) {
      this.activeNav = index;
    },
    /**
     * Handles logout confirmation and redirects to login page
     */
    handleLogout() {
      if (confirm('Are you sure you want to logout?')) {
        router.push({name: 'LoginView'});
        console.log('User logged out')
      }
    }
  }
};
</script>

<style scoped>
.index-container {
  font-family: 'Cambria', serif;
  display: grid;
  grid-template-columns: 80px 1fr;
  height: 100vh;
  background-color: #eceef8;
  overflow: hidden;
}

.left-column {
  background: linear-gradient(180deg, #3155ef 0%, #1a3cd6 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
  height: 100vh;
  box-shadow: 4px 0 15px rgba(0, 0, 0, 0.1);
  position: relative;
}

.top-icon {
  margin: 20px;
  width: 50px;
  height: 50px;
  background-color: #eceef8;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  transition: transform 0.3s;
}

.top-icon:hover {
  transform: scale(1.1);
}

.logo-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.nav-items-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1.5rem;
  padding: 1rem 0;
  position: relative;
  z-index: 100;
}

.nav-item {
  width: 56px;
  height: 56px;
  background-color: transparent;
  border: none;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.nav-icon {
  width: 1.75rem;
  height: 1.75rem;
  color: #fff;
  transition: transform 0.2s;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.15) !important;
  transform: translateY(-2px);
}

.nav-item.active {
  background: #fff !important;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(49, 85, 239, 0.3);
}

.nav-item.active .nav-icon {
  color: #3155ef !important;
}

.tooltip {
  position: absolute;
  left: calc(100% + 15px);
  top: 50%;
  transform: translateY(-50%);
  background: #fff;
  color: #3155ef;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 0.9rem;
  white-space: nowrap;
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
  pointer-events: none;
  z-index: 100;
  font-family: Arial, sans-serif;

}

.tooltip::before {
  content: '';
  position: absolute;
  left: -6px;
  top: 50%;
  transform: translateY(-50%);
  border-right: 6px solid #fff;
  border-top: 6px solid transparent;
  border-bottom: 6px solid transparent;
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(0.95);
  }
}

.bottom-icon {
  margin: 20px;
  width: 40px;
  height: 40px;
  background-color: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.bottom-icon:hover {
  background-color: rgba(255, 255, 255, 0.2) !important;
  transform: rotate(90deg);
}

.logout-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: #fff;
}

.main-content {
  height: 100vh;
}
</style>
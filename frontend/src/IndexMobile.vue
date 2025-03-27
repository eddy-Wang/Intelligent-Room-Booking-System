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
    permission() {
      return this.$user ? this.$user.permission : 'Student';
    },
    navItems() {
      return this.permission === 'Admin' ? this.adminNavItems : this.userNavItems;
    },
    activeComponent() {
      return this.navItems[this.activeNav].component;
    }
  },
  methods: {
    setActiveNav(index) {
      if (this.permission === 'Admin' && index === 0) {
        this.$router.back();
      } else {
        this.activeNav = index;
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
</style>

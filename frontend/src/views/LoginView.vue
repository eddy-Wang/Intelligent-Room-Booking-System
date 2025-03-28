<!--
LoginPage.vue - Landing page for DIICSU Room Booking System.

This component provides:
- Welcome screen with system branding
- Sign in button to begin authentication flow
- Responsive layout with background image
- Mobile-optimized design

Props: None
Events: None
Dependencies: Vue Router
-->
<template>
  <div class="app-container">
    <div class="main-content">
       <!-- Left content section with welcome message and sign in button -->
      <div class="left-content">
        <div class="header">
          <img src="../assets/header-logo.png" alt="DIICSU Header Logo" class="header-logo">
        </div>
        <!-- Welcome message section -->
        <h1 class="welcome-text">Welcome to</h1>
        <h2 class="system-name">DIICSU Room Booking System</h2>
        <p class="slogan">"Book Smarter: Real-Time Room Reservations for DIICSU."</p>
         <!-- Sign in button -->
        <button @click="handleSignIn" class="sign-in-button">
          Sign In
        </button>
      </div>
      <!-- Right content section with background image -->
      <div class="right-content">
        <img src="../assets/DIICSUPicture.png" alt="DIICSU Building" class="diicsu-picture">
      </div>
    </div>
  </div>
</template>

<script setup>
import {useRouter} from 'vue-router'

const router = useRouter()
/**
 * Handles sign in button click
 * Navigates to email authentication page
 */
const handleSignIn = () => {
  router.push('./email')
}
</script>

<style scoped>
/* Base reset styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Arial, sans-serif;
}
/* Main container styles */
.app-container {
  font-family: 'Cambria', serif;
  min-height: 100vh;
  background: #3155ef;
  display: flex;
  justify-content: space-between;
}

.main-content {
  flex: 1;
  display: flex;
  align-items: center;
}
/* Left content (welcome message) styling */
.left-content {
  flex: 0 0 50%;
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 40px 4rem 0;

  .header {
    max-width: 400px;
    left: 60px;
    width: 100%;
    margin-bottom: 30%;
  }

  .header-logo {
    height: 45px;
    width: auto;
  }
  /* Welcome text styling */
  .welcome-text {
    width: 100%;
    color: white;
    font-size: 3.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    margin-left: 20%;
  }
  /* System name styling */
  .system-name {
    width: 100%;
    color: white;
    font-size: 2.5rem;
    font-weight: 500;
    margin-bottom: 1rem;
    margin-left: 20%;
  }
  /* Slogan text styling */
  .slogan {
    width: 100%;
    color: white;
    font-size: 1.2rem;
    margin-bottom: 3rem;
    font-style: italic;
    opacity: 0.9;
    margin-left: 20%;
  }
  /* Sign in button styling */
  .sign-in-button {
    background: #5fb2fa;
    box-shadow: 0 4px 15px 0 rgba(41, 44, 225, 0.75);
    border: 0;
    text-transform: uppercase;
    font-size: 20px;
    font-weight: bold;
    padding: 15px 50px;
    border-radius: 50px;
    color: #FFFFFF;
    outline: none;
    position: relative;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 60%;
    margin-left: 20%;
  }

  /* Hover state */
  .sign-in-button:hover {
    background-image: linear-gradient(to right, #319efd, #7db3ff);
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(79, 172, 254, 0.9);
  }

  /* Active/pressed state */
  .sign-in-button:active {
    transform: translateY(1px);
    box-shadow: 0 2px 10px rgba(79, 172, 254, 0.6);
  }
}
/* Right content (image) styling */
.right-content {
  flex: 1;
  width: 40%;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  height: 100vh;
  padding: 2rem;
}

.diicsu-picture {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 20px;
}
/* Mobile responsive styles */
@media (max-width: 768px) {
  .app-container {
    padding: 0;
    min-height: 100vh;
  }

  .main-content {
    flex-direction: column;
    padding: 0;
    gap: 0;
    height: 100vh;
    position: relative;
  }

  /* Mobile header adjustments */
  .header {
    max-width: 400px;
    left: 60px;
    width: 100%;
    margin-bottom: 30%;
  }

  .header-logo {
    height: 45px;
    width: auto;
  }

  /* Mobile left content adjustments */
  .left-content {
    position: relative;
    z-index: 2;
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    width: 90%;
    margin: 0 auto;
    text-align: center;
    top: 50%;
    transform: translateY(-50%);

    /* Text size adjustments for mobile */
    .welcome-text {
      font-size: 2.2rem;
      margin-bottom: 1rem;
      margin-left: 0 ;
    }

    .system-name {
      font-size: 2rem;
      margin-bottom: 2rem;
      margin-left: 0 ;
    }

    .slogan {
      font-size: 1.1rem;
      margin-bottom: 2rem;
      margin-left: 0 ;
    }

    /* Button adjustments for mobile */
    .sign-in-button {
      width: 100%;
      max-width: 300px;
      padding: 1rem 2rem;
      font-size: 1rem;
      margin: 20% auto 20% 0;
    }
  }

  /* Mobile right content (background image) adjustments */
  .right-content {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    padding: 0;
    margin: 0;
  }

  /* Dark overlay for better text readability on mobile */
  .right-content::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    z-index: 2;
  }


  /* Image adjustments for mobile */
  .diicsu-picture {
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0.8;
    border-radius: 0;
  }
}

</style>
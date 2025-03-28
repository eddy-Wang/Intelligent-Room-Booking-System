<!--
VerifyView.vue - Component for email verification code entry.

Features:
- Two-column layout (single column on mobile)
- Verification code input with validation
- Responsive design with mobile adaptation
- Back button navigation
- Dynamic routing based on user permission
- Visual feedback for disabled states

Props: None
Events: None
Dependencies:
- Vue Router for navigation
- Element Plus for notifications
- @jamescoyle/vue-icon for SVG icons
- @mdi/js for Material Design icons
-->
<template>
  <!-- Main application container -->
  <div class="app-container">
    <div class="main-content">
      <div class="left-content">
        <div class="header">
          <img src="../assets/header-logo.png" alt="DIICSU Header Logo" class="header-logo">
        </div>
        <!-- Verification form container -->
        <div class="input-button-container">
          <h1 class="title">Verify Your Code</h1>
          <p class="subtitle">Please enter the verification code sent to your email</p>

          <!-- Verification code input group -->
          <div class="input-group">
            <input
                type="text"
                v-model="verificationCode"
                class="verification-input"
                placeholder="Enter verification code:"
                maxlength="6"
            >
          </div>
          <!-- Verify button -->
          <div class="button-container">
            <button
                @click="handleVerify"
                class="verify-button"
                :disabled="!isValidCode"
                :class="{ 'button-disabled': !isValidCode }"
            >
              <span class="button-text">VERIFY</span>
            </button>
          </div>
        </div>
        <!-- Back button -->
        <div class="back-button-container">
          <button
              @click="handleBack"
              class="back-button"
          >
            <svg-icon type="mdi" :path="path" class="back-icon"></svg-icon>
          </button>
        </div>
      </div>

      <!-- Right content section (image) -->
      <div class="right-content">
        <img src="../assets/DIICSUPicture.png" alt="DIICSU Building" class="diicsu-picture">
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, getCurrentInstance} from 'vue'
import {useRouter, useRoute} from 'vue-router'
import {ElMessage} from "element-plus";
import SvgIcon from '@jamescoyle/vue-icon';
import {mdiKeyboardBackspace} from '@mdi/js';
/**
 * Component initialization
 */
const vueInstance = getCurrentInstance()
const backendAddress = vueInstance.appContext.config.globalProperties.$backendAddress
const router = useRouter()
const route = useRoute()
// Get email from route params
const email = route.params.email

// Reactive data properties
const verificationCode = ref('')
const path = ref(mdiKeyboardBackspace)
/**
 * Computed property to check if verification code is valid
 * @returns {boolean} True if code length is exactly 6 characters
 */
const isValidCode = computed(() => verificationCode.value.length === 6)
/**
 * Handles verification code submission
 * @async
 */
const handleVerify = async () => {
  if (isValidCode.value) {
    try {
      // Send verification request to backend
      const response = await fetch(backendAddress + '/verify-code', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: email,
          code: verificationCode.value
        })
      });
      // Handle HTTP errors
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      // Process response
      const data = await response.json();
      if (data.code === "000") {
        const userPermission = data.data.permission
        if (window.innerWidth <= 768) {
          if (userPermission === "Admin") {
            await router.push({path: "../AdminEnterPageMobile"})
          } else {
            await router.push({path: "../IndexMobile"})
          }
        } else {
          if (userPermission === "Admin") {
            await router.push({path: "../AdminIndex"})
          } else {
            await router.push({path: "../Index"})
          }
        }
      } else {
        ElMessage.error(data.message)
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }
}
/**
 * Handles back button click - navigates to email entry page
 */
const handleBack = () => {
  router.push('/email')
}
</script>

<style scoped>
/* Base reset and typography */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Arial, sans-serif;
}
/* Main container styling */
.app-container {
  font-family: 'Cambria', serif;
  min-height: 100vh;
  background: #3155ef;
  display: flex;
  justify-content: space-between;
}
/* Main content area layout */
.main-content {
  flex: 1;
  display: flex;
  align-items: center;
}
/* Left content section styling (form area) */
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

  .title {
    font-size: 2.8rem;
    font-weight: 700;
    margin-bottom: 1.2rem;
    color: white;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    letter-spacing: -0.5px;
    text-align: center;
  }

  .subtitle {
    font-size: 1.2rem;
    opacity: 0.95;
    margin-bottom: 2.5rem;
    color: white;
    line-height: 1.6;
    text-align: center;
  }

  .input-group {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 50px;
    padding: 0.5rem 1rem;
    margin: 0 auto;
    max-width: 400px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    border: 2px solid transparent;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
    }
  }
  /* Verification input field */
  .verification-input {
    flex: 1;
    border: none;
    background: none;
    padding: 0.8rem;
    font-size: 1.1rem;
    color: #333;
    outline: none;
    width: 60%;

    &::placeholder {
      color: #999;
    }
  }

  .back-button {
    position: absolute;
    left: 2rem;
    bottom: 1rem;
    margin-left: 20px;
    margin-bottom: 20px;
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
    width: auto;
    height: auto;
  }

  .back-icon {
    width: 3.5em;
    height: 3.5em;
    color: white;
    transition: color 0.3s ease;
  }

  .back-button:hover .back-icon {
    color: rgba(255, 255, 255, 0.8);
  }

  .button-container {
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
    position: relative;
    padding: 0;
  }
  /* Verify button styles */
  .verify-button {
    background: #319efd;
    color: #FFFFFF;
    box-shadow: 0 4px 15px 0 rgba(41, 44, 225, 0.75);
    border: 0;
    margin: 20px auto;
    text-transform: uppercase;
    font-size: 20px;
    font-weight: bold;
    padding: 15px 50px;
    border-radius: 50px;
    outline: none;
    position: relative;
    cursor: pointer;
    transition: all 0.3s ease;
    display: block;
    width: 100%;
    max-width: 400px;
  }

  .button-text {
    transition: opacity 0.3s ease;
  }

  /* Disabled button state */
  .button-disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background-color: rgba(255, 255, 255, 0.8);
  }
}

/* Right content section (image area) */
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

    .input-button-container {
      width: 100%;
      min-height: 47%;
      padding: 2rem 2.5rem 2.5rem 2rem;
      background-color: rgba(49, 85, 239, 0.68);
      border-radius: 2.5rem;
    }
    /* Mobile typography adjustments */
    .title {
      font-size: 2rem;
      margin-bottom: 1rem;
    }

    .subtitle {
      font-size: 1.1rem;
      margin-bottom: 2rem;
    }
    /* Mobile input adjustments */
    .input-group {
      margin: 0 auto 1rem;
      width: 100%;
      max-width: 300px;
      padding: 0.4rem 1rem;
    }

    .verification-input {
      font-size: 0.95rem;
      padding: 0.3rem 0 0.3rem 0.3rem;
      width: 60%;
    }
    /* Mobile button adjustments */
    .button-container {
      max-width: 300px;
      margin: 0 auto;
      padding: 0;
    }

    .verify-button {
      text-align: center;
      width: 100%;
      max-width: 300px;
      height: 30%;
      padding: 1rem 2rem;
      font-size: 1rem;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .button-disabled {
      opacity: 1;
      cursor: not-allowed;
      background: rgba(213, 221, 255, 0.8);
    }
    /* Mobile back button adjustments */
    .back-button-container {
      position: fixed;
      left: 1rem;
      bottom: 1rem;
      z-index: 1000;
    }

    .back-button {
      position: static;
      margin: 0;
      background: none;
      border: none;
      padding: 0;
      cursor: pointer;
    }

    .back-icon {
      width: 1.4em;
      height: 1.4em;
      font-size: 2.5rem;
      color: #ffffff;
    }

    .back-button:hover .back-icon {
      color: rgba(49, 85, 239, 0.8);
    }
  }
  /* Mobile right content adjustments */
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
  /* Overlay for background image on mobile */
  .right-content::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    z-index: 2;
  }

  .diicsu-picture {
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0.7;
    border-radius: 0;
  }
}
/* Animation for form container */
.input-button-container {
  transition: transform 0.5s ease-in-out;
}
</style>

<template>
  <div class="header">
    <img src="../assets/header-logo.png" alt="DIICSU Header Logo" class="header-logo">
  </div>
  <div class="app-container">
    <div class="main-content">
      <div class="left-content">
        <h1 class="welcome-text">Welcome to</h1>
        <h2 class="system-name">DIICSU Room Booking System</h2>
        <p class="slogan">"Book Smarter: Real-Time Room Reservations for DIICSU."</p>
        <button @click="handleSignIn" class="sign-in-button">
          Sign In
        </button>
      </div>

      <div class="right-content">
        <img src="../assets/DIICSUPicture.png" alt="DIICSU Building" class="diicsu-picture">
      </div>

    </div>
  </div>
</template>

<script setup>
import {useRouter} from 'vue-router'

const router = useRouter()

const handleSignIn = () => {
  router.push('./email')
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Arial, sans-serif;
}

.header {
  position: fixed;
  max-width: 400px;
  top: 40px;
  left: 60px;
}

.app-container {
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
.header {
    background: #3155ef;
    width: 100%;
  }

  .header-logo {
    height: 45px;
    width: auto;
  }

.left-content {
  flex: 0 0 50%;
  padding: 0 4rem;

  .welcome-text {
    width: 100%;
    color: white;
    font-size: 3.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }

  .system-name {
    width: 100%;
    color: white;
    font-size: 2.8rem;
    font-weight: 500;
    margin-bottom: 1rem;
  }

  .slogan {
    width: 100%;
    color: white;
    font-size: 1.2rem;
    margin-bottom: 3rem;
    font-style: italic;
    opacity: 0.9;
  }

  .sign-in-button {
    width: 100%;
    background: #E8E8E8;
    color: #333;
    border: none;
    padding: 0.8rem 3rem;
    border-radius: 50px;
    font-size: 1.2rem;
    cursor: pointer;
    transition: all 0.3s ease;
    min-width: 200px;
    text-align: center;
  }

  .sign-in-button:hover {
    background: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }

  .sign-in-button:active {
    transform: translateY(0);
  }


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

  @media (max-width: 768px) {
    .app-container {
      padding: 0;
      min-height: 100vh;
      background: #3155ef;
    }

    .main-content {
      flex-direction: column;
      padding: 0;
      gap: 0;
      height: 100vh;
    }

    .header {
      position: static;
      padding: 1rem;
      margin-bottom: 0;
      text-align: center;
    }

    .left-content {
      flex: 1;
      width: 100%;
      padding: 2rem 1.5rem;
      text-align: center;
      display: flex;
      flex-direction: column;
      justify-content: center;

      .welcome-text {
        font-size: 2rem;
        margin-bottom: 1rem;
      }

      .system-name {
        font-size: 1.8rem;
        margin-bottom: 1rem;
      }

      .slogan {
        font-size: 1.1rem;
        margin-bottom: 2rem;
      }

      .sign-in-button {
        width: 100%;
        max-width: 300px;
        padding: 1rem 2rem;
        font-size: 1rem;
        margin: 0 auto;
      }
    }

    .right-content {
      width: 100%;
      height: 40vh;
      padding: 0;
      margin-top: 0;
    }

    .diicsu-picture {
      width: 100%;
      height: 100%;
      border-radius: 0;
      object-fit: cover;
    }
  }
}

</style>
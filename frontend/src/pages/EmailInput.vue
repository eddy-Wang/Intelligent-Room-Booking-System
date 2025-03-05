<template>
  <div class="header">
    <img src="../assets/header-logo.png" alt="DIICSU Header Logo" class="header-logo">
  </div>
  <div class="app-container">
    <div class="main-content">
      <div class="left-content">
        <div class="input-button-container">
          <h1 class="title">Verify your identification</h1>
          <p class="subtitle">Please enter your Dundee email address to continue</p>

          <div class="input-group">
            <input
                type="email"
                v-model="email"
                class="email-input"
                placeholder="your email address"
                :class="{ 'error': showError }"
                @input="validateEmail"
            >
            <span class="email-suffix">@dundee.ac.uk</span>
          </div>

          <p class="error-message" v-if="showError">
            Please enter a valid Dundee University email address
          </p>

          <div class="button-container">
            <button
                @click="handleNext"
                class="next-button"
                :class="{ 'button-disabled': !isValidEmail  }"
                :disabled="!isValidEmail"
            >
              <span class="button-text">{{ 'SEND CODE' }}</span>
            </button>
          </div>
        </div>
      </div>

      <div class="right-content">
        <img src="../assets/DIICSUPicture.png" alt="DIICSU Building" class="diicsu-picture">
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed} from 'vue'
import {useRouter} from 'vue-router'

const router = useRouter()
const email = ref('')
const showError = ref(false)
const isTransitioning = ref(false)

const isValidEmail = computed(() => {
  return email.value.length > 0 && !showError.value
})

const validateEmail = () => {
  const emailPattern = /^[a-zA-Z0-9._%+-]+@dundee\.ac\.uk$/
  showError.value = !emailPattern.test(email.value + '@dundee.ac.uk')
}

const handleNext = () => {
  if (isValidEmail.value) {
    isTransitioning.value = true
    setTimeout(() => {
      router.push('/verify')
    }, 500)
  }
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

  .title {
    font-size: 2.8rem;
    font-weight: 700;
    margin-bottom: 1.2rem;
    color: white;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    letter-spacing: -0.5px;
  }

  .subtitle {
    font-size: 1.2rem;
    opacity: 0.95;
    margin-bottom: 2.5rem;
    color: white;
    line-height: 1.6;
  }

  .input-group {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 50px;
    padding: 0.5rem 1rem;
    max-width: 400px;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    border: 2px solid transparent;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
    }
  }

  .email-input {
    flex: 1;
    border: none;
    background: none;
    padding: 0.8rem;
    font-size: 1.1rem;
    color: #333;
    outline: none;

    &::placeholder {
      color: #999;
    }
  }

  .email-suffix {
    color: #666;
    font-size: 1rem;
    padding: 0;
    font-weight: 500;
  }

  .error-message {
    color: #FFE5E5;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
    background: rgba(255, 255, 255, 0.1);
    padding: 1rem 1.5rem;
    border-radius: 12px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    animation: fadeIn 0.3s ease-in-out;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  }

  .button-container {
    width: 100%;
    max-width: 400px;
    margin: 0 0 0 0;
    position: relative;
    padding: 0 0 0 0;
  }

  .next-button {
    background: rgba(255, 255, 255, 0.95);
    color: #3155ef;
    border: none;
    padding: 1.2rem 3rem;
    border-radius: 50px;
    font-size: 1.1rem;
    cursor: pointer;
    width: 170px;
    text-align: center;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    position: relative;

    &:hover:not(.button-disabled) {
      background: white;
      transform: translateY(-2px);
      box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
    }
  }

  .button-text {
    transition: opacity 0.3s ease;
  }

  .button-disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background: rgba(255, 255, 255, 0.8);
  }
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

    .title {
      font-size: 2rem;
      margin-bottom: 1rem;
    }

    .subtitle {
      font-size: 1.1rem;
      margin-bottom: 2rem;
    }

    .input-group {
      margin: 0 auto 1rem;
      width: 100%;
      max-width: 300px;
      padding: 0.4rem 1rem;
    }

    .email-input {
      font-size: 0.95rem;
      padding: 0.6rem;
      width: 60%;
    }

    .email-suffix {
      font-size: 0.7rem;
      padding: 0;
      width: 40%;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .button-container {
      max-width: 300px;
      padding: 0 1rem;
    }

    .next-button {
      width: 100%;
      max-width: 300px;
      padding: 1rem 2rem;
      font-size: 1rem;
      height: 50px;

      &.slide-right {
        left: calc(100% - 400px);
      }
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

.input-button-container {
  transition: transform 0.5s ease-in-out;
}

.slide-right {
  transform: translateX(100%);
}
</style>
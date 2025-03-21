<template>
  <div class="app-container">
    <div class="main-content">
      <div class="left-content">
        <div class="header">
          <img src="../assets/header-logo.png" alt="DIICSU Header Logo" class="header-logo">
        </div>
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
                :class="{ 'button-disabled': !isValidEmail }"
                :disabled="!isValidEmail"
            >
              <span class="button-text">SEND CODE</span>
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
import {ref, computed, getCurrentInstance} from 'vue'
import {useRouter} from 'vue-router'

const router = useRouter()
const email = ref('')
const showError = ref(false)

const instance = getCurrentInstance()
const backendAddress = instance.appContext.config.globalProperties.$backendAddress

const isValidEmail = computed(() => {
  return email.value.length > 0 && !showError.value
})

const validateEmail = () => {
  const emailPattern = /^[a-zA-Z0-9._%+-]+@dundee\.ac\.uk$/
  showError.value = !emailPattern.test(email.value + '@dundee.ac.uk')
}

const handleNext = async () => {
  if (isValidEmail.value) {
    try {
      const response = await fetch(backendAddress+'/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: email.value + "@dundee.ac.uk",
        })
      });

      if (response.ok) {
        const data = await response.json();
        if (data.code === "000") {
          await router.push({
            name: 'VerifyView',
            params: {
              email: email.value + "@dundee.ac.uk"
            }
          })
        } else {
          alert(data.message)
        }

      }
    } catch (error) {
      console.error('Error:', error);
    }
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
  align-items: stretch;
}

.left-content {
  flex: 0 0 50%;
  padding: 0 4rem;
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding-top: 40px;

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
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    border: 2px solid transparent;
    max-width: 400px;

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
    width: 60%;

    &::placeholder {
      color: #999;
    }
  }

  .email-suffix {
    color: #666;
    font-size: 1rem;
    padding: 0;
    font-weight: 500;
    width: 40%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
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
    margin: 0 auto;
    position: relative;
    padding: 0;
  }

  .next-button {
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

    &:before {
      content: '';
      display: block;
      background: linear-gradient(to left, rgba(255, 255, 255, 0) 50%, rgba(255, 255, 255, 0.4) 50%);
      background-size: 210% 100%;
      background-position: right bottom;
      height: 100%;
      width: 100%;
      position: absolute;
      top: 0;
      bottom: 0;
      right: 0;
      left: 0;
      border-radius: 50px;
      transition: all 1s;
      -webkit-transition: all 1s;
    }

    &:hover:not(.button-disabled) {
      transform: translateY(-2px);
      box-shadow: 0 6px 25px rgba(79, 172, 254, 0.9);

      &:before {
        background-position: left bottom;
      }
    }

    &:active {
      transform: translateY(1px);
      box-shadow: 0 2px 10px rgba(79, 172, 254, 0.6);
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
  }

  .main-content {
    flex-direction: column;
    padding: 0;
    gap: 0;
    height: 100vh;
    position: relative;
  }

  .header {
    position: static;
    padding: 1rem;
    margin-bottom: 0;
    text-align: center;
  }

  .left-content {
    position: relative;
    z-index: 3;
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    width: 90%;
    margin: 0 auto;
    text-align: center;
    top: 50%;
    transform: translateY(-50%);

    .input-button-container {
      padding: 2rem 2.5rem 2.5rem 2rem;
      background-color: rgba(49, 85, 239, 0.68);
      border-radius: 2.5rem;
    }

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
      font-size: 0.8rem;
      padding: 0.3rem 0 0.3rem 0.3rem;
      width: 60%;
    }

    .email-suffix {
      font-size: 0.6rem;
      padding: 0;
      width: 40%;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .button-container {
      max-width: 300px;
      margin: 0 auto;
      padding: 0;
    }

    .next-button {
      text-align: center;
      width: 100%;
      max-width: 300px;
      height: 30px;
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
  }

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


.input-button-container {
  transition: transform 0.5s ease-in-out;
}
</style>
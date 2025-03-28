<template>
  <div class="app-container">
    <div class="main-content">
      <div class="left-content">
        <div class="header">
          <img src="../assets/header-logo.png" alt="DIICSU Header Logo" class="header-logo">
        </div>
        <div class="input-button-container" :class="{ 'has-error': showError }">
          <h1 class="title">Verify Your Identification</h1>
          <p class="subtitle">Please enter your Dundee or CSU email address to continue</p>
          <div class="input-group">
            <input
                type="email"
                v-model="email"
                class="email-input"
                placeholder="E-mail Address"
                :class="{ 'error': showError }"
                @input="validateEmail"
            >
            <select v-model="selectedSuffix" class="email-suffix">
              <option value="@dundee.ac.uk">@dundee.ac.uk</option>
              <option value="@csu.edu.cn">@csu.edu.cn</option>
            </select>
          </div>
          <p class="error-message" v-if="showError">
            Please enter a valid email address
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
import {ElMessage} from "element-plus";

const router = useRouter()
const email = ref('')
const showError = ref(false)
const selectedSuffix = ref('@dundee.ac.uk');

const instance = getCurrentInstance()
const backendAddress = instance.appContext.config.globalProperties.$backendAddress

const isValidEmail = computed(() => {
  return email.value.length > 0 && !showError.value
})

const validateEmail = () => {
  const emailPattern = selectedSuffix.value === '@dundee.ac.uk'
      ? /^[a-zA-Z0-9._%+-]+@dundee\.ac\.uk$/
      : /^[a-zA-Z0-9._%+-]+@csu\.edu\.cn$/;
  showError.value = !emailPattern.test(email.value + selectedSuffix.value);
};

const handleNext = async () => {
  if (isValidEmail.value) {
    try {
      const fullEmail = email.value + selectedSuffix.value;
      const response = await fetch(backendAddress + '/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: fullEmail,
        })
      });

      if (response.ok) {
        const data = await response.json();
        if (data.code === "000") {
          await router.push({
            name: 'VerifyView',
            params: {
              email: fullEmail
            }
          })
        } else {
          ElMessage.error(data.message)
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
  align-items: center;
}


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
    font-size: 0.9rem;
    padding: 0 15px 0 0;
    font-weight: 500;
    width: 40%;
    border: none;
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23666'%3e%3cpath d='M7 10l5 5 5-5z'/%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 5px center;
    background-size: 20px;
    cursor: pointer;
    border-radius: 50px 50px 50px 50px;
  }

  .email-suffix option {
    background: #fff;
    color: #333;
    padding: 0;
    font-size: 1rem;
  }

  .email-suffix option:checked {
    background: #f0f0f0;
  }

  .email-suffix:hover {
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23333333'%3e%3cpath d='M7 10l5 5 5-5z'/%3e%3c/svg%3e");
  }

  .error-message {
    color: #FFE5E5;
    font-size: 1.1rem;
    margin: 1.5rem auto 0.5rem;
    background: rgba(255, 255, 255, 0.1);
    padding: 1rem 1rem;
    border-radius: 50px 50px 50px 50px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    animation: fadeIn 0.3s ease-in-out;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    display: block;
    max-width: 400px;
    text-align: center;
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
    font-size: 1.1rem;
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

    .button-text {
      transition: opacity 0.3s ease;
    }

    .button-disabled {
      opacity: 0.6;
      cursor: not-allowed;
      background: rgba(255, 255, 255, 0.8);
    }
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
      height: 50%;
      padding: 2rem 2.5rem 2.5rem 2rem;
      background-color: rgba(49, 85, 239, 0.68);
      border-radius: 2.5rem;
    }

    .input-button-container.has-error {
      height: 60%;
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
      height: auto;
    }

    .email-input {
      font-size: 0.9rem;
      padding: 0.3rem 0 0.3rem 0.3rem;
      width: 50%;
    }

    .email-suffix {
      font-size: 0.9rem;
      padding: 0;
      width: 50%;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .button-container {
      max-width: 300px;
      margin: 0 auto;
      padding: 0;
    }


    .error-message {
      color: #FFE5E5;
      font-size: 0.9rem;
      margin: 5% auto 5%;
      background: rgba(255, 255, 255, 0.1);
      padding: 1rem 1rem;
      border-radius: 50px 50px 50px 50px;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      animation: fadeIn 0.3s ease-in-out;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
      display: block;
      max-width: 400px;
      text-align: center;
    }

    .next-button {
      text-align: center;
      width: 100%;
      max-width: 300px;
      height: 23%;
      padding: 1rem 2rem;
      font-size: 1rem;
      display: flex;
      justify-content: center;
      align-items: center;
      margin: 0;
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
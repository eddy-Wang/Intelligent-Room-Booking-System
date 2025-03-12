<template>
  <div class="app-container">
    <div class="main-content">
      <div class="left-content">
        <div class="header">
          <img src="../assets/header-logo.png" alt="DIICSU Header Logo" class="header-logo">
        </div>
        <div class="input-button-container">
          <h1 class="title">Verify your code</h1>
          <p class="subtitle">Please enter the verification code sent to your email</p>

          <div class="input-group">
            <input
                type="text"
                v-model="verificationCode"
                class="verification-input"
                placeholder="Enter verification code:"
                maxlength="6"
            >
          </div>

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
        <div class="back-button-container">
          <button
              @click="handleBack"
              class="back-button"
          >
            <!--            <FontAwesomeIcon :icon="faArrowLeft" class="back-icon"/>-->
            <FontAwesomeIcon :icon="faBackward" class="back-icon"/>
          </button>
        </div>
      </div>

      <div class="right-content">
        <img src="../assets/DIICSUPicture.png" alt="DIICSU Building" class="diicsu-picture">
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, onMounted, getCurrentInstance} from 'vue'
import {useRouter, useRoute} from 'vue-router'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import {faArrowLeft} from '@fortawesome/free-solid-svg-icons'
import {faBackward} from '@fortawesome/free-solid-svg-icons';

const vueInstance = getCurrentInstance()

const router = useRouter()
const route = useRoute()
const email = route.params.email

const verificationCode = ref('')

const isValidCode = computed(() => {
  return verificationCode.value.length === 6
})

const handleVerify = async () => {
  console.log(email)
  if (isValidCode.value) {
    try {
      const response = await fetch('http://127.0.0.1:8080/verify-code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: email,
          code: verificationCode.value
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      if (data.code==="000") {
        console.log(data)
        vueInstance.appContext.config.globalProperties.$user.email = data.data.email
        vueInstance.appContext.config.globalProperties.$user.name = data.data.name
        vueInstance.appContext.config.globalProperties.$user.permission = data.data.permission

        console.log(vueInstance.appContext.config.globalProperties.$user)
      } else {
        alert(data.message)
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }
}

const handleBack = () => {
  router.push('/email')
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
  background: #3155ef;
  display: flex;
  justify-content: space-between;
  min-height: 100vh;
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
    max-width: 400px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    border: 2px solid transparent;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
    }
  }

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
    background: none; /* 移除背景 */
    border: none; /* 移除边框 */
    padding: 0; /* 移除内边距 */
    cursor: pointer;
    width: auto; /* 自动宽度 */
    height: auto; /* 自动高度 */
  }

  .back-icon {
    font-size: 4rem; /* 调整箭头大小 */
    color: white; /* 箭头颜色 */
    transition: color 0.3s ease;
  }

  .back-button:hover .back-icon {
    color: rgba(255, 255, 255, 0.8); /* 鼠标悬停时箭头颜色变浅 */
  }

  .button-container {
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
    position: relative;
    padding: 0;
  }

  .verify-button {
    background-image: linear-gradient(to right, #319efd, #9ed2ff);
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

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 25px rgba(79, 172, 254, 0.9);

      &:before {
        background-position: left bottom;
      }
    }
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

  /* 背景图片铺满页面并半透明 */
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

  .diicsu-picture {
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0.7;
    border-radius: 0;
  }
  .header {
    position: static;
    padding: 1rem;
    margin-bottom: 0;
    text-align: center;
  }
  /* 登录框居中覆盖 */
  .left-content {
    position: relative;
    z-index: 2;
    //background: rgba(255, 255, 255, 0.9); /* 登录框背景颜色，稍微透明 */
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

    .verification-input {
      font-size: 0.95rem;
      //padding: 0.6rem;
      padding: 0.3rem 0 0.3rem 0.3rem;
      width: 60%;
    }

    .button-container {
      max-width: 300px;
      margin: 0 auto;
      padding: 0;
    }

    .verify-button {
      text-align: center;
      width: 100%;
      max-width: 300px;
      height: 30px;
      padding: 1rem 2rem;
      font-size: 1rem;
      display: flex; /* 使用 flex 布局 */
      justify-content: center; /* 水平居中 */
      align-items: center; /* 垂直居中 */
    }

    .button-disabled {
      opacity: 1;
      cursor: not-allowed;
      background: rgba(213, 221, 255, 0.8); /* 禁用状态按钮颜色 */
    }

    .back-button-container {
      margin-top: 1.5rem;
    }

    .back-button {
      margin-left: -2.5rem;
      margin-bottom: 2rem;
      background: none;
      border: none;
      padding: 0;
      cursor: pointer;
    }

    .back-icon {
      font-size: 2.5rem;
      color: #ffffff;
    }

    .back-button:hover .back-icon {
      color: rgba(49, 85, 239, 0.8); /* 鼠标悬停时箭头颜色变浅 */
    }
  }

}
.input-button-container {
  transition: transform 0.5s ease-in-out;
}
</style>
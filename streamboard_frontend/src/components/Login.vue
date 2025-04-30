<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref('')
const password = ref('')
const errorMessage = ref('')

const images = [
  'background_pic/1.jpg',
  'background_pic/2.jpeg',
  'background_pic/3.jpg',
  'background_pic/4.jpg',
  'background_pic/5.webp',
  'background_pic/6.jpg',
  'background_pic/7.webp',
  'background_pic/8.jpg',
  'background_pic/9.jpg',
]

const currentImageIndex = ref(0)

onMounted(() => {
  setInterval(() => {
    currentImageIndex.value = (currentImageIndex.value + 1) % images.length
  }, 5000)
})

const login = async () => {
  errorMessage.value = ''
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/login/', {
      username: username.value,
      password: password.value,
    })
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)
    router.push('/dashboard')
  } catch (error) {
    if (error.response && error.response.status === 401) {
      errorMessage.value = 'Invalid username or password.'
    } else {
      errorMessage.value = 'Something went wrong. Please try again.'
    }
  }
}
</script>

<template>
  <div class="login-wrapper">
    <div class="login-left">
      <div class="slideshow-container">
        <img v-for="(img, index) in images" :key="index" :src="img"
          :class="['slide-image', { active: index === currentImageIndex }]" alt="Background Slide" />
        <div class="gradient-overlay"></div>
      </div>
    </div>

    <div class="login-right">
      <div class="login-container">
        <img src="https://i.imgur.com/6SCZbId.png" alt="Logo" class="logo" />
        <p class="subtitle">Enter your Username and Password to sign in</p>

        <form @submit.prevent="login" class="form">
          <label for="username">Username:</label>
          <input id="username" v-model="username" type="text" placeholder="Enter your username" />

          <label for="password">Password:</label>
          <input id="password" v-model="password" type="password" placeholder="Enter your password" />

          <button type="submit">Sign in</button>

          <p class="subtitle">
            Don’t have an account?
            <router-link to="/signup" class="link">Sign Up</router-link>
          </p>
          <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
        </form>
      </div>
    </div>
  </div>
</template>


<style scoped>
*,
*::before,
*::after {
  box-sizing: border-box;
}

.login-wrapper {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.login-left,
.login-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 0;
}

.slideshow-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.slide-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity 1s ease-in-out;
}

.slide-image.active {
  opacity: 1;
  z-index: 1;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 8%;
  background: linear-gradient(to right, rgba(255, 255, 255, 0) 0%, #ffffff 100%);
  z-index: 2;
}

.login-left {}

.login-right {
  position: relative;
  background: white;
  z-index: 1;
}

.login-right::before {
  content: "";
  position: absolute;
  top: 0;
  left: -50px;
  width: 50px;
  height: 100%;
  background: linear-gradient(to right, rgba(255, 255, 255, 0) 0%, #ffffff 100%);
  z-index: -1;
}

.login-container {
  width: 100%;
  max-width: 550px;
  padding: 3rem;
  margin: 0 auto;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo {
  max-width: 150px;
  margin-bottom: 1rem;
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
  background: linear-gradient(to right, #3ec6ff, #005eff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.subtitle {
  margin-bottom: 1.5rem;
  color: #666;
  font-size: 0.95rem;
}

.form {
  width: 100%;
  max-width: 420px;
  text-align: left;
}

.form label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.form input {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  background-color: #f4f4f4;
  font-size: 1rem;
}

.form button {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(to right, #3ec6ff, #005eff);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

.form button:hover {
  opacity: 0.9;
}

.link {
  color: #005eff;
  font-weight: 600;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.error-msg {
  color: #dc3545;
  font-size: 0.9rem;
  margin-top: -0.5rem;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .login-wrapper {
    flex-direction: column;
  }

  .login-left {
    display: none;
  }

  .login-right {
    flex: none;
    width: 100%;
    padding: 0;
  }

  .login-container {
    padding: 2rem 1rem;
  }
}
</style>

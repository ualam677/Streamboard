<script setup>
import { ref, onMounted } from 'vue'
import lottie from 'lottie-web'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref('')
const password = ref('')
const errorMessage = ref('')

const login = async () => {
  errorMessage.value = ''

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/login/', {
      username: username.value,
      password: password.value,
    })

    // Save tokens to localStorage
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)

    // Optionally redirect
    router.push('/dashboard') // 🔁 Change to your actual route

  } catch (error) {
    if (error.response && error.response.status === 401) {
      errorMessage.value = 'Invalid username or password.'
    } else {
      errorMessage.value = 'Something went wrong. Please try again.'
    }
  }
}

onMounted(() => {
  lottie.loadAnimation({
    container: document.getElementById('lottie-container'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: 'https://lottie.host/0aaef542-4408-43d9-9e24-d2e117e0a681/T5qCcG1FhU.json'
  })
})
</script>

<template>
  <div class="login-wrapper">
    <div class="login-left">
      <div id="lottie-container" class="lottie-box"></div>
    </div>

    <div class="login-right">
      <div class="login-container">
        <img
          src="https://i.imgur.com/HNDynE2.png"
          alt="Logo" class="logo" />
        <h3 class="title">Streamboard</h3>
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

.login-left {
  background: #f8faff;
}

.login-container {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  margin: 0 auto;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.lottie-box {
  width: 80%;
  max-width: 400px;
  height: auto;
  max-height: 80vh;
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
  max-width: 320px;
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

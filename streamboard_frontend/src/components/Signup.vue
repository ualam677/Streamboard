<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

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

const router = useRouter()
const firstName = ref('')
const lastName = ref('')
const username = ref('')
const password = ref('')
const confirmPassword = ref('')

const passwordError = ref('')
const confirmPasswordError = ref('')
const fieldErrors = ref({
    first_name: '',
    last_name: '',
    username: '',
    password: '',
})

watch(password, (newVal) => {
    const strongRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/
    if (!strongRegex.test(newVal)) {
        passwordError.value =
            'Password must be at least 8 characters, include uppercase, lowercase, and a number.'
    } else {
        passwordError.value = null
    }
})

watch([password, confirmPassword], () => {
    if (confirmPassword.value && password.value !== confirmPassword.value) {
        confirmPasswordError.value = 'Passwords do not match.'
    } else {
        confirmPasswordError.value = null
    }
})

const signup = async () => {
    console.log('Signup function triggered')
    fieldErrors.value = {}

    if (passwordError.value || confirmPasswordError.value) {
        return
    }

    try {
        const response = await axios.post('http://127.0.0.1:8000/api/signup/', {
            first_name: firstName.value,
            last_name: lastName.value,
            username: username.value,
            password: password.value
        })
        router.push('/login')
    } catch (error) {
        const data = error.response?.data
        if (data) {
            for (const field in data) {
                fieldErrors.value[field] = data[field][0]
            }
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
                <p class="subtitle">Sign up to get started with Streamboard</p>

                <form @submit.prevent="signup" class="form">
                    <label for="firstName">First Name:</label>
                    <input id="firstName" v-model="firstName" type="text" placeholder="Enter your first name"
                        :class="{ 'input-error': fieldErrors.first_name }" />
                    <p v-if="fieldErrors.first_name" class="error-msg">{{ fieldErrors.first_name }}</p>

                    <label for="lastName">Last Name:</label>
                    <input id="lastName" v-model="lastName" type="text" placeholder="Enter your last name"
                        :class="{ 'input-error': fieldErrors.lsat_name }" />
                    <p v-if="fieldErrors.lsat_name" class="error-msg">{{ fieldErrors.lsat_name }}</p>

                    <label for="username">Username:</label>
                    <input id="username" v-model="username" type="text" placeholder="Enter your Username"
                        :class="{ 'input-error': fieldErrors.username }" />
                    <p v-if="fieldErrors.username" class="error-msg">{{ fieldErrors.username }}</p>

                    <label for="password">Password:</label>
                    <input id="password" v-model="password" type="password" placeholder="Create a password"
                        :class="{ 'input-error': passwordError || fieldErrors.password }" />
                    <p v-if="passwordError" class="error-msg">{{ passwordError }}</p>
                    <p v-if="fieldErrors.password" class="error-msg">{{ fieldErrors.password }}</p>

                    <label for="confirmPassword">Confirm Password:</label>
                    <input id="confirmPassword" v-model="confirmPassword" type="password" placeholder="Confirm password"
                        :class="{ 'input-error': confirmPasswordError }" />
                    <p v-if="confirmPasswordError" class="error-msg">{{ confirmPasswordError }}</p>

                    <button type="submit" :disabled="passwordError || confirmPasswordError">Sign Up</button>
                    <p class="subtitle">
                        Already have an account?
                        <router-link to="/login" class="link">Login</router-link>
                    </p>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.image-container {
    position: relative;
    width: 100%;
    height: 100%;
}

.background-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.gradient-overlay {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    width: 8%;
    background: linear-gradient(to right, rgba(255, 255, 255, 0) 0, #ffffff 100%);
}

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

.login-wrapper {
    display: flex;
    height: 100vh;
    width: 100vw;
    overflow: hidden;
}

.login-left,
.login-right {
    flex: 1;
    min-width: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.login-left {
    background: #f8faff;
}

.lottie-box {
    width: 80%;
    max-width: 400px;
    height: auto;
    max-height: 80vh;
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

.tooltip {
    margin-top: -0.5rem;
    margin-bottom: 1rem;
    font-size: 0.85rem;
    color: #d9534f;
}

.input-error {
    border-color: #d9534f;
}

.input-error {
    border: 1px solid #dc3545 !important;
}

.error-msg {
    margin-top: -0.5rem;
    margin-bottom: 1rem;
    font-size: 0.85rem;
    color: #dc3545;
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

@media (max-width: 768px) {
    .login-wrapper {
        flex-direction: column;
    }

    .login-left {
        display: none;
    }

    .login-right {
        width: 100%;
        padding: 0;
    }

    .login-container {
        padding: 2rem 1rem;
    }
}
</style>

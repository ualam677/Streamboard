<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const toast = useToast()

const profile = ref({
  first_name: '',
  last_name: '',
  email: '',
})

const currentPassword = ref('')
const newPassword = ref('')
const profilePicture = ref('')
const selectedProfileFile = ref(null)
const updatingProfile = ref(false)

const fetchProfile = async () => {
  try {
    const accessToken = localStorage.getItem('access_token')

    const response = await axios.get('http://127.0.0.1:8000/api/profile/', {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    })

    profile.value.first_name = response.data.first_name || ''
    profile.value.last_name = response.data.last_name || ''
    profilePicture.value = response.data.profile_picture || ''

  } catch (error) {
    toast.error('Session expired. Please log in again.')
  }
}

const onProfilePictureChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    selectedProfileFile.value = file
    const reader = new FileReader()
    reader.onload = () => {
      profilePicture.value = reader.result
    }
    reader.readAsDataURL(file)
  }
}

const updateProfile = async () => {
  try {
    updatingProfile.value = true

    const accessToken = localStorage.getItem('access_token')
    const formData = new FormData()
    formData.append('first_name', profile.value.first_name)
    formData.append('last_name', profile.value.last_name)
    if (selectedProfileFile.value) {
      formData.append('profile_picture', selectedProfileFile.value)
    }

    await axios.patch('http://127.0.0.1:8000/api/profile/update/', formData, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'multipart/form-data'
      }
    })

    toast.success('Profile updated successfully!')
    fetchProfile()
  } catch (error) {
    toast.error('Failed to update profile.')
  } finally {
    updatingProfile.value = false
  }
}

const changePassword = async () => {
  if (!currentPassword.value.trim() || !newPassword.value.trim()) {
    toast.error('Both fields are required!')
    return
  }

  if (newPassword.value.length < 8) {
    toast.error('New password must be at least 8 characters long.')
    return
  }

  if (newPassword.value === currentPassword.value) {
    toast.error('New password must be different from current password.')
    return
  }

  try {
    const accessToken = localStorage.getItem('access_token')

    await axios.put('http://127.0.0.1:8000/api/password/change/', {
      current_password: currentPassword.value,
      new_password: newPassword.value
    }, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    })

    toast.success('Password changed successfully! 🎉')
    currentPassword.value = ''
    newPassword.value = ''

  } catch (error) {
    console.error('Error changing password:', error)
    if (error.response && error.response.data?.detail) {
      toast.error(error.response.data.detail)
    } else {
      toast.error('Failed to change password.')
    }
  }
}

onMounted(() => {
  fetchProfile()
})
</script>

<template>
  <div class="settings-container">
    <h1>Account Settings</h1>

    <div class="profile-section">
      <div class="profile-pic-upload">
        <label>
          <input type="file" hidden @change="onProfilePictureChange">
          <img :src="profilePicture || 'https://as2.ftcdn.net/v2/jpg/12/69/82/49/1000_F_1269824904_2jpcrEdtDI2QYyQjNvhNTpimk1rWQZDW.jpg'" alt="Profile" class="profile-img" />
        </label>
      </div>
    </div>

    <div class="form-section">
      <label>First Name:</label>
      <input v-model="profile.first_name" type="text" />

      <label>Last Name:</label>
      <input v-model="profile.last_name" type="text" />

      <button @click="updateProfile" :disabled="updatingProfile">
        {{ updatingProfile ? 'Updating...' : 'Save Profile' }}
      </button>
    </div>

    <div class="password-section">
      <h2>Change Password</h2>
      <label>Current Password:</label>
      <input v-model="currentPassword" type="password" />

      <label>New Password:</label>
      <input v-model="newPassword" type="password" />

      <button @click="changePassword">Change Password</button>
    </div>
  </div>
</template>

<style scoped>
.settings-container {
  max-width: 480px;
  margin: 40px auto;
  padding: 30px 20px;
  background: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  border-radius: 12px;
  text-align: center;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: bold;
}

.profile-img {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #2d7bff;
  margin-bottom: 10px;
  cursor: pointer;
}

input[type="text"],
input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 10px 14px;
  margin: 8px 0;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 16px;
}

button {
  width: 100%;
  background: #2d7bff;
  color: white;
  padding: 12px;
  border: none;
  font-weight: bold;
  border-radius: 8px;
  margin-top: 10px;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover {
  background: #175be0;
}

.password-section {
  margin-top: 40px;
  text-align: left;
}

.password-section h2 {
  text-align: center;
  font-size: 20px;
  margin-bottom: 10px;
}
</style>

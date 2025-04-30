<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { useAuth } from '@/composables/useAuth'

const { handleAuthError } = useAuth()

const router = useRouter()
const toast = useToast()

const profile = ref(null)
const isDarkTheme = ref(false)
const profilePicture = ref('https://as2.ftcdn.net/v2/jpg/12/69/82/49/1000_F_1269824904_2jpcrEdtDI2QYyQjNvhNTpimk1rWQZDW.jpg')
const selectedProfileFile = ref(null)
const updatingPicture = ref(false)

const streamboards = ref([])
const recentBoards = ref([])

const showModal = ref(false)
const newBoardName = ref('')

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good Morning'
  else if (hour < 18) return 'Good Afternoon'
  else return 'Good Evening'
})

const livePreviewData = ref(null)

watch(
  () => recentBoards.value,
  (boards) => {
    if (boards.length > 0) {
      startLivePolling(boards[0].id)
    }
  },
  { immediate: true }
)
let intervalId = null

const startLivePolling = (streamboardId) => {
  clearInterval(intervalId)

  const fetchLiveBoard = async () => {
    try {
      const token = localStorage.getItem('access_token')
      const { data } = await axios.get(`http://127.0.0.1:8000/api/streamboard/latest/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      livePreviewData.value = data
    } catch (error) {
      console.error('Live preview fetch failed:', error)
    }
  }

  fetchLiveBoard()
  intervalId = setInterval(fetchLiveBoard, 2000)
}
const formatAccessTime = (timestamp) => {
  const now = new Date()
  const last = new Date(timestamp)
  const diffMs = now - last
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMins / 60)
  const diffDays = Math.floor(diffHours / 24)

  if (diffMins < 1) return 'just now'
  if (diffMins < 60) return `${diffMins} minute${diffMins === 1 ? '' : 's'} ago`
  if (diffHours < 24) return `${diffHours} hour${diffHours === 1 ? '' : 's'} ago`
  return `${diffDays} day${diffDays === 1 ? '' : 's'} ago`
}

const fetchProfile = async () => {
  try {
    const accessToken = localStorage.getItem('access_token')
    const response = await axios.get('http://127.0.0.1:8000/api/profile/', {
      headers: { Authorization: `Bearer ${accessToken}` }
    })

    profile.value = response.data
    profilePicture.value = response.data.profile_picture || 'https://as2.ftcdn.net/v2/jpg/12/69/82/49/1000_F_1269824904_2jpcrEdtDI2QYyQjNvhNTpimk1rWQZDW.jpg'

    isDarkTheme.value = profile.value.is_dark
    applyTheme()

  } catch (error) {
    handleAuthError(error, fetchProfile)
  }
}

const applyTheme = () => {
  const html = document.documentElement
  if (isDarkTheme.value) {
    html.classList.add('dark-mode')
    localStorage.setItem('theme', 'dark')
  } else {
    html.classList.remove('dark-mode')
    localStorage.setItem('theme', 'light')
  }
}

const fetchRecentBoards = async () => {
  try {
    const accessToken = localStorage.getItem('access_token')
    const response = await axios.get('http://127.0.0.1:8000/api/streamboard/recent-viewed/', {
      headers: { Authorization: `Bearer ${accessToken}` }
    })
    recentBoards.value = response.data
  } catch (error) {
    console.error('Failed to fetch recent streamboards:', error)
  }
}

const toggleTheme = async () => {
  isDarkTheme.value = !isDarkTheme.value
  applyTheme()

  try {
    const accessToken = localStorage.getItem('access_token')
    await axios.patch('http://127.0.0.1:8000/api/profile/update/', {
      is_dark: isDarkTheme.value
    }, {
      headers: { Authorization: `Bearer ${accessToken}` }
    })
  } catch (error) {
    console.error('Error saving theme preference:', error)
  }
}

const onProfilePictureChange = async (e) => {
  const file = e.target.files[0]
  if (file) {
    selectedProfileFile.value = file

    const reader = new FileReader()
    reader.onload = () => {
      profilePicture.value = reader.result
    }
    reader.readAsDataURL(file)

    await uploadProfilePicture()
  }
}
const uploadProfilePicture = async () => {
  if (!selectedProfileFile.value) {
    toast.warning('Please select a picture first!')
    return
  }

  try {
    updatingPicture.value = true
    const accessToken = localStorage.getItem('access_token')

    const formData = new FormData()
    formData.append('profile_picture', selectedProfileFile.value)

    await axios.patch('http://127.0.0.1:8000/api/profile/update/', formData, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'multipart/form-data'
      }
    })

    toast.success('Profile picture updated successfully! 🎉')

    await fetchProfile()

  } catch (error) {
    console.error('Error uploading profile picture:', error)
    toast.error('Failed to update profile picture ❌')
  } finally {
    updatingPicture.value = false
  }
}

const closeModal = () => {
  showModal.value = false
}

const createBoard = () => {
  if (newBoardName.value.trim()) {
    streamboards.value.unshift({
      id: Date.now(),
      name: newBoardName.value.trim(),
      live: false
    })
    closeModal()
  }
}

const goToController = (id) => {
  router.push(`/boards/${id}/controller`)
}
const player1Name = computed(() => {
  const layout = livePreviewData.value?.layout_json
  if (!Array.isArray(layout)) return 'PLAYER 1'

  return layout.find(f => f.player === 1 && f.type === 'name')?.value || 'PLAYER 1'
})

const player2Name = computed(() => {
  const layout = livePreviewData.value?.layout_json
  if (!Array.isArray(layout)) return 'PLAYER 2'

  return layout.find(f => f.player === 2 && f.type === 'name')?.value || 'PLAYER 2'
})

const player1Score = computed(() => {
  const layout = livePreviewData.value?.layout_json
  if (!Array.isArray(layout)) return 0

  return layout.find(f => f.player === 1 && f.type === 'score')?.value || 0
})

const player2Score = computed(() => {
  const layout = livePreviewData.value?.layout_json
  if (!Array.isArray(layout)) return 0

  return layout.find(f => f.player === 2 && f.type === 'score')?.value || 0
})


onMounted(() => {
  fetchProfile()
  fetchRecentBoards()
})
</script>

<template>
  <DefaultLayout :is-dark-mode="isDarkTheme">
    <div class="container">
      <main class="main-content">
        <header class="header">
          <div class="greeting">
            <h1>{{ greeting }}, <span class="username">{{ profile?.first_name || 'Loading...' }}</span></h1>
          </div>
          <div class="profile">
            <label class="profile-upload">
              <input type="file" accept="image/*" @change="onProfilePictureChange" hidden>
              <img :src="profilePicture" alt="Profile" class="profile-img" />
            </label>
            <p>{{ profile?.username || 'loading...' }}</p>
          </div>
        </header>

        <div class="buttons">
          <router-link to='/boards/new'><button class="btn">▶️ ➕ Create New</button></router-link>
          <router-link to="/manage-boards"><button class="btn">▶️ Manage Boards</button></router-link>
          <button class="btn" @click="toggleTheme">
            {{ isDarkTheme ? '☀️ Light Mode' : '🌙 Dark Mode' }}
          </button>
          <router-link to="/settings"><button class="btn">⚙️ Settings</button></router-link>
        </div>

        <div class="content">
          <div class="recent">
            <h2>Recent Streamboards:</h2>
            <div v-for="board in recentBoards" :key="board.id" class="recent-streamboard"
              @click="goToController(board.id)" style="cursor: pointer;">
              <div class="icon-box">
                <template v-if="board.logo">
                  <img :src="board.logo" alt="Board Logo" class="logo-image" />
                </template>
                <template v-else-if="board.title">
                  <span class="letter-icon">{{ board.title.charAt(0).toUpperCase() }}</span>
                </template>
                <template v-else>
                  <span class="letter-icon"></span>
                </template>
              </div>
              <div class="board-details">
                <div class="board-title">
                  {{ board.title }}
                  <span v-if="board.live" class="live-indicator">LIVE <span class="dot">●</span></span>
                </div>
                <div class="last-accessed">
                  Accessed {{ formatAccessTime(board.last_view) }}
                </div>
              </div>
            </div>
          </div>

          <div class="divider"></div>

          <div class="scoreboard">
            <h2 class="scoreboard-title">Scoreboard Preview:</h2>

            <div class="score-card" v-if="livePreviewData">
              <div class="live-indicator">LIVE <span class="red-dot">●</span></div>
              <div class="names-row">
                <div class="player-name">{{ player1Name }}</div>
                <div class="player-name">{{ player2Name }}</div>
              </div>

              <div class="scores-row">
                <div class="player-score">{{ player1Score }}</div>
                <div class="dash">-</div>
                <div class="player-score">{{ player2Score }}</div>
              </div>
            </div>

            <div v-else class="score-card">Waiting for match data...</div>
          </div>
          <div class="watermark-logo">
            <img src="https://i.imgur.com/6SCZbId.png" alt="Streamboard Logo" />
          </div>
        </div>
      </main>
    </div>
  </DefaultLayout>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Arial', sans-serif;
  background: white;
  color: black;
}

.container {
  display: flex;
  min-height: 95vh;
  flex-direction: row;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  margin-left: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 10px;
  border-bottom: 4px solid black;
}

/* larger Nexa Heavy greeting */
.greeting h1 {
  font-family: 'Nexa', sans-serif;
  font-weight: bold;
  font-size: 3rem;
  color: var(--text-color);
}

.username {
  color: #2d7bff;
}

.profile {
  text-align: center;
}

.profile-img {
  width: 70px;
  height: 70px;
  object-fit: cover;
  border-radius: 50%;
  border: 3px solid #2d7bff;
  cursor: pointer;
}

.profile p {
  font-size: 14px;
}

.buttons {
  margin-top: 20px;
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.btn {
  background: #2d7bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  font-weight: bold;
  font-size: 16px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn:hover {
  background-color: #1b5edb;
}

.btn a {
  text-decoration: none !important;
}

router-link {
  text-decoration: none;
}

.content {
  display: flex;
  flex: 1;
  margin-top: 30px;
}

.recent,
.scoreboard {
  flex: 1;
}

.recent h2,
.scoreboard h2 {
  font-size: 28px;
  margin-bottom: 20px;
}

.streamboard {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
}

.stream-title {
  font-size: 22px;
  font-weight: bold;
}

.stream-time {
  font-size: 16px;
  color: gray;
}

.live {
  color: red;
  font-size: 16px;
  font-weight: bold;
}

.red-dot {
  color: red;
  font-size: 18px;
  vertical-align: middle;
}

.divider {
  width: 4px;
  background: black;
  margin: 0 30px;
}


.footer img {
  width: 30px;
}

.footer span {
  font-size: 20px;
  font-weight: bold;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal {
  background: white;
  padding: 30px;
  border-radius: 12px;
  width: 400px;
  text-align: center;
}

.modal h2 {
  font-size: 28px;
  margin-bottom: 20px;
}

.modal input {
  width: 100%;
  padding: 12px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 16px;
}

.modal-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.dark-mode {
  background: #121212;
  color: #f0f0f0;
}

.dark-mode .main-content {
  background: #121212;
  color: #f0f0f0;
}

.dark-mode .sidebar {
  background: #1f1f1f;
}

.dark-mode .letter-icon {
  background: #2c2c2c;
  color: white;
}

.dark-mode .logout-icon img {
  filter: invert(1);
}

.dark-mode .btn {
  background: #195bb1;
  color: white;
}

.dark-mode .btn:hover {
  background: #13488d;
}

.dark-mode .modal {
  background: #1e1e1e;
  color: white;
}

.dark-mode .score-card {
  background: #195bb1;
}

.dark-mode .stream-title,
.dark-mode .stream-time,
.dark-mode .player,
.dark-mode .score,
.dark-mode .footer {
  color: white;
}


@media (max-width: 1024px) {
  .buttons {
    justify-content: center;
  }

  .content {
    flex-direction: column;
    align-items: center;
  }

  .divider {
    display: none;
  }

  .recent,
  .scoreboard {
    width: 100%;
    text-align: center;
  }

  .streamboard {
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
  }

  .sidebar {
    flex-direction: row;
    height: 70px;
    width: 100%;
    padding: 10px;
  }

  .sidebar-icons {
    flex-direction: row;
    gap: 15px;
  }

  .logout-icon {
    position: absolute;
    right: 20px;
    top: 20px;
  }

  .main-content {
    padding: 20px;
  }

  .header {
    flex-direction: column;
    gap: 15px;
  }

  .greeting h1 {
    font-size: 28px;
    text-align: center;
  }

  .profile-img {
    width: 70px;
    height: 70px;
  }

.buttons {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    width: 70%;
    max-width: 360px;
    margin: 20px auto;
    gap: 15px;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }

  .scoreboard {
    width: 100%;
    margin-bottom: 7rem;
  }

}

.recent-streamboard {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.icon-box {
  width: 50px;
  height: 50px;
  background-color: #12264d;
  border-radius: 12px;
  border: 4px solid #1a4aac;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.logo-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.letter-icon {
  color: white;
  font-size: 32px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
} 

.custom-icon svg {
  width: 26px;
  height: 26px;
}

.board-details {
  display: flex;
  flex-direction: column;
}

.board-title {
  font-weight: 600;
  font-size: 18px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.last-accessed {
  font-size: 14px;
  color: gray;
}

.live-indicator {
  color: red;
  font-size: 14px;
  font-weight: bold;
}

.dot {
  font-size: 16px;
  vertical-align: middle;
}

.watermark-logo {
  position: fixed;
  bottom: 20px;
  right: 20px;
  opacity: 0.5;
  z-index: 1;
  pointer-events: none;
}

.watermark-logo img {
  width: 120px;
  height: auto;
}

.scoreboard {
  text-align: center;
  margin-top: 40px;
}

.scoreboard-title {
  font-size: 26px;
  font-weight: bold;
  margin-bottom: 20px;
}

.score-card {
  background-color: #1f74e1;
  border-radius: 30px;
  padding: 40px 30px;
  max-width: 480px;
  margin: 0 auto;
  color: white;
  font-family: 'Arial', sans-serif;
}

.names-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 25px;
}

.player-name {
  width: 50%;
  font-size: 16px;
  font-weight: bold;
  text-transform: uppercase;
  text-align: center;
}

.scores-row {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 52px;
  font-weight: bold;
  gap: 30px;
}

.player-score {
  width: 80px;
  text-align: center;
}

.dash {
  font-size: 36px;
}

.live-indicator {
  font-weight: bold;
  font-size: 14px;
  color: red;
  text-transform: uppercase;
  margin-bottom: 15px;
}

.red-dot {
  font-size: 16px;
  vertical-align: middle;
  color: red;
}
</style>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { GraphQLClient, gql } from 'graphql-request'
import { useToast } from 'vue-toastification'

const router = useRouter()
const toast = useToast()

const profile = ref(null)
const isDarkTheme = ref(false)
const profilePicture = ref('https://as2.ftcdn.net/v2/jpg/12/69/82/49/1000_F_1269824904_2jpcrEdtDI2QYyQjNvhNTpimk1rWQZDW.jpg')
const selectedProfileFile = ref(null)
const updatingPicture = ref(false)

const streamboards = ref([
  { id: 1, name: 'Stream Test', live: true },
  { id: 2, name: 'Amazeboard', live: false },
  { id: 3, name: 'Smash Bros', live: false }
])

const showModal = ref(false)
const newBoardName = ref('')

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good Morning'
  else if (hour < 18) return 'Good Afternoon'
  else return 'Good Evening'
})

const endpoint = 'https://api.start.gg/gql/alpha'
const startggToken = 'c56e70671542a9aef164b1d4938186ad'
const liveMatch = ref(null)


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
    handleAuthError(error)
  }
}

const applyTheme = () => {
  if (isDarkTheme.value) {
    document.body.classList.add('dark-mode')
    localStorage.setItem('theme', 'dark')
  } else {
    document.body.classList.remove('dark-mode')
    localStorage.setItem('theme', 'light')
  }
}

const handleAuthError = async (error) => {
  if (error.response && error.response.status === 401) {
    try {
      const refresh = localStorage.getItem('refresh_token')
      const refreshResponse = await axios.post('http://127.0.0.1:8000/api/token/refresh/', { refresh })
      const newAccess = refreshResponse.data.access
      localStorage.setItem('access_token', newAccess)
      await fetchProfile()
    } catch (refreshError) {
      console.error('Refresh token expired, redirecting to login')
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      router.push('/login')
    }
  } else {
    console.error('Failed to load profile:', error)
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

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push('/login')
}

const openModal = () => {
  showModal.value = true
  newBoardName.value = ''
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

const fetchLiveMatch = async () => {
  const graphQLClient = new GraphQLClient(endpoint, {
    headers: {
      Authorization: `Bearer ${startggToken}`
    }
  })

  const query = gql`
    query LiveMatch {
      event(id: 1366953) {
        sets(perPage: 1, sortType: RECENT) {
          nodes {
            id
            winnerId
            slots {
              entrant {
                name
              }
              standing {
                stats {
                  score {
                    value
                  }
                }
              }
            }
          }
        }
      }
    }
  `

  try {
    const data = await graphQLClient.request(query)
    liveMatch.value = data.event.sets.nodes[0]
  } catch (error) {
    console.error('Error fetching live match:', error)
  }
}

onMounted(() => {
  fetchProfile()
  fetchLiveMatch()
  setInterval(fetchLiveMatch, 5000)
})
</script>




<template>
    <div class="container">
        <aside class="sidebar">
            <div class="sidebar-icons">
                <img src="https://img.icons8.com/ios-filled/50/ffffff/video-playlist.png" alt="Icon" class="icon-img" />
                <div class="letter-icon">S</div>
                <div class="letter-icon">A</div>
                <img src="https://img.icons8.com/ios-filled/50/ffffff/smash.png" alt="Icon" class="icon-img" />
            </div>
            <div class="logout-icon" @click="logout">
                <img src="https://img.icons8.com/ios-glyphs/30/ffffff/logout-rounded-left.png" alt="Logout" />
            </div>
        </aside>

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
                    <div v-for="board in streamboards" :key="board.id" class="streamboard">
                        <div class="letter-icon">{{ board.name.charAt(0).toUpperCase() }}</div>
                        <div class="details">
                            <p class="stream-title">
                                {{ board.name }}
                                <span v-if="board.live" class="live">LIVE <span class="red-dot">●</span></span>
                            <p v-else class="stream-time">Recently created</p>
                            </p>
                        </div>
                    </div>
                </div>

                <div class="divider"></div>

                <div class="scoreboard">
                    <h2>Scoreboard Preview:</h2>

                    <div v-if="liveMatch" class="score-card">
                        <div class="player">{{ liveMatch.slots[0]?.entrant?.name || 'Player 1' }}</div>
                        <div class="score">
                            {{ liveMatch.slots[0]?.standing?.stats?.score?.value ?? 0 }} -
                            {{ liveMatch.slots[1]?.standing?.stats?.score?.value ?? 0 }}
                        </div>
                        <div class="player">{{ liveMatch.slots[1]?.entrant?.name || 'Player 2' }}</div>
                    </div>

                    <div v-else class="score-card">
                        Waiting for match data...
                    </div>
                </div>
            </div>

            <footer class="footer">
                <img src="https://img.icons8.com/ios-filled/50/000000/video-playlist.png" alt="Logo" />
                <span>Streamboard</span>
            </footer>
        </main>

        <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
            <div class="modal">
                <h2>Create New Streamboard</h2>
                <input v-model="newBoardName" type="text" placeholder="Enter board name" />
                <div class="modal-buttons">
                    <button class="btn" @click="createBoard">Create</button>
                    <button class="btn" @click="closeModal">Cancel</button>
                </div>
            </div>
        </div>
    </div>
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
    height: 100vh;
}

.sidebar {
    width: 90px;
    background: #0c1c2c;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;
}

.sidebar-icons {
    display: flex;
    flex-direction: column;
    gap: 25px;
    align-items: center;
}

.icon-img {
    width: 40px;
}

.letter-icon {
    background: white;
    color: black;
    font-size: 28px;
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    border-radius: 12px;
}

.smash {
    background: url('https://img.icons8.com/ios-filled/50/000000/smash.png') no-repeat center center;
    background-size: 30px 30px;
    background-color: white;
}

.logout-icon img {
    width: 30px;
    cursor: pointer;
}

.main-content {
    flex: 1;
    padding: 20px 40px;
    display: flex;
    flex-direction: column;
    position: relative;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 10px;
    border-bottom: 4px solid black;
}

.greeting h1 {
    font-size: 36px;
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
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #1b5edb;
}
.btn a{
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

.score-card {
    background: #2d7bff;
    color: white;
    text-align: center;
    padding: 30px 20px;
    border-radius: 15px;
}

.player {
    font-size: 20px;
    font-weight: bold;
}

.score {
    font-size: 40px;
    margin: 10px 0;
}

.footer {
    margin-top: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
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
    background: #444;
    color: white;
}

.dark-mode .btn:hover {
    background: #666;
}

.dark-mode .modal {
    background: #1e1e1e;
    color: white;
}

.dark-mode .score-card {
    background: #333;
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
        width: 60px;
        height: 60px;
    }

    .buttons {
        flex-direction: column;
        align-items: center;
        gap: 10px;
    }

    .btn {
        width: 100%;
        justify-content: center;
    }

    .score-card {
        width: 100%;
    }

    .footer {
        justify-content: center;
        margin-bottom: 20px;
    }
}
</style>

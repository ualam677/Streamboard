<template>
    <aside class="sidebar">
        <div class="sidebar-top">
            <router-link to="/dashboard" class="icon-img">
                <img src="https://i.imgur.com/HNDynE2.png" alt="Icon" class="icon-img" />
            </router-link>
        </div>
        <div class="sidebar-container">
            <div class="fade-top"></div>
            <div class="sidebar-boards">
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
                </div>
            </div>
            <div class="fade-bottom"></div>
        </div>
        <div class="logout-icon" @click="logout">
            <img src="https://img.icons8.com/ios-glyphs/30/ffffff/logout-rounded-left.png" alt="Logout" />
        </div>
    </aside>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import axios from 'axios'

const router = useRouter()
const recentBoards = ref([])

const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    router.push('/login')
}

const fetchRecentBoards = async () => {
    try {
        const accessToken = localStorage.getItem('access_token')
        const response = await axios.get('http://127.0.0.1:8000/api/streamboard/list/', {
            headers: { Authorization: `Bearer ${accessToken}` }
        })
        // Sort by last_view date, newest first
        recentBoards.value = response.data.sort((a, b) => 
            new Date(b.last_view) - new Date(a.last_view)
        )
    } catch (error) {
        console.error('Failed to fetch recent streamboards:', error)
    }
}
const goToController = (id) => {
    router.push(`/boards/${id}/controller`)
}

onMounted(() => {
    fetchRecentBoards()
})

</script>

<style scoped>
.sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 80px;
    background: #0c1c2c;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;
    z-index: 1000;
    border-right: #1a4aac 5px solid;
}

.sidebar-top {
    margin-bottom: 15px;
}

.sidebar-container {
    position: relative;
    flex-grow: 1;
    width: 100%;
    overflow: hidden;
}

.sidebar-boards {
    display: flex;
    flex-direction: column;
    gap: 25px;
    align-items: center;
    overflow-y: auto;
    max-height: 100%;
    height: 100%;
    scrollbar-width: none; /* Firefox */
    scrollbar-color: transparent transparent;
    padding: 0 15px;
    padding-bottom: 20px; /* Add padding at the bottom for spacing before logout */
    padding-top: 10px;
}

.sidebar-boards::-webkit-scrollbar {
    display: none; /* Safari and Chrome */
    width: 0;
}

.sidebar-boards::-webkit-scrollbar-track {
    background: transparent;
}

.sidebar-boards::-webkit-scrollbar-thumb {
    background-color: transparent;
}

.icon-img {
    width: 50px;
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

.logout-icon {
  padding-top: 5px;
  position: relative;
}

.logout-icon::before {
  content: '';
  position: absolute;
  top: -10px;
  left: 0;
  right: 0;
  height: 15px;
  background: linear-gradient(to bottom, rgba(12, 28, 44, 0), #0c1c2c);
  pointer-events: none;
}

.logout-icon img {
    width: 30px;
    cursor: pointer;
}

.fade-top {
    position: absolute;
    top: 0;
    left: 0;
    right: 5px; /* Account for the border on the right */
    height: 10px;
    background: linear-gradient(to bottom, #0c1c2c, rgba(12, 28, 44, 0));
    z-index: 10;
    pointer-events: none;
}

.fade-bottom {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 5px; /* Account for the border on the right */
    height: 30px;
    background: linear-gradient(to top, #0c1c2c, rgba(12, 28, 44, 0));
    z-index: 10;
    pointer-events: none;
}

@media (max-width: 768px) {
    .sidebar {
        position: relative;
        width: 100%;
        height: auto;
        flex-direction: row;
        padding: 10px;
    }

    .sidebar-top {
        margin-bottom: 0;
    }

    .sidebar-boards {
        flex-direction: row;
        max-height: none;
        overflow-x: auto;
        overflow-y: hidden;
        padding: 0 10px;
        scrollbar-width: none;
    }

    .sidebar-boards::-webkit-scrollbar {
        display: none;
    }

    .sidebar-container {
        flex-grow: 1;
        width: auto;
    }
    
    .fade-top, .fade-bottom {
        display: none;
    }
}
</style>
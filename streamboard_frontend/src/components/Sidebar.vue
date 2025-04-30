<template>
    <aside class="sidebar">
        <div class="sidebar-icons">
            <router-link to="/dashboard" class="icon-img">
                <img src="https://i.imgur.com/HNDynE2.png" alt="Icon" class="icon-img" />
            </router-link>
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
        const response = await axios.get('http://127.0.0.1:8000/api/streamboard/recent-viewed/', {
            headers: { Authorization: `Bearer ${accessToken}` }
        })
        recentBoards.value = response.data
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
    overflow: hidden;
    border-right: #1a4aac 5px solid;
}

.sidebar-icons {
    display: flex;
    flex-direction: column;
    gap: 25px;
    align-items: center;
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

.logout-icon img {
    width: 30px;
    cursor: pointer;
}

@media (max-width: 768px) {
    .sidebar {
        position: relative;
        width: 100%;
        height: auto;
        flex-direction: row;
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
}
</style>
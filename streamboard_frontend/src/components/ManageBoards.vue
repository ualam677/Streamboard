<script setup>
import { ref, onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth'
import axios from 'axios'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { useToast } from 'vue-toastification'

const { handleAuthError } = useAuth()

const toast = useToast()
const boards = ref([])
const loading = ref(true)
const isDarkTheme = ref(localStorage.getItem("theme") === "dark")


const fetchBoards = async () => {
  try {
    loading.value = true
    const accessToken = localStorage.getItem('access_token')
    const response = await axios.get('http://127.0.0.1:8000/api/streamboard/list/', {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    })
    boards.value = response.data
  } catch (error) {
    await handleAuthError(error)
  } finally {
    loading.value = false
  }
}

const deleteBoard = async (id) => {
  if (!confirm('Are you sure you want to delete this board? This action is permanent!')) {
    return
  }

  try {
    const accessToken = localStorage.getItem('access_token')
    await axios.delete(`http://127.0.0.1:8000/api/streamboard/${id}/`, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    })
    boards.value = boards.value.filter(b => b.id !== id)
    toast.success('Board deleted successfully!')
  } catch (error) {
    console.error('Failed to delete board', error)
    await handleAuthError(error)
  }
}
const applyThemeToMain = (isDark) => {
  console.log('Applying theme to main:', isDark)
  const main = document.querySelector('.page-content')
  if (main) {
    if (isDark) {
      main.style.backgroundColor = '#121212'
      main.style.color = '#111111'           
    } else {
      main.style.backgroundColor = '#ffffff'
      main.style.color = '#111111'           
    }
  }
}

onMounted(() => {
  applyThemeToMain(isDarkTheme.value)
  fetchBoards()
})
</script>

<template>
  <DefaultLayout :dark-theme="isDarkTheme">
    <div class="manage-boards-page">
      <div class="content">
        <h1>Manage Boards</h1>

        <div v-if="loading">
          <p>Loading boards...</p>
        </div>

        <div v-else-if="boards.length === 0">
          <p>No boards found.</p>
        </div>

        <div v-else class="board-list">
          <div v-for="board in boards" :key="board.id" class="board-card">
            <h3>{{ board.title || 'Untitled Board' }}</h3>
            <p>ID: {{ board.id }}</p>

            <div class="buttons">
              <router-link :to="{ path: '/boards/new', query: { edit: true, id: board.id } }">
                <button>✏️ Edit</button>
              </router-link>
              <button class="danger" @click="deleteBoard(board.id)">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<style scoped>
.manage-boards-page {
  display: flex;
}

.content {
  flex: 1;
  padding: 40px;
}

.board-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 30px;
}

.board-card {
  background: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 20px;
  width: 260px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.board-card h3 {
  margin-bottom: 10px;
}

.buttons {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

button {
  padding: 10px;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

button:hover {
  opacity: 0.8;
}

.danger {
  background: #e74c3c;
  color: white;
}

/* Make page title blue */
.content h1 {
  color: #2d7bff;
}
</style>

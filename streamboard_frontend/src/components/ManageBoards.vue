<script setup>
import { ref } from 'vue'

const boards = ref([
  { id: 1, name: 'Stream Test', live: true },
  { id: 2, name: 'Amazeboard', live: false },
  { id: 3, name: 'Smash Bros', live: false }
])

const deleteBoard = (id) => {
  boards.value = boards.value.filter(board => board.id !== id)
}

const renameBoard = (id) => {
  const newName = prompt('Enter new board name:')
  if (newName) {
    const board = boards.value.find(b => b.id === id)
    if (board) board.name = newName
  }
}
</script>

<template>
  <div class="manage-container">
    <h1>Manage Your Streamboards</h1>

    <div v-if="boards.length" class="boards-list">
      <div v-for="board in boards" :key="board.id" class="board-card">
        <div class="board-info">
          <h2>{{ board.name }}</h2>
          <p v-if="board.live" class="live-badge">LIVE ●</p>
        </div>
        <div class="board-actions">
          <button @click="renameBoard(board.id)">✏️ Rename</button>
          <button @click="deleteBoard(board.id)">🗑️ Delete</button>
        </div>
      </div>
    </div>

    <div v-else class="no-boards">
      <p>No boards found. Create one!</p>
    </div>
  </div>
</template>

<style scoped>
.manage-container {
  padding: 40px;
  text-align: center;
}

h1 {
  font-size: 36px;
  margin-bottom: 30px;
}

.boards-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}

.board-card {
  background: #f4f4f4;
  padding: 20px;
  width: 400px;
  border-radius: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.board-info {
  text-align: left;
}

.board-info h2 {
  font-size: 24px;
  margin-bottom: 5px;
}

.live-badge {
  color: red;
  font-weight: bold;
}

.board-actions button {
  background: #2d7bff;
  color: white;
  border: none;
  padding: 8px 12px;
  margin-left: 8px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

.no-boards {
  font-size: 20px;
  margin-top: 40px;
}
</style>

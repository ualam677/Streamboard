<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <h2 class="modal-title">➕ Add New Field</h2>

      <div v-if="step === 1" class="step">
        <h3>Select Player:</h3>
        <div class="options-grid">
          <button v-for="player in playerOptions" :key="player.value"
            :class="['option-btn', selectedPlayer === player.value ? 'selected' : '']"
            @click="selectPlayer(player.value)">
            {{ player.label }}
          </button>
        </div>
        <button class="next-btn" :disabled="!selectedPlayer" @click="step = 2">Next ➡️</button>
      </div>

      <div v-if="step === 2" class="step">
        <h3 v-if="selectedPlayer !== 'custom'">Select Field Type:</h3>
        <input v-if="selectedPlayer === 'custom'" v-model="customFieldName" placeholder="Enter Custom Field Name" class="custom-input" />

        <div v-if="selectedPlayer !== 'custom'" class="options-grid">
          <button v-for="field in getFieldOptions()" :key="field.value"
            :class="['option-btn', selectedFieldType === field.value ? 'selected' : '']"
            @click="selectFieldType(field.value)">
            {{ field.label }}
          </button>
        </div>

        <div class="step-actions">
          <button class="prev-btn" @click="step = 1">⬅️ Back</button>
          <button class="confirm-btn" :disabled="!isConfirmEnabled" @click="confirmSelection">✅ Confirm</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  show: Boolean,
  onClose: Function,
  onConfirm: Function,
  numPlayers: {
    type: Number,
    default: 2
  }
})

const step = ref(1)
const selectedPlayer = ref(null)
const selectedFieldType = ref(null)
const customFieldName = ref('')

const playerOptions = ref([
  { label: 'Player 1', value: 1 },
  { label: 'Player 2', value: 2 },
  { label: 'Player 3', value: 3 },
  { label: 'Player 4', value: 4 },
  { label: 'Tournament', value: 'tournament' },
  { label: 'Custom', value: 'custom' }
])

const selectPlayer = (value) => {
  selectedPlayer.value = value
  selectedFieldType.value = null
  customFieldName.value = ''
}

const selectFieldType = (value) => {
  selectedFieldType.value = value
}

const getFieldOptions = () => {
  if (selectedPlayer.value === 'tournament') {
    return [
      { label: 'Tournament Name', value: 'tournament_name' },
      { label: 'Tournament Round', value: 'tournament_round' },
      { label: 'Bracket Link', value: 'bracket_link' }
    ]
  } else {
    return [
      { label: 'Name', value: 'name' },
      { label: 'Score', value: 'score' },
      { label: 'Sponsor/Tag', value: 'sponsor' },
      { label: 'Twitter/X Handle', value: 'twitter' },
      { label: 'Pronouns', value: 'pronouns' },
      { label: 'Country', value: 'country' }
    ]
  }
}

const isConfirmEnabled = computed(() => {
  if (selectedPlayer.value === 'custom') {
    return customFieldName.value.trim().length > 0
  }
  return selectedFieldType.value !== null
})

const confirmSelection = () => {
  if (selectedPlayer.value === 'custom') {
    props.onConfirm('custom', customFieldName.value.trim())
  } else {
    props.onConfirm(selectedPlayer.value, selectedFieldType.value)
  }
  resetModal()
}

const closeModal = () => {
  props.onClose()
  resetModal()
}

const resetModal = () => {
  step.value = 1
  selectedPlayer.value = null
  selectedFieldType.value = null
  customFieldName.value = ''
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background: #2d7bff;
  color: white;
  padding: 30px;
  width: 90%;
  max-width: 500px;
  border-radius: 15px;
  text-align: center;
  animation: fadeIn 0.3s ease-out;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.modal-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.step h3 {
  font-size: 18px;
  margin-bottom: 15px;
}

.options-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.option-btn {
  background: #f1f5f9;
  border: 2px solid transparent;
  padding: 10px 15px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

.option-btn.selected {
  border-color: #2d7bff;
  background: #e0efff;
}

.custom-input {
  width: 100%;
  padding: 10px;
  margin: 15px 0;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.next-btn,
.prev-btn,
.confirm-btn {
  margin-top: 20px;
  padding: 10px 20px;
  background: #ffffff;
  color: black;
  border: none;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
  font-size: 1rem;
}

.step-actions {
  display: flex;
  justify-content: space-between;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>

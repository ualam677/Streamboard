<template>
    <div class="match-selector">
        <h1 class="title">🎮 Select a Match</h1>

        <div class="input-group">
            <input v-model="eventId" type="text" placeholder="Enter Event ID" />
            <button class="btn" @click="fetchMatches">Fetch Matches</button>
        </div>

        <div v-if="loading" class="loading">Loading matches...</div>

        <div v-if="matches.length" class="match-list">
            <div v-for="match in matches" :key="match.id" class="match-card">
                <div class="players">
                    <span>{{ match.player1 || 'TBD' }}</span> vs <span>{{ match.player2 || 'TBD' }}</span>
                </div>
                <button class="btn select-btn" @click="selectMatch(match)">Select</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue'
import axios from 'axios'


const eventId = ref('')
const matches = ref([])
const loading = ref(false)


const fetchMatches = async () => {
    if (!eventId.value) {
        alert('Please enter a valid Event ID!')
        return
    }

    loading.value = true
    matches.value = []

    try {
        const response = await axios.post('https://api.start.gg/gql/alpha', {
            query: `
          query EventMatches($eventId: ID!) {
            event(id: $eventId) {
              sets(perPage: 10, page: 1) {
                nodes {
                  id
                  slots {
                    entrant {
                      name
                    }
                  }
                }
              }
            }
          }
        `,
            variables: { eventId: eventId.value },
        }, {
            headers: {
                Authorization: `Bearer c56e70671542a9aef164b1d4938186ad`
            }
        })

        const nodes = response.data.data.event?.sets.nodes || []
        matches.value = nodes.map(set => ({
            id: set.id,
            player1: set.slots[0]?.entrant?.name,
            player2: set.slots[1]?.entrant?.name,
        }))

    } catch (error) {
        console.error('Failed to fetch matches:', error)
        alert('Error fetching matches.')
    } finally {
        loading.value = false
    }
}

const emit = defineEmits(['match-selected'])

const selectMatch = (match) => {
    emit('match-selected', match)
}
</script>

<style scoped>
.match-selector {
    max-width: 800px;
    margin: 40px auto;
    padding: 20px;
    text-align: center;
}

.title {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 30px;
    background: linear-gradient(to right, #ff758c, #ff7eb3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.input-group {
    display: flex;
    gap: 10px;
    justify-content: center;
    margin-bottom: 20px;
}

input {
    padding: 10px;
    width: 250px;
    border: 2px solid #ccc;
    border-radius: 8px;
    font-size: 1rem;
}

.btn {
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
}

.btn:hover {
    opacity: 0.9;
}

.loading {
    margin-top: 20px;
    font-weight: bold;
}

.match-list {
    margin-top: 30px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.match-card {
    border: 2px solid #ddd;
    padding: 15px;
    border-radius: 10px;
    background-color: #f9f9f9;
}

.players {
    margin-bottom: 10px;
    font-size: 1.1rem;
    font-weight: bold;
}

.select-btn {
    background-color: #2196f3;
}
</style>
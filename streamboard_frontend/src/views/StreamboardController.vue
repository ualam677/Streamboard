<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { GraphQLClient, gql } from 'graphql-request'
import { useToast } from 'vue-toastification'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

// reflect current theme
const isDarkMode = ref(localStorage.getItem('theme') === 'dark')

const route = useRoute()
const toast = useToast()

const boardId = route.params.id
const overlayLink = `${window.location.origin}/overlay/${boardId}`

const streamboard = ref(null)
const fields = ref([])
const isSaving = ref(false)

const tournamentUrl = ref('')
const events = ref([])
const selectedEventId = ref('')
const matches = ref([])
const selectedMatchId = ref('')
const startggToken = 'c56e70671542a9aef164b1d4938186ad'
const access_token = localStorage.getItem('access_token')

// add scoreboard name state
const scoreboardName = ref('')

const fetchStreamboard = async () => {
  try {
    const { data } = await axios.get(`http://127.0.0.1:8000/api/streamboard/${boardId}/`, {
      headers: {
        Authorization: `Bearer ${access_token}`
      }
    })
    streamboard.value = data
    scoreboardName.value = data.name                // ← set name
    const rawFields = Array.isArray(data.layout_json) ? data.layout_json : []
    fields.value = rawFields.map(field => ({
      ...field,
      value: field.value ?? ''
    }))
  } catch (error) {
    console.error('Failed to fetch Streamboard:', error)
    toast.error('Failed to load Streamboard.')
  }
}

const saveChanges = async () => {
  try {
    isSaving.value = true

    const payload = {
      layout_json: fields.value
    }

    await axios.patch(`http://127.0.0.1:8000/api/streamboard/${boardId}/`, payload, {
      headers: {
        Authorization: `Bearer ${access_token}`
      }
    })

    toast.success('Changes saved successfully! 🎉')
  } catch (error) {
    console.error('Failed to save changes:', error)
    toast.error('Failed to save changes.')
  } finally {
    isSaving.value = false
  }
}

const onTournamentUrlChange = async () => {
  const slug = extractSlugFromUrl(tournamentUrl.value)
  if (slug) {
    await fetchEvents(slug)
  }
}

const extractSlugFromUrl = (url) => {
  const match = url.match(/tournament\/([^/]+)/)
  return match ? match[1] : null
}

const fetchEvents = async (slug) => {
  try {
    const graphQLClient = new GraphQLClient('https://api.start.gg/gql/alpha', {
      headers: {
        Authorization: `Bearer ${startggToken}`
      }
    })

    const query = gql`
      query GetTournamentInfo($slug: String!) {
        tournament(slug: $slug) {
          name
          events {
            id
            name
          }
        }
      }
    `

    const data = await graphQLClient.request(query, { slug })

    const tournamentName = data.tournament?.name || ''

    fields.value.forEach(field => {
      if (field.name.toLowerCase().includes('tournament') && field.name.toLowerCase().includes('name')) {
        field.value = tournamentName
      } else if (field.name.toLowerCase().includes('bracket') && field.name.toLowerCase().includes('link')) {
        field.value = tournamentUrl.value
      }
    })

    events.value = data.tournament?.events || []

  } catch (error) {
    console.error('Failed to fetch tournament info', error)
    toast.error('Failed to fetch tournament or events.')
    events.value = []
  }
}

const onEventSelected = async () => {
  if (!selectedEventId.value) return

  try {
    const graphQLClient = new GraphQLClient('https://api.start.gg/gql/alpha', {
      headers: {
        Authorization: `Bearer ${startggToken}`
      }
    })

    const query = gql`
      query GetEventSets($eventId: ID!) {
        event(id: $eventId) {
          sets(perPage: 50) {
            nodes {
              id
              round
              slots {
                entrant {
                  name
                  team { name }
                  participants {
                    gamerTag
                    user {
                      genderPronoun
                      location { country }
                    }
                  }
                }
                standing {
                  stats { score { value } }
                }
              }
            }
          }
        }
      }
    `

    const data = await graphQLClient.request(query, { eventId: selectedEventId.value })

    matches.value = data.event?.sets?.nodes.map(set => ({
      id: set.id,
      display: set.slots.map(slot => slot.entrant?.name || '').join(' vs '),
      slots: set.slots,
      round: set.round
    })) || []

  } catch (error) {
    console.error('Failed to fetch matches', error)
    toast.error('Failed to fetch matches.')
    matches.value = []
  }
}

const onMatchSelected = () => {
  const match = matches.value.find(m => m.id === selectedMatchId.value)
  if (!match) return

  match.slots.forEach((slot, index) => {
    const playerInfo = extractPlayerInfo(slot)
    const playerNumber = index + 1

    fields.value.forEach(field => {
      const lowerName = field.name.toLowerCase()

      if (lowerName.includes(`player ${playerNumber}`)) {
        if (lowerName.includes('name')) field.value = playerInfo.name || ''
        else if (lowerName.includes('score')) field.value = playerInfo.score
        else if (lowerName.includes('sponsor')) field.value = playerInfo.sponsor || ''
        else if (lowerName.includes('twitter')) field.value = playerInfo.twitter || ''
        else if (lowerName.includes('country')) field.value = playerInfo.country || ''
        else if (lowerName.includes('pronoun')) field.value = playerInfo.pronoun || ''
      }
    })
  })

  fields.value.forEach(field => {
    if (field.name.toLowerCase().includes('tournament') && field.name.toLowerCase().includes('round')) {
      field.value = match.round ? `Round ${match.round}` : ''
    }
  })
}


const extractPlayerInfo = (slot) => {
  if (!slot?.entrant) return {}

  const entrant = slot.entrant
  const participant = entrant.participants?.[0]

  return {
    name: entrant.name || participant?.gamerTag || '',
    sponsor: entrant.team?.name || '',
    twitter: participant?.user?.authorizations?.[0]?.externalUsername || '',
    pronoun: participant?.user?.genderPronoun || '',
    country: participant?.user?.location?.country || '',
    score: slot.standing?.stats?.score?.value ?? '0'
  }
}
const copyOverlayLink = async () => {
  try {
    await navigator.clipboard.writeText(overlayLink)
    toast.success('Overlay link copied! ✅')
  } catch (err) {
    console.error('Failed to copy:', err)
    toast.error('Failed to copy link ❌')
  }
}
const incrementScore = field => {
  field.value = Number(field.value) + 1
}
const decrementScore = field => {
  field.value = Math.max(0, Number(field.value) - 1)
}
onMounted(() => {
  fetchStreamboard()
})
</script>

<template>
  <DefaultLayout :is-dark-mode="isDarkMode">
    <div class="controller-container">
      <!-- title row: left static, right scoreboard name + edit -->
      <div class="title-row">
        <h1>Streamboard Controller</h1>
        <div class="board-info">
          <span>{{ scoreboardName }}</span>
          <router-link 
            :to="`/boards/new?id=${boardId}&edit=true`" 
            class="edit-btn"
          >
            Edit
          </router-link>
        </div>
      </div>

      <div class="startgg-section">
        <label>Tournament URL:</label>
        <input v-model="tournamentUrl" @input="onTournamentUrlChange" placeholder="Paste Start.gg tournament URL" />

        <div v-if="events.length">
          <label>Select Event:</label>
          <select v-model="selectedEventId" @change="onEventSelected">
            <option disabled value="">-- Choose Event --</option>
            <option v-for="event in events" :key="event.id" :value="event.id">
              {{ event.name }}
            </option>
          </select>
        </div>

        <div v-if="matches.length">
          <label>Select Match:</label>
          <select v-model="selectedMatchId" @change="onMatchSelected">
            <option disabled value="">-- Choose Match --</option>
            <option v-for="match in matches" :key="match.id" :value="match.id">
              {{match.slots.map(s => s.entrant?.name).filter(Boolean).join(' vs ')}}
            </option>
          </select>
        </div>
      </div>

      <div v-if="streamboard">
        <form @submit.prevent="saveChanges" class="fields-form">
          <div v-for="(field, index) in fields" :key="index" class="field-item">
            <label>{{ field.name }}</label>
            <div v-if="field.name.toLowerCase().includes('score')" class="score-input">
              <button type="button" @click="decrementScore(field)">–</button>
              <input
                v-model.number="field.value"
                type="number"
                @keydown.up.prevent="incrementScore(field)"
                @keydown.down.prevent="decrementScore(field)"
              />
              <button type="button" @click="incrementScore(field)">+</button>
            </div>
            <input v-else v-model="field.value" type="text" />
          </div>

          <button type="submit" :disabled="isSaving">
            {{ isSaving ? 'Saving...' : 'Save Changes' }}
          </button>
        </form>

        <div class="overlay-preview-wrapper">
          <iframe
            :src="overlayLink"
            frameborder="0"
            class="overlay-preview"
          ></iframe>
        </div>

        <div class="overlay-link">
          <h3>Public Overlay Link:</h3>
          <input :value="overlayLink" readonly />
          <button @click="copyOverlayLink">📋 Copy Link</button>
        </div>
      </div>

      <div v-else>
        Loading...
      </div>
    </div>
  </DefaultLayout>
</template>

<style scoped>
.controller-container {
  padding: 20px;
}

.startgg-section {
  margin-bottom: 30px;
}

.startgg-section input,
.startgg-section select {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.overlay-preview-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}
.overlay-preview {
  width: 100%;
  max-width: 960px;
  aspect-ratio: 16/9;
  border: 1px solid #ccc;
}

.fields-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-width: 400px;
}

.field-item label {
  font-weight: bold;
}

.field-item input {
  padding: 8px;
  border-radius: 8px;
  border: 1px solid #ccc;
  width: 100%;
}

.fields-form button {
  padding: 10px;
  background-color: #2d7bff;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  margin-top: 20px;
  cursor: pointer;
}

.overlay-link {
  margin-top: 40px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.overlay-link input {
  width: 80%;
  padding: 8px;
  margin-right: 10px;
}

/* larger Nexa Heavy controller title */
.title-row h1 {
  font-family: 'Nexa', sans-serif;
  font-weight: bold;
  font-size: 3rem;
  color: #2d7bff;
  margin: 0;
}

.score-input {
  display: flex;
  align-items: center;
}
.score-input button {
  width: 24px;
  height: 24px;
  margin: 0 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

/* title row layout */
.title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.board-info {
  display: flex;
  align-items: center;
}

.board-info span {
  font-size: 1.2rem;
  font-weight: bold;
  margin-right: 8px;
}

.edit-btn {
  padding: 4px 8px;
  font-size: 0.9rem;
  border: 1px solid #2d7bff;
  background: #fff;
  color: #2d7bff;
  border-radius: 4px;
  text-decoration: none;
}
</style>

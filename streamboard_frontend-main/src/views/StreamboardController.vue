<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { GraphQLClient, gql } from 'graphql-request'
import { useToast } from 'vue-toastification'

const route = useRoute()
const router = useRouter()
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

const fetchStreamboard = async () => {
  try {
    const { data } = await axios.get(`http://127.0.0.1:8000/api/streamboard/${boardId}/`)
    streamboard.value = data
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
    const accessToken = localStorage.getItem('access_token')

    const payload = {
      fields: fields.value.map(field => ({
        id: field.id,
        name: field.name,
        x: field.x,
        y: field.y,
        font_size: field.font_size,
        color: field.color,
        value: field.value,
      }))
    }

    await axios.patch(`http://127.0.0.1:8000/api/streamboard/${boardId}/`, payload, {
      headers: {
        Authorization: `Bearer ${accessToken}`
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
        Authorization: `Bearer c56e70671542a9aef164b1d4938186ad`
      }
    })

    const query = gql`
      query GetTournamentEvents($slug: String!) {
        tournament(slug: $slug) {
          events {
            id
            name
          }
        }
      }
    `
    const data = await graphQLClient.request(query, { slug })
    events.value = data.tournament?.events || []
  } catch (error) {
    console.error('Failed to fetch events', error)
    events.value = []
    toast.error('Failed to fetch events from tournament URL.')
  }
}

const onEventSelected = async () => {
  if (!selectedEventId.value) return

  try {
    const graphQLClient = new GraphQLClient('https://api.start.gg/gql/alpha', {
      headers: {
        Authorization: `Bearer c56e70671542a9aef164b1d4938186ad`
      }
    })

    const query = gql`
      query GetEventSets($eventId: ID!) {
        event(id: $eventId) {
          sets(perPage: 50) {
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
    `
    const data = await graphQLClient.request(query, { eventId: selectedEventId.value })
    matches.value = data.event?.sets?.nodes.map(set => ({
      id: set.id,
      display: set.slots.map(s => s.entrant?.name).filter(Boolean).join(' vs ')
    })) || []
  } catch (error) {
    console.error('Failed to fetch matches', error)
    matches.value = []
    toast.error('Failed to fetch matches.')
  }
}

const onMatchSelected = () => {
  const match = matches.value.find(m => m.id === selectedMatchId.value)
  if (!match) return

  const [player1, player2] = match.display.split(' vs ')

  if (fields.value.length >= 4) {
    fields.value[0].value = player1 || ''
    fields.value[1].value = player2 || ''
    fields.value[2].value = '0'
    fields.value[3].value = '0'
  }
}

onMounted(() => {
  fetchStreamboard()
})
</script>

<template>
  <div class="controller-container">
    <h1>Edit Streamboard</h1>

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
            {{ match.display }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="streamboard">
      <img :src="streamboard.background_image" class="background-preview" alt="Background" />

      <form @submit.prevent="saveChanges" class="fields-form">
        <div v-for="(field, index) in fields" :key="index" class="field-item">
          <label>{{ field.name }}</label>
          <input v-model="field.value" type="text" />
        </div>

        <button type="submit" :disabled="isSaving">
          {{ isSaving ? 'Saving...' : 'Save Changes' }}
        </button>
      </form>

      <div class="overlay-link">
        <h3>Public Overlay Link:</h3>
        <input :value="overlayLink" readonly />
        <button @click="() => { navigator.clipboard.writeText(overlayLink); toast.success('Overlay link copied!') }">
          📋 Copy Link
        </button>
      </div>
    </div>

    <div v-else>
      Loading...
    </div>
  </div>
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

.background-preview {
  width: 100%;
  max-width: 960px;
  margin-bottom: 20px;
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
}

.overlay-link input {
  width: 80%;
  padding: 8px;
  margin-right: 10px;
}
</style>

<template>
    <div class="tournament-selector">
      <h2 class="title">Select a Tournament 🎯</h2>
  
      <input
        v-model="tournamentUrl"
        type="text"
        class="input"
        placeholder="Paste start.gg tournament URL"
      />
  
      <button class="btn" @click="fetchEvents">
        Fetch Events
      </button>
  
      <div v-if="events.length" class="event-dropdown">
        <label class="dropdown-label">Select Event:</label>
        <select v-model="selectedEventId" class="dropdown">
          <option disabled value="">Please select an event</option>
          <option v-for="event in events" :key="event.id" :value="event.id">
            {{ event.name }}
          </option>
        </select>
      </div>
  
      <div v-if="selectedEventId" class="selected-event">
        <p>✅ Selected Event ID: {{ selectedEventId }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import { useToast } from 'vue-toastification'
  
  const tournamentUrl = ref('')
  const events = ref([])
  const selectedEventId = ref('')
  const toast = useToast()
  
  const fetchEvents = async () => {
    if (!tournamentUrl.value) {
      toast.error('Please enter a tournament URL.')
      return
    }
  
    try {
      const slugMatch = tournamentUrl.value.match(/tournament\/([^\/]+)/)
      if (!slugMatch) {
        toast.error('Invalid tournament URL.')
        return
      }
  
      const slug = slugMatch[1]
  
      const query = `
        query TournamentQuery($slug: String!) {
          tournament(slug: $slug) {
            events {
              id
              name
            }
          }
        }
      `
  
      const response = await axios.post('https://api.start.gg/gql/alpha', {
        query,
        variables: { slug }
      }, {
        headers: {
          'Authorization': `Bearer c56e70671542a9aef164b1d4938186ad`,
          'Content-Type': 'application/json'
        }
      })
  
      const fetchedEvents = response.data?.data?.tournament?.events || []
  
      if (!fetchedEvents.length) {
        toast.error('No events found for this tournament.')
      }
  
      events.value = fetchedEvents
      selectedEventId.value = ''
  
      toast.success('Events fetched successfully!')
    } catch (error) {
      console.error(error)
      toast.error('Failed to fetch events.')
    }
  }
  </script>
  
  <style scoped>
  .tournament-selector {
    max-width: 500px;
    margin: 50px auto;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    background: #ffffff;
    text-align: center;
  }
  
  .title {
    font-size: 1.8rem;
    font-weight: bold;
    margin-bottom: 20px;
  }
  
  .input {
    width: 100%;
    padding: 10px;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 8px;
    margin-bottom: 15px;
  }
  
  .btn {
    width: 100%;
    padding: 12px;
    background-color: #2d7bff;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    margin-bottom: 20px;
    font-size: 1rem;
    transition: background 0.3s;
  }
  
  .btn:hover {
    background-color: #155edb;
  }
  
  .event-dropdown {
    margin-bottom: 20px;
    text-align: left;
  }
  
  .dropdown-label {
    font-weight: bold;
    margin-bottom: 5px;
    display: block;
  }
  
  .dropdown {
    width: 100%;
    padding: 10px;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 8px;
  }
  
  .selected-event {
    margin-top: 20px;
    background: #e9f6ff;
    padding: 15px;
    border-radius: 8px;
    font-size: 1rem;
  }
  
  @media (max-width: 600px) {
    .tournament-selector {
      margin: 20px;
      padding: 15px;
    }
  
    .title {
      font-size: 1.5rem;
    }
  }
  </style>
  
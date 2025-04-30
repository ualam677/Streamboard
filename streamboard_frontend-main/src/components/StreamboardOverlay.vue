<template>
    <div class="overlay-wrapper">
        <div v-if="backgroundImageUrl" class="overlay-container" ref="overlayContainer">
            <img :src="backgroundImageUrl" class="background-image" @load="handleImageLoad" alt="Background" />
            <div v-for="(field, index) in fields" :key="index" class="field" :style="{
                left: field.x + 'px',
                top: field.y + 'px',
                color: field.color,
                fontSize: (field.fontSize || 24) + 'px'
            }">
                {{ field.value }}
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const boardId = route.params.id

const backgroundImageUrl = ref('')
const fields = ref([])
const overlayContainer = ref(null)
let pollingInterval = null


const fetchStreamboard = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/streamboard/${boardId}/`)
    const data = response.data

    backgroundImageUrl.value = data.background_image || ''

    fields.value = Array.isArray(data.layout_json) ? data.layout_json : []

  } catch (error) {
    console.error('Error fetching streamboard:', error)
    fields.value = []
  }
}

const handleImageLoad = () => {
    const container = overlayContainer.value
    if (container) {
        container.style.width = container.firstChild.naturalWidth + 'px'
        container.style.height = container.firstChild.naturalHeight + 'px'
    }
}

onMounted(() => {
    fetchStreamboard()
    pollingInterval = setInterval(fetchStreamboard, 2000)
})
onUnmounted(() => {
  clearInterval(pollingInterval)
})
</script>

<style scoped>
.overlay-container {
    position: relative;
    width: 1365px;
    height: 768px;
    overflow: hidden;
    margin: 0 auto;
    background-color: black;
}
.background-image {
    width: 100%;
    height: 100%;
    object-fit: contain;
}
.field {
    position: absolute;
    z-index: 2;
    font-weight: bold;
    white-space: nowrap;
}
</style>
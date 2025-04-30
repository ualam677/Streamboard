<template>
    <div class="overlay-wrapper">
      <div
        v-if="backgroundImageUrl"
        class="overlay-container"
        ref="overlayContainer"
      >
        <img
          :src="backgroundImageUrl"
          class="background-image"
          @load="handleImageLoad"
          alt="Background"
        />
  
        <div
          v-for="(field, index) in fields"
          :key="index"
          class="field"
          :style="getFieldStyle(field)"
        >
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
      const response = await axios.get(
        `http://127.0.0.1:8000/api/streamboard/${boardId}/retrieve/`
      )
      const data = response.data
      backgroundImageUrl.value = data.background_image || ''
      fields.value = Array.isArray(data.layout_json)
        ? data.layout_json
        : []
    } catch (error) {
      console.error('Error fetching streamboard:', error)
      fields.value = []
    }
  }
  
  const handleImageLoad = () => {
    const container = overlayContainer.value
    if (container) {
      const img = container.querySelector('img')
      container.style.width = img.naturalWidth + 'px'
      container.style.height = img.naturalHeight + 'px'
    }
  }
  
  /**
   * Build a CSS style object for each field based on its JSON props.
   */
  const getFieldStyle = (field) => {
    const justifyMap = {
      left: 'flex-start',
      center: 'center',
      right: 'flex-end',
    }
    const alignMap = {
      top: 'flex-start',
      middle: 'center',
      bottom: 'flex-end',
    }
  
    return {
      position: 'absolute',
      left: `${field.x}px`,
      top: `${field.y}px`,
      width: `${field.width}px`,
      height: `${field.height}px`,
  
      display: 'flex',
      justifyContent: justifyMap[field.alignment] || 'flex-start',
      alignItems: alignMap[field.verticalAlignment] || 'flex-start',
  
      color: field.color,
      fontSize: `${field.fontSize}px`,
      fontWeight: field.bold ? 'bold' : 'normal',
      fontStyle: field.italic ? 'italic' : 'normal',
      fontFamily: field.fontFamily || 'sans-serif',
  
      overflow: 'hidden',
      whiteSpace: 'nowrap',
      textOverflow: 'ellipsis',
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
    overflow: hidden;
    margin: 0 auto;
  }
  
  .background-image {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
  
  .field {
    z-index: 2;
  }
  </style>

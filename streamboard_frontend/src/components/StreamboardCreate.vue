<template>
    <div class="create-streamboard-page">
        <h1 class="title">🎨 Create a New Streamboard</h1>

        <div class="upload-box">
            <label for="background-upload" class="upload-label">
                📷 Upload Background Image
            </label>
            <input id="background-upload" type="file" @change="handleBackgroundUpload" />
        </div>

        <div v-if="backgroundImage" class="background-preview">
            <img :src="backgroundImage" alt="Background Preview" @load="handleImageLoad" />
        </div>

        <div class="controls">
            <button class="btn add-field" @click="addField">➕ Add Text Field</button>
            <button class="btn save" @click="saveStreamboard">💾 Save Streamboard</button>
        </div>

        <div v-if="backgroundImage" class="overlay-editor"
            :style="{ backgroundImage: `url(${backgroundImage})`, width: naturalWidth + 'px', height: naturalHeight + 'px' }">

            <div v-for="(field, index) in fields" :key="index" class="overlay-field" :style="{
                top: field.y + 'px',
                left: field.x + 'px',
                fontSize: field.fontSize + 'px',
                color: field.color
            }" @mousedown.prevent="startDragging(field, $event)">
                {{ field.name }}
            </div>

        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

const router = useRouter()
const toast = useToast()

const backgroundImage = ref(null)
const backgroundFile = ref(null) // we need to upload real file
const fields = ref([])
const naturalWidth = ref(0)
const naturalHeight = ref(0)

const handleImageLoad = (e) => {
    naturalWidth.value = e.target.naturalWidth
    naturalHeight.value = e.target.naturalHeight
}

const handleBackgroundUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
        backgroundFile.value = file
        const reader = new FileReader()
        reader.onload = (e) => {
            backgroundImage.value = e.target.result
        }
        reader.readAsDataURL(file)
    }
}

const addField = () => {
    fields.value.push({
        name: 'New Field',
        x: 50,
        y: 50,
        fontSize: 24,
        color: 'red',
    })
}

const saveStreamboard = async () => {
    if (!backgroundFile.value || fields.value.length === 0) {
        toast.error('Please upload a background and add at least one field.')
        return
    }
    const fieldsToSave = fields.value.map(field => ({
        ...field,
        y: field.y < 0 ? 0 : field.y,
        x: field.x < 0 ? 0 : field.x, // 🔥 bonus: fix x too if negative
    }));

    try {
        const formData = new FormData()
        formData.append('background_image', backgroundFile.value)
        formData.append('layout_json', JSON.stringify(fieldsToSave))  // <-- corrected here

        const accessToken = localStorage.getItem('access_token')

        const response = await axios.post('http://127.0.0.1:8000/api/streamboard/', formData, {
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'multipart/form-data'
            }
        })

        toast.success('Streamboard created successfully! 🚀')

        const streamboardId = response.data.id
        router.push(`/boards/${streamboardId}/controller`) // Move to controller page
    } catch (error) {
        console.error(error)
        toast.error('Failed to create Streamboard. Please try again.')
    }
}
let draggingField = null

const startDragging = (field, event) => {
    draggingField = field
    const onMouseMove = (e) => {
        draggingField.x += e.movementX
        draggingField.y += e.movementY
    }
    const onMouseUp = () => {
        document.removeEventListener('mousemove', onMouseMove)
        document.removeEventListener('mouseup', onMouseUp)
        draggingField = null
    }
    document.addEventListener('mousemove', onMouseMove)
    document.addEventListener('mouseup', onMouseUp)
}
</script>

<style scoped>
.create-streamboard-page {
    max-width: 1200px;
    margin: 40px auto;
    padding: 20px;
    text-align: center;
}

.title {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 30px;
    background: linear-gradient(to right, #4facfe, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.upload-box {
    margin-bottom: 20px;
}

.upload-label {
    display: block;
    font-weight: bold;
    margin-bottom: 10px;
}

.background-preview img {
    width: 100%;
    max-width: 800px;
    margin: 20px auto;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
}

.controls {
    margin-top: 20px;
    display: flex;
    justify-content: center;
    gap: 20px;
}

.btn {
    background-color: #2d7bff;
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 10px;
    font-weight: bold;
    cursor: pointer;
    font-size: 1rem;
    transition: 0.3s;
}

.btn:hover {
    opacity: 0.9;
}

.overlay-editor {
    position: relative;
    margin-top: 30px;
    margin-left: auto;
    margin-right: auto;
    background-repeat: no-repeat;
    background-size: contain;
    border: 2px dashed #ccc;
    overflow: hidden;
    /* 👈 Important to avoid dragging fields outside */
}

.overlay-field {
    position: absolute;
    background-color: rgba(0, 0, 0, 0.5);
    padding: 5px 10px;
    border-radius: 5px;
    cursor: move;
    user-select: none;
}
</style>
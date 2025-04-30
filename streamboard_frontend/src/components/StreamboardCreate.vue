<template>
    <DefaultLayout :is-dark-mode="isDarkMode">
        <div class="create-streamboard-page">
            <h1 class="title">
                ✨ {{ isEditMode ? 'Edit Streamboard' : 'Create a New Streamboard' }}
            </h1>

            <div class="title-input">
                <label for="board-title" class="upload-label">🏷️ Board Title:</label>
                <input id="board-title" type="text" v-model="boardTitle" placeholder="Enter board title here..."
                    class="title-textbox" />
            </div>
            <div class="upload-box">
                <label for="logo-upload" class="upload-label">🖼️ Upload Logo Image</label>
                <input id="logo-upload" type="file" @change="handleLogoUpload" />
            </div>

            <div v-if="logoImage" class="logo-preview">
                <img :src="logoImage" alt="Logo Preview" style="max-height: 100px; margin-top: 10px;" />
            </div>
            <div class="upload-box">
                <label for="background-upload" class="upload-label">📷 Upload Background Image</label>
                <input id="background-upload" type="file" @change="handleBackgroundUpload" />
            </div>

            <div v-if="backgroundImage" class="background-preview">
                <img :src="backgroundImage" alt="Background Preview" @load="handleImageLoad" />
            </div>

            <div class="controls">
                <button class="btn add-field" @click="showAddFieldModal = true">
                    ➕ Add Field
                </button>
                <button class="btn save" @click="saveStreamboard">
                    💾 Save Streamboard
                </button>
            </div>

            <div v-if="backgroundImage" ref="editorRef" class="overlay-editor">
                <img :src="backgroundImage" :width="naturalWidth" :height="naturalHeight" class="background-img"
                    alt="Streamboard Background" @click="captureClickPosition($event)" />
                <div v-for="(field, index) in fields" :key="index" class="overlay-field" :style="getFieldStyles(field)"
                    @mousedown.self.prevent="startDragging(field, $event)"
                    @pointerdown.self.prevent=" startDragging(field, $event)">
                    <button class=" delete-button" @click.stop="deleteField(index)">✖</button>
                    <input type="color" v-model="field.color" class="color-picker" @click.stop />
                    <span class="resize-handle" @mousedown.self.stop.prevent="startResizing(field, $event)"
                        @pointerdown.self.stop.prevent="startResizing(field, $event)">⤡</span>
                    <div class="field-label" @mousedown.self.prevent="startDragging(field, $event)"
                        @pointerdown.self.prevent=" startDragging(field, $event)">{{ field.name }}</div>
                    <div class="field-controls" @click.stop>
                        <select v-model="field.alignment">
                            <option value="left">Left</option>
                            <option value="center">Center</option>
                            <option value="right">Right</option>
                        </select>
                        <select v-model="field.verticalAlignment">
                            <option value="top">Top</option>
                            <option value="middle">Middle</option>
                            <option value="bottom">Bottom</option>
                        </select>
                        <input type="number" v-model.number="field.fontSize" min="10" max="100" class="font-size-input"
                            placeholder="Size" />
                        <select v-model="field.fontFamily">
                            <option v-for="font in availableFonts" :key="font" :value="font"
                                :style="{ fontFamily: font }">
                                {{ font }}
                            </option>
                        </select>
                        <button @click="field.bold = !field.bold" :class="{ active: field.bold }">B</button>
                        <button @click="field.italic = !field.italic" :class="{ active: field.italic }">I</button>
                    </div>
                </div>
            </div>

            <AddFieldModal v-if="showAddFieldModal" :show="showAddFieldModal"
                :onClose="() => (showAddFieldModal = false)" :onConfirm="handleAddField" :numPlayers="2" />
        </div>
    </DefaultLayout>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useToast } from 'vue-toastification'
import AddFieldModal from '@/components/AddFieldModal.vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

const router = useRouter()
const route = useRoute()
const toast = useToast()
const boardTitle = ref('')
const isEditMode = ref(false)
const streamboardId = ref(null)
const backgroundImage = ref(null)
const backgroundFile = ref(null)
const fields = ref([])
const naturalWidth = ref(0)
const naturalHeight = ref(0)
const showAddFieldModal = ref(false)
const editorRef = ref(null)
const clickPosition = ref({ x: 0, y: 0 })

const availableFonts = ref([
    'Nexa',
    'Arial',
    'Helvetica',
    'Verdana',
    'Tahoma',
    'Trebuchet MS',
    'Times New Roman',
    'Georgia',
    'Palatino Linotype',
    'Book Antiqua',
    'Courier New',
    'Lucida Console',
    'Lucida Sans Unicode',
    'Garamond',
    'Comic Sans MS',
    'Impact',
    'Segoe UI',
    'Consolas'
])


onMounted(() => {
    isEditMode.value = route.query.edit === 'true'
    streamboardId.value = route.query.id || null
    if (isEditMode.value && streamboardId.value) loadExistingStreamboard()
})

// reflect current theme setting
const isDarkMode = ref(localStorage.getItem('theme') === 'dark')

const logoImage = ref(null)
const logoFile = ref(null)

const handleLogoUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
        logoFile.value = file
        const reader = new FileReader()
        reader.onload = (ev) => {
            logoImage.value = ev.target.result
        }
        reader.readAsDataURL(file)
    }
}

const captureClickPosition = e => {
    const rect = e.target.getBoundingClientRect()
    clickPosition.value.x = e.clientX - rect.left + editorRef.value.scrollLeft
    clickPosition.value.y = e.clientY - rect.top + editorRef.value.scrollTop
}

const loadExistingStreamboard = async () => {
    try {
        const token = localStorage.getItem('access_token')
        const { data } = await axios.get(
            `http://127.0.0.1:8000/api/streamboard/${streamboardId.value}/`,
            { headers: { Authorization: `Bearer ${token}` } }
        )
        backgroundImage.value = data.background_image
        boardTitle.value = data.title
        logoImage.value = data.logo || null

        nextTick(() => {
            naturalWidth.value = data.width || naturalWidth.value
            naturalHeight.value = data.height || naturalHeight.value
        })
        fields.value = Array.isArray(data.layout_json)
            ? data.layout_json.map(f => ({
                ...f,
                verticalAlignment: f.verticalAlignment || 'middle',
                bold: f.bold || false,
                italic: f.italic || false,
                fontFamily: f.fontFamily || 'Arial'
            }))
            : []
    } catch {
        toast.error('Failed to load Streamboard.')
    }
}

const formatTournamentField = type => ({
    tournament_name: 'Tournament Name',
    tournament_round: 'Tournament Round',
    bracket_link: 'Bracket Link'
}[type] || type)

const formatPlayerField = type => ({
    name: 'Name', score: 'Score', sponsor: 'Sponsor',
    twitter: 'Twitter', pronouns: 'Pronouns', country: 'Country'
}[type] || type)

const handleAddField = (player, fieldType) => {
    const defaultW = 150
    const defaultH = 50
    let name = ''
    if (fieldType === 'custom') name = player
    else if (player === 'tournament') name = formatTournamentField(fieldType)
    else name = `Player ${player} ${formatPlayerField(fieldType)}`

    const x = clickPosition.value.x
    const y = clickPosition.value.y

    fields.value.push({
        player,
        type: fieldType,
        name,
        x: x - defaultW / 2,
        y: y - defaultH / 2,
        width: defaultW,
        height: defaultH,
        fontSize: 24,
        color: '#ffffff',
        alignment: 'center',
        verticalAlignment: 'middle',
        bold: false,
        italic: false,
        fontFamily: 'Arial'
    })
    showAddFieldModal.value = false
}

const deleteField = i => fields.value.splice(i, 1)

let dragging = null
let draggingprevX = 0, draggingprevY = 0

function startDragging(field, e) {
    dragging = field
    draggingprevX = e.clientX
    draggingprevY = e.clientY

    const onMove = ev => {
        const dx = ev.movementX != null
            ? ev.movementX
            : ev.clientX - draggingprevX
        const dy = ev.movementY != null
            ? ev.movementY
            : ev.clientY - draggingprevY

        draggingprevX = ev.clientX
        draggingprevY = ev.clientY

        dragging.x += dx
        dragging.y += dy
    }

    const onUp = () => {
        document.removeEventListener('mousemove', onMove)
        document.removeEventListener('pointermove', onMove)
        document.removeEventListener('mouseup', onUp)
        document.removeEventListener('pointerup', onUp)
        dragging = null
    }

    document.addEventListener('mousemove', onMove)
    document.addEventListener('pointermove', onMove)
    document.addEventListener('mouseup', onUp)
    document.addEventListener('pointerup', onUp)
}

let resizing = null
let prevX = 0
let prevY = 0

const startResizing = (field, e) => {
    resizing = field
    prevX = e.clientX
    prevY = e.clientY

    const onMove = ev => {
        const dx = (ev.movementX != null)
            ? ev.movementX
            : ev.clientX - prevX
        const dy = (ev.movementY != null)
            ? ev.movementY
            : ev.clientY - prevY

        prevX = ev.clientX
        prevY = ev.clientY

        resizing.width = Math.max(20, resizing.width + dx)
        resizing.height = Math.max(20, resizing.height + dy)
    }

    const onUp = () => {
        document.removeEventListener('mousemove', onMove)
        document.removeEventListener('pointermove', onMove)
        document.removeEventListener('mouseup', onUp)
        document.removeEventListener('pointerup', onUp)
        resizing = null
    }

    document.addEventListener('mousemove', onMove)
    document.addEventListener('pointermove', onMove)
    document.addEventListener('mouseup', onUp)
    document.addEventListener('pointerup', onUp)
}

const getFieldStyles = f => ({
    position: 'absolute', top: f.y + 'px', left: f.x + 'px', width: f.width + 'px', height: f.height + 'px',
    color: f.color, fontSize: f.fontSize + 'px', fontWeight: f.bold ? 'bold' : 'normal', fontStyle: f.italic ? 'italic' : 'normal',
    fontFamily: f.fontFamily, display: 'flex', textAlign: f.alignment,
    justifyContent: f.alignment === 'left' ? 'flex-start' : f.alignment === 'right' ? 'flex-end' : 'center',
    alignItems: f.verticalAlignment === 'top' ? 'flex-start' : f.verticalAlignment === 'bottom' ? 'flex-end' : 'center'
})

const handleBackgroundUpload = e => {
    const file = e.target.files[0]
    if (file) { backgroundFile.value = file; const reader = new FileReader(); reader.onload = ev => (backgroundImage.value = ev.target.result); reader.readAsDataURL(file) }
}

const handleImageLoad = e => {
    naturalWidth.value = e.target.naturalWidth
    naturalHeight.value = e.target.naturalHeight
}

const saveStreamboard = async () => {
    if (!backgroundImage.value || fields.value.length === 0) {
        toast.error('Please upload a background and add at least one field.')
        return
    }

    const fieldsToSave = fields.value.map(field => ({
        ...field,
        y: Math.max(0, field.y),
        x: Math.max(0, field.x),
        width: field.width || 150,
        height: field.height || 50,
    }))

    const accessToken = localStorage.getItem('access_token')

    try {
        if (isEditMode.value) {
            const formData = new FormData()

            formData.append('title', boardTitle.value)
            formData.append('layout_json', JSON.stringify(fieldsToSave))

            if (backgroundFile.value) {
                formData.append('background_image', backgroundFile.value)
            }
            if (logoFile.value) {
                formData.append('logo', logoFile.value)
            }

            await axios.patch(`http://127.0.0.1:8000/api/streamboard/${streamboardId.value}/`, formData, {
                headers: {
                    Authorization: `Bearer ${accessToken}`,
                    'Content-Type': 'multipart/form-data'
                }
            })

            toast.success('Streamboard updated successfully! 🚀')
            router.push(`/boards/${streamboardId.value}/controller`)

        } else {
            const formData = new FormData()
            formData.append('background_image', backgroundFile.value)
            formData.append('layout_json', JSON.stringify(fieldsToSave))
            formData.append('title', boardTitle.value)
            formData.append('logo', logoFile.value)

            const response = await axios.post('http://127.0.0.1:8000/api/streamboard/', formData, {
                headers: {
                    Authorization: `Bearer ${accessToken}`,
                    'Content-Type': 'multipart/form-data'
                }
            })

            toast.success('Streamboard created successfully! 🎨')
            router.push(`/boards/${response.data.id}/controller`)
        }
    } catch (error) {
        console.error(error)
        toast.error('Failed to save Streamboard.')
    }
}
</script>

<style>
.create-streamboard-page {
    background: var(--background-color);
    color: var(--text-color);
    max-width: 1200px;
    margin: 40px auto;
    padding: 20px;
    text-align: center;
}

/* larger Nexa Heavy title */
.title {
  font-family: 'Nexa', sans-serif;
  font-weight: bold;
  font-size: 3rem;
  color: #2d7bff !important;
}

.upload-box,
.title-input {
    margin-bottom: 20px;
}

.upload-label {
    display: block;
    font-weight: bold;
    margin-bottom: 10px;
}

.title-textbox {
    width: 100%;
    max-width: 500px;
    padding: 10px;
    font-size: 18px;
    border-radius: 8px;
    border: 1px solid #ccc;
    margin: 0 auto;
}

.background-preview img {
    width: 100%;
    max-width: 800px;
    margin: 20px auto;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.controls {
    margin-top: 20px;
    display: flex;
    justify-content: center;
    gap: 20px;
}

.btn {
    background-color: var(--button-background);
    color: black;
    padding: 12px 20px;
    border-radius: 10px;
    font-weight: bold;
    font-size: 1rem;
    cursor: pointer;
}

.controls .btn {
  background-color: #2d7bff;
  color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.overlay-editor {
    position: relative;
    width: 100%;
    height: 80vh;
    overflow: auto;
    border: 2px dashed #ccc;
    box-sizing: border-box;
}

.background-img {
    display: block;
}

.overlay-field {
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 5px;
    cursor: move;
    user-select: none;
    touch-action: none;
    cursor: grab;
}

.overlay-field:active {
    cursor: grabbing;
}

.delete-button {
    position: absolute;
    top: -10px;
    right: -10px;
    background: red;
    color: white;
    border: none;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    font-size: 12px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.color-picker {
    position: absolute;
    top: -10px;
    left: -10px;
    width: 20px;
    height: 20px;
    background: transparent;
    cursor: pointer;
}

.resize-handle {
    position: absolute;
    bottom: 0;
    right: 0;
    cursor: se-resize;
    font-size: 12px;
    background: rgba(255, 255, 255, 0.2);
    padding: 2px;
    touch-action: none;
}

.field-controls {
    position: absolute;
    bottom: -36px;
    left: 0;
    display: flex;
    gap: 4px;
    background: rgba(255, 255, 255, 0.9);
    padding: 2px;
    border-radius: 4px;
    z-index: 2;
}

.field-controls select,
.field-controls input {
    font-size: 12px;
    padding: 2px;
}

.field-controls button {
    font-weight: bold;
    border: none;
    background: transparent;
    cursor: pointer;
}

.field-controls button.active {
    text-decoration: underline;
}
</style>
<template>
    <div class="layout-container">
        <Sidebar />
        <main class="page-content" style="background: var(--background-color); color: var(--text-color);">
            <slot />
        </main>
    </div>
</template>

<script setup>
import { watch, onMounted } from 'vue'
import Sidebar from '@/components/Sidebar.vue'

const props = defineProps({
    isDarkMode: {
        type: Boolean,
        required: true
    }
})
const applyThemeToMain = (isDark) => {
    const main = document.querySelector('.page-content')
    if (main) {
        if (isDark) {
            main.style.backgroundColor = '#121212'
            main.style.color = '#f0f0f0'           
        } else {
            main.style.backgroundColor = '#ffffff'
            main.style.color = '#111111'           
        }
    }
}

watch(() => props.isDarkMode, (newVal) => {
    console.log('Dark mode switched:', newVal)
    const html = document.documentElement

    if (newVal) {
        html.classList.add('dark-mode')
    } else {
        html.classList.remove('dark-mode')
    }

    applyThemeToMain(newVal)
}, { immediate: true })

onMounted(() => {
    applyThemeToMain(props.isDarkMode)
})
</script>

<style>
.layout-container {
    display: flex;
    min-height: 100vh;
    background: var(--background-color);
    color: var(--text-color);
}

.page-content {
    margin-left: 80px;
    flex: 1;
    /* padding: 20px; */
    overflow-x: hidden;
}

@media (max-width: 768px) {
    .layout-container {
        flex-direction: column;
    }

    .page-content {
        margin-left: 0;
        margin-top: 80px;
        width: 100%;
    }
}
</style>
<template>
  <router-view />
</template>

<script setup>
</script>

<style>
@font-face {
  font-family: 'Nexa';
  src: url('@/assets/fonts/Nexa-Heavy.ttf') format('truetype');
  font-weight: bold;
}

@font-face {
  font-family: 'Nexa';
  src: url('@/assets/fonts/Nexa-Bold.ttf') format('truetype');
  font-weight: 300;
}
html, body, #app {
  margin: 0;
  padding: 0;
  width: 100vw;
  height: 100vh;
  box-sizing: border-box;
  font-family: 'Nexa', sans-serif;
}

*, *::before, *::after {
  box-sizing: inherit;
}

.app-wrapper {
  width: 100vw;
  height: 100vh;
  display: flex;
}

</style>

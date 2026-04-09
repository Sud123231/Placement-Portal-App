<template>
  <DriveView>
    <template #actions>
      <button class="btn blue small" @click="goBack">
        Go Back
      </button>
    </template>
  </DriveView>
</template>

<script setup>
import DriveView from './Driveview.vue'
import router from '/src/router/index.js'

const goBack = () => router.back()
</script>

<style scoped>
.btn {
  background-color: white;
  border-radius: 5px;
  padding: 6px 12px;
  cursor: pointer;
  border: 1px solid transparent;
  font-weight: 500;
  transition: all 0.3s ease;
}
.btn.small {
  padding: 5px 24px;
}

.btn.blue {
  border: 1px solid #3088f2;
  color: #3088f2;
}

.btn.blue:hover {
  background-color: #3088f2;
  color: white;
}

</style>
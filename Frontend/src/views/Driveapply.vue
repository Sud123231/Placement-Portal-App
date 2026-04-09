<template>
  <DriveView>
    <template #actions>
      <button 
        class="btn blue small"
        @click="showPanel = true"
        :disabled="applied"
      >
        <span v-if="applied">Applied ✔</span>
        <span v-else>Apply</span>
      </button>

      <button class="btn blue small" @click="goBack">
        Go Back
      </button>
    </template>
  </DriveView>

  <!-- SUCCESS TOAST -->
  <div v-if="showSuccess" class="toast success">
    Successfully applied to drive
  </div>

  <!-- ERROR TOAST -->
  <div v-if="errorMessage" class="toast error">
    {{ errorMessage }}
  </div>

  <!-- BOTTOM PANEL -->
  <div class="panel" v-if="showPanel">
    <div class="panel-content">

      <h3>Upload Resume</h3>

      <!-- DRAG & DROP -->
      <div 
        class="drop-zone"
        @dragover.prevent
        @drop.prevent="handleDrop"
        @click="triggerFileInput"
      >
        <p v-if="!selectedFile">Drag & drop resume here or click</p>
        <p v-else>{{ selectedFile.name }}</p>
      </div>

      <!-- HIDDEN INPUT -->
      <input 
        type="file" 
        ref="fileInput"
        accept=".pdf"
        @change="handleFile"
        style="display: none"
      />

      <div class="panel-actions">
        <button class="btn blue small" @click="handleApply">Upload & Apply</button>
        <button id = "cancel-btn" class="btn red small" @click="showPanel = false">Cancel</button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DriveView from './Driveview.vue'
import api from '/src/services/api.js'
import router from '/src/router/index.js'
import { useRoute } from 'vue-router'

const route = useRoute()

const showPanel = ref(false)
const showSuccess = ref(false)
const errorMessage = ref('')
const selectedFile = ref(null)
const applicationId = ref(null)
const applied = ref(false)
const fileInput = ref(null)

const goBack = () => router.back()

// APPLY + UPLOAD
const handleApply = async () => {
  if (applied.value) return

  if (!selectedFile.value) {
    errorMessage.value = 'Please select a resume file first'
    setTimeout(() => (errorMessage.value = ''), 3000)
    return
  }

  const student_id = localStorage.getItem('student_id')

  const formData = new FormData()
  formData.append('drive_id', route.params.id)
  formData.append('resume', selectedFile.value)

  try {
    const res = await api.post(`/api/students/${student_id}/applications`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    applicationId.value = res.data.application_id
    applied.value = true
    showSuccess.value = true
    showPanel.value = false

    setTimeout(() => (showSuccess.value = false), 3000)

  } catch (err) {
    if (err.response) {
      errorMessage.value = err.response.data?.message || 'Something went wrong'
      if (err.response.status === 400) {
        applied.value = true
        showPanel.value = false
      }
      setTimeout(() => (errorMessage.value = ''), 3000)
    } else {
      errorMessage.value = 'Network error. Please try again.'
      setTimeout(() => (errorMessage.value = ''), 3000)
    }
  }
}

// FILE PICK
const triggerFileInput = () => {
  fileInput.value.click()
}

// FILE SELECT
const handleFile = (e) => {
  selectedFile.value = e.target.files[0]
}

// DRAG DROP
const handleDrop = (e) => {
  selectedFile.value = e.dataTransfer.files[0]
}
</script>

<style scoped>

/* TOAST */
.toast {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 20px;
  border-radius: 6px;
  color: white;
  font-size: 14px;
  z-index: 1000;
  animation: fadeSlide 0.3s ease;
}

/* SUCCESS */
.toast.success {
  background-color: #22c55e;
}

/* ERROR */
.toast.error {
  background-color: #ef4444;
}

/* ANIMATION */
@keyframes fadeSlide {
  from {
    opacity: 0;
    transform: translate(-50%, -10px);
  }
  to {
    opacity: 1;
    transform: translate(-50%, 0);
  }
}

/* PANEL */
.panel {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background: rgba(0, 0, 0, 0.3);
}

.panel-content {
  background: #fff;
  padding: 20px;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
  text-align: center;
  animation: slideUp 0.3s ease;
}

/* DROP ZONE */
.drop-zone {
  border: 2px dashed #3088f2;
  padding: 20px;
  border-radius: 10px;
  margin: 12px 0;
  cursor: pointer;
  transition: background 0.2s ease;
}

.drop-zone:hover {
  background-color: #f5f9ff;
}

/* PANEL ANIMATION */
@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
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
#cancel-btn {
  margin-left:10px;
}
.btn.red {
  border: 1px solid #ef4444;
  color: #ef4444;
}
.btn.red:hover {
  background-color: #ef4444;
  color: white;
}
</style>
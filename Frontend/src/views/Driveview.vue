<template>
  <div class="page">
    <div class="card">

      <div v-if="loading" class="muted">Loading...</div>

      <div v-else-if="error" class="muted">{{ error }}</div>

      <div v-else-if="drive">

        <div class="drive-layout">

          <!-- Left Side -->
          <div class="drive-info">
            <h1>{{ drive.name }}</h1>
            <hr class="divider" />

            <div class="info-block">
              <span class="label">Job Title</span>
              <span class="value">{{ drive.job_title }}</span>
            </div>

            <div class="info-block">
              <span class="label">Job Description</span>
              <p class="value">{{ drive.job_description }}</p>
            </div>

            <div class="info-block">
              <span class="label">Salary</span>
              <span class="value">{{ drive.salary }}</span>
            </div>

            <div class="info-block">
              <span class="label">Location</span>
              <span class="value">{{ drive.location }}</span>
            </div>

            <div class="info-block">
              <span class="label">Status</span>
              <span class="status-badge" :class="drive.status?.toLowerCase()">{{ drive.status }}</span>
            </div>

          </div>

          <!-- Right Side -->
          <div class="company-box">
            <i class="bi bi-building company-icon"></i>
            <span class="company-name">{{ drive.company_name }}</span>
          </div>

        </div>

        <!-- Actions Slot -->
        <div class="actions">
          <slot name="actions"></slot>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '/src/services/api.js'
import { useRoute } from 'vue-router'

const route = useRoute()

const drive = ref(null)
const loading = ref(true)
const error = ref('')

const fetchDrive = async () => {
  try {
    const res = await api.get(`/api/drives/${route.params.id}`)
    drive.value = res.data.drive
  } catch (err) {
    error.value = 'Failed to load drive'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchDrive()
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: sans-serif;
}

.page {
  display: flex;
  justify-content: center;
  padding: 40px 20px;
  background: #f4f8ff;
  min-height: 100vh;
}

.card {
  width: 100%;
  max-width: 1100px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08);
  padding: 30px 40px;
  height: fit-content;
}

/* Layout */
.drive-layout {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 30px;
}

/* Left */
.drive-info {
  flex: 1;
}

.drive-info h1 {
  color: #002b80;
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 12px;
}

.divider {
  margin: 12px 0 20px 0;
  border: none;
  height: 1px;
  background: #e2e8ff;
}

/* Info Blocks */
.info-block {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px 16px;
  background: #f9fbff;
  border: 1px solid #e2e8ff;
  border-radius: 10px;
  margin-bottom: 10px;
}

.label {
  font-size: 13px;
  font-weight: 600;
  color: #002b80;
  min-width: 120px;
}

.value {
  font-size: 14px;
  color: #333;
  font-weight: 400;
  line-height: 1.6;
}

/* Status Badge */
.status-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 3px 12px;
  border-radius: 20px;
  text-transform: capitalize;
}

.status-badge.ongoing {
  background: #dcfce7;
  color: #16a34a;
}

.status-badge.completed {
  background: #e0f0ff;
  color: #3088f2;
}

.status-badge.suspended {
  background: #fee2e2;
  color: #dc2626;
}

/* Right - Company Box */
.company-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px 20px;
  min-width: 160px;
  border: 1px solid #e2e8ff;
  border-radius: 12px;
  background: #f9fbff;
}

.company-icon {
  font-size: 50px;
  color: #4a7dff;
}

.company-name {
  font-size: 13px;
  font-weight: 600;
  color: #002b80;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Actions */
.actions {
  margin-top: 28px;
  display: flex;
  justify-content: center;
  gap: 12px;
}

/* Misc */
.muted {
  color: #888;
  font-style: italic;
  text-align: center;
  padding: 30px 0;
}
</style>
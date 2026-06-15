<template>
  <div class="page">
    <div class="card">

      <div v-if="loading" class="muted">Loading...</div>

      <div v-else-if="error" class="muted">{{ error }}</div>

      <div v-else-if="application">

        <div class="app-layout">

          <!-- Left Side -->
          <div class="app-info">
            <h1>Student Application</h1>
            <hr class="divider" />

            <div class="info-block">
              <span class="label">Student Name</span>
              <span class="value">{{ application.name }}</span>
            </div>

            <div class="info-block">
              <span class="label">Department</span>
              <span class="value">{{ application.department }}</span>
            </div>

            <div class="info-block">
              <span class="label">Drive</span>
              <span class="value">{{ application.drive }}</span>
            </div>

            <div class="info-block">
              <span class="label">Job Title</span>
              <span class="value">{{ application.job_title }}</span>
            </div>

            <div class="info-block">
              <span class="label">Status</span>
              <span class="status-badge" :class="application.status?.toLowerCase()">{{ application.status }}</span>
            </div>

          </div>

          <!-- Right Side: Student Avatar -->
          <div class="avatar-box">
            <div class="avatar-circle">
              <i class="bi bi-person-workspace avatar-icon"></i>
            </div>
          </div>

        </div>

        <!-- Buttons -->
        <div class="actions">
          <slot name="actions"></slot>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import router from '/src/router/index.js'
import api from '/src/services/api.js';
import { useRoute } from 'vue-router';

const route = useRoute();

const application = ref(null);
const loading = ref(true);
const error = ref('');

const fetchApplication = async () => {
  try {
    const appId = route.params.id;
    const res = await api.get(`/api/applications/${appId}`);
    application.value = res.data;
  } catch (err) {
    error.value = 'Failed to load application details.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchApplication();
});
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

/* Two-column layout */
.app-layout {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 30px;
}

/* Left */
.app-info {
  flex: 1;
}

.app-info h1 {
  color: #002b80;
  font-size: 22px;
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
  align-items: center;
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
}

/* Status Badge */
.status-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 3px 12px;
  border-radius: 20px;
  text-transform: capitalize;
}

.status-badge.applied {
  background: #e0f0ff;
  color: #3088f2;
}

.status-badge.shortlisted {
  background: #fef9c3;
  color: #b45309;
}

.status-badge.selected {
  background: #dcfce7;
  color: #16a34a;
}

.status-badge.rejected {
  background: #fee2e2;
  color: #dc2626;
}

/* Right - Avatar */
.avatar-box {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  min-width: 140px;
}

.avatar-circle {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  background: #f0f4ff;
  border: 2px solid #c5d4ff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-icon {
  font-size: 55px;
  color: #4a7dff;
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
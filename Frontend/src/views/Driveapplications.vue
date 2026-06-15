<template>
  <div class="page">
    <div class="card">

      <div v-if="loading" class="muted">Loading...</div>

      <div v-else-if="error" class="muted">{{ error }}</div>

      <div v-else>
        <h1>Update Applications for the Drive</h1>
        <h3 class="subtitle">Job Title: {{ jobTitle }}</h3>

        <hr class="divider" />

        <h2>Received Applications</h2>

        <div class="list">
          <div v-if="applications.length === 0">
            <p class="muted">No applications received.</p>
          </div>
          <div v-for="app in applications" :key="app.id" class="list-item">
            <div class="item-left">
              <span class="name">{{ app.student_name }}</span>
            </div>
            <div class="item-actions">
              <button class="btn blue small" @click="reviewApplication(app.id)">review application</button>
            </div>
          </div>
        </div>

        <div class="actions">
          <button class="btn green small" @click="goBack">save</button>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '/src/services/api.js';
import router from '/src/router/index.js'
import {useRoute} from 'vue-router';

const route = useRoute();

const applications = ref([]);
const jobTitle = ref('');
const loading = ref(true);
const error = ref('');

const driveId = route.params.id;

const fetchApplications = async () => {
  try {
    const res = await api.get(`/api/drives/${driveId}/applications`);
    applications.value = res.data.applications;
    jobTitle.value = res.data.job_title;
  } catch (err) {
    error.value = 'Failed to load applications.';
  } finally {
    loading.value = false;
  }
};

const reviewApplication = (id) => {
  router.push(`/student/application/${id}/update`);
};

const goBack = () => {
  router.back();
};

onMounted(() => {
  fetchApplications();
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
}

.card {
  width: 100%;
  max-width: 1100px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08);
  padding: 30px 40px;
}

h1 {
  color: #002b80;
  font-size: 22px;
  font-weight: 600;
}

.subtitle {
  font-size: 14px;
  color: #333;
  margin-top: 10px;
}

h2 {
  margin-top: 25px;
  font-size: 20px;
  color: #002b80;
  border-left: 4px solid #4a7dff;
  padding-left: 8px;
}

.divider {
  margin: 20px 0;
  border: none;
  height: 1px;
  background: #e2e8ff;
}

/* List */
.list {
  margin-top: 12px;
}

.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 16px;
  background: #f9fbff;
  border: 1px solid #e2e8ff;
  border-radius: 10px;
  margin-bottom: 10px;
  transition: 0.25s;
}

.list-item:hover {
  background: #eef3ff;
  transform: scale(1.01);
}

.item-left {
  display: flex;
  align-items: center;
}

.name {
  font-weight: 500;
  color: #333;
}

.item-actions {
  display: flex;
  gap: 8px;
}

/* Actions */
.actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* Buttons */
.btn {
  background-color: white;
  border-radius: 5px;
  padding: 6px 12px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  font-weight: 500;
}

.btn.small {
  padding: 5px 14px;
  font-size: 0.9rem;
}

.btn.blue {
  border: 1px solid #3088f2;
  color: #3088f2;
}
.btn.blue:hover {
  background-color: #3088f2;
  color: white;
}

.btn.green {
  border: 1px solid #22c55e;
  color: #22c55e;
}
.btn.green:hover {
  background-color: #22c55e;
  color: white;
}

.btn:hover {
  transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out;
}

.muted {
  color: #888;
  font-style: italic;
  text-align: center;
  padding: 20px 0;
}
</style>
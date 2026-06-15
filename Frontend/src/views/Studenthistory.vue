<template>
  <div class="page">
    <div class="card">
      <div v-if="loading" class="muted">Loading...</div>

      <div v-else-if="error" class="muted">{{ error }}</div>

      <div v-else>
        <div class="top-row">
          <h1>Student Application History</h1>

          <div class="actions">
            <button
              class="btn blue small"
              :disabled="exporting"
              @click="exportHistory"
            >
              {{ exporting ? 'Exporting...' : 'Export' }}
            </button>
            <button class="btn blue small" @click="goBack">Back</button>
          </div>
        </div>

        <p v-if="exportMessage" class="status success">{{ exportMessage }}</p>
        <p v-if="exportError" class="status error-text">{{ exportError }}</p>

        <hr class="divider" />

        <h4 class="info">Student Name: {{ studentName }}</h4>
        <h4 class="info">Department: {{ department }}</h4>

        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Drive No.</th>
                <th>Drive Name</th>
                <th>Job Title</th>
                <th>Results</th>
                <th>Remark</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="applications.length === 0">
                <td colspan="5" class="muted">No applications found.</td>
              </tr>
              <tr v-for="(app, idx) in applications" :key="app.id">
                <td>{{ idx + 1 }}.</td>
                <td>{{ app.drive }}</td>
                <td>{{ app.job_title }}</td>
                <td>{{ app.status }}</td>
                <td>{{ app.remark || 'None' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '/src/services/api.js';
import router from '/src/router/index.js';

const route = useRoute();
const studentId = route.params.id;

const applications = ref([]);
const studentName = ref('');
const department = ref('');
const loading = ref(true);
const error = ref('');
const exporting = ref(false);
const exportMessage = ref('');
const exportError = ref('');
let exportMessageTimer = null;

const fetchApplications = async () => {
  try {
    const res = await api.get(`/api/students/${studentId}/applications`);
    applications.value = res.data.applications;
    studentName.value = res.data.student_name;
    department.value = res.data.department;
  } catch (err) {
    error.value = 'Failed to load history.';
  } finally {
    loading.value = false;
  }
};

const goBack = () => {
  router.back();
};

const downloadExport = async (filename) => {
  const response = await api.get(`/api/exports/${filename}`, {
    responseType: 'blob',
  });

  const blobUrl = window.URL.createObjectURL(response.data);
  const link = document.createElement('a');
  link.href = blobUrl;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(blobUrl);
};

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const clearExportMessageLater = (delayMs = 3000) => {
  if (exportMessageTimer) {
    clearTimeout(exportMessageTimer);
  }

  exportMessageTimer = setTimeout(() => {
    exportMessage.value = '';
    exportMessageTimer = null;
  }, delayMs);
};

const exportHistory = async () => {
  if (exporting.value) {
    return;
  }

  exportMessage.value = 'Starting export...';
  exporting.value = true;

  try {
    const { data: startData } = await api.post(
      `/api/students/${studentId}/export-applications`,
    );

    const taskId = startData.task_id;
    if (!taskId) {
      throw new Error('Task id missing from server response.');
    }

    for (let attempt = 0; attempt < 30; attempt += 1) {
      const { data: statusData } = await api.get(`/api/export-status/${taskId}`);
      const status = statusData.status;

      if (status === 'completed') {
        const taskResult = statusData.result || {};
        if (taskResult.status !== 'success' || !taskResult.filename) {
          throw new Error(taskResult.message || 'Export failed.');
        }

        window.alert('Export completed. Downloading file now.');
        await downloadExport(taskResult.filename);
        exportMessage.value = 'Download started...';
        return;
      }

      if (status === 'error') {
        throw new Error(statusData.message || 'Export failed.');
      }

      exportMessage.value = statusData.message || 'Preparing your export...';
      await sleep(2000);
    }

    throw new Error('Export is taking longer than expected. Try again in a moment.');
  } catch (err) {
    exportError.value =
      err.response?.data?.message || 'Unable to export';
  } finally {
    exporting.value = false;
  }
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
  font-family: "Poppins", sans-serif;
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

.top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.top-row h1 {
  color: #002b80;
  font-size: 22px;
  font-weight: 600;
}

.actions {
  display: flex;
  gap: 10px;
}

.status {
  margin-top: 14px;
  font-size: 14px;
}

.success {
  color: #1f6f43;
}

.error-text {
  color: #b42318;
}

.info {
  font-size: 14px;
  color: #333;
  margin-bottom: 6px;
}

.divider {
  margin: 16px 0;
  border: none;
  height: 1px;
  background: #e2e8ff;
}

.table-wrap {
  margin-top: 16px;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

table th,
table td {
  padding: 10px 14px;
  border-bottom: 1px solid #e2e8ff;
  text-align: left;
}

table th {
  background: #f0f4ff;
  color: #002b80;
  font-weight: 600;
}

table tbody tr:hover {
  background: #f7f9ff;
}

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
  padding: 5px 18px;
  font-size: 0.9rem;
}

.btn.blue {
  border: 1px solid #3088f2;
  color: #3088f2;
}

.btn.blue:hover:not(:disabled) {
  background-color: #3088f2;
  color: white;
  transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out;
}

.btn:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.muted {
  color: #888;
  font-style: italic;
  text-align: center;
}
</style>

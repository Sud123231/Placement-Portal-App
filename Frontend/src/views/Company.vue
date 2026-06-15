<template>
  <div class="page">
    <div class="card">

      <!-- Top Row -->
      <div class="top-row">
        <h1>Welcome {{ company.name }}</h1>
        <button class="link-btn" @click="handleLogout">logout</button>
      </div>

      <hr class="divider" />

      <!-- Upcoming Drives -->
      <div class="section-header">
        <h2>Upcoming Drives</h2>
        <button class="btn green small" @click="goToCreateDrive">Create Drive</button>
      </div>

      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Sr No.</th>
              <th>Drive Name</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="ongoingDrives.length === 0">
              <td colspan="3" class="muted">No upcoming drives.</td>
            </tr>
            <tr v-for="(drive,idx) in ongoingDrives" :key="drive.id">
              <td>{{ idx + 1 }}</td>
              <td>{{ drive.name }}</td>
              <td class="action-cell">
                <button class="btn blue small" @click="viewDetails(drive.id)">view details</button>
                <button class="btn green small" @click="markComplete(drive.id)">mark as complete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Closed Drives -->
      <h2>Closed Drives</h2>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Sr No.</th>
              <th>Drive Name</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="closedDrives.length === 0">
              <td colspan="3" class="muted">No closed drives.</td>
            </tr>
            <tr v-for="drive in closedDrives" :key="drive.id">
              <td>{{ drive.id }}</td>
              <td>{{ drive.name }}</td>
              <td class="action-cell">
                <button class="btn blue small" @click="updateDrive(drive.id)">update</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import router from '/src/router/index.js'
import api from '/src/services/api.js';
import { useRoute} from 'vue-router';

const route = useRoute();

const company = ref({ name: '' });
const ongoingDrives = ref([]);
const closedDrives = ref([]);
const companyId=route.params.id;

const fetchCompany = async () => {
  const res = await api.get(`/api/companies/${companyId}`);
  company.value = res.data.company;
};

const fetchDrives = async () => {
  const res = await api.get(`/api/companies/${companyId}/drives`);
  const companyDrives = res.data.drives;
  ongoingDrives.value = companyDrives.filter(d => d.status === 'Ongoing');
  closedDrives.value = companyDrives.filter(d => d.status === 'Completed' || d.status === 'Cancelled');
};

const viewDetails = (id) => {
  router.push(`/drives/${id}/applications`);
};

const markComplete = async (id) => {
  await api.patch(`/api/drives/${id}`, { status: 'Completed' });
  await fetchDrives();
};

const updateDrive = (id) => {
  router.push(`/drives/${id}/edit`);
};

const goToCreateDrive = () => {
  router.push(`/company/${companyId}/drives/create`);
};

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

onMounted(() => {
  fetchCompany();
  fetchDrives();
});
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: sans-serif;
}

.link-btn {
  background: none;
  border: none;
  color: #555;
  font-size: 14px;
  font-family: "Poppins", sans-serif;
  cursor: pointer;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.link-btn:hover {
  background: #f0f4ff;
  color: #3088f2;
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

/* Top Row */
.top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.top-row h1 {
  color: #002b80;
  font-size: 24px;
  font-weight: 600;
}

/* Section header with button */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 25px;
}

.section-header h2 {
  margin-top: 0;
}

/* Section Titles */
h2 {
  margin-top: 25px;
  font-size: 20px;
  color: #002b80;
  border-left: 4px solid #4a7dff;
  padding-left: 8px;
}

/* Table */
.table-wrap {
  margin-top: 15px;
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
  text-align:center;
}

table th {
  background: #f0f4ff;
  color: #002b80;
  font-weight: 600;
}

table tbody tr:hover {
  background: #f7f9ff;
}

.action-cell {
  display: flex;
  gap: 8px;
  justify-content:center;
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
  text-decoration: none;
}

.btn.small {
  padding: 5px 10px;
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

.btn.red {
  border: 1px solid #ef4444;
  color: #ef4444;
}
.btn.red:hover {
  background-color: #ef4444;
  color: white;
}

.btn:hover {
  transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out;
}

/* Misc */
.muted {
  color: #888;
  font-style: italic;
  text-align: center;
}

.divider {
  margin: 20px 0;
  border: none;
  height: 1px;
  background: #e2e8ff;
}
</style>
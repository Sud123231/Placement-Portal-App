<template>
  <div class="page">
    <div class="card">

      <!-- Top Row -->
      <div class="top-row">
        <h1>Welcome {{ student.name }}</h1>
        <div class="top-actions">
          <button class="link-btn" @click="editProfile">edit profile</button>
          <span class="separator">|</span>
          <button class="link-btn" @click="history">History</button>
          <span class="separator">|</span>
          <button class="link-btn" @click="handleLogout">logout</button>
        </div>
      </div>

      <hr class="divider" />

      <!-- Organizations -->
      <h2>Organizations</h2>
      <div class="list">
        <p class="muted" v-if="companies.length === 0">No organizations found.</p>
        <div v-for="company in companies" :key="company.id" class="list-item">
          <div class="item-left">
            <span class="name">{{ company.name }}</span>
          </div>
          <div class="item-actions">
            <button class="btn blue small" @click="viewCompany(company.id)">view details</button>
          </div>
        </div>
      </div>

      <!-- Applied Drives -->
      <h2>Applied Drives</h2>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Sr No.</th>
              <th>Drive Name</th>
              <th>Company</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="appliedDrives.length === 0">
              <td colspan="5" class="muted">No applied drives.</td>
            </tr>
            <tr v-for="(drive, idx) in appliedDrives" :key="drive.drive_id">
              <td>{{ idx + 1 }}.</td>
              <td>{{ drive.drive_name }}</td>
              <td>{{ drive.company_name }}</td>
              <td>{{ drive.applied_date }}</td>
              <td>
                <button class="btn blue small" @click="viewDrive(drive.drive_id)">view details</button>
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
import { useRoute } from 'vue-router';
import api from '/src/services/api.js';
import router from '/src/router/index.js';

const route = useRoute();

const studentId = route.params.id;

const student = ref({ name: '' });
const companies = ref([]);
const appliedDrives = ref([]);

const fetchStudent = async () => {
  const res = await api.get(`/api/students/${studentId}`);
  student.value = res.data.student;
};

const fetchCompanies = async () => {
  const res = await api.get('/api/companies');
  companies.value = res.data.companies;
};

const fetchAppliedDrives = async () => {
  const res = await api.get(`/api/students/${studentId}/drives`);
  appliedDrives.value = res.data.applied_drives;
};

const viewCompany = (id) => {
  router.push(`/companies/${id}`);
};

const viewDrive = (id) => {
  router.push(`/drives/${id}`);
};

const editProfile = () => {
  router.push(`/student/${studentId}/edit`);
};

const history = () => {
  router.push(`/student/${studentId}/history`);
};

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

onMounted(() => {
  fetchStudent();
  fetchCompanies();
  fetchAppliedDrives();
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

/* Top Row */
.top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.top-row h1 {
  color: #002b80;
  font-size: 24px;
  font-weight: 600;
}

.top-actions {
  display: flex;
  align-items: center;
  gap: 4px;
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

.separator {
  color: #ccc;
  font-size: 14px;
}

/* Section Titles */
h2 {
  margin-top: 25px;
  font-size: 20px;
  color: #002b80;
  border-left: 4px solid #4a7dff;
  padding-left: 8px;
}

/* Divider */
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
  transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out;
}

/* Misc */
.muted {
  color: #888;
  font-style: italic;
  text-align: center;
}
</style> 
<template>
  <div class="page">
    <div class="card">

      <div v-if="loading" class="muted">Loading...</div>

      <div v-else-if="error" class="muted">{{ error }}</div>

      <div v-else>

        <!-- Top Row -->
        <div class="top-row">
          <h1>{{ company.name }}</h1>
          <button class="link-btn" @click="handleLogout">logout</button>
        </div>

        <hr class="divider" />

        <!-- Overview -->
        <h2>Overview</h2>
        <p class="description">{{ company.description }}</p>

        <!-- Current Drives -->
        <h2>Current Drives</h2>
        <div class="list">
          <p class="muted" v-if="drives.length === 0">No current drives.</p>
          <div v-for="drive in drives" :key="drive.id" class="list-item">
            <div class="item-left">
              <span class="name">{{ drive.name }}</span>
            </div>
            <div class="item-actions">
              <button class="btn blue small" @click="viewDrive(drive.id)">view details</button>
            </div>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '/src/services/api.js'
import router from '/src/router/index.js'

const route = useRoute();

const companyId = route.params.id;

const company = ref({});
const drives = ref([]);
const loading = ref(true);
const error = ref('');
const student = ref({});

const fetchCompany = async () => {
  const res = await api.get(`/api/companies/${companyId}`);
  company.value = res.data.company;
};

const fetchStudent = async () =>{
   const student_id = localStorage.getItem("student_id");
   const res = await api.get(`/api/students/${student_id}`);
   student.value = res.data.student;
};   


const fetchDrives = async () => {
  const res = await api.get(`/api/companies/${companyId}/drives`);
  drives.value = res.data.drives.filter( d => student.value.cgpa >= d.min_cgpa && d.status === 'Ongoing');
};

const viewDrive = (id) => {
  router.push(`/drives/${id}/apply`);
};

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

onMounted(async () => {
  try {
    await fetchCompany();
    await fetchStudent();
    await fetchDrives();
  } catch (err) {
    error.value = 'Failed to load company details.';
  } finally {
    loading.value = false;
  }
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
}

.top-row h1 {
  color: #002b80;
  font-size: 24px;
  font-weight: 600;
}

/* Divider */
.divider {
  margin: 20px 0;
  border: none;
  height: 1px;
  background: #e2e8ff;
}

/* Section Titles */
h2 {
  margin-top: 25px;
  font-size: 20px;
  color: #002b80;
  border-left: 4px solid #4a7dff;
  padding-left: 8px;
}

/* Description */
.description {
  margin-top: 10px;
  font-size: 14px;
  color: #333;
  line-height: 1.7;
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
  transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out;
}

/* Misc */
.muted {
  color: #888;
  font-style: italic;
  text-align: center;
}
</style>
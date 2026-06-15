<template>
  <div class="page">
    <div class="card">

      <div v-if="loading" class="muted">Loading...</div>

      <div v-else-if="error" class="muted">{{ error }}</div>

      <div v-else>

        <div class="top-row">
          <h1>Edit Profile</h1>
          <button class="btn blue small" @click="goBack">back</button>
        </div>

        <hr class="divider" />

        <div class="form">

          <div class="form-row">
            <label>Full Name</label>
            <input v-model="form.name" type="text" />
          </div>

          <div class="form-row">
            <label>Department</label>
            <input v-model="form.department" type="text" />
          </div>

          <div class="form-row">
            <label>New Password</label>
            <input v-model="form.password" type="password" placeholder="Leave blank to keep current" />
          </div>

          <div class="actions">
            <button class="btn green small" @click="handleSave">save</button>
          </div>

        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '/src/services/api.js';

const route = useRoute();
const router = useRouter();

const studentId = route.params.id;

const form = ref({
  name: '',
  department: '',
  password: ''
});

const loading = ref(true);
const error = ref('');

const fetchStudent = async () => {
  try {
    const res = await api.get(`/api/students/${studentId}`);
    const student = res.data.student;
    form.value.name = student.name;
    form.value.department = student.department;
  } catch (err) {
    error.value = 'Failed to load profile.';
  } finally {
    loading.value = false;
  }
};

const handleSave = async () => {
  try {
    const payload = {
      name: form.value.name,
      department: form.value.department,
      ...(form.value.password && { password: form.value.password })
    };
    await api.patch(`/api/students/${studentId}`, payload);
    router.push(`/student/${studentId}`);
  } catch (err) {
    error.value = 'Failed to update profile.';
  }
};

const goBack = () => {
  router.back();
};

onMounted(() => {
  fetchStudent();
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
  font-size: 22px;
  font-weight: 600;
}

.divider {
  margin: 20px 0;
  border: none;
  height: 1px;
  background: #e2e8ff;
}

/* Form */
.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.form-row label {
  width: 150px;
  min-width: 150px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  text-align: right;
}

.form-row input {
  flex: 1;
  padding: 7px 10px;
  border: 1px solid #c5d4ff;
  border-radius: 6px;
  font-size: 14px;
  font-family: "Poppins", sans-serif;
  outline: none;
  transition: 0.3s;
}

.form-row input:focus {
  border-color: #4a7dff;
  box-shadow: 0 0 0 3px rgba(74, 125, 255, 0.15);
}

/* Actions */
.actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
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
  padding: 5px 18px;
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
  transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out;
}

.muted {
  color: #888;
  font-style: italic;
  text-align: center;
  padding: 30px 0;
}
</style>
<template>
  <div class="page">
    <div class="card">

      <h1>Create a Drive</h1>

      <hr class="divider" />

      <div class="form">

        <div class="form-row">
          <label>Drive Name</label>
          <input v-model="form.name" type="text" />
        </div>

        <div class="form-row">
          <label>Job Title</label>
          <input v-model="form.job_title" type="text" />
        </div>

        <div class="form-row">
          <label>Job Description</label>
          <textarea v-model="form.job_description"></textarea>
        </div>

        <div class="form-row">
          <label>Eligibility Criteria</label>
          <input v-model="form.eligibility_criteria" type="text" />
        </div>

        <div class="form-row">
          <label>Application Deadline</label>
          <input v-model="form.application_deadline" type="date" />
        </div>

        <div class="form-row">
          <label>Salary</label>
          <input v-model="form.salary" type="number" />
        </div>

        <div class="form-row">
          <label>Location</label>
          <input v-model="form.location" type="text" />
        </div>

        <div class="form-row">
          <label>Min-CGPA</label>
          <input v-model="form.min_cgpa" title="leave empty if nothing" type="number" />
        </div>

        <div class="actions">
          <button class="btn green small" @click="handleSave">save</button>
        </div>

      </div>

    </div>
    <div v-if="errorMessage" class="toast error">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import router from '/src/router/index.js';
import api from '/src/services/api.js';
import { useRoute} from 'vue-router';

const route = useRoute();
const errorMessage = ref('');


const form = ref({
  name: '',
  job_title: '',
  job_description: '',
  eligibility_criteria: '',
  application_deadline: '',
  salary: '',
  location: '',
  min_cgpa:null
});

const handleSave = async () => {
  const companyId = route.params.id;
  try {
    await api.post('/api/drives', {
      ...form.value,
      id: companyId
    });

    router.push(`/company/${companyId}`);

  } catch (err) {
    errorMessage.value =
      err.response?.data?.message || 'Failed to create drive';

    setTimeout(() => {
      errorMessage.value = '';
    }, 3000);
  }
};
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

h1 {
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
  align-items: flex-start;
  gap: 16px;
}

.form-row label {
  width: 180px;
  min-width: 180px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  padding-top: 7px;
  text-align: right;
}

.form-row input,
.form-row textarea {
  flex: 1;
  padding: 7px 10px;
  border: 1px solid #c5d4ff;
  border-radius: 6px;
  font-size: 14px;
  font-family: "Poppins", sans-serif;
  outline: none;
  transition: 0.3s;
}

.form-row input:focus,
.form-row textarea:focus {
  border-color: #4a7dff;
  box-shadow: 0 0 0 3px rgba(74, 125, 255, 0.15);
}

.form-row textarea {
  height: 80px;
  resize: vertical;
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

.btn.green {
  border: 1px solid #22c55e;
  color: #22c55e;
}

.btn.green:hover {
  background-color: #22c55e;
  color: white;
  transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out;
}
/* ADD THIS ONLY */
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

.toast.error {
  background-color: #ef4444;
}

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
</style>
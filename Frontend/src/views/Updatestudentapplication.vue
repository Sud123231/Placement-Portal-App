<template>
   <studentbaseapplication>
        <template #actions>
            <a :href="`${api.defaults.baseURL}/api/students/applications/${route.params.id}/resume`" 
            target="_blank" 
            class="btn blue small">view resume</a>

            <select v-model="status" class="status-select" @change="updateStatus">
                <option value="Shortlisted">Shortlist</option>
                <option value="Selected">Select</option>
                <option value="Rejected">Reject</option>
            </select>

            <button class="btn blue small" @click="goBack">back</button>
        </template>
    </studentbaseapplication>    
</template>

<script setup>
import studentbaseapplication from './Studentapplicationbase.vue';
import { ref } from 'vue';
import api from '/src/services/api.js';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const status = ref('');

const updateStatus = async () => {
  await api.patch(`/api/applications/${route.params.id}`, { status: status.value });
};

const goBack = () => {
  router.back();
};
</script>

<style scoped>
.status-select {
  padding: 5px 10px;
  border: 1px solid #3088f2;
  border-radius: 5px;
  color: #3088f2;
  font-size: 0.9rem;
  font-family: "Poppins", sans-serif;
  outline: none;
  cursor: pointer;
  background: white;
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
  text-decoration: none;
  display: inline-block;
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
  transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out;
}
</style>

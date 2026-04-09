<template>
    <studentapplicationbase>
      <template v-slot:actions>
          <a :href="`${api.defaults.baseURL}/api/students/applications/${route.params.id}/resume`" target="_blank" class="btn blue small">view resume</a>
          <button class="btn blue small" @click="goBack">back</button>
      </template>
    </studentapplicationbase>
</template>

<script setup>
import studentapplicationbase from './Studentapplicationbase.vue';
import router from '/src/router/index.js';
import api from '/src/services/api.js';
import { useRoute } from 'vue-router';

const route=useRoute();

const goBack = () => {
  router.back()
}; 

</script>

<style scoped>
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
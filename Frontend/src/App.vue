<template>
  <div>
    <!-- ================= NAVBAR ================= -->
    <nav v-if="showPublicNavbar" class="navbar-section">
      <div class="logo">
        🎓 Student Placement Portal
      </div>

      <ul class="nav-links">
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/register">Register</router-link></li>
        <li><router-link to="/login">Login</router-link></li>
      </ul>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const publicNavbarRoutes = ['/', '/register', '/login']
const showPublicNavbar = computed(() => publicNavbarRoutes.includes(route.path))
   
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}
h1 {
  margin-bottom: 16px;
}
/* =========================
   NAVBAR
========================= */
.navbar-section {
  width: 100%;
  background: #1f56f0;
  position: relative;
  z-index: 10;

  display: flex;
  justify-content: space-between;
  align-items: center;

  padding: 0 36px;
  min-height: 70px;
  border-bottom: 2px solid rgba(0, 0, 0, 0.2);
  box-shadow: 0 7px 10px rgba(0, 0, 0, 0.1);
}

.logo {
  color: white;
  font-size: 1.35rem;
  font-weight: 700;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 14px;

  list-style: none;
}

.nav-links a {
  text-decoration: none;
  color: white;

  font-size: 0.95rem;
  font-weight: 500;

  padding: 13px 22px;
  border-radius: 12px;

  transition: 0.3s ease;
}

.nav-links a:hover {
  background: rgba(255, 255, 255, 0.12);
}

.router-link-active {
  background: rgba(0, 0, 0, 0.15);
}
</style>

<template>
  <div class="page">
    <div class="flash" v-if="flashMessage">{{ flashMessage }}</div>
    <div id="container">
        <h2 id="loginhead">Login</h2>

        <!-- Role Toggle -->
        <div class="toggle">
            <button type="button" :class="{ active: role === 'Student' }" @click="role = 'Student'">Student</button>
            <button type="button" :class="{ active: role === 'Company' }" @click="role = 'Company'">Company</button>
            <button type="button" :class="{ active: role === 'Admin' }" @click="role = 'Admin'">Admin</button>
        </div>

        <div id="formcontainer">
          <form @submit.prevent='handleLogin'>

              <!-- Student Fields -->
              <template v-if="role === 'Student'">
                  <input type="text" v-model="rollNo" placeholder="Roll Number" required>
              </template>

              <!-- Company Fields -->
              <template v-if="role === 'Company'">
                  <input type="text" v-model="gstNumber" placeholder="GST Number" required>
              </template>

              <!-- Admin Fields -->
              <template v-if="role === 'Admin'">
                  <input type="email" v-model="email" placeholder="Email" required>
              </template>

              <!-- Common Fields -->
              <input type="password" v-model="password" placeholder="Password" required>

              <div id="buttondiv">
                 <button type="submit" class="submit-btn">LOGIN</button>
              </div>

              <p>Don't Have an account? <router-link to="/register">Register</router-link></p>
          </form>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import router from '/src/router/index.js'
import api from '/src/services/api.js'

const role = ref('Student')
const password = ref("")
const flashMessage = ref("")

const rollNo = ref("")
const gstNumber = ref("")
const email = ref("")

const showFlash = (msg) => {
  flashMessage.value = msg;
  setTimeout(() => { flashMessage.value = ""; }, 2000);
};

const handleLogin = async () => {
  const payload = {
    password: password.value,
    ...(role.value == 'Student' && { role: role.value, roll_no: rollNo.value }),
    ...(role.value == 'Company' && { role: role.value, gst_number: gstNumber.value }),
    ...(role.value == 'Admin' && { role: role.value, email: email.value })
  };

  try {
    const res = await api.post("/api/auth/login", payload);
    localStorage.setItem('token', res.data.token);
    if (res.data.role == 'Student') {
      router.push(`/student/${res.data.id}`);
      localStorage.setItem('student_id',res.data.id);
    } else if (res.data.role == 'Company') {
      router.push(`/company/${res.data.id}`);
    } else {
      router.push('/admin');
    }
  } catch (error) {
    showFlash(error.response?.data?.message || "Login failed!");
  }
};
</script>

<style scoped>
* {
  margin: 0px;
  padding: 0px;
  font-family: "Inter", sans-serif;
  box-sizing: border-box;
}

.page {
  background-color: #E9F3FF;
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
}

.flash {
  position: fixed;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #ffdddd;
  color: #a60000;
  border: 1px solid #ff8a8a;
  padding: 12px 20px;
  border-radius: 6px;
  font-weight: bold;
  z-index: 9999;
}

#container {
  width: 300px;
  background-color: white;
  border-radius: 10px;
  transition: transform 0.3s ease-in-out;
  padding-bottom: 20px;
  margin-bottom: 100px;
}

#container:hover {
  transform: scale(1.01);
}

#loginhead {
  text-align: center;
  margin-bottom: 40px;
  margin-top: 30px;
  font-weight: 700;
  font-size: 2rem;
  color: #252eff;
}

/* Role Toggle */
.toggle {
  display: flex;
  justify-content: center;
  gap: 6px;
  margin-bottom: 10px;
}

.toggle button {
  width: 80px;
  height: 32px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  border: 2px solid blue;
  background-color: white;
  color: blue;
  transition: all 0.3s ease;
}

.toggle button.active {
  background-color: blue;
  color: white;
}

.toggle button:hover {
  background-color: blue;
  color: white;
}

#formcontainer {
  display: flex;
  justify-content: center;
}

input {
  display: block;
  width: 250px;
  background: #f8fafc;
  border: 1.5px solid #dce3eb;
  padding-left: 5px;
  height: 30px;
  border-radius: 20px;
  margin: 15px;
  outline: none;
  font-size: 0.95rem;
}

input::placeholder {
  font-size: 13px;
  font-weight: 600;
}

#buttondiv {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  margin-bottom: 15px;
}

.submit-btn {
  width: 130px;
  height: 30px;
  color: white;
  font-weight: 500;
  border-radius: 20px;
  background-color: blue;
  font-size: 13px;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s ease-in-out;
}

.submit-btn:hover {
  background-color: rgb(5, 5, 163);
}

p {
  font-weight: 500;
  font-size: 15px;
  text-align: center;
  padding-bottom: 10px;
}
</style>
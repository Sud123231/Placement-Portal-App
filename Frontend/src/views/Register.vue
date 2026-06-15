<template>
  <div class="page">
    <div v-if="flashMessage" class="flash">{{ flashMessage }}</div>
    <div id="container">
      <h2 id="Registerhead">Register</h2>

      <!-- Role Toggle -->
      <div class="toggle">
        <button type="button" :class="{ active: role === 'Student' }" @click="role = 'Student'">Student</button>
        <button type="button" :class="{ active: role === 'Company' }" @click="role = 'Company'">Company</button>
      </div>

      <form @submit.prevent="handleRegister">
        <!-- Common Fields -->
        <input type="text" v-model="name" placeholder="Full Name" required>
        <input type="text" v-model="email" placeholder="Email" required>
        <input type="password" v-model="password" placeholder="Password" required>
        <input type="password" v-model="confirmPassword" placeholder="Confirm Password" required>

        <!-- Student Fields -->
        <template v-if="role === 'Student'">
          <input type="text" v-model="rollNo" placeholder="Roll Number" required>
          <input type="text" v-model="department" placeholder="Department" required>
          <input type="number" v-model="cgpa" placeholder="CGPA" required>
        </template>

        <!-- Company Fields -->
        <template v-if="role === 'Company'">
          <input type="text" v-model="gstNumber" placeholder="GST Number" required>
          <input type="text" v-model="hrContact" placeholder="HR Contact" required>
          <textarea v-model="description" placeholder="Company Overview"></textarea>
        </template>

        <button type="submit" class="submit-btn">Register</button>
        <p>Have account? <router-link to="/login">Login</router-link></p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '/src/services/api.js'
import router from '/src/router/index.js'

const role = ref('Student')
const name = ref("")
const password = ref("")
const confirmPassword = ref("")

// Student fields
const rollNo = ref("")
const department = ref("")
const cgpa = ref(null)
const email = ref("")

// Company fields
const gstNumber = ref("")
const hrContact = ref("")
const description = ref("")

const flashMessage = ref("")

const showFlash = (msg) => {
  flashMessage.value = msg;
  setTimeout(() => { flashMessage.value = "" }, 2000);
}

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    showFlash("Passwords do not match!")
    return
  }   
  const payload = {
    role: role.value,
    name: name.value,
    password: password.value,
    email: email.value,
    ...(role.value === 'Student' && { roll_no: rollNo.value, department: department.value, cgpa: cgpa.value }),
    ...(role.value === 'Company' && { gst_number: gstNumber.value, description: description.value, hr_contact: hrContact.value})
  }

  try {
    await api.post("/api/auth/register", payload)
    router.push('/login')
  } catch (error) {
    showFlash(error.response?.data?.message || "Registration failed!")
  }
}
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
  min-height: 100vh;
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
  width: 400px;
  margin-top:40px;
  background-color: white;
  border-radius: 10px;
  padding-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.3s ease-in-out;
}

#container:hover {
  transform: scale(1.01);
}

#Registerhead {
  text-align: center;
  margin-bottom: 15px;
  margin-top: 10px;
  font-weight: 700;
  font-size: 2rem;
  color: black;
}

/* Role Toggle */
.toggle {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.toggle button {
  width: 120px;
  height: 32px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  border: 2px solid #3088f2;
  background-color: white;
  color: #3088f2;
  transition: all 0.3s ease;
}

.toggle button.active {
  background-color: #3088f2;
  color: white;
}

.toggle button:hover {
  background-color: #3088f2;
  color: white;
}

/* Form */
form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

input,
textarea {
  display: block;
  width: 250px;
  background: #f8fafc;
  border: 1.5px solid #dce3eb;
  padding: 5px 10px;
  border-radius: 20px;
  margin: 10px 0;
  outline: none;
  font-size: 0.95rem;
  font-family: "Inter", sans-serif;
}

input {
  height: 30px;
}

textarea {
  height: 80px;
  border-radius: 10px;
  resize: vertical;
  padding: 8px 10px;
}

input::placeholder,
textarea::placeholder {
  font-size: 13px;
  font-weight: 600;
}

/* Submit Button */
.submit-btn {
  display: block;
  margin-top: 20px;
  margin-bottom: 15px;
  width: 250px;
  height: 30px;
  color: white;
  font-weight: 500;
  border-radius: 20px;
  background-color: #3088f2;
  font-size: 13px;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s ease-in-out;
}

.submit-btn:hover {
  background-color: #1f75e2;
}

p {
  font-weight: 500;
  font-size: 15px;
  text-align: center;
}
</style>
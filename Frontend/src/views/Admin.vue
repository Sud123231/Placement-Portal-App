<template>
  <div class="page">
    <div class="card">
        <div class="top-row">
          <h1>Welcome Admin</h1>
          <form @submit.prevent='handleSearch(search)' class="search-form"> 
            <input v-model="search" placeholder="student, organizations..." />
            <button class="search-btn" type="submit">search</button>
          </form>
        </div>
            <!-- all buttons also have to be fixed -->
        <hr class="divider"/>
        <!-- Registered Companies -->
        <h2>Registered Companies</h2>
        <div class="list">
          <div v-if="companies.length > 0">
            <div v-for="(company,idx) in companies" class="list-item" :key="company.id">
              <div class="item-left">
                <i class="bi bi-building icon"></i>
                <span class="name">{{ company.name }}</span>
              </div>
              <div class="item-actions">
                <form @submit.prevent='companyBlacklist(idx,company.id)'> <!--need to be fixed -->
                  <button class="btn small red">blacklist</button>
                </form>
              </div> 
            </div>  
          </div>
          <p class="muted" v-else>No companies registered.</p>
        </div>

        <!-- Registered Students -->
        <h2>Registered Students</h2>
        <div class="list">
          <div v-if="students.length > 0">
            <div v-for="(student,idx) in students" class="list-item" :key="student.id">
              <div class="item-left">
                <i class="bi bi-person icon"></i>
                <span class="name">{{ student.name }}</span>
              </div>
              <div class="item-actions">
                <form @submit.prevent='studentBlacklist(idx,student.id)'> <!--need to be fixed -->
                  <button class="btn small red">blacklist</button>
                </form>
              </div> 
            </div>  
          </div>
          <p class="muted" v-else>No students registered.</p>
        </div>

        <!-- Company Applications -->
        <h2>Company Applications</h2>
        <div class="list">
          <div v-if="companyApplications.length > 0">
            <div v-for="(application,idx) in companyApplications" class="list-item" :key="application.id">
              <div class="item-left">
                <i class="bi bi-building icon"></i>
                <span class="name">{{ application.name }}</span>
              </div>
              <div class="item-actions">
                  <button class="btn small green" @click='approveCompany(idx,application.id)'>Approve</button>
                  <button class="btn small red" @click='rejectCompany(idx,application.id)'>Reject</button>
              </div> 
            </div>  
          </div>
          <p class="muted" v-else>No Company applications registered.</p>
        </div>
           
        <!-- Ongoing Drives -->
        <h2>Ongoing Drives</h2>
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
              <tr v-if="drives.length === 0">
                <td colspan="3" class="muted">No drives registered</td>
              </tr>
              <tr v-for="(drive, idx) in drives" :key="drive.id" v-else>
                <td>{{ idx + 1 }}</td>
                <td>{{ drive.name }}</td>
                <td>
                    <button class="blue btn" @click="viewDrive(idx, drive.id)">view details</button>
                    <button class="green btn" @click="markComplete(idx, drive.id)">marks as complete</button>
                    <button class="btn small red" @click="rejectDrive(idx,drive.id)">Reject</button>
                </td>
              </tr>
            </tbody>
          </table>  
        </div>
      <!-- Student Applications -->
      <h2>Student Applications</h2>
      <div class="table-wrap">
        <table>
          <thead>
              <tr>
                <th>Sr No.</th>
                <th>Name</th>
                <th>Drive</th>
                <th>Company</th>
                <th>Date</th>
                <th>Action</th>
              </tr>
          </thead>
          <tbody class="list" v-if="studentApplications.length>0">
              <tr v-for="(s,idx) in studentApplications" :key="s.id">
                <td>{{idx + 1}}</td>
                <td>{{s.student_name}}</td>
                <td>{{s.drive}}</td>
                <td>{{s.company}}</td>
                <td>{{s.date}}</td>
                <td>
                  <button type="submit" v-on:click="viewStudentApplication(idx, s.id)" class="blue btn">view</button>
                </td>
              </tr>
          </tbody>
          <tr v-else><td colspan="6" class="muted">No applications registered</td></tr>
        </table>
      </div>  
    </div>         <!-- enclosing div for card -->
  </div>             <!-- enclosing div for page -->
</template>  

<script setup>
  import {ref,onMounted} from 'vue';
  import api from '/src/services/api.js'
  import router from '/src/router/index.js'

  const search=ref("");
  let companies=ref([]);
  let students=ref([]);
  let companyApplications=ref([]);
  let drives=ref([]);
  let studentApplications=ref([]);

  const companiesBackup=ref([]);
  const studentsBackup=ref([]);
  const companyApplicationsBackup=ref([]);
  const drivesBackup=ref([]);
  const studentApplicationsBackup=ref([]);

  /* -----------------------Fetchers------------------------- */
    const fetchCompanies = async () => {
      const res = await api.get("/api/companies");
      companies.value = res.data.companies;
      companiesBackup.value=res.data.companies;
    };

    const fetchStudents = async()=> {
      const res=await api.get("/api/students");
      students.value=res.data.students;
      studentsBackup.value=res.data.students;
    };

    const fetchCompanyApplications= async()=> {
      const res=await api.get("/api/companies/applications");
      companyApplications.value=res.data.companyapplications;
      companyApplicationsBackup.value=res.data.companyapplications;
    };  

    const fetchOngoingDrives=async()=>{
      const res=await api.get("/api/drives");  
      drives.value=res.data.drives.filter((obj)=>{
        return obj.status==='Ongoing';
      });
      drivesBackup.value=[...drives.value]
    };  
    
    const fetchStudentApplications=async()=>{
      const res=await api.get("/api/students/applications");
      studentApplications.value=res.data.applications;
      studentApplicationsBackup.value=res.data.applications;
    };  
      
    //searching
    const handleSearch = (query) => {
      if (!query) {
        companies.value = [...companiesBackup.value];
        students.value = [...studentsBackup.value];
        companyApplications.value = [...companyApplicationsBackup.value];
        drives.value = [...drivesBackup.value];
        studentApplications.value = [...studentApplicationsBackup.value];
      } else {
        let res = companiesBackup.value.filter((obj) => {
          return obj.name.toLowerCase().includes(query.toLowerCase());
        });
        companies.value = [...res];

        res = studentsBackup.value.filter((obj) => {
          return obj.name.toLowerCase().includes(query.toLowerCase());
        });
        students.value = [...res];

        res = companyApplicationsBackup.value.filter((obj) => {
          return obj.name.toLowerCase().includes(query.toLowerCase());
        });
        companyApplications.value = [...res];

        res = drivesBackup.value.filter((obj) => {
          return obj.name.toLowerCase().includes(query.toLowerCase());
        });
        drives.value = [...res];

        res = studentApplicationsBackup.value.filter((obj) => {
          return obj.student_name.toLowerCase().includes(query.toLowerCase());
        });
        studentApplications.value = [...res];
      }
    };
    

    //blacklisting the company
    const companyBlacklist=async (idx, id)=>{

      const payload={
        status:"Blacklisted"
      };
      const res=await api.patch(`/api/companies/${id}`,payload);
      companies.value.splice(idx,1);
      drives.value=[];   
    };

    //blacklisting the student
    const studentBlacklist=async (idx,id)=>{
      const payload={
        status:"Blacklisted"
      };
      const res=await api.patch(`/api/students/${id}`,payload);
      students.value.splice(idx,1); 
    }; 

    //approving company
    const approveCompany=async (idx,id)=>{

      const payload={
        status:"Approved"
      };
      const res=await api.patch(`/api/companies/${id}`,payload);
      companies.value.push(res.data.company);
      companyApplications.value.splice(idx,1);   
    };

    //Rejecting company
    const rejectCompany=async (idx,id)=>{

      const payload={
        status:"Rejected"
      };
      const res=await api.patch(`/api/companies/${id}`,payload);
      companyApplications.value.splice(idx,1);   
    };

    //marking as completed to drive
    const markComplete=async (idx,id)=>{
      const payload={
        status:"Completed"
      };
      const res=await api.patch(`/api/drives/${id}`,payload);
      drives.value.splice(idx,1);
    };

    //Rejecting drive
    const rejectDrive=async (idx,id)=>{
      const payload={
        status:"Cancelled"
      };
      const res=await api.patch(`/api/drives/${id}`,payload);
      drives.value.splice(idx,1);
    };  

    //view the student application detail
    const viewStudentApplication = (idx, id) => {
      router.push(`/applications/${id}`)
    }

    //view the drive detail
    const viewDrive=(idx,id)=>{
      router.push(`/drives/${id}`);
    };
        

    onMounted(()=>{
     fetchCompanies();
     fetchStudents();
     fetchCompanyApplications();
     fetchOngoingDrives();
     fetchStudentApplications(); 
     });
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: sans-serif;
}

#body {
  background: #f4f8ff;
  color: #333;
}

/* Page Layout */
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

/* Search Bar */
.search-form {
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-form input {
  padding: 8px 14px;
  border-radius: 8px;
  border: 1px solid #c5d4ff;
  outline: none;
  width: 250px;
  transition: 0.3s;
}

.search-form input:focus {
  border-color: #4a7dff;
  box-shadow: 0 0 0 3px rgba(74, 125, 255, 0.15);
}

.search-btn {
  background: #4a7dff;
  color: #fff;
  padding: 8px 14px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.3s;
}

.search-btn:hover {
  background: #3565e8;
}

/* Section Titles */
h2 {
  margin-top: 25px;
  font-size: 20px;
  color: #002b80;
  border-left: 4px solid #4a7dff;
  padding-left: 8px;
}

/*  Lists  */
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
  gap: 10px;
}

.icon {
  color: #4a7dff;
  font-size: 18px;
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
/* General Button Styling */
.btn {
  background-color: white;
  border-radius: 5px;
  padding: 6px 12px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  font-weight: 500;
  text-decoration:none;
  margin-left:10px;
}

.btn.small {
  padding: 5px 10px;
  font-size: 0.9rem;
}

/* Button Variants  */

/* Edit Button (Yellow) */
.btn.yellow {
  border: 1px solid #f59e0b;
  color: #f59e0b;
}
.btn.yellow:hover {
  background-color: #f59e0b;
  color: white;
}

/* Delete Button (Red) */
.btn.red {
  border: 1px solid #ef4444;
  color: #ef4444;
}
.btn.red:hover {
  background-color: #ef4444;
  color: white;
}

/* Blacklist Button (Gray) */
.btn.gray {
  border: 1px solid #6b7280;
  color: #6b7280;
}
.btn.gray:hover {
  background-color: #6b7280;
  color: white;
}

/* View Button (Blue) */
.btn.blue {
  border: 1px solid #3088f2;
  color: #3088f2;
}
.btn.blue:hover {
  background-color: #3088f2;
  color: white;
}

/* Smooth hover transition for all */
.btn:hover {
  transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out;
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


/*  Misc  */
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
.green{
  background-color: white;
  border-radius: 5px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #22c55e;
  color: #22c55e;
  padding: 8px 15px;
}
.green:hover{
  background-color: #22c55e;
  color:white;
}
.dept{
  margin-top:10px;
}
</style>

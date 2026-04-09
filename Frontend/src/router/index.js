import { createRouter, createWebHistory } from "vue-router";
import register from "/src/views/Register.vue";
import login from "/src/views/Login.vue";
import admin from "/src/views/Admin.vue";
import drivedetail from "/src/views/Drivedetail.vue";
import company from "/src/views/Company.vue";
import createdrive from "/src/views/Createdrive.vue";
import driveapplications from "/src/views/Driveapplications.vue";
import editdrive from "/src/views/Editdrive.vue";
import student from "/src/views/Student.vue";
import viewcompany from "/src/views/Viewcompany.vue";
import driveapply from "/src/views/Driveapply.vue";
import editstudentprofile from "/src/views/Editstudentprofile.vue";

const routes = [
    {
        path: "/",
        component: register
    },
    {
        path: "/login",
        component: login
    },
    {
        path: "/admin",
        component: admin
    },
    {
        path: "/drives/:id",
        component: drivedetail
    },
    {
        path: "/company/:id",
        component: company
    },
    {
        path: "/student/:id",
        component: student
    },
    {
        path: "/company/:id/drives/create",
        component: createdrive
    },
    {
        path: "/drives/:id/applications",
        component: driveapplications
    },
    {
        path: "/companies/:id",
        component: viewcompany
    },
    {
        path: "/drives/:id/apply",
        component: driveapply
    },
    {
        path: "/student/:id/edit",
        component: editstudentprofile
    },
    {
        path: "/drives/:id/edit",
        component: editdrive
    },
    {
        path: "/:pathMatch(.*)*",
        component: register
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;

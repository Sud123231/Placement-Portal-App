import { createRouter, createWebHistory } from "vue-router";
import register from "/src/views/Register.vue";
import login from "/src/views/Login.vue";
import admin from "/src/views/Admin.vue";
import drivedetail from "/src/views/Drivedetail.vue";
import company from "/src/views/Company.vue";
import createdrive from "/src/views/Createdrive.vue";
import driveapplications from "/src/views/Driveapplications.vue";
import editdrive from "/src/views/Editdrive.vue";

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
        path: "/company/:id/drives/create",
        component: createdrive
    },
    {
        path: "/drives/:id/applications",
        component: driveapplications
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

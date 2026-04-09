import { createRouter, createWebHistory } from "vue-router";
import register from "/src/views/Register.vue";
import login from "/src/views/Login.vue";

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
        path: "/:pathMatch(.*)*",
        component: register
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;

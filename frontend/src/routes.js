import { createRouter, createWebHistory } from 'vue-router';
import payments_page from '../src/components/payments_page.vue' // Import the component

const routes = [
    { path: '/payment', component: payments_page } // Ensure 'Payments' is imported
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;

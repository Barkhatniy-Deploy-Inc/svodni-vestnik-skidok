import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../views/Dashboard.vue';
import AddItem from '../views/AddItem.vue';

const routes = [
  { path: '/', component: Dashboard },
  { path: '/add', component: AddItem }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

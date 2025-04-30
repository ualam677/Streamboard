import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/components/Login.vue'
import Signup from '@/components/Signup.vue'
import Dashboard from '@/components/Dashboard.vue'
import ManageBoards from '@/components/ManageBoards.vue'
import Settings from '@/components/Settings.vue'
import StreamboardCreate from '@/components/StreamboardCreate.vue'
import StreamboardOverlay from '@/components/StreamboardOverlay.vue'
import StreamboardController from '@/views/StreamboardController.vue'


const routes = [
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login },
    { path: '/signup', component: Signup },
    { path: '/dashboard', component: Dashboard },
    { path: '/manage-boards', name: 'ManageBoards', component: ManageBoards },
    { path: '/settings', name: 'Settings', component: Settings },
    { path: '/boards/new', component: StreamboardCreate },
    { path: '/boards/:id/controller', component: StreamboardController },
    { path: '/overlay/:id', component: StreamboardOverlay },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router

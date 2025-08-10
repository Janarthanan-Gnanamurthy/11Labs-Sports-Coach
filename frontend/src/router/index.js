import { createRouter, createWebHistory } from 'vue-router'
import WelcomePage from '../components/WelcomePage.vue'
import SportSelection from '../components/SportSelection.vue'
import AgentSelection from '../components/AgentSelection.vue'
import SessionSetup from '../components/SessionSetup.vue'
import LiveCoaching from '../components/LiveCoaching.vue'
import Dashboard from '../components/Dashboard.vue'
import Settings from '../components/Settings.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Welcome',
      component: WelcomePage
    },
    {
      path: '/sport-selection',
      name: 'SportSelection',
      component: SportSelection
    },
    {
      path: '/agent-selection',
      name: 'AgentSelection',
      component: AgentSelection
    },
    {
      path: '/session-setup',
      name: 'SessionSetup',
      component: SessionSetup
    },
    {
      path: '/live-coaching',
      name: 'LiveCoaching',
      component: LiveCoaching
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: '/settings',
      name: 'Settings',
      component: Settings
    }
  ]
})

export default router

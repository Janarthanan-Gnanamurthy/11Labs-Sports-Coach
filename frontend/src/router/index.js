import { createRouter, createWebHistory } from 'vue-router'
import WelcomePage from '../components/WelcomePage.vue'
import LoginPage from '../components/LoginPage.vue'
import WorkoutPlanGeneration from '../components/WorkoutPlanGeneration.vue'
import SportSelection from '../components/SportSelection.vue'
import AgentSelection from '../components/AgentSelection.vue'
import SessionSetup from '../components/SessionSetup.vue'
import LiveCoaching from '../components/LiveCoaching.vue'
import Dashboard from '../components/Dashboard.vue'
import Settings from '../components/Settings.vue'
import WorkoutOverview from '../components/WorkoutOverview.vue'
import WorkoutSession from '../components/WorkoutSession.vue'
import WorkoutCelebration from '../components/WorkoutCelebration.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Welcome',
      component: WelcomePage
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginPage
    },
    {
      path: '/workout-plan-generation',
      name: 'WorkoutPlanGeneration',
      component: WorkoutPlanGeneration
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
    },
    {
      path: '/workout-overview/:planId/:dayNumber',
      name: 'WorkoutOverview',
      component: WorkoutOverview
    },
    {
      path: '/workout-session/:planId/:dayNumber',
      name: 'WorkoutSession',
      component: WorkoutSession
    },
    {
      path: '/workout-celebration/:planId/:dayNumber',
      name: 'WorkoutCelebration',
      component: WorkoutCelebration
    }
  ]
})

export default router

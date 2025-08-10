import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  // User profile data
  const userProfile = ref({
    id: 'user_001',
    name: 'John Doe',
    email: 'john@example.com',
    preferences: {
      sport: 'running',
      fitnessLevel: 'intermediate',
      goals: ['endurance', 'weight-loss'],
      notifications: true
    }
  })

  // Session data
  const selectedSport = ref('running')
  const selectedAgent = ref({
    id: 'coach',
    name: 'The Coach',
    emoji: '💪',
    description: 'Structured, motivating, results-focused'
  })
  const sessionData = ref({
    duration: 30,
    intensity: 'medium',
    mood: 'energetic'
  })
  
  // Sample session history
  const sessionHistory = ref([
    {
      id: 'session_001',
      sport: 'running',
      duration: 1800, // 30 minutes
      completedPercentage: 95,
      agent: 'The Coach',
      date: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString() // Yesterday
    },
    {
      id: 'session_002',
      sport: 'gym',
      duration: 2700, // 45 minutes
      completedPercentage: 88,
      agent: 'The Motivator',
      date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString() // 3 days ago
    }
  ])

  // Navigation state
  const currentRoute = ref('/')

  // Computed properties
  const lastSession = computed(() => {
    return sessionHistory.value.length > 0 
      ? sessionHistory.value[sessionHistory.value.length - 1] 
      : null
  })

  const recentSessions = computed(() => {
    return sessionHistory.value.slice(-5).reverse()
  })

  const totalSessions = computed(() => {
    return sessionHistory.value.length
  })

  const totalMinutes = computed(() => {
    return Math.round(sessionHistory.value.reduce((total, session) => 
      total + (session.duration / 60), 0))
  })

  const weeklyStats = computed(() => {
    const now = new Date()
    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
    
    const weekSessions = sessionHistory.value.filter(session => 
      new Date(session.date) >= weekAgo
    )
    
    return {
      sessions: weekSessions.length,
      totalMinutes: Math.round(weekSessions.reduce((total, session) => 
        total + (session.duration / 60), 0))
    }
  })

  // Actions
  function setUserProfile(profile) {
    userProfile.value = { ...userProfile.value, ...profile }
  }

  function setSelectedSport(sport) {
    selectedSport.value = sport
  }

  function setSelectedAgent(agent) {
    selectedAgent.value = agent
  }

  function setSessionData(data) {
    sessionData.value = { ...sessionData.value, ...data }
  }

  function addSessionToHistory(session) {
    const sessionWithId = {
      ...session,
      id: `session_${Date.now()}`,
      date: new Date().toISOString()
    }
    sessionHistory.value.push(sessionWithId)
  }

  function updateSessionData(data) {
    sessionData.value = { ...sessionData.value, ...data }
  }

  function clearSessionData() {
    sessionData.value = {}
    selectedSport.value = null
    selectedAgent.value = null
  }

  function setCurrentRoute(route) {
    currentRoute.value = route
  }

  function resetUserData() {
    userProfile.value = {
      id: null,
      name: '',
      email: '',
      preferences: {
        sport: null,
        fitnessLevel: 'beginner',
        goals: [],
        notifications: true
      }
    }
    clearSessionData()
    sessionHistory.value = []
  }

  // Utility functions
  function formatDuration(seconds) {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return mins > 0 ? `${mins}m ${secs}s` : `${secs}s`
  }

  function formatDate(dateString) {
    const date = new Date(dateString)
    const now = new Date()
    const diffTime = Math.abs(now - date)
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays === 1) return 'Today'
    if (diffDays === 2) return 'Yesterday'
    if (diffDays <= 7) return `${diffDays - 1} days ago`
    return date.toLocaleDateString()
  }

  return {
    // State
    userProfile,
    selectedSport,
    selectedAgent,
    sessionData,
    sessionHistory,
    currentRoute,
    
    // Computed
    lastSession,
    recentSessions,
    totalSessions,
    totalMinutes,
    weeklyStats,
    
    // Actions
    setUserProfile,
    setSelectedSport,
    setSelectedAgent,
    setSessionData,
    addSessionToHistory,
    updateSessionData,
    clearSessionData,
    setCurrentRoute,
    resetUserData,
    
    // Utilities
    formatDuration,
    formatDate
  }
})

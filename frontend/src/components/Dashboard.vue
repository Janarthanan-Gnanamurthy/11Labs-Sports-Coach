<template>
  <div class="min-h-screen bg-gray-50">
    <!-- iPhone-style Status Bar -->
    <div class="bg-black text-white px-6 py-2 flex justify-between items-center text-sm">
      <span>9:41</span>
      <div class="flex items-center space-x-1">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
        <svg class="w-6 h-3" fill="currentColor" viewBox="0 0 24 12">
          <rect x="2" y="2" width="18" height="8" rx="1" fill="currentColor"/>
          <rect x="4" y="4" width="2" height="4" fill="black"/>
          <rect x="7" y="4" width="2" height="4" fill="black"/>
          <rect x="10" y="4" width="2" height="4" fill="black"/>
        </svg>
      </div>
    </div>

    <!-- Header -->
    <div class="bg-white px-6 py-4 border-b border-gray-100">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p class="text-gray-600 text-sm">Welcome back, {{ userProfile.name }}</p>
        </div>
        <button 
          @click="startNewSession"
          class="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center shadow-lg"
        >
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
        </button>
      </div>
    </div>
  
    <!-- Main Content -->
    <div class="px-4 py-6 space-y-4">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>

      <!-- Progress Overview Card -->
      <div v-else class="bg-white rounded-3xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold text-gray-900">This Week</h2>
          <span class="text-sm text-gray-500">{{ getCurrentWeekRange() }}</span>
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div class="bg-blue-50 rounded-2xl p-4">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-2xl font-bold text-blue-600">{{ progressData.total_sessions || 0 }}</p>
                <p class="text-blue-700 text-sm font-medium">Sessions</p>
              </div>
              <div class="w-10 h-10 bg-blue-200 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </div>
            </div>
          </div>
          
          <div class="bg-green-50 rounded-2xl p-4">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-2xl font-bold text-green-600">{{ Math.round(progressData.average_rpe || 0) }}</p>
                <p class="text-green-700 text-sm font-medium">Avg RPE</p>
              </div>
              <div class="w-10 h-10 bg-green-200 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
              </div>
            </div>
          </div>
        </div>
        
        <div class="mt-4 bg-gray-50 rounded-2xl p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-lg font-bold text-gray-900">{{ Math.round((progressData.success_rate || 0) * 100) }}%</p>
              <p class="text-gray-600 text-sm">Success Rate</p>
            </div>
            <div class="w-12 h-12 bg-purple-200 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-purple-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Current Plan Card -->
      <div v-if="currentPlan" class="bg-white rounded-3xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold text-gray-900">Current Plan</h2>
          <span class="text-sm text-blue-600 font-medium">{{ currentPlan.plan.total_days }} days</span>
        </div>
        
        <div class="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl p-4 text-white">
          <h3 class="text-lg font-bold mb-2">{{ currentPlan.plan.title }}</h3>
          <p class="text-blue-100 text-sm mb-3">{{ currentPlan.plan.description }}</p>
          <div class="flex items-center justify-between mb-4">
            <span class="text-sm">Progress</span>
            <span class="text-lg font-bold">{{ Math.round((completedDays / currentPlan.plan.total_days) * 100) }}%</span>
          </div>
          <div class="w-full bg-blue-400 rounded-full h-2 mb-4">
            <div 
              class="bg-white h-2 rounded-full transition-all duration-300"
              :style="{ width: `${(completedDays / currentPlan.plan.total_days) * 100}%` }"
            ></div>
          </div>
          
          <!-- Start Workout Button -->
          <button 
            @click="startWorkout"
            class="w-full bg-white text-blue-600 py-3 rounded-xl font-bold text-lg shadow-lg hover:bg-gray-50 transition-colors"
          >
            Start Today's Workout
          </button>
        </div>
      </div>

      <!-- AI Assistant Card -->
      <div class="bg-white rounded-3xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold text-gray-900">AI Fitness Assistant</h2>
          <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/>
            </svg>
          </div>
        </div>
        <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-4">
          <p class="text-gray-700 text-sm mb-4">Ask your AI assistant about workouts, nutrition, form tips, and progress tracking. Click the voice button to start talking!</p>
          
          <!-- ElevenLabs ConvAI Widget Container -->
          <div class="flex justify-center">
            <elevenlabs-convai agent-id="agent_4501k29zamd4faztws0yk8rhwp1y"></elevenlabs-convai>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="bg-white rounded-3xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold text-gray-900">Recent Activity</h2>
          <button @click="viewAllActivity" class="text-blue-600 text-sm font-medium">View All</button>
        </div>
        
        <div v-if="recentReports.length === 0" class="text-center py-8">
          <div class="w-16 h-16 mx-auto bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <svg class="w-8 h-8 text-gray-400" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
          </div>
          <p class="text-gray-500 font-medium">No workouts yet</p>
          <p class="text-gray-400 text-sm">Complete your first workout to see progress here</p>
        </div>
        
        <div v-else class="space-y-3">
          <div 
            v-for="report in recentReports" 
            :key="report.id"
            class="flex items-center justify-between p-4 bg-gray-50 rounded-2xl"
          >
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M13.49 5.48c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM9.89 19.38l1-4.4 2.1 2v6h2v-7.5l-2.1-2 .6-3c1.3 1.5 3.3 2.5 5.5 2.5v-2c-1.9 0-3.5-1-4.3-2.4l-1-1.6c-.4-.6-1-1-1.7-1-.3 0-.5.1-.8.1L9 5.5v4.5h2V7.4l1.8 7.4L8 19l1.9.4z"/>
                </svg>
              </div>
              <div>
                <p class="font-semibold text-gray-900">Workout Session</p>
                <p class="text-gray-500 text-sm">{{ formatDate(report.date) }}</p>
              </div>
            </div>
            <div class="text-right">
              <p class="font-semibold text-gray-900">RPE {{ report.rpe }}</p>
              <p class="text-gray-500 text-sm">{{ report.sets_completed }} sets</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="bg-white rounded-3xl shadow-sm p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
        <div class="grid grid-cols-2 gap-3">
          <button 
            @click="startNewSession"
            class="bg-blue-500 text-white p-4 rounded-2xl text-center font-medium"
          >
            <svg class="w-6 h-6 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            New Workout
          </button>
          <button 
            @click="viewSettings"
            class="bg-gray-100 text-gray-700 p-4 rounded-2xl text-center font-medium"
          >
            <svg class="w-6 h-6 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            Settings
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '../stores/user.js'
import { useRouter } from 'vue-router'
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'Dashboard',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    
    // Reactive data
    const loading = ref(true)
    const progressData = ref({})
    const currentPlan = ref(null)
    const recentReports = ref([])
    const completedDays = ref(0)
    
    // Computed properties
    const userProfile = computed(() => userStore.userProfile)
    
    // Check if user is logged in
    const checkAuth = () => {
      const isLoggedIn = userStore.loadUserFromStorage()
      if (!isLoggedIn) {
        router.push('/login')
        return false
      }
      return true
    }
    
    // Load ElevenLabs ConvAI script
    const loadConvAIScript = () => {
      // Check if script is already loaded
      if (document.querySelector('script[src*="convai-widget-embed"]')) {
        return
      }
      
      const script = document.createElement('script')
      script.src = 'https://unpkg.com/@elevenlabs/convai-widget-embed'
      script.async = true
      script.type = 'text/javascript'
      document.head.appendChild(script)
    }
    
    // Fetch user progress data from backend
    const fetchProgressData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/users/${userProfile.value.id}/progress?days=30`)
        if (response.ok) {
          progressData.value = await response.json()
        }
      } catch (error) {
        console.error('Error fetching progress data:', error)
      }
    }
    
    // Fetch user's current plan
    const fetchCurrentPlan = async () => {
      try {
        const response = await fetch(`http://localhost:8000/users/${userProfile.value.id}/plans`)
        if (response.ok) {
          const plans = await response.json()
          if (plans.length > 0) {
            // Get the most recent active plan
            const activePlan = plans.find(plan => plan.is_active) || plans[0]
            const planDetailsResponse = await fetch(`http://localhost:8000/plans/${activePlan.id}`)
            if (planDetailsResponse.ok) {
              currentPlan.value = await planDetailsResponse.json()
              // Calculate completed days (simplified - you might want to track this in the backend)
              completedDays.value = Math.min(Math.floor(progressData.value.total_sessions / 2), currentPlan.value.plan.total_days)
            }
          }
        }
      } catch (error) {
        console.error('Error fetching current plan:', error)
      }
    }
    
    // Fetch recent session reports
    const fetchRecentReports = async () => {
      try {
        const response = await fetch(`http://localhost:8000/users/${userProfile.value.id}/progress?days=7`)
        if (response.ok) {
          const data = await response.json()
          recentReports.value = data.recent_reports || []
        }
      } catch (error) {
        console.error('Error fetching recent reports:', error)
      }
    }
    
    // Load all data
    const loadDashboardData = async () => {
      loading.value = true
      try {
        await Promise.all([
          fetchProgressData(),
          fetchCurrentPlan(),
          fetchRecentReports()
        ])
      } catch (error) {
        console.error('Error loading dashboard data:', error)
      } finally {
        loading.value = false
      }
    }
    
    // Utility functions
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      const diffTime = Math.abs(now - date)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays === 1) return 'Yesterday'
      if (diffDays === 0) return 'Today'
      if (diffDays < 7) return `${diffDays} days ago`
      
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric' 
      })
    }
    
    const getCurrentWeekRange = () => {
      const now = new Date()
      const startOfWeek = new Date(now.setDate(now.getDate() - now.getDay()))
      const endOfWeek = new Date(now.setDate(now.getDate() - now.getDay() + 6))
      
      return `${startOfWeek.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} - ${endOfWeek.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`
    }
    
    // Navigation methods
    const startNewSession = () => {
      router.push('/sport-selection')
    }
    
    const startWorkout = () => {
      if (currentPlan.value) {
        // Start with day 1 or the next incomplete day
        const nextDay = Math.min(completedDays.value + 1, currentPlan.value.plan.total_days)
        router.push({
          name: 'WorkoutOverview',
          params: { 
            planId: currentPlan.value.plan.id,
            dayNumber: nextDay
          }
        })
      }
    }
    
    const viewSettings = () => {
      router.push('/settings')
    }
    
    const viewAllActivity = () => {
      // You could navigate to a detailed activity page
      console.log('View all activity')
    }
    
    // Load data when component mounts
    onMounted(() => {
      if (!checkAuth()) {
        return
      }
      loadDashboardData()
      loadConvAIScript()
    })
    
    return {
      // State
      loading,
      progressData,
      currentPlan,
      recentReports,
      completedDays,
      userProfile,
      
      // Methods
      formatDate,
      getCurrentWeekRange,
      startNewSession,
      startWorkout,
      viewSettings,
      viewAllActivity
    }
  }
}
</script>
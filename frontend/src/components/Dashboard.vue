<template>
    <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <!-- Header -->
      <div class="bg-white shadow-sm border-b border-gray-100">
        <div class="px-6 py-4">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-2xl font-bold text-gray-900">Progress Dashboard</h1>
              <p class="text-gray-600 text-sm">Track your fitness journey</p>
            </div>
            <button 
              @click="startNewSession"
              class="btn btn-primary btn-sm rounded-xl shadow-md"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
              </svg>
              New Session
            </button>
          </div>
        </div>
      </div>
  
      <!-- ElevenLabs AI Coach Widget -->
      <div class="px-6 py-4">
        <div class="bg-white rounded-3xl shadow-lg p-6 border border-gray-100">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-purple-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                  <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-bold text-gray-900">AI Coach Chat</h3>
                <p class="text-gray-500 text-sm">Get personalized fitness advice</p>
              </div>
            </div>
            <div class="flex items-center space-x-1">
              <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span class="text-green-600 text-xs font-medium">Live</span>
            </div>
          </div>
          
          <!-- ElevenLabs Widget Container -->
          <div class="elevenlabs-widget-container rounded-2xl overflow-hidden bg-gradient-to-br from-purple-50 to-blue-50 p-4 min-h-[200px] flex items-center justify-center">
            <elevenlabs-convai agent-id="agent_7401k28639nnf808an9vcf1zb869"></elevenlabs-convai>
            
            <!-- Fallback UI when widget fails to load -->
            <div v-if="!widgetLoaded" class="text-center">
              <div class="w-16 h-16 mx-auto bg-purple-100 rounded-full flex items-center justify-center mb-4">
                <svg class="w-8 h-8 text-purple-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                  <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                </svg>
              </div>
              <p class="text-purple-700 font-medium mb-2">AI Coach Setup Required</p>
              <div class="text-purple-500 text-sm space-y-2 mb-4">
                <p>To use voice coaching, please:</p>
                <ul class="text-left max-w-xs mx-auto space-y-1">
                  <li>• Use HTTPS or localhost</li>
                  <li>• Allow microphone access</li>
                  <li>• Use a modern browser</li>
                </ul>
              </div>
              <button 
                @click="retryWidgetLoad" 
                class="mt-3 px-4 py-2 bg-purple-600 text-white rounded-lg text-sm hover:bg-purple-700 transition-colors"
              >
                Try Again
              </button>
            </div>
          </div>
          
          <div class="mt-4 text-center">
            <p class="text-gray-500 text-xs">Click to start a voice conversation with your AI fitness coach</p>
          </div>
        </div>
      </div>
  
      <div class="px-6 py-8 space-y-8">
        <!-- Session Complete Card -->
        <div v-if="lastSession" class="bg-white rounded-3xl shadow-lg p-8 border border-gray-100">
          <div class="text-center space-y-4">
            <div class="w-20 h-20 mx-auto bg-green-100 rounded-full flex items-center justify-center">
              <svg class="w-10 h-10 text-green-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h2 class="text-2xl font-bold text-gray-900">Session Complete!</h2>
            <p class="text-gray-600">Great work! You completed {{ Math.round(lastSession.completedPercentage) }}% of your workout.</p>
            
            <div class="grid grid-cols-3 gap-6 mt-8">
              <div class="text-center">
                <p class="text-2xl font-bold text-blue-600">{{ formatDuration(lastSession.duration) }}</p>
                <p class="text-gray-500 text-sm">Duration</p>
              </div>
              <div class="text-center">
                <p class="text-2xl font-bold text-green-600">{{ Math.round(lastSession.completedPercentage) }}%</p>
                <p class="text-gray-500 text-sm">Completed</p>
              </div>
              <div class="text-center">
                <p class="text-2xl font-bold text-purple-600">{{ lastSession.sport || 'Running' }}</p>
                <p class="text-gray-500 text-sm">Activity</p>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Weekly Progress -->
        <div class="bg-white rounded-3xl shadow-lg p-6 border border-gray-100">
          <h3 class="text-xl font-bold text-gray-900 mb-6">This Week</h3>
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-blue-50 rounded-2xl p-4">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-blue-900 font-semibold">{{ weeklyStats.sessions }}</p>
                  <p class="text-blue-600 text-sm">Sessions</p>
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
                  <p class="text-green-900 font-semibold">{{ weeklyStats.totalMinutes }}min</p>
                  <p class="text-green-600 text-sm">Total Time</p>
                </div>
                <div class="w-10 h-10 bg-green-200 rounded-full flex items-center justify-center">
                  <svg class="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Recent Sessions -->
        <div class="bg-white rounded-3xl shadow-lg p-6 border border-gray-100">
          <h3 class="text-xl font-bold text-gray-900 mb-6">Recent Sessions</h3>
          <div v-if="sessionHistory.length === 0" class="text-center py-8">
            <div class="w-16 h-16 mx-auto bg-gray-100 rounded-full flex items-center justify-center mb-4">
              <svg class="w-8 h-8 text-gray-400" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              </svg>
            </div>
            <p class="text-gray-500">No sessions yet</p>
            <p class="text-gray-400 text-sm">Complete your first workout to see progress here</p>
          </div>
          <div v-else class="space-y-3">
            <div 
              v-for="(session, index) in recentSessions" 
              :key="index"
              class="flex items-center justify-between p-4 bg-gray-50 rounded-2xl"
            >
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                  <svg class="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M13.49 5.48c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM9.89 19.38l1-4.4 2.1 2v6h2v-7.5l-2.1-2 .6-3c1.3 1.5 3.3 2.5 5.5 2.5v-2c-1.9 0-3.5-1-4.3-2.4l-1-1.6c-.4-.6-1-1-1.7-1-.3 0-.5.1-.8.1L9 5.5v4.5h2V7.4l1.8 7.4L8 19l1.9.4z"/>
                  </svg>
                </div>
                <div>
                  <p class="font-semibold text-gray-900">{{ session.sport || 'Workout' }}</p>
                  <p class="text-gray-500 text-sm">{{ formatDate(session.date) }}</p>
                </div>
              </div>
              <div class="text-right">
                <p class="font-semibold text-gray-900">{{ formatDuration(session.duration) }}</p>
                <p class="text-gray-500 text-sm">{{ Math.round(session.completedPercentage) }}% complete</p>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Achievements -->
        <div class="bg-white rounded-3xl shadow-lg p-6 border border-gray-100">
          <h3 class="text-xl font-bold text-gray-900 mb-6">Achievements</h3>
          <div class="grid grid-cols-2 gap-4">
            <div class="text-center p-4 bg-yellow-50 rounded-2xl">
              <div class="w-12 h-12 mx-auto bg-yellow-200 rounded-full flex items-center justify-center mb-3">
                <svg class="w-6 h-6 text-yellow-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </div>
              <p class="font-semibold text-gray-900">First Session</p>
              <p class="text-gray-500 text-xs">You did it!</p>
            </div>
            <div class="text-center p-4 bg-gray-50 rounded-2xl opacity-50">
              <div class="w-12 h-12 mx-auto bg-gray-200 rounded-full flex items-center justify-center mb-3">
                <svg class="w-6 h-6 text-gray-400" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </div>
              <p class="font-semibold text-gray-400">Week Streak</p>
              <p class="text-gray-400 text-xs">7 days in a row</p>
            </div>
          </div>
        </div>
  
        <!-- Action Buttons -->
        <div class="space-y-4 pb-8">
          <button 
            @click="startNewSession"
            class="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-4 rounded-2xl text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200"
          >
            Start New Workout
          </button>
          <button 
            @click="viewSettings"
            class="w-full bg-gray-100 text-gray-700 py-4 rounded-2xl text-lg font-medium hover:bg-gray-200 transition-all duration-200"
          >
            Settings & Profile
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { useUserStore } from '../stores/user.js'
  import { useRouter } from 'vue-router'
  import { ref, onMounted } from 'vue'
  
  export default {
    name: 'Dashboard',
    setup() {
      const userStore = useUserStore()
      const router = useRouter()
      const widgetLoaded = ref(false)
      
      // Check browser compatibility and provide detailed feedback
      const checkBrowserCompatibility = () => {
        const issues = []
        
        if (!window.isSecureContext) {
          issues.push('HTTPS or localhost required')
        }
        
        if (!navigator.mediaDevices) {
          issues.push('Media devices not supported')
        }
        
        if (!navigator.mediaDevices?.getUserMedia && 
            !navigator.getUserMedia && 
            !navigator.webkitGetUserMedia && 
            !navigator.mozGetUserMedia && 
            !navigator.msGetUserMedia) {
          issues.push('getUserMedia not supported')
        }
        
        return issues
      }
      
      // Load ElevenLabs Convai widget script with error handling
      const loadElevenLabsWidget = async () => {
        try {
          // Check for compatibility issues
          const compatibilityIssues = checkBrowserCompatibility()
          
          if (compatibilityIssues.length > 0) {
            console.warn('Browser compatibility issues:', compatibilityIssues)
            widgetLoaded.value = false
            return
          }
          
          // Check if script is already loaded
          if (document.querySelector('script[src*="elevenlabs/convai-widget-embed"]')) {
            widgetLoaded.value = true
            return
          }
          
          // Load the script
          const script = document.createElement('script')
          script.src = 'https://unpkg.com/@elevenlabs/convai-widget-embed'
          script.async = true
          script.type = 'text/javascript'
          
          // Add error handling for script loading
          script.onerror = () => {
            console.error('Failed to load ElevenLabs Convai widget script')
            widgetLoaded.value = false
          }
          
          script.onload = () => {
            console.log('ElevenLabs Convai widget script loaded successfully')
            // Give the widget time to initialize
            setTimeout(() => {
              widgetLoaded.value = true
            }, 2000)
          }
          
          document.head.appendChild(script)
        } catch (error) {
          console.error('Error loading ElevenLabs widget:', error)
          widgetLoaded.value = false
        }
      }
      
      // Retry loading the widget
      const retryWidgetLoad = () => {
        widgetLoaded.value = false
        loadElevenLabsWidget()
      }
      
      // Load widget when component mounts
      onMounted(() => {
        loadElevenLabsWidget()
      })
      
      return {
        // Widget state
        widgetLoaded,
        
        // Store data
        lastSession: userStore.lastSession,
        recentSessions: userStore.recentSessions,
        sessionHistory: userStore.sessionHistory,
        weeklyStats: userStore.weeklyStats,
        
        // Store methods
        formatDuration: userStore.formatDuration,
        formatDate: userStore.formatDate,
        
        // Widget methods
        retryWidgetLoad,
        checkBrowserCompatibility,
        
        // Navigation methods
        startNewSession() {
          router.push('/sport-selection')
        },
        viewSettings() {
          router.push('/settings')
        }
      }
    }
  }
  </script>
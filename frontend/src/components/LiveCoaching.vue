<template>
  <div class="min-h-screen bg-gradient-to-br from-[#0f2027] via-[#203a43] to-[#2c5364] text-white font-sans relative overflow-hidden">
    
    <!-- Header -->
    <div class="flex items-center justify-between px-6 pt-6 pb-4 bg-white/5 backdrop-blur-md rounded-b-3xl shadow-lg">
      <button 
        @click="endSession"
        class="btn btn-ghost btn-circle text-white hover:bg-white/20 transition"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
      <div class="text-center">
        <p class="text-white/70 text-xs tracking-wide">LIVE COACHING</p>
        <p class="text-lg font-bold tracking-tight">{{ formatTime(elapsedTime) }}</p>
      </div>
      <button class="btn btn-ghost btn-circle text-white hover:bg-white/20 transition">
        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
      </button>
    </div>
    
    <!-- Camera/Pose Detection -->
    <div class="px-6 mt-8">
      <div class="aspect-[4/3] bg-white/10 backdrop-blur-lg rounded-3xl border border-white/20 shadow-lg flex items-center justify-center">
        <div class="text-center space-y-2">
          <div class="w-20 h-20 mx-auto bg-white/20 rounded-full flex items-center justify-center shadow-md">
            <svg class="w-10 h-10" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
          </div>
          <p class="text-white/80 text-sm">Position yourself in frame</p>
          <p class="text-white/50 text-xs">Pose detection active</p>
        </div>
      </div>
    </div>
    
    <!-- Voice Interaction -->
    <div class="px-6 mt-8">
      <div class="bg-white/10 backdrop-blur-md rounded-3xl p-6 shadow-md">
        <div class="flex items-center space-x-3 mb-4">
          <div class="w-10 h-10 bg-accent rounded-full flex items-center justify-center shadow-inner">
            <span class="text-lg">💪</span>
          </div>
          <div>
            <p class="font-semibold text-white">The Coach</p>
            <p class="text-white/60 text-xs">Speaking...</p>
          </div>
        </div>
        <p class="text-white/90 italic leading-relaxed">
          "{{ currentMessage }}"
        </p>
      </div>
    </div>
    
    <!-- Controls -->
    <div class="fixed bottom-8 left-6 right-6">
      <!-- End Session Button -->
      <div class="flex justify-center mb-4">
        <button 
          @click="endSession"
          class="btn bg-red-500/20 border border-red-400/50 text-red-200 hover:bg-red-500/30 px-6 py-2 rounded-2xl shadow-lg backdrop-blur-md transition-all duration-200"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m0 0a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/>
          </svg>
          End Session
        </button>
      </div>

      <div class="flex items-center justify-center space-x-6">
        
        <!-- Mute -->
        <button class="btn btn-circle bg-white/20 border border-white/30 text-white hover:bg-white/30 shadow-lg">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
          </svg>
        </button>
        
        <!-- Main Talk Button -->
        <button 
          @mousedown="startTalking"
          @mouseup="stopTalking"
          @touchstart="startTalking"
          @touchend="stopTalking"
          class="btn btn-circle w-20 h-20 border border-white/30 text-white hover:bg-white/30 shadow-2xl transition-all duration-300"
          :class="{ 'bg-red-500 scale-110 shadow-red-500/50': isTalking, 'bg-white/20': !isTalking }"
        >
          <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
            <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
          </svg>
        </button>
        
        <!-- Settings -->
        <button class="btn btn-circle bg-white/20 border border-white/30 text-white hover:bg-white/30 shadow-lg">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
        </button>
      </div>
      
      <!-- Progress Bar -->
      <div class="mt-6 bg-white/10 rounded-full h-2 shadow-inner overflow-hidden">
        <div 
          class="bg-gradient-to-r from-green-400 to-green-200 h-2 rounded-full transition-all duration-300"
          :style="{ width: progressPercentage + '%' }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '../stores/user.js'
import { useRouter } from 'vue-router'
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

export default {
  name: 'LiveCoaching',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    
    const elapsedTime = ref(0)
    const totalDuration = ref(1800) // 30 minutes in seconds
    const isTalking = ref(false)
    const currentMessage = ref("Great! Let's start with some light stretching to warm up those muscles. I can see you're ready to go!")
    const timer = ref(null)
    const messageTimer = ref(null)

    // Check if user is logged in
    const checkAuth = () => {
      const isLoggedIn = userStore.loadUserFromStorage()
      if (!isLoggedIn) {
        router.push('/login')
        return false
      }
      return true
    }
    
    const messages = [
      "Great! Let's start with some light stretching to warm up those muscles.",
      "Perfect form! Keep that back straight and core engaged.",
      "You're doing amazing! Push through for 10 more seconds.",
      "I can see you're working hard. Remember to breathe steadily.",
      "Excellent! Let's move to the next exercise."
    ]
    
    const progressPercentage = computed(() => {
      return (elapsedTime.value / totalDuration.value) * 100
    })
    
    const startTimer = () => {
      timer.value = setInterval(() => {
        elapsedTime.value++
      }, 1000)
    }
    
    const startMessageRotation = () => {
      messageTimer.value = setInterval(() => {
        const randomMessage = messages[Math.floor(Math.random() * messages.length)]
        currentMessage.value = randomMessage
      }, 8000)
    }
    
    const formatTime = (seconds) => {
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }
    
    const startTalking = () => {
      isTalking.value = true
    }
    
    const stopTalking = () => {
      isTalking.value = false
    }
    
    const endSession = () => {
      // Clear timers
      if (timer.value) clearInterval(timer.value)
      if (messageTimer.value) clearInterval(messageTimer.value)
      
      // Create session data
      const sessionData = {
        duration: elapsedTime.value,
        completedPercentage: progressPercentage.value,
        sport: userStore.selectedSport || 'Running',
        agent: userStore.selectedAgent?.name || 'The Coach',
        date: new Date().toISOString()
      }
      
      // Add session to history
      userStore.addSessionToHistory(sessionData)
      
      // Navigate to dashboard
      router.push('/dashboard')
    }
    
    onMounted(() => {
      // Check authentication first
      if (!checkAuth()) {
        return
      }
      startTimer()
      startMessageRotation()
    })
    
    onBeforeUnmount(() => {
      if (timer.value) clearInterval(timer.value)
      if (messageTimer.value) clearInterval(messageTimer.value)
    })
    
    return {
      elapsedTime,
      totalDuration,
      isTalking,
      currentMessage,
      progressPercentage,
      startTimer,
      startMessageRotation,
      formatTime,
      startTalking,
      stopTalking,
      endSession
    }
  }
}
</script>
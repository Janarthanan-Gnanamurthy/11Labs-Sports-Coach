<template>
  <div class="min-h-screen bg-base-100 px-6 py-8">
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <button @click="goBack" class="btn btn-ghost btn-circle">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </button>
      <h1 class="text-xl font-bold">Choose Your Sport</h1>
      <div class="w-10"></div>
    </div>
    
    <!-- Sport Cards -->
    <div class="space-y-4">
      <div 
        @click="selectSport('running')"
        class="card bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg hover:shadow-xl transition-all duration-200 cursor-pointer transform hover:scale-[1.02]"
      >
        <div class="card-body flex-row items-center">
          <div class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center">
            <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
              <path d="M13.49 5.48c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM9.89 19.38l1-4.4 2.1 2v6h2v-7.5l-2.1-2 .6-3c1.3 1.5 3.3 2.5 5.5 2.5v-2c-1.9 0-3.5-1-4.3-2.4l-1-1.6c-.4-.6-1-1-1.7-1-.3 0-.5.1-.8.1L9 5.5v4.5h2V7.4l1.8 7.4L8 19l1.9.4z"/>
            </svg>
          </div>
          <div class="flex-1 ml-4">
            <h2 class="text-2xl font-bold">Running</h2>
            <p class="text-white/80">Outdoor & treadmill workouts</p>
            <div class="flex mt-2 space-x-2">
              <span class="badge badge-ghost bg-white/20 text-white">Cardio</span>
              <span class="badge badge-ghost bg-white/20 text-white">Endurance</span>
            </div>
          </div>
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </div>
      </div>
      
      <div 
        @click="selectSport('gym')"
        class="card bg-gradient-to-r from-orange-500 to-red-500 text-white shadow-lg hover:shadow-xl transition-all duration-200 cursor-pointer transform hover:scale-[1.02]"
      >
        <div class="card-body flex-row items-center">
          <div class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center">
            <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
              <path d="M20.57 14.86L22 13.43 20.57 12 17 15.57 8.43 7 12 3.43 10.57 2 9.14 3.43 7.71 2 5.57 4.14 4.14 2.71 2.71 4.14l1.43 1.43L2 7.71l1.43 1.43L2 10.57 3.43 12 7 8.43 15.57 17 12 20.57 13.43 22l1.43-1.43L16.29 22l2.14-2.14 1.43 1.43 1.43-1.43-1.43-1.43L22 16.29l-1.43-1.43z"/>
            </svg>
          </div>
          <div class="flex-1 ml-4">
            <h2 class="text-2xl font-bold">Gym</h2>
            <p class="text-white/80">Strength & weight training</p>
            <div class="flex mt-2 space-x-2">
              <span class="badge badge-ghost bg-white/20 text-white">Strength</span>
              <span class="badge badge-ghost bg-white/20 text-white">Muscle</span>
            </div>
          </div>
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </div>
      </div>
    </div>
    
    <!-- Coming Soon -->
    <div class="mt-8 p-4 bg-base-200 rounded-lg">
      <h3 class="font-semibold text-base-content/60 mb-2">Coming Soon</h3>
      <div class="grid grid-cols-2 gap-3">
        <div class="flex items-center space-x-2 text-base-content/40">
          <div class="w-8 h-8 bg-base-300 rounded-full flex items-center justify-center">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
          </div>
          <span class="text-sm">Yoga</span>
        </div>
        <div class="flex items-center space-x-2 text-base-content/40">
          <div class="w-8 h-8 bg-base-300 rounded-full flex items-center justify-center">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
            </svg>
          </div>
          <span class="text-sm">Swimming</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '../stores/user.js'
import { useRouter } from 'vue-router'

export default {
  name: 'SportSelection',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    
    // Check if user is logged in
    const checkAuth = () => {
      const isLoggedIn = userStore.loadUserFromStorage()
      if (!isLoggedIn) {
        router.push('/login')
        return false
      }
      return true
    }
    
    const selectSport = (sport) => {
      if (!checkAuth()) return
      userStore.setSelectedSport(sport)
      router.push('/agent-selection')
    }

    const goBack = () => {
      router.go(-1)
    }
    
    // Check authentication on component mount
    if (!checkAuth()) {
      return {}
    }
    
    return {
      selectSport,
      goBack
    }
  }
}
</script>
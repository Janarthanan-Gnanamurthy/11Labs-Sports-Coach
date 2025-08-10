<template>
  <div class="min-h-screen bg-base-100 px-6 py-8">
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <button @click="goBack" class="btn btn-ghost btn-circle">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </button>
      <h1 class="text-xl font-bold">Session Setup</h1>
      <div class="w-10"></div>
    </div>
    
    <!-- Quick Start -->
    <div class="mb-8">
      <h2 class="text-lg font-semibold mb-4">Quick Start Options</h2>
      <div class="grid grid-cols-2 gap-4">
        <button class="btn btn-outline btn-lg h-20 flex-col">
          <svg class="w-6 h-6 mb-1" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
          <span class="text-sm">15 Min</span>
        </button>
        <button class="btn btn-outline btn-lg h-20 flex-col">
          <svg class="w-6 h-6 mb-1" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
          </svg>
          <span class="text-sm">30 Min</span>
        </button>
      </div>
    </div>
    
    <!-- Custom Setup -->
    <div class="space-y-6">
      <h2 class="text-lg font-semibold">Custom Setup</h2>
      
      <!-- Duration -->
      <div class="form-control">
        <label class="label">
          <span class="label-text font-medium">Duration (minutes)</span>
        </label>
        <input 
          v-model="sessionData.duration" 
          type="range" 
          min="10" 
          max="120" 
          class="range range-primary" 
        />
        <div class="flex justify-between text-xs text-base-content/60 px-2 mt-1">
          <span>10</span>
          <span>30</span>
          <span>60</span>
          <span>120</span>
        </div>
        <div class="text-center mt-2 text-primary font-semibold">
          {{ sessionData.duration }} minutes
        </div>
      </div>
      
      <!-- Intensity -->
      <div class="form-control">
        <label class="label">
          <span class="label-text font-medium">Intensity Level</span>
        </label>
        <div class="grid grid-cols-3 gap-2">
          <button 
            v-for="level in intensityLevels"
            :key="level.value"
            @click="sessionData.intensity = level.value"
            class="btn btn-sm"
            :class="sessionData.intensity === level.value ? 'btn-primary' : 'btn-outline'"
          >
            {{ level.emoji }} {{ level.name }}
          </button>
        </div>
      </div>
      
      <!-- Mood Check -->
      <div class="form-control">
        <label class="label">
          <span class="label-text font-medium">How are you feeling today?</span>
        </label>
        <select v-model="sessionData.mood" class="select select-bordered">
          <option value="">Select mood</option>
          <option value="energetic">😄 Energetic</option>
          <option value="motivated">💪 Motivated</option>
          <option value="tired">😴 Tired</option>
          <option value="stressed">😤 Stressed</option>
          <option value="neutral">😐 Neutral</option>
        </select>
      </div>
    </div>
    
    <!-- Start Session Button -->
    <div class="mt-8">
      <button 
        @click="startSession"
        class="btn btn-primary btn-block btn-lg"
      >
        Start AI Coaching Session
        <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1.5a1.5 1.5 0 011.5 1.5V12a1.5 1.5 0 01-1.5 1.5H9m0-4V9a1.5 1.5 0 011.5-1.5H12"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '../stores/user.js'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

export default {
  name: 'SessionSetup',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    
    const sessionData = ref({
      duration: 30,
      intensity: 'medium',
      mood: ''
    })
    
    const intensityLevels = [
      { value: 'low', name: 'Easy', emoji: '🟢' },
      { value: 'medium', name: 'Medium', emoji: '🟡' },
      { value: 'high', name: 'Intense', emoji: '🔴' }
    ]
    
    const startSession = () => {
      userStore.setSessionData(sessionData.value)
      router.push('/live-coaching')
    }

    const goBack = () => {
      router.go(-1)
    }
    
    return {
      sessionData,
      intensityLevels,
      startSession,
      goBack
    }
  }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 px-6 py-8">
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <button @click="goBack" class="btn btn-ghost btn-circle">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </button>
      <h1 class="text-xl font-bold">Settings & Profile</h1>
      <div class="w-10"></div>
    </div>

    <!-- Profile Section -->
    <div class="bg-white rounded-3xl shadow-lg p-6 border border-gray-100 mb-6">
      <h2 class="text-lg font-bold text-gray-900 mb-4">Profile Information</h2>
      <div class="space-y-4">
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium">Name</span>
          </label>
          <input 
            v-model="userProfile.name" 
            type="text" 
            class="input input-bordered" 
            placeholder="Enter your name"
          />
        </div>
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium">Email</span>
          </label>
          <input 
            v-model="userProfile.email" 
            type="email" 
            class="input input-bordered" 
            placeholder="Enter your email"
          />
        </div>
      </div>
    </div>

    <!-- Preferences Section -->
    <div class="bg-white rounded-3xl shadow-lg p-6 border border-gray-100 mb-6">
      <h2 class="text-lg font-bold text-gray-900 mb-4">Fitness Preferences</h2>
      <div class="space-y-4">
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium">Fitness Level</span>
          </label>
          <select v-model="userProfile.preferences.fitnessLevel" class="select select-bordered">
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium">Preferred Sport</span>
          </label>
          <select v-model="userProfile.preferences.sport" class="select select-bordered">
            <option value="">Select sport</option>
            <option value="running">Running</option>
            <option value="gym">Gym</option>
            <option value="yoga">Yoga</option>
            <option value="swimming">Swimming</option>
          </select>
        </div>
        <div class="form-control">
          <label class="label cursor-pointer">
            <span class="label-text font-medium">Notifications</span>
            <input 
              v-model="userProfile.preferences.notifications" 
              type="checkbox" 
              class="toggle toggle-primary" 
            />
          </label>
        </div>
      </div>
    </div>

    <!-- Goals Section -->
    <div class="bg-white rounded-3xl shadow-lg p-6 border border-gray-100 mb-6">
      <h2 class="text-lg font-bold text-gray-900 mb-4">Fitness Goals</h2>
      <div class="space-y-3">
        <div 
          v-for="goal in availableGoals" 
          :key="goal.id"
          class="flex items-center space-x-3"
        >
          <input 
            :id="goal.id"
            v-model="userProfile.preferences.goals" 
            :value="goal.id"
            type="checkbox" 
            class="checkbox checkbox-primary" 
          />
          <label :for="goal.id" class="label cursor-pointer">
            <span class="label-text">{{ goal.name }}</span>
          </label>
        </div>
      </div>
    </div>

    <!-- Actions Section -->
    <div class="space-y-4">
      <button 
        @click="saveSettings"
        class="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-4 rounded-2xl text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200"
      >
        Save Changes
      </button>
      <button 
        @click="logout"
        class="w-full bg-gray-100 text-gray-700 py-4 rounded-2xl text-lg font-medium hover:bg-gray-200 transition-all duration-200"
      >
        Logout
      </button>
      <button 
        @click="resetData"
        class="w-full bg-red-100 text-red-700 py-4 rounded-2xl text-lg font-medium hover:bg-red-200 transition-all duration-200"
      >
        Reset All Data
      </button>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '../stores/user.js'
import { useRouter } from 'vue-router'
import { computed } from 'vue'

export default {
  name: 'Settings',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    
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
    
    const availableGoals = [
      { id: 'weight-loss', name: 'Weight Loss' },
      { id: 'muscle-gain', name: 'Muscle Gain' },
      { id: 'endurance', name: 'Improve Endurance' },
      { id: 'flexibility', name: 'Increase Flexibility' },
      { id: 'strength', name: 'Build Strength' },
      { id: 'general-fitness', name: 'General Fitness' }
    ]
    
    const goBack = () => {
      router.go(-1)
    }
    
    const saveSettings = () => {
      if (!checkAuth()) return
      userStore.setUserProfile(userProfile.value)
      // You could add a success message here
      router.push('/dashboard')
    }
    
    const logout = () => {
      if (confirm('Are you sure you want to logout?')) {
        userStore.logout()
        router.push('/')
      }
    }
    
    const resetData = () => {
      if (confirm('Are you sure you want to reset all your data? This action cannot be undone.')) {
        userStore.resetUserData()
        router.push('/')
      }
    }

    // Check authentication on component mount
    if (!checkAuth()) {
      return {}
    }
    
    return {
      userProfile,
      availableGoals,
      goBack,
      saveSettings,
      logout,
      resetData
    }
  }
}
</script>

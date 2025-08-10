<template>
  <div class="min-h-screen bg-base-100 px-6 py-8">
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <button @click="goBack" class="btn btn-ghost btn-circle">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </button>
      <h1 class="text-xl font-bold">Choose Your AI Coach</h1>
      <div class="w-10"></div>
    </div>
    
    <!-- Agent Cards -->
    <div class="space-y-4">
      <div 
        v-for="agent in agents" 
        :key="agent.id"
        @click="selectAgent(agent)"
        class="card bg-white shadow-lg hover:shadow-xl transition-all duration-200 cursor-pointer transform hover:scale-[1.02] border-2"
        :class="selectedAgentId === agent.id ? 'border-primary' : 'border-transparent'"
      >
        <div class="card-body">
          <div class="flex items-center space-x-4">
            <div class="avatar">
              <div class="w-12 h-12 rounded-full" :class="agent.bgColor">
                <div class="w-full h-full flex items-center justify-center text-white text-xl">
                  {{ agent.emoji }}
                </div>
              </div>
            </div>
            <div class="flex-1">
              <h3 class="font-bold text-lg">{{ agent.name }}</h3>
              <p class="text-base-content/60 text-sm">{{ agent.description }}</p>
            </div>
            <div v-if="selectedAgentId === agent.id" class="text-primary">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
          </div>
          <div class="flex flex-wrap gap-2 mt-3">
            <span 
              v-for="trait in agent.traits" 
              :key="trait"
              class="badge badge-outline badge-sm"
            >
              {{ trait }}
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Continue Button -->
    <div class="mt-8">
      <button 
        @click="continueToSetup"
        :disabled="!selectedAgentId"
        class="btn btn-primary btn-block btn-lg"
        :class="selectedAgentId ? 'btn-primary' : 'btn-disabled'"
      >
        Continue with {{ selectedAgent?.name || 'Coach' }}
      </button>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '../stores/user.js'
import { useRouter } from 'vue-router'
import { ref, computed } from 'vue'

export default {
  name: 'AgentSelection',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    
    const selectedAgentId = ref(null)

    // Check if user is logged in
    const checkAuth = () => {
      const isLoggedIn = userStore.loadUserFromStorage()
      if (!isLoggedIn) {
        router.push('/login')
        return false
      }
      return true
    }
    
    const agents = [
      {
        id: 'coach',
        name: 'The Coach',
        emoji: '💪',
        bgColor: 'bg-blue-500',
        description: 'Structured, motivating, results-focused',
        traits: ['Disciplined', 'Goal-oriented', 'Technical']
      },
      {
        id: 'motivator',
        name: 'The Motivator',
        emoji: '🔥',
        bgColor: 'bg-red-500',
        description: 'High-energy, encouraging, pump-you-up',
        traits: ['Energetic', 'Positive', 'Inspiring']
      },
      {
        id: 'buddy',
        name: 'Twin Buddy',
        emoji: '👯',
        bgColor: 'bg-green-500',
        description: 'Friendly, supportive, like a workout partner',
        traits: ['Casual', 'Supportive', 'Fun']
      },
      {
        id: 'wellness',
        name: 'Wellness Guide',
        emoji: '🧘',
        bgColor: 'bg-purple-500',
        description: 'Mindful, holistic, balance-focused',
        traits: ['Mindful', 'Balanced', 'Gentle']
      }
    ]
    
    const selectedAgent = computed(() => {
      return agents.find(agent => agent.id === selectedAgentId.value)
    })
    
    const selectAgent = (agent) => {
      if (!checkAuth()) return
      selectedAgentId.value = agent.id
    }
    
    const continueToSetup = () => {
      if (!checkAuth()) return
      if (selectedAgentId.value) {
        userStore.setSelectedAgent(selectedAgent.value)
        router.push('/session-setup')
      }
    }

    const goBack = () => {
      router.go(-1)
    }

    // Check authentication on component mount
    if (!checkAuth()) {
      return {}
    }
    
    return {
      selectedAgentId,
      agents,
      selectedAgent,
      selectAgent,
      continueToSetup,
      goBack
    }
  }
}
</script>

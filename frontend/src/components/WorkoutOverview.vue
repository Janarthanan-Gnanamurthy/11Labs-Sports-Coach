<template>
  <div class="min-h-screen bg-gray-50">
    <!-- iPhone-style Status Bar -->
    <div class="bg-black text-white px-6 py-2 flex justify-between items-center text-sm">
      <span>5:15</span>
      <div class="flex items-center space-x-1">
        <span class="text-xs">1.62 KB/s</span>
        <span class="text-xs">5G</span>
        <span class="text-xs">44%</span>
      </div>
    </div>

    <!-- Header -->
    <div class="bg-white px-6 py-4 border-b border-gray-100">
      <div class="flex items-center justify-between">
        <button @click="goBack" class="w-8 h-8 flex items-center justify-center">
          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
        </button>
        <button class="w-8 h-8 flex items-center justify-center">
          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="px-6 py-4">
      <!-- Workout Title -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">{{ workoutDay.title || `Day ${workoutDay.day_number}` }}</h1>
          <div class="flex items-center mt-2">
            <div class="flex items-center">
              <svg v-for="i in 3" :key="i" class="w-5 h-5 mr-1" :class="i <= difficultyLevel ? 'text-purple-500' : 'text-gray-300'" fill="currentColor" viewBox="0 0 24 24">
                <path d="M13 2.05v3.03c3.39.49 6 3.39 6 6.92 0 .9-.18 1.75-.5 2.54l2.6 1.53c.56-1.24.9-2.62.9-4.07 0-5.18-3.95-9.45-9-9.95zM12 19c-3.87 0-7-3.13-7-7 0-3.53 2.61-6.43 6-6.92V2.05c-5.05.5-9 4.76-9 9.95 0 5.52 4.47 10 9.99 10 3.31 0 6.24-1.61 8.06-4.09l-2.6-1.53C16.17 17.98 14.21 19 12 19z"/>
              </svg>
            </div>
            <span class="text-gray-600 font-medium ml-2">{{ difficultyText }}</span>
          </div>
        </div>
        <div class="w-20 h-20 bg-gray-200 rounded-full overflow-hidden">
          <img src="https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=80&h=80&fit=crop&crop=face" alt="Workout" class="w-full h-full object-cover">
        </div>
      </div>

      <!-- Workout Summary Card -->
      <div class="bg-white rounded-3xl p-6 mb-6 shadow-sm">
        <div class="grid grid-cols-3 gap-4 text-center">
          <div>
            <p class="text-2xl font-bold text-gray-900">{{ workoutDay.exercises?.length || 0 }}</p>
            <p class="text-gray-600 text-sm">Exercises</p>
          </div>
          <div>
            <p class="text-2xl font-bold text-gray-900">{{ estimatedTime }}</p>
            <p class="text-gray-600 text-sm">Time</p>
          </div>
          <div>
            <p class="text-2xl font-bold text-gray-900">{{ estimatedCalories }}</p>
            <p class="text-gray-600 text-sm">Calories</p>
          </div>
        </div>
      </div>

      <!-- Workout Settings -->
      <div class="bg-white rounded-3xl p-6 mb-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">Workout Settings</h3>
            <p class="text-gray-600 text-sm">Music & Coach & Timer, etc.</p>
          </div>
          <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </div>
      </div>

      <!-- Exercise List -->
      <div class="bg-white rounded-3xl p-6 mb-6 shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Exercise</h3>
          <button class="w-6 h-6 flex items-center justify-center">
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
          </button>
        </div>
        
        <div class="space-y-4">
          <div 
            v-for="(exercise, index) in workoutDay.exercises" 
            :key="exercise.instance.id"
            class="flex items-center justify-between p-4 bg-gray-50 rounded-2xl"
          >
            <div class="flex items-center space-x-4">
              <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M13.49 5.48c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM9.89 19.38l1-4.4 2.1 2v6h2v-7.5l-2.1-2 .6-3c1.3 1.5 3.3 2.5 5.5 2.5v-2c-1.9 0-3.5-1-4.3-2.4l-1-1.6c-.4-.6-1-1-1.7-1-.3 0-.5.1-.8.1L9 5.5v4.5h2V7.4l1.8 7.4L8 19l1.9.4z"/>
                </svg>
              </div>
              <div>
                <h4 class="font-semibold text-gray-900">{{ exercise.exercise_type.name }}</h4>
                <p class="text-gray-500 text-sm">
                  {{ exercise.instance.current_sets || exercise.instance.target_sets }} sets × 
                  {{ exercise.instance.current_reps || exercise.instance.target_reps }} reps
                </p>
              </div>
            </div>
            <div class="text-right">
              <p class="text-sm text-gray-500">
                {{ exercise.instance.rest_seconds }}s rest
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex space-x-4 mb-6">
        <button 
          @click="adjustWorkout"
          class="flex-1 bg-gray-200 text-gray-700 py-4 rounded-2xl font-medium flex items-center justify-center space-x-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
          </svg>
          <span>Adjust</span>
        </button>
      </div>

      <!-- Start Button -->
      <button 
        @click="startWorkout"
        class="w-full bg-blue-500 text-white py-4 rounded-2xl font-bold text-lg shadow-lg"
      >
        START
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../stores/user.js'

export default {
  name: 'WorkoutOverview',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const userStore = useUserStore()
    
    const loading = ref(true)
    const workoutDay = ref({})
    const planId = ref(null)
    const dayNumber = ref(null)
    
    // Computed properties
    const difficultyLevel = computed(() => {
      const level = userStore.userProfile?.fitness_level || 'beginner'
      switch (level) {
        case 'beginner': return 1
        case 'intermediate': return 2
        case 'advanced': return 3
        default: return 2
      }
    })
    
    const difficultyText = computed(() => {
      const level = userStore.userProfile?.fitness_level || 'beginner'
      return level.charAt(0).toUpperCase() + level.slice(1)
    })
    
    const estimatedTime = computed(() => {
      if (!workoutDay.value.exercises) return '0 min'
      const totalExercises = workoutDay.value.exercises.length
      const estimatedMinutes = Math.ceil(totalExercises * 2.5) // ~2.5 min per exercise
      return `${estimatedMinutes} min`
    })
    
    const estimatedCalories = computed(() => {
      if (!workoutDay.value.exercises) return '0 kcal'
      const totalExercises = workoutDay.value.exercises.length
      const estimatedCalories = Math.round(totalExercises * 8.9) // ~8.9 calories per exercise
      return `${estimatedCalories} kcal(≈)`
    })
    
    // Methods
    const fetchWorkoutDay = async () => {
      try {
        const response = await fetch(`http://localhost:8000/plans/${planId.value}`)
        if (response.ok) {
          const planData = await response.json()
          const day = planData.days.find(d => d.day.day_number === dayNumber.value)
          if (day) {
            workoutDay.value = day
          } else {
            throw new Error('Day not found')
          }
        } else {
          throw new Error('Failed to fetch workout data')
        }
      } catch (error) {
        console.error('Error fetching workout day:', error)
        // Fallback to mock data for demo
        workoutDay.value = {
          day_number: dayNumber.value,
          title: `Day ${dayNumber.value}`,
          exercises: [
            {
              instance: { id: 1, target_sets: 3, target_reps: 12, rest_seconds: 60 },
              exercise_type: { name: 'JUMPING JACKS' }
            },
            {
              instance: { id: 2, target_sets: 3, target_reps: 14, rest_seconds: 60 },
              exercise_type: { name: 'LONG ARM CRUNCHES' }
            },
            {
              instance: { id: 3, target_sets: 3, target_reps: 14, rest_seconds: 60 },
              exercise_type: { name: 'HEEL TOUCH' }
            },
            {
              instance: { id: 4, target_sets: 3, target_reps: 12, rest_seconds: 60 },
              exercise_type: { name: 'FLUTTER KICKS' }
            }
          ]
        }
      } finally {
        loading.value = false
      }
    }
    
    const goBack = () => {
      // Go back to dashboard if coming from there, otherwise go back in history
      if (document.referrer.includes('/dashboard')) {
        router.push('/dashboard')
      } else {
        router.go(-1)
      }
    }
    
    const adjustWorkout = () => {
      // Navigate to workout adjustment page
      console.log('Adjust workout')
    }
    
    const startWorkout = () => {
      router.push({
        name: 'WorkoutSession',
        params: { 
          planId: planId.value,
          dayNumber: dayNumber.value
        }
      })
    }
    
    // Initialize
    onMounted(() => {
      planId.value = parseInt(route.params.planId)
      dayNumber.value = parseInt(route.params.dayNumber)
      fetchWorkoutDay()
    })
    
    return {
      loading,
      workoutDay,
      difficultyLevel,
      difficultyText,
      estimatedTime,
      estimatedCalories,
      goBack,
      adjustWorkout,
      startWorkout
    }
  }
}
</script>

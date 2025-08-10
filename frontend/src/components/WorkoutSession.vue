<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Progress Bar -->
    <div class="bg-white px-6 py-4">
      <div class="flex items-center justify-between mb-2">
        <span class="text-sm text-gray-600">Progress</span>
        <span class="text-sm font-medium text-gray-900">{{ currentExerciseIndex + 1 }} / {{ totalExercises }}</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div 
          class="bg-blue-500 h-2 rounded-full transition-all duration-300"
          :style="{ width: `${((currentExerciseIndex + 1) / totalExercises) * 100}%` }"
        ></div>
      </div>
    </div>

    <!-- Header Controls -->
    <div class="bg-white px-6 py-4 border-b border-gray-100">
      <div class="flex items-center justify-between">
        <button @click="goBack" class="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
        </button>
        
        <div class="flex space-x-2">
          <button class="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
          </button>
          <button class="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"/>
            </svg>
          </button>
          <button class="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"/>
            </svg>
          </button>
          <button class="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Exercise Display -->
    <div class="flex-1 flex flex-col items-center justify-center px-6 py-8">
      <!-- Exercise Illustration -->
      <div class="w-64 h-64 bg-blue-50 rounded-3xl flex items-center justify-center mb-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-br from-blue-100 to-blue-200 opacity-50"></div>
        <div class="relative z-10 text-center">
          <div class="w-32 h-32 mx-auto mb-4 bg-white rounded-full flex items-center justify-center shadow-lg">
            <svg class="w-16 h-16 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M13.49 5.48c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM9.89 19.38l1-4.4 2.1 2v6h2v-7.5l-2.1-2 .6-3c1.3 1.5 3.3 2.5 5.5 2.5v-2c-1.9 0-3.5-1-4.3-2.4l-1-1.6c-.4-.6-1-1-1.7-1-.3 0-.5.1-.8.1L9 5.5v4.5h2V7.4l1.8 7.4L8 19l1.9.4z"/>
            </svg>
          </div>
          <p class="text-xs text-blue-600 font-medium">LEAPFITNESS</p>
        </div>
      </div>

      <!-- Exercise Info -->
      <div class="text-center mb-8">
        <div class="mb-4">
          <p class="text-4xl font-bold text-gray-900">{{ currentExercise?.instance?.current_reps || currentExercise?.instance?.target_reps }}</p>
          <p class="text-lg text-gray-600">reps</p>
        </div>
        
        <div class="mb-4">
          <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ currentExercise?.exercise_type?.name }}</h2>
          <div class="flex items-center justify-center space-x-2">
            <button class="w-6 h-6 bg-gray-100 rounded-full flex items-center justify-center">
              <svg class="w-3 h-3 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Feedback Buttons -->
        <div class="flex items-center justify-center space-x-4">
          <button class="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14H5.236a2 2 0 01-1.789-2.894l3.5-7A2 2 0 018.736 3h4.018a2 2 0 01.485.06l3.76.94m-7 10v5a2 2 0 002 2h.096c.5 0 .905-.405.905-.904 0-.715.211-1.413.608-2.008L17 13V4m-7 10h2m5-10h2a2 2 0 012 2v6a2 2 0 01-2 2h-2.5"/>
            </svg>
          </button>
          <button class="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Bottom Controls -->
    <div class="bg-white px-6 py-6 border-t border-gray-100">
      <div class="flex items-center justify-between">
        <button 
          @click="previousExercise"
          :disabled="currentExerciseIndex === 0"
          class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center disabled:opacity-50"
        >
          <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
        </button>

        <button 
          @click="completeExercise"
          class="flex-1 bg-blue-500 text-white py-4 rounded-2xl font-bold text-lg mx-4 flex items-center justify-center"
        >
          <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          Complete
        </button>

        <button 
          @click="nextExercise"
          :disabled="currentExerciseIndex === totalExercises - 1"
          class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center disabled:opacity-50"
        >
          <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../stores/user.js'

export default {
  name: 'WorkoutSession',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const userStore = useUserStore()
    
    const loading = ref(true)
    const workoutDay = ref({})
    const currentExerciseIndex = ref(0)
    const completedExercises = ref([])
    const planId = ref(null)
    const dayNumber = ref(null)
    
    // Computed properties
    const totalExercises = computed(() => workoutDay.value.exercises?.length || 0)
    
    const currentExercise = computed(() => {
      if (!workoutDay.value.exercises) return null
      return workoutDay.value.exercises[currentExerciseIndex.value]
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
      // Go back to workout overview
      router.push({
        name: 'WorkoutOverview',
        params: { 
          planId: planId.value,
          dayNumber: dayNumber.value
        }
      })
    }
    
    const previousExercise = () => {
      if (currentExerciseIndex.value > 0) {
        currentExerciseIndex.value--
      }
    }
    
    const nextExercise = () => {
      if (currentExerciseIndex.value < totalExercises.value - 1) {
        currentExerciseIndex.value++
      }
    }
    
    const completeExercise = async () => {
      const exercise = currentExercise.value
      if (!exercise) return
      
      // Add to completed exercises
      completedExercises.value.push({
        exercise_instance_id: exercise.instance.id,
        rpe: 7.0, // Default RPE - could be made interactive
        reps_completed: exercise.instance.current_reps || exercise.instance.target_reps,
        sets_completed: exercise.instance.current_sets || exercise.instance.target_sets,
        success: true,
        duration_seconds: 120 // Default duration - could be tracked
      })
      
      // Move to next exercise or finish workout
      if (currentExerciseIndex.value < totalExercises.value - 1) {
        currentExerciseIndex.value++
      } else {
        // Workout completed - save to backend and show celebration
        await saveWorkoutSession()
        router.push({
          name: 'WorkoutCelebration',
          params: { 
            planId: planId.value,
            dayNumber: dayNumber.value
          }
        })
      }
    }
    
    const saveWorkoutSession = async () => {
      try {
        const response = await fetch(`http://localhost:8000/users/${userStore.userProfile.id}/plans/${planId.value}/session`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(completedExercises.value)
        })
        
        if (!response.ok) {
          throw new Error('Failed to save workout session')
        }
        
        console.log('Workout session saved successfully')
      } catch (error) {
        console.error('Error saving workout session:', error)
      }
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
      currentExerciseIndex,
      totalExercises,
      currentExercise,
      goBack,
      previousExercise,
      nextExercise,
      completeExercise
    }
  }
}
</script>

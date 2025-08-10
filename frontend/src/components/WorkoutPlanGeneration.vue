<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">Create Your Personalized Workout Plan</h1>
        <p class="text-lg text-gray-600">Let's design a workout plan tailored to your fitness goals and preferences</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-flex items-center px-4 py-2 font-semibold leading-6 text-white bg-blue-600 rounded-md shadow-sm">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Generating your personalized workout plan...
        </div>
        <p class="mt-4 text-gray-600">This may take a few moments as we create the perfect plan for you</p>
      </div>

      <!-- Plan Generation Form -->
      <div v-else-if="!planGenerated" class="bg-white rounded-2xl shadow-xl p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Plan Preferences</h2>
        
        <form @submit.prevent="generatePlan" class="space-y-6">
          <!-- Plan Duration -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-3">Plan Duration</label>
            <div class="grid grid-cols-3 gap-4">
              <label 
                v-for="duration in planDurations" 
                :key="duration.days"
                class="relative cursor-pointer"
              >
                <input 
                  type="radio" 
                  :value="duration.days" 
                  v-model="planForm.days" 
                  class="sr-only"
                />
                <div class="border-2 rounded-lg p-4 text-center transition-all duration-200"
                     :class="planForm.days === duration.days ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'">
                  <div class="text-lg font-semibold text-gray-900">{{ duration.days }} Days</div>
                  <div class="text-sm text-gray-600">{{ duration.description }}</div>
                </div>
              </label>
            </div>
          </div>

          <!-- Focus Areas -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-3">Focus Areas (Select all that apply)</label>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
              <label 
                v-for="area in focusAreas" 
                :key="area.id"
                class="relative cursor-pointer"
              >
                <input 
                  type="checkbox" 
                  :value="area.id" 
                  v-model="planForm.focus_areas" 
                  class="sr-only"
                />
                <div class="border-2 rounded-lg p-3 text-center transition-all duration-200"
                     :class="planForm.focus_areas.includes(area.id) ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'">
                  <div class="text-sm font-medium text-gray-900">{{ area.name }}</div>
                  <div class="text-xs text-gray-600">{{ area.description }}</div>
                </div>
              </label>
            </div>
          </div>

          <!-- Equipment Preference -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-3">Equipment Preference</label>
            <div class="grid grid-cols-2 gap-4">
              <label class="relative cursor-pointer">
                <input 
                  type="radio" 
                  :value="false" 
                  v-model="planForm.include_equipment" 
                  class="sr-only"
                />
                <div class="border-2 rounded-lg p-4 text-center transition-all duration-200"
                     :class="!planForm.include_equipment ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'">
                  <div class="text-lg font-semibold text-gray-900">Bodyweight Only</div>
                  <div class="text-sm text-gray-600">No equipment needed</div>
                </div>
              </label>
              <label class="relative cursor-pointer">
                <input 
                  type="radio" 
                  :value="true" 
                  v-model="planForm.include_equipment" 
                  class="sr-only"
                />
                <div class="border-2 rounded-lg p-4 text-center transition-all duration-200"
                     :class="planForm.include_equipment ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'">
                  <div class="text-lg font-semibold text-gray-900">With Equipment</div>
                  <div class="text-sm text-gray-600">Dumbbells, resistance bands, etc.</div>
                </div>
              </label>
            </div>
          </div>

          <!-- Additional Preferences -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Additional Preferences (Optional)</label>
            <textarea
              v-model="planForm.preferences"
              rows="3"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              placeholder="Any specific preferences, injuries, or special considerations..."
            ></textarea>
          </div>

          <!-- Generate Button -->
          <button
            type="submit"
            :disabled="generating"
            class="w-full bg-blue-600 text-white py-4 rounded-lg font-medium hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="generating" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Generating Plan...
            </span>
            <span v-else>Generate My Workout Plan</span>
          </button>
        </form>

        <!-- Error Message -->
        <div v-if="error" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-red-600 text-sm">{{ error }}</p>
        </div>
      </div>

      <!-- Generated Plan Display -->
      <div v-else-if="planGenerated && workoutPlan" class="space-y-6">
        <!-- Plan Header -->
        <div class="bg-white rounded-2xl shadow-xl p-8">
          <div class="flex items-center justify-between mb-6">
            <div>
              <h2 class="text-3xl font-bold text-gray-900 mb-2">{{ workoutPlan.plan.title }}</h2>
              <p class="text-lg text-gray-600">{{ workoutPlan.plan.description }}</p>
            </div>
            <div class="text-right">
              <div class="text-2xl font-bold text-blue-600">{{ workoutPlan.plan.total_days }} Days</div>
              <div class="text-sm text-gray-500">Workout Plan</div>
            </div>
          </div>
          
          <div class="flex flex-wrap gap-4">
            <div class="bg-blue-50 px-4 py-2 rounded-lg">
              <span class="text-sm font-medium text-blue-800">Generated for: {{ userProfile.name }}</span>
            </div>
            <div class="bg-green-50 px-4 py-2 rounded-lg">
              <span class="text-sm font-medium text-green-800">Level: {{ userProfile.fitness_level || 'Beginner' }}</span>
            </div>
            <div class="bg-purple-50 px-4 py-2 rounded-lg">
              <span class="text-sm font-medium text-purple-800">Focus: {{ getFocusAreasText() }}</span>
            </div>
          </div>
        </div>

        <!-- Plan Days -->
        <div v-for="dayData in workoutPlan.days" :key="dayData.day.id" class="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div class="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4">
            <h3 class="text-xl font-bold text-white">{{ dayData.day.title }}</h3>
            <p class="text-blue-100">{{ getDayDescription(dayData.day) }}</p>
          </div>
          
          <div class="p-6">
            <div v-if="dayData.day.rest_day" class="text-center py-8">
              <div class="text-6xl mb-4">😴</div>
              <h4 class="text-xl font-semibold text-gray-900 mb-2">Rest Day</h4>
              <p class="text-gray-600">Take time to recover and prepare for your next workout</p>
            </div>
            
            <div v-else class="space-y-4">
              <div v-for="exercise in dayData.exercises" :key="exercise.instance.id" class="border border-gray-200 rounded-lg p-4">
                <div class="flex items-start justify-between mb-3">
                  <div>
                    <h4 class="text-lg font-semibold text-gray-900">{{ exercise.exercise_type.name }}</h4>
                    <p class="text-sm text-gray-600">{{ exercise.exercise_type.primary_muscle }}</p>
                  </div>
                  <div class="text-right">
                    <div class="text-lg font-bold text-blue-600">{{ exercise.instance.target_sets }} × {{ exercise.instance.target_reps }}</div>
                    <div class="text-sm text-gray-500">{{ exercise.instance.rest_seconds }}s rest</div>
                  </div>
                </div>
                
                <div v-if="exercise.instance.notes" class="bg-gray-50 p-3 rounded-lg">
                  <p class="text-sm text-gray-700">{{ exercise.instance.notes }}</p>
                </div>
                
                <div class="flex items-center mt-3 text-sm text-gray-500">
                  <span v-if="exercise.exercise_type.equipment_needed" class="flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    Equipment needed
                  </span>
                  <span v-else class="flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    Bodyweight only
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-col sm:flex-row gap-4">
          <button
            @click="startWorkout"
            class="flex-1 bg-blue-600 text-white py-4 rounded-lg font-medium hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200"
          >
            Start My First Workout
          </button>
          <button
            @click="goToDashboard"
            class="flex-1 bg-gray-100 text-gray-700 py-4 rounded-lg font-medium hover:bg-gray-200 focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-all duration-200"
          >
            View Dashboard
          </button>
          <button
            @click="generateNewPlan"
            class="flex-1 bg-green-600 text-white py-4 rounded-lg font-medium hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all duration-200"
          >
            Generate New Plan
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

export default {
  name: 'WorkoutPlanGeneration',
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    
    const loading = ref(false)
    const generating = ref(false)
    const planGenerated = ref(false)
    const workoutPlan = ref(null)
    const error = ref('')
    
    const planForm = ref({
      days: 7,
      focus_areas: ['strength'],
      include_equipment: false,
      preferences: ''
    })
    
    const planDurations = [
      { days: 7, description: '1 Week' },
      { days: 14, description: '2 Weeks' },
      { days: 21, description: '3 Weeks' }
    ]
    
    const focusAreas = [
      { id: 'strength', name: 'Strength', description: 'Build muscle and power' },
      { id: 'cardio', name: 'Cardio', description: 'Improve endurance' },
      { id: 'flexibility', name: 'Flexibility', description: 'Increase mobility' },
      { id: 'weight_loss', name: 'Weight Loss', description: 'Burn calories' },
      { id: 'muscle_gain', name: 'Muscle Gain', description: 'Build lean mass' },
      { id: 'endurance', name: 'Endurance', description: 'Improve stamina' }
    ]
    
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
    
    const generatePlan = async () => {
      if (!checkAuth()) return
      
      generating.value = true
      error.value = ''
      
      try {
        const response = await fetch(`http://localhost:8000/users/${userProfile.value.id}/plans/generate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(planForm.value)
        })
        
        if (response.ok) {
          const planResult = await response.json()
          
          // Get the detailed plan
          const planDetailsResponse = await fetch(`http://localhost:8000/plans/${planResult.plan_id}`)
          if (planDetailsResponse.ok) {
            workoutPlan.value = await planDetailsResponse.json()
            planGenerated.value = true
          } else {
            throw new Error('Failed to fetch plan details')
          }
        } else {
          const errorData = await response.json()
          error.value = errorData.detail || 'Failed to generate workout plan. Please try again.'
        }
      } catch (err) {
        console.error('Plan generation error:', err)
        error.value = 'Network error. Please check your connection and try again.'
      } finally {
        generating.value = false
      }
    }
    
    const getFocusAreasText = () => {
      if (!planForm.value.focus_areas.length) return 'General Fitness'
      return planForm.value.focus_areas
        .map(area => focusAreas.find(fa => fa.id === area)?.name)
        .filter(Boolean)
        .join(', ')
    }
    
    const getDayDescription = (day) => {
      if (day.rest_day) return 'Rest and Recovery'
      return `Day ${day.day_number} of your workout plan`
    }
    
    const startWorkout = () => {
      if (workoutPlan.value) {
        router.push({
          name: 'WorkoutOverview',
          params: { 
            planId: workoutPlan.value.plan.id,
            dayNumber: 1
          }
        })
      }
    }
    
    const goToDashboard = () => {
      router.push('/dashboard')
    }
    
    const generateNewPlan = () => {
      planGenerated.value = false
      workoutPlan.value = null
      planForm.value = {
        days: 7,
        focus_areas: ['strength'],
        include_equipment: false,
        preferences: ''
      }
    }
    
    onMounted(() => {
      if (!checkAuth()) {
        return
      }
    })
    
    return {
      loading,
      generating,
      planGenerated,
      workoutPlan,
      error,
      planForm,
      planDurations,
      focusAreas,
      userProfile,
      generatePlan,
      getFocusAreasText,
      getDayDescription,
      startWorkout,
      goToDashboard,
      generateNewPlan
    }
  }
}
</script>

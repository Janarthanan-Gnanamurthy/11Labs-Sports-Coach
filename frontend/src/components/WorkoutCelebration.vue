<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex flex-col items-center justify-center px-6 py-8 relative overflow-hidden">
      <!-- Confetti Animation - Fixed positioning -->
      <div class="fixed inset-0 pointer-events-none z-0">
        <div 
          v-for="i in 20" 
          :key="i"
          class="absolute w-2 h-2 bg-yellow-400 rounded-full animate-bounce opacity-80"
          :style="{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 2}s`,
            animationDuration: `${1 + Math.random() * 2}s`
          }"
        ></div>
        <div 
          v-for="i in 15" 
          :key="`star-${i}`"
          class="absolute w-3 h-3 bg-white rounded-full animate-pulse opacity-60"
          :style="{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 3}s`,
            animationDuration: `${2 + Math.random() * 2}s`
          }"
        ></div>
      </div>
  
      <!-- Main Content - Higher z-index -->
      <div class="relative z-10 flex flex-col items-center w-full max-w-lg">
        <!-- Trophy Section -->
        <div class="relative mb-8">
          <!-- Trophy Icon -->
          <div class="relative w-32 h-32 bg-yellow-400 rounded-full flex items-center justify-center shadow-2xl animate-bounce">
            <svg class="w-20 h-20 text-yellow-800" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
          </div>
        </div>
  
        <!-- Celebration Text -->
        <div class="text-center mb-8">
          <h1 class="text-4xl font-bold text-white mb-4 animate-pulse drop-shadow-lg">🎉 Congratulations! 🎉</h1>
          <p class="text-xl text-white mb-2 drop-shadow-md">You've completed</p>
          <h2 class="text-3xl font-bold text-white mb-4 drop-shadow-lg">{{ workoutDay.title || `Day ${workoutDay.day_number}` }}</h2>
          <p class="text-lg text-white drop-shadow-md">Great job! Keep up the amazing work!</p>
        </div>
  
        <!-- Workout Stats -->
        <div class="bg-white/20 backdrop-blur-sm rounded-3xl p-6 mb-8 w-full border border-white/30">
          <h3 class="text-xl font-bold text-white mb-4 text-center drop-shadow-md">Workout Summary</h3>
          <div class="grid grid-cols-2 gap-4">
            <div class="text-center">
              <p class="text-3xl font-bold text-white drop-shadow-md">{{ workoutStats.totalExercises }}</p>
              <p class="text-white text-sm font-medium drop-shadow-sm">Exercises</p>
            </div>
            <div class="text-center">
              <p class="text-3xl font-bold text-white drop-shadow-md">{{ workoutStats.totalTime }}</p>
              <p class="text-white text-sm font-medium drop-shadow-sm">Minutes</p>
            </div>
            <div class="text-center">
              <p class="text-3xl font-bold text-white drop-shadow-md">{{ workoutStats.totalCalories }}</p>
              <p class="text-white text-sm font-medium drop-shadow-sm">Calories</p>
            </div>
            <div class="text-center">
              <p class="text-3xl font-bold text-white drop-shadow-md">{{ workoutStats.successRate }}%</p>
              <p class="text-white text-sm font-medium drop-shadow-sm">Success</p>
            </div>
          </div>
        </div>
  
        <!-- Progress Update -->
        <div class="bg-white/20 backdrop-blur-sm rounded-3xl p-6 mb-8 w-full border border-white/30">
          <h3 class="text-xl font-bold text-white mb-4 text-center drop-shadow-md">Progress Update</h3>
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-white font-medium drop-shadow-sm">Weekly Goal</span>
              <span class="text-white font-semibold drop-shadow-sm">{{ progressData.weeklyProgress }}/{{ progressData.weeklyGoal }}</span>
            </div>
            <div class="w-full bg-blue-300/30 rounded-full h-3">
              <div 
                class="bg-yellow-400 h-3 rounded-full transition-all duration-1000"
                :style="{ width: `${Math.min((progressData.weeklyProgress / progressData.weeklyGoal) * 100, 100)}%` }"
              ></div>
            </div>
            <p class="text-center text-white text-sm font-medium drop-shadow-sm">
              {{ progressData.weeklyProgress >= progressData.weeklyGoal ? 'Weekly goal achieved! 🎯' : `${progressData.weeklyGoal - progressData.weeklyProgress} more workouts to go!` }}
            </p>
          </div>
        </div>
  
        <!-- Action Buttons -->
        <div class="w-full space-y-4">
          <button 
            @click="continueToNextDay"
            class="btn btn-primary w-full bg-yellow-400 text-yellow-900 border-yellow-400 hover:bg-yellow-300 hover:border-yellow-300 py-4 rounded-2xl font-bold text-lg shadow-lg transition-colors"
          >
            Continue to Next Day
          </button>
          
          <button 
            @click="goToDashboard"
            class="btn btn-outline w-full text-white border-white/40 hover:bg-white/20 hover:border-white/60 py-4 rounded-2xl font-bold text-lg backdrop-blur-sm transition-colors"
          >
            Back to Dashboard
          </button>
          
          <button 
            @click="shareWorkout"
            class="btn btn-ghost w-full text-white hover:bg-white/20 py-3 rounded-2xl font-medium backdrop-blur-sm transition-colors"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z"/>
            </svg>
            Share Achievement
          </button>
        </div>
  
        <!-- Motivational Quote -->
        <div class="mt-8 text-center">
          <p class="text-white italic text-sm drop-shadow-sm opacity-90">
            "The only bad workout is the one that didn't happen."
          </p>
          <p class="text-white text-xs mt-1 drop-shadow-sm opacity-70">- Unknown</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { useUserStore } from '../stores/user.js'
  
  export default {
    name: 'WorkoutCelebration',
    setup() {
      const router = useRouter()
      const route = useRoute()
      const userStore = useUserStore()
      
      const workoutDay = ref({})
      const workoutStats = ref({
        totalExercises: 0,
        totalTime: 0,
        totalCalories: 0,
        successRate: 100
      })
      const progressData = ref({
        weeklyProgress: 0,
        weeklyGoal: 5
      })
      const planId = ref(null)
      const dayNumber = ref(null)
      
      // Methods
      const fetchWorkoutData = async () => {
        try {
          const response = await fetch(`http://localhost:8000/plans/${planId.value}`)
          if (response.ok) {
            const planData = await response.json()
            const day = planData.days.find(d => d.day.day_number === dayNumber.value)
            if (day) {
              workoutDay.value = day
              calculateWorkoutStats(day)
            }
          }
        } catch (error) {
          console.error('Error fetching workout data:', error)
          // Fallback data
          workoutDay.value = {
            day_number: dayNumber.value,
            title: `Day ${dayNumber.value}`,
            exercises: [
              { instance: { target_sets: 3, target_reps: 12 } },
              { instance: { target_sets: 3, target_reps: 14 } },
              { instance: { target_sets: 3, target_reps: 14 } },
              { instance: { target_sets: 3, target_reps: 12 } }
            ]
          }
          calculateWorkoutStats(workoutDay.value)
        }
      }
      
      const calculateWorkoutStats = (day) => {
        if (!day.exercises) return
        
        const totalExercises = day.exercises.length
        const totalSets = day.exercises.reduce((sum, ex) => sum + (ex.instance.target_sets || 3), 0)
        const totalReps = day.exercises.reduce((sum, ex) => sum + (ex.instance.target_reps || 10), 0)
        
        workoutStats.value = {
          totalExercises,
          totalTime: Math.ceil(totalExercises * 2.5), // ~2.5 min per exercise
          totalCalories: Math.round(totalExercises * 8.9), // ~8.9 calories per exercise
          successRate: 100
        }
      }
      
      const fetchProgressData = async () => {
        try {
          const response = await fetch(`http://localhost:8000/users/${userStore.userProfile.id}/progress?days=7`)
          if (response.ok) {
            const data = await response.json()
            progressData.value.weeklyProgress = data.total_sessions || 0
          }
        } catch (error) {
          console.error('Error fetching progress data:', error)
          // Increment weekly progress for demo
          progressData.value.weeklyProgress = Math.min(progressData.value.weeklyProgress + 1, progressData.value.weeklyGoal)
        }
      }
      
      const continueToNextDay = () => {
        const nextDay = dayNumber.value + 1
        router.push({
          name: 'WorkoutOverview',
          params: { 
            planId: planId.value,
            dayNumber: nextDay
          }
        })
      }
      
      const goToDashboard = () => {
        router.push('/dashboard')
      }
      
      const shareWorkout = () => {
        // Share functionality - could integrate with social media APIs
        if (navigator.share) {
          navigator.share({
            title: 'Workout Completed!',
            text: `I just completed ${workoutDay.value.title} on LEAPFITNESS! 💪`,
            url: window.location.origin
          })
        } else {
          // Fallback - copy to clipboard
          navigator.clipboard.writeText(`I just completed ${workoutDay.value.title} on LEAPFITNESS! 💪`)
          alert('Achievement copied to clipboard!')
        }
      }
      
      // Initialize
      onMounted(() => {
        planId.value = parseInt(route.params.planId)
        dayNumber.value = parseInt(route.params.dayNumber)
        fetchWorkoutData()
        fetchProgressData()
      })
      
      return {
        workoutDay,
        workoutStats,
        progressData,
        continueToNextDay,
        goToDashboard,
        shareWorkout
      }
    }
  }
  </script>
  
  <style scoped>
  /* Additional custom styles if needed */
  .btn {
    @apply transition-all duration-200 ease-in-out;
  }
  </style>
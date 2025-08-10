<template>
  <div class="min-h-screen bg-white relative overflow-hidden">
    <!-- Status Bar -->
    <div class="flex justify-between items-center px-6 pt-3 pb-2 text-black text-sm font-medium">
      <span>10:57</span>
      <div class="flex items-center space-x-1">
        <span class="text-xs">0.13 KB/s</span>
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M2 17h20v2H2zm1.15-4.05L4 11.47l.85 1.48L3 14.42l2.75 1.78L6.6 14.75l1.85 1.28L9 14.28zm5.75-7.5L8 7.03 8.85 8.51 8 9.97 10.75 11.75 11.6 10.25 13.45 11.53 14 9.78zm8.1 2.5L16 7.03 16.85 8.51 16 9.97 18.75 11.75 19.6 10.25 21.45 11.53 22 9.78z"/>
        </svg>
        <span class="bg-black text-white px-1 rounded text-xs">88</span>
      </div>
    </div>

    <!-- Slides Container -->
    <div class="relative h-screen">
      <!-- Slide 1: Workspace -->
      <div 
        v-show="currentSlide === 0"
        class="absolute inset-0 transition-all duration-700 ease-in-out"
        :class="currentSlide === 0 ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'"
      >
        <div class="h-2/3 bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center relative overflow-hidden">
          <!-- Mock workspace image -->
          <div class="absolute inset-0 bg-gradient-to-br from-blue-50 to-purple-50"></div>
          <div class="relative z-10 text-center">
            <div class="w-32 h-24 bg-gray-300 rounded-lg mx-auto mb-4 flex items-center justify-center shadow-lg">
              <svg class="w-16 h-16 text-gray-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20 3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h3l-1 1v2h12v-2l-1-1h3c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 13H4V5h16v11z"/>
              </svg>
            </div>
            <div class="w-16 h-16 bg-amber-200 rounded-full mx-auto shadow-md"></div>
          </div>
          <div class="absolute top-4 right-4 w-8 h-8 bg-gray-400 rounded-full"></div>
          <div class="absolute bottom-8 left-8 w-4 h-4 bg-gray-500 rounded-sm"></div>
        </div>
        <div class="h-1/3 bg-white px-8 pt-12 pb-8">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">Work Out Anywhere</h2>
          <p class="text-lg text-gray-600 leading-relaxed">Transform any space into your personal gym. Whether at home, office, or traveling.</p>
        </div>
      </div>

      <!-- Slide 2: Bedroom -->
      <div 
        v-show="currentSlide === 1"
        class="absolute inset-0 transition-all duration-700 ease-in-out"
        :class="currentSlide === 1 ? 'translate-x-0 opacity-100' : currentSlide < 1 ? 'translate-x-full opacity-0' : '-translate-x-full opacity-0'"
      >
        <div class="h-2/3 bg-gradient-to-br from-amber-100 to-orange-100 flex items-center justify-center relative overflow-hidden">
          <!-- Mock bedroom image -->
          <div class="absolute inset-0 bg-gradient-to-br from-amber-50 to-orange-50"></div>
          <div class="relative z-10">
            <div class="w-48 h-32 bg-amber-200 rounded-lg mx-auto mb-4 shadow-lg relative">
              <div class="absolute top-2 left-2 w-8 h-8 bg-amber-300 rounded-full"></div>
              <div class="absolute top-2 right-2 w-8 h-8 bg-amber-300 rounded-full"></div>
              <div class="absolute bottom-0 left-0 right-0 h-16 bg-amber-300 rounded-b-lg"></div>
            </div>
          </div>
          <div class="absolute top-6 right-6 w-12 h-12 bg-amber-300 rounded-full"></div>
          <div class="absolute bottom-4 left-4 w-6 h-12 bg-amber-400 rounded-full"></div>
        </div>
        <div class="h-1/3 bg-white px-8 pt-12 pb-8">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">Morning Routines</h2>
          <p class="text-lg text-gray-600 leading-relaxed">Start your day right with guided morning workouts. Just 6 minutes to energize your body.</p>
        </div>
      </div>

      <!-- Slide 3: Outdoor -->
      <div 
        v-show="currentSlide === 2"
        class="absolute inset-0 transition-all duration-700 ease-in-out"
        :class="currentSlide === 2 ? 'translate-x-0 opacity-100' : currentSlide < 2 ? 'translate-x-full opacity-0' : '-translate-x-full opacity-0'"
      >
        <div class="h-2/3 bg-gradient-to-br from-green-200 to-teal-200 flex items-center justify-center relative overflow-hidden">
          <!-- Mock outdoor image -->
          <div class="absolute inset-0 bg-gradient-to-br from-green-100 to-teal-100"></div>
          <div class="relative z-10">
            <div class="w-40 h-24 bg-green-500 rounded-lg mx-auto mb-4 shadow-lg relative">
              <div class="absolute -top-2 left-4 w-8 h-16 bg-green-600 rounded-t-full"></div>
              <div class="absolute -top-1 right-8 w-6 h-12 bg-green-600 rounded-t-full"></div>
              <div class="absolute top-2 left-1/2 transform -translate-x-1/2 w-16 h-12 bg-teal-500 rounded-full"></div>
            </div>
          </div>
          <div class="absolute top-8 left-8 w-16 h-8 bg-green-400 rounded-full opacity-60"></div>
          <div class="absolute bottom-8 right-8 w-12 h-12 bg-teal-400 rounded-full opacity-60"></div>
        </div>
        <div class="h-1/3 bg-white px-8 pt-12 pb-8">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">Outdoor Adventures</h2>
          <p class="text-lg text-gray-600 leading-relaxed">Take your fitness journey outdoors. AI coaching adapts to any environment, anytime.</p>
        </div>
      </div>

      <!-- Slide 4: Final/App Intro -->
      <div 
        v-show="currentSlide === 3"
        class="absolute inset-0 transition-all duration-700 ease-in-out"
        :class="currentSlide === 3 ? 'translate-x-0 opacity-100' : '-translate-x-full opacity-0'"
      >
        <div class="h-2/3 bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center relative overflow-hidden">
          <!-- Mock bathroom/clean space -->
          <div class="absolute inset-0 bg-gradient-to-br from-indigo-50 to-purple-50"></div>
          <div class="relative z-10">
            <div class="w-32 h-20 bg-white rounded-lg mx-auto mb-4 shadow-lg relative border-2 border-gray-200">
              <div class="absolute top-2 right-2 w-4 h-4 bg-indigo-300 rounded-full"></div>
              <div class="absolute bottom-2 left-2 right-2 h-8 bg-gray-100 rounded"></div>
            </div>
            <div class="w-24 h-24 bg-indigo-200 rounded-full mx-auto shadow-md flex items-center justify-center">
              <svg class="w-12 h-12 text-indigo-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              </svg>
            </div>
          </div>
          <div class="absolute top-6 left-6 w-8 h-16 bg-indigo-300 rounded-full"></div>
          <div class="absolute bottom-6 right-6 w-6 h-6 bg-purple-300 rounded-full"></div>
        </div>
        <div class="h-1/3 bg-white px-8 pt-12 pb-8">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">Fast & Convenient</h2>
          <p class="text-lg text-gray-600 leading-relaxed">Just 6 minutes each time. Sculpt your body anytime, anywhere with AI-powered coaching.</p>
        </div>
      </div>
    </div>

    <!-- Bottom Section -->
    <div class="absolute bottom-0 left-0 right-0 bg-white px-8 pb-8">
      <!-- Progress Indicators -->
      <div class="flex justify-center space-x-2 mb-8">
        <div 
          v-for="(slide, index) in slides" 
          :key="index"
          class="w-2 h-2 rounded-full transition-all duration-300"
          :class="currentSlide === index ? 'bg-gray-800 w-8' : 'bg-gray-300'"
        ></div>
      </div>
      
      <!-- Continue Button -->
      <button 
        @click="currentSlide < 3 ? nextSlide() : getStarted()"
        class="w-full bg-gray-900 text-white py-4 rounded-2xl text-lg font-semibold transition-all duration-200 hover:bg-gray-800 active:scale-[0.98]"
      >
        {{ currentSlide < 3 ? 'Continue' : 'Get Started' }}
      </button>
      
      <!-- Skip Button -->
      <button 
        v-if="currentSlide < 3"
        @click="getStarted"
        class="w-full text-gray-500 py-3 mt-2 text-base"
      >
        Skip
      </button>
    </div>

    <!-- Swipe Areas (for mobile) -->
    <div 
      @touchstart="handleTouchStart"
      @touchend="handleTouchEnd"
      @click="nextSlide"
      class="absolute inset-0 z-10"
      style="pointer-events: auto;"
    ></div>
  </div>
</template>

<script>
export default {
  name: 'WelcomePage',
  data() {
    return {
      currentSlide: 0,
      slides: [
        { title: 'Work Out Anywhere', description: 'Transform any space into your personal gym' },
        { title: 'Morning Routines', description: 'Start your day right with guided workouts' },
        { title: 'Outdoor Adventures', description: 'Take your fitness journey outdoors' },
        { title: 'Fast & Convenient', description: 'Just 6 minutes each time' }
      ],
      touchStartX: 0,
      touchEndX: 0
    }
  },
  methods: {
    nextSlide() {
      if (this.currentSlide < 3) {
        this.currentSlide++
      } else {
        this.getStarted()
      }
    },
    prevSlide() {
      if (this.currentSlide > 0) {
        this.currentSlide--
      }
    },
    getStarted() {
      this.$router.push('/sport-selection')
    },
    handleTouchStart(event) {
      this.touchStartX = event.changedTouches[0].screenX
    },
    handleTouchEnd(event) {
      this.touchEndX = event.changedTouches[0].screenX
      this.handleSwipe()
    },
    handleSwipe() {
      const swipeThreshold = 50
      const diff = this.touchStartX - this.touchEndX
      
      if (Math.abs(diff) > swipeThreshold) {
        if (diff > 0) {
          // Swipe left - next slide
          this.nextSlide()
        } else {
          // Swipe right - previous slide
          this.prevSlide()
        }
      }
    }
  },
  mounted() {
    // Auto-advance slides every 4 seconds (optional)
    // this.autoAdvance = setInterval(() => {
    //   if (this.currentSlide < 3) {
    //     this.nextSlide()
    //   }
    // }, 4000)
  },
  beforeUnmount() {
    if (this.autoAdvance) {
      clearInterval(this.autoAdvance)
    }
  }
}
</script>
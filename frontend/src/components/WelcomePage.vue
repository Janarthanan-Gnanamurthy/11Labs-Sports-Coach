<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
    <!-- Animated Background Particles -->
    <div class="absolute inset-0 overflow-hidden">
      <div 
        v-for="i in 20" 
        :key="i"
        class="absolute w-1 h-1 bg-white rounded-full animate-pulse opacity-20"
        :style="getParticleStyle(i)"
      ></div>
    </div>

    <!-- Main Content Container -->
    <div class="relative min-h-screen flex flex-col">
      
      <!-- Slides Container -->
      <div class="flex-1 relative overflow-hidden">
        <!-- Slide 0: Your Personal AI Coach (reverted) -->
        <div 
          v-show="currentSlide === 0"
          class="absolute inset-0 transition-all duration-700 ease-in-out flex flex-col"
          :class="getSlideClasses(0)"
        >
          <div class="flex-1 flex items-center justify-center p-4 sm:p-6 lg:p-8">
            <div class="text-center max-w-md w-full">
              <!-- Glassmorphic Card with Siri-like Animated Icon -->
              <div class="relative mb-8 flex flex-col items-center">
                <div class="glass-card p-8 rounded-3xl shadow-2xl border border-blue-400/30 relative overflow-hidden w-full">
                  <div class="absolute -inset-2 bg-gradient-to-br from-blue-400/30 via-purple-400/20 to-pink-400/10 blur-2xl opacity-60 animate-glow"></div>
                  <div class="relative flex flex-col items-center">
                    <!-- Animated Siri-like Icon -->
                    <div class="siri-glow mb-4">
                      <svg class="w-24 h-24 sm:w-28 sm:h-28" viewBox="0 0 64 64" fill="none">
                        <ellipse cx="32" cy="32" rx="28" ry="28" fill="url(#siriGradient2)"/>
                        <ellipse cx="32" cy="32" rx="20" ry="20" fill="url(#siriGradient3)" fill-opacity=".7"/>
                        <path d="M32 18c-7.732 0-14 6.268-14 14s6.268 14 14 14 14-6.268 14-14-6.268-14-14-14zm0 24c-5.523 0-10-4.477-10-10s4.477-10 10-10 10 4.477 10 10-4.477 10-10 10z" fill="#fff" fill-opacity=".3"/>
                        <defs>
                          <radialGradient id="siriGradient2" cx="0.5" cy="0.5" r="0.5" fx="0.5" fy="0.5">
                            <stop offset="0%" stop-color="#5ef1ff"/>
                            <stop offset="100%" stop-color="#7b61ff"/>
                          </radialGradient>
                          <radialGradient id="siriGradient3" cx="0.5" cy="0.5" r="0.5" fx="0.5" fy="0.5">
                            <stop offset="0%" stop-color="#fff"/>
                            <stop offset="100%" stop-color="#7b61ff"/>
                          </radialGradient>
                        </defs>
                      </svg>
                    </div>
                    <div class="flex space-x-2 mb-2">
                      <span class="inline-block px-3 py-1 bg-gradient-to-r from-purple-500/30 to-blue-500/30 text-purple-200 rounded-full text-xs font-semibold border border-purple-400/30 shadow">🎤 Conversational AI</span>
                      <span class="inline-block px-3 py-1 bg-gradient-to-r from-blue-500/30 to-cyan-500/30 text-blue-200 rounded-full text-xs font-semibold border border-blue-400/30 shadow">⚡ Real-time</span>
                    </div>
                    <h2 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-white mb-2 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent animate-fade-in-up">Your Personal AI Coach</h2>
                    <p class="text-base sm:text-lg text-gray-200 leading-relaxed px-2 animate-fade-in-up">Start a conversation with your AI coach for personalized guidance in running and gym workouts.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Slide 1: AI Call-Like Coaching -->
        <!-- Slide 4: Dynamic Plans & Analytics -->
        <div 
          v-show="currentSlide === 4"
          class="absolute inset-0 transition-all duration-700 ease-in-out flex flex-col"
          :class="getSlideClasses(4)"
        >
          <div class="flex-1 flex items-center justify-center p-4 sm:p-6 lg:p-8">
            <div class="text-center max-w-md w-full">
              <div class="relative mb-8 flex flex-col items-center">
                <div class="glass-card p-8 rounded-3xl shadow-2xl border border-cyan-400/30 relative overflow-hidden w-full">
                  <div class="absolute -inset-2 bg-gradient-to-br from-cyan-400/30 via-blue-400/20 to-emerald-400/10 blur-2xl opacity-60 animate-glow"></div>
                  <div class="relative flex flex-col items-center">
                    <div class="siri-glow mb-4">
                      <svg class="w-24 h-24 sm:w-28 sm:h-28" viewBox="0 0 64 64" fill="none">
                        <rect x="16" y="16" width="32" height="32" rx="16" fill="#5ef1ff" fill-opacity=".7"/>
                        <path d="M32 24v8M28 32h8" stroke="#fff" stroke-width="2" stroke-linecap="round"/>
                      </svg>
                    </div>
                    <div class="flex space-x-2 mb-2">
                      <span class="inline-block px-3 py-1 bg-gradient-to-r from-cyan-500/30 to-blue-500/30 text-cyan-200 rounded-full text-xs font-semibold border border-cyan-400/30 shadow">📈 Analytics</span>
                      <span class="inline-block px-3 py-1 bg-gradient-to-r from-blue-500/30 to-emerald-500/30 text-blue-200 rounded-full text-xs font-semibold border border-blue-400/30 shadow">🪄 Dynamic Plans</span>
                    </div>
                    <h2 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-white mb-2 bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent animate-fade-in-up">Personalized Progress</h2>
                    <p class="text-base sm:text-lg text-gray-200 leading-relaxed px-2 animate-fade-in-up">Track your stats, performance analytics on video feed,unlock badges, and get adaptive workout plans for running and gym</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Slide 5: Motivation & Inclusivity -->
        <div 
          v-show="currentSlide === 3"
          class="absolute inset-0 transition-all duration-700 ease-in-out flex flex-col"
          :class="getSlideClasses(3)"
        >
          <div class="flex-1 flex items-center justify-center p-4 sm:p-6 lg:p-8">
            <div class="text-center max-w-md w-full">
              <div class="relative mb-8 flex flex-col items-center">
                <div class="glass-card p-8 rounded-3xl shadow-2xl border border-pink-400/30 relative overflow-hidden w-full">
                  <div class="absolute -inset-2 bg-gradient-to-br from-pink-400/30 via-yellow-400/20 to-emerald-400/10 blur-2xl opacity-60 animate-glow"></div>
                  <div class="relative flex flex-col items-center">
                    <div class="siri-glow mb-4">
                      <svg class="w-24 h-24 sm:w-28 sm:h-28" viewBox="0 0 64 64" fill="none">
                        <ellipse cx="32" cy="32" rx="28" ry="28" fill="#fbbf24" fill-opacity=".3"/>
                        <path d="M32 44c6-2 10-8 10-14 0-6-4-12-10-14-6 2-10 8-10 14 0 6 4 12 10 14z" fill="#fff" fill-opacity=".7"/>
                        <path d="M24 32c0-4 4-8 8-8s8 4 8 8-4 8-8 8-8-4-8-8z" fill="#f472b6" fill-opacity=".7"/>
                      </svg>
                    </div>
                    <div class="flex space-x-2 mb-2">
                      <span class="inline-block px-3 py-1 bg-gradient-to-r from-pink-500/30 to-yellow-500/30 text-pink-200 rounded-full text-xs font-semibold border border-pink-400/30 shadow">💬 Motivation</span>
                      <span class="inline-block px-3 py-1 bg-gradient-to-r from-yellow-500/30 to-emerald-500/30 text-yellow-200 rounded-full text-xs font-semibold border border-yellow-400/30 shadow">🌈 Inclusive</span>
                    </div>
                    <h2 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-white mb-2 bg-gradient-to-r from-pink-400 to-yellow-400 bg-clip-text text-transparent animate-fade-in-up">Motivation & Support</h2>
                    <p class="text-base sm:text-lg text-gray-200 leading-relaxed px-2 animate-fade-in-up">Get real-time praise, humor, and inclusive advice and support for every gender, ability, and mood.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Slide 2: Smart Form Detection -->
        <div 
          v-show="currentSlide === 1"
          class="absolute inset-0 transition-all duration-700 ease-in-out flex flex-col"
          :class="getSlideClasses(1)"
        >
          <div class="flex-1 flex items-center justify-center p-4 sm:p-6 lg:p-8">
            <div class="text-center max-w-md w-full">
              <!-- Glassmorphic Card with Animated Pose Icon -->
              <div class="relative mb-8 flex flex-col items-center">
                <div class="glass-card p-8 rounded-3xl shadow-2xl border border-emerald-400/30 relative overflow-hidden w-full">
                  <div class="absolute -inset-2 bg-gradient-to-br from-emerald-400/30 via-teal-400/20 to-cyan-400/10 blur-2xl opacity-60 animate-glow"></div>
                  <div class="relative flex flex-col items-center">
                    <img src="/pose-detection.jpeg" alt="Pose Detection" class="w-24 h-24 sm:w-28 sm:h-28 rounded-2xl shadow-xl mb-4 object-cover border-4 border-emerald-400/40" />
                    <!-- Animated Human Pose Icon -->
                   
                    <div class="flex space-x-2 mb-2">
                      <span class="inline-block px-3 py-1 bg-gradient-to-r from-emerald-500/30 to-teal-500/30 text-emerald-200 rounded-full text-xs font-semibold border border-emerald-400/30 shadow">🧍‍♂️ Pose Detection</span>
                      <span class="inline-block px-3 py-1 bg-gradient-to-r from-teal-500/30 to-cyan-500/30 text-teal-200 rounded-full text-xs font-semibold border border-teal-400/30 shadow">⚡ Live Feedback</span>
                    </div>
                    <h2 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-white mb-2 bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent animate-fade-in-up">Smart Form Detection</h2>
                    <p class="text-base sm:text-lg text-gray-200 leading-relaxed px-2 animate-fade-in-up">Get instant feedback on your form and technique for safer, more effective workouts.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Slide 3: Level Up System -->
        <div 
          v-show="currentSlide === 2"
          class="absolute inset-0 transition-all duration-700 ease-in-out flex flex-col"
          :class="getSlideClasses(2)"
        >
          <div class="flex-1 flex items-center justify-center p-4 sm:p-6 lg:p-8">
            <div class="text-center max-w-md w-full">
              <!-- Glassmorphic Card with Animated Trophy Icon -->
              <div class="relative mb-8 flex flex-col items-center">
                <div class="glass-card p-8 rounded-3xl shadow-2xl border border-amber-400/30 relative overflow-hidden w-full">
                  <div class="absolute -inset-2 bg-gradient-to-br from-amber-400/30 via-orange-400/20 to-red-400/10 blur-2xl opacity-60 animate-glow"></div>
                  <div class="relative flex flex-col items-center">
                    <!-- Animated Trophy Icon -->
                    <div class="siri-glow mb-4">
                      <svg class="w-24 h-24 sm:w-28 sm:h-28" viewBox="0 0 64 64" fill="none">
                        <ellipse cx="32" cy="32" rx="28" ry="28" fill="url(#trophyGradient)"/>
                        <path d="M20 16v6a12 12 0 0024 0v-6h4a2 2 0 012 2v6a10 10 0 01-10 10h-2v6h4v6H24v-6h4v-6h-2A10 10 0 0116 24v-6a2 2 0 012-2h2zm24 0v6a8 8 0 01-16 0v-6h16z" fill="#fff" fill-opacity=".7"/>
                        <defs>
                          <radialGradient id="trophyGradient" cx="0.5" cy="0.5" r="0.5" fx="0.5" fy="0.5">
                            <stop offset="0%" stop-color="#ffe066"/>
                            <stop offset="100%" stop-color="#ff8800"/>
                          </radialGradient>
                        </defs>
                      </svg>
                    </div>
                    <div class="flex space-x-2 mb-2">
                      <span class="inline-block px-3 py-1 bg-gradient-to-r from-amber-500/30 to-orange-500/30 text-amber-700 rounded-full text-xs font-semibold border border-amber-400/30 shadow">🏆 Achievements</span>
                      <span class="inline-block px-3 py-1 bg-gradient-to-r from-orange-500/30 to-red-500/30 text-orange-700 rounded-full text-xs font-semibold border border-orange-400/30 shadow">🎁 Rewards</span>
                    </div>
                    <h2 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-white mb-2 bg-gradient-to-r from-amber-400 to-orange-400 bg-clip-text text-transparent animate-fade-in-up">Level Up Your Fitness</h2>
                    <p class="text-base sm:text-lg text-gray-200 leading-relaxed px-2 animate-fade-in-up">Track progress, earn achievements, and unlock new challenges as you grow stronger.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Slide 4: Get Started -->
        <div 
          v-show="currentSlide === 5"
          class="absolute inset-0 transition-all duration-700 ease-in-out flex flex-col"
          :class="getSlideClasses(5)"
        >
          <div class="flex-1 flex items-center justify-center p-4 sm:p-6 lg:p-8">
            <div class="text-center max-w-md w-full">
              <!-- Activity Grid -->
              <div class="grid grid-cols-2 gap-4 mb-6 sm:mb-8">
                <div class="bg-gradient-to-br from-indigo-500/20 to-purple-500/20 backdrop-blur-sm p-6 rounded-2xl border border-indigo-400/30 transform hover:scale-105 transition-all duration-300 flex flex-col items-center">
                  <svg class="w-10 h-10 sm:w-14 sm:h-14 text-indigo-400 mx-auto mb-1" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M13.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM9.8 8.9L7 23h2.1l1.8-8 2.1 2v6h2v-7.5l-2.1-2 .6-3C14.8 12 16.8 13 19 13v-2c-1.9 0-3.5-1-4.3-2.4l-1-1.6c-.4-.6-1-1-1.7-1-.3 0-.5.1-.8.1L6 8.3V13h2V9.6l1.8-.7"/>
                  </svg>
                  <span class="block text-sm sm:text-base font-semibold text-indigo-300">🏃‍♂️ Running</span>
                </div>
                <div class="bg-gradient-to-br from-violet-500/20 to-pink-500/20 backdrop-blur-sm p-6 rounded-2xl border border-violet-400/30 transform hover:scale-105 transition-all duration-300 flex flex-col items-center">
                  <svg class="w-10 h-10 sm:w-14 sm:h-14 text-violet-400 mx-auto mb-1" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20.57 14.86L22 13.43 20.57 12 17 15.57 8.43 7 12 3.43 10.57 2 9.14 3.43 7.71 2 5.57 4.14 4.14 2.71 2.71 4.14l1.43 1.43L2 7.71l1.43 1.43L2 10.57 3.43 12 7 8.43 15.57 17 12 20.57 13.43 22l1.43-1.43L16.29 22l2.14-2.14 1.43 1.43 1.43-1.43-1.43-1.43L22 16.29z"/>
                  </svg>
                  <span class="block text-sm sm:text-base font-semibold text-violet-300">💪 Gym</span>
                </div>
              </div>

              <div class="animate-fade-in-up" style="animation-delay: 0.5s">
                <h2 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-white mb-4 bg-gradient-to-r from-indigo-400 to-violet-400 bg-clip-text text-transparent">
                  Ready to Begin?
                </h2>
                <p class="text-base sm:text-lg text-gray-300 leading-relaxed px-2 mb-6">
                  Just 6 minutes each time. Sculpt your body anytime, anywhere with AI-powered coaching.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Fixed Section -->
      <div class="bg-black/20 backdrop-blur-md border-t border-white/10 p-4 sm:p-6 lg:p-8">
        <!-- Progress Indicators -->
        <div class="flex justify-center space-x-3 mb-6">
          <div 
            v-for="(slide, index) in slides" 
            :key="index"
            class="h-2 rounded-full transition-all duration-500 cursor-pointer"
            :class="currentSlide === index ? 'bg-gradient-to-r from-purple-400 to-pink-400 w-8 shadow-lg' : 'bg-white/30 w-2 hover:bg-white/50'"
            @click="goToSlide(index)"
          ></div>
        </div>
        
        <!-- Action Buttons -->
        <div class="space-y-3">
          <button 
            @click="currentSlide < 5 ? nextSlide() : getStarted()"
            class="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white py-4 rounded-2xl text-base sm:text-lg font-bold transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98] shadow-lg hover:shadow-xl"
          >
            {{ currentSlide < 5 ? 'Continue' : '🎮 Start Your Adventure' }}
          </button>
          
          <button 
            v-if="currentSlide < 5"
            @click="getStarted"
            class="w-full text-white/70 hover:text-white py-3 text-sm sm:text-base transition-all duration-200"
          >
            Skip Introduction
          </button>
        </div>
      </div>
    </div>

    <!-- Touch Interaction Areas -->
    <div 
      @touchstart="handleTouchStart"
      @touchend="handleTouchEnd"
      class="absolute inset-0 z-10 pointer-events-auto"
      @click="handleClick"
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
        { title: 'Meet Your Agents', description: 'Coach, Motivator, Twin Buddy, Wellness Guide' },
        { title: 'Conversational Coaching', description: 'Call-like AI sessions for real-time guidance' },
        { title: 'Smart Form Detection', description: 'Real-time feedback for better technique' },
        { title: 'Personalized Progress', description: 'Analytics and dynamic plans for you' },
        { title: 'Motivation & Support', description: 'Inclusive, motivational, and adaptive' },
        { title: 'Level Up Your Fitness', description: 'Gamified progress with achievements and rewards' },
      ],
      touchStartX: 0,
      touchEndX: 0,
      particles: []
    }
  },
  methods: {
    nextSlide() {
      if (this.currentSlide < this.slides.length - 1) {
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
    goToSlide(index) {
      this.currentSlide = index
    },
    getStarted() {
      // Add a celebratory effect before navigation
      this.showCelebration()
      setTimeout(() => {
        this.$router.push('/sport-selection')
      }, 1000)
    },
    showCelebration() {
      // Simple celebration effect - you can enhance this further
      const button = document.querySelector('button')
      if (button) {
        button.style.animation = 'pulse 0.5s ease-in-out'
      }
    },
    handleTouchStart(event) {
      this.touchStartX = event.changedTouches[0].screenX
    },
    handleTouchEnd(event) {
      this.touchEndX = event.changedTouches[0].screenX
      this.handleSwipe()
    },
    handleClick(event) {
      // Only advance on tap if not clicking progress indicators or buttons
      if (!event.target.closest('.bg-gradient-to-r') && !event.target.closest('[class*="cursor-pointer"]')) {
        this.nextSlide()
      }
    },
    handleSwipe() {
      const swipeThreshold = 50
      const diff = this.touchStartX - this.touchEndX
      
      if (Math.abs(diff) > swipeThreshold) {
        if (diff > 0) {
          this.nextSlide()
        } else {
          this.prevSlide()
        }
      }
    },
    getSlideClasses(slideIndex) {
      if (this.currentSlide === slideIndex) {
        return 'translate-x-0 opacity-100'
      } else if (this.currentSlide > slideIndex) {
        return '-translate-x-full opacity-0'
      } else {
        return 'translate-x-full opacity-0'
      }
    },
    getParticleStyle(index) {
      return {
        left: Math.random() * 100 + '%',
        top: Math.random() * 100 + '%',
        animationDelay: Math.random() * 3 + 's',
        animationDuration: (Math.random() * 3 + 2) + 's'
      }
    }
  },
  mounted() {
    // Initialize particles for background animation
    this.particles = Array.from({ length: 20 }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      delay: Math.random() * 3
    }))
  }
}
</script>

<style scoped>
@keyframes bounce-slow {
  0%, 20%, 53%, 80%, 100% {
    transform: translate3d(0,0,0);
  }
  40%, 43% {
    transform: translate3d(0, -15px, 0);
  }
  70% {
    transform: translate3d(0, -8px, 0);
  }
  90% {
    transform: translate3d(0, -3px, 0);
  }
}

@keyframes wiggle {
  0% { transform: rotate(0deg); }
  25% { transform: rotate(5deg); }
  50% { transform: rotate(0deg); }
  75% { transform: rotate(-5deg); }
  100% { transform: rotate(0deg); }
}

@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse-strong {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.animate-bounce-slow {
  animation: bounce-slow 2s infinite;
}

.animate-wiggle {
  animation: wiggle 1s ease-in-out infinite;
}

.animate-fade-in-up {
  animation: fade-in-up 0.6s ease-out forwards;
  opacity: 0;
}

.animate-pulse-strong {
  animation: pulse-strong 2s ease-in-out infinite;
}

/* Custom scrollbar for webkit browsers */
::-webkit-scrollbar {
  display: none;
}

/* Ensure smooth transitions on all interactive elements */
* {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter;
  transition-duration: 200ms;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
/* Glassmorphic card and Siri-glow animation */
.glass-card {
  background: rgba(30, 41, 59, 0.7);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 1.5rem;
  border: 1px solid rgba(255,255,255,0.12);
}
.siri-glow {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
.siri-glow svg {
  filter: drop-shadow(0 0 16px #7b61ff88) drop-shadow(0 0 32px #5ef1ff44);
  animation: siri-pulse 2.5s infinite alternate;
}
@keyframes siri-pulse {
  0% { filter: drop-shadow(0 0 8px #7b61ff88) drop-shadow(0 0 16px #5ef1ff44); }
  100% { filter: drop-shadow(0 0 32px #7b61ffcc) drop-shadow(0 0 48px #5ef1ff88); }
}
.animate-glow {
  animation: glow-bg 4s ease-in-out infinite alternate;
}
@keyframes glow-bg {
  0% { opacity: 0.4; }
  100% { opacity: 0.7; }
}
</style>
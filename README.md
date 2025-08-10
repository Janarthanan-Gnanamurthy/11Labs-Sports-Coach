# 11Labs 2.0 Frontend

A Vue.js fitness application with AI coaching capabilities, featuring proper routing and state management.

## Architecture

### Routing Structure
The application now uses Vue Router instead of component switching:

- `/` - Welcome page with onboarding slides
- `/sport-selection` - Choose your preferred sport/activity
- `/agent-selection` - Select your AI coach personality
- `/session-setup` - Configure workout session parameters
- `/live-coaching` - Active AI coaching session
- `/dashboard` - Progress tracking and session history
- `/settings` - User profile and preferences

### State Management
Uses Pinia for centralized state management with the `useUserStore`:

#### User Store Features:
- **User Profile**: Name, email, fitness preferences
- **Session Data**: Sport selection, agent choice, workout parameters
- **Session History**: Track completed workouts with metrics
- **Navigation State**: Current route tracking
- **Computed Properties**: Weekly stats, recent sessions, progress calculations

#### Key Store Methods:
- `setUserProfile()` - Update user information
- `setSelectedSport()` - Set chosen activity
- `setSelectedAgent()` - Set AI coach preference
- `addSessionToHistory()` - Save completed workout
- `resetUserData()` - Clear all user data

## Features

### AI Coaching
- ElevenLabs integration for voice coaching
- Multiple coach personalities (Coach, Motivator, Buddy, Wellness Guide)
- Real-time pose detection and feedback
- Session customization (duration, intensity, mood)

### Progress Tracking
- Session completion tracking
- Weekly statistics
- Achievement system
- Historical workout data

### User Experience
- Responsive design with Tailwind CSS
- Smooth navigation between routes
- Persistent state across sessions
- Back button navigation

## Development

### Prerequisites
- Node.js 16+
- npm or yarn

### Setup
```bash
cd frontend
npm install
npm run dev
```

### Build
```bash
npm run build
```

## Technology Stack

- **Vue 3** - Progressive JavaScript framework
- **Vue Router 4** - Official router for Vue.js
- **Pinia** - Intuitive, type safe store for Vue
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Next generation frontend tooling

## Component Structure

All components now use the Composition API with `<script setup>` syntax and integrate with the user store for state management and Vue Router for navigation.

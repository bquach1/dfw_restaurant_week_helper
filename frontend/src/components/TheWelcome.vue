<script setup>
const features = [
  {
    name: 'Restaurant List',
    route: '/restaurants',
    description: 'Browse all participating restaurants.',
  },
  {
    name: 'Recommender',
    route: '/recommender',
    description: 'Get personalized restaurant recommendations.',
  },
  {
    name: 'My Profile',
    route: '/profile',
    description: 'View and edit your preferences.',
  },
]
</script>

<template>
  <div class="feature-list">
    <div v-for="feature in features" :key="feature.route">
      <router-link :to="feature.route">
        <strong>{{ feature.name }}</strong>
      </router-link>
      <span> - {{ feature.description }}</span>
    </div>
  </div>
</template>

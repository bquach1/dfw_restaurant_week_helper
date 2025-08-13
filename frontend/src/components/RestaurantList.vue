<script setup>
import { ref } from 'vue'

const restaurantName = ref('')
const loading = ref(false)

const fetchRestaurantInfo = async () => {
  if (!restaurantName.value) return
  loading.value = true
  console.log(`Fetching info for restaurant: ${restaurantName.value}`)
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/restaurants/google_places/?name=${restaurantName.value}`,
    )
    console.log(response.json())
  } catch (error) {
    console.error('Error fetching restaurant info:', error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="restaurant-list">
    <h2>Restaurant Finder</h2>
    <input
      v-model="restaurantName"
      type="text"
      placeholder="Enter restaurant name"
      @keyup.enter="fetchRestaurantInfo"
    />
    <button @click="fetchRestaurantInfo" :disabled="loading">Search</button>
  </div>
</template>

<style scoped>
.restaurant-list {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1rem;
  background: black;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
h2 {
  margin-bottom: 1rem;
}
input {
  margin-right: 1rem;
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ccc;
}
button {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  border: none;
  background: #007bff;
  color: #fff;
  cursor: pointer;
}
button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>

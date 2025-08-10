import { createRouter, createWebHistory } from 'vue-router'
import RestaurantList from '../components/RestaurantList.vue'
import Recommender from '../components/RecommendationPage.vue'
import MyProfile from '../components/MyProfile.vue'
import TheWelcome from '../components/TheWelcome.vue'

const routes = [
  { path: '/', component: TheWelcome },
  { path: '/restaurants', component: RestaurantList },
  { path: '/recommender', component: Recommender },
  { path: '/profile', component: MyProfile },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

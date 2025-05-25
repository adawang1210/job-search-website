import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProfileView from '../views/ProfileView.vue'
import CompanyView from '../views/CompanyView.vue'
import NotificationView from '../views/NotificationView.vue'
import SearchResultView from '../views/SearchResultView.vue'
import FavoriteJobsView from '../views/FavoriteJobsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      alias: '/home'
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },
    {
      path: '/company',
      name: 'company',
      alias: '/company',
      component: CompanyView,
    },
    {
      path: '/notification',
      name: 'notification',
      component: NotificationView,
    },
    {
      path: '/searchresult',
      name: 'searchresult',
      component: SearchResultView,
      // props: route => ({ query: route.query.q }) // 如果想透過 props 傳遞查詢參數
    },
  ],
})

export default router

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProfileView from '../views/ProfileView.vue'
import CompanyView from '../views/CompanyView.vue'
import NotificationView from '../views/NotificationView.vue'
import SearchResultView from '../views/SearchResultView.vue'
import FavoriteJobsView from '../views/FavoriteJobsView.vue'
import AllCompanyView from '../views/AllCompanyView.vue'
import JobDetailView from '@/views/JobDetailView.vue'

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
      path: '/company/:id', 
      name: 'company',
      component: CompanyView,
      props: true,
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
    },
    {
      path: '/favoritejobs/:id',
      name: 'favoritejobs',
      component: FavoriteJobsView,
      props: true,
    },
    {
      path: '/allcompany',
      name: 'AllCompany',
      component: AllCompanyView
    },
    {
      path: '/jobdetail/:id',
      name: 'jobdetail',
      component: JobDetailView,
      props: true,
    },
  ],
})

export default router
import { createRouter, createWebHistory } from 'vue-router';

// 引入您的視圖 (View) 組件
import HomeView from '../views/HomeView.vue';
import ProfileView from '../views/ProfileView.vue';
import CompanyView from '../views/CompanyView.vue';
import NotificationView from '../views/NotificationView.vue';
import SearchResultView from '../views/SearchResultView.vue'; // 確保這是您 SearchResult 組件的正確名稱和路徑

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Home', // 建議使用帕斯卡命名法 (PascalCase)
    component: HomeView,
    // alias: '/home' // 通常可以移除，除非有特定向後兼容需求
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView,
  },
  {
    path: '/company',
    name: 'Company',
    component: CompanyView,
    // alias: '/company' // 通常可以移除
  },
  {
    path: '/notification',
    name: 'Notification',
    component: NotificationView,
  },
  {
    path: '/search', // **統一路徑為 /search**
    name: 'SearchResult', // **統一名稱為 SearchResult**
    component: SearchResultView,
  },
  // 您可以在此處添加其他頂層路由，例如 404 頁面
  // {
  //   path: '/:pathMatch(.*)*', // 匹配所有未定義的路徑
  //   name: 'NotFound',
  //   component: () => import('../views/NotFoundView.vue') // 假設您有一個 NotFoundView
  // }
];

// 創建路由實例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // 確保與您的專案構建工具匹配 (Vite 用 import.meta.env)
  routes, // ES6 縮寫，相當於 routes: routes
  scrollBehavior(to, from, savedPosition) {
    // 頁面跳轉後滾動到頂部行為
    if (savedPosition) {
      return savedPosition; // 如果是瀏覽器的前進/後退，則恢復之前保存的滾動位置
    } else {
      return { top: 0 }; // 否則滾動到頁面頂部
    }
  }
});

export default router;
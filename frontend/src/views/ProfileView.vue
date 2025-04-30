<template>
  <div class="profile">
    <Navbar />
    <LeftSidebar />
    <MainPanel>
      <h1>個人頁面</h1>
      <div class="profile-content">
        <!-- 個人資訊區塊 -->
        <div class="profile-info">
          <h2>基本資料</h2>
          <!-- 這裡放個人資料表單 -->
        </div>

        <!-- 履歷區塊 -->
        <div class="resume-section">
          <h2>我的履歷</h2>
          <!-- 這裡放履歷列表 -->
        </div>

        <!-- 申請記錄區塊 -->
        <div class="application-section">
          <h2>申請記錄</h2>
          <!-- 這裡放申請記錄列表 -->
        </div>
      </div>
    </MainPanel>
    <RightSidebar />
  </div>
</template>

<script>
import Navbar from '@/components/layout/Navbar.vue'
import LeftSidebar from '@/components/layout/LeftSidebar.vue'
import MainPanel from '@/components/layout/MainPanel.vue'
import RightSidebar from '@/components/layout/RightSidebar.vue'

export default {
  name: 'ProfileView',
  components: {
    Navbar,
    LeftSidebar,
    MainPanel,
    RightSidebar
  },
  data() {
    return {
      // 這裡放資料
    }
  },
  methods: {
    // 這裡放方法
  }
}
</script>

<style scoped>
.profile {
  min-height: 100vh;
  background-color: #121212;
}

.profile-content {
  max-width: 1200px;
  margin: 0 auto;
}

.profile-info,
.resume-section,
.application-section {
  margin-bottom: 30px;
  padding: 20px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style> 
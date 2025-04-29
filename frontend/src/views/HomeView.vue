<script>
export default {
  name: 'HomeView',
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

<template>
  <div class="home">
    <div class="hero-section">
      <h1>歡迎來到求職網站</h1>
      <p>找到你的理想工作，或是找到理想的人才</p>
    </div>

    <div class="search-section">
      <h2>職位搜尋</h2>
      <!-- 這裡放搜尋表單 -->
    </div>

    <div class="job-listings">
      <h2>熱門職位</h2>
      <!-- 這裡放職位列表 -->
    </div>

    <div class="company-listings">
      <h2>熱門公司</h2>
      <!-- 這裡放公司列表 -->
    </div>
  </div>
</template>

<style scoped>
.home {
  padding: 20px;
}

.hero-section {
  text-align: center;
  padding: 40px;
  background-color: #f5f5f5;
  border-radius: 8px;
  margin-bottom: 30px;
}

.search-section,
.job-listings,
.company-listings {
  max-width: 1200px;
  margin: 0 auto 30px;
  padding: 20px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>

<script>
import BaseLayout from '@/components/layout/BaseLayout.vue'
import Home from '@/components/main-panel/Home.vue'

export default {
  name: 'HomeView',
  components: {
    BaseLayout,
    Home,
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

<template>
  <BaseLayout>
    <Home>
      
    </Home>
  </BaseLayout>
</template>

<style scoped>
.home {
  min-height: 100vh;
  background-color: #121212;
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

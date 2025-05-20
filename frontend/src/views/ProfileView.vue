<template>
  <BaseLayout>
    <Profile>
      
    </Profile>
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/layout/BaseLayout.vue'
import Profile from '@/components/main-panel/Profile.vue'

export default {
  name: 'ProfileView',
  components: {
    BaseLayout,
    Profile,
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
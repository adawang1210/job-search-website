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
    <Home />
  </BaseLayout>
</template>

<style scoped>
/* 只保留最基本的容器样式 */
.home {
  width: 100%;
  min-height: 100vh;
  background-color: #121212;
}
</style>

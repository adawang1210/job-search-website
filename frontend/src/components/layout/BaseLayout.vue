<template>
  <div class="layout">
    <Navbar />
    <div class="content">
      <LeftSidebar />
      <MainPanel>
        <slot></slot>
      </MainPanel>
      <RightSidebar />
    </div>
  </div>
</template>

<script>
import Navbar from './Navbar.vue'
import LeftSidebar from './LeftSidebar.vue'
import RightSidebar from './RightSidebar.vue'
import MainPanel from './MainPanel.vue'

export default {
  name: 'BaseLayout',
  components: {
    Navbar,
    LeftSidebar,
    RightSidebar,
    MainPanel
  }
}
</script>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.content {
  display: flex;
  flex: 1;
  overflow: hidden;
}
</style> 
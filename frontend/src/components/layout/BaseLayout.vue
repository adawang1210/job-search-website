<!--將頁面分為上下結構（layout），並將navbar、leftsidebar、rightsidebar、mainpanel、slot（內容）分開-->
<template>
  <div class="layout">
    <Navbar />
    <div class="content">
      <LeftSidebar />
      <div class="main-panel">
        <slot></slot>
      </div>
      <RightSidebar />
    </div>
  </div>
</template>

<script>
import Navbar from './Navbar.vue'
import LeftSidebar from './LeftSidebar.vue'
import RightSidebar from './RightSidebar.vue'

export default {
  name: 'BaseLayout',
  components: {
    Navbar,
    LeftSidebar,
    RightSidebar
  }
}
</script>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  padding-top: 56px; /* Navbar的高度 */
}

.content {
  display: flex;
  flex: 1;
  overflow: hidden;
  position: relative;
  width: 100%;
  padding-left: 272px; /* LeftSidebar的宽度(240px) + 左右padding(32px) */
  box-sizing: border-box;
}

.main-panel {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style> 
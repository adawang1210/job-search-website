<template>
  <main class="main-panel">
    <slot></slot>
  </main>
</template>

<script>
export default {
  name: 'MainPanel'
}
</script>

<style scoped>
.main-panel {
  flex: 1;
  background-color: #121212;
  margin-left: 240px; /* 左側邊欄寬度 */
  margin-right: 300px; /* 右側邊欄寬度 */
  margin-top: 60px; /* 頂部導航欄高度 */
  padding: 20px;
  min-height: calc(100vh - 60px);
  overflow-y: auto;
}
</style> 
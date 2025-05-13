<template>
  <div class="right-side-bar"></div>
</template>

<script>
export default {
  name: 'RightSidebar'
}
</script>

<style scoped>
.right-side-bar {
  width: 240px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: stretch;
  box-sizing: border-box;
  background-color: #383333;
  border-radius: 10px;
  height: calc(100vh - 72px); /* 減去Navbar高度(56px)和padding(16px) */
  flex-shrink: 0;
  position: fixed;
  right: 16px;
  margin-top: 16px;
  overflow-y: auto;
  /* 你可以根據需要加上滾動條樣式 */
}
</style> 
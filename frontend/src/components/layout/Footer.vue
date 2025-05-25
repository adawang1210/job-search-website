<template>
  <footer class="footer-in-panel">
    <div class="footer-content">
      <p>&copy; {{ currentYear }} Your Company. All Rights Reserved.</p>
      </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer',
  data() {
    return {
      currentYear: new Date().getFullYear()
    };
  }
}
</script>

<style scoped>
.footer-in-panel {
  padding: 20px 15px; /* Footer 內邊距 */
  background-color: #2a2a2a; /* Footer 背景色，可自訂以匹配您的設計 */
  color: #a0a0a0; /* Footer 文字顏色 */
  text-align: center;
  border-top: 1px solid #444; /* Footer 頂部分隔線 */
  flex-shrink: 0; /* 防止在 flex 佈局中被壓縮 */
  margin-top: auto; /* 這個通常用在希望 footer 填滿剩餘空間的情況，但在滾動內容末尾可能不需要 */
}

.footer-content {
  max-width: 900px; /* 可選：限制內容寬度 */
  margin: 0 auto;
}
</style>
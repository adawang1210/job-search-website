<template>
  <aside class="right-sidebar">
    <div class="sidebar-header">
      <h3>相關職位</h3>
    </div>
    <div class="related-jobs">
      <!-- 這裡可以放相關職位列表 -->
      <div class="job-card" v-for="i in 5" :key="i">
        <div class="job-info">
          <h4>職位名稱 {{ i }}</h4>
          <p>公司名稱</p>
        </div>
        <button class="save-button">
          <i class="fas fa-bookmark"></i>
        </button>
      </div>
    </div>
  </aside>
</template>

<script>
export default {
  name: 'RightSidebar'
}
</script>

<style scoped>
.right-sidebar {
  width: 300px;
  background-color: #121212;
  padding: 20px;
  height: 100%;
  position: fixed;
  right: 0;
  top: 60px; /* 與navbar高度相同 */
  bottom: 0;
  overflow-y: auto;
}

.sidebar-header {
  margin-bottom: 20px;
}

.sidebar-header h3 {
  color: white;
  font-size: 16px;
}

.related-jobs {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.job-card {
  background-color: #282828;
  padding: 15px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.job-card:hover {
  background-color: #404040;
}

.job-info h4 {
  color: white;
  margin: 0;
  font-size: 14px;
}

.job-info p {
  color: #b3b3b3;
  margin: 5px 0 0;
  font-size: 12px;
}

.save-button {
  background: none;
  border: none;
  color: #b3b3b3;
  cursor: pointer;
  padding: 5px;
}

.save-button:hover {
  color: white;
}
</style> 
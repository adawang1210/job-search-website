<template>
  <aside class="left-sidebar">
    <div class="logo">
      <img src="@/assets/logo.svg" alt="Logo">
    </div>
    <nav class="main-nav">
      <router-link to="/" class="nav-item">
        <i class="fas fa-home"></i>
        <span>首頁</span>
      </router-link>
      <router-link to="/search" class="nav-item">
        <i class="fas fa-search"></i>
        <span>搜尋</span>
      </router-link>
      <router-link to="/profile" class="nav-item">
        <i class="fas fa-user"></i>
        <span>個人頁面</span>
      </router-link>
      <router-link to="/company" class="nav-item">
        <i class="fas fa-building"></i>
        <span>公司頁面</span>
      </router-link>
    </nav>
    <div class="playlist-section">
      <div class="playlist-header">
        <h3>我的收藏</h3>
        <button class="add-button">
          <i class="fas fa-plus"></i>
        </button>
      </div>
      <div class="playlist-list">
        <!-- 這裡可以放收藏的職位或公司列表 -->
      </div>
    </div>
  </aside>
</template>

<script>
export default {
  name: 'LeftSidebar'
}
</script>

<style scoped>
.left-sidebar {
  width: 240px;
  background-color: #000;
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 60px; /* 與navbar高度相同 */
  bottom: 0;
}

.logo {
  margin-bottom: 20px;
}

.logo img {
  width: 120px;
}

.main-nav {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.nav-item {
  color: #b3b3b3;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-item:hover {
  color: white;
  background-color: #282828;
}

.nav-item.router-link-active {
  color: white;
  background-color: #282828;
}

.playlist-section {
  margin-top: auto;
}

.playlist-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.playlist-header h3 {
  color: #b3b3b3;
  font-size: 14px;
  text-transform: uppercase;
}

.add-button {
  background: none;
  border: none;
  color: #b3b3b3;
  cursor: pointer;
}

.playlist-list {
  max-height: 200px;
  overflow-y: auto;
}
</style> 
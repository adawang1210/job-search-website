<template>
  <nav class="navbar">
    <div class="navbar-left">
      <div class="nav-buttons">
        <button class="nav-button">
          <i class="fas fa-chevron-left"></i>
        </button>
        <button class="nav-button">
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>
    <div class="navbar-right">
      <div class="search-bar">
        <i class="fas fa-search"></i>
        <input type="text" placeholder="搜尋...">
      </div>
      <div class="user-menu">
        <button class="user-button">
          <i class="fas fa-user"></i>
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar'
}
</script>

<style scoped>
.navbar {
  height: 60px;
  background-color: #000;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
}

.nav-buttons {
  display: flex;
  gap: 10px;
}

.nav-button {
  background-color: rgba(0, 0, 0, 0.7);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.search-bar {
  background-color: white;
  border-radius: 20px;
  padding: 8px 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-bar input {
  border: none;
  outline: none;
  width: 200px;
}

.user-button {
  background-color: #282828;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style> 
<template>
  <div class="left-side-bar" :class="{ active: isCollapsed }">
    <div class="header1">
      <p>你的職料庫</p>
      <button type="button" class="collapse-btn" @click="toggleCollapse">
        <i class="fas fa-chevron-left"></i>
      </button>
    </div>
    <div class="block1">
      <p>建立你的第一個收藏清單</p>
      <button type="button" class="create-btn">建立收藏清單</button>
    </div>
    <hr>
    <p class="header2">瀏覽過的職缺</p>
    <div class="block2">
      <div class="viewed-job-frame"></div>
      <div class="viewed-job-text">
        <p class="title">信用卡產品經理</p>
        <p class="info">台北富邦商業銀行股份有限公司</p>
      </div>
      <button type="button" class="like-btn" :class="{ active: isLiked }" @click="toggleLike">
        <i class="fa-regular fa-heart"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LeftSidebar',
  data() {
    return {
      isCollapsed: false,
      isLiked: false
    }
  },
  methods: {
    toggleCollapse() {
      this.isCollapsed = !this.isCollapsed;
    },
    toggleLike() {
      this.isLiked = !this.isLiked;
    }
  }
}
</script>

<style scoped>
.left-side-bar {
    width: 240px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
    box-sizing: border-box;
    color: white;
    background-color: #383333;
    border-radius: 10px;
    height: calc(100vh - 72px); /* 减去Navbar的高度(56px)和padding(16px) */
    transition: width 0.5s ease;
    flex-shrink: 0;
    position: fixed;
    left: 16px;
    margin-top: 16px; /* Navbar的高度(56px) + padding(16px) */
    overflow-y: auto;
}

/* 添加滚动条样式 */
.left-side-bar::-webkit-scrollbar {
    width: 6px;
}

.left-side-bar::-webkit-scrollbar-track {
    background: #383333;
    border-radius: 3px;
}

.left-side-bar::-webkit-scrollbar-thumb {
    background: #594f4f;
    border-radius: 3px;
}

.left-side-bar::-webkit-scrollbar-thumb:hover {
    background: #746a6a;
}

.collapse-btn.active i {
    transform: rotate(180deg); 
}

.left-side-bar .header1 {
    height: 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.left-side-bar .header1 p {   
    font-size: 14px;
}

.collapse-btn {
    border: none;
    background: none;
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: transform 0.5s ease;
}

.collapse-btn:hover {
    transform: scale(1.1);
}

.left-side-bar .header1 p,
.left-side-bar .block1,
.left-side-bar .header2,
.left-side-bar .viewed-job-text,
.left-side-bar .create-btn,
.left-side-bar hr {
    display: block;
    opacity: 1;
    visibility: visible; 
    transition: opacity 0.3s ease 0.3s, visibility 0.3s ease 0.3s;
}

.left-side-bar .block1 p {
    font-size: 12px;
    margin-top: 0;
}

.left-side-bar .block1 .create-btn {
    border: none;
    background: white;
    color: black;
    font-size: 10px;
    border-radius: 50px;
    padding: 6px 12px;
    margin-top: 0px;
    cursor: pointer;
}

.left-side-bar .block1,
.left-side-bar .block2 {
    background-color: #594f4f;
    border-radius: 5px;
    padding: 12px;
}

hr {
    border: none;
    height: 1px;
    background-color: #746a6a;
    opacity: 50%;
    margin: 8px 0;
}

.left-side-bar .header2 {
    font-size: 14px;
    margin-top: 0px;
    margin-bottom: 4px;
}

.left-side-bar .block2 {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    position: relative;
}

.left-side-bar .block2 .viewed-job-frame {
    width: 64px;
    height: 64px;
    border-radius: 10px;
    background-color: #ffffff;
    background-image: url("/public/台北富邦銀行.jpg");
    background-size: cover;
    background-position: center;
    border: none;
    padding: 0;
    flex-shrink: 0; 
}

.left-side-bar .block2 .viewed-job-text {
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex-grow: 1;
    color: white;
    overflow: hidden;
}

.left-side-bar .block2 .viewed-job-text p {
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.left-side-bar .block2 .viewed-job-text .title {
    font-size: 12px; 
}

.left-side-bar .block2 .viewed-job-text .info {
    font-size: 10px;
}

.left-side-bar .block2 .like-btn {
    position: absolute;
    right: 8px;
    bottom: 8px;
    border: none;
    background: none;
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: transform 0.5s ease;
}

.left-side-bar .block2 .like-btn:hover {
    transform: scale(1.1);
}

.left-side-bar .block2 .like-btn.active {
    color: #ff9f9f;
}

.left-side-bar * {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.left-side-bar.active {
    width: 60px;
    padding: 20px 8px;
    align-items: center;
    left: 16px;
}

.left-side-bar.active p,
.left-side-bar.active .block1,
.left-side-bar.active hr,
.left-side-bar.active .like-btn,
.left-side-bar.active .viewed-job-text {
    display: none;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.2s ease, visibility 0.2s ease;
}

.left-side-bar.active .block2 {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: transparent;
    padding: 0;
    width: 100%;
}

.left-side-bar.active .viewed-job-frame {
    width: 40px; 
    height: 40px;
}
</style> 
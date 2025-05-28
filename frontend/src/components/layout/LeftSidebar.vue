<template>
  <div class="left-side-bar" :class="{ active: collapsed }" :style="{ width: width + 'px' }">
    <div class="header1">
      <p v-if="!collapsed">你的職料庫</p>
      <button type="button" class="collapse-btn" @click="toggleCollapseInternal">
        <font-awesome-icon :icon="['fas', collapsed ? 'chevron-right' : 'chevron-left']" />
      </button>
    </div>

    <div class="block1 scrollable-block">
      <template v-if="likedItems && likedItems.length > 0">
        <div v-for="item in likedItems" :key="item.id" class="job-card-in-sidebar liked-job-card" @click="handleItemClick(item)">
          <div v-if="item.image" class="job-image-sidebar" :style="{ backgroundImage: 'url(' + item.image + ')' }">
          </div>
          <div class="content-container-sidebar" v-show="!collapsed">
            <p class="title-sidebar">{{ item.title }}</p>
            <p v-if="item.company" class="company-sidebar">{{ item.company }}</p>
          </div>
          <button type="button" class="like-btn active" @click.stop="handleUnlikeFromSidebar(item)" v-show="!collapsed">
            <font-awesome-icon :icon="['fas', 'heart']" class="heart-icon" />
          </button>
        </div>
      </template>
      <template v-else-if="!collapsed">
        <div class="block-empty-state">
          <p>建立你的第一個收藏清單</p>
        </div>
      </template>
    </div>

    <hr v-show="!collapsed || (likedItems && likedItems.length > 0) || (viewedItems && viewedItems.length > 0)">

    <p class="header2" v-show="!collapsed">瀏覽過的職缺</p>

    <div class="block2 scrollable-block">
      <template v-if="viewedItems && viewedItems.length > 0">
        <div v-for="item in viewedItems" :key="item.id" class="job-card-in-sidebar viewed-job-card"
          @click="handleItemClick(item)">
          <div v-if="item.image" class="job-image-sidebar" :style="{ backgroundImage: 'url(' + item.image + ')' }">
          </div>
          <div class="content-container-sidebar" v-show="!collapsed">
            <p class="title-sidebar">{{ item.title }}</p>
            <p v-if="item.company" class="company-sidebar">{{ item.company }}</p>
          </div>
          <button type="button" class="like-btn" :class="{ active: item.isItemLiked }" @click.stop="toggleLikeFromViewed(item)" v-show="!collapsed">
            <font-awesome-icon :icon="[item.isItemLiked ? 'fas' : 'far', 'heart']" class="heart-icon" />
          </button>
        </div>
      </template>
      <template v-else-if="!collapsed">
        <div class="block-empty-state">
          <p>尚未瀏覽任何職缺</p>
        </div>
      </template>
    </div>

    <div class="resizer" @mousedown="startResizing"></div>
  </div>
</template>

<script>
import eventBus from '/src/eventBus.js';

export default {
  name: 'LeftSidebar',
  props: {
    width: {
      type: Number,
      default: 240
    },
    collapsed: {
      type: Boolean,
      default: false
    },
    likedItems: {
      type: Array,
      default: () => []
    },
    viewedItems: { // New prop for viewed items
      type: Array,
      default: () => []
    }
  },
  inject: ['openRightSidebar', 'updateLikedItemInSidebar'], // 確保注入 openRightSidebar
  data() {
    return {
      isResizing: false,
      initialMouseX: 0,
      initialWidth: 0,
    };
  },
  mounted() {
    document.addEventListener('mousemove', this.handleResizeMouseMove);
    document.addEventListener('mouseup', this.stopResizing);
  },
  beforeUnmount() {
    document.removeEventListener('mousemove', this.handleResizeMouseMove);
    document.removeEventListener('mouseup', this.stopResizing);
  },
  methods: {
    toggleCollapseInternal() {
      this.$emit('toggle-collapse');
    },

    // 這個方法在「收藏列表」的實心愛心被點擊時觸發 (取消收藏)
    handleUnlikeFromSidebar(itemToUnlike) {
      if (itemToUnlike) {
        // 通知 Home.vue 更新 UI 狀態，並讓 Home.vue 調用 API 取消收藏
        // 注意：這裡傳遞 itemToUnlike.id 就夠了，Home.vue 會處理 isLiked=false
        eventBus.emit('unlike-item-in-home-via-sidebar', itemToUnlike.id);
        // 通知 BaseLayout 從收藏列表刪除該項目，並更新瀏覽列表中該項目的愛心狀態為空心
        this.$emit('remove-item-from-liked-list', itemToUnlike.id);
      }
    },

    toggleLikeFromViewed(itemToToggle) {
      if (itemToToggle) {
        // 計算新的愛心狀態：如果目前是收藏的，就變成取消收藏；如果目前是未收藏的，就變成收藏
        const newLikedStatus = !itemToToggle.isItemLiked;

        // 1. 通知 BaseLayout 更新數據：
        //    - 如果是收藏：將該職缺加入或更新到 `likedItemsForLeftSidebar`，並更新 `viewedItemsForLeftSidebar` 中該職缺的 `isItemLiked` 狀態。
        //    - 如果是取消收藏：將該職缺從 `likedItemsForLeftSidebar` 移除，並更新 `viewedItemsForLeftSidebar` 中該職缺的 `isItemLiked` 狀態。
        //    我們需要傳遞原始數據 (`_originalData`) 和新的收藏狀態 (`newLikedStatus`) 給 BaseLayout。
        this.updateLikedItemInSidebar(itemToToggle.originalData, newLikedStatus);

        // 2. 透過 eventBus 通知 Home.vue 同步愛心狀態，並觸發 API 調用：
        //    Home.vue 的 `syncLikeStatusAcrossSections` 會根據這個事件更新主頁面的愛心圖示。
        //    同時 Home.vue 的 `toggleLike` 方法會執行 API 收藏/取消收藏。
        if (newLikedStatus) {
          eventBus.emit('like-item-in-home-via-sidebar', itemToToggle.id);
        } else {
          eventBus.emit('unlike-item-in-home-via-sidebar', itemToToggle.id);
        }
      }
    },
    handleItemClick(item) {
      // 點擊瀏覽過的項目或收藏項目時，開啟右側邊欄
      // 將儲存的 _originalData (原始職缺數據) 傳遞給 BaseLayout
      if (typeof this.openRightSidebar === 'function') {
        this.openRightSidebar(item.originalData);
      }
    },

    startResizing(event) {
      this.isResizing = true;
      this.initialMouseX = event.clientX;
      this.initialWidth = this.width;
      document.body.style.userSelect = 'none';
      document.body.style.cursor = 'ew-resize';
      event.preventDefault();
    },
    handleResizeMouseMove(e) {
      if (this.isResizing) {
        const deltaX = e.clientX - this.initialMouseX;
        let newWidth = this.initialWidth + deltaX;
        const minWidth = 60;
        const maxWidth = 400;
        newWidth = Math.max(minWidth, Math.min(newWidth, maxWidth));
        this.$emit('update-width', newWidth);
      }
    },
    stopResizing() {
      if (this.isResizing) {
        this.isResizing = false;
        document.body.style.userSelect = '';
        document.body.style.cursor = '';
      }
    }
  },
  watch: {
    likedItems(newVal) {
      console.log('LeftSidebar.vue: likedItems prop updated:', JSON.parse(JSON.stringify(newVal)));
    }
  }
}
</script>

<style scoped>
/* 主側邊欄樣式 */
.left-side-bar {
  height: 100%;
  padding: 16px;
  background-color: #383333;
  border-radius: 10px;
  color: white;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  align-items: stretch;
  transition: width 0.5s ease;
  min-width: 60px;
  box-sizing: border-box;
  position: relative;
  flex-shrink: 0;
}

/* 間距控制 */
.left-side-bar>.header1 {
  margin-bottom: 8px;
}

.left-side-bar>.scrollable-block {
  margin-bottom: 16px;
}

.left-side-bar>hr {
  margin-top: 0;
  margin-bottom: 16px;
}

.left-side-bar>.header2 {
  margin-bottom: 8px;
}

.left-side-bar>.resizer {
  margin-bottom: 0;
}

.left-side-bar .block2.scrollable-block:has(+ .resizer) {
  margin-bottom: 0;
}


/* Resizer */
.resizer {
  position: absolute;
  top: 0;
  right: -2.5px;
  width: 5px;
  height: 100%;
  cursor: ew-resize;
  background-color: transparent;
  z-index: 10;
}

/* Header1 and collapse button */
.left-side-bar .header1 {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 32px;
  flex-shrink: 0;
}

.left-side-bar .header1 p {
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.collapse-btn {
  border: none;
  background: none;
  color: white;
  font-size: 16px;
  cursor: pointer;
  padding: 5px;
  transition: transform 0.3s ease;
}

.collapse-btn:hover {
  transform: scale(1.1);
}

/* Common styles for scrollable blocks (block1 and block2) */
.scrollable-block {
  border-radius: 5px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 176px;
  /* Approx 2 cards (80px each + 8px gap) + 4px padding */
  overflow-y: auto;
  overflow-x: hidden;
  padding: 4px;
  scrollbar-width: thin;
  scrollbar-color: #727272 transparent;
}

.scrollable-block::-webkit-scrollbar {
  width: 6px;
}

.scrollable-block::-webkit-scrollbar-track {
  background: transparent;
  margin: 2px 0;
}

.scrollable-block::-webkit-scrollbar-thumb {
  background-color: #727272;
  border-radius: 3px;
}

.scrollable-block::-webkit-scrollbar-thumb:hover {
  background-color: #888888;
}

/* Styling for the empty state message inside blocks */
.block-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 12px;
  text-align: center;
  min-height: 60px;
  color: #b0b0b0;
}

.block-empty-state p {
  font-size: 12px;
  margin: 0;
}

hr {
  height: 1px;
  background-color: #746a6a;
  opacity: 0.5;
  border: none;
  flex-shrink: 0;
  width: 100%;
}

.left-side-bar .header2 {
  font-size: 14px;
  flex-shrink: 0;
}

/* --- CSS for cards in sidebar (liked-job-card and viewed-job-card) --- */
.job-card-in-sidebar {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 12px;
  background-color: #594f4f;
  border-radius: 5px;
  padding: 8px;
  color: white;
  position: relative;
  flex-shrink: 0;
  min-height: 80px;
  box-sizing: border-box;
}

.job-image-sidebar {
  width: 64px;
  height: 64px;
  border-radius: 6px;
  background-size: cover;
  background-position: center;
  flex-shrink: 0;
}

.content-container-sidebar {
  display: flex;
  flex-direction: column;
  gap: 4px;
  color: white;
  overflow: hidden;
  flex-grow: 1;
  min-width: 0;
}

.content-container-sidebar p {
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.title-sidebar {
  font-size: 12px;
  font-weight: bold;
}

.company-sidebar {
  font-size: 10px;
}

.job-card-in-sidebar .like-btn {
  position: absolute;
  right: 8px;
  bottom: 8px;
  background: none;
  border: none;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: transform 0.3s ease, color 0.3s ease;
  padding: 5px;
  z-index: 1;
}

.job-card-in-sidebar .like-btn:hover {
  transform: scale(1.1);
}

.job-card-in-sidebar .like-btn.active {
  /* For liked items in block1 */
  color: rgb(235, 178, 189);
}

.heart-icon {
  transition: color 0.3s ease;
}


/* Collapsed styles */
.left-side-bar.active {
  padding: 16px 8px;
  align-items: center;
}

.left-side-bar.active .scrollable-block {
  padding: 0;
  max-height: none;
  overflow: visible;
  gap: 8px;
  align-items: center;
  width: auto;
}

.left-side-bar.active .job-card-in-sidebar {
  background-color: transparent;
  padding: 0;
  gap: 0;
  min-height: auto;
  width: 40px;
  height: 40px;
  justify-content: center;
  align-items: center;
  margin-bottom: 0;
}

.left-side-bar.active .job-image-sidebar {
  width: 40px;
  height: 40px;
  border-radius: 4px;
}

.left-side-bar.active .content-container-sidebar,
.left-side-bar.active .job-card-in-sidebar .like-btn,
.left-side-bar.active .header1 p,
.left-side-bar.active .header2,
.left-side-bar.active .block-empty-state {
  display: none;
}

.left-side-bar.active hr {
  width: 40px;
  opacity: 0.3;
}
</style>
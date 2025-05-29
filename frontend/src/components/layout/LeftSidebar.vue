<!-- 左側邊欄組件：用於顯示用戶收藏的職位和瀏覽歷史 -->
<template>
  <!-- 主容器：可折疊的側邊欄，寬度可調整 -->
  <div class="left-side-bar" :class="{ active: collapsed }" :style="{ width: width + 'px' }">
    <!-- 頂部標題欄：包含標題和折疊按鈕 -->
    <div class="header1">
      <p v-if="!collapsed">你的職料庫</p>
      <button type="button" class="collapse-btn" @click="toggleCollapseInternal">
        <font-awesome-icon :icon="['fas', collapsed ? 'chevron-right' : 'chevron-left']" />
      </button>
    </div>

    <!-- 收藏職位列表區域 -->
    <div class="block1 scrollable-block">
      <template v-if="likedItems && likedItems.length > 0">
        <!-- 遍歷顯示所有收藏的職位卡片 -->
        <div v-for="item in likedItems.filter(item => item.isLiked || item.isItemLiked)" 
             :key="item.id + '-' + item.type" 
             class="job-card-in-sidebar liked-job-card" 
             @click="handleItemClick(item)">
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
        <div v-for="item in viewedItems" :key="item.id" class="job-card-in-sidebar viewed-job-card">
          <div v-if="item.image" class="job-image-sidebar" :style="{ backgroundImage: 'url(' + item.image + ')' }">
          </div>
          <div class="content-container-sidebar" v-show="!collapsed">
            <p class="title-sidebar">{{ item.title }}</p>
            <p v-if="item.company" class="company-sidebar">{{ item.company }}</p>
          </div>
          <button type="button" class="like-btn" @click="handleLikeFromViewed(item)" v-show="!collapsed">
            <font-awesome-icon :icon="['far', 'heart']" class="heart-icon" />
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
import { updateLikedCompanies } from '@/api/company';

export default {
  name: 'LeftSidebar',
  props: {
    // 側邊欄寬度，默認240像素
    width: {
      type: Number,
      default: 240
    },
    // 控制側邊欄是否折疊
    collapsed: {
      type: Boolean,
      default: false
    },
    // 收藏的職位列表
    likedItems: {
      type: Array,
      default: () => []
    },
    // 瀏覽過的職位列表
    viewedItems: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      // 用於控制側邊欄寬度調整的狀態
      isResizing: false,
      initialMouseX: 0,
      initialWidth: 0,
    };
  },
  mounted() {
    // 添加全局事件監聽器，用於處理側邊欄寬度調整
    document.addEventListener('mousemove', this.handleResizeMouseMove);
    document.addEventListener('mouseup', this.stopResizing);
  },
  beforeUnmount() {
    // 組件銷毀前移除事件監聽器
    document.removeEventListener('mousemove', this.handleResizeMouseMove);
    document.removeEventListener('mouseup', this.stopResizing);
  },
  methods: {
    // 觸發折疊/展開事件
    toggleCollapseInternal() {
      this.$emit('toggle-collapse');
    },

    // 從收藏列表中移除職位
    async handleUnlikeFromSidebar(itemToUnlike) {
      if (itemToUnlike) {
        try {
          // 先調用 API 更新後端狀態
          await updateLikedCompanies(itemToUnlike.id, false);
          
          // 通知父組件移除這個項目，同時傳遞 type
          this.$emit('remove-item-from-liked-list', itemToUnlike.id, itemToUnlike.type || 'job');
          
          // 更新瀏覽列表中該項目的狀態
          const viewedItemIndex = this.viewedItems.findIndex(item => item.id === itemToUnlike.id);
          if (viewedItemIndex !== -1) {
            this.viewedItems[viewedItemIndex].isLiked = false;
          }

          // 發送事件通知其他組件更新狀態
          eventBus.emit('update-like-status', {
            id: itemToUnlike.id,
            type: itemToUnlike.type || 'job',
            isLiked: false
          });
        } catch (error) {
          console.error('Failed to unlike item:', error);
        }
      }
    },

    // 將瀏覽過的職位添加到收藏列表
    async handleLikeFromViewed(itemToLike) {
      if (itemToLike) {
        try {
          await updateLikedCompanies(itemToLike.id, true);
          this.$emit('add-item-to-liked-list', itemToLike);
        } catch (error) {
          console.error('Failed to like item:', error);
        }
      }
    },

    // 開始調整側邊欄寬度
    startResizing(event) {
      this.isResizing = true;
      this.initialMouseX = event.clientX;
      this.initialWidth = this.width;
      document.body.style.userSelect = 'none';
      document.body.style.cursor = 'ew-resize';
      event.preventDefault();
    },

    // 處理側邊欄寬度調整過程
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

    // 結束側邊欄寬度調整
    stopResizing() {
      if (this.isResizing) {
        this.isResizing = false;
        document.body.style.userSelect = '';
        document.body.style.cursor = '';
      }
    }
  },
  watch: {
    // 監聽收藏列表變化，處理取消收藏的情況
    likedItems: {
      handler(newVal) {
        console.log('LeftSidebar.vue: likedItems prop updated:', JSON.parse(JSON.stringify(newVal)));
        newVal.forEach(item => {
          if (!item.isLiked) {
            this.handleUnlikeFromSidebar(item);
          }
        });
      },
      deep: true
    }
  }
}
</script>

<style scoped>
/* 主側邊欄基礎樣式 */
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
  gap: 8px;
}

/* 各區塊間距控制 */
.left-side-bar > .header1 {
  margin-bottom: 8px;
}
.left-side-bar > .scrollable-block {
  margin-bottom: 16px;
}
.left-side-bar > hr {
  margin-top: 0;
  margin-bottom: 16px;
}
.left-side-bar > .header2 {
  margin-bottom: 8px;
}
.left-side-bar > .resizer {
  margin-bottom: 0;
}
.left-side-bar .block2.scrollable-block:has(+ .resizer) {
  margin-bottom: 0;
}

/* 寬度調整器樣式 */
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

/* 頂部標題和折疊按鈕樣式 */
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

/* 可滾動區塊的通用樣式 */
.scrollable-block {
  border-radius: 5px;
  flex-shrink: 1;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 88px;
  max-height: 40%;
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

/* 空狀態顯示樣式 */
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

/* 分隔線樣式 */
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

/* 職位卡片在側邊欄中的樣式 */
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
  height: 80px;
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

.job-card-in-sidebar .like-btn.active { /* For liked items in block1 */
  color: rgb(235, 178, 189);
}

.heart-icon {
  transition: color 0.3s ease;
}

/* 折疊狀態下的樣式調整 */
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
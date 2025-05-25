<!--將頁面分為上下結構（layout），並將navbar、leftsidebar、rightsidebar、mainpanel、slot（內容）分開-->
<template>
  <div class="layout">
    <Navbar />
    <div class="content">
      <LeftSidebar :width="leftSidebarWidth" :collapsed="isSidebarCollapsed" :liked-items="likedItemsForLeftSidebar"
        :viewed-items="viewedItemsForLeftSidebar" @update-width="updateLeftSidebarWidth"
        @toggle-collapse="toggleCollapse" @remove-item-from-liked-list="handleRemoveItemFromLikedList" />

      <div class="main-panel">
        <div class="main-panel-slot-wrapper">
          <slot></slot>
        </div>
        <SiteFooter />
      </div>

      <div v-if="isRightSidebarVisible" class="right-sidebar-wrapper" :style="{ width: rightSidebarWidth + 'px' }">
        <RightSidebar :is-visible="isRightSidebarVisible" :job-data="selectedJobForRightSidebar"
          :current-actual-width="rightSidebarWidth" @close="closeRightSidebar"
          @update-width="updateRightSidebarWidth" />
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './Navbar.vue'
import LeftSidebar from './LeftSidebar.vue'
import RightSidebar from './RightSidebar.vue'
import SiteFooter from './Footer.vue';
// import eventBus from '/src/eventBus.js';

export default {
  name: 'BaseLayout',
  components: {
    Navbar,
    LeftSidebar,
    RightSidebar,
    SiteFooter
  },
  provide() {
    return {
      openRightSidebar: this.handleOpenRightSidebar,
      updateLikedItemInSidebar: this.handleUpdateLikedItemInSidebar,
      addViewedItemToSidebar: this.handleAddViewedItemToSidebar,
    };
  },
  data() {
    return {
      isSidebarCollapsed: false,
      leftSidebarWidth: 240,
      rightSidebarWidth: 240,
      isRightSidebarVisible: false,
      selectedJobForRightSidebar: null,
      likedItemsForLeftSidebar: [], // 將由 localStorage 初始化
      viewedItemsForLeftSidebar: [], // 將由 localStorage 初始化
    };
  },
  created() {
    // 從 localStorage 加載收藏的項目
    const storedLikedItems = localStorage.getItem('likedJobItems');
    if (storedLikedItems) {
      this.likedItemsForLeftSidebar = JSON.parse(storedLikedItems);
    }
    // 從 localStorage 加載瀏覽過的項目
    const storedViewedItems = localStorage.getItem('viewedJobItems');
    if (storedViewedItems) {
      this.viewedItemsForLeftSidebar = JSON.parse(storedViewedItems);
    }
  },
  watch: {
    likedItemsForLeftSidebar: {
      handler(newValue, oldValue) {
        console.log('[BaseLayout Watch] likedItemsForLeftSidebar changed.');
        console.log('New value:', JSON.parse(JSON.stringify(newValue)));
        // console.log('Old value:', JSON.parse(JSON.stringify(oldValue))); // 可選
        localStorage.setItem('likedJobItems', JSON.stringify(newValue));
      },
      deep: true
    },
    viewedItemsForLeftSidebar: {
      handler(newValue) {
        localStorage.setItem('viewedJobItems', JSON.stringify(newValue));
      },
      deep: true // 深度監聽，因為是物件陣列
    }
  },
  methods: {
    toggleCollapse() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
      this.leftSidebarWidth = this.isSidebarCollapsed ? 60 : 240;
    },
    updateLeftSidebarWidth(newWidth) {
      const minWidth = 60;
      const maxWidth = 280;
      this.leftSidebarWidth = Math.max(minWidth, Math.min(newWidth, maxWidth));
      this.isSidebarCollapsed = this.leftSidebarWidth <= 120;
    },
    updateRightSidebarWidth(newWidth) {
      const minRightWidth = 200;
      const maxRightWidth = 280;
      this.rightSidebarWidth = Math.max(minRightWidth, Math.min(newWidth, maxRightWidth));
    },
    handleOpenRightSidebar(jobData) {
      this.selectedJobForRightSidebar = jobData;
      this.isRightSidebarVisible = true;
      const minRightWidth = 200;
      if (this.rightSidebarWidth < minRightWidth) {
        this.rightSidebarWidth = 240;
      }
    },
    closeRightSidebar() {
      this.isRightSidebarVisible = false;
      this.selectedJobForRightSidebar = null;
    },
    handleUpdateLikedItemInSidebar(jobData, isLiked) {
      console.log('[BaseLayout] handleUpdateLikedItemInSidebar called with jobData:', JSON.parse(JSON.stringify(jobData)), 'isLiked:', isLiked);
      if (!jobData || typeof jobData.id === 'undefined') {
        console.error('[BaseLayout] Received jobData with undefined id:', JSON.parse(JSON.stringify(jobData)));
        return;
      }

      if (isLiked) {
        const existingItem = this.likedItemsForLeftSidebar.find(item => item.id === jobData.id);
        console.log('[BaseLayout] Is item already in liked list (by id ' + jobData.id + ')?', existingItem ? JSON.parse(JSON.stringify(existingItem)) : 'No');
        if (!existingItem) {
          this.likedItemsForLeftSidebar.unshift({ ...jobData }); // 確保 jobData 包含所有必要欄位
          console.log('[BaseLayout] Item added to likedItemsForLeftSidebar. New list:', JSON.parse(JSON.stringify(this.likedItemsForLeftSidebar)));
        } else {
          console.log('[BaseLayout] Item already in liked list. Not adding again.');
          // 如果項目已存在，確保其 isLiked 狀態與 jobData 一致 (如果需要)
          // existingItem.isLiked = true; // 或其他需要的屬性更新
        }
        this.viewedItemsForLeftSidebar = this.viewedItemsForLeftSidebar.filter(item => item.id !== jobData.id);
      } else {
        const initialLength = this.likedItemsForLeftSidebar.length;
        this.likedItemsForLeftSidebar = this.likedItemsForLeftSidebar.filter(item => item.id !== jobData.id);
        console.log(`[BaseLayout] Item with id ${jobData.id} removed (or attempted). Liked list count changed from ${initialLength} to ${this.likedItemsForLeftSidebar.length}. New list:`, JSON.parse(JSON.stringify(this.likedItemsForLeftSidebar)));
      }
    },
    handleRemoveItemFromLikedList(itemId) {
      // 先找到要移除的項目，以便之後可能將其加入瀏覽列表
      // const itemToRemove = this.likedItemsForLeftSidebar.find(item => item.id === itemId);

      this.likedItemsForLeftSidebar = this.likedItemsForLeftSidebar.filter(item => item.id !== itemId);

      // 如果希望從側邊欄取消收藏後，該項目加入到「瀏覽過」的列表 (且不在裡面)
      // if (itemToRemove) {
      //   const isAlreadyViewed = this.viewedItemsForLeftSidebar.some(viewedItem => viewedItem.id === itemToRemove.id);
      //   const isStillLiked = this.likedItemsForLeftSidebar.some(likedItem => likedItem.id === itemToRemove.id); // 應該為 false
      //   if (!isAlreadyViewed && !isStillLiked) {
      //     //  this.handleAddViewedItemToSidebar(itemToRemove); // 確保 itemToRemove 是完整物件
      //   }
      // }
      // localStorage 的更新將由 watcher 自動處理
    },
    handleAddViewedItemToSidebar(jobData) {
      const isAlreadyLiked = this.likedItemsForLeftSidebar.some(item => item.id === jobData.id);
      if (isAlreadyLiked) {
        return;
      }
      this.viewedItemsForLeftSidebar = this.viewedItemsForLeftSidebar.filter(item => item.id !== jobData.id);
      this.viewedItemsForLeftSidebar.unshift({ ...jobData });
      if (this.viewedItemsForLeftSidebar.length > 10) {
        this.viewedItemsForLeftSidebar.pop();
      }
      // localStorage 的更新將由 watcher 自動處理
    }
  }
}
</script>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  background-color: #000000;
  box-sizing: border-box;
  overflow: hidden;
  padding-top: 56px;
}

.content {
  display: flex;
  flex-grow: 1;
  padding: 0 8px 8px 8px;
  gap: 8px;
  box-sizing: border-box;
  overflow: hidden;
  min-height: 0;
  /* Flexbox 修正，防止內容溢出時 flex item 計算錯誤 */
}

.main-panel {
  flex-grow: 1;
  /* main-panel 佔據 content 中除了 sidebar 的剩餘空間 */
  min-width: 0;
  /* 防止內容過多時撐開佈局 */

  display: flex;
  /* 使 main-panel 成為 flex 容器 */
  flex-direction: column;
  /* 使 slot-wrapper 和 footer 垂直排列 */

  overflow-y: auto;
  /* 關鍵：main-panel 自身垂直滾動 */
  border-radius: 10px;
  transition: background-color 0.3s ease;

}

.main-panel::-webkit-scrollbar {
  display: none;
}


.right-sidebar-wrapper {
  flex-shrink: 0;
  transition: width 0.3s ease;
  height: 100%;
  /* overflow-y: auto; */
  /* 如果 RightSidebar 也需要獨立滾動 */
}
</style>
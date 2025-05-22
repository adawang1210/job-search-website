<!--將頁面分為上下結構（layout），並將navbar、leftsidebar、rightsidebar、mainpanel、slot（內容）分開-->
<template>
  <div class="layout">
    <Navbar />
    <div class="content">
      <LeftSidebar
        :width="leftSidebarWidth"
        :collapsed="isSidebarCollapsed"
        :liked-items="likedItemsForLeftSidebar"
        :viewed-items="viewedItemsForLeftSidebar" @update-width="updateLeftSidebarWidth"
        @toggle-collapse="toggleCollapse"
        @remove-item-from-liked-list="handleRemoveItemFromLikedList"
      />

      <div class="main-panel">
        <slot></slot>
      </div>

      <div v-if="isRightSidebarVisible" class="right-sidebar-wrapper" :style="{ width: rightSidebarWidth + 'px' }">
        <RightSidebar
          :is-visible="isRightSidebarVisible"
          :job-data="selectedJobForRightSidebar"
          :current-actual-width="rightSidebarWidth"
          @close="closeRightSidebar"
          @update-width="updateRightSidebarWidth"
        />
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './Navbar.vue'
import LeftSidebar from './LeftSidebar.vue'
import RightSidebar from './RightSidebar.vue'
// import eventBus from '/src/eventBus.js';

export default {
  name: 'BaseLayout',
  components: {
    Navbar,
    LeftSidebar,
    RightSidebar,
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
      handler(newValue) {
        localStorage.setItem('likedJobItems', JSON.stringify(newValue));
      },
      deep: true // 深度監聽，因為是物件陣列
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
      if (isLiked) {
        const existingItem = this.likedItemsForLeftSidebar.find(item => item.id === jobData.id);
        if (!existingItem) {
          this.likedItemsForLeftSidebar.unshift({ ...jobData });
        }
        this.viewedItemsForLeftSidebar = this.viewedItemsForLeftSidebar.filter(item => item.id !== jobData.id);
      } else {
        this.likedItemsForLeftSidebar = this.likedItemsForLeftSidebar.filter(item => item.id !== jobData.id);
        // 注意：如果您希望取消收藏後自動加入到瀏覽列表，
        // 您可能需要調用 this.handleAddViewedItemToSidebar(jobData) (並確保 jobData 是完整的物件)
        // 但目前的邏輯是瀏覽列表僅通過點擊卡片來添加。
      }
      // localStorage 的更新將由 watcher 自動處理
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
/* Styles remain the same */
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
}

.main-panel {
  flex-grow: 1;
  min-width: 0;
  overflow-y: auto;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.main-panel::-webkit-scrollbar {
  display: none;
}

.right-sidebar-wrapper {
  flex-shrink: 0;
  transition: width 0.3s ease;
  height: 100%;
}
</style>
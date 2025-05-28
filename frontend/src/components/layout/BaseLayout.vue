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
      // 假設 localStorage 存的是簡化格式，直接解析
      // 如果之前存的是原始格式，需要類似 handleUpdateLikedItemInSidebar 的轉換邏輯
      try {
        const parsedItems = JSON.parse(storedLikedItems);
        this.likedItemsForLeftSidebar = parsedItems.map(item => ({
          id: item.id,
          title: item.title,
          company: item.company,
          image: item.image,
          _originalData: item._originalData || item, // 如果沒有_originalData就用自身
        }));
      } catch (e) {
        console.error("Error parsing likedJobItems from localStorage:", e);
        this.likedItemsForLeftSidebar = [];
      }
    }

    // 從 localStorage 加載瀏覽過的項目
    const storedViewedItems = localStorage.getItem('viewedJobItems');
    if (storedViewedItems) {
      try {
        const parsedItems = JSON.parse(storedViewedItems);
        // 將從 localStorage 讀取的項目轉換為簡化格式
        this.viewedItemsForLeftSidebar = parsedItems.map(item => ({
          id: item.id,
          title: item.title,
          company: item.company,
          image: item.image,
          _originalData: item._originalData || item, // 如果沒有_originalData就用自身
        }));
      } catch (e) {
        console.error("Error parsing viewedJobItems from localStorage:", e);
        this.viewedItemsForLeftSidebar = [];
      }
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
    handleOpenRightSidebar(jobOriginalData) {
      this.selectedJobForRightSidebar = jobOriginalData; // 直接將原始數據賦值給 RightSidebar
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
    handleUpdateLikedItemInSidebar(jobDataFromSource, isLiked) {
      console.log('[BaseLayout] handleUpdateLikedItemInSidebar called with jobDataFromSource:', JSON.parse(JSON.stringify(jobDataFromSource)), 'isLiked:', isLiked);

      if (!jobDataFromSource || typeof jobDataFromSource.id === 'undefined') {
        console.error('[BaseLayout] Received jobDataFromSource with undefined id:', JSON.parse(JSON.stringify(jobDataFromSource)));
        return;
      }

      // 將原始職缺數據轉換為 LeftSidebar 收藏列表所需的簡化格式
      const formattedLikedItem = {
        id: jobDataFromSource.id,
        title: jobDataFromSource.title,
        company: jobDataFromSource.company && jobDataFromSource.company.name ? jobDataFromSource.company.name : jobDataFromSource.company || '未知公司', // 確保是字串
        image: jobDataFromSource.company_logo || jobDataFromSource.image || 'default_job_image.png',
        originalData: jobDataFromSource, // 保留原始數據
      };

      if (isLiked) {
        const existingItem = this.likedItemsForLeftSidebar.find(item => item.id === formattedLikedItem.id);
        if (!existingItem) {
          this.likedItemsForLeftSidebar.unshift({ ...formattedLikedItem });
        } else {
          // 如果已存在，確保其 isLiked 狀態與 jobDataFromSource 一致 (如果需要)
          // existingItem.isLiked = true; // 收藏列表中的項目本身就代表已收藏
        }
        // 如果職缺被收藏，就從瀏覽紀錄中移除
        this.viewedItemsForLeftSidebar = this.viewedItemsForLeftSidebar.filter(item => item.id !== formattedLikedItem.id);
      } else {
        // 如果取消收藏，從收藏列表中移除
        this.likedItemsForLeftSidebar = this.likedItemsForLeftSidebar.filter(item => item.id !== formattedLikedItem.id);
        // 可以考慮將取消收藏的職缺重新加入瀏覽紀錄（如果它不在裡面）
        // 確保加回去的也是簡化格式
        const isAlreadyViewed = this.viewedItemsForLeftSidebar.some(item => item.id === formattedLikedItem.id);
        if (!isAlreadyViewed) {
          this.viewedItemsForLeftSidebar.unshift(formattedLikedItem);
          if (this.viewedItemsForLeftSidebar.length > 10) { // 限制數量
            this.viewedItemsForLeftSidebar.pop();
          }
        }
      }
    },

    handleRemoveItemFromLikedList(itemId) {
      // 這是 LeftSidebar 點擊收藏按鈕時觸發的
      // 找到要移除的項目，並確保其 isLiked 狀態為 false
      const itemToRemove = this.likedItemsForLeftSidebar.find(item => item.id === itemId);

      this.likedItemsForLeftSidebar = this.likedItemsForLeftSidebar.filter(item => item.id !== itemId);

      // 將取消收藏的項目加回瀏覽紀錄 (如果它還不在裡面)
      if (itemToRemove) {
        const isAlreadyViewed = this.viewedItemsForLeftSidebar.some(viewedItem => viewedItem.id === itemToRemove.id);
        if (!isAlreadyViewed) {
          this.viewedItemsForLeftSidebar.unshift(itemToRemove);
          if (this.viewedItemsForLeftSidebar.length > 10) {
            this.viewedItemsForLeftSidebar.pop();
          }
        }
      }
    },

    handleAddViewedItemToSidebar(jobOriginalData) {
      if (!jobOriginalData || typeof jobOriginalData.id === 'undefined') {
        console.error('[BaseLayout] Received jobOriginalData with undefined id for viewed item:', jobOriginalData);
        return;
      }

      // 檢查是否已經被收藏
      const isAlreadyLiked = this.likedItemsForLeftSidebar.some(item => item.id === jobOriginalData.id);
      if (isAlreadyLiked) {
        return; // 如果已經被收藏，則不加入瀏覽紀錄
      }

      // 將原始職缺數據轉換為 LeftSidebar 瀏覽紀錄所需的簡化格式
      const formattedViewedItem = {
        id: jobOriginalData.id,
        title: jobOriginalData.title,
        company: jobOriginalData.company && jobOriginalData.company.name ? jobOriginalData.company.name : jobOriginalData.company || '未知公司', // 確保是字串
        image: jobOriginalData.company_logo || jobOriginalData.image || 'default_job_image.png',
        originalData: jobOriginalData, // 保留原始數據供 RightSidebar 使用
      };

      // 移除舊的相同項目，確保最新瀏覽的在最前面
      this.viewedItemsForLeftSidebar = this.viewedItemsForLeftSidebar.filter(item => item.id !== formattedViewedItem.id);
      this.viewedItemsForLeftSidebar.unshift(formattedViewedItem);

      // 限制數量
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
  flex: 1;
  padding: 0 4px 4px 4px;
  gap: 4px;
  box-sizing: border-box;
  overflow: hidden;
  min-height: 0;
  /* Flexbox 修正，防止內容溢出時 flex item 計算錯誤 */
}

.main-panel {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  border-radius: 10px;
  transition: background-color 0.3s ease;
  padding: 0 4px;
  box-sizing: border-box;
}

.main-panel-slot-wrapper {
  flex: 1;
  width: 100%;
  min-width: 0;
  display: flex;
  flex-direction: column;
  padding: 0;
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
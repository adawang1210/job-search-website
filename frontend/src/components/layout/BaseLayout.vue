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
import eventBus from '/src/eventBus.js';

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
    try {
      const parsedItems = JSON.parse(storedLikedItems);
      this.likedItemsForLeftSidebar = parsedItems.map(item => ({
        // 確保加載時帶有 isItemLiked: true
        id: item.id,
        title: item.title,
        company: item.company,
        image: item.image,
        originalData: item.originalData || item,
        isItemLiked: true, // 收藏列表的項目預設為實心愛心
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
      // 加載瀏覽記錄時，需要判斷它是否同時也在收藏列表中，來設定 isItemLiked 狀態
      this.viewedItemsForLeftSidebar = parsedItems.map(item => {
        // 在這裡判斷這個瀏覽項目是否被收藏
        const isLiked = this.likedItemsForLeftSidebar.some(likedItem => likedItem.id === item.id);
        return {
          id: item.id,
          title: item.title,
          company: item.company,
          image: item.image,
          originalData: item.originalData || item,
          isItemLiked: isLiked, // 根據是否在收藏列表來設定愛心狀態
        };
      });
    } catch (e) {
      console.error("Error parsing viewedJobItems from localStorage:", e);
      this.viewedItemsForLeftSidebar = [];
    }
  }
},
  watch: {
    likedItemsForLeftSidebar: {
      handler(newValue) {
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
        isItemLiked: isLiked, // 新增：用來控制側邊欄中愛心圖示的狀態
      };

    if (isLiked) { // 如果是收藏操作 (點擊愛心)
      // 1. 新增到收藏列表 (如果不在裡面)
      const existingLikedItemIndex = this.likedItemsForLeftSidebar.findIndex(item => item.id === formattedLikedItem.id);
      if (existingLikedItemIndex === -1) {
        this.likedItemsForLeftSidebar.unshift({ ...formattedLikedItem, isItemLiked: true }); // 確保收藏列表中的顯示為實心
      } else {
        // 如果已經在收藏列表，更新其狀態為實心 (雖然通常點擊愛心就會是實心)
        this.likedItemsForLeftSidebar[existingLikedItemIndex].isItemLiked = true;
      }

      // 2. 更新瀏覽列表中該項目的愛心狀態為實心 (如果它在瀏覽列表的話)
      const existingViewedItemIndex = this.viewedItemsForLeftSidebar.findIndex(item => item.id === formattedLikedItem.id);
      if (existingViewedItemIndex !== -1) {
        this.viewedItemsForLeftSidebar[existingViewedItemIndex].isItemLiked = true;
      }

    } else { // 如果是取消收藏操作 (取消愛心)
      // 1. 從收藏列表刪除
      this.likedItemsForLeftSidebar = this.likedItemsForLeftSidebar.filter(item => item.id !== formattedLikedItem.id);

      // 2. 更新瀏覽列表中該項目的愛心狀態為空心 (如果它在瀏覽列表的話)
      const existingViewedItemIndex = this.viewedItemsForLeftSidebar.findIndex(item => item.id === formattedLikedItem.id);
      if (existingViewedItemIndex !== -1) {
        this.viewedItemsForLeftSidebar[existingViewedItemIndex].isItemLiked = false;
      }
    }
  },

  handleRemoveItemFromLikedList(itemId) {
    // 找到要移除的項目，以便之後可以更新瀏覽列表的狀態
    const itemToRemove = this.likedItemsForLeftSidebar.find(item => item.id === itemId);

    // 從收藏列表中移除
    this.likedItemsForLeftSidebar = this.likedItemsForLeftSidebar.filter(item => item.id !== itemId);

    // 如果該項目曾經是收藏的，並且在瀏覽列表中存在，則更新瀏覽列表中的愛心狀態為空心
    if (itemToRemove) {
      const viewedItemToUpdate = this.viewedItemsForLeftSidebar.find(item => item.id === itemId);
      if (viewedItemToUpdate) {
        viewedItemToUpdate.isItemLiked = false;
      }
      // 因為是取消收藏，所以也需要通知 Home.vue
      // 注意：這會觸發 Home.vue 的 handleUnlikeFromSidebar，進而觸發 syncLikeStatusAcrossSections
      // 確保 syncLikeStatusAcrossSections 能正確處理 isItemLiked 狀態
      eventBus.emit('unlike-item-in-home-via-sidebar', itemId); // 假設是職缺
    }
    // localStorage 的更新將由 watcher 自動處理
  },

    // 這個方法在 Home.vue 點擊卡片時被呼叫
  // jobOriginalData 是原始職缺數據
    handleAddViewedItemToSidebar(jobOriginalData) {
      if (!jobOriginalData || typeof jobOriginalData.id === 'undefined') {
        console.error('[BaseLayout] Received jobOriginalData with undefined id for viewed item:', jobOriginalData);
        return;
      }

      // 檢查該職缺是否已經被收藏 (在收藏列表裡)
      const isAlreadyLiked = this.likedItemsForLeftSidebar.some(item => item.id === jobOriginalData.id);

      // 將原始職缺數據轉換為 LeftSidebar 瀏覽紀錄所需的簡化格式
      // 這裡的 isItemLiked 狀態來自於收藏列表的狀態
      const formattedViewedItem = {
        id: jobOriginalData.id,
        title: jobOriginalData.title,
        company: jobOriginalData.company && jobOriginalData.company.name ? jobOriginalData.company.name : jobOriginalData.company || '未知公司',
        image: jobOriginalData.company_logo || jobOriginalData.image || 'default_job_image.png',
        originalData: jobOriginalData, // 保留原始數據供 RightSidebar 使用
        isItemLiked: isAlreadyLiked, // 決定在瀏覽列表中顯示實心還是空心愛心
      };

      // 移除舊的相同項目，確保最新瀏覽的在最前面 (保持唯一性，新瀏覽的排在最前)
      this.viewedItemsForLeftSidebar = this.viewedItemsForLeftSidebar.filter(item => item.id !== formattedViewedItem.id);
      this.viewedItemsForLeftSidebar.unshift(formattedViewedItem);

      // 限制瀏覽紀錄的數量
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
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
import { updateLikedCompanies } from '@/api/home.js';

const ITEM_TYPE_JOB = 'job';
const ITEM_TYPE_COMPANY = 'company';

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
      isItemCurrentlyLiked: this.isItemCurrentlyLiked,
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
    console.log('Loading stored items from localStorage:', storedLikedItems);
    
    if (storedLikedItems) {
      try {
        const parsedItems = JSON.parse(storedLikedItems);
        this.likedItemsForLeftSidebar = parsedItems.map(item => ({
          id: item.id,
          title: item.title,
          company: item.company,
          image: item.image,
          originalData: item.originalData || item,
          isItemLiked: true,
          isLiked: true,
          type: item.type,
        }));
        console.log('Loaded liked items:', this.likedItemsForLeftSidebar);
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
          const isLiked = this.likedItemsForLeftSidebar.some(likedItem => likedItem.id === item.id && likedItem.type === item.type);
          return {
            id: item.id,
            title: item.title,
            company: item.company,
            image: item.image,
            originalData: item.originalData || item,
            isItemLiked: isLiked,
            type: item.type, // 【新增】確保從 localStorage 加載時也包含 type
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
    handleOpenRightSidebar(originalData) {
      this.selectedJobForRightSidebar = originalData; // 直接將原始數據賦值給 RightSidebar
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
    isItemCurrentlyLiked(itemId, itemType) {
      return this.likedItemsForLeftSidebar.some(item => item.id === itemId && item.type === itemType);
    },
    // 【關鍵】handleRemoveItemFromLikedList：現在負責處理取消收藏並呼叫 API (如果需要)
    async handleRemoveItemFromLikedList(itemId, itemType) { // 【新增】async
      // 找到要移除的項目，以便之後可以更新瀏覽列表的狀態，並獲取原始數據
      const itemToRemove = this.likedItemsForLeftSidebar.find(item => item.id === itemId && item.type === itemType);
      
      // 樂觀更新 BaseLayout 內部列表
      this.likedItemsForLeftSidebar = this.likedItemsForLeftSidebar.filter(item => item.id !== itemId || item.type !== itemType);
      const viewedItemToUpdate = this.viewedItemsForLeftSidebar.find(item => item.id === itemId && item.type === itemType);
      if (viewedItemToUpdate) {
        viewedItemToUpdate.isItemLiked = false;
      }
      
      // 處理 API 呼叫 (只針對公司)
      try {
        if (itemType === ITEM_TYPE_COMPANY) {
          await updateLikedCompanies(itemId, false); // 取消收藏，所以 isLiked 為 false
          console.log(`[BaseLayout API Success] 公司 ${itemId} 已取消收藏。`);
        }
        // 職缺類型：不呼叫 API
      } catch (error) {
        console.error(`[BaseLayout API Error] 無法從後端取消收藏 ${itemType} ID ${itemId}:`, error);
        alert(`取消收藏操作失敗，請稍後再試。\n錯誤訊息: ${error.message || error}`);

        // API 失敗，執行回滾邏輯 (將項目加回收藏列表，並將瀏覽列表的愛心狀態設為 true)
        if (itemToRemove) { // itemToRemove 應該是收藏時的 formattedItem
          const existingLikedItemIndex = this.likedItemsForLeftSidebar.findIndex(item => item.id === itemToRemove.id && item.type === itemToRemove.type);
          if (existingLikedItemIndex === -1) { // 如果已經被移除了，再加回去
             this.likedItemsForLeftSidebar.unshift({ ...itemToRemove, isItemLiked: true });
          } else { // 如果還在，確保是實心
             this.likedItemsForLeftSidebar[existingLikedItemIndex].isItemLiked = true;
          }
          const viewedItemIndex = this.viewedItemsForLeftSidebar.findIndex(item => item.id === itemToRemove.id && item.type === itemToRemove.type);
          if (viewedItemIndex !== -1) {
            this.viewedItemsForLeftSidebar[viewedItemIndex].isItemLiked = true;
          }
        }
        // 此處因為是取消收藏失敗，所以最終狀態是 true (仍然被收藏)
        eventBus.emit('update-like-status', { id: itemId, type: itemType, isLiked: true }); 
        return; // API 失敗後，直接返回，不再執行下面的成功事件
      }

      // 無論 API 成功或職缺收藏 (無 API)，都發送 eventBus 事件
      eventBus.emit('update-like-status', { id: itemId, type: itemType, isLiked: false }); // 最終狀態為取消收藏，所以 isLiked 為 false
      // localStorage 的更新將由 watcher 自動處理
    },
        // 【關鍵】handleUpdateLikedItemInSidebar：現在負責區分職缺和公司，並呼叫 API
    async handleUpdateLikedItemInSidebar(itemOriginalData, isLiked) { // 【新增】async 關鍵字
      console.log('[BaseLayout] handleUpdateLikedItemInSidebar called with itemOriginalData:', JSON.parse(JSON.stringify(itemOriginalData)), 'isLiked:', isLiked);

      if (!itemOriginalData || typeof itemOriginalData.id === 'undefined' || !itemOriginalData.type) {
        console.error('[BaseLayout] Received itemOriginalData with undefined id or type:', JSON.parse(JSON.stringify(itemOriginalData)));
        return;
      }

      const originalIsLikedStatus = isLiked ? false : true; // 如果是收藏操作，原始是false；如果是取消，原始是true
      let formattedItem = {}; 

      // 構建 formattedItem
      if (itemOriginalData.type === ITEM_TYPE_JOB) {
        formattedItem = {
          id: itemOriginalData.id,
          title: itemOriginalData.title,
          company: itemOriginalData.company && itemOriginalData.company.name ? itemOriginalData.company.name : itemOriginalData.company || '未知公司',
          image: itemOriginalData.company_logo || itemOriginalData.image || 'default_job_image.png',
          originalData: itemOriginalData,
          type: ITEM_TYPE_JOB,
          isItemLiked: isLiked, // 最終的愛心狀態
        };
      } else if (itemOriginalData.type === ITEM_TYPE_COMPANY) {
        formattedItem = {
          id: itemOriginalData.id,
          title: itemOriginalData.name,
          company: itemOriginalData.industry || '未知行業',
          image: itemOriginalData.media && itemOriginalData.media.logo ? itemOriginalData.media.logo : itemOriginalData.image || 'default_company_logo_path.png',
          originalData: itemOriginalData,
          type: ITEM_TYPE_COMPANY,
          isItemLiked: isLiked, // 最終的愛心狀態
        };
      } else {
        console.warn('[BaseLayout] Unknown item type for updateLikedItemInSidebar:', itemOriginalData.type);
        return;
      }

      // 【核心邏輯】樂觀更新列表，並呼叫 API (如果需要)
      // 步驟 1: 更新 BaseLayout 內部的兩個列表 (likedItemsForLeftSidebar 和 viewedItemsForLeftSidebar)
      if (isLiked) { // 收藏操作
        const existingLikedItemIndex = this.likedItemsForLeftSidebar.findIndex(item => item.id === formattedItem.id && item.type === formattedItem.type);
        if (existingLikedItemIndex === -1) {
          this.likedItemsForLeftSidebar.unshift({ ...formattedItem, isItemLiked: true });
        } else {
          this.likedItemsForLeftSidebar[existingLikedItemIndex].isItemLiked = true;
        }
        const existingViewedItemIndex = this.viewedItemsForLeftSidebar.findIndex(item => item.id === formattedItem.id && item.type === formattedItem.type);
        if (existingViewedItemIndex !== -1) {
          this.viewedItemsForLeftSidebar[existingViewedItemIndex].isItemLiked = true;
        }
      } else { // 取消收藏操作
        this.likedItemsForLeftSidebar = this.likedItemsForLeftSidebar.filter(item => item.id !== formattedItem.id || item.type !== formattedItem.type);
        const existingViewedItemIndex = this.viewedItemsForLeftSidebar.findIndex(item => item.id === formattedItem.id && item.type === formattedItem.type);
        if (existingViewedItemIndex !== -1) {
          this.viewedItemsForLeftSidebar[existingViewedItemIndex].isItemLiked = false;
        }
      }

      // 步驟 2: 處理 API 呼叫 (只針對公司)
      try {
        if (itemOriginalData.type === ITEM_TYPE_COMPANY) {
          await updateLikedCompanies(itemOriginalData.id, isLiked);
          console.log(`[BaseLayout API Success] 公司 ${itemOriginalData.id} 收藏狀態已更新為 ${isLiked}。`);
        }
        // 職缺類型：不呼叫 API
      } catch (error) {
        console.error(`[BaseLayout API Error] 無法更新 ${itemOriginalData.type} ID ${itemOriginalData.id} 的收藏狀態到後端:`, error);
        alert(`收藏操作失敗，請稍後再試。\n錯誤訊息: ${error.message || error}`);
        
        // API 失敗，執行回滾邏輯 (將 BaseLayout 內部的列表狀態回滾)
        if (isLiked) { // 如果是收藏失敗，則從 likedItems 移除，並將 viewedItems 中的 isItemLiked 設為 false
          this.likedItemsForLeftSidebar = this.likedItemsForLeftSidebar.filter(item => item.id !== formattedItem.id || item.type !== formattedItem.type);
          const viewedItemIndex = this.viewedItemsForLeftSidebar.findIndex(item => item.id === formattedItem.id && item.type === formattedItem.type);
          if (viewedItemIndex !== -1) {
            this.viewedItemsForLeftSidebar[viewedItemIndex].isItemLiked = false;
          }
        } else { // 如果是取消收藏失敗，則將 item 加回 likedItems，並將 viewedItems 中的 isItemLiked 設為 true
          const existingLikedItemIndex = this.likedItemsForLeftSidebar.findIndex(item => item.id === formattedItem.id && item.type === formattedItem.type);
          if (existingLikedItemIndex === -1) {
            this.likedItemsForLeftSidebar.unshift({ ...formattedItem, isItemLiked: true });
          } else {
            this.likedItemsForLeftSidebar[existingLikedItemIndex].isItemLiked = true;
          }
          const viewedItemIndex = this.viewedItemsForLeftSidebar.findIndex(item => item.id === formattedItem.id && item.type === formattedItem.type);
          if (viewedItemIndex !== -1) {
            this.viewedItemsForLeftSidebar[viewedItemIndex].isItemLiked = true;
          }
        }
        // 將 isLiked 變數設置為回滾後的狀態，以便 eventBus 發出正確的事件
        isLiked = originalIsLikedStatus; 
      }

      // 步驟 3: 無論 API 成功或失敗，都發送 eventBus 事件
      // 這個事件通知所有組件該項目的最終愛心狀態 (如果 API 失敗則為回滾後的狀態)
      eventBus.emit('update-like-status', { id: formattedItem.id, type: formattedItem.type, isLiked: isLiked });
    },
    handleAddViewedItemToSidebar(jobOriginalData) {
      if (!jobOriginalData || typeof jobOriginalData.id === 'undefined' || !jobOriginalData.type || jobOriginalData.type !== ITEM_TYPE_JOB) { // 【新增】檢查 type 且必須是職缺
        console.error('[BaseLayout] Received invalid jobOriginalData for viewed item:', JSON.parse(JSON.stringify(jobOriginalData)));
        return;
      }

      // 檢查該職缺是否已經被收藏 (在收藏列表裡)，同時判斷 id 和 type
      const isAlreadyLiked = this.likedItemsForLeftSidebar.some(item => item.id === jobOriginalData.id && item.type === ITEM_TYPE_JOB);

      // 將原始職缺數據轉換為 LeftSidebar 瀏覽紀錄所需的簡化格式
      const formattedViewedItem = {
        id: jobOriginalData.id,
        title: jobOriginalData.title,
        company: jobOriginalData.company && jobOriginalData.company.name ? jobOriginalData.company.name : jobOriginalData.company || '未知公司',
        image: jobOriginalData.company_logo || jobOriginalData.image || 'default_job_image.png',
        originalData: jobOriginalData,
        type: ITEM_TYPE_JOB, // 明確類型為職缺
        isItemLiked: isAlreadyLiked,
      };

      // 移除舊的相同項目，確保最新瀏覽的在最前面 (保持唯一性，同時判斷 id 和 type)
      this.viewedItemsForLeftSidebar = this.viewedItemsForLeftSidebar.filter(item => item.id !== formattedViewedItem.id || item.type !== formattedViewedItem.type);
      this.viewedItemsForLeftSidebar.unshift(formattedViewedItem);

      if (this.viewedItemsForLeftSidebar.length > 10) {
        this.viewedItemsForLeftSidebar.pop();
      }
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
}
</style>
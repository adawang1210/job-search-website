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
          id: item.id,
          title: item.title, // 職缺 title 或 公司 name
          company: item.company, // 職缺公司名稱 或 公司行業/描述 (如果公司有這個屬性)
          image: item.image, // 職缺圖片 或 公司 logo
          originalData: item.originalData || item,
          isItemLiked: true,
          type: item.type, // 【新增】確保從 localStorage 加載時也包含 type
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
    handleUpdateLikedItemInSidebar(itemOriginalData, isLiked) {
      console.log('[BaseLayout] handleUpdateLikedItemInSidebar called with itemOriginalData:', JSON.parse(JSON.stringify(itemOriginalData)), 'isLiked:', isLiked);

      if (!itemOriginalData || typeof itemOriginalData.id === 'undefined' || !itemOriginalData.type) { // 【修改】新增 type 檢查
        console.error('[BaseLayout] Received itemOriginalData with undefined id or type:', JSON.parse(JSON.stringify(itemOriginalData)));
        return;
      }

      // 【新增】根據類型構建統一格式
      let formattedItem = {};
      if (itemOriginalData.type === ITEM_TYPE_JOB) {
        formattedItem = {
          id: itemOriginalData.id,
          title: itemOriginalData.title,
          company: itemOriginalData.company && itemOriginalData.company.name ? itemOriginalData.company.name : itemOriginalData.company || '未知公司',
          image: itemOriginalData.company_logo || itemOriginalData.image || 'default_job_image.png',
          originalData: itemOriginalData,
          type: ITEM_TYPE_JOB,
          isItemLiked: isLiked,
        };
      } else if (itemOriginalData.type === ITEM_TYPE_COMPANY) {
        formattedItem = {
          id: itemOriginalData.id,
          title: itemOriginalData.name, // 公司的名稱作為標題
          company: itemOriginalData.industry || '未知行業', // 公司的行業作為副標題
          image: itemOriginalData.media && itemOriginalData.media.logo ? itemOriginalData.media.logo : itemOriginalData.image || 'default_company_logo_path.png',
          originalData: itemOriginalData,
          type: ITEM_TYPE_COMPANY,
          isItemLiked: isLiked,
        };
      } else {
        console.warn('[BaseLayout] Unknown item type for updateLikedItemInSidebar:', itemOriginalData.type);
        return;
      }

      if (isLiked) { // 如果是收藏操作 (點擊愛心)
        // 1. 新增到收藏列表 (如果不在裡面)，需要同時判斷 id 和 type
        const existingLikedItemIndex = this.likedItemsForLeftSidebar.findIndex(item => item.id === formattedItem.id && item.type === formattedItem.type);
        if (existingLikedItemIndex === -1) {
          this.likedItemsForLeftSidebar.unshift({ ...formattedItem, isItemLiked: true });
        } else {
          this.likedItemsForLeftSidebar[existingLikedItemIndex].isItemLiked = true;
        }

        // 2. 更新瀏覽列表中該項目的愛心狀態為實心 (如果它在瀏覽列表的話)，需要同時判斷 id 和 type
        const existingViewedItemIndex = this.viewedItemsForLeftSidebar.findIndex(item => item.id === formattedItem.id && item.type === formattedItem.type);
        if (existingViewedItemIndex !== -1) {
          this.viewedItemsForLeftSidebar[existingViewedItemIndex].isItemLiked = true;
        }

      } else { // 如果是取消收藏操作 (取消愛心)
        // 1. 從收藏列表刪除，需要同時判斷 id 和 type
        this.likedItemsForLeftSidebar = this.likedItemsForLeftSidebar.filter(item => item.id !== formattedItem.id || item.type !== formattedItem.type);

        // 2. 更新瀏覽列表中該項目的愛心狀態為空心 (如果它在瀏覽列表的話)，需要同時判斷 id 和 type
        const existingViewedItemIndex = this.viewedItemsForLeftSidebar.findIndex(item => item.id === formattedItem.id && item.type === formattedItem.type);
        if (existingViewedItemIndex !== -1) {
          this.viewedItemsForLeftSidebar[existingViewedItemIndex].isItemLiked = false;
        }
      }

      // 【新增這行程式碼】
      // 在數據更新完成後，發出一個通用的事件，通知所有頁面職缺/公司的愛心狀態已經改變
      eventBus.emit('update-like-status', { id: formattedItem.id, type: formattedItem.type, isLiked: isLiked });
    },

    handleRemoveItemFromLikedList(itemId, itemType) { // 【新增】接收 itemType 參數
      // 找到要移除的項目，需要同時判斷 id 和 type
      const itemToRemove = this.likedItemsForLeftSidebar.find(item => item.id === itemId && item.type === itemType);

      // 從收藏列表中移除
      this.likedItemsForLeftSidebar = this.likedItemsForLeftSidebar.filter(item => item.id !== itemId || item.type !== itemType);

      // 如果該項目曾經是收藏的，並且在瀏覽列表中存在，則更新瀏覽列表中的愛心狀態為空心
      if (itemToRemove) {
        const viewedItemToUpdate = this.viewedItemsForLeftSidebar.find(item => item.id === itemId && item.type === itemType);
        if (viewedItemToUpdate) {
          viewedItemToUpdate.isItemLiked = false;
        }
        eventBus.emit('update-like-status', { id: itemId, type: itemType, isLiked: false });
      }
      // localStorage 的更新將由 watcher 自動處理
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
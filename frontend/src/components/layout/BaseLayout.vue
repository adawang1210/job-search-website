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
// import eventBus from '/src/eventBus.js'; // Potentially needed if BaseLayout emits to Home

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
      addViewedItemToSidebar: this.handleAddViewedItemToSidebar, // ADDED: Provide method to add viewed items
    };
  },
  data() {
    return {
      isSidebarCollapsed: false,
      leftSidebarWidth: 240,
      rightSidebarWidth: 240,
      isRightSidebarVisible: false,
      selectedJobForRightSidebar: null,
      likedItemsForLeftSidebar: [],
      viewedItemsForLeftSidebar: [], // ADDED: Store viewed items
    };
  },
  methods: {
    toggleCollapse() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
      this.leftSidebarWidth = this.isSidebarCollapsed ? 60 : 240;
    },
    updateLeftSidebarWidth(newWidth) {
      const minWidth = 60;
      const maxWidth = 280; // Or 400 if LeftSidebar's max is 400
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

    // MODIFIED: To also handle viewed items list
    handleUpdateLikedItemInSidebar(jobData, isLiked) {
      if (isLiked) {
        // Add item to the liked list if it's not already there
        const existingItem = this.likedItemsForLeftSidebar.find(item => item.id === jobData.id);
        if (!existingItem) {
          this.likedItemsForLeftSidebar.unshift({ ...jobData }); // Add to top for liked items
        }
        // Remove from viewed items list if it exists there
        this.viewedItemsForLeftSidebar = this.viewedItemsForLeftSidebar.filter(item => item.id !== jobData.id);
      } else {
        // Remove item from the liked list
        this.likedItemsForLeftSidebar = this.likedItemsForLeftSidebar.filter(item => item.id !== jobData.id);
        // Optional: If unliking should add it to viewed, do it here. Current spec doesn't require this.
      }
    },

    handleRemoveItemFromLikedList(itemId) {
      this.likedItemsForLeftSidebar = this.likedItemsForLeftSidebar.filter(item => item.id !== itemId);
      // Optional: If unliking should add it to viewed, find the jobData and call handleAddViewedItemToSidebar.
      // This would require finding the original jobData. Simpler to keep current behavior.
    },

    // ADDED: New method to handle adding items to the viewed list
    handleAddViewedItemToSidebar(jobData) {
      // Don't add to viewed if it's already liked
      const isAlreadyLiked = this.likedItemsForLeftSidebar.some(item => item.id === jobData.id);
      if (isAlreadyLiked) {
        return;
      }

      // Remove if already in viewed list (to move to top)
      this.viewedItemsForLeftSidebar = this.viewedItemsForLeftSidebar.filter(item => item.id !== jobData.id);

      // Add to the beginning of the viewed list
      this.viewedItemsForLeftSidebar.unshift({ ...jobData });

      // Ensure viewed list does not exceed 10 items
      if (this.viewedItemsForLeftSidebar.length > 10) {
        this.viewedItemsForLeftSidebar.pop(); // Remove the oldest item
      }
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
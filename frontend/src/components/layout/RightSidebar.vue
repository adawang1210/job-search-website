<template>
  <div class="right-sidebar" :class="{ active: isVisible }">
    <div class="resizer" @mousedown="startResizing"></div>
    <div class="sidebar-header">
      <h3>職缺詳細資訊</h3>
      <button @click="closeSidebar" class="close-btn">
        <font-awesome-icon :icon="['fas', 'times']" />
      </button>
    </div>
    <div v-if="jobData" class="sidebar-content-wrapper">
      <div class="sidebar-content">
        <h4>{{ jobData.title || jobData.name }}</h4>
        <img v-if="jobData.image" :src="jobData.image" :alt="jobData.title || jobData.name" class="sidebar-main-image" />
        <p v-if="jobData.company"><strong>公司：</strong> {{ jobData.company }}</p>
        <p v-if="jobData.location"><strong>地點：</strong> {{ jobData.location }}</p>
        <p v-if="jobData.salary"><strong>薪資：</strong> {{ jobData.salary }}</p>

        <template v-if="jobData.type === 'company'">
          <p>這是一家優質企業。</p>
        </template>
        <template v-else-if="jobData.type === 'favoriteJob'">
          <p>這是您收藏的職缺。</p>
          <img v-if="jobData.icon" :src="jobData.icon" alt="Company Icon" class="sidebar-company-icon" />
        </template>

        <p style="margin-top: 20px;"><em>更多詳細內容將顯示於此...</em></p>
      </div>
    </div>
    <div v-else class="sidebar-content-wrapper">
      <div class="sidebar-content">
        <p>請選擇一個項目以查看詳細資訊。</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RightSidebar',
  emits: ['close', 'update-width'],
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    jobData: {
      type: Object,
      default: null
    },
    currentActualWidth: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      isResizing: false,
      initialMouseX: 0,
      initialWidthForDrag: 0,
      minWidth: 200,
      maxWidth: 600
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
    closeSidebar() {
      this.$emit('close');
    },
    startResizing(event) {
      if (event.button !== 0) return;
      this.isResizing = true;
      this.initialMouseX = event.clientX;
      this.initialWidthForDrag = this.currentActualWidth;
      document.body.style.userSelect = 'none';
      document.body.style.cursor = 'ew-resize';
      event.preventDefault();
    },
    handleResizeMouseMove(e) {
      if (!this.isResizing) return;
      const deltaX = e.clientX - this.initialMouseX;
      let newWidth = this.initialWidthForDrag - deltaX;
      newWidth = Math.max(this.minWidth, Math.min(newWidth, this.maxWidth));
      this.$emit('update-width', newWidth);
    },
    stopResizing() {
      if (this.isResizing) {
        this.isResizing = false;
        document.body.style.userSelect = '';
        document.body.style.cursor = '';
      }
    }
  }
}
</script>

<style scoped>
/* 主側邊欄樣式 */
.right-sidebar {
  width: 100%;
  height: 100%;
  background-color: #383333;
  color: white;
  border-radius: 10px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
  flex-shrink: 0;
  box-sizing: border-box;
}

.resizer {
  position: absolute;
  top: 0;
  left: -2.5px;
  width: 5px;
  height: 100%;
  cursor: ew-resize;
  background-color: transparent;
  z-index: 10;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 32px;
  flex-shrink: 0;
  margin-bottom: 16px;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 16px;
  cursor: pointer;
  padding: 5px;
  transition: transform 0.3s ease, color 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  transform: scale(1.1);
  color: #f0f0f0;
}

.sidebar-content-wrapper {
  background-color: #594f4f;
  border-radius: 5px;
  flex-grow: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 12px;
}

.sidebar-content h4 {
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 600;
  color: white;
}

.sidebar-content p {
  margin-bottom: 8px;
  line-height: 1.5;
  font-size: 12px;
  color: white;
}

.sidebar-content strong {
  color: #e0e0e0;
  font-weight: bold;
}

.sidebar-main-image {
  max-width: 180px;  /* 圖片最大寬度 */
  width: 100%;       /* 圖片寬度填充容器，但不超過 max-width */
  height: auto;      /* 高度自動以保持長寬比 */
  max-height: 180px; /* 最大高度限制 */
  object-fit: cover;   /* 保持圖片填充方式，可能會裁剪 */
  display: block;
  margin-left: auto;
  margin-right: auto;
  border-radius: 8px;
  margin-bottom: 12px;
  background-color: #444;
}

.sidebar-company-icon {
  width: 48px;
  height: 48px;
  object-fit: contain;
  border-radius: 5px;
  margin-top: 8px;
  background-color: #fff;
  padding: 4px;
  box-sizing: border-box;
  /* 如果也希望它在容器變窄時能縮小，可以考慮類似的 max-width/width:100%/height:auto 策略 */
  /* display: block; */ /* 如果要用 margin auto 居中 */
  /* margin-left: auto; */
  /* margin-right: auto; */
}

.sidebar-content-wrapper::-webkit-scrollbar {
  width: 6px;
}

.sidebar-content-wrapper::-webkit-scrollbar-track {
  background: #594f4f;
}

.sidebar-content-wrapper::-webkit-scrollbar-thumb {
  background: #746a6a;
  border-radius: 3px;
}

.sidebar-content-wrapper::-webkit-scrollbar-thumb:hover {
  background: #8d8383;
}
</style>
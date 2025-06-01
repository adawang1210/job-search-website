<template>
  <n-layout-header class="navbar">
    <div class="overlay" v-show="showPositionPopup || showRegionPopup" @click="closeAllPopups"></div>

    <router-link to="/" class="home-btn">
      <n-icon size="20">
        <home-icon />
      </n-icon>
    </router-link>

    <div class="search">

      <!-- 職務彈出視窗-->
      <n-popover trigger="click" :show="showPositionPopup" @update:show="(show) => showPositionPopup = show"
        placement="bottom" :style="{ width: '500px' }" :raw="true">
        <template #trigger>
          <n-button quaternary class="position-btn">
            職務
            <template #icon>
              <n-icon>
                <chevron-down-icon />
              </n-icon>
            </template>
          </n-button>
        </template>
        <div class="popup-content">
          <n-space vertical>
            <n-checkbox-group v-model:value="selectedPositions">
              <n-grid :cols="2" :x-gap="12" :y-gap="8">
                <n-grid-item v-for="position in positions" :key="position.value">
                  <n-checkbox :value="position.value">
                    {{ position.label }}
                  </n-checkbox>
                </n-grid-item>
              </n-grid>
            </n-checkbox-group>
            <n-button type="primary" @click="confirmPosition" block class="confirm-btn">
              確認
            </n-button>
          </n-space>
        </div>
      </n-popover>

      <div class="divider"> | </div>
      <!-- 地區彈出視窗-->
      <n-popover trigger="click" :show="showRegionPopup" @update:show="(show) => showRegionPopup = show"
        placement="bottom" :style="{ width: '500px' }" :raw="true">
        <template #trigger>
          <n-button quaternary class="region-btn">
            地區
            <template #icon>
              <n-icon>
                <chevron-down-icon />
              </n-icon>
            </template>
          </n-button>
        </template>
        <div class="popup-content">
          <n-space vertical>
            <n-checkbox-group v-model:value="selectedRegions">
              <n-grid :cols="3" :x-gap="12" :y-gap="8">
                <n-grid-item v-for="region in regions" :key="region.id">
                  <n-checkbox :value="region.id">
                    {{ region.name }}
                  </n-checkbox>
                </n-grid-item>
              </n-grid>
            </n-checkbox-group>
            <n-button type="primary" @click="confirmRegion" block class="confirm-btn">
              確認
            </n-button>
          </n-space>
        </div>
      </n-popover>

      <div class="divider">|</div>

      <n-input v-model:value="searchQuery" placeholder="工作職稱、公司名稱" @keydown.enter.prevent="handleSearch">
        <template #suffix>
          <n-button quaternary @click="handleSearch">
            <template #icon>
              <n-icon>
                <search-icon />
              </n-icon>
            </template>
          </n-button>
        </template>
      </n-input>
    </div>

    <div class="quick-link">
      <router-link to="/allcompany"> 
        <n-button quaternary>公司</n-button>
      </router-link>
      <router-link to="/profile">
        <n-button quaternary>個人檔案</n-button>
      </router-link>
      <n-button quaternary class="bell-btn">
        <template #icon>
          <n-icon>
            <bell-icon />
          </n-icon>
        </template>
      </n-button>
    </div>

    <router-link to="/profile" class="avatar-frame"></router-link>
  </n-layout-header>
</template>

<script>
import { defineComponent } from 'vue'
import {
  NLayoutHeader,
  NButton,
  NInput,
  NIcon,
  NPopover,
  NCheckbox,
  NCheckboxGroup,
  NGrid,
  NGridItem,
  NSpace
} from 'naive-ui'
import {
  HomeOutline as HomeIcon,
  SearchOutline as SearchIcon,
  NotificationsOutline as BellIcon,
  ChevronDownOutline as ChevronDownIcon
} from '@vicons/ionicons5'

export default defineComponent({
  name: 'Navbar',
  components: {
    NLayoutHeader,
    NButton,
    NInput,
    NIcon,
    NPopover,
    NCheckbox,
    NCheckboxGroup,
    NGrid,
    NGridItem,
    NSpace,
    HomeIcon,
    SearchIcon,
    BellIcon,
    ChevronDownIcon
  },
  data() {
    return {
      showPositionPopup: false,
      showRegionPopup: false,
      selectedPositions: [], // 已選職務 (value 陣列)
      selectedRegions: [], // 已選地區 (id 陣列)
      searchQuery: '', // 關鍵字
      positions: [
        { value: 'position1', label: '經營/人資類' },
        { value: 'position2', label: '行政/總務/法務類' },
        { value: 'position3', label: '財會/金融專業類' },
        { value: 'position4', label: '行銷/企劃/專案管理類' },
        { value: 'position5', label: '客服/門市/業務/貿易類' },
        { value: 'position6', label: '餐飲/旅遊/美容美髮類' },
        { value: 'position7', label: '資訊軟體系統類' },
        { value: 'position8', label: '操作/技術/維修類' },
        { value: 'position9', label: '資材/物流/運輸類' },
        { value: 'position10', label: '營建/製圖類' },
        { value: 'position11', label: '傳播藝術/設計類' },
        { value: 'position12', label: '文字/傳媒工作類' },
        { value: 'position13', label: '醫療/保健服務類' },
        { value: 'position14', label: '學術/教育/輔導類' },
        { value: 'position15', label: '研發相關類' },
        { value: 'position16', label: '生產製造/品管/環衛類' },
        { value: 'position17', label: '軍警消/保全類' },
        { value: 'position18', label: '其他職類' }
      ],
      regions: [
        { id: '台北市', name: '台北市' },
        { id: '新北市', name: '新北市' },
        { id: '宜蘭縣', name: '宜蘭縣' },
        { id: '基隆市', name: '基隆市' },
        { id: '桃園市', name: '桃園市' },
        { id: '新竹縣市', name: '新竹縣市' },
        { id: '苗栗縣', name: '苗栗縣' },
        { id: '台中市', name: '台中市' },
        { id: '彰化縣', name: '彰化縣' },
        { id: '南投縣', name: '南投縣' },
        { id: '雲林縣', name: '雲林縣' },
        { id: '嘉義縣市', name: '嘉義縣市' },
        { id: '台南市', name: '台南市' },
        { id: '高雄市', name: '高雄市' },
        { id: '屏東縣', name: '屏東縣' },
        { id: '台東縣', name: '台東縣' },
        { id: '花蓮縣', name: '花蓮縣' },
        { id: '澎湖縣', name: '澎湖縣' },
        { id: '金門縣', name: '金門縣' },
        { id: '連江縣', name: '連江縣' }
      ]
    }
  },
  methods: {
    closeAllPopups() {
      this.showPositionPopup = false;
      this.showRegionPopup = false;
    },
    confirmPosition() {
      this.showPositionPopup = false;
      // 可以在這裡考慮是否自動觸發搜尋，如果 searchQuery 有值
      if (this.searchQuery.trim() !== '') this.handleSearch();
    },
    confirmRegion() {
      this.showRegionPopup = false;
      // 同上
      if (this.searchQuery.trim() !== '') this.handleSearch();
    },
    handleSearch() {
      const query = {};

      if (this.searchQuery && this.searchQuery.trim() !== '') {
        query.q = this.searchQuery.trim();
      }
      if (this.selectedPositions && this.selectedPositions.length > 0) {
        query.positions = this.selectedPositions.join(','); // 將陣列轉為逗號分隔的字串
      }
      if (this.selectedRegions && this.selectedRegions.length > 0) {
        query.regions = this.selectedRegions.join(','); // 將陣列轉為逗號分隔的字串
      }

      // 確保 $router 存在
      if (this.$router) {
        if (Object.keys(query).length > 0) {
          this.$router.push({
            name: 'searchresult', // 確保路由名稱正確
            query: query
          });
        } else {
          if (this.$route.name !== 'searchresult') {
             this.$router.push({ name: 'searchresult' });
          }
        }
      } else {
        console.error("Vue Router instance is not available.");
      }

      this.closeAllPopups();
    }
  }
})
</script>

<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.navbar {
  display: flex;
  align-items: center;
  padding: 16px 20px 0px 16px;
  background-color: #000000;
  height: 56px;
  box-sizing: border-box;
  flex-wrap: nowrap;
  overflow: hidden;
  gap: 16px;
  min-width: 0;
  flex-shrink: 0;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.search {
  display: flex;
  align-items: center;
  flex-shrink: 1;
  flex-grow: 1;
  min-width: 0;
  min-width: 200px;
  max-width: 500px;
  margin-bottom: 8px;
  padding: 4px 8px;
  gap: 8px;
  border-radius: 30px;
  background-color: #2a2a2a;
  height: 32px;
  overflow: hidden;
  box-sizing: border-box;
}

.search-input {
  flex-grow: 1;
  min-width: 0;
}

.quick-link {
  display: flex;
  align-items: center;
  gap: clamp(8px, 2vw, 30px);
  margin-bottom: 8px;
  white-space: nowrap;
  margin-left: clamp(8px, 2vw, 30px);
  flex-shrink: 0;
}

.avatar-frame {
  all: unset;
  display: inline-block;
  width: 32px;
  height: 32px;
  margin-bottom: 8px;
  border-radius: 50%;
  background-color: white;
  background-image: url("/子源大帥哥.jpg");
  background-size: cover;
  background-position: center;
  cursor: pointer;
  flex-shrink: 0;
  margin-left: auto;
}

:deep(.n-button) {
  background-color: transparent !important;
  color: white !important;
  border: none;
}

:deep(.confirm-btn) {
  background-color: #585858 !important;
  color: white !important;
  border: none !important;
  box-shadow: none !important; 
  outline: none !important;
}


:deep(.confirm-btn:hover) {
  background-color: #707070 !important;
  color: white !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
}

:deep(.confirm-btn:active),
:deep(.confirm-btn:focus), 
:deep(.confirm-btn:focus-visible) { 
  background-color: #404040 !important;
  color: white !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important; 
}

:deep(.n-button--primary:focus-visible .n-button__border) {
  border: none !important;
}

:deep(.n-button--primary:focus-visible .n-button__state-border) {
  border: none !important;
}

:deep(.n-input) {
  background-color: transparent !important;
}

:deep(.n-button:focus-visible) {
  outline: none !important;
  box-shadow: none !important;
}

:deep(.n-button:focus-visible .n-button__border) {
    border-color: transparent !important; /* 確保焦點時的邊框透明 */
}

:deep(.n-button:focus-visible .n-button__state-border) {
    border-color: transparent !important; /* 確保焦點時的狀態邊框透明 */
}

:deep(.n-button .n-button__state-border) {
    border-color: transparent !important; /* 確保狀態邊框透明 */
}

:deep(.n-input .n-input__input-el),
:deep(.n-input .n-input__input-el:focus),
:deep(.n-input .n-input__input-el:hover) {
  background-color: transparent !important;
  box-shadow: none !important;
  outline: none !important;
  color: #ffffff;
  border-color: none !important;
}

:deep(.n-input .n-input__state-border),
:deep(.n-input .n-input__border) {
  display: none !important;
}

:deep(.n-input .n-input__placeholder) {
  color: rgb(145, 145, 145);
}

:deep(.n-input .n-input__input-el::placeholder) {
  color: rgb(145, 145, 145);
}

:deep(.n-input .n-input__input-el:focus::placeholder) {
  color: rgb(145, 145, 145);
}

:deep(.n-popover) {
  position: fixed !important;
  transform: none !important;
  left: auto !important;
}

/* 強制設置彈出菜單背景為白色，不透明 */
:deep(.n-popover-body) {
  background-color: #2a2a2a !important;
  opacity: 1 !important;
  border-radius: 6px !important;
  box-shadow: 0 3px 6px -4px rgba(0, 0, 0, 0.12), 0 6px 16px 0 rgba(0, 0, 0, 0.08), 0 9px 28px 8px rgba(0, 0, 0, 0.05) !important;
}

:deep(.n-popover .n-popover__content) {
  padding: 16px;
  background-color: #2a2a2a !important;
  opacity: 1 !important;
}

:deep(.position-btn),
:deep(.region-btn) {
  color: white !important;
}

:deep(.position-btn:hover),
:deep(.region-btn:hover) {
  color: white !important;
}

:deep(.quick-link .n-button) {
  color: white !important;
}

:deep(.quick-link .n-button:hover) {
  color: white !important;
}

:deep(.home-btn) {
  color: white !important;
}

:deep(.n-checkbox) {
  --n-color: transparent !important; /* 未勾選時的背景色 */
  --n-color-checked: #ffffff !important; /* 勾選時的背景色 */
  --n-color-checked-hover: #ffffff !important; /* 勾選時 hover 的背景色 */
  --n-text-color: #ffffff !important; /* 文字顏色 */

  /* 移除 Naive UI 可能有的預設綠色邊框或陰影 */
  --n-border-checked: 1px solid #ffffff !important; /* 勾選時的邊框 */
  --n-border-hover: 1px solid #cccccc !important; /* 未勾選 hover 時的邊框 */
  --n-border-focus: 1px solid #cccccc !important; /* 焦點時的邊框 */
  --n-box-shadow-focus: none !important; /* 移除焦點時的陰影 */
}

/* 確保勾選框內部打勾符號的顏色 */
:deep(.n-checkbox .n-checkbox__check) {
  color: #000000 !important; /* 將打勾符號設為深色，才能在白色背景上看到 */
}

:deep(.n-checkbox--checked .n-checkbox__check) {
  color: #000000 !important; /* 已勾選時的打勾符號顏色 */
}

:deep(.n-checkbox:not(.n-checkbox--checked):hover .n-checkbox__box) {
  border-color: #cccccc !important;
}
:deep(.n-checkbox:not(.n-checkbox--checked):focus .n-checkbox__box) {
  border-color: #cccccc !important;
  box-shadow: none !important; /* 再次確保焦點陰影為無 */
}
:deep(.n-checkbox:not(.n-checkbox--checked):focus-visible .n-checkbox__box) {
  border-color: #cccccc !important;
  box-shadow: none !important; /* 再次確保焦點陰影為無 */
}


/* 勾選框被勾選且 hover 時的樣式 */
:deep(.n-checkbox--checked:hover .n-checkbox__box) {
  border-color: #ffffff !important; /* 保持白色邊框 */
  background-color: #ffffff !important; /* 保持白色背景 */
}

:deep(.n-checkbox__label) {
  color: #ffffff;
}

:deep(.n-space) {
  width: 100%;
}

@media (max-width: 480px) {

  .position-btn,
  .region-btn {
    display: none;
  }
}

.popup-content {
  background-color: #2a2a2a !important;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 16px;
}

.popup-content .n-checkbox-group {
  margin: 8px 0;
}

.popup-content .n-grid {
  margin-bottom: 16px;
}

.popup-content .confirm-btn {
  margin-top: 8px;
}

:deep(.n-checkbox) {
  margin: 4px 0;
}

:deep(.n-popover) {
  border: none !important;
  padding: 0 !important;
  border-radius: 8px !important;
  overflow: hidden;
}

:deep(.n-popover-shared) {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1) !important;
}

:deep(.n-popover .n-popover__content) {
  background-color: #2a2a2a !important;
}

:deep(.n-popover-body) {
  background-color: #2a2a2a !important;
}

:deep(.n-popover .n-popover__arrow-wrapper .n-popover__arrow) {
  background-color: #2a2a2a !important; /* 確保箭頭的背景色也是深灰色 */
}

:deep(.n-popover .n-popover__arrow-wrapper .n-popover__arrow-mask) {
  background-color: #2a2a2a !important; /* 確保箭頭的遮罩色也是深灰色 */
}

.divider {
  color: rgb(137, 137, 137);
  font-size: 14px;
  padding: 0 4px;
}
</style>
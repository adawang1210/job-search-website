<template>
  <div class="search-results-page">
    <h1>搜尋結果</h1>
    <p v-if="searchQuery && !isLoading && !error">
      你搜尋的是： "{{ searchQuery }}" {{ totalResultsMessage }}
    </p>
    <p v-else-if="!searchQuery && !isLoading && !error">請輸入關鍵字進行搜尋。</p>

    <div v-if="isLoading" class="loading-message">
      正在載入搜尋結果...
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="!isLoading && !error && searchResults.length > 0" class="search-results-grid">
      <div class="job-card-wrapper" v-for="job in displayedResults" :key="job.id" @click="handleCardClick(job)">
        <p class="job-card-title" @click.stop="handleTitleClick(job)">{{ job.title }}</p>
        <div class="job-card-image" :style="{ backgroundImage: 'url(' + (job.image || defaultImage) + ')' }"></div>
        <div class="job-card-details">
          <div class="job-card-info-left">
            <p class="job-card-company">{{ job.company }}</p>
            <p class="job-card-salary">{{ job.salary }}</p>
          </div>
          <button type="button" class="like-btn job-card-like-btn" :class="{ active: job.isLiked }"
            @click.stop="toggleLike(job)">
            <font-awesome-icon :icon="[job.isLiked ? 'fas' : 'far', 'heart']" class="heart-icon" />
          </button>
        </div>
      </div>
    </div>

    <div v-if="!isLoading && !error && searchResults.length === 0 && searchQuery" class="no-data-message">
      找不到與 "{{ searchQuery }}" 相關的職缺。
    </div>
  </div>
</template>

<script>

import { getJobs, getJobDetail } from '@/api/home.js';
import eventBus from '/src/eventBus.js';

const ITEM_TYPE_JOB = 'job';

export default {
  name: 'SearchResult',
  inject: ['openRightSidebar', 'updateLikedItemInSidebar', 'addViewedItemToSidebar', 'isItemCurrentlyLiked'],
  data() {
    return {
      searchQuery: '',
      activePositions: [],
      activeRegions: [],
      searchResults: [],
      isLoading: false,
      error: null,
      defaultImage: 'default_company_logo_path.png',
    };
  },
  computed: {
    // 實際顯示的職缺 (最多 8 行 * 4 列 = 32 個)
    displayedResults() {
      return this.searchResults.slice(0, 32);
    },
    totalResultsMessage() {
      if (this.searchResults.length > 0) {
        if (this.searchResults.length > 32) {
          return `(共 ${this.searchResults.length} 筆結果，顯示前 32 筆)`;
        }
        return `(共 ${this.searchResults.length} 筆結果)`;
      }
      return '';
    },
    // 實際的登入狀態檢查
    isUserLoggedIn() {
      // 這裡應該是您專案中檢查用戶是否登入的邏輯
      // 例如，從 Vuex store, localStorage, 或某個全局狀態獲取
      // return this.$store.state.auth.isLoggedIn;
      // return !!localStorage.getItem('user-token');
      return true; // 暫時假設總是登入
    }
  },
  // SearchResult.vue - created
  created() {
    this.searchQuery = this.$route.query.q || '';
    this.activePositions = this.$route.query.positions ? this.$route.query.positions.split(',') : [];
    this.activeRegions = this.$route.query.regions ? this.$route.query.regions.split(',') : [];

    if (this.searchQuery || this.activePositions.length > 0 || this.activeRegions.length > 0) {
      this.fetchSearchResults();
    }
  },
  // SearchResult.vue - watch
  watch: {
    '$route.query': {
      handler(newQuery) {
        this.searchQuery = newQuery.q || '';
        this.activePositions = newQuery.positions ? newQuery.positions.split(',') : [];
        this.activeRegions = newQuery.regions ? newQuery.regions.split(',') : [];
        this.searchResults = [];
        this.error = null;
        if (this.searchQuery || this.activePositions.length > 0 || this.activeRegions.length > 0) {
          this.fetchSearchResults();
        }
      },
      deep: true // 監聽 query 物件內部變化
    }
  },
  mounted() {
    // 【新增】監聽來自 BaseLayout 或 LeftSidebar 的收藏狀態更新事件
    eventBus.on('update-like-status', this.handleUpdateLikeStatus);
  },
  beforeUnmount() {
    // 【新增】在組件銷毀前移除事件監聽器
    eventBus.off('update-like-status', this.handleUpdateLikeStatus);
  },
  methods: {
    async fetchSearchResults() {
  this.isLoading = true;
  this.error = null;

  try {
    // 不帶參數，直接抓全部職缺
    const apiResponse = await getJobs();
    const rawJobs = apiResponse.results || apiResponse || [];

    // 前端過濾：搜尋關鍵字、職位、地區
    const filtered = rawJobs.filter(job => {
      const searchText = this.searchQuery?.toLowerCase() || '';

      // 模糊比對職缺名稱或公司名稱
      const titleMatch = job.title?.toLowerCase().includes(searchText);
      const companyMatch = job.company?.name?.toLowerCase().includes(searchText);
      const keywordMatch = searchText ? (titleMatch || companyMatch) : true;

      const positionMatch = this.activePositions.length
        ? this.activePositions.includes(job.characteristics)
        : true;

      const address = (job.location || '').toLowerCase(); // 地區是完整地址
      const regionMatch = this.activeRegions.length
        ? this.activeRegions.some(region => address.includes(region.toLowerCase()))
        : true;

      return keywordMatch && positionMatch && regionMatch;
    });

    this.searchResults = filtered.map(job => ({
      id: job.id,
      title: job.title,
      image: job.company_logo?.startsWith('http') 
        ? job.company_logo 
        : 'http://localhost:8000/' + (job.company_logo || 'default_job_image.png'),
      company: job.company?.name || '未知公司',
      salary: job.salary_max ? `$${job.salary_max}` : '面議',
      isLiked: job.is_liked_by_user || false,
      originalData: { ...job, type: ITEM_TYPE_JOB },
      type: ITEM_TYPE_JOB,
    }));
    console.log(this.searchResults)

    // 同步收藏狀態
    if (typeof this.isItemCurrentlyLiked === 'function') {
      this.searchResults.forEach(job => {
        job.isLiked = this.isItemCurrentlyLiked(job.id, job.type);
      });
    }

  } catch (err) {
    this.error = '載入職缺資料時發生錯誤，請稍後再試。';
    this.searchResults = [];
  } finally {
    this.isLoading = false;
  }
},
    handleUpdateLikeStatus(data) { // 預期 data 為 { id: itemId, type: itemType, isLiked: newStatus }
      const { id, type, isLiked } = data;
      // SearchResult 只顯示職缺，所以只處理 ITEM_TYPE_JOB 類型
      if (type === ITEM_TYPE_JOB) {
        const jobToUpdate = this.searchResults.find(job => job.id === id);
        if (jobToUpdate) {
          jobToUpdate.isLiked = isLiked;
        }
      }
    },
    // 【修改】點擊職缺卡片時，觸發瀏覽和開啟右側邊欄
    // job 已經是 SearchResult.vue 轉換過的格式：{ id, title, ..., isLiked, originalData, type }
    handleCardClick(job) {
      // 確保傳遞給 BaseLayout 的是原始 API 數據 (其中已包含 type)
      const dataForSidebar = job.originalData || job;

      // 1. 新增到瀏覽紀錄 (BaseLayout 的 addViewedItemToSidebar 只處理職缺)
      if (typeof this.addViewedItemToSidebar === 'function') {
        this.addViewedItemToSidebar(dataForSidebar);
      }
      // 2. 開啟右側邊欄
      if (typeof this.openRightSidebar === 'function') {
        this.openRightSidebar(dataForSidebar);
      }
    },
    // 【修改】點擊愛心按鈕時，處理收藏/取消收藏邏輯 (與 Home.vue 保持一致)
    // job 參數是 SearchResult.vue 內部轉換過的 job 物件
    async toggleLike(job) { // 這裡的 job 其實就是 item

      // 檢查是否是有效的職缺數據，包含 ID 和類型
      if (!job || !job.id || job.type !== ITEM_TYPE_JOB) {
        console.error('toggleLike: 無效的職缺數據或類型不符', job);
        return;
      }

      const newLikedStatus = !job.isLiked;

      // 1. 樂觀更新 UI
      job.isLiked = newLikedStatus;

      // 2. 通知 BaseLayout 更新側邊欄的收藏和瀏覽紀錄列表
      // 傳遞 job.originalData (原始 API 數據，包含 type) 和新的 isLiked 狀態
      if (typeof this.updateLikedItemInSidebar === 'function') {
        this.updateLikedItemInSidebar(job.originalData || job, newLikedStatus);
      }

      // 3. 透過 eventBus 通知所有頁面同步愛心狀態
      // 因為沒有 API 失敗回滾，所以這裡直接發送最終狀態即可
      eventBus.emit('update-like-status', { id: job.id, type: job.type, isLiked: newLikedStatus });

      // 【移除】try-catch 塊及其內部所有 API 呼叫和錯誤處理
      console.log(`[Frontend Only] 職缺 ${job.id} 的收藏狀態已更新為 ${newLikedStatus} (僅前端處理)`);

    },
    handleTitleClick(job) {
      // 與 Home.vue 保持一致的行為，例如導航到公司頁面
      // 這裡可以先 console.log 或 alert
      alert(`職缺標題 "${job.title}" 被點擊，預計導航或執行其他操作。`);
      // 實際導航邏輯:
      // if (job.originalData && job.originalData.company && job.originalData.company.id) {
      //   this.$router.push({ name: 'CompanyDetail', params: { id: job.originalData.company.id } });
      // }
    }
  }
};
</script>

<style scoped>
/* --- SearchResultsPage 基本樣式 --- */
.search-results-page {
  padding: 20px;
  color: white;
  background-color: #383333;
  border-radius: 10px;
  width: 100%;
  box-sizing: border-box;
}

.search-results-page h1 {
  font-size: 20px;
  padding-bottom: 8px;
  color: white;
  margin-bottom: 10px;
}

.search-results-page>p {
  margin-bottom: 15px;
  font-size: 1em;
}


/* --- 網格佈局 --- */
.search-results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  /* 響應式，最小260px，嘗試填滿4列 */
  gap: 20px;
  /* 卡片間距 */
  padding-top: 10px;
}

/* --- 複製自 Home.vue 的 JOB CARD STYLES 並稍作調整 --- */
.job-card-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: transparent;
  /* 或 #594f4f00 */
  border-radius: 5px;
  padding: 10px 25px 10px 25px;
  /* 上下10px，左右15px，您可以根據喜好調整 */
  box-sizing: border-box;
  color: white;
  transition: transform 0.3s ease-out, box-shadow 0.3s ease-out, background-color 0.3s ease-out;
  cursor: pointer;
  min-width: 0;
  width: 200px;
}

.job-card-wrapper:hover {
  background-color: #524a4a;
  /* hover 時的背景色 */
  transform: translateY(-1px);
  /* 稍微上浮 */
  box-shadow: 0 6px 6px rgba(0, 0, 0, 0.25);
  /* 移除了 width 變化，因為在網格中會導致佈局問題 */

}

.job-card-title {
  font-size: 15px;
  font-weight: bold;
  margin-bottom: 4px;
  margin-top: -6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 150px;
}

.job-card-title:hover {
  text-decoration: underline;
}

.job-card-image {
  width: 150px;
  height: 150px;
  background-color: white;
  /* 占位符背景 */
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 5px;
  margin-bottom: 5px;
  /* 圖片與下方詳情的間距 */
}

.job-card-details {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  width: 100%;
  /* 占滿卡片padding內的寬度 */
  margin-top: auto;
  /* 如果卡片內容高度不一致，確保details部分在底部 */
}

.job-card-info-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  /* 文字左對齊 */
  text-align: left;
  overflow: hidden;
  padding-right: 8px;
  /* 與愛心按鈕之間留點空隙 */
  flex-grow: 1;
  /* 佔據剩餘空間 */
}

.job-card-company,
.job-card-salary {
  font-size: 13px;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
  /* 佔滿 .job-card-info-left 的寬度 */
}

.job-card-company {
  font-weight: bold;
}

.job-card-salary {
  font-size: 12px;
  margin-top: -2px;
  color: #E0E0E0;
}

.job-card-like-btn.like-btn {
  /* .like-btn 已有通用樣式，這裡可微調 */
  display: flex;
  align-items: center;
  /* 確保愛心垂直居中（如果按鈕有高度） */
  font-size: 18px;
  flex-shrink: 0;
  /* 防止按鈕被壓縮 */
  margin-right: 6px;
}

/* --- 收藏按鈕通用樣式 (來自 Home.vue，保持一致) --- */
.like-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: white;
  font-size: 18px;
  /* 與 .job-card-like-btn 中的一致 */
  padding: 0;
  /* 移除預設 padding */
  transition: transform 0.2s ease, color 0.2s ease;
}

.like-btn:hover {
  transform: scale(1.1);
}

.like-btn.active {
  color: rgb(235, 178, 189);
  /* 粉色實心 */
}

.heart-icon {
  transition: color 0.3s ease;

}

/* --- 載入/錯誤/無數據訊息樣式 --- */
.loading-message,
.error-message,
.no-data-message {
  padding: 25px 20px;
  text-align: center;
  color: #ccc;
  width: 100%;
  box-sizing: border-box;
  font-size: 1.1em;
}

.error-message {
  color: #f8d7da;
  background-color: rgba(248, 215, 218, 0.1);
  border: 1px solid rgba(245, 198, 203, 0.3);
  border-radius: 5px;
  margin: 15px 0;
}

.loading-message {
  font-style: italic;
}

.no-data-message {
  margin-top: 20px;
}

/* --- 響應式調整 --- */
@media (max-width: 1200px) {
  .search-results-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
}

@media (max-width: 880px) {
  .search-results-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }
}

@media (max-width: 580px) {
  .search-results-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .job-card-wrapper {
    padding: 15px;
    /* 在單列時可以給更多 padding */
  }
}
</style>
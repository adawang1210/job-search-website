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
// 導入您在 home.js 中定義的真實 API 函數
import { searchJobsApi, likeJob as likeJobApi, unlikeJob as unlikeJobApi } from '@/api/home.js'; // 確保路徑正確

export default {
  name: 'SearchResult',
  inject: ['openRightSidebar', 'updateLikedItemInSidebar', 'addViewedItemToSidebar'],
  data() {
    return {
      searchQuery: '',
      activePositions: [],
      activeRegions: [],
      searchResults: [], // 儲存從 API 獲取的完整結果
      isLoading: false,
      error: null,
      defaultImage: 'https://via.placeholder.com/150/CCCCCC/FFFFFF?Text=No+Image', // 預設圖片
      // 假設的登入狀態，您需要根據您的實際應用來實現
      // isUserLoggedIn: true, // 或者從 store, localStorage 等地方獲取
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
  methods: {
    async fetchSearchResults() {
      // 修改執行條件：只要任一條件存在就搜尋
      if (!this.searchQuery && this.activePositions.length === 0 && this.activeRegions.length === 0) {
        // 如果所有條件都為空，可以選擇清空結果或顯示提示，然後返回
        this.searchResults = [];
        this.isLoading = false; // 確保重置 loading 狀態
        // 可以在 p v-else-if 中處理 "請輸入關鍵字或選擇篩選條件進行搜尋"
        return;
      }

      this.isLoading = true;
      this.error = null;
      // this.searchResults = []; // 可以在 watch 中清空

      console.log(`準備根據關鍵字 "${this.searchQuery}" 獲取搜尋結果...`);
      try {
        console.log(`準備根據以下條件獲取搜尋結果:
          關鍵字: "${this.searchQuery}",
          職務: "${this.activePositions.join(', ')}",
          地區: "${this.activeRegions.join(', ')}"`
        );
         const criteria = {
          keyword: this.searchQuery,
          positions: this.activePositions, // 這些是陣列
          regions: this.activeRegions     // 這些是陣列
        };

        const apiResponse = await searchJobsApi(criteria);

              // 處理 apiResponse (假設 searchJobsApi 返回 { jobs: [], pagination: ... })
        if (apiResponse && Array.isArray(apiResponse.jobs)) {
          this.searchResults = apiResponse.jobs.map(job => ({ // home.js 中的 searchJobsApi 已經做了 transform
            ...job,
            // 如果 isLiked 不是由 searchJobsApi 的 transformJobDataMinimal 處理，
            // 或者您希望在這裡根據其他來源（例如 localStorage）再次確認，
            // 否則可以直接使用 job.isLiked
            isLiked: job.isLiked !== undefined ? job.isLiked : false,
          }));
          // this.paginationData = apiResponse.pagination; // 如果您需要處理分頁
          if (this.searchResults.length === 0 && (this.searchQuery || this.activePositions.length > 0 || this.activeRegions.length > 0)) {
              // 提示已在模板中處理
          }
        } else {
          console.warn("API 回傳格式非預期 (SearchResult.vue):", apiResponse);
          this.searchResults = [];
          // this.paginationData = null;
          this.error = '無法獲取搜尋結果，回傳格式不正確。'; // 或其他合適的錯誤訊息
        }
      } catch (err) {
        console.error("搜尋時發生錯誤:", err);
        this.error = '搜尋時發生錯誤，請稍後再試。';
        this.searchResults = [];
      } finally {
        this.isLoading = false;
      }
    },
    handleCardClick(job) {
      const dataForSidebar = job.originalData || job; // Home.vue 的習慣
      if (typeof this.addViewedItemToSidebar === 'function') {
        this.addViewedItemToSidebar(dataForSidebar);
      }
      if (typeof this.openRightSidebar === 'function') {
        this.openRightSidebar(dataForSidebar);
      }
    },
    async toggleLike(job) {
      if (!this.isUserLoggedIn) {
        alert('您需要先登入才能收藏職缺！');
        // 導向登入頁面
        // if (this.$router) { this.$router.push({ path: '/login' }); }
        return;
      }

      const originalLikedStatus = job.isLiked;
      const newLikedStatus = !job.isLiked;

      // 樂觀更新 UI
      job.isLiked = newLikedStatus;

      try {
        // **修改此處：調用真實的 API 函數**
        if (newLikedStatus) { // 或者 job.isLiked (因為已經樂觀更新了)
          await likeJobApi(job.id);
        } else {
          await unlikeJobApi(job.id);
        }

        if (typeof this.updateLikedItemInSidebar === 'function') {
          this.updateLikedItemInSidebar(job.originalData || job, newLikedStatus);
        }
      } catch (error) {
        console.error(`Error toggling like status for job ID ${job.id}:`, error);
        // API 失敗，恢復 UI 狀態
        job.isLiked = originalLikedStatus;
        alert(`更新 "${job.title}" 的收藏狀態失敗，請稍後再試。`);
        // 可以在此處處理特定錯誤，如 token 失效等
      }
    },
    handleTitleClick(job) {
      // 與 Home.vue 保持一致的行為，例如導航到公司頁面
      // 這裡可以先 console.log 或 alert
      console.log('Title clicked for job:', job.title, 'Company:', job.company);
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
  /* 與 Home.vue .middle-content 類似背景 */
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
  /* 針對 "你搜尋的是：" 和 "請輸入關鍵字" 的段落 */
  margin-bottom: 15px;
  font-size: 1em;
}


/* --- 網格佈局 --- */
.search-results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  /* 響應式，最小260px，嘗試填滿4列 */
  gap: 20px;
  /* 卡片間距 */
  padding-top: 10px;
}

/* --- 複製自 Home.vue 的 JOB CARD STYLES 並稍作調整 --- */
.job-card-wrapper {
  display: flex;
  flex-direction: column;
  background-color: transparent; /* 或 #594f4f00 */
  border-radius: 5px;
  padding: 10px 15px; /* 上下10px，左右15px，您可以根據喜好調整 */
  box-sizing: border-box;
  color: white;
  transition: transform 0.3s ease-out, box-shadow 0.3s ease-out, background-color 0.3s ease-out;
  cursor: pointer;
  min-width: 0;
}

.job-card-wrapper:hover {
  background-color: #524a4a;
  /* hover 時的背景色 */
  transform: translateY(-3px);
  /* 稍微上浮 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);
  /* 移除了 width 變化，因為在網格中會導致佈局問題 */
}

.job-card-title {
  font-size: 15px;
  font-weight: bold;
  margin-top: 0;       /* 與頂部無額外間距 */
  margin-bottom: 8px;  /* 標題與圖片之間的間距，可微調 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 150px;        /* 與圖片寬度一致 */
}

.job-card-title:hover {
  text-decoration: underline;
}

.job-card-image {
  width: 150px;        /* **修改**: 與標題寬度一致 */
  height: 150px;       /* **修改**: 保持正方形 */
  background-color: white; /* 占位符背景 */
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 5px;
  margin-bottom: 8px;  /* 圖片與下方詳情的間距 */
}

.job-card-details {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  width: 100%;        /* 占滿卡片padding內的寬度 */
  margin-top: auto;   /* 如果卡片內容高度不一致，確保details部分在底部 */
}

.job-card-info-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* 文字左對齊 */
  text-align: left;
  overflow: hidden;
  padding-right: 8px; /* 與愛心按鈕之間留點空隙 */
  flex-grow: 1; /* 佔據剩餘空間 */
}

.job-card-company,
.job-card-salary {
  font-size: 13px;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%; /* 佔滿 .job-card-info-left 的寬度 */
}

.job-card-company {
  font-weight: bold;
}

.job-card-salary {
  font-size: 12px;
  color: #E0E0E0;
  margin-top: 2px;
}

.job-card-like-btn.like-btn { /* .like-btn 已有通用樣式，這裡可微調 */
  display: flex;
  align-items: center; /* 確保愛心垂直居中（如果按鈕有高度） */
  font-size: 18px;
  flex-shrink: 0; /* 防止按鈕被壓縮 */
  /* align-self: flex-end; /* .job-card-details 的 align-items: flex-end 已經處理了底部對齊 */
}

/* --- 收藏按鈕通用樣式 (來自 Home.vue，保持一致) --- */
.like-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: white;
  font-size: 18px; /* 與 .job-card-like-btn 中的一致 */
  padding: 0; /* 移除預設 padding */
  transition: transform 0.2s ease, color 0.2s ease;
}

.like-btn:hover {
  transform: scale(1.15);
}

.like-btn.active {
  color: rgb(235, 178, 189); /* 粉色實心 */
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
    padding: 15px; /* 在單列時可以給更多 padding */
  }
}
</style>
<template>
  <div class="all-companies-container">
    <div v-if="isLoadingCompanies" class="loading-message">
      正在載入優質企業...
    </div>
    <div v-if="errorCompanies" class="error-message">
      {{ errorCompanies }}
    </div>
    <template v-if="!isLoadingCompanies && !errorCompanies">
      <div v-if="companies.length > 0" class="company-grid">
        <div class="content-wrapper" v-for="(company, cIndex) in companies" :key="'company-' + cIndex"
          @click="handleCompanyCardClick(company)">
          <div class="company-icon" :style="{ backgroundImage: 'url(' + company.image + ')' }"></div>
          <div class="job-card-details">
            <p class="company-name">{{ company.name }}</p>
            <button type="button" class="like-btn job-card-like-btn" :class="{ active: company.isLiked }"
              @click.stop="toggleLike(company)">
              <font-awesome-icon :icon="[company.isLiked ? 'fas' : 'far', 'heart']" class="heart-icon" />
            </button>
          </div>
        </div>
      </div>
      <div v-else class="no-data-message">
        目前沒有優質企業資料。
      </div>
    </template>
  </div>
</template>

<script>
import { getGreatCompanies, likeJob, unlikeJob } from '@/api/home.js'; // 假設您的 API 函數在此
import eventBus from '/src/eventBus.js';

const ITEM_TYPE_COMPANY = 'company';

export default {
  name: 'AllCompany',
  inject: ['updateLikedItemInSidebar'],
  data() {
    return {
      companies: [],
      isLoadingCompanies: false,
      errorCompanies: null,
    };
  },
  async mounted() {
    this.loadCompaniesData();
    // 【新增】監聽來自 BaseLayout 或其他頁面的愛心狀態更新事件
    eventBus.on('update-like-status', this.handleUpdateLikeStatus);
  },
  beforeUnmount() {
    // 【新增】在組件銷毀前移除事件監聽器
    eventBus.off('update-like-status', this.handleUpdateLikeStatus);
  },
  methods: {
    async loadCompaniesData() {
      this.isLoadingCompanies = true;
      this.errorCompanies = null;
      try {
        const companiesData = await getGreatCompanies();
        const rawCompanies = companiesData.results || companiesData || [];
        
        // 【修改】映射數據，新增 isLiked 和 type 屬性
        this.companies = rawCompanies.map(company => ({
          id: company.id,
          name: company.name,
          image: company.media && company.media.logo ? company.media.logo : 'default_company_logo_path.png',
          isLiked: company.is_liked_by_user || false, // 假設後端 API 返回 is_liked_by_user
          originalData: { ...company, type: ITEM_TYPE_COMPANY }, // 【新增】在 originalData 中加入 type
          type: ITEM_TYPE_COMPANY, // 【新增】在頂層也保留 type，方便直接使用 company 物件
        }));
      } catch (error) {
        console.error('Error fetching companies:', error);
        if (error.message && error.message.toLowerCase().includes('network error')) {
          this.errorCompanies = '無法載入企業資訊，請檢查網路連線。';
        } else {
          this.errorCompanies = '載入企業資訊失敗，請稍後再試。';
        }
      } finally {
        this.isLoadingCompanies = false;
      }
    },
     // 【新增】通用 toggleLike 方法 (與 Home.vue 中的邏輯一致)
    async toggleLike(company) { // 這裡的 company 就是 item
      // 假設需要登入才能收藏
      // if (!this.isUserLoggedIn) { 
      //   alert('您需要先登入才能收藏！');
      //   return;
      // }

      if (!company || !company.id || company.type !== ITEM_TYPE_COMPANY) { // 【新增】檢查 type
        console.error('toggleLike: 無效的公司數據或類型不符', company);
        return;
      }

      const originalLikedStatus = company.isLiked;
      const newLikedStatus = !company.isLiked;

      // 1. 樂觀更新 UI
      company.isLiked = newLikedStatus;

      try {
        // 2. 呼叫後端 API (統一使用 likeJob/unlikeJob)
        // 假設 likeJob/unlikeJob API 能處理公司 ID
        if (newLikedStatus) {
          await likeJob(company.id); 
        } else {
          await unlikeJob(company.id);
        }

        // 3. 通知 BaseLayout 更新側邊欄的收藏列表
        // 傳遞公司原始數據 (company.originalData) 和新的 isLiked 狀態
        if (typeof this.updateLikedItemInSidebar === 'function') {
          this.updateLikedItemInSidebar(company.originalData || company, newLikedStatus); 
        }
        
        // 4. 透過 eventBus 通知所有頁面同步愛心狀態
        // 統一事件名稱 'update-like-status'，並傳遞 ID, 類型, 和新狀態
        eventBus.emit('update-like-status', { id: company.id, type: company.type, isLiked: newLikedStatus });

      } catch (error) {
        console.error(`Failed to update company like status for ID ${company.id}:`, error);
        // API 失敗，恢復 UI 狀態
        company.isLiked = originalLikedStatus;
        alert(`收藏公司操作失敗，請稍後再試。`);

        // 恢復 BaseLayout 列表狀態
        if (typeof this.updateLikedItemInSidebar === 'function') {
          this.updateLikedItemInSidebar(company.originalData || company, originalLikedStatus);
        }
        // 通知所有頁面恢復愛心狀態
        eventBus.emit('update-like-status', { id: company.id, type: company.type, isLiked: originalLikedStatus });
      }
    },
    // 【新增】處理來自 eventBus 的愛心狀態更新事件
    // 這個方法會接收一個包含 { id: itemId, type: itemType, isLiked: newStatus } 的數據物件
    handleUpdateLikeStatus(data) {
      const { id, type, isLiked } = data;
      // AllCompany 頁面只顯示公司，所以只處理 ITEM_TYPE_COMPANY 類型
      if (type === ITEM_TYPE_COMPANY) {
        const companyToUpdate = this.companies.find(company => company.id === id);
        if (companyToUpdate) {
          companyToUpdate.isLiked = isLiked;
        }
      }
    },

    handleCompanyCardClick(company) {
      console.log('Company card clicked:', company);
      // 假設您有一個路由到公司頁面，並且需要公司ID
      this.$router.push({ name: 'company', params: { id: company.id } });
    },
  },
};
</script>

<style scoped>
/* AllCompany.vue 的樣式修改 */
.all-companies-container {
  display: flex;
  flex-direction: column;
  padding: 20px;
  background-color: #383333;
  /* 深灰色背景 */
  color: white;
  min-height: 100vh;
  /* 確保內容撐開整個頁面 */
  box-sizing: border-box;
  /* ==== 新增這四行，讓它有圓角效果 ==== */
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
  /* ================================== */
}

.company-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  /* 響應式網格佈局 */
  gap: 25px;
  /* 增大間距 */
  width: 100%;
  justify-items: center;
  /* 讓每個項目在網格單元格中居中 */
  padding: 0 15px;
  /* 左右內邊距 */
  box-sizing: border-box;
}

/* 從 Home.vue 複製過來的公司卡片樣式 */
.content-wrapper {
  display: flex;
  flex-direction: column;
  background-color: #594f4f00;
  /* 保持透明 */
  border-radius: 5px;
  padding: 10px 25px;
  width: 250px;
  /* 固定寬度，或調整為響應式 */
  box-sizing: border-box;
  color: white;
  transition: transform 0.5s ease-out,
    /* 加快過渡速度 */
    box-shadow 0.5s ease-out,
    background-color 0.5s ease-out;
  cursor: pointer;
}

.content-wrapper:hover {
  background-color: #594f4f;
  transform: translateY(-3px) scale(1.02);
  /* 輕微放大效果 */
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.4);
  /* 更明顯的陰影 */
}

.company-icon {
  width: 200px;
  height: 200px;
  border-radius: 5px;
  background-color: #ffffff;
  background-size: cover;
  background-position: center;
  border: none;
  padding: 0;
  flex-shrink: 0;
  margin-bottom: 8px;
  /* 增加與名稱的間距 */
}

.company-name {
  font-size: 16px;
  /* 稍大一點 */
  font-weight: bold;
  color: white;
  margin: 0;
  /*text-align: center;*/
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  width: 100%;
  /* 確保文本寬度與父容器對齊 */
}

/* 消息提示樣式 */
.loading-message,
.error-message,
.no-data-message {
  padding: 20px;
  text-align: center;
  color: #ccc;
  width: 100%;
  box-sizing: border-box;
  margin-top: 20px;
}

.error-message {
  color: #ffffff;
  background-color: rgba(128, 128, 128, 0.1);
  border: 1px solid rgba(211, 211, 211, 0.3);
  border-radius: 5px;
  margin: 20px auto;
  /* 居中顯示 */
  max-width: 600px;
  /* 限制寬度 */
}

.loading-message {
  font-style: italic;
}

.job-card-details {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  width: 100%;
}

/* 收藏按鈕通用樣式 */
.like-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: white;
  font-size: 18px;
  padding: 0px;
  transition: transform 0.5s ease, color 0.3s ease;
}

.like-btn:hover {
  transform: scale(1.1);
}

.like-btn.active {
  color: rgb(235, 178, 189);
}
</style>
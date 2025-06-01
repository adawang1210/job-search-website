<template>
  <div class="middle-content">
    <section class="recommend" v-for="(section, index) in sections" :key="index">
      <h1>{{ section.title }}</h1>

      <div v-if="section.isLoading" class="loading-message">
        正在載入 {{ section.title }}...
      </div>

      <div v-if="section.error" class="error-message">
        {{ section.error }}
      </div>

      <template v-if="!section.isLoading && !section.error">
        <div v-if="section.jobs.length > 0" class="recommend-content" @mousedown="startDrag" @mousemove="onDrag"
          @mouseup="stopDrag" @mouseleave="stopDrag" :class="{ active: isDragging }">
          <div class="job-card-wrapper" v-for="(job, jobIndex) in section.jobs" :key="job.id || jobIndex"
            @click="handleCardClick(job)">
            <p class="job-card-title" @click.stop="handleTitleClick(job)">{{ job.title }}</p>
            <div class="job-card-image" :style="{ backgroundImage: 'url(' + job.image + ')' }"></div>
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
        <div v-else class="no-data-message">
          目前沒有 {{ section.title }} 的職缺。
        </div>
      </template>
    </section>

    <section class="love-job-section">
      <h1>最愛行業</h1>
      <div class="love-job-content" @mousedown="startDrag" @mousemove="onDrag" @mouseup="stopDrag"
        @mouseleave="stopDrag" :class="{ active: isDragging }">
        <div class="love-job-card" v-for="(item, index) in loveJobItems" :key="'love-job-' + index"
          :style="{ backgroundImage: 'url(\'/love-job-frame.png\')' }" @click="handleLoveCardClick(item.id)">
          <img :src="item.image" :alt="item.name" class="love-job-photo">
          <p class="love-job-name">{{ item.name }}</p>
        </div>
      </div>
    </section>

    <section class="great-company">
      <h1>優質企業</h1>
      <div v-if="isLoadingCompanies" class="loading-message">
        正在載入優質企業...
      </div>
      <div v-if="errorCompanies" class="error-message">
        {{ errorCompanies }}
      </div>
      <template v-if="!isLoadingCompanies && !errorCompanies">
        <div v-if="companies.length > 0" class="recommend-content" @mousedown="startDrag" @mousemove="onDrag"
          @mouseup="stopDrag" @mouseleave="stopDrag" :class="{ active: isDragging }">
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
    </section>

    <section class="favorite-job-section">
      <h1>最愛職缺</h1>
      <template v-if="favoriteJobs.length > 0">
        <div class="favorite-job-grid">
          <div class="favorite-job-card" v-for="(favJob, fIndex) in favoriteJobs" :key="favJob.id || 'favjob-' + fIndex"
            :style="{ backgroundImage: 'url(' + favJob.image + ')' }" @click="handleFavoriteJobCardClick(favJob)">
            <div class="card-overlay-content">
              <div class="card-top-info">
                <div class="favorite-job-icon" :style="{ backgroundImage: 'url(' + favJob.icon + ')' }" @click.stop>
                </div>
                <p class="favorite-job-name" @click.stop>{{ favJob.name }}</p>
              </div>
              <p class="favorite-job-description" @click.stop>{{ favJob.description }}</p>
            </div>
          </div>
        </div>
      </template>
      <div v-else class="no-data-message">
        目前沒有最愛職缺資料。
      </div>
    </section>
  </div>
</template>



<script>
import eventBus from '/src/eventBus.js';
import { getJobs, getGreatCompanies, getJobDetail, updateLikedCompanies } from '@/api/home.js';

const ITEM_TYPE_JOB = 'job';
const ITEM_TYPE_COMPANY = 'company';

export default {
  name: 'Home',
  inject: ['openRightSidebar', 'updateLikedItemInSidebar', 'addViewedItemToSidebar','isItemCurrentlyLiked'],
  data() {
    return {
      isDragging: false,
      startX: 0,
      scrollLeft: 0,
      sections: [
        {
          title: '為你推薦',
          jobs: [],
          isLoading: false,
          error: null,
        },
        {
          title: '熱門職缺',
          jobs: [],
          isLoading: false,
          error: null,
        },
        {
          title: '最新職缺',
          jobs: [],
          isLoading: false,
          error: null,
        },
      ],
      loveJobItems: [
        { id: 'love_job_1', name: '航空業', image: '/love-job-1.jpg' },
        { id: 'love_job_2', name: '傳統產業', image: '/love-job-2.jpg' },
        { id: 'love_job_3', name: '家具業', image: '/love-job-3.jpg' },
        { id: 'love_job_4', name: '電子產品製造業', image: '/love-job-4.jpg' },
        { id: 'love_job_5', name: '餐飲服務業', image: '/love-job-5.jpg' },
        { id: 'love_job_6', name: '速食餐飲業', image: '/love-job-6.jpg' }
      ],
      allApiJobs: [], // 用於存儲從 API 獲取並轉換格式後的所有職缺
      companies: [],
      favoriteJobs: [
        { id: 'fav_dentist', name: '最愛牙醫師', image: '/favorite-bg-1.jpg', icon: '/favorite-icon-1.png', description: '雅德斯牙醫診所、蒔美牙醫集團和更多', isLiked: false },
        { id: 'fav_designer', name: '最愛室內設計師', image: '/favorite-bg-2.jpg', icon: '/favorite-icon-2.png', description: '雅和室內設計、拾間室內裝修設計和更多', isLiked: false },
        { id: 'fav_barista', name: '最愛咖啡師', image: '/favorite-bg-3.jpeg', icon: '/favorite-icon-3.png', description: '咖碼、路易莎和更多', isLiked: false },
        { id: 'fav_baker', name: '最愛烘焙技師', image: '/favorite-bg-4.jpg', icon: '/favorite-icon-4.png', description: '歐立食品、亞尼克和更多', isLiked: false },
        { id: 'fav_engineer', name: '最愛半導體工程師', image: '/favorite-bg-5.jpg', icon: '/favorite-icon-5.png', description: 'nvidia台灣分公司、台積電和更多', isLiked: false },
        { id: 'fav_staff', name: '最愛門市人員', image: '/favorite-bg-6.jpg', icon: '/favorite-icon-6.png', description: '宜得利、無印良品和更多', isLiked: false }
      ],
      isLoadingCompanies: false,
      errorCompanies: null,
    };
  },
  async mounted() {
    this.loadInitialData(); // 2. 組件掛載時獲取數據
    eventBus.on('update-like-status', this.handleUpdateLikeStatus);
  },
  beforeUnmount() {
    eventBus.off('update-like-status', this.handleUpdateLikeStatus);
  },
  methods: {
    async loadInitialData() {
      try {
        const [jobsData, companiesData] = await Promise.all([
          getJobs(),
          getGreatCompanies(),
        ]);

        // 處理職缺數據
        const rawJobs = jobsData.results || jobsData || [];
        this.allApiJobs = rawJobs.map(job => ({
          id: job.id,
          title: job.title,
          image: job.company_logo?.startsWith('http') 
            ? job.company_logo 
            : 'http://localhost:8000/' + (job.company_logo || 'default_job_image.png'),
          company: job.company && job.company.name ? job.company.name : '未知公司',
          salary: job.salary_max ? `$${job.salary_max}` : '面議',
          isLiked: job.is_liked_by_user || false, // 初始收藏狀態來自後端
          originalData: { ...job, type: ITEM_TYPE_JOB }, // 【修改】在原始數據中加入 type 屬性
          type: ITEM_TYPE_JOB, // 【新增】在頂層也保留 type，方便直接使用 job 物件
        }));
        this.distributeJobsRandomly();

        // 處理企業數據
        const rawCompanies = companiesData.results || companiesData || [];
        this.companies = rawCompanies.map(company => ({
          id: company.id,
          name: company.name,
          image: company.media && company.media.logo ? company.media.logo : 'default_company_logo_path.png',
          isLiked: company.is_liked_by_user || false, // 【新增】初始化公司的收藏狀態
          originalData: { ...company, type: ITEM_TYPE_COMPANY }, // 【修改】在原始數據中加入 type 屬性
          type: ITEM_TYPE_COMPANY, // 【新增】在頂層也保留 type，方便直接使用 company 物件
        }));

        // 【新增】在所有數據加載並處理完畢後，執行一次全局愛心狀態同步
        // 確保所有職缺和公司的 isLiked 狀態與 BaseLayout (localStorage) 保持一致
        if (typeof this.isItemCurrentlyLiked === 'function') {
            // 同步職缺的 isLiked 狀態
            this.sections.forEach(section => {
                section.jobs.forEach(job => {
                    job.isLiked = this.isItemCurrentlyLiked(job.id, job.type);
                });
            });
            // 同步公司的 isLiked 狀態
            this.companies.forEach(company => {
                company.isLiked = this.isItemCurrentlyLiked(company.id, company.type);
            });
        } else {
            console.warn('Home.vue: isItemCurrentlyLiked method not injected, initial liked status might be inaccurate.');
        }

      } catch (error) {
        console.error('Error fetching initial data:', error);
        let jobErrorOccurred = false;
        let companyErrorOccurred = false;
        if (error.message && error.message.toLowerCase().includes('network error')) {
          jobErrorOccurred = true;
          companyErrorOccurred = true;
        } else if (error.config && error.config.url) {
          if (error.config.url.includes('/api/jobs')) jobErrorOccurred = true;
          if (error.config.url.includes('/api/companies')) companyErrorOccurred = true;
        } else if (error.isAxiosError && error.request && error.request.responseURL) {
          if (error.request.responseURL.includes('/api/jobs')) jobErrorOccurred = true;
          if (error.request.responseURL.includes('/api/companies')) companyErrorOccurred = true;
        } else {
          jobErrorOccurred = true;
          companyErrorOccurred = true;
        }

        if (jobErrorOccurred) {
          this.sections.forEach(section => {
            section.error = '無法載入職缺資訊，請稍後再試。';
          });
        }
        if (companyErrorOccurred) {
          this.errorCompanies = '無法載入企業資訊，請稍後再試。';
        }

        if (!this.sections.some(s => s.error) && !this.errorCompanies && (jobErrorOccurred || companyErrorOccurred)) {
          const generalErrorMsg = '資料載入失敗，請檢查網路連線或稍後重試。';
          this.sections.forEach(section => {
            if (!section.error) section.error = generalErrorMsg;
          });
          if (!this.errorCompanies) this.errorCompanies = generalErrorMsg;
        }

      } finally {
        this.sections.forEach(section => section.isLoading = false);
        this.isLoadingCompanies = false;
      }
    },

    distributeJobsRandomly() {
      if (!this.allApiJobs.length) return;

      let availableJobs = [...this.allApiJobs]; // 創建一個可修改的副本

      // 打亂職缺順序
      for (let i = availableJobs.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [availableJobs[i], availableJobs[j]] = [availableJobs[j], availableJobs[i]];
      }

      // 為每個區塊分配職缺，盡量不重複，且數量可自訂
      const jobsPerSection = 6; // 您希望每個區塊顯示的職缺數量

      this.sections.forEach(section => {
        section.jobs = []; // 清空現有職缺
        // 從打亂後的職缺中取N個，如果職缺不夠，則取剩餘所有
        const jobsForThisSection = availableJobs.splice(0, Math.min(jobsPerSection, availableJobs.length));
        section.jobs = jobsForThisSection;
      });
    },

    // item 可能是 job 或 company 物件，它已經包含 isLiked 和 originalData (其中包含 type)
    async toggleLike(item) {

      if (!item || !item.id || !item.type) {
        console.error('toggleLike: 無效的項目數據或缺少 ID/類型', item);
        return;
      }

      const originalLikedStatus = item.isLiked;
      const newLikedStatus = !item.isLiked;

      // 1. 樂觀更新 UI (直接修改傳入的 item 物件)
      item.isLiked = newLikedStatus;

      // 2. 立即通知 BaseLayout 更新側邊欄和 localStorage
      // 這對於職缺（無需 API）和公司（需等待 API 回應）都是立即更新的
      if (typeof this.updateLikedItemInSidebar === 'function') {
        this.updateLikedItemInSidebar(item.originalData || item, newLikedStatus); 
      }
      // 立即透過 eventBus 通知所有頁面同步愛心狀態
      eventBus.emit('update-like-status', { id: item.id, type: item.type, isLiked: newLikedStatus });

      try {
        // 3. 區分呼叫 API 還是只處理前端邏輯
        if (item.type === ITEM_TYPE_JOB) {
          // 職缺：只處理前端，無需呼叫後端 API
          // 如果這裡需要等待任何非同步操作，例如動畫，可以在這裡加 await new Promise(...)
        } else if (item.type === ITEM_TYPE_COMPANY) {
          // 公司：呼叫後端 API
          await updateLikedCompanies(item.id, newLikedStatus);
        } else {
          console.warn(`toggleLike: 未知的項目類型 ${item.type}，未呼叫 API。`);
        }

      } catch (error) {
        console.error(`Failed to update ${item.type} like status for ID ${item.id}:`, error);
        /// 只有公司收藏 API 失敗時才需要回滾
        if (item.type === ITEM_TYPE_COMPANY) {
          item.isLiked = originalLikedStatus; // 回滾 Home.vue 自己的 isLiked 狀態
          alert(`收藏公司操作失敗！請稍後再試。\n錯誤訊息: ${error.message || error}`);

          // 通知 BaseLayout 回滾列表狀態
          if (typeof this.updateLikedItemInSidebar === 'function') {
            this.updateLikedItemInSidebar(item.originalData || item, originalLikedStatus); 
          }
          // 通知所有頁面回滾愛心狀態
          eventBus.emit('update-like-status', { id: item.id, type: item.type, isLiked: originalLikedStatus });
        } else {
          // 職缺：API 失敗不會發生，所以這裡理論上不會觸發。
          // 但為了安全，如果觸發，可以顯示通用錯誤。
          console.warn(`職缺收藏錯誤，但沒有 API 呼叫。可能為其他邏輯錯誤：${error.message || error}`);
        }
      }
    },

    // 處理來自 eventBus 的通用愛心狀態更新事件
    handleUpdateLikeStatus(data) { // data 預期為 { id: itemId, type: itemType, isLiked: newStatus }
      const { id, type, isLiked } = data;
      // 1. 更新 sections 中的職缺愛心狀態
      if (type === ITEM_TYPE_JOB) {
        this.sections.forEach(section => {
          const jobInSection = section.jobs.find(j => j.id === id);
          if (jobInSection) {
            jobInSection.isLiked = isLiked;
          }
        });
      }
      // 2. 更新 companies 中的公司愛心狀態
      else if (type === ITEM_TYPE_COMPANY) {
        const companyToUpdate = this.companies.find(c => c.id === id);
        if (companyToUpdate) {
          companyToUpdate.isLiked = isLiked;
        }
      }
    },

    startDrag(e) {
      const RContent = e.currentTarget;
      this.isDragging = true;
      this.startX = e.pageX - RContent.offsetLeft;
      this.scrollLeft = RContent.scrollLeft;
      // RContent.classList.add('active'); // 如果模板中有 .active 樣式可以加上
    },
    onDrag(e) {
      if (!this.isDragging) return;
      e.preventDefault();
      const RContent = e.currentTarget;
      const x = e.pageX - RContent.offsetLeft;
      const walk = (x - this.startX) * 2; // 可以調整滑動速度
      RContent.scrollLeft = this.scrollLeft - walk;
    },
    stopDrag(e) {
      // const RContent = e.currentTarget;
      this.isDragging = false;
      // RContent.classList.remove('active');
    },

    handleCardClick(jobData) {
      // jobData 已經是 Home.vue 內部處理過的格式，包含 originalData 和 type
      const dataForSidebar = jobData.originalData || jobData; // 確保取得原始 API 數據
      if (typeof this.addViewedItemToSidebar === 'function') {
        this.addViewedItemToSidebar(dataForSidebar); // 傳遞原始職缺數據給瀏覽紀錄
      }
      if (typeof this.openRightSidebar === 'function') {
        this.openRightSidebar(dataForSidebar); // 傳遞原始職缺數據給右側邊欄
      }
    },
    handleTitleClick(job) {
      this.$router.push({ name: 'jobdetail', params: { id: job.id } });
    },
    handleCompanyCardClick(company) {
      // 這個方法只處理公司卡片點擊和路由導向，不會開啟右側邊欄或新增到已瀏覽
      this.$router.push({ name: 'company', params: { id: company.id } });
    },
    handleLoveCardClick(loveId) {
      this.$router.push({ name: 'favoritejobs', params: { id: loveId } });
    }
  }
}
</script>

<style scoped>
/* 中央內容框架樣式 */
.middle-content {
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  box-sizing: border-box;
  background-color: #383333;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  border-bottom-right-radius: 0;
  /* 下方圓角設為 0 */
  border-bottom-left-radius: 0;
  /* 下方圓角設為 0 */
  color: white;
  gap: 10px;
  width: 100%;
  max-width: none;
}

/* 區塊標題與橫向區塊通用樣式 */
.middle-content .recommend,
.middle-content .great-company,
.middle-content .love-job-section,
.middle-content .favorite-job-section {
  display: flex;
  flex-direction: column;
  white-space: nowrap;
  gap: 8px;
  padding: 4px 25px;
}

.middle-content section h1 {
  font-size: 20px;
  padding: 8px 0px;
  color: white;
}

/* 橫向滑動內容區塊樣式 */
.middle-content .recommend-content {
  display: flex;
  flex-direction: row;
  gap: 10px;
  overflow-x: auto;
  flex-wrap: nowrap;
  box-sizing: border-box;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  cursor: grab;
  scrollbar-width: none;
  -ms-overflow-style: none;
  padding-bottom: 10px;
}

.middle-content .love-job-content {
  display: flex;
  flex-direction: row;
  gap: 10px;
  overflow-x: auto;
  flex-wrap: nowrap;
  box-sizing: border-box;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  cursor: grab;
  scrollbar-width: none;
  -ms-overflow-style: none;
  padding: 0px 10px 10px 0px;
  transition: transform 0.5s ease-out,
    box-shadow 0.5s ease-out,
    background-color 0.5s ease-out;
}

.middle-content .recommend-content::-webkit-scrollbar,
.middle-content .love-job-content::-webkit-scrollbar {
  display: none;
}


/* --- MODIFIED JOB CARD STYLES START --- */
.job-card-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #594f4f00;
  border-radius: 5px;
  padding: 10px 25px 10px 25px;
  width: 280px;
  box-sizing: border-box;
  color: white;
  text-align: center;
  transition: transform 0.5s ease-out,
    box-shadow 0.5s ease-out,
    background-color 0.5s ease-out,
    width 0.5s ease-out;
  cursor: pointer;
}

.job-card-wrapper:hover {
  background-color: #594f4f;
  transform: translateY(-1px);
  box-shadow: 0 8px 8px rgba(0, 0, 0, 0.3);
  width: 350px;
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
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 5px;
  margin-bottom: 5px;
}

.job-card-details {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  width: 100%;
}

.job-card-info-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
  padding-right: 8px;
}

.job-card-company {
  font-size: 13px;
  font-weight: bold;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
}

.job-card-salary {
  font-size: 12px;
  color: #E0E0E0;
  margin-top: -2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.job-card-like-btn.like-btn {
  display: flex;
  font-size: 18px;
  align-self: flex-end;
  margin-right: 6px;
}

/* --- LOVE JOB SECTION STYLES START --- */
.love-job-section .love-job-content .love-job-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  position: relative;
  width: 250px;
  height: 210px;
  background-color: #594f4f00;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 15px;
  box-sizing: border-box;
  color: white;
  cursor: pointer;
  transition: transform 0.5s ease-out,
    box-shadow 0.5s ease-out,
    background-color 0.5s ease-out;
  flex-shrink: 0;
}

.love-job-section .love-job-content .love-job-card:hover {
  background-color: #594f4f;
  /* 與 great-company 一致 */
  border-radius: 4px;
  transform: translateY(-1px);
  /* 與 great-company 一致 */
  box-shadow: 0 8px 8px rgba(0, 0, 0, 0.3);
  /* 與 great-company 一致 */
}

.love-job-section .love-job-photo {
  width: 160px;
  /* Occupy padded space */
  height: 130px;
  /* Adjust based on your frame image, leaves space for name */
  margin-top: 24px;
  /* Adjust as needed */
}

.love-job-section .love-job-name {
  position: absolute;
  left: 15px;
  /* Align with padding */
  right: 15px;
  /* Align with padding */
  top: 175px;
  font-size: 16px;
  font-weight: bold;
  color: white;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  z-index: 1;
  /* Ensure it's above the photo if photo positioning is tricky */
}

/* --- LOVE JOB SECTION STYLES END --- */

.middle-content .great-company .recommend-content .content-wrapper:hover {
  background-color: #594f4f;
  transform: translateY(-1px);
  box-shadow: 0 8px 8px rgba(0, 0, 0, 0.3);
  width: 250px;
}

/* 優質企業圖示樣式 (great-company section) */
.middle-content .great-company .company-icon {
  width: 200px;
  height: 200px;
  border-radius: 5px;
  background-color: #ffffff;
  background-size: cover;
  background-position: center;
  border: none;
  padding: 0;
  flex-shrink: 0;
}

/* 優質企業公司名稱樣式 (great-company section) */
.middle-content .great-company .recommend-content .content-wrapper .company-name {
  font-size: 14px;
  font-weight: bold;
  color: white;
  margin-top: 6px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  width: 200px;
}

.favorite-job-section {
  margin-bottom: 20px;
}

.favorite-job-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
  width: 100%;
}

.favorite-job-card {
  aspect-ratio: 16 / 10;
  border-radius: 4px;
  max-width: 320px;
  /* 例如 */
  min-height: 320px;
  width: 100%;
  /* 確保它能縮小 */
  background-size: cover;
  background-position: center;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease-out, box-shadow 0.3s ease-out;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 18px;
  box-sizing: border-box;
}

.favorite-job-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.35);
  border-radius: inherit;
  z-index: 1;
  transition: background-color 0.3s ease;
}

.favorite-job-card:hover {
  transform: translateY(-3px) scale(1.01);
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.25);
}

.favorite-job-card:hover::before {
  background-color: rgba(0, 0, 0, 0.2);
}

.card-overlay-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  color: white;
}

.card-top-info {
  display: flex;
  align-items: flex-start;
  margin-left: -20px;
}

.favorite-job-icon {
  width: 100px;
  height: 100px;
  background-size: contain;
  background-repeat: no-repeat;
  border-radius: 4px;
  flex-shrink: 0;
}

.favorite-job-name {
  font-size: 15px;
  font-weight: bold;
  margin: 0;
  padding-top: 15px;
  margin-left: -10px;
}

.favorite-job-description {
  font-size: 13px;
  line-height: 1.5;
  color: #e0e0e0;
  margin: 0;
  align-self: flex-start;
  margin-top: auto;
  width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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

.heart-icon {
  transition: color 0.3s ease;
}

.middle-content .recommend-content.active {
  cursor: grabbing;
  user-select: none;
}

.middle-content .great-company .recommend-content .content-wrapper {
  display: flex;
  flex-direction: column;
  background-color: #594f4f00;
  border-radius: 5px;
  padding: 10px 25px;
  width: 250px;
  box-sizing: border-box;
  color: white;
  transition: transform 0.5s ease-out,
    box-shadow 0.5s ease-out,
    background-color 0.5s ease-out;
  cursor: pointer;
}

.middle-content .favorite-job .content-container {
  cursor: pointer;
}

.loading-message,
.error-message,
.no-data-message {
  padding: 20px;
  text-align: center;
  color: #ccc;
  width: 100%;
}

.error-message {
  color: #ffffff;
  background-color: rgba(128, 128, 128, 0.1);
  border: 1px solid rgba(211, 211, 211, 0.3);
  border-radius: 5px;
  margin: 10px 0;
}

.loading-message {
  font-style: italic;
}
</style>
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
                @click.stop="toggleLike(section.title, jobIndex)">
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
            <div class="company-icon" :style="{ backgroundImage: 'url(' + company.image + ')' }" @click.stop></div>
            <p class="company-name" @click.stop>{{ company.name }}</p>
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

import {
  getRecommendedJobs,
  getHotJobs,
  getLatestJobs,
  getTopCompanies,
  likeJob,
  unlikeJob,
} from '@/api/home.js';

export default {
  name: 'Home',
  inject: ['openRightSidebar', 'updateLikedItemInSidebar', 'addViewedItemToSidebar'],
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
          apiService: getRecommendedJobs, // 對應 home.js 中的函數
          apiParams: { limit: 10 }       // 傳遞給 API 的參數 (可選)
        },
        {
          title: '熱門職缺',
          jobs: [],
          isLoading: false,
          error: null,
          apiService: getHotJobs,
          apiParams: { limit: 10, sort: 'popularity' } // 假設 API 支持這些參數
        },
        {
          title: '最新職缺',
          jobs: [],
          isLoading: false,
          error: null,
          apiService: getLatestJobs,
          apiParams: { limit: 10, sort: 'newest' }
        },
      ],
      companies: [],
      favoriteJobs: [
        { id: 'fav_dentist', name: '最愛牙醫師', image: '/favorite-bg-1.jpg', icon: '/favorite-icon-1.png', description: '雅德斯牙醫診所、蒔美牙醫集團和更多' },
        { id: 'fav_designer', name: '最愛室內設計師', image: '/favorite-bg-2.jpg', icon: '/favorite-icon-2.png', description: '雅和室內設計、拾間室內裝修設計有限公司和更多' },
        { id: 'fav_barista', name: '最愛咖啡師', image: '/favorite-bg-3.jpeg', icon: '/favorite-icon-3.png', description: '咖碼股份有限公司、路易莎職人咖啡股份有限公司和更多' },
        { id: 'fav_baker', name: '最愛烘焙技師', image: '/favorite-bg-4.jpg', icon: '/favorite-icon-4.png', description: '歐立食品股份有限公司、亞尼克菓子工房股份有限公司和更多' },
      ],
      isLoadingCompanies: false,
      errorCompanies: null,
    };
  },
  mounted() {
    eventBus.on('unlike-item-in-home-via-sidebar', this.handleUnlikeFromSidebar);
    eventBus.on('like-item-in-home-via-sidebar', this.handleLikeFromSidebar);
    this.fetchAllData();
  },
  beforeUnmount() {
    eventBus.off('unlike-item-in-home-via-sidebar', this.handleUnlikeFromSidebar);
    eventBus.off('like-item-in-home-via-sidebar', this.handleLikeFromSidebar);
  },
  methods: {
    async fetchAllData() {
      const promises = [];

      // 獲取各個職缺區塊的資料
      this.sections.forEach(section => {
        promises.push(this.fetchSectionData(section));
      });

      // 獲取優質企業資料
      promises.push(this.fetchCompaniesFromAPI());

      console.log('Starting to fetch all initial data for Home.vue...');
      try {
        await Promise.all(promises);
        console.log('All initial data for Home.vue has been loaded (or attempted).');
      } catch (error) {
        // 單個 fetch 方法內部已處理各自的錯誤狀態用於UI。
        // 此處的 catch 主要用於記錄 Promise.all 本身的失敗或未被捕獲的全局性錯誤。
        console.error('One or more initial data fetches failed globally for Home.vue:', error);
      }
    },

    async fetchSectionData(section) {
      if (!section || typeof section.apiService !== 'function') {
        console.error('無效的 section 或 apiService 未定義:', section);
        if (section) section.error = '無法載入此區塊的設定。';
        return;
      }
      section.isLoading = true;
      section.error = null;
      try {
        const jobsData = await section.apiService(section.apiParams || {});
        console.log(`Data received in Home.vue for section [${section.title}]:`, JSON.parse(JSON.stringify(jobsData))); // 使用 JSON.parse(JSON.stringify()) 來避免打印 Proxy 物件
        if (Array.isArray(jobsData) && jobsData.length > 0) {
          console.log(`First job data for [${section.title}]:`, JSON.parse(JSON.stringify(jobsData[0])));
        }
        section.jobs = jobsData;
      } catch (err) {
        console.error(`Error fetching ${section.title} for Home.vue:`, err);
        section.error = `無法載入 ${section.title} 資料，請稍後再試。`;
        section.jobs = []; // 出錯時確保 jobs 是空陣列
      } finally {
        section.isLoading = false;
      }
    },

    async fetchCompaniesFromAPI() {
      this.isLoadingCompanies = true;
      this.errorCompanies = null;
      try {
        this.companies = await getTopCompanies(); // home.js 返回已轉換的數據
      } catch (err) {
        console.error('Error fetching top companies for Home.vue:', err);
        this.errorCompanies = '無法載入優質企業資料。';
        this.companies = [];
      } finally {
        this.isLoadingCompanies = false;
      }
    },

    async toggleLike(sectionTitle, jobIndex) {

      // --- 步驟 1: 檢查登入狀態 ---
      if (!this.isUserLoggedIn) {
        // --- 步驟 2: 提示使用者並可選擇導向 ---
        alert('您需要先登入才能收藏職缺！'); // 或使用更美觀的提示框，例如 Vuetify 的 v-snackbar 或 Element Plus 的 ElMessage

        // 可選：導向到登入頁面
        // 確保您的 Vue Router 中有設定名為 'Login' 或路徑為 '/login' 的路由
        if (this.$router) { // 檢查 $router 是否可用
          this.$router.push({ path: '/login' }); // 或者 this.$router.push({ name: 'Login' });
        } else {
          console.warn('Vue Router instance ($router) is not available. Cannot redirect to login.');
        }
        return; // 停止後續的收藏操作
      }
      // --- 如果已登入，則執行原有的收藏邏輯 ---
      const section = this.sections.find(s => s.title === sectionTitle);
      let jobToUpdate = null;

      if (section && section.jobs && section.jobs[jobIndex]) {
        jobToUpdate = section.jobs[jobIndex];
      }

      if (!jobToUpdate) {
        console.error('Home.vue: Job not found for toggleLike', sectionTitle, jobIndex);
        return;
      }
      const originalLikedStatus = jobToUpdate.isLiked;
      const newLikedStatus = !jobToUpdate.isLiked;
      jobToUpdate.isLiked = newLikedStatus; // 樂觀更新
      try {
        if (newLikedStatus) {
          await likeJob(jobToUpdate.id); // 使用 home.js 中的 likeJob
          console.log(`Job ID ${jobToUpdate.id} liked successfully via API.`);
        } else {
          await unlikeJob(jobToUpdate.id);
          console.log(`Job ID ${jobToUpdate.id} unliked successfully via API.`);
        }

        if (typeof this.updateLikedItemInSidebar === 'function') {
          this.updateLikedItemInSidebar(jobToUpdate, newLikedStatus);
        } else {
          console.error('updateLikedItemInSidebar is not available from BaseLayout');
        }
        this.syncLikeStatusAcrossSections(jobToUpdate.id, newLikedStatus);
      } catch (error) {
        console.error(`Error toggling like status for job ID ${jobToUpdate.id} via API:`, error);
        // API 失敗，恢復 UI 狀態
        jobToUpdate.isLiked = originalLikedStatus;
        
        // 這裡可以根據 API 返回的錯誤狀態碼做更細緻的處理
        // 例如，如果錯誤是 401/403，即使前端檢查已登入，也可能表示 token 失效，同樣提示登入
        if (error.response && (error.response.status === 401 || error.response.status === 403)) {
          alert('您的登入已失效或無權限，請重新登入後再嘗試收藏。');
          if (this.$router) {
            this.$router.push({ path: '/login' });
          }
        } else {
          alert(`更新 "${jobToUpdate.title}" 的收藏狀態失敗，請稍後再試。`);
        }
      }
    },

    // 新增輔助方法，用於同步收藏狀態 (如果同一個職缺可能出現在多個列表)
    syncLikeStatusAcrossSections(jobId, newLikedStatus) {
      this.sections.forEach(section => {
        const jobInSection = section.jobs.find(j => j.id === jobId);
        if (jobInSection && jobInSection.isLiked !== newLikedStatus) {
          jobInSection.isLiked = newLikedStatus;
        }
      });
      // 如果 favoriteJobs 也包含這些職缺對象實例，它們應該已經通過 jobToUpdate 被更新了。
      // 但如果 favoriteJobs 是獨立複製的物件，則這裡也需要更新：
      const favJob = this.favoriteJobs.find(j => j.id === jobId);
      if (favJob && favJob.isLiked !== newLikedStatus) {
        favJob.isLiked = newLikedStatus;
      }
    },

    handleUnlikeFromSidebar(itemId) { // itemId 應為職缺的 id
      this.syncLikeStatusAcrossSections(itemId, false);
      // 以下邏輯保留，但 syncLikeStatusAcrossSections 應該已經處理了
      let jobFound = false;
      for (const section of this.sections) {
        const job = section.jobs.find(j => j.id === itemId);
        if (job) {
          job.isLiked = false;
          jobFound = true;
          // 不跳出，繼續檢查其他 section 是否有同一個 job
        }
      }
    },

    handleLikeFromSidebar(itemId) { // itemId 應為職缺的 id
      this.syncLikeStatusAcrossSections(itemId, true);
      // 以下邏輯保留，但 syncLikeStatusAcrossSections 應該已經處理了
      let jobFound = false;
      for (const section of this.sections) {
        const job = section.jobs.find(j => j.id === itemId);
        if (job) {
          if (!job.isLiked) {
            job.isLiked = true;
            // Sidebar 應已調用 updateLikedItemInSidebar
          }
          jobFound = true;
          // 不跳出，繼續檢查其他 section 是否有同一個 job
        }
      }
    },

    startDrag(e) {
      this.isDragging = true;
      this.startX = e.pageX - e.currentTarget.offsetLeft;
      this.scrollLeft = e.currentTarget.scrollLeft;
    },
    onDrag(e) {
      if (!this.isDragging) return;
      e.preventDefault();
      const x = e.pageX - e.currentTarget.offsetLeft;
      const walk = (x - this.startX) * 2; // 調整滾動速度
      e.currentTarget.scrollLeft = this.scrollLeft - walk;
    },
    stopDrag() {
      this.isDragging = false;
    },

    handleCardClick(jobData) {
      // jobData 是從 home.js 轉換後的格式，它內部有 originalData
      const dataForSidebar = jobData.originalData || jobData;

      if (typeof this.addViewedItemToSidebar === 'function') {
        this.addViewedItemToSidebar(dataForSidebar);
      } else {
        console.error('addViewedItemToSidebar is not available from BaseLayout');
      }
      if (typeof this.openRightSidebar === 'function') {
        this.openRightSidebar(dataForSidebar);
      } else {
        console.error('openRightSidebar is not available from BaseLayout');
      }
    },
    handleTitleClick(job) { // job 是轉換後的職缺對象
      console.log('Title clicked for job:', job.title, 'Company:', job.company);
      alert(`預計導航至公司頁面: ${job.company}. (請實現 Vue Router 功能)`);
      // 實際導航:
      // if (job.originalData && job.originalData.company && job.originalData.company.id) {
      //   this.$router.push({ name: 'CompanyDetail', params: { id: job.originalData.company.id } });
      // } else {
      //   console.warn('無法獲取公司ID進行導航');
      // }
    },
    handleCompanyCardClick(company) { // company 是轉換後的公司對象
      console.log('Company card clicked:', company);
      alert(`點擊了公司: ${company.name}`);
      // 實際導航或打開 sidebar:
      // const dataForSidebar = company.originalData || company;
      // this.openRightSidebar({ ...dataForSidebar, type: 'company' });
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
  /* 整體背景色 */
  border-radius: 10px;
  color: white;
  gap: 10px;
  width: 100%;
  max-width: none;
}

/* 區塊標題與橫向區塊通用樣式 */
.middle-content .recommend,
.middle-content .great-company,
.middle-content .favorite-job-section {
  /* great-company 保持原有樣式 */
  display: flex;
  flex-direction: column;
  white-space: nowrap;
  gap: 8px;
  padding: 4px 25px;
  /* 左右padding */
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
  /* 卡片之間的間距 */
  overflow-x: auto;
  flex-wrap: nowrap;
  box-sizing: border-box;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  cursor: grab;
  scrollbar-width: none;
  /* Firefox */
  -ms-overflow-style: none;
  /* IE and Edge */
  padding-bottom: 10px;
  /* 給滾動條一些空間，如果有的話，或避免內容截斷 */
}

.middle-content .recommend-content::-webkit-scrollbar {
  display: none;
  /* Chrome, Safari, Opera */
}


/* --- MODIFIED JOB CARD STYLES START --- */
.job-card-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #594f4f00;
  /* 正常狀態背景色 (目前是透明) */
  border-radius: 5px;
  padding: 10px 25px 10px 25px;
  width: 280px;
  /* 卡片原始寬度 */
  box-sizing: border-box;
  color: white;
  text-align: center;
  /* MODIFIED: 在 transition 中加入 width 和 background-color */
  transition: transform 0.5s ease-out,
    box-shadow 0.5s ease-out,
    background-color 0.5s ease-out,
    /* 新增背景色過渡 */
    width 0.5s ease-out;
  /* 新增寬度過渡 */
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
  margin-bottom: -8px;
  margin-left: 6px;
}

.job-card-company {
  font-size: 13px;
  font-weight: bold;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 110px;
}

.job-card-salary {
  font-size: 12px;
  color: #E0E0E0;
  margin-top: -2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 110px;
}

.job-card-like-btn.like-btn {
  display: flex;
  font-size: 18px;
  align-self: flex-end;
  margin-bottom: 3px;
  /* 往上移動按鈕 */
  margin-right: 6px;
}


.middle-content .great-company .recommend-content .content-wrapper:hover {
  /* From hover effect */
  background-color: #4a4444;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* 優質企業圖示樣式 (great-company section) */
.middle-content .great-company .company-icon {
  width: 200px;
  height: 200px;
  border-radius: 10px;
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
  text-align: center;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  width: 200px;
  /* 配合 company-icon 寬度 */
}

/* 只調整「優質企業」區塊中卡片的間距 */
.middle-content .great-company .recommend-content {
  gap: 50px;
  margin-left: 25px;
  /* 設定您希望的「優質企業」卡片間距，例如 25px */
  margin-top: 10px;
}


/* --- FAVORITE JOB SECTION STYLES (修改後) --- */
.favorite-job-section {
  /* padding 已在 .middle-content .favorite-job-section 統一設定 */
  margin-bottom: 20px;
  /* 與下方內容的間距 */
}

.favorite-job-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  /* 響應式網格，最小寬度320px */
  gap: 25px;
  /* 卡片之間的間距 */
  width: 100%;
}

.favorite-job-card {
  aspect-ratio: 16 / 10;
  /* 卡片寬高比，可根據內容調整 */
  min-height: 220px;
  /* 最小高度 */
  border-radius: 8px;
  background-size: cover;
  background-position: center;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease-out, box-shadow 0.3s ease-out;
  display: flex;
  /* 使內部 .card-overlay-content 能使用 flex 定位 */
  flex-direction: column;
  /* 使內容垂直排列 */
  justify-content: space-between;
  /* 將頂部信息和描述文字推向兩端 */
  padding: 18px;
  /* 卡片內部 padding */
  box-sizing: border-box;
}

.favorite-job-card::before {
  /* 添加一個遮罩層，使文字更易讀 */
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.35);
  /* 調整透明度和顏色以匹配圖片 */
  border-radius: inherit;
  /* 繼承父元素的圓角 */
  z-index: 1;
  /* 在背景圖之上，內容之下 */
  transition: background-color 0.3s ease;
}

.favorite-job-card:hover {
  transform: translateY(-6px) scale(1.03);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.25);
}

.favorite-job-card:hover::before {
  background-color: rgba(0, 0, 0, 0.2);
  /* Hover 時遮罩可稍微變淡 */
}

.card-overlay-content {
  position: relative;
  /* 確保內容在 ::before 遮罩之上 */
  z-index: 2;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  /* 分散頂部信息和底部描述 */
  height: 100%;
  /* 佔滿卡片高度 */
  color: white;
}

.card-top-info {
  display: flex;
  align-items: flex-start;
  /* 圖標和標題頂部對齊 */
  gap: 12px;
  /* 圖標和標題之間的間距 */
}

.favorite-job-icon {
  width: 50px;
  /* 根據附圖調整圖標大小 */
  height: 50px;
  background-size: cover;
  /* 或 cover，根據圖標類型 */
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 4px;
  /* 圖標輕微圓角 */
  flex-shrink: 0;
}

.favorite-job-name {
  font-size: 17px;
  /* 調整字體大小 */
  font-weight: bold;
  margin: 0;
  padding-top: 10px;
  /* 微調，使其與圖標看起來更對齊 */
}

.favorite-job-description {
  font-size: 13px;
  /* 調整字體大小 */
  line-height: 1.5;
  color: #e0e0e0;
  /* 稍淺的文字顏色 */
  margin: 0;
  /* white-space: normal; (預設就是 normal) */
  /* text-align: left; (預設) */
  /* 確保它在底部 */
  align-self: flex-start;
  /* 確保文字從左邊開始 */
  margin-top: auto;
  /* 將其推到底部，如果 card-overlay-content 的 justify-content 不是 space-between */
  /* 但因為 card-overlay-content 和 favorite-job-card 都是 flex space-between，這行可能非必要 */
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
  /* Added color transition */
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
  /* Already here, good */
}

/* 滑動中游標變成抓取狀態 */
.middle-content .recommend-content.active {
  /* Applies to both job and company recommend-content */
  cursor: grabbing;
  user-select: none;
}

/* 通用：為可交互卡片添加鼠標指針 */
.job-card-wrapper,
/* New job card */
.middle-content .great-company .recommend-content .content-wrapper,
/* Company card */
.middle-content .favorite-job .content-container {
  /* Favorite job card */
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
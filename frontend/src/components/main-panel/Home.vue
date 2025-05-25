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
import {  getJobs, getGreatCompanies, likeJob, unlikeJob, getJobDetail } from '@/api/home.js';

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
      allApiJobs: [], // 用於存儲從 API 獲取並轉換格式後的所有職缺
      companies: [],
      favoriteJobs: [ 
        { id: 'fav_dentist', name: '最愛牙醫師', image: '/favorite-bg-1.jpg', icon: '/favorite-icon-1.png', description: '雅德斯牙醫診所、蒔美牙醫集團和更多', isLiked: false },
        { id: 'fav_designer', name: '最愛室內設計師', image: '/favorite-bg-2.jpg', icon: '/favorite-icon-2.png', description: '雅和室內設計、拾間室內裝修設計有限公司和更多', isLiked: false },
        { id: 'fav_barista', name: '最愛咖啡師', image: '/favorite-bg-3.jpeg', icon: '/favorite-icon-3.png', description: '咖碼股份有限公司、路易莎職人咖啡股份有限公司和更多', isLiked: false },
        { id: 'fav_baker', name: '最愛烘焙技師', image: '/favorite-bg-4.jpg', icon: '/favorite-icon-4.png', description: '歐立食品股份有限公司、亞尼克菓子工房股份有限公司和更多', isLiked: false },
        { id: 'fav_engineer', name: '最愛半導體工程師', image: '/favorite-bg-5.jpg', icon: '/favorite-icon-5.png', description: 'nvidia台灣分公司、台積電和更多', isLiked: false },
        { id: 'fav_staff', name: '最愛門市人員', image: '/favorite-bg-6.jpg', icon: '/favorite-icon-6.png', description: '宜得利家居股份有限公司、無印良品和更多', isLiked: false }
      ],
      isLoadingCompanies: false,
      errorCompanies: null,
    };
  },
  async mounted() {
    this.loadInitialData(); // 2. 組件掛載時獲取數據

    eventBus.on('unlike-item-in-home-via-sidebar', this.handleUnlikeFromSidebar);
    eventBus.on('like-item-in-home-via-sidebar', this.handleLikeFromSidebar);
  },
  beforeUnmount() {
    eventBus.off('unlike-item-in-home-via-sidebar', this.handleUnlikeFromSidebar);
    eventBus.off('like-item-in-home-via-sidebar', this.handleLikeFromSidebar);
  },
  methods: {
    async loadInitialData() {
      // 同時開始加載職缺和公司數據
      this.sections.forEach(section => {
        section.isLoading = true;
        section.error = null;
      });
      this.isLoadingCompanies = true;
      this.errorCompanies = null;

      try {
        // 使用 Promise.all 並行獲取數據
        const [jobsData, companiesData] = await Promise.all([
          getJobs(),
          getGreatCompanies(),
        ]);

        // 3. 處理職缺數據
        const rawJobs = jobsData.results || jobsData || [];
        this.allApiJobs = rawJobs.map(job => ({
          id: job.id,
          title: job.title, 
          image: job.company_logo || 'default_job_image.png',
          company: job.company && job.company.name ? job.company.name : '未知公司',
          salary: job.salary_max ? `$${job.salary_max}` : '面議', 
          isLiked: job.is_liked_by_user || false, // 初始收藏狀態
          originalData: job, // 保留原始API數據，方便後續使用
        }));
        this.distributeJobsRandomly(); // 將獲取的職缺隨機分配到各區塊

        // 4. 處理企業數據
        const rawCompanies = companiesData.results || companiesData || [];
        this.companies = rawCompanies.map(company => ({
          id: company.id,
          name: company.name, 
          image: company.media && company.media.logo ? company.media.logo : 'default_company_logo_path.png',
          originalData: company,
        }));

      } catch (error) {
        console.error('Error fetching initial data:', error);
          let jobErrorOccurred = false;
          let companyErrorOccurred = false;
        if (error.message && error.message.toLowerCase().includes('network error')) {
            // 網路錯誤可能影響所有請求
            jobErrorOccurred = true;
            companyErrorOccurred = true;
        } else if (error.config && error.config.url) { // 如果錯誤對象包含請求配置
            if (error.config.url.includes('/api/jobs')) jobErrorOccurred = true;
            if (error.config.url.includes('/api/companies')) companyErrorOccurred = true;
        } else if (error.isAxiosError && error.request && error.request.responseURL) {
            // 另一種判斷方式
            if (error.request.responseURL.includes('/api/jobs')) jobErrorOccurred = true;
            if (error.request.responseURL.includes('/api/companies')) companyErrorOccurred = true;
        }
        else { // 如果無法判斷，假設兩個都可能出錯或是一個通用錯誤
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
        
        // 如果沒有特定錯誤，但依然進入catch，顯示通用錯誤
        if (!this.sections.some(s => s.error) && !this.errorCompanies && (jobErrorOccurred || companyErrorOccurred) ) {
            const generalErrorMsg = '資料載入失敗，請檢查網路連線或稍後重試。';
            this.sections.forEach(section => {
                if(!section.error) section.error = generalErrorMsg;
            });
            if(!this.errorCompanies) this.errorCompanies = generalErrorMsg;
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
      const jobsPerSection = 10; // 您希望每個區塊顯示的職缺數量

      this.sections.forEach(section => {
        section.jobs = []; // 清空現有職缺
        // 從打亂後的職缺中取N個，如果職缺不夠，則取剩餘所有
        const jobsForThisSection = availableJobs.splice(0, Math.min(jobsPerSection, availableJobs.length));
        section.jobs = jobsForThisSection;
      });
    },

    async toggleLike(sectionTitle, jobIndex) {
      const section = this.sections.find(s => s.title === sectionTitle);
      if (!section) return;

      const job = section.jobs[jobIndex];
      if (!job) return;

      const originalLikedStatus = job.isLiked;
      job.isLiked = !job.isLiked; // UI先行，樂觀更新

      this.updateLikedItemInSidebar(job.id, job.isLiked, job.originalData);
      this.syncLikeStatusAcrossSections(job.id, job.isLiked); // 同步所有地方的收藏狀態

      //5. (可選) 連接真實後端 API
      try {
        if (job.isLiked) {
          await likeJob(job.id); // 假設 likeJob 是 API 請求函數
        } else {
          await unlikeJob(job.id); // 假設 unlikeJob 是 API 請求函數
        }
       } catch (error) {
         console.error('Failed to update like status:', error);
         job.isLiked = originalLikedStatus; // API 失敗，回滾UI狀態
         this.updateLikedItemInSidebar(job.id, job.isLiked, job.originalData);
         this.syncLikeStatusAcrossSections(job.id, job.isLiked);
         alert('收藏操作失敗，請稍後再試。');
       }
    },

    syncLikeStatusAcrossSections(jobId, newLikedStatus) {
      // 同步 sections 中的職缺收藏狀態
      this.sections.forEach(section => {
        const jobInSection = section.jobs.find(j => j.id === jobId);
        if (jobInSection && jobInSection.isLiked !== newLikedStatus) {
          jobInSection.isLiked = newLikedStatus;
        }
      });
      // 同步 favoriteJobs 中的職缺收藏狀態 (如果 id 匹配)
      const favJob = this.favoriteJobs.find(j => j.id === jobId);
      if (favJob && favJob.isLiked !== newLikedStatus) {
        favJob.isLiked = newLikedStatus;
      }
    },

    handleUnlikeFromSidebar(item) { // 假設 item 是包含 id 的對象，或者直接是 id
      const itemId = typeof item === 'object' ? item.originalData.id || item.id : item;
      this.syncLikeStatusAcrossSections(itemId, false);
      // 如果您在 toggleLike 中啟用了 API 調用，這裡也可以考慮調用 unlikeJob(itemId)
    },

    handleLikeFromSidebar(item) { // 假設 item 是包含 id 的對象，或者直接是 id
      const itemId = typeof item === 'object' ? item.originalData.id || item.id : item;
      this.syncLikeStatusAcrossSections(itemId, true);
      // 如果您在 toggleLike 中啟用了 API 調用，這裡也可以考慮調用 likeJob(itemId)
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
      const dataForSidebar = jobData.originalData || jobData;
      if (typeof this.addViewedItemToSidebar === 'function') {
        this.addViewedItemToSidebar(dataForSidebar);
      }
      if (typeof this.openRightSidebar === 'function') {
        this.openRightSidebar(dataForSidebar);
      }
    },
    handleTitleClick(job) {
      console.log('Title clicked for job:', job.title, 'Company:', job.company);
      // 通常點擊職位標題或公司名稱會導航到公司或職缺詳情頁
      // 假設您有一個路由到公司頁面，並且需要公司ID
      // job.originalData.company.id
      alert(`預計導航至公司頁面: ${job.company}. (此功能需 Vue Router 支持)`);
    },
    handleCompanyCardClick(company) {
      console.log('Company card clicked:', company);
      // company.originalData.id
      alert(`點擊了公司: ${company.name}. (此功能需 Vue Router 支持)`);
    },
    // 如果 favorite-job-card 有點擊事件，也需要實現
    handleFavoriteJobCardClick(favJob) {
        console.log('Favorite job card clicked:', favJob);
        // 創建一個與普通職缺結構相似的對象傳給 sidebar
        const dataForSidebar = {
            id: favJob.id,
            title: favJob.name,
            image: favJob.icon, // 或者 favJob.image
            company: favJob.description.split('、')[0] || '相關企業', // 嘗試從描述中獲取
            salary: 'N/A',
            isLiked: favJob.isLiked !== undefined ? favJob.isLiked : true, // 收藏列表預設為已收藏
            originalData: favJob
        };
        if (typeof this.addViewedItemToSidebar === 'function') {
            this.addViewedItemToSidebar(dataForSidebar);
        }
        if (typeof this.openRightSidebar === 'function') {
            this.openRightSidebar(dataForSidebar);
        }
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

.middle-content .recommend-content::-webkit-scrollbar {
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


.middle-content .great-company .recommend-content .content-wrapper:hover {
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
}

.middle-content .great-company .recommend-content {
  gap: 50px;
  margin-left: 25px;
  margin-top: 10px;
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
  max-width: 320px; /* 例如 */
  min-height: 320px;
  width: 100%; /* 確保它能縮小 */
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
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.25);
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
  margin-left:-20px;
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

.job-card-wrapper,
.middle-content .great-company .recommend-content .content-wrapper,
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
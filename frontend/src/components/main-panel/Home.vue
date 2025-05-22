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
        <div v-if="section.jobs.length > 0"
             class="recommend-content"
             @mousedown="startDrag"
             @mousemove="onDrag"
             @mouseup="stopDrag"
             @mouseleave="stopDrag"
             :class="{ active: isDragging }">
          <div class="job-card-wrapper" v-for="(job, jobIndex) in section.jobs" :key="job.id || jobIndex" @click="handleCardClick(job)">
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
        <div v-if="companies.length > 0"
             class="recommend-content"
             @mousedown="startDrag"
             @mousemove="onDrag"
             @mouseup="stopDrag"
             @mouseleave="stopDrag"
             :class="{ active: isDragging }">
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

    <section class="favorite-job">
      <div v-if="isLoadingFavoriteJobs" class="loading-message">
        正在載入最愛職缺...
      </div>
      <div v-if="errorFavoriteJobs" class="error-message">
        {{ errorFavoriteJobs }}
      </div>
      <template v-if="!isLoadingFavoriteJobs && !errorFavoriteJobs">
        <template v-if="favoriteJobs.length > 0">
          <div class="content-container"
               v-for="(favJob, fIndex) in favoriteJobs"
               :key="'favjob-' + fIndex"
               :style="{ backgroundImage: 'url(' + favJob.image + ')' }"
               @click="handleFavoriteJobCardClick(favJob)">
            <div class="favorite-icon" :style="{ backgroundImage: 'url(' + favJob.icon + ')' }" @click.stop></div>
            <p class="favorite-name" @click.stop>{{ favJob.name }}</p>
          </div>
        </template>
        <div v-else class="no-data-message">
          目前沒有最愛職缺資料。
        </div>
      </template>
    </section>
  </div>
</template>


<script>
import eventBus from '/src/eventBus.js';
import axios from 'axios';

export default {
  name: 'MainPanel',
  inject: ['openRightSidebar', 'updateLikedItemInSidebar', 'addViewedItemToSidebar'],
  data() {
    return {
      isDragging: false,
      startX: 0,
      scrollLeft: 0,
      sections: [
        { title: '為你推薦', jobs: [], isLoading: false, error: null },
        { title: '熱門職缺', jobs: [], isLoading: false, error: null },
        { title: '最新職缺', jobs: [], isLoading: false, error: null },
      ],
      companies: [],
      favoriteJobs: [
        { name: '最愛牙醫師', image: '/favorite-bg-1.jpg', icon: '/favorite-icon-1.png' },
        { name: '最愛室內設計師', image: '/favorite-bg-2.jpg', icon: '/favorite-icon-2.png' },
        { name: '最愛咖啡師', image: '/favorite-bg-3.jpeg', icon: '/favorite-icon-3.png' },
        { name: '最愛蛋糕師傅', image: '/favorite-bg-4.jpg', icon: '/favorite-icon-4.png' },
      ],
      // Moved these into the data object
      isLoadingCompanies: false,
      errorCompanies: null,
      isLoadingFavoriteJobs: false,
      errorFavoriteJobs: null,
    };
  },
  mounted() {
    // Keep existing eventBus listeners
    eventBus.on('unlike-item-in-home-via-sidebar', this.handleUnlikeFromSidebar);
    eventBus.on('like-item-in-home-via-sidebar', this.handleLikeFromSidebar);

    // --- ADDED: Call methods to fetch data ---
    this.fetchAllData();
  },
  beforeUnmount() {
    eventBus.off('unlike-item-in-home-via-sidebar', this.handleUnlikeFromSidebar);
    eventBus.off('like-item-in-home-via-sidebar', this.handleLikeFromSidebar);
  },
  methods: {
    // --- ADDED: Method to orchestrate all data fetching ---
    async fetchAllData() {
      // You can show a global loading indicator here if you want
      Promise.all([
        this.fetchRecommendedJobs(),
        this.fetchPopularJobs(),
        this.fetchLatestJobs(),
        this.fetchCompanies(),
        // Ensure this API endpoint and data structure match your needs
      ]).then(() => {
        console.log('All initial data for Home.vue has been loaded (or attempted).');
        // Hide global loading indicator here
      }).catch(error => {
        console.error('One or more initial data fetches failed for Home.vue:', error);
        // Handle global error display if necessary
        // Hide global loading indicator here
      });
    },

    async fetchJobsForSection(sectionTitle, localJsonPath) { // 第二個參數現在是本地 JSON 路徑
      const section = this.sections.find(s => s.title === sectionTitle);
      if (!section) return;

      section.isLoading = true;
      section.error = null;
      try {
        // *** 修改點：直接使用 localJsonPath ***
        const response = await axios.get(localJsonPath); // 例如: axios.get('/api/jobs-recommended.json')
        section.jobs = response.data.jobs.map(job => ({ ...job, isLiked: job.isLiked || false }));
      } catch (err) {
        console.error(`Error fetching ${sectionTitle} from ${localJsonPath}:`, err);
        section.error = '無法載入模擬資料，請檢查 JSON 檔案路徑及格式。';
        section.jobs = [];
      } finally {
        section.isLoading = false;
      }
    },

    async fetchRecommendedJobs() {
      // *** 修改點：傳入 JSON 檔案路徑 ***
      await this.fetchJobsForSection('為你推薦', '/jobs-recommended.json');
    },

    async fetchPopularJobs() {
      // *** 修改點：傳入 JSON 檔案路徑 ***
      await this.fetchJobsForSection('熱門職缺', '/jobs-popular.json');
    },

    async fetchLatestJobs() {
      // *** 修改點：傳入 JSON 檔案路徑 ***
      await this.fetchJobsForSection('最新職缺', '/jobs-latest.json');
    },

    async fetchCompanies() {
      this.isLoadingCompanies = true;
      this.errorCompanies = null;
      try {
        // *** 修改點：直接使用 JSON 檔案路徑 ***
        const response = await axios.get('/companies-great.json');
        this.companies = response.data.companies;
      } catch (err) {
        console.error('Error fetching companies from /companies-great.json:', err);
        this.errorCompanies = '無法載入模擬企業資料。';
        this.companies = [];
      } finally {
        this.isLoadingCompanies = false;
      }
    },

    // toggleLike 方法的處理：
    // 因為沒有實際後端，POST/DELETE 操作無法真正執行。
    // 您可以暫時註解掉 API 呼叫，只更新本地狀態，或者 console.log 模擬 API 呼叫。
    async toggleLike(sectionTitle, jobIndex) {
      const section = this.sections.find(s => s.title === sectionTitle);
      if (section && section.jobs && section.jobs[jobIndex]) {
        const job = section.jobs[jobIndex];
        const newLikedStatus = !job.isLiked;

        console.log(`Simulating API call: Job ID ${job.id} new liked status: ${newLikedStatus}`);
        // 暫時不實際呼叫後端 API
        // try {
        //   const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api';
        //   if (newLikedStatus) {
        //     await axios.post(`${baseUrl}/jobs/${job.id}/like`);
        //   } else {
        //     await axios.delete(`${baseUrl}/jobs/${job.id}/like`);
        //   }
        //   job.isLiked = newLikedStatus; // 更新本地狀態
        // } catch (error) {
        //   console.error('Error simulating toggle like status:', error);
        //   alert('模擬更新收藏狀態失敗。');
        //   // 可能需要恢復 job.isLiked 的原始狀態
        //   return; // 提前返回，不更新 sidebar
        // }

        // 僅更新本地 UI 狀態以供測試
        job.isLiked = newLikedStatus;

        if (typeof this.updateLikedItemInSidebar === 'function') {
          this.updateLikedItemInSidebar(job, job.isLiked);
        } else {
          console.error('updateLikedItemInSidebar is not available from BaseLayout');
        }
      } else {
        console.error('Job or section not found for toggleLike');
      }
    },
    handleUnlikeFromSidebar(itemId) {
      let jobFound = false;
      for (const section of this.sections) {
        const job = section.jobs.find(j => j.id === itemId);
        if (job) {
          job.isLiked = false;
          jobFound = true;
          // If this action implies backend update, it should happen in LeftSidebar or BaseLayout,
          // or an event should trigger an API call here.
          break;
        }
      }
      if (!jobFound) {
        console.warn(`Job with id ${itemId} not found in Home.vue sections to unlike.`);
      }
    },
    handleLikeFromSidebar(itemId) {
      let jobFound = false;
      for (const section of this.sections) {
        const job = section.jobs.find(j => j.id === itemId);
        if (job) {
          if (!job.isLiked) {
            job.isLiked = true;
            // This should reflect a backend change, confirmed via updateLikedItemInSidebar
            if (typeof this.updateLikedItemInSidebar === 'function') {
              this.updateLikedItemInSidebar(job, true);
            } else {
              console.error('updateLikedItemInSidebar is not available from BaseLayout');
            }
          }
          jobFound = true;
          break;
        }
      }
      if (!jobFound) {
        console.warn(`Job with id ${itemId} not found in Home.vue sections to like from sidebar.`);
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
      const walk = (x - this.startX) * 2;
      e.currentTarget.scrollLeft = this.scrollLeft - walk;
    },
    stopDrag() {
      this.isDragging = false;
    },
    handleCardClick(jobData) {
      if (typeof this.addViewedItemToSidebar === 'function') {
        this.addViewedItemToSidebar(jobData);
      } else {
        console.error('addViewedItemToSidebar is not available from BaseLayout');
      }
      if (typeof this.openRightSidebar === 'function') {
        this.openRightSidebar(jobData);
      } else {
        console.error('openRightSidebar is not available from BaseLayout');
      }
    },
    handleTitleClick(job) {
      console.log('Title clicked for job:', job.title, 'Company:', job.company);
      alert(`Navigating to company page for: ${job.company}. Implement Vue Router push here.`);
    },
    handleCompanyCardClick(company) {
      console.log('Company card clicked:', company);
      // Example: this.openRightSidebar({ ...company, type: 'company' });
    },
    handleFavoriteJobCardClick(favJob) {
      console.log('Favorite job card clicked:', favJob);
      // Example: this.openRightSidebar({ ...favJob, type: 'favoriteJob' });
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
  background-color: #383333; /* 整體背景色 */
  border-radius: 10px;
  color: white;
  gap: 10px;
  width: 100%;
  max-width: none;
}

/* 區塊標題與橫向區塊通用樣式 */
.middle-content .recommend,
.middle-content .great-company { /* great-company 保持原有樣式 */
  display: flex;
  flex-direction: column;
  white-space: nowrap;
  gap: 8px;
  padding: 4px 25px; /* 左右padding */
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
  gap: 10px; /* 卡片之間的間距 */
  overflow-x: auto;
  flex-wrap: nowrap;
  box-sizing: border-box;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  cursor: grab;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
  padding-bottom: 10px; /* 給滾動條一些空間，如果有的話，或避免內容截斷 */
}
.middle-content .recommend-content::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}


/* --- MODIFIED JOB CARD STYLES START --- */
.job-card-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #594f4f00; /* 正常狀態背景色 (目前是透明) */
  border-radius: 5px;
  padding: 10px 25px 10px 25px;
  width: 280px; /* 卡片原始寬度 */
  box-sizing: border-box;
  color: white;
  text-align: center;
  /* MODIFIED: 在 transition 中加入 width 和 background-color */
  transition: transform 0.5s ease-out,
              box-shadow 0.5s ease-out,
              background-color 0.5s ease-out, /* 新增背景色過渡 */
              width 0.5s ease-out;            /* 新增寬度過渡 */
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
width: 100%;
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
  margin-bottom: 3px; /* 往上移動按鈕 */
  margin-right: 6px;
}


.middle-content .great-company .recommend-content .content-wrapper:hover { /* From hover effect */
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
  width: 200px; /* 配合 company-icon 寬度 */
}

/* 只調整「優質企業」區塊中卡片的間距 */
.middle-content .great-company .recommend-content {
  gap: 50px;
  margin-left:25px; /* 設定您希望的「優質企業」卡片間距，例如 25px */
  margin-top:10px;
}


/* 最愛職缺樣式 (favorite-job section) */
.middle-content .favorite-job {
  display: flex;
  flex-wrap: wrap;
  gap: 50px;
  padding: 40px 40px 0px 70px;
  margin-bottom: 20px;
}
.middle-content .favorite-job .content-container { /* This is the card for favorite jobs */
  display: flex;
  gap: 10px;
  width: 400px;
  height: 450px;
  border-radius: 5px;
  background-color: #ffffff;
  background-size: cover;
  background-position: center;
  border: none;
  padding: 25px;
  flex-shrink: 0;
  cursor: pointer;
  position: relative; /* For hover effect */
  overflow: hidden; /* For hover effect */
  transition: transform 0.25s ease-out, box-shadow 0.25s ease-out; /* From hover effect */
}
.middle-content .favorite-job .content-container::before { /* From hover effect */
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.15);
  opacity: 0;
  transition: opacity 0.25s ease-out;
  border-radius: 5px;
  pointer-events: none;
}
.middle-content .favorite-job .content-container:hover { /* From hover effect */
  transform: scale(1.02) translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.22);
}
.middle-content .favorite-job .content-container:hover::before { /* From hover effect */
  opacity: 1;
}
.middle-content .favorite-job .content-container p {
  margin-top: 20px;
}
.middle-content .favorite-job .content-container .favorite-icon {
  width: 80px;
  height: 80px;
  border-radius: 5px;
  background-color: #ffffff00;
  background-size: cover;
  background-position: center;
  border: none;
  padding: 0;
  flex-shrink: 0;
  position: relative; /* From hover effect */
  z-index: 1; /* From hover effect */
  transition: transform 0.25s ease-out; /* From hover effect */
}
.middle-content .favorite-job .content-container:hover .favorite-icon { /* From hover effect */
  transform: scale(1.08);
}
.middle-content .favorite-job .content-container .favorite-name { /* From hover effect */
 position: relative;
 z-index: 1;
}


/* 收藏按鈕通用樣式 */
.like-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: white;
  font-size: 18px;
  padding: 0px;
  transition: transform 0.5s ease, color 0.3s ease; /* Added color transition */
}
.like-btn:hover {
  transform: scale(1.1);
}
.like-btn.active {
  color: rgb(235, 178, 189); /* 粉色實心 */
}
.heart-icon {
  transition: color 0.3s ease; /* Already here, good */
}

/* 滑動中游標變成抓取狀態 */
.middle-content .recommend-content.active { /* Applies to both job and company recommend-content */
  cursor: grabbing;
  user-select: none;
}

/* 通用：為可交互卡片添加鼠標指針 */
.job-card-wrapper, /* New job card */
.middle-content .great-company .recommend-content .content-wrapper, /* Company card */
.middle-content .favorite-job .content-container { /* Favorite job card */
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
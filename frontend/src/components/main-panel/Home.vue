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
          <div class="content-wrapper" v-for="(job, jobIndex) in section.jobs" :key="job.id || jobIndex">
            <div class="card" @click="handleCardClick(job)">
              <div class="job-image" :style="{ backgroundImage: 'url(' + job.image + ')' }"></div>
              <div class="content-container">
                <p class="title" @click.stop="handleTitleClick(job)">{{ job.title }}</p>
                <p class="info">{{ job.location }}</p>
                <p class="info salary-and-like">
                  {{ job.salary }}
                  <button type="button" class="like-btn" :class="{ active: job.isLiked }"
                          @click.stop="toggleLike(section.title, jobIndex)">
                    <font-awesome-icon :icon="[job.isLiked ? 'fas' : 'far', 'heart']" class="heart-icon" />
                  </button>
                </p>
              </div>
            </div>
            <p class="company-name">{{ job.company }}</p>
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
  background-color: #383333;
  border-radius: 10px;
  color: white;
  gap: 25px;
  width: 100%;
  max-width: none;
}


/* 區塊標題與橫向區塊通用樣式 */
.middle-content .recommend,
.middle-content .great-company {
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  white-space: nowrap;
  gap: 8px;
  padding: 4px 25px;
}

/* 每個職缺卡片的容器 */
.middle-content .recommend .recommend-content .content-wrapper,
.middle-content .great-company .recommend-content .content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  /* 卡片與下方公司名稱的間距，可酌情調整 */
}


/* 職缺卡片本體樣式 */
.card {
  display: flex;
  flex-direction: row;
  align-items: center;
  background-color: #594f4f;
  border-radius: 10px;
  /* 調整圓角以匹配新尺寸 */
  padding: 8px 8px 8px 12px;
  /* MODIFIED: 稍微減少 padding */
  width: 240px;
  /* MODIFIED: 將寬度從 300px 改為 240px */
  box-sizing: border-box;
  transition: box-shadow 0.25s ease-out, transform 0.25s ease-out;
  /* 保持 hover 效果的 transition */
}

/* 橫向滑動內容區塊樣式 */
.middle-content .recommend-content,
.middle-content .great-company .recommend-content {
  display: flex;
  flex-direction: row;
  gap: 20px;
  /* MODIFIED: 如果卡片變小，可以稍微減少卡片間的間距 */
  overflow-x: auto;
  flex-wrap: nowrap;
  max-width: 100%;
  box-sizing: border-box;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  cursor: grab;
  scrollbar-width: none;
  /* Firefox */
  -ms-overflow-style: none;
}

/* 文字與圖片的職缺內容容器 */
.middle-content .recommend .content-container {
  display: flex;
  /* MODIFIED: 改為 flex 佈局更好控制內部 */
  flex-direction: column;
  /* MODIFIED: 讓內部元素垂直排列 */
  justify-content: center;
  /* MODIFIED: 垂直居中內容 (可選) */
  /* width: 200px; */
  /* MODIFIED: 移除固定寬度，讓 flex-grow 生效 */
  background-color: #594f4f;
  /* 與 card 背景色相同，通常不需要單獨設定 */
  /* border-radius: 5px; */
  /* 如果 card 有圓角，這裡通常不需要 */
  box-sizing: border-box;
  flex-grow: 1;
  /* 填充 card 內剩餘空間 */
  margin-left: 8px;
  /* MODIFIED: 新增圖片和文字容器之間的間距 */
}

/* 職缺圖片 */
.middle-content .recommend .job-image {
  width: 64px;
  /* MODIFIED: 從 80px 調整為 64px */
  height: 64px;
  /* MODIFIED: 從 80px 調整為 64px */
  border-radius: 6px;
  /* MODIFIED: 調整圓角 */
  background-size: cover;
  background-position: center;
  flex-shrink: 0;
}

/* 職缺標題與說明文字 */
.middle-content section h1 {
  font-size: 20px;
  padding: 8px 0px;
}

.middle-content .recommend .content-container .title {
  display: inline-block;
  /* 修改點：讓元素寬度自適應內容 */
  align-self: flex-start;
  max-width: 100%;
  /* 新增：確保在內容過長時，仍能配合 overflow 和 ellipsis */
  font-size: 14px;
  margin: 0 0 4px 0;
  font-weight: bold;
  white-space: nowrap;
  /* 保持不換行 */
  overflow: hidden;
  /* 超出部分隱藏 */
  text-overflow: ellipsis;
  /* 超出部分顯示省略號 */
  cursor: pointer;
}

.middle-content .recommend .content-container .title:hover,
.middle-content .recommend .company-name:hover {
  text-decoration: underline;
  /* Underline on hover */
  cursor: pointer;
}

/* 優質企業圖示樣式 */
.middle-content .recommend .content-container .info {
  font-size: 12px;
  /* MODIFIED: 從 14px 調整為 12px */
  margin: 0 0 2px 0;
  /* MODIFIED: 調整 margin */
  color: #f4f4f4;
  white-space: nowrap;
  /* 確保不換行 */
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 公司名稱樣式 */
.middle-content .recommend .content-container .salary-and-like {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
  /* MODIFIED: 移除底部 margin，因為 content-container 會處理間距 */
}

/* 最愛職缺樣式 */
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


.middle-content .recommend .recommend-content .content-wrapper .company-name,
.middle-content .great-company .recommend-content .content-wrapper .company-name {
  font-size: 14px;
  /* MODIFIED: 從 16px 調整為 14px，如果需要 */
  font-weight: bold;
  color: white;
  margin-top: 6px;
  /* 保持與上方卡片的間距 */
  text-align: center;
  /* 如果希望公司名稱在卡片下方居中對齊 */
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  width: 240px;
  /* MODIFIED: 讓公司名稱的寬度與卡片寬度一致，以便正確的 text-align: center */
}

.middle-content .favorite-job {
  display: flex;
  flex-wrap: wrap;
  gap: 50px;
  padding: 40px 40px 0px 70px;
  margin-bottom: 20px;
}

.middle-content .favorite-job .content-container {
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
}

/* 收藏按鈕樣式 */
.like-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: white;
  /* 空心愛心預設白色 */
  font-size: 18px;
  /* MODIFIED: 從 20px 調整為 18px */
  padding: 3px;
  /* MODIFIED: 稍微減少 padding */
  transition: transform 0.5s ease;
}

.middle-content .recommend .content-container .like-btn:hover {
  transform: scale(1.1);
}

.like-btn.active {
  color: rgb(235, 178, 189);
  /* 喜歡後變成粉色實心 */
}

.heart-icon {
  transition: color 0.3s ease;
}

/* 滑動中游標變成抓取狀態 */
.middle-content .recommend-content.active {
  cursor: grabbing;
  user-select: none;
}





/* --- 新增或修改以下 Hover 效果 --- */

/* 通用：為可交互卡片添加鼠標指針 */
.card,
.middle-content .great-company .recommend-content .content-wrapper,
.middle-content .favorite-job .content-container {
  cursor: pointer;
}

/* 職缺卡片 (.card) Hover 效果 - 背景出現陰影 */
/* .card 的 transition 已在上方定義 */

.card:hover {
  transform: scale(1.03);
  /* 可以保持或微調 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  /* MODIFIED: 陰影也可以微調以適應新尺寸 */
}

/* 優質企業卡片 (.content-wrapper in .great-company) Hover 效果 - 背景出現陰影 */
.middle-content .great-company .recommend-content .content-wrapper {
  border-radius: 10px;
  padding: 8px;
  transition: box-shadow 0.25s ease-out, background-color 0.25s ease-out;
}

.middle-content .great-company .recommend-content .content-wrapper:hover {
  background-color: #4a4444;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}



/* 最愛職缺卡片 (.favorite-job .content-container) Hover 效果 */
.middle-content .favorite-job .content-container {
  position: relative;
  overflow: hidden;
  transition: transform 0.25s ease-out, box-shadow 0.25s ease-out;
}

/* 疊加層 */
.middle-content .favorite-job .content-container::before {
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

.middle-content .favorite-job .content-container:hover {
  transform: scale(1.02) translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.22);
}

.middle-content .favorite-job .content-container:hover::before {
  opacity: 1;
}

/* 確保最愛職缺卡片內的圖示和文字在疊加層之上 (如果需要) */
.middle-content .favorite-job .content-container .favorite-icon,
.middle-content .favorite-job .content-container .favorite-name {
  position: relative;
  z-index: 1;
}

/* 可選：最愛職缺卡片內部圖示的 hover 效果 */
.middle-content .favorite-job .content-container .favorite-icon {
  transition: transform 0.25s ease-out;
}

.middle-content .favorite-job .content-container:hover .favorite-icon {
  transform: scale(1.08);
}

.loading-message,
.error-message,
.no-data-message {
  padding: 20px;
  text-align: center;
  color: #ccc; /* 根據您的背景調整顏色 */
  width: 100%; /* 確保佔滿寬度，使其在 section 內居中 */
}

.error-message {
  color: #ffffff; /* 紅色系用於錯誤提示 */
  background-color: rgba(128, 128, 128, 0.1); /* 可選的淡紅色背景 */
  border: 1px solid rgba(211, 211, 211, 0.3);
  border-radius: 5px;
  margin: 10px 0; /* 給予上下間距 */
}

.loading-message {
  font-style: italic;
}

</style>
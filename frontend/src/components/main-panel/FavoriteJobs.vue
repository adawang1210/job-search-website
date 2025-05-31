<template>
  <div class="middle-content">
    <div v-if="!companies || !filterJobs">
      載入中...
    </div>
    <!-- 資料載入後才顯示內容 -->
    <div v-else>
      <section class="company-profile">
        <div class="profile-container">
          <div class="profile-grid">
            <div class="logo-column">
              <div class="company-logo">
                <img ref="avatar" :src="selectedLoveJob.image" alt="Company Logo" class="logo-image" />
              </div>
            </div>
            <div class="info-column">
              <div class="company-info">
                <span class="info-label">行業</span>
                <h1 class="company-name">最愛{{ selectedLoveJob?.name }}</h1>
                <!-- <p class="company-tags">標籤</p> -->
                <p class="job-count">{{ filterJobs.length }}個工作機會</p>
              </div>
            </div>
          </div>
        </div>
        
      </section>

      <section class="job-listings">
        <div class="listings-header">
          <h2 class="section-title">工作機會</h2>
          <div class="page-size">
            <label class="label">每頁 {{ pageSize }} 筆</label>
            <div class="dropdown">
              <button type="button" class="dropdown-toggle" @click="toggleDropdownJob">
                <n-icon class="caret-icon">
                  <CaretDown />
                </n-icon>
              </button>
              <ul v-show="dropdownOpenJob" class="dropdown-menu bottom-right">
                <li @click="selectPageSize(10)">10 筆</li>
                <li @click="selectPageSize(20)">20 筆</li>
              </ul>
            </div>
          </div>
        </div>
        <!-- JobCard -->
        <article v-for="(job, jobIndex) in paginatedJobs" :key="job.id || jobIndex" class="job-card"
          @click="handleCardClick(job)">
          <div class="job-content">
            <div class="main-info">
              <div class="date-block">
                <time class="date">{{ formatDate(job.created_at) }}</time>
              </div>
              <div class="content-block">
                <div class="header">
                  <h3 class="title" @click.stop="handleTitleClick(job)">{{ job.title }}</h3>
                </div>
                <div class="details">
                  <div class="company-info-job">
                    <span class="company-name-job">{{ job.company.name }}</span>
                    <span class="industry-job">{{ formatJobIndustry(job.company.name) }}</span>
                  </div>
                  <div class="job-specs">
                    <span class="spec">{{ formatLocation(job.location) }}</span>
                    <span class="spec">{{ job.experience_required }}</span>
                    <span class="spec">{{ job.education_required }}</span>
                    <span class="spec">{{ formattedSalary(job.id) }}</span>
                  </div>
                  <div class="benefits">
                    <span v-for="(benefit, index) in job.benefits" :key="index" class="benefit-tag-job">
                      {{ benefit.benefits_description }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div class="actions-button">
              <button type="button" class="like-btn" :class="{ active: job.isLiked }"
                @click.stop="toggleLike(job)">
                <n-icon class="heart-icon">
                  <component :is="job.isLiked ? iconHeartSolid : iconHeartRegular" />
                </n-icon>
              </button>
              <button type="button" class="envelope-btn"
                @click.stop="openModal(job.id)">
                <n-icon class="envelope-icon">
                  <component :is="job.isApplied ? iconEnvelopeSolid : iconEnvelopeRegular" />
                </n-icon>
              </button>

              <!-- <p class="applicants">{{ job.applicants }}</p> -->
            </div>
          </div>
        </article>
      </section>
      <!-- Modal 彈窗 -->
      <transition name="modal">
        <div v-if="showApplyModal" class="modal-overlay" @click="closeModal">
          <div class="modal" @click.stop>
            <div class="modal-header">
              <h2 class="modal-title">{{ currentItem.title }}</h2>
            </div>

            <form @submit.prevent>
              <div class="form-group">
                <label class="form-label">標題</label>
                <input type="text" class="form-input" v-model="formData.title" placeholder="請輸入標題...">
              </div>

              <div class="form-group">
                <label class="form-label">內容</label>
                <textarea class="form-input form-textarea" v-model="formData.content" placeholder="請輸入內容..."></textarea>
              </div>

              <div class="file-upload-container">
                <label class="form-label">上傳檔案</label>
                <div class="file-upload-btn">
                  <input type="file" class="file-input" @change="handleFileUpload" multiple>
                  <span v-if="selectedFiles.length === 0">
                    📁 點擊選擇檔案或拖拽到此處
                  </span>
                  <span v-else>
                    ✅ 已選擇 {{ selectedFiles.length }} 個檔案
                  </span>
                </div>
              </div>

              <div class="modal-actions">
                <button type="button" class="btn btn-cancel" @click="closeModal">
                  取消
                </button>
                <button type="button" class="btn btn-submit" @click="handleSubmit(applyJobId)">
                  送出
                </button>
              </div>
            </form>
          </div>
        </div>
      </transition>
      <!-- 分享彈窗 -->
      <transition name="modal">
        <div v-if="showShare" class="modal-overlay" @click="showShare = false">
          <div class="modal" @click.stop>
            <div class="modal-header">
              <h2 class="modal-title">分享這個內容</h2>
            </div>
            <form @submit.prevent>
              <div class="form-group">
                <input type="text" :value="shareLink" readonly class="form-input"></input>
              </div>
              <div class="modal-actions">
                <button type="button" class="btn btn-cancel" @click="showShare = false">取消</button>
                <button type="button" class="btn btn-submit" @click="copyLink">複製連結</button>
              </div>
            </form>
          </div>
        </div>
      </transition>

      <!-- 檢舉彈窗 -->
      <transition name="modal">
        <div v-if="showReport" class="modal-overlay" @click="showReport = false">
          <div class="modal" @click.stop>
            <div class="modal-header">
              <h2 class="modal-title">檢舉內容</h2>
            </div>
            <div class="form-group">
              <textarea v-model="reportReason" rows="3" class="form-input"></textarea>
            </div>
            <div class="modal-actions">
              <button type="button" class="btn btn-cancel" @click="showReport = false">取消</button>
              <button type="button" class="btn btn-submit" @click="submitReport">送出檢舉</button>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { ref, defineComponent } from 'vue'
import axios from 'axios';
import eventBus from '/src/eventBus.js';
import { getJobs, getGreatCompanies, getJobDetail } from '@/api/home.js';
import { NIcon } from 'naive-ui'
import { Heart, HeartRegular, CaretDown, EllipsisH, Envelope, EnvelopeRegular } from '@vicons/fa'

const ITEM_TYPE_JOB = 'job';
const ITEM_TYPE_COMPANY = 'company';

export default defineComponent({
  name: 'FavoriteJobs',
  inject: ['updateLikedItemInSidebar', 'openRightSidebar', 'addViewedItemToSidebar'], // 注入來自 BaseLayout 的方法
  components: {
    NIcon, Heart, HeartRegular, CaretDown, EllipsisH, Envelope, EnvelopeRegular,
  },

  props: {
    id: { // 這個 'id' 會接收從路由傳過來的公司 ID
      type: [String, Number],
      required: true
    }
  },

  data() {
    return {
      loveJobItems: [
        { id: 'love_job_1', name: '航空業', image: '/love-job-1.jpg' },
        { id: 'love_job_2', name: '傳統產業', image: '/love-job-2.jpg' },
        { id: 'love_job_3', name: '家具業', image: '/love-job-3.jpg' },
        { id: 'love_job_4', name: '電子產品製造業', image: '/love-job-4.jpg' },
        { id: 'love_job_5', name: '餐飲服務業', image: '/love-job-5.jpg' },
        { id: 'love_job_6', name: '速食餐飲業', image: '/love-job-6.jpg' }
      ],
      selectedLoveJob: null,
      characteristicsMap: {
        '航空業': ['CHINA AIRLINE', 'STARLUX'],
        '傳統產業': ['Toyota', '捷安特'],
        '家具業': ['IKEA', '宜得利'],
        '電子產品製造業': ['GARMIN', '金寶電子'],
        '餐飲服務業': ['路易莎', 'Starbucks'],
        '速食餐飲業': ["mcdonald's", '摩斯漢堡']
      },
      pageSize: 10,
      dropdownOpenJob: false,
      dropdownOpenProfile: false,
      profileOptions: ['分享', '檢舉'],
      showApplyModal: false,
      showShare: false,
      showReport: false,
      applyJobId: 0,
      shareLink: 'https://example.com/share',
      reportReason: '',
      company: null,
      companies: null,
      filterJobs: [],
    };
  },
  watch: {
    // 監聽 id prop 的變化，當 id 改變時重新載入公司資料
    id: {
      immediate: true, // 組件載入時立即執行一次
      async handler(newId) {
        if (newId) {
          this.shareLink = window.location.href;

          const [companiesData, jobsData] = await Promise.all([
            getGreatCompanies(),
            getJobs(),
          ]);
          //console.log(jobsData);
          // 資料處理邏輯（建議放在 mounted 或 API 請求完成後）
          // 企業資料處理（只抓一筆 company 顯示詳細頁）
          const rawCompanies = companiesData.results || companiesData || [];
          this.companies = rawCompanies.map(company => ({
            id: company.id,
            name: company.name,
            image: company.media && company.media.logo ? company.media.logo : 'default_company_logo_path.png',
            industry: company.industry,
            isLiked: company.is_liked_by_user || false, // 【新增】初始化公司的收藏狀態
            originalData: { ...company, type: ITEM_TYPE_COMPANY }, // 【修改】在原始數據中加入 type 屬性
            type: ITEM_TYPE_COMPANY, // 【新增】在頂層也保留 type，方便直接使用 company 物件
          }));

          const rawJobs = jobsData.results || jobsData || [];
          this.allApiJobs = rawJobs.map(job => ({
            id: job.id,
            title: job.title,
            image: job.company_logo?.startsWith('http') 
              ? job.company_logo 
              : 'http://localhost:8000/' + (job.company_logo || 'default_job_image.png'),
            company: {
              name: job.company?.name || '未知公司',
              industry: job.company?.industry || '',
            },
            salary: job.salary_max ? `$${job.salary_max}` : '面議',
            location: job.location || '',
            experience_required: job.experience_required || '不拘',
            education_required: job.education_required || '不拘',
            created_at: job.created_at,
            isLiked: job.is_liked_by_user || false,
            isApplied: job.is_applied_by_user || false,
            benefits: job.benefits || [],
            applicants: job.applicants || 0,
            originalData: { ...job, type: ITEM_TYPE_JOB },
            type: ITEM_TYPE_JOB,
          }));

          // 過濾與目前公司有關的工作
          this.selectedLoveJob = this.loveJobItems.find(item => item.id === newId);
          const currentCharacteristic = this.selectedLoveJob ? this.selectedLoveJob.name : null;

          const companyNames = currentCharacteristic ? this.characteristicsMap[currentCharacteristic] || [] : [];
          this.filterJobs = this.allApiJobs.filter(job => companyNames.includes(job.company.name));

          // 圖片抓色更改背景
          this.$nextTick(() => {
            const logoUrl = this.selectedLoveJob.image || 'default.png';
            const img = new Image();
            img.crossOrigin = 'anonymous';  // 這行很重要
            img.src = logoUrl;

            img.onload = () => {
              this.handleImage(img);
            };

            img.onerror = () => {
              console.error('圖片載入失敗：', logoUrl);
            };
          });
        }
      }
    }
  },
  async mounted() {
    eventBus.on('update-like-status', this.handleUpdateLikeStatus);
  },
  beforeUnmount() {
    eventBus.off('update-like-status', this.handleUpdateLikeStatus);
  },
  computed: {
    paginatedJobs() {
      return Array.isArray(this.filterJobs) ? this.filterJobs.slice(0, this.pageSize) : [0, 0, 0, 0, 0];
    },
    iconHeartSolid() {
      return Heart
    },
    iconHeartRegular() {
      return HeartRegular
    },
    iconEnvelopeSolid() {
      return Envelope
    },
    iconEnvelopeRegular() {
      return EnvelopeRegular
    },
  },
  methods: {
    // data format
    formatDate(isoString) {    // process job.created_at
      const date = new Date(isoString);
      return `${date.getMonth() + 1}/${date.getDate()}`
    },
    formatJobIndustry(jobCompany) {
      return this.companies.find(item => item.name === jobCompany).industry
    },
    formatLocation(location) {
      const loc = location.slice(0, 3);
      return loc
    },
    formattedSalary(jobId) {
      const job = this.filterJobs.find(i => i.id === jobId)

      if (job.salary_type === '月薪') {
        return `月薪${job.salary_min}~${job.salary_max}元`;
      } else if (job.salary_type === '時薪') {
        return `時薪${job.salary_number}元`;
      } else {
        return '薪資未提供';
      }
    },
    // dropdown 顯示
    toggleDropdownJob() {
      this.dropdownOpenJob = !this.dropdownOpenJob
    },
    toggleDropdownProfile() {
      this.dropdownOpenProfile = !this.dropdownOpenProfile;
    },
    selectPageSize(size) {
      this.pageSize = size
      this.dropdownOpenJob = false
    },
    selectAction(option) {
      switch (option) {
        case '分享':
          console.log('執行分享功能');
          this.showShare = true;
          break;
        case '檢舉':
          console.log('執行檢舉功能');
          this.showReport = true;
          break;
        default:
          console.warn('未知選項', option);
      }
      this.dropdownOpenProfile = false
    },
    // heart icon clicked
    // item 可能是 job 或 company 物件，它已經包含 isLiked 和 originalData (其中包含 type)
    async toggleLike(item) {
      // 假設需要登入才能收藏
      // if (!this.isUserLoggedIn) { 
      //   alert('您需要先登入才能收藏！');
      //   return;
      // }
      console.log('test');

      if (!item || !item.id || !item.type) {
        console.error('toggleLike: 無效的項目數據或缺少 ID/類型', item);
        return;
      }

      const originalLikedStatus = item.isLiked;
      const newLikedStatus = !item.isLiked;

      // 1. 樂觀更新 UI (直接修改傳入的 item 物件)
      item.isLiked = newLikedStatus;

      try {
        // 2. 呼叫後端 API (統一使用 likeJob/unlikeJob)
        if (newLikedStatus) {
          await likeJob(item.id); // 假設 likeJob API 能處理職缺和公司 ID
        } else {
          await unlikeJob(item.id); // 假設 unlikeJob API 能處理職缺和公司 ID
        }

        // 3. 通知 BaseLayout 更新側邊欄的收藏和瀏覽紀錄列表
        // 傳遞 item.originalData 和新的 isLiked 狀態
        if (typeof this.updateLikedItemInSidebar === 'function') {
          this.updateLikedItemInSidebar(item.originalData || item, newLikedStatus); // originalData 已經包含 type
        }

        // 4. 透過 eventBus 通知所有頁面同步愛心狀態
        // 統一事件名稱 'update-like-status'，並傳遞 ID, 類型, 和新狀態
        eventBus.emit('update-like-status', { id: item.id, type: item.type, isLiked: newLikedStatus });

      } catch (error) {
        console.error(`Failed to update ${item.type} like status for ID ${item.id}:`, error);
        // API 失敗，恢復 UI 狀態
        item.isLiked = originalLikedStatus;
        alert(`收藏操作失敗，請稍後再試。`);

        // 恢復 BaseLayout 列表狀態
        if (typeof this.updateLikedItemInSidebar === 'function') {
          this.updateLikedItemInSidebar(item.originalData || item, originalLikedStatus);
        }
        // 通知所有頁面恢復愛心狀態
        eventBus.emit('update-like-status', { id: item.id, type: item.type, isLiked: originalLikedStatus });
      }
    },
    // 處理來自 eventBus 的通用愛心狀態更新事件
    handleUpdateLikeStatus(data) { // data 預期為 { id: itemId, type: itemType, isLiked: newStatus }
      const { id, type, isLiked } = data;
      // 1. 更新 sections 中的職缺愛心狀態
      if (type === ITEM_TYPE_JOB) {
        const jobInSection = this.filterJobs.find(j => j.id === id);
          if (jobInSection) {
            jobInSection.isLiked = isLiked;
          }
      }
      // 2. 更新 companies 中的公司愛心狀態
      else if (type === ITEM_TYPE_COMPANY) {
        const companyToUpdate = this.company;
        if (companyToUpdate) {
          companyToUpdate.isLiked = isLiked;
        }
      }
    },
    handleCardClick(jobData) {
      const dataForSidebar = jobData.originalData || jobData; // 確保取得原始 API 數據
      if (typeof this.addViewedItemToSidebar === 'function') {
        this.addViewedItemToSidebar(dataForSidebar)
      } else {
        console.error('addViewedItemToSidebar is not available from BaseLayout')
      }

      if (typeof this.openRightSidebar === 'function') {
        this.openRightSidebar(dataForSidebar)
      } else {
        console.error('openRightSidebar is not available from BaseLayout')
      }
    },
    handleTitleClick(job) {
      this.$router.push({ name: 'jobdetail', params: { id: job.id } });
    },
    //應徵彈窗
    openModal(id) {
      this.applyJobId = id;
      this.currentItem = this.paginatedJobs.find(job => job.id === id);
      this.showApplyModal = true;
      // 重置表單
      this.formData = {
        title: '',
        content: ''
      };
      this.selectedFiles = [];
    },
    closeModal() {
      this.showApplyModal = false;
    },
    handleFileUpload(event) {
      //file when apply
      this.selectedFiles = Array.from(event.target.files);
    },
    handleSubmit(jobId) {
      const item = this.paginatedJobs.find(job => job.id === jobId);
      console.log("item",item);
      // 這裡可以處理送出邏輯
      console.log('送出資料:', {
        item: item,
        formData: this.formData,
        files: this.selectedFiles
      });

      alert('資料已送出！');
      item.isApplied = true;

      this.closeModal();
    },
    copyLink() {
      navigator.clipboard.writeText(shareLink.value)
      alert('已複製連結')
    },
    submitReport() {
      if (!reason.value.trim()) {
        alert('請填寫檢舉原因')
        return
      }
      alert(`檢舉已送出：${reason.value}`)
      reason.value = ''
      showReport.value = false
    },
    //head image 擷取顏色，並更改背景
    handleImage(img) {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');

      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      ctx.drawImage(img, 0, 0);

      const imageData = ctx.getImageData(0, 0, img.naturalWidth, 50);
      const pixels = imageData.data;

      let r = 0, g = 0, b = 0, count = 0;
      for (let i = 0; i < pixels.length; i += 4) {
        r += pixels[i];
        g += pixels[i + 1];
        b += pixels[i + 2];
        count++;
      }

      r = Math.floor(r / count);
      g = Math.floor(g / count);
      b = Math.floor(b / count);

      const avgColor = `rgb(${r}, ${g}, ${b})`;

      // 改變背景
      const contentEl = document.querySelector('.middle-content');
      contentEl.style.background = `linear-gradient(
                                    to bottom,
                                    ${avgColor} 0px,
                                    #121212 720px,
                                    #121212 100%
                                    )`;
    }
  }
})
</script>

<style scoped>
.middle-content {
  background-color: linear-gradient(to bottom,#b3b3b3 0%,#121212 20%,#121212 100%);
  border-radius: 10px;
  color: white;
  box-sizing: border-box;
  font-family: 'Roboto', sans-serif;
  font-size: 14px;
}

/* actions button */
.actions-button {
  display: inline-flex;
  align-items: flex-start;
  width: auto;
  max-width: 100%;
}

.profile-button {
  margin-top: 16px;
}

.like-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: white;
  /* 空心愛心預設白色 */
  font-size: 24px;
  padding: 3px;
  transition: transform 0.5s ease, color 0.3s ease;
}

.like-btn:hover {
  transform: scale(1.1);
}

.like-btn.active {
  color: rgb(235, 178, 189);
  /* 喜歡後變成粉色實心 */
}

/* dropdown icon */
.ellipsis-icon {
  font-size: 24px;
  margin-left: 10px;

}

/* 應徵 icon */
.envelope-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: white;
  font-size: 24px;
  margin-left: 10px;
  padding: 3px;
  transition: transform 0.5s ease, color 0.3s ease;
}

.envelope-btn:hover {
  transform: scale(1.1);
}

/* dropdown styles */
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-toggle {
  background: none;
  border: none;
  cursor: pointer;
  color: white;
  font-size: 18px;
  padding: 3px;
  transition: transform 0.5s ease, color 0.3s ease;
}

.dropdown-toggle:hover {
  transform: scale(1.1);
}

.dropdown-menu {
  list-style: none;
  margin: 0;
  padding: 0;
  background-color: rgba(0, 0, 0, 0.6);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  position: absolute;
  z-index: 1000;
  min-width: 120px;
  max-width: 10vw;
}

.dropdown-menu.bottom-left {
  top: 100%;
  left: 0;
  right: auto;
}

.dropdown-menu.bottom-right {
  top: 100%;
  left: auto;
  right: 0;
}

.dropdown-menu li {
  padding: 8px 12px;
  cursor: pointer;
  white-space: nowrap;
}

.dropdown-menu li:hover {
  background-color: #f0f0f0;
}

/* company profile */
.company-profile {
  display: flex;
  width: 100%;
  flex-direction: column;
  padding: 48px 28px 40px;
  background: transparent;
}

.profile-container {
  padding: 0;
}

.profile-grid {
  display: flex;
  gap: 20px;
  align-items: flex-end;
}

.logo-column {
  width: 239px;
}

.company-logo {
  box-shadow: 0px 0px 24px rgba(0, 0, 0, 0.25);
  height: 239px;
  overflow: hidden;
  display: flex;
  align-items: flex-end;
  /* 圖片貼底 */
}

.logo-image {
  width: 100%;
  object-fit: contain;
}

.info-column {
  width: 64%;
}

.company-info {
  color: #fff;
  font-family: Roboto, -apple-system, Roboto, Helvetica, sans-serif;
}

.info-label {
  font-size: 16px;
  font-weight: 500;
  letter-spacing: -0.32px;
}

.company-name {
  font-size: 40px;
  font-weight: 900;
  margin: 23px 0 0;
}

.company-tags {
  font-size: 20px;
  font-weight: 400;
  margin: 20px 0 0;
}

.job-count {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.18px;
  margin: 14px 0 0;
}

/* section title for 職缺&關於*/
.section-title {
  font-family: 'Noto Sans', sans-serif;
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 16px;
}

/* job listings */
.job-listings {
  margin: 0;
  padding: 28px;
  background-color: rgba(0, 0, 0, 0.3);
}

.listings-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  width: 100%;
  color: #fff;
  font-family: Noto Sans, -apple-system, Roboto, Helvetica, sans-serif;
}

.page-size {
  display: flex;
  gap: 10px;
  border-radius: 40px;
  padding: 3px 12px 28px 3px;
  font-size: 18px;
  font-weight: 400;
  letter-spacing: -0.18px;
}

/* JobCard 样式 */
.job-card {
  border-radius: 10px;
  background-color: rgba(255, 255, 255, 0.1);
  margin-top: 12px;
  padding: 20px 24px;
  overflow: hidden;
  cursor: pointer;
}

.job-content {
  display: flex;
  justify-content: space-between;
}

.main-info {
  display: flex;
  align-items: flex-start;
}

.date-block {
  margin-top: 3px;
  width: 40px;
}

.date {
  color: #b3b3b3;
  font-size: 16px;
  font-weight: 400;
}

.content-block {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding-left: 12px;
}

.header {
  font-family: Roboto, -apple-system, Roboto, Helvetica, sans-serif;
}

.title {
  color: #f5f5f5;
  font-size: 20px;
  font-weight: 600;
  letter-spacing: 0.2px;
  margin: 0;
  cursor: pointer;
}

.title:hover {
  text-decoration: underline;
}

.details {
  margin-top: 2px;
}

.company-info-job {
  display: flex;
  align-items: center;
  gap: 24px;
  font-size: 16px;
  font-weight: 500;
}

.company-name-job {
  color: #f5f5f5;
  font-family: Roboto, -apple-system, Roboto, Helvetica, sans-serif;
}

.industry-job {
  color: #b3b3b3;
  font-family: Noto Sans, -apple-system, Roboto, Helvetica, sans-serif;
}

.job-specs {
  display: flex;
  align-items: center;
  margin-top: 10px;
  gap: 24px;
  font-family: Noto Sans, -apple-system, Roboto, Helvetica, sans-serif;
  color: #f5f5f5;
  font-size: 16px;
  font-weight: 600;
}

.spec {
  font-weight: bold;
}

.benefits {
  display: flex;
  margin: 6px 0;
  flex-wrap: wrap;
  gap: 12px;
}

.benefit-tag-job {
  border-radius: 16px;
  background-color: rgba(179, 179, 179, 0.25);
  padding: 5px 10px;
  color: #b3b3b3;
  font-family: Noto Sans, -apple-system, Roboto, Helvetica, sans-serif;
  font-size: 14px;
  font-weight: 400;
}

.applicants {
  color: #f5f5f5;
  font-size: 16px;
  font-family: Noto Sans, -apple-system, Roboto, Helvetica, sans-serif;
  font-weight: 500;
  text-align: right;
  margin: 6px 0 0;
}

/*company information*/
.company-information {
  margin: 0;
  padding: 28px;
  background-color: rgba(0, 0, 0, 0.3);
}

.cards {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

div h3 {
  font-family: 'Noto Sans', sans-serif;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
}

/* Info Cards */
.info-card {
  background: rgba(255, 255, 255, 0.1);
  margin: 0;
  padding: 24px;
  border-radius: 10px;
}

.company-details {
  display: grid;
  grid-template-columns: 227px 1fr;
  gap: 30px;
}

.detail-group {
  margin-bottom: 50px;
  overflow: hidden;
}

.detail-item {
  margin-bottom: 20px;
}

.detail-item .label {
  font-size: 16px;
  font-weight: 600;
  font-family: 'Noto Sans', sans-serif;
}

.detail-item .value {
  font-size: 14px;
  color: #b3b3b3;
  margin-top: 5px;
}

.description {
  font-size: 16px;
  line-height: 1.6;
  color: #b3b3b3;
}

.benefits-grid {
  display: grid;
  grid-template-columns: 227px 1fr;
  gap: 30px;
}

.benefit-tags h4 {
  font-family: 'Noto Sans', sans-serif;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 20px;
}

.benefit-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.benefit-tag {
  background: rgba(179, 179, 179, 0.25);
  padding: 5px 10px;
  border-radius: 16px;
  font-size: 14px;
  width: fit-content;
}

.benefits-description h4 {
  font-size: 14px;
  color: #b3b3b3;
  margin-bottom: 10px;
}

/* Gallery */
.gallery {
  background: rgba(255, 255, 255, 0.1);
  margin: 0;
  padding: 24px;
  border-radius: 10px;
}

.gallery-scroll-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.gallery-grid {
  display: flex;
  gap: 24px;
  width: max-content;
  height: 200px;
  background: transparent;
  margin: 0;
}

.gallery-item {
  flex: 0 0 auto;
  aspect-ratio: 3 / 2;
  background: transparent;
  box-shadow: 0 0 24px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

.gallery-item img {
  display: block;
  width: auto;
  height: 100%;
  max-height: 200px;
  object-fit: contain;
}

/* Modal 樣式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(10px);/* 模糊背景效果 */
}

.modal {
  background: linear-gradient(135deg, #191414, #2a2a2a);
  border-radius: 5px;
  width: 90%;
  max-width: 500px;
  padding: 30px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);/* 投影效果 */
  position: relative;/* 相對定位，可用於內部絕對定位元素 */
}

.modal-header {
  margin-bottom: 30px;/* 底部間距 */
  text-align: center;/* 文字置中對齊 */
}

.modal-title {
  font-size: 18px;/* 文字大小 */
  font-weight: bold;/* 字體粗體 */
  color: #D2691E;/* 橘色標題 */
  margin-bottom: 10px;/* 標題與下方元素的間距 */
}


/* 表單區塊 */
.form-group {
  margin-bottom: 20px;/* 元素間的底部間距 */
}

.form-label {
  display: block;/* 佔滿整行 */
  margin-bottom: 8px;/* 與輸入欄的間距 */
  font-weight: bold;/* 字體粗體 */
  color: #ffffff;/* 白色文字 */
  font-size: 16px;/* 標籤字體大小 */
  text-transform: uppercase;/* 字母大寫 */
  letter-spacing: 1px;/* 字元間距 */
}

.form-input {
  width: 100%;/* 寬度佔滿父容器 */
  padding: 15px;/* 內距 */
  border: 2px solid rgba(255, 255, 255, 0.1);/* 淡白色邊框 */
  border-radius: 5px;/* 圓角 */
  background-color: rgba(255, 255, 255, 0.05);/* 半透明白背景 */
  color: white;/* 輸入文字為白色 */
  font-size: 1rem;/* 標準字體大小 */
  transition: all 0.3s ease;/* 動畫過渡效果 */
}

.form-input:focus {
  outline: none;/* 移除瀏覽器預設外框 */
  border-color: #D2691E;/* 聚焦時變成橘色邊框 */
  background-color: rgba(255, 255, 255, 0.1);/* 背景稍微變亮 */
}

.form-textarea {
  resize: vertical;/* 垂直方向可調整大小 */
  min-height: 80px;/* 最小高度為 80px */
  font-family: inherit;/* 使用繼承字體 */
}

.file-upload-btn {
  box-sizing: border-box;
  width: 100%;
  height: 80px;
  padding: 15px;
  border: 2px dashed #D2691E;
  border-radius: 10px;
  background-color: rgba(244, 188, 103, 0.1);
  color: #D2691E;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  line-height: 47px;/* 水平置中 */
  font-weight: 600;
  position: relative;
}

.file-upload-btn:hover {
  border-color: #D2691E;
  background-color: rgba(244, 188, 103, 0.4);
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  opacity: 0;
  width: 100%;
  height: 80px;
  cursor: pointer;
}



.modal-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 30px;
}

/* btns for modal */
.btn {
  padding: 4px 20px;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 50px;
}

.btn-cancel {
  background-color: transparent;
  color: #b3b3b3;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.btn-cancel:hover {
  color: white;
  border-color: rgba(255, 255, 255, 0.4);
  background-color: rgba(255, 255, 255, 0.1);
}

.btn-submit {
  background: linear-gradient(135deg, #D2691E, #D2691E);
  color: white;
  box-shadow: 0 4px 10px rgba(244, 188, 103, 0.3);
}

.btn-submit:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 10px rgba(244, 188, 103, 0.4);
}

.btn-submit:active {
  transform: translateY(0);
}

/* 動畫效果 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal,
.modal-leave-active .modal {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal,
.modal-leave-to .modal {
  transform: scale(0.8) translateY(50px);
}
</style>
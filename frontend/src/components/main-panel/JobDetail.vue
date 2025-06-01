<template>
  <div class="middle-content">
    <div v-if="!jobDetail">
      載入中...
    </div>
    <!-- 資料載入後才顯示內容 -->
    <div v-else>
      <section class="company-profile">
        <div class="profile-container">
          <div class="profile-grid">
            <div class="logo-column">
              <div class="company-logo">
                <img ref="avatar" :src="jobDetail.image" alt="Company Logo" class="logo-image" />
              </div>
            </div>
            <div class="info-column">
              <div class="company-info">
                <span class="info-label">工作機會詳細資訊</span>
                <h1 class="company-name">{{ jobDetail.title }}</h1>
                <p class="company-tags">
                  <router-link :to="companyLink" class="company-link">{{ jobDetail.company.name }}</router-link>
                </p>
                <p class="job-count">{{ formatDate(jobDetail.created_at) }}更新</p>
              </div>
            </div>
          </div>
        </div>
        <div class="profile-button actions-button">
          <button type="button" class="like-btn" :class="{ active: jobDetail.isLiked }"
            @click.stop="toggleLike(jobDetail)">
            <n-icon class="heart-icon">
              <component :is="jobDetail.isLiked ? iconHeartSolid : iconHeartRegular" />
            </n-icon>
          </button>
          <button type="button" class="envelope-btn"
                @click.stop="openModal(jobDetail.id)">
                <n-icon class="envelope-icon">
                  <component :is="jobDetail.isApplied ? iconEnvelopeSolid : iconEnvelopeRegular" />
                </n-icon>
          </button>
        </div>
      </section>

      <section class="company-information">
        <h2 class="section-title">關於</h2>
        <div class="cards">
          <div class="info-card">
            <h3>{{ jobDetail.title }}</h3>
            <div class="company-details">
              <div>
                <div class="detail-group">
                  <div class="detail-item">
                    <div class="label">{{ jobDetail.characteristics }}</div>
                    <div class="value">職業類別</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ formattedSalary(jobDetail.id) }}</div>
                    <div class="value">工作待遇</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ jobDetail.recruitment_type }}</div>
                    <div class="value">工作性質</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ jobDetail.location }}</div>
                    <div class="value">上班地點</div>
                  </div>
                </div>
                <div class="detail-group">
                  <div class="detail-item">
                    <div class="label">{{ jobDetail.experience_required }}</div>
                    <div class="value">經歷要求</div>
                  </div>
                  
                  <div class="detail-item">
                    <div class="label">{{ jobDetail.education_required }}</div>
                    <div class="value">學歷要求</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ jobDetail.major_required }}</div>
                    <div class="value">學位要求</div>
                  </div>
                </div>

                <div class="detail-group">
                  <div class="detail-item">
                    <div class="benefit-group">
                      <div class="benefit-tag" v-for="(b, index) in jobDetail.benefits" :key="'tag' + index">
                        {{ b.benefits_description }}
                      </div>
                    </div>
                    <div class="value">福利制度</div>
                  </div>
                </div>
              </div>

              <div class="description" v-html="jobDetail.description.replace(/\n/g, '<br><br>')"></div>
            </div>
          </div>

        </div>
      </section>
      <!-- Modal 彈窗 -->
      <transition name="modal">
        <div v-if="showApplyModal" class="modal-overlay" @click="closeModal">
          <div class="modal" @click.stop>
            <div class="modal-header">
              <h2 class="modal-title">{{ jobDetail.name }}</h2>
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
import { getJobDetail, getGreatCompanies } from '@/api/home.js';//暫時用home
import { NIcon } from 'naive-ui'
import { Heart, HeartRegular, CaretDown, EllipsisH, Envelope, EnvelopeRegular } from '@vicons/fa'

const ITEM_TYPE_JOB = 'job';
const ITEM_TYPE_COMPANY = 'company';

export default defineComponent({
  name: 'JobDetail',
  inject: ['updateLikedItemInSidebar', 'openRightSidebar', 'addViewedItemToSidebar','isItemCurrentlyLiked'], // 注入來自 BaseLayout 的方法
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
      jobDetail: null,
      jjobs: [],
    };
  },
  watch: {
    // 監聽 id prop 的變化，當 id 改變時重新載入公司資料
    id: {
      immediate: true, // 組件載入時立即執行一次
      async handler(newId) {
        if (newId) {
          const [jobDetailData, companiesData] = await Promise.all([
            getJobDetail(newId),
            getGreatCompanies(),
          ]);
          
          const rawJobDetail = jobDetailData.results || jobDetailData || [];
          this.jobDetail = {
            id: rawJobDetail.id,
            title: rawJobDetail.title,
            image: rawJobDetail.company_logo?.startsWith('http') 
              ? rawJobDetail.company_logo 
              : 'http://localhost:8000/' + (rawJobDetail.company_logo || 'default_job_image.png'),
            company: {
              name: rawJobDetail.company?.name || '未知公司',
              industry: rawJobDetail.company?.industry || '',
            },
            salary: rawJobDetail.salary_max ? `$${rawJobDetail.salary_max}` : '面議',
            characteristics: rawJobDetail.characteristics || '為提供',
            recruitment_type: rawJobDetail.recruitment_type || '為提供',
            location: rawJobDetail.location || '',
            experience_required: rawJobDetail.experience_required || '不拘',
            education_required: rawJobDetail.education_required || '不拘',
            major_required: rawJobDetail.major_required || '不拘',
            created_at: rawJobDetail.created_at,
            description: rawJobDetail.description,
            //isLiked: rawJobDetail.is_liked_by_user || false,
            isApplied: rawJobDetail.is_applied_by_user || false,
            benefits: rawJobDetail.benefits || [],
            applicants: rawJobDetail.applicants || 0,
            originalData: { ...rawJobDetail, type: ITEM_TYPE_JOB },
            type: ITEM_TYPE_JOB,
          };

          // 【新增】在數據加載後，從 BaseLayout 獲取最新收藏狀態，覆蓋初始狀態
        if (typeof this.isItemCurrentlyLiked === 'function') {
          this.jobDetail.isLiked = this.isItemCurrentlyLiked(this.jobDetail.id, this.jobDetail.type);
        } else {
            // 如果 isItemCurrentlyLiked 未被注入，則使用 API 返回的原始值
            this.jobDetail.isLiked = rawJobDetail.is_liked_by_user || false;
        }

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

          // 圖片抓色更改背景
          this.$nextTick(() => {
            const logoUrl = this.jobDetail.image || 'default.png';
            const img = new Image();
            img.crossOrigin = 'anonymous';  // ⚠️ 這行很重要
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
  mounted() {
    // 【新增】監聽來自 BaseLayout 或 LeftSidebar 的收藏狀態更新事件
    eventBus.on('update-like-status', this.handleUpdateLikeStatus);
  },
  beforeUnmount() {
    // 【新增】在組件銷毀前移除事件監聽器
    eventBus.off('update-like-status', this.handleUpdateLikeStatus);
  },
  computed: {
    companyLink() {
      const companyName = this.jobDetail.company.name;
      // 從 this.companies 找出 name 相同的公司
      const company = this.companies.find(c => c.name === companyName);

      if (company && company.id) {
        return `/company/${company.id}/`;
      } else {
        // 找不到公司，回傳預設路徑或空字串
        return '../';
      }
    },
    paginatedJobs() {
      return Array.isArray(this.jjobs) ? this.jjobs.slice(0, this.pageSize) : [0, 0, 0, 0, 0];
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
    formatLocation(location) {
      const loc = location.slice(0, 3);
      return loc
    },
    formattedSalary(jobId) {
      const job = this.jobDetail

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
          this.showShare = true;
          break;
        case '檢舉':
          this.showReport = true;
          break;
        default:
          console.warn('未知選項', option);
      }
      this.dropdownOpenProfile = false
    },
    // heart icon clicked
    // item 可能是 job 或 company 物件，它已經包含 isLiked 和 originalData (其中包含 type)
    async toggleLike(job) {
      // 檢查是否是有效的職缺數據，包含 ID 和類型
      if (!job || !job.id || job.type !== ITEM_TYPE_JOB) {
        console.error('toggleLike: 無效的職缺數據或類型不符', job);
        return;
      }

      // 1. 樂觀更新 UI
      const newLikedStatus = !job.isLiked;
      job.isLiked = newLikedStatus;

      // 2. 通知 BaseLayout 更新側邊欄的收藏和瀏覽紀錄列表
      // 傳遞 job.originalData (原始 API 數據，包含 type) 和新的 isLiked 狀態
      if (typeof this.updateLikedItemInSidebar === 'function') {
        this.updateLikedItemInSidebar(job.originalData || job, newLikedStatus);
      } else {
        console.warn('updateLikedItemInSidebar is not available from BaseLayout.');
      }

      // 3. 透過 eventBus 通知所有頁面同步愛心狀態
      // 因為收藏職缺不需要後端，所以沒有 API 失敗回滾的問題，直接發送最終狀態即可。
      eventBus.emit('update-like-status', { id: job.id, type: job.type, isLiked: newLikedStatus });
    },
    // 處理來自 eventBus 的通用愛心狀態更新事件
    handleUpdateLikeStatus(data) {
      const { id, type, isLiked } = data;
      // 只處理當前頁面 jobDetail 的收藏狀態
      if (type === ITEM_TYPE_JOB && this.jobDetail && this.jobDetail.id === id) {
        this.jobDetail.isLiked = isLiked;
      }
    },
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
      const item = this.jobDetail;

      alert('資料已送出！');
      item.isApplied = true;

      this.closeModal();
    },
    copyLink() {
      navigator.clipboard.writeText(this.shareLink);
      alert(`已複製連結：${this.shareLink}`);
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

  white-space: nowrap;      /* 不換行 */
  overflow: hidden;         /* 超出部分隱藏 */
  text-overflow: ellipsis;  /* 顯示省略號 */
  max-width: 100%;          /* 限制寬度，避免無限延伸 */
}

.company-tags {
  font-size: 20px;
  font-weight: 700;
  margin: 20px 0 0;
}

.company-link {
  color:#fff;
  font-size: 20px;
  font-weight: 700;
}

.company-link:hover {
  background-color: transparent !important;
  text-decoration: underline;
}

.job-count {
  font-size: 18px;
  font-weight: 400;
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
  grid-template-columns: 300px 1fr;
  gap: 30px;
}

.detail-group {
  margin-bottom: 40px;
  overflow: hidden;
}

.detail-item {
  margin-bottom: 16px;
}

.detail-item .label {
  font-size: 16px;
  font-weight: 600;
  font-family: 'Noto Sans', sans-serif;
}

.detail-item .value {
  font-size: 14px;
  color: #b3b3b3;
  margin-top: 2px;
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
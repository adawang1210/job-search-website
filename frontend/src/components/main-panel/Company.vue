<template>
  <div class="middle-content">
    <div v-if="!company || !filterJobs">
      載入中...
    </div>
    <!-- 資料載入後才顯示內容 -->
    <div v-else>
      <section class="company-profile">
        <div class="profile-container">
          <div class="profile-grid">
            <div class="logo-column">
              <div class="company-logo">
                <img ref="avatar" :src="company.image" alt="Company Logo" class="logo-image" />
              </div>
            </div>
            <div class="info-column">
              <div class="company-info">
                <span class="info-label">公司</span>
                <h1 class="company-name">{{ company.name }}</h1>
                <p class="company-tags">{{ company.bg_color_hex }}</p>
                <p class="job-count">{{ filterJobs.length }}個工作機會</p>
              </div>
            </div>
          </div>
        </div>
        <div class="profile-button actions-button">
          <button type="button" class="like-btn" :class="{ active: company.isLiked }" @click.stop="toggleLike(company)">
            <n-icon class="heart-icon">
              <component :is="company.isLiked ? iconHeartSolid : iconHeartRegular" />
            </n-icon>
          </button>
          <div class="ellipsis-button">
            <div class="dropdown">
              <button type="button" class="dropdown-toggle" @click="toggleDropdownProfile">
                <n-icon class="ellipsis-icon">
                  <EllipsisH />
                </n-icon>
              </button>
              <ul v-show="dropdownOpenProfile" class="dropdown-menu bottom-left">
                <li v-for="(item, index) in profileOptions" :key="index" @click="selectAction(item)">
                  {{ item }}
                </li>
              </ul>
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
                    <span class="industry-job">{{ company?.industry }}</span>
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
              <button type="button" class="like-btn" :class="{ active: job.isLiked }" @click.stop="toggleLike(job)">
                <n-icon class="heart-icon">
                  <component :is="job.isLiked ? iconHeartSolid : iconHeartRegular" />
                </n-icon>
              </button>
              <button type="button" class="envelope-btn" @click.stop="openModal(job.id)">
                <n-icon class="envelope-icon">
                  <component :is="job.isApplied ? iconEnvelopeSolid : iconEnvelopeRegular" />
                </n-icon>
              </button>

              <!-- <p class="applicants">{{ job.applicants }}</p> -->
            </div>
          </div>
        </article>
      </section>

      <section class="company-information">
        <h2 class="section-title">關於</h2>
        <div class="cards">
          <div class="info-card">
            <h3>公司介紹</h3>
            <div class="company-details">
              <div>
                <div class="detail-group">
                  <div class="detail-item">
                    <div class="label">{{ company?.industry }}</div>
                    <div class="value">產業類別</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ company?.industry_description }}</div>
                    <div class="value">產業描述</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ company?.employees }}</div>
                    <div class="value">員工人數</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ company?.capital }}</div>
                    <div class="value">資本額</div>
                  </div>
                </div>

                <div class="detail-group">
                  <div class="detail-item">
                    <div class="label">{{ company.contacts[0].name }}</div>
                    <div class="value">聯絡人</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ company.contacts[0].phone }}</div>
                    <div class="value">電話</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ company.contacts[0].fax }}</div>
                    <div class="value">傳真</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ company.contacts[0].email }}</div>
                    <div class="value">地址</div>
                  </div>
                </div>

                <div class="detail-group">
                  <div class="detail-item" v-for="(link, index) in company.websites" :key="index">
                    <div class="label">{{ link.website }}</div>
                  </div>
                </div>
              </div>

              <div class="description" v-html="company.introduction.replace(/\n/g, '<br><br>')"></div>
            </div>
          </div>

          <!-- 主要商品 -->
          <div class="info-card">
            <h3>主要商品</h3>
            <div class="description">
              對外：{{ company?.main_product }}<br>
              <!-- 對內：{{ company?.main_product }}<br><br> -->
            </div>
          </div>

          <!-- 福利制度 -->
          <div class="info-card">
            <h3>福利制度</h3>
            <div class="benefits-grid">
              <div class="benefit-tags">
                <div class="benefit-group">
                  <div class="benefit-tag" v-for="(tag, index) in company.benefits[0].statutory" :key="'tag' + index">
                    {{ tag.benefit }}
                  </div>
                </div>
                <h4>法定項目</h4>

                <div class="benefit-group">
                  <div class="benefit-tag" v-for="(law, index) in company.benefits[0].others" :key="'legal' + index">{{
                    law.benefit }}</div>
                </div>
                <h4>其他福利</h4>
              </div>

              <div class="description">
                <div class="content" v-html="company.benefits[0].benefits_description.replace(/\n/g, '<br>')"></div>
              </div>
            </div>
          </div>

          <div class="gallery">
            <h3>企業照片</h3>
            <n-marquee :play-reversed="true" :auto-play="true" :interval="3000" :style="{ padding: '0', margin: '0' }">
              <div class="project-group" v-for="(photo, index) in company.photos" :key="photo.id">
                <div class="project-cover">
                  <n-image :src="photo.photo" :alt="'Photo ' + (index + 1)" class="project-image" />
                </div>
              </div>
            </n-marquee>

          </div>

        </div>
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
import { getCompanyInfo, getCompanyJobs, updateLikedCompanies } from '@/api/company';
import { NIcon, NMarquee, NImage } from 'naive-ui'
import { Heart, HeartRegular, CaretDown, EllipsisH, Envelope, EnvelopeRegular } from '@vicons/fa'

const ITEM_TYPE_JOB = 'job';
const ITEM_TYPE_COMPANY = 'company';

export default defineComponent({
  name: 'Company',
  inject: ['updateLikedItemInSidebar', 'openRightSidebar', 'addViewedItemToSidebar', 'isItemCurrentlyLiked'], // 注入來自 BaseLayout 的方法
  components: {
    NIcon, NMarquee, NImage, Heart, HeartRegular, CaretDown, EllipsisH, Envelope, EnvelopeRegular,
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
      filterJobs: [],
      allApiJobs: [],
    };
  },
  watch: {
    // 監聽 id prop 的變化，當 id 改變時重新載入公司資料
    id: {
      immediate: true, // 組件載入時立即執行一次
      async handler(newId) {
        if (newId) {
          this.shareLink = window.location.href;
          // 重置狀態
          this.company = null;
          this.filterJobs = [];
          try {
            const [companyData, jobsData] = await Promise.all([
              getCompanyInfo(newId),
              getCompanyJobs(), // 假設這個 API 返回所有職缺，您需要在這裡過濾
            ]);

            // 企業資料處理
            const rawCompany = companyData.results || companyData || {};
            const currentCompany = rawCompany; // 你可以用 ID 過濾正確公司
            this.company = { // 【修改】確保 company 包含 isLiked 和 type 屬性
              id: rawCompany.id,
              name: rawCompany.name,
              image: rawCompany.media?.logo || 'default_company_logo_path.png',
              industry: rawCompany.industry || '',
              industry_description: rawCompany.industry_description || '',
              employees: rawCompany.employees || '',
              capital: rawCompany.capital || '',
              media: rawCompany.media || {},
              introduction: rawCompany.introduction || '',
              main_product: rawCompany.main_product || '',
              contacts: rawCompany.contacts || [],
              websites: rawCompany.websites || [],
              benefits: rawCompany.benefits || [{
                statutory: [],
                others: [],
                benefits_description: ''
              }],
              photos: (rawCompany.media && rawCompany.media.photos) ? rawCompany.media.photos : [],
              isLiked: rawCompany.is_liked_by_user || false, // 初始收藏狀態來自後端
              originalData: { ...rawCompany, type: ITEM_TYPE_COMPANY }, // 在 originalData 中加入 type
              type: ITEM_TYPE_COMPANY // 在頂層也保留 type
            };

            // 職缺數據處理
            const rawJobs = jobsData.results || jobsData || [];
            this.allApiJobs = rawJobs.map(job => ({ // 【修改】確保每個 job 都包含 isLiked 和 type 屬性
              id: job.id,
              title: job.title,
              image: job.company_logo?.startsWith('http')
                ? job.company_logo
                : 'http://localhost:8000/' + (job.company_logo || 'default_job_image.png'),
              company: {
                name: job.company?.name || '未知公司',
                industry: job.company?.industry || '',
              },
              salary_type: job.salary_type,
              salary_min: job.salary_min,
              salary_max: job.salary_max,
              salary_number: job.salary_number,
              location: job.location || '',
              experience_required: job.experience_required || '不拘',
              education_required: job.education_required || '不拘',
              created_at: job.created_at,
              isLiked: job.is_liked_by_user || false, // 初始收藏狀態來自後端
              isApplied: job.is_applied_by_user || false,
              benefits: job.benefits || [],
              applicants: job.applicants || 0,
              originalData: { ...job, type: ITEM_TYPE_JOB }, // 在 originalData 中加入 type
              type: ITEM_TYPE_JOB, // 在頂層也保留 type
            }));


            // 過濾與目前公司有關的工作
            this.filterJobs = this.allApiJobs.filter(job => job.company.name === this.company.name);

            // 【新增】在數據加載後，從 BaseLayout 獲取最新收藏狀態，覆蓋初始狀態
            // 由於 isItemCurrentlyLiked 是一個方法，我們在 loaded 的數據上直接調用
            if (typeof this.isItemCurrentlyLiked === 'function') {
                // 更新公司自身的收藏狀態
                this.company.isLiked = this.isItemCurrentlyLiked(this.company.id, this.company.type);
                
                // 更新每個職缺的收藏狀態
                this.filterJobs.forEach(job => {
                    job.isLiked = this.isItemCurrentlyLiked(job.id, job.type);
                });
            }

            // 圖片抓色更改背景
            this.$nextTick(() => {
              const logoUrl = this.company.image || 'default.png';
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
            } catch (error) {
            console.error('Error fetching company or jobs:', error);
            // 處理錯誤狀態，例如顯示錯誤訊息給用戶
          }
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
    formatLocation(location) {
      const loc = location.slice(0, 3);
      return loc
    },
    formattedSalary(jobId) {
      const job = this.filterJobs.find(i => i.id === jobId);

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
    async toggleLike(item) { // item 可能是 company 或 job 物件
      if (!item || !item.id || !item.type) {
        console.error('toggleLike: 無效的項目數據或缺少 ID/類型', item);
        return;
      }

      const originalLikedStatus = item.isLiked; // 儲存原始狀態用於回滾
      const newLikedStatus = !item.isLiked;

      // 1. 樂觀更新 UI
      item.isLiked = newLikedStatus;

      // 2. 立即通知 BaseLayout 更新側邊欄和 localStorage
      if (typeof this.updateLikedItemInSidebar === 'function') {
        this.updateLikedItemInSidebar(item.originalData || item, newLikedStatus); 
      }
      // 立即透過 eventBus 通知所有頁面同步愛心狀態
      // 這行會觸發 Home.vue, SearchResult.vue, AllCompany.vue 的 handleUpdateLikeStatus
      // 以及 Company.vue 自身的 handleUpdateLikeStatus
      eventBus.emit('update-like-status', { id: item.id, type: item.type, isLiked: newLikedStatus });

      try {
        // 3. 區分呼叫 API 還是只處理前端邏輯
        if (item.type === ITEM_TYPE_JOB) {
          // 職缺：只處理前端，無需呼叫後端 API
        } else if (item.type === ITEM_TYPE_COMPANY) {
          // 公司：呼叫後端 API
          await updateLikedCompanies(item.id, newLikedStatus); // 【呼叫 updateLikedCompanies API】
        } else {
          console.warn(`toggleLike: 未知的項目類型 ${item.type}，未呼叫 API。`);
        }

      } catch (error) {
        // 4. API 失敗時的回滾邏輯 (只針對公司收藏)
        console.error(`Failed to update ${item.type} like status for ID ${item.id}:`, error);
        
        // 只有公司收藏 API 失敗時才需要回滾
        if (item.type === ITEM_TYPE_COMPANY) {
          item.isLiked = originalLikedStatus; // 回滾 Company.vue 自己的 isLiked 狀態
          alert(`收藏公司操作失敗！請稍後再試。\n錯誤訊息: ${error.message || error}`);

          // 通知 BaseLayout 回滾列表狀態
          if (typeof this.updateLikedItemInSidebar === 'function') {
            this.updateLikedItemInSidebar(item.originalData || item, originalLikedStatus); 
          }
          // 通知所有頁面回滾愛心狀態
          eventBus.emit('update-like-status', { id: item.id, type: item.type, isLiked: originalLikedStatus });
        } else {
          // 職缺：API 失敗不會發生，所以這裡理論上不會觸發。
          console.warn(`職缺收藏錯誤，但沒有 API 呼叫。可能為其他邏輯錯誤：${error.message || error}`);
        }
      }
    },
    // 處理來自 eventBus 的通用愛心狀態更新事件
    handleUpdateLikeStatus(data) { 
      const { id, type, isLiked } = data;
      // 1. 更新公司本身的愛心狀態 (如果 Company.vue 頁面顯示的就是這個公司)
      if (type === ITEM_TYPE_COMPANY && this.company && this.company.id === id) {
        this.company.isLiked = isLiked;
      } 
      // 2. 更新該公司發布的職缺的愛心狀態
      else if (type === ITEM_TYPE_JOB) {
        const jobToUpdate = this.filterJobs.find(job => job.id === id);
        if (jobToUpdate) {
          jobToUpdate.isLiked = isLiked;
        }
      }
    },
    // 【修改】handleCardClick (點擊職缺卡片)
    handleCardClick(jobData) {
      const dataForSidebar = jobData.originalData || jobData; // 確保取得原始 API 數據 (包含 type)
      
      // 1. 新增到瀏覽紀錄 (BaseLayout 的 addViewedItemToSidebar 只處理職缺)
      if (typeof this.addViewedItemToSidebar === 'function') {
        this.addViewedItemToSidebar(dataForSidebar); 
      } else {
        console.error('addViewedItemToSidebar is not available from BaseLayout');
      }

      // 2. 開啟右側邊欄
      if (typeof this.openRightSidebar === 'function') {
        this.openRightSidebar(dataForSidebar); 
      } else {
        console.error('openRightSidebar is not available from BaseLayout');
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
                                    ${avgColor} 0%,
                                    #121212 20%,
                                    #2a2a2a 100%
                                    )`;
    }
  }
})
</script>

<style scoped>
.middle-content {
  background-color: linear-gradient(to bottom, #b3b3b3 0%, #121212 20%, #121212 100%);
  border-radius: 10px 10px 0 0;
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

.project-group {
  display: inline-block;
  margin-right: 24px;
  height: 200px;
  width: auto;
  overflow: hidden;
}

.project-cover {
  height: 100%;
  display: flex;
  align-items: center;
}

.project-image {
  height: 100%;
  width: auto; /* 這才會依比例縮放 */
}

/* 選中 n-image 裡面的 img，讓它高度滿，高寬等比 */
::v-deep(.project-image img) {
  height: 100%;
  width: auto;
  display: block;
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
  backdrop-filter: blur(10px);
  /* 模糊背景效果 */
}

.modal {
  background: linear-gradient(135deg, #191414, #2a2a2a);
  border-radius: 5px;
  width: 90%;
  max-width: 500px;
  padding: 30px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  /* 投影效果 */
  position: relative;
  /* 相對定位，可用於內部絕對定位元素 */
}

.modal-header {
  margin-bottom: 30px;
  /* 底部間距 */
  text-align: center;
  /* 文字置中對齊 */
}

.modal-title {
  font-size: 18px;
  /* 文字大小 */
  font-weight: bold;
  /* 字體粗體 */
  color: #D2691E;
  /* 橘色標題 */
  margin-bottom: 10px;
  /* 標題與下方元素的間距 */
}


/* 表單區塊 */
.form-group {
  margin-bottom: 20px;
  /* 元素間的底部間距 */
}

.form-label {
  display: block;
  /* 佔滿整行 */
  margin-bottom: 8px;
  /* 與輸入欄的間距 */
  font-weight: bold;
  /* 字體粗體 */
  color: #ffffff;
  /* 白色文字 */
  font-size: 16px;
  /* 標籤字體大小 */
  text-transform: uppercase;
  /* 字母大寫 */
  letter-spacing: 1px;
  /* 字元間距 */
}

.form-input {
  width: 100%;
  /* 寬度佔滿父容器 */
  padding: 15px;
  /* 內距 */
  border: 2px solid rgba(255, 255, 255, 0.1);
  /* 淡白色邊框 */
  border-radius: 5px;
  /* 圓角 */
  background-color: rgba(255, 255, 255, 0.05);
  /* 半透明白背景 */
  color: white;
  /* 輸入文字為白色 */
  font-size: 1rem;
  /* 標準字體大小 */
  transition: all 0.3s ease;
  /* 動畫過渡效果 */
}

.form-input:focus {
  outline: none;
  /* 移除瀏覽器預設外框 */
  border-color: #D2691E;
  /* 聚焦時變成橘色邊框 */
  background-color: rgba(255, 255, 255, 0.1);
  /* 背景稍微變亮 */
}

.form-textarea {
  resize: vertical;
  /* 垂直方向可調整大小 */
  min-height: 80px;
  /* 最小高度為 80px */
  font-family: inherit;
  /* 使用繼承字體 */
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
  line-height: 47px;
  /* 水平置中 */
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
<template>
  <div class="middle-content">
    <div v-if="!ccompany || !jjobs">
      載入中...
    </div>
    <!-- 資料載入後才顯示內容 -->
    <div v-else>
      <section class="company-profile">
        <div class="profile-container">
          <div class="profile-grid">
            <div class="logo-column">
              <div class="company-logo">
                <img ref="avatar" src="/company-icon.png" alt="Company Logo" class="logo-image" />
              </div>
            </div>
            <div class="info-column">
              <div class="company-info">
                <span class="info-label">公司</span>
                <h1 class="company-name">{{ ccompany.name }}</h1>
                <p class="company-tags">{{ ccompany.bg_color_hex }}</p>
                <p class="job-count">{{ jjobs.length }}個工作機會</p>
              </div>
            </div>
          </div>
        </div>
        <div class="profile-button actions-button">
          <button type="button" class="like-btn" :class="{ active: ccompany.isLiked }"
            @click.stop="handleLikeClick('company')">
            <n-icon class="heart-icon">
              <component :is="company.isLiked ? iconHeartSolid : iconHeartRegular" />
            </n-icon>
          </button>
          <div class="ellipsis-button">
            <div class="dropdown">
              <button type="button" class="dropdown-toggle" @click="toggleDropdownProfile">
                <n-icon class="ellipsis-icon">
                  <component :is="iconEllipsisH" />
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
                  <component :is="iconCaretDown" />
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
                    <span class="industry-job">{{ ccompany?.industry }}</span>
                  </div>
                  <div class="job-specs">
                    <span class="spec">{{ formatLocation(job.location) }}</span>
                    <span class="spec">{{ job.experience_required }}</span>
                    <span class="spec">{{ job.education_required }}</span>
                    <!-- <span class="spec">{{ job.major_required }}</span> -->
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
                @click.stop="handleLikeClick(job.id)">
                <n-icon class="heart-icon">
                  <component :is="job.isLiked ? iconHeartSolid : iconHeartRegular" />
                </n-icon>
              </button>
              <button type="button" class="envelope-btn" :class="{ active: job.isLiked }"
                @click.stop="openModal(job.id)">
                <n-icon class="envelope-icon">
                  <component :is="job.isLiked ? iconEnvelopeSolid : iconEnvelopeRegular" />
                </n-icon>
              </button>

              <p class="applicants">{{ job.applicants }}</p>
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
                    <div class="label">{{ ccompany?.industry }}</div>
                    <div class="value">產業類別</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ ccompany?.industry_description }}</div>
                    <div class="value">產業描述</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ ccompany?.employees }}</div>
                    <div class="value">員工人數</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ ccompany?.capital }}</div>
                    <div class="value">資本額</div>
                  </div>
                </div>

                <div class="detail-group">
                  <div class="detail-item">
                    <div class="label">{{ ccompany?.contacts[0].name }}</div>
                    <div class="value">聯絡人</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ ccompany?.contacts[0].phone }}</div>
                    <div class="value">電話</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ ccompany?.contacts[0].fax }}</div>
                    <div class="value">傳真</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ ccompany?.contacts[0].email }}</div>
                    <div class="value">地址</div>
                  </div>
                </div>

                <div class="detail-group">
                  <div class="detail-item" v-for="(link, index) in ccompany.websites" :key="index">
                    <div class="label">{{ link.website }}</div>
                  </div>
                </div>
              </div>

              <div class="description" v-html="ccompany.introduction.replace(/\n/g, '<br><br>')"></div>
            </div>
          </div>

          <!-- 主要商品 -->
          <div class="info-card">
            <h3>主要商品</h3>
            <div class="description">
              對外：{{ ccompany?.main_product }}<br>
              <!-- 對內：{{ ccompany?.main_product }}<br><br> -->
            </div>
          </div>

          <!-- 福利制度 -->
          <div class="info-card">
            <h3>福利制度</h3>
            <div class="benefits-grid">
              <div class="benefit-tags">
                <div class="benefit-group">
                  <div class="benefit-tag" v-for="(tag, index) in ccompany.benefits[0].statutory" :key="'tag' + index">
                    {{ tag.benefit }}
                  </div>
                </div>
                <h4>法定項目</h4>

                <div class="benefit-group">
                  <div class="benefit-tag" v-for="(law, index) in ccompany.benefits[0].others" :key="'legal' + index">{{
                    law.benefit }}</div>
                </div>
                <h4>其他福利</h4>
              </div>

              <div class="description">
                <div class="content" v-html="ccompany.benefits[0].benefits_description.replace(/\n/g, '<br>')"></div>
              </div>
            </div>
          </div>

          <div class="gallery">
            <h3>企業照片</h3>
            <div class="gallery-scroll-wrapper">
              <div class="gallery-grid">
                <div class="gallery-item"><img src="/company-photo1.jpg" alt="Photo 1"></div>
                <div class="gallery-item"><img src="/company-photo2.jpg" alt="Photo 2"></div>
                <div class="gallery-item"><img src="/company-photo3.jpg" alt="Photo 3"></div>
                <div class="gallery-item"><img src="/company-photo4.jpg" alt="Photo 4"></div>
                <div class="gallery-item"><img src="/company-photo5.jpg" alt="Photo 5"></div>
              </div>
            </div>
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
                <button type="button" class="btn btn-submit" @click="handleSubmit">
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
          <div class="modal">
            <div class="modal-header">
              <h2 class="modal-title">分享這個內容</h2>
            </div>
            <div class="form-group">
              <input type="text" :value="shareLink" readonly class="share-link"></input>
            </div>
            <div class="modal-actions">
              <button type="button" class="btn btn-submit" @click="copyLink">複製連結</button>
              <button type="button" class="btn btn-cancel" @click="showShare = false">關閉</button>
            </div>
          </div>
        </div>
      </transition>

      <!-- 檢舉彈窗 -->
      <transition name="modal">
        <div v-if="showReport" class="modal-overlay" @click="showReport = false">
          <div class="modal">
            <div class="modal-header">
              <h2 class="modal-title">檢舉內容</h2>
            </div>
            <div class="form-group">
              <textarea v-model="reportReason" rows="3" class="w-full my-2"></textarea>
            </div>
            <div class="modal-actions">
              <button type="button" class="btn btn-submit" @click="submitReport">送出檢舉</button>
              <button type="button" class="btn btn-cancel" @click="showReport = false">關閉</button>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios';
import { defineComponent } from 'vue'
import { NIcon } from 'naive-ui'
import { Heart, HeartRegular, CaretDown, EllipsisH, Envelope, EnvelopeRegular } from '@vicons/fa'

export default defineComponent({
  name: 'Company',
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
      pageSize: 10,
      dropdownOpenJob: false,
      dropdownOpenProfile: false,
      profileOptions: ['分享', '檢舉'],
      showApplyModal: false,
      showShare: false,
      showReport: false,
      shareLink: 'https://example.com/share',
      reportReason: '',
      company: {
        "isLiked": false
      },
      jjobs: [],
      ccompany: null
    };
  },
  watch: {
    // 監聽 id prop 的變化，當 id 改變時重新載入公司資料
    id: {
      immediate: true, // 組件載入時立即執行一次
      handler(newId) {
        if (newId) {
          this.fetchCompanyDetails(newId);
        }
      }
    }
  },
  computed: {
    paginatedJobs() {
      return Array.isArray(this.jjobs) ? this.jjobs.slice(0, this.pageSize) : [0, 0, 0, 0, 0];
    },
    iconCaretDown() {
      return CaretDown
    },
    iconEllipsisH() {
      return EllipsisH
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
  mounted() {
    Promise.all([
      axios.get('http://127.0.0.1:8000/api/jobs/'),
      axios.get('http://127.0.0.1:8000/api/companies/'),

    ])
      .then(([jjobsRes, ccompanyRes]) => {
        this.ccompany = ccompanyRes.data[0];

        this.jjobs = jjobsRes.data;
        //console.log(this.ccompany);

        // 圖片抓色
        this.$nextTick(() => {
          const img = this.$refs.avatar;
          if (img.complete) {
            this.handleImage(img);
          } else {
            img.onload = () => {
              this.handleImage(img);
            };
          }
        });
      })
      .catch(error => {
        console.error('讀取 JSON 發生錯誤：', error);
      });
  },
  methods: {
    async fetchCompanyDetails(companyId) {
      this.isLoading = true;
      this.error = null;
      try {
        // 替換成你的實際 API 呼叫，用 companyId 去請求公司資料
        // 假設你有一個 API 函數叫 getCompanyDetails
        const response = await getCompanyDetails(companyId);
        this.companyDetails = response.data; // 根據你的 API 響應調整
      } catch (err) {
        console.error('Failed to fetch company details:', err);
        this.error = '無法載入公司詳情。';
      } finally {
        this.isLoading = false;
      }
    },


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
      const job = this.jjobs.find(i => i.id === jobId)

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
        case '忘了':
          console.log('你真的忘了喔...');
          break;
        default:
          console.warn('未知選項', option);
      }
      this.dropdownOpenProfile = false
    },
    // heart icon clicked
    handleLikeClick(Id) {
      if (Id == 'company') {
        this.handleToggleLike(this.ccompany, this.ccompany.id);
      }
      else {
        this.handleToggleLike(this.jjobs, Id);
      }
    },
    handleCardClick(job) {
      if (typeof this.addViewedItemToSidebar === 'function') {
        this.addViewedItemToSidebar(job)
      } else {
        console.error('addViewedItemToSidebar is not available from BaseLayout')
      }

      if (typeof this.openRightSidebar === 'function') {
        this.openRightSidebar(job)
      } else {
        console.error('openRightSidebar is not available from BaseLayout')
      }
    },
    handleTitleClick(job) {
      console.log('Title clicked for job:', job.title, 'Company:', job.company.name)
      alert(`Navigating to company page for: ${job.company.name}. Implement Vue Router push here.`)
    },
    //like 處理
    handleToggleLike(list, itemId) {
      var item = list// 預設company
      if (Array.isArray(list)) {// 是陣列，item is job
        item = list.find(i => i.id === itemId);
      }
      if (item) {
        item.isLiked = !item.isLiked;

        if (typeof this.updateLikedItemInSidebar === 'function') {
          this.updateLikedItemInSidebar(item, item.isLiked);
        } else {
          console.warn('updateLikedItemInSidebar is not available from BaseLayout');
        }
      } else {
        console.warn(`找不到 id 為 ${itemId} 的項目`);
      }
    },
    openModal(id) {
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
    handleSubmit() {
      // 這裡可以處理送出邏輯
      console.log('送出資料:', {
        item: this.currentItem,
        formData: this.formData,
        files: this.selectedFiles
      });

      // 顯示成功訊息（可選）
      alert('資料已送出！');

      // 關閉彈窗
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
                                    ${avgColor} 0%,
                                    #121212 20%,
                                    #121212 100%
                                    )`;
    }
  }
})
</script>

<style scoped>
.middle-content {
  background-color: #121212;
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

/* 合并的 JobCard 样式 */
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

.benefits-section {
  background: rgba(255, 255, 255, 0.1);
  margin: 30px 40px;
  padding: 24px;
  border-radius: 10px;
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

.benefits-description {
  grid-column: span 2;
  margin-top: 30px;
}

.benefits-description h4 {
  font-size: 14px;
  color: #b3b3b3;
  margin-bottom: 10px;
}

.benefits-description .content {
  color: #b3b3b3;
  line-height: 1.6;
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
  height: 100%;
  max-height: 200px;
  width: auto;
  object-fit: contain;
  display: block;
}

/* Modal 樣式 */
.modal-overlay {
  position: fixed;
  /* 固定定位，覆蓋整個視窗 */
  top: 0;
  /* 從畫面最上方開始 */
  left: 0;
  /* 從畫面最左側開始 */
  width: 100%;
  /* 寬度為整個視窗寬 */
  height: 100%;
  /* 高度為整個視窗高 */
  background-color: rgba(0, 0, 0, 0.8);
  /* 背景為半透明黑色 */
  display: flex;
  /* 使用 Flex 排版，置中內容 */
  justify-content: center;
  /* 水平置中 */
  align-items: center;
  /* 垂直置中 */
  z-index: 1000;
  /* 疊層順序，確保在最上層 */
  backdrop-filter: blur(10px);
  /* 模糊背景效果 */
}

.modal {
  background: linear-gradient(135deg, #191414, #2a2a2a);
  /* 漸層背景 */
  border-radius: 5px;
  /* 圓角邊框 */
  width: 90%;
  /* 寬度為螢幕的 90% */
  max-width: 500px;
  /* 最大寬度限制為 500px */
  padding: 30px;
  /* 內距為 30px */
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

.file-upload-container {
  position: relative;
  margin-bottom: 30px;
}

.file-upload-btn {
  width: 100%;
  padding: 15px;
  border: 2px dashed #D2691E;
  border-radius: 10px;
  background-color: rgba(244, 188, 103, 0.1);
  color: #D2691E;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  font-weight: 600;
}

.file-upload-btn:hover {
  border-color: #D2691E;
  background-color: rgba(244, 188, 103, 0.4);
}

.file-input {
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
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
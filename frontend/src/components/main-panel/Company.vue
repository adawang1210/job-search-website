<template>
  <div class="middle-content">
    <div v-if="!company || !jobs">
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
                <h1 class="company-name">{{ company.title }}</h1>
                <p class="company-tags">{{ company.profile_tags }}</p>
                <p class="job-count">26個工作機會</p>
              </div>
            </div>
          </div>
        </div>
        <div class="profile-button">
          <button type="button" class="like-btn" :class="{ active: company.isLiked }"
            @click.stop="handleCompanyLikeClick">
            <n-icon class="heart-icon">
              <component :is="iconHeart()" />
            </n-icon>
          </button>
          <div class="ellipsis-button">
            <div class="dropdown">
              <button type="button" class="ellipsis-btn" @click="toggleDropdownProfile">
                <n-icon class="ellipsis-icon">
                  <component :is="iconEllipsisH" />
                </n-icon>
              </button>

              <ul v-show="dropdownOpenProfile" class="dropdown-menu">
                <li @click="selectPageSize(5)">5 筆</li>
                <li @click="selectPageSize(10)">10 筆</li>
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

              <ul v-show="dropdownOpenJob" class="dropdown-menu">
                <li @click="selectPageSize(5)">5 筆</li>
                <li @click="selectPageSize(10)">10 筆</li>
              </ul>
            </div>
          </div>
        </div>
        <!-- JobCard -->
        <article 
          v-for="(job, jobIndex) in paginatedJobs" 
          :key="job.id || jobIndex"
          class="job-card" 
          @click="handleCardClick(job)"
        >
          <div class="job-content">
            <div class="main-info">
              <div class="header">
                <time class="date">{{ job.date }}</time>
                <h3 class="title" @click.stop="handleTitleClick(job)">{{ job.title }}</h3>
              </div>
              <div class="details">
                <div class="company-info-job">
                  <span class="company-name-job">{{ job.company }}</span>
                  <span class="industry-job">{{ job.industry }}</span>
                </div>
                <div class="job-specs">
                  <span class="spec">{{ job.location }}</span>
                  <span class="spec">{{ job.experience }}</span>
                  <span class="spec">{{ job.education }}</span>
                  <span class="spec">{{ job.salary }}</span>
                </div>
                <div class="benefits">
                  <span v-for="(benefit, index) in job.benefits" :key="index" class="benefit-tag-job">
                    {{ benefit }}
                  </span>
                </div>
              </div>
            </div>
            <div class="actions">
              <button type="button" class="like-btn-job" :class="{ active: job.isLiked }" @click.stop="handleJobLikeClick(job.id)">
                <n-icon class="heart-icon">
                  <component :is="job.isLiked ? iconHeartSolid : iconHeartRegular" />
                </n-icon>
              </button>
              <button type="button" class="envelope-btn" :class="{ active: job.isLiked }" @click.stop="handleJobLikeClick(job.id)">
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
                    <div class="label">{{ company?.industry.category }}</div>
                    <div class="value">產業類別</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ company?.industry.description }}</div>
                    <div class="value">產業描述</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ company?.industry.employees }}</div>
                    <div class="value">員工人數</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ company?.industry.capital }}</div>
                    <div class="value">資本額</div>
                  </div>
                </div>

                <div class="detail-group">
                  <div class="detail-item">
                    <div class="label">{{ company?.contact.person }}</div>
                    <div class="value">聯絡人</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ company?.contact.phone }}</div>
                    <div class="value">電話</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ company?.contact.fax }}</div>
                    <div class="value">傳真</div>
                  </div>
                  <div class="detail-item">
                    <div class="label">{{ company?.contact.address }}</div>
                    <div class="value">地址</div>
                  </div>
                </div>

                <div class="detail-group">
                  <div class="detail-item" v-for="(link, index) in company.links" :key="index">
                    <div class="label">{{ link }}</div>
                  </div>
                </div>
              </div>

              <div class="description" v-html="company.description.replace(/\n/g, '<br><br>')"></div>
            </div>
          </div>

          <!-- 主要商品 -->
          <div class="info-card">
            <h3>主要商品</h3>
            <div class="description">
              對外：{{ company?.products.external }}<br>
              對內：{{ company?.products.internal }}<br><br>
              {{ company?.products.note }}
            </div>
          </div>

          <!-- 福利制度 -->
          <div class="info-card">
            <h3>福利制度</h3>
            <div class="benefits-grid">
              <div class="benefit-tags">
                <div class="benefit-group">
                  <div class="benefit-tag" v-for="(tag, index) in company.benefits.tags"
                    :key="'tag' + index">{{ tag }}
                  </div>
                </div>

                <h4>法定項目</h4>
                <div class="benefit-group">
                  <div class="benefit-tag" v-for="(law, index) in company.benefits.legal"
                    :key="'legal' + index">{{ law
                    }}</div>
                </div>

                <h4>其他福利</h4>
              </div>

              <div class="description">
                <div class="content" v-html="company.benefits.description.replace(/\n/g, '<br>')"></div>
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
  data() {
    return {
      pageSize: 5,
      dropdownOpenJob: false,
      dropdownOpenProfile: false,
      jobs: [],
      company: null
    };
  },
  computed: {
    paginatedJobs() {
      return Array.isArray(this.jobs) ? this.jobs.slice(0, this.pageSize): [0,0,0,0,0];
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
      axios.get('/company.json'),
      axios.get('/jobs.json')  // 第二個 JSON
    ])
    .then(([companyRes, jobsRes]) => {
      this.company = companyRes.data.companys[0];
      this.jobs = jobsRes.data.jobs;

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
    iconHeart() {
      return this.company.isLiked ? Heart : HeartRegular
    },
    toggleDropdownJob() {
      this.dropdownOpenJob = !this.dropdownOpenJob
    },
    toggleDropdownProfile() {
    this.dropdownOpenProfile = !this.dropdownOpenProfile;
  },
    selectPageSize(size) {
      this.pageSize = size
      this.dropdownOpen = false
    },
    handleCompanyLikeClick() {
      const list = this.company?.companys;
      const itemId = list[0].id;

      if (list && itemId) {
        this.handleToggleLike(list, itemId);
      } else {
        console.log('無法取得公司資料或 ID');
      }
    },
    // 合并的 JobCard 方法
    handleJobLikeClick(jobId) {
      this.handleToggleLike(this.jobs, jobId);
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
      console.log('Title clicked for job:', job.title, 'Company:', job.company)
      alert(`Navigating to company page for: ${job.company}. Implement Vue Router push here.`)
    },
    handleToggleLike(list, itemId) {
      const item = list.find(i => i.id === itemId);
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

.like-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: white; /* 空心愛心預設白色 */
  font-size: 18px;
  padding: 3px;
  transition: transform 0.5s ease, color 0.3s ease;
}

.like-btn:hover {
  transform: scale(1.1);
}

.like-btn.active {
  color: rgb(235, 178, 189); /* 喜歡後變成粉色實心 */
}

.ellipsis-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: white; /* 空心愛心預設白色 */
  font-size: 18px;
  padding: 3px;
  transition: transform 0.5s ease, color 0.3s ease;
}

.ellipsis-btn:hover {
  transform: scale(1.1);
}

/* company profile */
.company-profile {
  display: flex;
  width: 100%;
  flex-direction: column;
  padding: 40px 36px 28px 28px;
  overflow: hidden;
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
  margin: 80px 0 30px;
}

/* job listings */
.job-listings {
  margin: 0;
  padding: 28px;
  background: transparent;
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
  width: 84%;
}

.header {
  display: flex;
  align-items: center;
  gap: 23px;
  font-family: Roboto, -apple-system, Roboto, Helvetica, sans-serif;
}

.date {
  color: #b3b3b3;
  font-size: 16px;
  font-weight: 400;
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
  margin-top: 8px;
  padding-left: 63px;
}

.company-info-job {
  display: flex;
  align-items: center;
  gap: 32px;
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
  margin-top: 16px;
  align-items: center;
  gap: 32px;
  font-family: Noto Sans, -apple-system, Roboto, Helvetica, sans-serif;
  color: #f5f5f5;
  font-size: 16px;
  font-weight: 600;
}

.benefits {
  display: flex;
  margin-top: 10px;
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

.actions {
  width: 16%;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
}

.like-btn-job {
  background: none;
  border: none;
  cursor: pointer;
  color: white;
  font-size: 18px;
  padding: 3px;
  transition: transform 0.5s ease, color 0.3s ease;
}

.like-btn-job:hover {
  transform: scale(1.1);
}

.like-btn-job.active {
  color: rgb(235, 178, 189);
}

.envelope-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: white;
  font-size: 18px;
  padding: 3px;
  transition: transform 0.5s ease, color 0.3s ease;
}

.envelope-btn:hover {
  transform: scale(1.1);
}

.applicants {
  color: #f5f5f5;
  font-size: 16px;
  font-family: Noto Sans, -apple-system, Roboto, Helvetica, sans-serif;
  font-weight: 500;
  text-align: right;
  margin: 6px 0 0;
}

/* dropdown styles */
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

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-menu {
  list-style: none;
  margin: 0;
  padding: 0;
  background-color: rgba(0, 0, 0, 0.6);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  position: absolute;
  top: 100%;
  right: 0;
  z-index: 1000;
  min-width: 120px;
  max-width: 10vw;
}

.dropdown-menu li {
  padding: 8px 12px;
  cursor: pointer;
  white-space: nowrap;
}

.dropdown-menu li:hover {
  background-color: #f0f0f0;
}

/*company information*/
.company-information {
  margin: 0;
  padding: 28px;
  background: transparent;
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

</style>
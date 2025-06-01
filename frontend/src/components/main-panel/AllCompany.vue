<template>
  <div class="all-companies-container">
    <div v-if="isLoadingCompanies" class="loading-message">
      正在載入優質企業...
    </div>
    <div v-else-if="errorCompanies" class="error-message">
      {{ errorCompanies }}
    </div>
    <div v-else>
      <div v-if="companies.length > 0">
        <div class="company-grid">
          <div class="company-card" v-for="(company, cIndex) in companies" :key="'company-' + cIndex"
            @click="handleCompanyCardClick(company)">
            <div class="card-image-container">
              <div class="company-image" :style="{ backgroundImage: 'url(' + company.image + ')' }"></div>
              <div class="play-button">
                <n-icon size="30">
                  <play-circle-outline />
                </n-icon>
              </div>
            </div>
            <div class="card-content">
              <h3 class="company-name">{{ company.name }}</h3>
              <p class="company-description">{{ company.industry }}</p>
              <div class="company-stats">
                <span class="employee-count">{{ formatEmployeeCount(company.employees) }}人</span>
                <span class="capital">資本額 {{ formatCapital(company.capital) }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="all-companies-button">
          <span class="view-all-text">看全部</span>
        </div>

        <div class="carousel-section">
          <n-carousel
            effect="card"
            prev-slide-style="transform: translateX(-150%) translateZ(-800px);"
            next-slide-style="transform: translateX(50%) translateZ(-800px);"
            style="height: 240px"
            :show-dots="false"
          >
            <n-carousel-item v-for="(photo, index) in carouselPhotos" :key="index" :style="{ width: '60%' }">
              <img
                class="carousel-img"
                :src="photo.url"
                :alt="'Carousel image ' + (index + 1)"
              >
            </n-carousel-item>
          </n-carousel>
        </div>
      </div>
      <div v-else class="no-data-message">
        目前沒有優質企業資料。
      </div>
    </div>
  </div>
</template>

<script>
import { getGreatCompanies} from '@/api/home.js';
import { PlayCircleOutline } from '@vicons/ionicons5';
import { NCarousel, NCarouselItem } from 'naive-ui';
import eventBus from '/src/eventBus.js';

const ITEM_TYPE_COMPANY = 'company';

export default {
  name: 'AllCompany',
  inject: ['updateLikedItemInSidebar'],
  components: {
    PlayCircleOutline,
    NCarousel,
    NCarouselItem
  },
  data() {
    return {
      companies: [],
      likedCompanies: [],
      isLoadingCompanies: false,
      errorCompanies: null,
      carouselPhotos: [
        { url: 'https://images.1111.com.tw/aidma/zone/newhome2023_banner_228_3957267719.jpg' },
        { url: 'https://images.1111.com.tw/aidma/zone/newhome2023_banner_234_3956376983.jpg' },
        { url: 'https://images.1111.com.tw/aidma/zone/newhome2023_banner_226_3954569761.jpg' },
        { url: 'https://images.1111.com.tw/aidma/zone/newhome2023_banner_238_3956376456.jpg' }
      ]
    };
  },
  components: {
    PlayCircleOutline,
    NCarousel,
    NCarouselItem
  },
  async mounted() {
    await Promise.all([
      this.loadCompaniesData()
    ]);
    
    // 監聽來自 BaseLayout 或其他頁面的愛心狀態更新事件
    eventBus.on('update-like-status', this.handleUpdateLikeStatus);
  },
  beforeUnmount() {
    // 在組件銷毀前移除事件監聽器
    eventBus.off('update-like-status', this.handleUpdateLikeStatus);
  },
  methods: {
    formatEmployeeCount(count) {
      return count ? count.toLocaleString() : '未提供';
    },
    formatCapital(capital) {
      if (!capital) return '未提供';
      return (capital / 10000000).toFixed(1) + '億';
    },
    async loadCompaniesData() {
      this.isLoadingCompanies = true;
      this.errorCompanies = null;
      try {
        const companiesData = await getGreatCompanies();
        const rawCompanies = companiesData.results || companiesData || [];
        
        this.companies = rawCompanies.map(company => ({
          id: company.id,
          name: company.name,
          image: company.media?.logo || 'default_company_logo_path.png',
          industry: company.industry || '未提供',
          industry_description: company.industry_description || '',
          employees: company.employees,
          capital: company.capital,
          isLiked: company.is_liked_by_user || false,
          originalData: { ...company, type: ITEM_TYPE_COMPANY },
          type: ITEM_TYPE_COMPANY
        }));
      } catch (error) {
        console.error('Error fetching companies:', error);
        if (error.message && error.message.toLowerCase().includes('network error')) {
          this.errorCompanies = '無法載入企業資訊，請檢查網路連線。';
        } else {
          this.errorCompanies = '載入企業資訊失敗，請稍後再試。';
        }
      } finally {
        this.isLoadingCompanies = false;
      }
    },
    async toggleLike(company) {
      if (!company || !company.id || company.type !== ITEM_TYPE_COMPANY) {
        console.error('toggleLike: 無效的公司數據或類型不符', company);
        return;
      }

      const originalLikedStatus = company.isLiked;
      const newLikedStatus = !company.isLiked;

      // 1. 樂觀更新 UI
      company.isLiked = newLikedStatus;

      try {
        // 2. 呼叫後端 API
        if (newLikedStatus) {
          await likeJob(company.id); 
        } else {
          await unlikeJob(company.id);
        }

        // 3. 通知 BaseLayout 更新側邊欄
        if (typeof this.updateLikedItemInSidebar === 'function') {
          this.updateLikedItemInSidebar(company.originalData || company, newLikedStatus); 
        }
        
        // 4. 通知其他組件更新 UI
        eventBus.emit('update-like-status', {
          id: company.id,
          type: company.type,
          isLiked: newLikedStatus
        });

      } catch (error) {
        console.error(`Failed to update company like status for ID ${company.id}:`, error);
        company.isLiked = originalLikedStatus;
        alert(`收藏公司操作失敗，請稍後再試。`);

        if (typeof this.updateLikedItemInSidebar === 'function') {
          this.updateLikedItemInSidebar(company.originalData || company, originalLikedStatus);
        }
        eventBus.emit('update-like-status', {
          id: company.id,
          type: company.type,
          isLiked: originalLikedStatus
        });
      }
    },
    handleUpdateLikeStatus(data) {
      const { id, type, isLiked } = data;
      if (type === ITEM_TYPE_COMPANY) {
        const companyToUpdate = this.companies.find(company => company.id === id);
        if (companyToUpdate) {
          companyToUpdate.isLiked = isLiked;
        }
      }
    },
    handleCompanyCardClick(company) {
      this.$router.push(`/company/${company.id}`);
    }
  }
};
</script>

<style scoped>

/* AllCompany.vue 的樣式修改 */
.all-companies-container {
  display: flex;
  flex-direction: column;
  padding: 20px;
  background-color: #2a2a2a;
  /* 深灰色背景 */
  color: white;
  min-height: 100vh;
  /* 確保內容撐開整個頁面 */
  box-sizing: border-box;
  /* ==== 新增這四行，讓它有圓角效果 ==== */
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
  /* ================================== */
}

.company-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 24px;
  padding: 20px;
}

.company-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 16px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.company-card:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-4px);
}

.card-image-container {
  position: relative;
  width: 100%;
  padding-bottom: 100%;
  margin-bottom: 16px;
  border-radius: 4px;
  overflow: hidden;
}

.company-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.play-button {
  position: absolute;
  right: 8px;
  bottom: 8px;
  width: 48px;
  height: 48px;
  background: #1DB954;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: translateY(8px);
  transition: all 0.3s ease;
}

.company-card:hover .play-button {
  opacity: 1;
  transform: translateY(0);
}

.play-button :deep(.n-icon) {
  color: white;
}

.card-content {
  padding: 12px 8px;
}

.company-name {
  color: white;
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  letter-spacing: 0.5px;
}

.company-info {
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  font-weight: 500;
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.company-description {
  color: rgba(255, 255, 255, 0.7);
  font-size: 13px;
  margin: 0 0 8px 0;
  margin-top: -10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.company-stats {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

.employee-count, .capital {
  background: rgba(255, 255, 255, 0.1);
  padding: 4px 8px;
  border-radius: 4px;
}

/* 消息提示樣式 */
.loading-message,
.error-message,
.no-data-message {
  padding: 20px;
  text-align: center;
  color: #ccc;
  width: 100%;
  box-sizing: border-box;
  margin-top: 20px;
}

.error-message {
  color: #ffffff;
  background-color: rgba(128, 128, 128, 0.1);
  border: 1px solid rgba(211, 211, 211, 0.3);
  border-radius: 5px;
  margin: 20px auto;
  /* 居中顯示 */
  max-width: 600px;
  /* 限制寬度 */
}

.loading-message {
  font-style: italic;
}

.all-companies-button {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  padding: 8px 0;
  margin: 20px auto;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 150px;
}

.all-companies-button:hover {
  background: rgba(255, 255, 255, 0.2);
}

.view-all-text {
  color: rgba(255, 255, 255, 0.8);
  font-size: 13px;
  font-weight: 600;  /* 增加文字粗細 */
  letter-spacing: 1px;  /* 增加字間距 */
}

.carousel-section {
  margin-top: 40px;
  padding: 0 20px;
}

.carousel-img {
  margin: 0 auto;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.job-card-details {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  width: 100%;
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
</style>
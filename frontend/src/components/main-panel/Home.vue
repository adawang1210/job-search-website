<template>
  <div class="middle-content">
    <section class="recommend" v-for="(section, index) in sections" :key="index">
      <h1>{{ section.title }}</h1>
      <div class="recommend-content" @mousedown="startDrag" @mousemove="onDrag" @mouseup="stopDrag"
        @mouseleave="stopDrag" :class="{ active: isDragging }">
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
    </section>

    <section class="great-company">
      <h1>優質企業</h1>
      <div class="recommend-content" @mousedown="startDrag" @mousemove="onDrag" @mouseup="stopDrag"
        @mouseleave="stopDrag" :class="{ active: isDragging }">
        <div class="content-wrapper"
             v-for="(company, cIndex) in companies"
             :key="'company-' + cIndex"
             @click="handleCompanyCardClick(company)">
          <div class="company-icon" :style="{ backgroundImage: 'url(' + company.image + ')' }" @click.stop></div>
          <p class="company-name" @click.stop>{{ company.name }}</p>
        </div>
      </div>
    </section>

    <section class="favorite-job">
      <div class="content-container" 
           v-for="(favJob, fIndex) in favoriteJobs"
           :key="'job-' + fIndex"
           :style="{ backgroundImage: 'url(' + favJob.image + ')' }"
           @click="handleFavoriteJobCardClick(favJob)"> <div class="favorite-icon" :style="{ backgroundImage: 'url(' + favJob.icon + ')' }" @click.stop></div>
        <p class="favorite-name" @click.stop>{{ favJob.name }}</p>
      </div>
    </section>
  </div>
</template>


<script>

import eventBus from '/src/eventBus.js';

export default {
  name: 'MainPanel',
  inject: ['openRightSidebar', 'updateLikedItemInSidebar', 'addViewedItemToSidebar'], // 注入來自 BaseLayout 的方法
  data() {
    return {
      isDragging: false, // 控制滑動時的狀態
      startX: 0, // 滑動起點 X 座標
      scrollLeft: 0, // 滑動前的 scrollLeft 值

      // 各種職缺區塊
      sections: [
        {
          title: '為你推薦',
          jobs: [
            { 
              id: 'job-rec-1',
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false,
              image: '/摩斯漢堡.jfif'
            },
            {
              id: 'job-rec-2',
              title: '前端工程師',
              location: '台北市內湖區',
              salary: '月薪60,000元以上',
              company: '科技先鋒公司',
              isLiked: false,
              image: '/摩斯漢堡.jfif'
            },
            {
              id: 'job-rec-3',
              title: '行政專員',
              location: '桃園市中壢區',
              salary: '月薪33,000元以上',
              company: '國立中央大學',
              isLiked: false,
              image: '/摩斯漢堡.jfif'
            },
            {
              id: 'job-rec-4',
              title: '行銷企劃人員',
              location: '台北市信義區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false,
              image: '/摩斯漢堡.jfif'
            },
            {
              id: 'job-rec-5',
              title: '銷售員',
              location: '台北市大安區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false,
              image: '/摩斯漢堡.jfif'
            }
          ]
        },
        {
          title: '熱門職缺',
          jobs: [
            { id: 'job-hot-1',
              title: '行銷專員',
              location: '台中市西屯區',
              salary: '月薪40,000元以上',
              company: '創意行銷社',
              isLiked: false,
              image: '/摩斯漢堡.jfif'
            },
            {
              id: 'job-hot-2',
              title: '廚師助理',
              location: '桃園市中壢區',
              salary: '月薪33,000元以上',
              company: '鼎泰豐',
              isLiked: false,
              image: '/摩斯漢堡.jfif'
            },
            {
              id: 'job-hot-3',
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false,
              image: '/摩斯漢堡.jfif'
            },
            {
              id: 'job-hot-4',
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false,
              image: '/摩斯漢堡.jfif'
            },
            {
              id: 'job-hot-5',
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false,
              image: '/摩斯漢堡.jfif'
            }
          ]
        },
        {
          title: '最新職缺',
          jobs: [
            {
              id: 'job-new-1',
              title: '調酒師',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false,
              image: '/摩斯漢堡.jfif'
            },
            {
              id: 'job-new-2',
              title: '燈具銷售員',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false,
              image: '/摩斯漢堡.jfif'
            },
            {
              id: 'job-new-3',
              title: '行政櫃台人員',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false,
              image: '/摩斯漢堡.jfif'
            },
            {
              id: 'job-new-4',
              title: '美髮助理',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false,
              image: '/摩斯漢堡.jfif'
            },
            {
              id: 'job-new-5',
              title: '社群小編',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false,
              image: '/摩斯漢堡.jfif'
            }
          ]
        }
      ],

      // 優質企業資料
      companies: [
        { name: 'Advantech_研華股份有限公司', image: '/研華科技.jpg' },
        { name: 'Advantech_研華股份有限公司', image: '/研華科技.jpg' },
        { name: 'Advantech_研華股份有限公司', image: '/研華科技.jpg' },
        { name: 'Advantech_研華股份有限公司', image: '/研華科技.jpg' },
        { name: 'Advantech_研華股份有限公司', image: '/研華科技.jpg' },
        { name: 'Advantech_研華股份有限公司', image: '/研華科技.jpg' }
      ],

      // 最愛職缺
      favoriteJobs: [
        { name: '最愛牙醫師', image: '/最愛牙醫師.jpg', icon: '/牙醫logo.jpg' },
        { name: '最愛牙醫師', image: '/最愛牙醫師.jpg', icon: '/牙醫logo.jpg' },
        { name: '最愛牙醫師', image: '/最愛牙醫師.jpg', icon: '/牙醫logo.jpg' },
        { name: '最愛牙醫師', image: '/最愛牙醫師.jpg', icon: '/牙醫logo.jpg' },
        { name: '最愛牙醫師', image: '/最愛牙醫師.jpg', icon: '/牙醫logo.jpg' },
        { name: '最愛牙醫師', image: '/最愛牙醫師.jpg', icon: '/牙醫logo.jpg' }
      ]
    }
  },
  mounted() {
    eventBus.on('unlike-item-in-home-via-sidebar', this.handleUnlikeFromSidebar);
    // ADDED: Listen for like event from LeftSidebar's viewed items
    eventBus.on('like-item-in-home-via-sidebar', this.handleLikeFromSidebar);
  },
  beforeUnmount() {
    eventBus.off('unlike-item-in-home-via-sidebar', this.handleUnlikeFromSidebar);
    // ADDED: Remove listener
    eventBus.off('like-item-in-home-via-sidebar', this.handleLikeFromSidebar);
  },
  methods: {
    // 切換喜歡與否的狀態
    toggleLike(sectionTitle, jobIndex) {
      const section = this.sections.find(s => s.title === sectionTitle);
      if (section) {
        const job = section.jobs[jobIndex];
        job.isLiked = !job.isLiked;
        // 調用從 BaseLayout 注入的方法來更新側邊欄的喜歡項目
        if (typeof this.updateLikedItemInSidebar === 'function') {
          this.updateLikedItemInSidebar(job, job.isLiked);
        } else {
          console.error('updateLikedItemInSidebar is not available from BaseLayout');
        }
      }
    },
    // 新增方法：處理從 LeftSidebar (通過事件總線) 發來的取消收藏事件
    handleUnlikeFromSidebar(itemId) {
      let jobFound = false;
      for (const section of this.sections) {
        const job = section.jobs.find(j => j.id === itemId);
        if (job) {
          job.isLiked = false; // 更新 Home 中的職缺狀態
          jobFound = true;
          // Note: updateLikedItemInSidebar is not called here again,
          // as BaseLayout already handled the list update.
          // This is purely for UI sync in Home.vue.
          break;
        }
      }
      if (!jobFound) {
        console.warn(`Job with id ${itemId} not found in Home.vue sections to unlike.`);
      }
    },

    // ADDED: New method to handle liking from LeftSidebar's viewed items
    handleLikeFromSidebar(itemId) {
      let jobFound = false;
      for (const section of this.sections) {
        const job = section.jobs.find(j => j.id === itemId);
        if (job) {
          if (!job.isLiked) { // Only proceed if it's not already liked in Home's state
            job.isLiked = true;
            // Call the injected method to update BaseLayout's state
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

    // 滑動開始
    startDrag(e) {
      this.isDragging = true;
      this.startX = e.pageX - e.currentTarget.offsetLeft;
      this.scrollLeft = e.currentTarget.scrollLeft;
    },
    // 滑動中
    onDrag(e) {
      if (!this.isDragging) return;
      e.preventDefault();
      const x = e.pageX - e.currentTarget.offsetLeft;
      const walk = (x - this.startX) * 2;
      e.currentTarget.scrollLeft = this.scrollLeft - walk;
    },
    // 滑動結束
    stopDrag() {
      this.isDragging = false;
    },
    // RENAMED and MODIFIED: from handleCardBackgroundClick to handleCardClick
    // This method is now called when the card itself (not just background) is clicked.
    // The like button has .stop modifier, so its click won't bubble here.
    handleCardClick(jobData) {
      // Add to viewed items list via BaseLayout
      if (typeof this.addViewedItemToSidebar === 'function') {
        this.addViewedItemToSidebar(jobData);
      } else {
        console.error('addViewedItemToSidebar is not available from BaseLayout');
      }

      // Open right sidebar (existing functionality)
      if (typeof this.openRightSidebar === 'function') {
        this.openRightSidebar(jobData);
      } else {
        console.error('openRightSidebar is not available from BaseLayout');
      }
    },

    handleTitleClick(job) {
      console.log('Title clicked for job:', job.title, 'Company:', job.company);
      alert(`Navigating to company page for: ${job.company}. Implement Vue Router push here.`);
      // Potentially also add to viewed items if title click implies viewing content
      // if (typeof this.addViewedItemToSidebar === 'function') {
      //   this.addViewedItemToSidebar(job);
      // }
    },
    
    handleCompanyCardClick(company) {
      console.log('Company card clicked:', company);
      // If company cards should also be added to a "viewed companies" list or similar,
      // you would implement that logic here or by calling a relevant provided function.
      // For now, it doesn't add to the job viewed list.
      // Example: this.openRightSidebar({ ...company, type: 'company' });
    },
    handleFavoriteJobCardClick(favJob) {
      console.log('Favorite job card clicked:', favJob);
      // Similar to company cards, if these have a detail view and should be "viewed"
      // Example: this.addViewedItemToSidebar({ ...favJob, type: 'favoriteJobDetails' });
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
  gap: 6px; /* 卡片與下方公司名稱的間距，可酌情調整 */
}


/* 職缺卡片本體樣式 */
.card {
  display: flex;
  flex-direction: row;
  align-items: center;
  background-color: #594f4f;
  border-radius: 10px; /* 調整圓角以匹配新尺寸 */
  padding: 8px 8px 8px 12px; /* MODIFIED: 稍微減少 padding */
  width: 240px; /* MODIFIED: 將寬度從 300px 改為 240px */
  box-sizing: border-box;
  transition: box-shadow 0.25s ease-out, transform 0.25s ease-out; /* 保持 hover 效果的 transition */
}

/* 橫向滑動內容區塊樣式 */
.middle-content .recommend-content,
.middle-content .great-company .recommend-content {
  display: flex;
  flex-direction: row;
  gap: 20px; /* MODIFIED: 如果卡片變小，可以稍微減少卡片間的間距 */
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
  display: flex; /* MODIFIED: 改為 flex 佈局更好控制內部 */
  flex-direction: column; /* MODIFIED: 讓內部元素垂直排列 */
  justify-content: center; /* MODIFIED: 垂直居中內容 (可選) */
  /* width: 200px; */ /* MODIFIED: 移除固定寬度，讓 flex-grow 生效 */
  background-color: #594f4f; /* 與 card 背景色相同，通常不需要單獨設定 */
  /* border-radius: 5px; */ /* 如果 card 有圓角，這裡通常不需要 */
  box-sizing: border-box;
  flex-grow: 1; /* 填充 card 內剩餘空間 */
  margin-left: 8px; /* MODIFIED: 新增圖片和文字容器之間的間距 */
}

/* 職缺圖片 */
.middle-content .recommend .job-image {
  width: 64px; /* MODIFIED: 從 80px 調整為 64px */
  height: 64px; /* MODIFIED: 從 80px 調整為 64px */
  border-radius: 6px; /* MODIFIED: 調整圓角 */
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
  display: inline-block; /* 修改點：讓元素寬度自適應內容 */
  align-self: flex-start;
  max-width: 100%;      /* 新增：確保在內容過長時，仍能配合 overflow 和 ellipsis */
  font-size: 14px;
  margin: 0 0 4px 0;
  font-weight: bold;
  white-space: nowrap; /* 保持不換行 */
  overflow: hidden;    /* 超出部分隱藏 */
  text-overflow: ellipsis; /* 超出部分顯示省略號 */
  cursor: pointer;
}

.middle-content .recommend .content-container .title:hover,
.middle-content .recommend .company-name:hover {
  text-decoration: underline; /* Underline on hover */
  cursor: pointer;
}

/* 優質企業圖示樣式 */
.middle-content .recommend .content-container .info {
  font-size: 12px; /* MODIFIED: 從 14px 調整為 12px */
  margin: 0 0 2px 0; /* MODIFIED: 調整 margin */
  color: #f4f4f4;
  white-space: nowrap; /* 確保不換行 */
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 公司名稱樣式 */
.middle-content .recommend .content-container .salary-and-like {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0; /* MODIFIED: 移除底部 margin，因為 content-container 會處理間距 */
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
  font-size: 14px; /* MODIFIED: 從 16px 調整為 14px，如果需要 */
  font-weight: bold;
  color: white;
  margin-top: 6px; /* 保持與上方卡片的間距 */
  text-align: center; /* 如果希望公司名稱在卡片下方居中對齊 */
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  width: 240px; /* MODIFIED: 讓公司名稱的寬度與卡片寬度一致，以便正確的 text-align: center */
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
  width: 64px;
  height: 64px;
  border-radius: 5px;
  background-color: #ffffff;
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
  color: white; /* 空心愛心預設白色 */
  font-size: 18px; /* MODIFIED: 從 20px 調整為 18px */
  padding: 3px; /* MODIFIED: 稍微減少 padding */
  transition: transform 0.5s ease;
}

.middle-content .recommend .content-container .like-btn:hover {
  transform: scale(1.1);
}

.like-btn.active {
  color: rgb(235, 178, 189); /* 喜歡後變成粉色實心 */
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
  transform: scale(1.03); /* 可以保持或微調 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); /* MODIFIED: 陰影也可以微調以適應新尺寸 */
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

</style>
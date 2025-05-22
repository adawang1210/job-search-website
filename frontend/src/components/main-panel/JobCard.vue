<template>
  <article class="job-card " @click="handleCardClick(job)">
    <div class="job-content">
      <div class="main-info">
        <div class="header">
          <time class="date">{{ job.date }}</time>
          <h3 class="title" @click.stop="handleTitleClick(job)">{{ job.title }}</h3>
        </div>
        <div class="details">
          <div class="company-info">
            <span class="company-name">{{ job.company }}</span>
            <span class="industry">{{ job.industry }}</span>
          </div>
          <div class="job-specs">
            <span class="spec">{{ job.location }}</span>
            <span class="spec">{{ job.experience }}</span>
            <span class="spec">{{ job.education }}</span>
            <span class="spec">{{ job.salary }}</span>
          </div>
          <div class="benefits">
            <span v-for="(benefit, index) in job.benefits" :key="index" class="benefit-tag">
              {{ benefit }}
            </span>
          </div>
        </div>
      </div>
      <div class="actions">
        <button type="button" class="like-btn" :class="{ active: job.isLiked }" @click.stop="handleLikeClick">
          <n-icon class="heart-icon">
            <component :is="iconHeart" />
          </n-icon>
        </button>
        <button type="button" class="envelope-btn" :class="{ active: job.isLiked }" @click.stop="handleLikeClick">
          <n-icon class="envelope-icon">
            <component :is="iconEnvelope" />
          </n-icon>
        </button>

        <p class="applicants">{{ job.applicants }}</p>
      </div>
    </div>
  </article>
</template>
  
  <script>
  import { defineComponent } from 'vue'
import { NIcon } from 'naive-ui'
import { Heart, HeartRegular, Envelope, EnvelopeRegular } from '@vicons/fa'

  export default defineComponent({
  name: 'JobCard',
  inject: ['openRightSidebar', 'addViewedItemToSidebar'], // 注入 BaseLayout 的方法
  components: {
    NIcon,
    Heart, HeartRegular, Envelope, EnvelopeRegular,
  },
  props: {
    job: {
      type: Object,
      required: true
    }
  },
  computed: {
    iconHeart() {
      return this.job.isLiked ? Heart : HeartRegular
    },
    iconEnvelope() {
      return this.job.isLiked ? Envelope : EnvelopeRegular
    }
  },
  methods: {
    handleLikeClick() {
      this.$emit('toggle-like', this.job.id)
    },
    handleCardClick(jobData) {
      if (typeof this.addViewedItemToSidebar === 'function') {
        this.addViewedItemToSidebar(jobData)
      } else {
        console.error('addViewedItemToSidebar is not available from BaseLayout')
      }

      if (typeof this.openRightSidebar === 'function') {
        this.openRightSidebar(jobData)
      } else {
        console.error('openRightSidebar is not available from BaseLayout')
      }
    },
    handleTitleClick(job) {
      console.log('Title clicked for job:', job.title, 'Company:', job.company)
      alert(`Navigating to company page for: ${job.company}. Implement Vue Router push here.`)
    }
  }
})
  </script>
  
  <style scoped>
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

.envelope-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: white; /* 空心愛心預設白色 */
  font-size: 18px;
  padding: 3px;
  transition: transform 0.5s ease, color 0.3s ease;
}

.envelope-btn:hover {
  transform: scale(1.1);
}

  .job-card {
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.1);
    margin-top: 12px;
    padding: 20px 24px;
    overflow: hidden;
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
  }
  
  .details {
    margin-top: 8px;
    padding-left: 63px;
  }
  
  .company-info {
    display: flex;
    align-items: center;
    gap: 32px;
    font-size: 16px;
    font-weight: 500;
  }
  
  .company-name {
    color: #f5f5f5;
    font-family: Roboto, -apple-system, Roboto, Helvetica, sans-serif;
  }
  
  .industry {
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
  
  .benefit-tag {
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
  }
  
  .action-icons {
    display: flex;
    justify-content: flex-end;
    gap: 18px;
  }
  
  .action-icon {
    width: 28px;
    aspect-ratio: 1;
    object-fit: contain;
  }
  
  .applicants {
    color: #f5f5f5;
    font-size: 16px;
    font-family: Noto Sans, -apple-system, Roboto, Helvetica, sans-serif;
    font-weight: 500;
    text-align: right;
    margin: 6px 0 0;
  }
  
  @media (max-width: 991px) {
    .job-card {
      max-width: 100%;
      margin-right: 4px;
      padding: 20px;
    }
  
    .job-content {
      flex-direction: column;
    }
  
    .main-info {
      width: 100%;
    }
  
    .details {
      padding-left: 20px;
    }
  
    .actions {
      width: 100%;
      margin-top: 40px;
    }
  }
  </style>
  
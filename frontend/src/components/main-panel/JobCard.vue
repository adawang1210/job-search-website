<template>
    <article class="job-card">
      <div class="job-content">
        <div class="main-info">
          <div class="header">
            <time class="date">{{ job.date }}</time>
            <h3 class="title">{{ job.title }}</h3>
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
              <span v-for="(benefit, index) in job.benefits"
                    :key="index"
                    class="benefit-tag">
                {{ benefit }}
              </span>
            </div>
          </div>
        </div>
        <div class="actions">
          <div class="action-icons">
            <img v-for="(icon, index) in job.actionIcons"
                 :key="index"
                 :src="icon"
                 alt="Action"
                 class="action-icon" />
          </div>
          <p class="applicants">{{ job.applicants }}</p>
        </div>
      </div>
    </article>
  </template>
  
  <script>
  export default {
    name: 'JobCard',
    props: {
      job: {
        type: Object,
        required: true
      }
    }
  }
  </script>
  
  <style scoped>
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
  
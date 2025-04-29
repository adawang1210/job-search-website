<template>
  <div class="company">
    <h1>公司頁面</h1>
    <div class="company-content">
      <!-- 公司資訊區塊 -->
      <div class="company-info">
        <h2>公司資料</h2>
        <!-- 這裡放公司資料表單 -->
      </div>

      <!-- 職位管理區塊 -->
      <div class="job-management">
        <h2>職位管理</h2>
        <!-- 這裡放職位列表 -->
      </div>

      <!-- 申請者管理區塊 -->
      <div class="applicant-management">
        <h2>申請者管理</h2>
        <!-- 這裡放申請者列表 -->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CompanyView',
  data() {
    return {
      // 這裡放資料
    }
  },
  methods: {
    // 這裡放方法
  }
}
</script>

<style scoped>
.company {
  padding: 20px;
}

.company-content {
  max-width: 1200px;
  margin: 0 auto;
}

.company-info,
.job-management,
.applicant-management {
  margin-bottom: 30px;
  padding: 20px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style> 
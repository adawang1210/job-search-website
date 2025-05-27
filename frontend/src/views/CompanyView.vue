<template>
  <BaseLayout>
    <Company :id="id" />
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/layout/BaseLayout.vue'
import Company from '@/components/main-panel/Company.vue'

export default {
  name: 'CompanyView',
  props: ['id'],
  components: {
    BaseLayout,
    Company,
  },
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
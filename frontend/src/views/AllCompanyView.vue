<template>
  <BaseLayout>
    <AllCompany />
  </BaseLayout>
</template>

<script>
import BaseLayout from '@/components/layout/BaseLayout.vue'
import AllCompany from '@/components/main-panel/AllCompany.vue'

export default {
  name: 'AllCompanyView',
  components: {
    BaseLayout,
    AllCompany
  }
}
</script>

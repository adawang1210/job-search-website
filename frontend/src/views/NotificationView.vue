<template>
    <BaseLayout>
        <Notify>

        </Notify>
    </BaseLayout>
  </template>

<script>
import BaseLayout from '@/components/layout/BaseLayout.vue'
import Notify from '@/components/main-panel/Notify.vue'

export default {
  name: 'NotificationView',
  components: {
    BaseLayout,
    Notify,
  },
}
</script>

<style scoped>

</style>
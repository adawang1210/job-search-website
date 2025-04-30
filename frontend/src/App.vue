<script>
import BaseLayout from './components/layout/BaseLayout.vue'

export default {
  name: 'App',
  components: {
    BaseLayout
  }
}
</script>

<template>
  <BaseLayout>
    <router-view></router-view>
  </BaseLayout>
</template>

<style>
#app {
  height: 100vh;
}
</style>

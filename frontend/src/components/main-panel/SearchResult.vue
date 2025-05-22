<template>
  <div class="search-results-page">
    <h1>搜尋結果</h1>
    <p v-if="searchQuery">你搜尋的是：{{ searchQuery }}</p>
    <p v-else>請輸入關鍵字進行搜尋。</p>
    </div>
</template>

<script>
export default {
  name: 'SearchResult',
  data() {
    return {
      searchQuery: ''
    };
  },
  created() {
    // 當組件創建時，從路由參數讀取搜尋關鍵字
    this.searchQuery = this.$route.query.q || '';
    // 在這裡你可以根據 searchQuery 發起 API 請求獲取數據
    if (this.searchQuery) {
      this.fetchSearchResults();
    }
  },
  watch: {
    // 監聽路由變化，如果用戶在搜尋結果頁面進行新的搜尋
    '$route.query.q'(newQuery) {
      this.searchQuery = newQuery || '';
      if (this.searchQuery) {
        this.fetchSearchResults();
      }
    }
  },
  methods: {
    fetchSearchResults() {
      console.log(`準備根據關鍵字 "${this.searchQuery}" 獲取搜尋結果...`);
      // TODO: 實作 API 呼叫邏輯
      // 例如:
      // axios.get(`/api/jobs/search?keyword=<span class="math-inline">\{this\.searchQuery\}&positions\=</span>{this.<span class="math-inline">route\.query\.positions\}&regions\=</span>{this.$route.query.regions}`)
      //   .then(response => {
      //     this.results = response.data;
      //   })
      //   .catch(error => {
      //     console.error("搜尋時發生錯誤:", error);
      //   });
    }
  }
};
</script>

<style scoped>
.search-results-page {
  padding: 20px;
  color: white; /* 假設你的主要背景是暗色 */
}
</style>
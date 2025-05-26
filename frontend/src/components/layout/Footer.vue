<template>
  <footer class="footer-in-panel">
    <div class="footer-content">
      <div class="footer-links-container">
        <div class="footer-column">
          <h4>關於HireLink</h4>
          <ul>
            <li><a href="#">最新消息</a></li>
            <li><a href="#">合作夥伴</a></li>
            </ul>
        </div>
        <div class="footer-column">
          <h4>求職者</h4>
          <ul>
            <li><a href="#">搜尋最新職缺</a></li>
            <li><a href="#">瀏覽公司列表</a></li>
            <li><a href="#">履歷填寫技巧</a></li>
            <li><a href="#">面試準備攻略</a></li>
            <li><a href="#">訂閱工作通知</a></li>
          </ul>
        </div>
        <div class="footer-column">
          <h4>企業主</h4>
          <ul>
            <li><a href="#">刊登職缺</a></li>
            <li><a href="#">公司帳號登入</a></li>
            <li><a href="#">人才資料庫搜尋</a></li>
            <li><a href="#">雇主品牌宣傳</a></li>
          </ul>
        </div>
        <div class="footer-column">
          <h4>支援服務</h4>
          <ul>
            <li><a href="#">常見問題 (FAQ)</a></li>
            <li><a href="#">聯絡我們</a></li>
            <li><a href="#">服務條款</a></li>
            <li><a href="#">隱私權政策</a></li>
            <li><a href="#">網站導覽</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; {{ currentYear }} HireLink. 保留一切權利.</p>
        <div class="social-media-icons">
          <img src="/HireLink.png" alt="HireLink" style="height: 24px; width: auto;">
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer',
  data() {
    return {
      currentYear: new Date().getFullYear()
    };
  }
}
</script>

<style scoped>
.footer-in-panel {
  padding: 30px 15px; /* 增加上下內邊距 */
  background-color: #2a2a2a;
  color: #a0a0a0;
  flex-shrink: 0;
  margin-top: auto;
}

.footer-content {
  max-width: 1100px; /* 稍微增加寬度以容納更多內容 */
  margin: 0 auto;
  text-align: left; /* 讓內容預設靠左 */
}

.footer-links-container {
  display: flex;
  flex-wrap: wrap; /* 在小螢幕上換行 */
  justify-content: space-between; /* 平均分配空間 */
  gap: 20px; /* 各欄位之間的間距 */
  margin-bottom: 30px; /* 與下方版權資訊的間距 */
}

.footer-column {
  flex: 1; /* 讓各欄位平均分配寬度 */
  min-width: 180px; /* 設定最小寬度，避免過度壓縮 */
  padding: 0 10px; /* 欄位內邊距 */
}

.footer-column h4 {
  color: #ffffff; /* 標題顏色調亮 */
  margin-bottom: 15px;
  font-size: 1.1em;
}

.footer-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-column ul li {
  margin-bottom: 10px; /* 項目間距 */
}

.footer-column ul li a {
  color: #a0a0a0; /* 連結預設文字顏色 */
  text-decoration: none; /* 連結預設無底線 (但在 hover 時會加上) */
  background-color: transparent; /* 確保預設背景是透明的 */
  transition: color 0.3s ease, background-color 0.3s ease; /* 平滑過渡效果 */
  padding: 2px 0; /* 可選：增加一點點垂直內邊距，讓底線和文字有點距離，視覺上可能更好 */
}

.footer-column ul li a:hover {
  text-decoration: underline;
}

.footer-bottom {
  padding-top: 20px;
  border-top: 1px solid #444; /* 在連結區和版權區之間加一條分隔線 */
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  text-align: center; 
  gap: 10px; /* 版權和社交圖示之間的間隔 */
}

.footer-bottom p {
  margin: 0;
  font-size: 0.9em;
}

.social-media-icons span {
  font-size: 0.9em;
  /* 實際使用圖標時，可以調整圖標大小和間距 */
}

@media (max-width: 768px) {
  .footer-links-container {
    flex-direction: column; /* 在較小螢幕上堆疊排列 */
    align-items: center; /* 欄位內容置中 */
    text-align: center; /* 欄位文字置中 */
  }
  .footer-column {
    min-width: unset; /* 取消最小寬度限制 */
    width: 100%; /* 欄位佔滿寬度 */
    margin-bottom: 20px; /* 堆疊時的欄位間距 */
  }
  .footer-column:last-child {
    margin-bottom: 0;
  }
  .footer-bottom {
    flex-direction: column; /* 版權和社交圖示也堆疊 */
    text-align: center;
  }
  .footer-bottom p {
    margin-bottom: 10px; /* 版權文字和社交圖示的間距 */
  }
}
</style>
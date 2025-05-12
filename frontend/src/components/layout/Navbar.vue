<template>
  <div class="navbar">
    <div class="overlay" v-show="showPositionPopup || showRegionPopup" @click="closeAllPopups"></div>
    
    <router-link to="/" class="home-btn">
      <i class="fa-solid fa-house"></i>
    </router-link>
    <div class="search">
      <div class="popup" :class="{ active: showPositionPopup }">
        <div class="position-list">
          <div class="close-btn" @click="closePopup('position')">&times;</div>
          <button type="button" class="yes-btn" @click="confirmPosition">確認</button>
          <div class="jobs">
            <ul class="jobs-column">
              <li v-for="(position, index) in positions.slice(0, 9)" :key="index">
                <label>
                  <input type="checkbox" v-model="selectedPositions" :value="position.value">
                  {{ position.label }}
                </label>
              </li>
            </ul>
            <ul class="jobs-column">
              <li v-for="(position, index) in positions.slice(9)" :key="index">
                <label>
                  <input type="checkbox" v-model="selectedPositions" :value="position.value">
                  {{ position.label }}
                </label>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <button type="button" class="position-btn" @click="togglePopup('position')">
        職務 <i class="fa-solid fa-caret-down"></i>
      </button>

      <div class="popup" :class="{ active: showRegionPopup }">
        <div class="region-list">
          <div class="close-btn" @click="closePopup('region')">&times;</div>
          <button type="button" class="yes-btn" @click="confirmRegion">確認</button>
          <div class="region">
            <ul class="region-column" v-for="(column, index) in regionColumns" :key="index">
              <li v-for="region in column" :key="region.id">
                <label>
                  <input type="checkbox" v-model="selectedRegions" :value="region.id">
                  {{ region.name }}
                </label>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <button type="button" class="region-btn" @click="togglePopup('region')">
        地區 <i class="fa-solid fa-caret-down"></i>
      </button>
      <input class="search-input" v-model="searchQuery" placeholder="工作職稱、公司名、技能">
      <button type="submit" class="search-btn" @click="handleSearch">
        <i class="fa-solid fa-magnifying-glass"></i>
      </button>
    </div>
    <div class="quick-link">
      <router-link to="/company" class="all-company">公司</router-link>
      <router-link to="/profile" class="personal-profile">個人檔案</router-link>
      <button type="button" class="bell-btn">
        <i class="fa-solid fa-bell"></i>
      </button>
    </div>
    <router-link to="/profile" class="avatar-frame"></router-link>
  </div>
</template>

<script>
export default {
  name: 'Navbar',
  data() {
    return {
      showPositionPopup: false,
      showRegionPopup: false,
      selectedPositions: [],
      selectedRegions: [],
      searchQuery: '',
      positions: [
        { value: 'position1', label: '經營/人資類' },
        { value: 'position2', label: '行政/總務/法務類' },
        { value: 'position3', label: '財會/金融專業類' },
        { value: 'position4', label: '行銷/企劃/專案管理類' },
        { value: 'position5', label: '客服/門市/業務/貿易類' },
        { value: 'position6', label: '餐飲/旅遊/美容美髮類' },
        { value: 'position7', label: '資訊軟體系統類' },
        { value: 'position8', label: '操作/技術/維修類' },
        { value: 'position9', label: '資材/物流/運輸類' },
        { value: 'position10', label: '營建/製圖類' },
        { value: 'position11', label: '傳播藝術/設計類' },
        { value: 'position12', label: '文字/傳媒工作類' },
        { value: 'position13', label: '醫療/保健服務類' },
        { value: 'position14', label: '學術/教育/輔導類' },
        { value: 'position15', label: '研發相關類' },
        { value: 'position16', label: '生產製造/品管/環衛類' },
        { value: 'position17', label: '軍警消/保全類' },
        { value: 'position18', label: '其他職類' }
      ],
      regions: [
        { id: '台北市', name: '台北市' },
        { id: '新北市', name: '新北市' },
        { id: '宜蘭縣', name: '宜蘭縣' },
        { id: '基隆市', name: '基隆市' },
        { id: '桃園市', name: '桃園市' },
        { id: '新竹縣市', name: '新竹縣市' },
        { id: '苗栗縣', name: '苗栗縣' },
        { id: '台中市', name: '台中市' },
        { id: '彰化縣', name: '彰化縣' },
        { id: '南投縣', name: '南投縣' },
        { id: '雲林縣', name: '雲林縣' },
        { id: '嘉義縣市', name: '嘉義縣市' },
        { id: '台南市', name: '台南市' },
        { id: '高雄市', name: '高雄市' },
        { id: '屏東縣', name: '屏東縣' },
        { id: '台東縣', name: '台東縣' },
        { id: '花蓮縣', name: '花蓮縣' },
        { id: '澎湖縣', name: '澎湖縣' },
        { id: '金門縣', name: '金門縣' },
        { id: '連江縣', name: '連江縣' }
      ]
    }
  },
  computed: {
    regionColumns() {
      const chunkSize = 7;
      const columns = [];
      for (let i = 0; i < this.regions.length; i += chunkSize) {
        columns.push(this.regions.slice(i, i + chunkSize));
      }
      return columns;
    }
  },
  methods: {
    togglePopup(type) {
      if (type === 'position') {
        this.showPositionPopup = !this.showPositionPopup;
        this.showRegionPopup = false;
      } else if (type === 'region') {
        this.showRegionPopup = !this.showRegionPopup;
        this.showPositionPopup = false;
      }
    },
    closePopup(type) {
      if (type === 'position') {
        this.showPositionPopup = false;
      } else if (type === 'region') {
        this.showRegionPopup = false;
      }
    },
    closeAllPopups() {
      this.showPositionPopup = false;
      this.showRegionPopup = false;
    },
    confirmPosition() {
      this.showPositionPopup = false;
      // 这里可以添加确认后的处理逻辑
    },
    confirmRegion() {
      this.showRegionPopup = false;
      // 这里可以添加确认后的处理逻辑
    },
    handleSearch() {
      // 这里可以添加搜索处理逻辑
      console.log('Search query:', this.searchQuery);
      console.log('Selected positions:', this.selectedPositions);
      console.log('Selected regions:', this.selectedRegions);
    }
  }
}
</script>

<style scoped>
body {
    background-color: black;
    font-family: Arial, sans-serif;
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100vh;
    margin: 0;
    overflow-x: hidden;
}

.navbar {
    display: flex;
    align-items: center;
    padding: 16px 20px 0px 16px;       
    background-color: #000000;
    height: 56px;            
    box-sizing: border-box;
    flex-wrap: nowrap;
    overflow: hidden; 
    gap: 16px;
    min-width: 0;
    flex-shrink: 0;
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
}

.navbar .avatar-frame {
    all: unset; /* 移除所有 bootstrap 繼承樣式 */
    display: inline-block;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: white;
    background-image: url("/public/user-avatar.png");
    background-size: cover;
    background-position: center;
    cursor: pointer;
    flex-shrink: 0;
    margin-left: auto; 
}

.navbar a,
.navbar button {
    border: none;
    background: none;
    font-size: 14px;
    padding: 4px 8px;
    color: #ffffff;
    white-space: nowrap;
    cursor: pointer; 
}

.search-btn i,
.bell-btn i,
.fa-solid {
    font-size: 16px;
}

.search {
    display: flex;
    align-items: center;
    flex-shrink: 1;     
    flex-grow: 1;       
    min-width: 0;
    min-width: 200px;
    max-width: 500px;       
    padding: 4px 8px;
    gap: 8px;
    border-radius: 30px;
    background-color: #383333;    
    height: 32px;
    overflow: hidden;
    box-sizing: border-box;
}

.search-input {
    flex-grow: 1;
    min-width: 0;
    font-size: 14px;
    border: none;
    outline: none;
    background-color: #383333;
    caret-color: #ffffff;
    color: white;
}

input::placeholder {
    color: rgb(145, 145, 145); 
    opacity: 1;  
}

.quick-link {
    display: flex; 
    align-items: center;
    gap: clamp(8px, 2vw, 30px);
    white-space: nowrap;
    margin-left: clamp(8px, 2vw, 30px);
    flex-shrink: 0; 
}

.navbar a {
    text-decoration: none;
    color: rgb(255, 255, 255);
}

@media (max-width: 480px) {
    .position-btn,
    .region-btn {
      display: none;
    }
}

.popup {
    display: none;
    position: fixed;
    top: 50%;
    left: 50%;
    width: 70vw;
    max-width: 500px;
    height: 60vh;
    max-height: 500px;
    transform: translate(-50%, -50%);
    border-radius: 10px;
    padding: 20px 30px 60px;
    z-index: 1001;
    overflow-y: auto;
    background-color: #594f4f;
}

.popup.active {
    display: block;
}

.overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.7);
    z-index: 1000;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.overlay.active {
    display: block;
    opacity: 1;
}

.popup .position-list,
.popup .region-list {
    position: relative;
    width: 100%;
    height: 100%;
    background: #594f4f;
    border-radius: 10px;
    padding: 20px 30px 60px;
    box-sizing: border-box;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: stretch;
    box-shadow: 0 0 10px rgba(110, 110, 110, 0.3);
}

.popup .position-list .jobs,.popup .region-list .region {
    list-style: none;
    padding: 0;
    display: flex;
    justify-content: center;
    gap: 0px; 
    flex-wrap: nowrap;
}

.popup .position-list .jobs-column{
    display: flex;
    flex-direction: column;
    gap: 4px;
    max-width: 45%;
}

.popup .position-list .jobs li{
    font-size: 14px;
    cursor: pointer;
    padding: 2px;
    margin-left: -30px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.popup .position-list .jobs li label{
    display: flex;
    align-items: center;
    gap: 6px;
    color: #ffffff;
    text-decoration: none;
    cursor: pointer;
    white-space: nowrap;             /* 不換行 */
    overflow: hidden;                /* 超出裁切 */
    text-overflow: ellipsis;        /* 顯示省略號 */
    max-width: 100%;
}

.popup .region-list .region-column {
    display: flex;
    flex-direction: column;
    gap: 4px;
    max-width: 45%;
}

.popup .region-list .region li {
    font-size: 14px;
    cursor: pointer;
    padding: 6px;
    margin-left: -30px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.popup .region-list .region li label {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #ffffff;
    text-decoration: none;
    cursor: pointer;
    white-space: nowrap;             /* 不換行 */
    overflow: hidden;                /* 超出裁切 */
    text-overflow: ellipsis;        /* 顯示省略號 */
    max-width: 100%;
}

.popup .close-btn {
    position:absolute;
    right:20px;
    top:20px;
    width:30px;
    height:30px;
    color:#ffffff;
    font-size:20px;
    line-height:30px;
    text-align:center;
    border-radius:50%;
    cursor: pointer;
}

.popup .yes-btn {
    position: absolute;
    right: 40px;
    bottom: 40px;
    border: #a9a3a1 2px solid;
    color: white;
    padding: 4px 8px;
    border-radius: 50px;
    font-size: 10px;
    cursor: pointer;
}

/* 添加按钮样式 */
.position-btn,
.region-btn {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 4px 8px;
    border: none;
    background: none;
    color: white;
    font-size: 14px;
    cursor: pointer;
    white-space: nowrap;
}

.position-btn:hover,
.region-btn:hover {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}

.position-btn i,
.region-btn i {
    font-size: 12px;
    transition: transform 0.3s ease;
}

.position-btn:hover i,
.region-btn:hover i {
    transform: rotate(180deg);
}
</style> 
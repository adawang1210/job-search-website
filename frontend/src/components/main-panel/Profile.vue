<template>
    <div class="middle-content">
        <div class="container">
            <section class="profile">
                <img ref="avatar" src="/photo-20706-u.jpg" alt="劉子源大頭照" class="avatar">
                <div class="info">
                    <h1>劉子源</h1>
                    <p>桃園中壢・30歲・應屆畢業生</p>
                </div>
            </section>


            <!-- 編輯按鈕放在 profile 與 about 之間 -->
            <i class="fa-solid fa-pen edit-icon"></i>

            <h2>關於</h2>
            <section class="about">
                <ul>
                    <li><strong>姓名：</strong>劉子源</li>
                    <li><strong>年齡：</strong>30歲</li>
                    <li><strong>性別：</strong>男</li>
                    <li><strong>學歷：</strong>國立政治大學資訊科學學系博士</li>
                    <li><strong>手機：</strong>0800 000 000</li>
                    <li><strong>信箱：</strong>zylu@ncu.edu.tw</li>
                    <li><strong>地址：</strong>320桃園市中壢區中大路300號</li>
                    <li><strong>語言：</strong>中文/英文</li>
                </ul>
            </section>


            <h2>技能</h2>
            <section class="skills">
                <ul>
                    <li> 密碼學</li>
                    <li> 資訊安全</li>
                    <li> 隱私保護技術</li>
                    <li> 網頁程式設計</li>
                </ul>
            </section>


            <h2>履歷表</h2>
            <!-- 簡介區塊 -->
            <section class="intro">
            <h3><i class="fa-solid fa-circle-info"></i> 簡介</h3>
            <p>
                我在大學與研究所期間專注於應用密碼學，尤其著重在搜尋加密、身分基礎加密與抗量子電腦攻擊的加密系統設計。這些背景構成了我後續研究與教學的核心方向。
            </p>
            </section>

            <!-- 學歷區塊（使用節點式時間軸風格顯示） -->
            <section class="education timeline-section">
            <h3><i class="fa-solid fa-graduation-cap"></i> 學歷</h3>
            <div class="timeline">

                <!-- 第一段：2010 - 2014 -->
                <div class="timeline-segment"> <!-- 一段學歷經歷區塊 -->
                <div class="timeline-point">
                    <span class="year-label">2010</span>
                    <div class="dot"></div>
                </div>
                <div class="timeline-line"></div>
                <div class="timeline-point">
                    <span class="year-label">2014</span>
                    <div class="dot"></div>
                </div>
                <div class="timeline-entry">
                    <h4>國立清華大學資訊工程學士</h4>
                    <p>我的主要研究重點是應用密碼學領域，尤其專注於搜尋加密和基於身分的加密等領域。此外，我還關注基於格的密碼系統，由於它們能夠抗重量學電腦攻擊，很可能成為下個世紀的關鍵密碼學。</p>
                </div>
                </div>

                <!-- 第二段：2015 - 2018 -->
                <div class="timeline-segment">
                <div class="timeline-point">
                    <span class="year-label">2015</span>
                    <div class="dot"></div>
                </div>
                <div class="timeline-line"></div>
                <div class="timeline-point">
                    <span class="year-label">2018</span>
                    <div class="dot"></div>
                </div>
                <div class="timeline-entry">
                    <h4>國立清華大學資訊工程碩士</h4>
                    <p>我的主要研究重點是應用密碼學領域，尤其專注於搜尋加密和基於身分的加密等領域。此外，我還關注基於格的密碼系統，由於它們能夠抗重量學電腦攻擊，很可能成為下個世紀的關鍵密碼學。</p>
                </div>
                </div>

                <!-- 第三段：2019 - 2024 -->
                <div class="timeline-segment">
                <div class="timeline-point">
                    <span class="year-label">2019</span>
                    <div class="dot"></div>
                </div>
                <div class="timeline-line"></div>
                <div class="timeline-point">
                    <span class="year-label">2024</span>
                    <div class="dot"></div>
                </div>
                <div class="timeline-entry">
                    <h4>國立政治大學資訊科學博士</h4>
                    <p>博士學位畢業於台灣國立政治大學資訊學系，師從 Raylin Tso 教授。此外，我還獲得了另一個博士學位，畢業於日本金澤大學自然科學技術研究生院，師從 Masahiro Mambo 教授（雙學位課程）。</p>
                </div>
                </div>

            </div>
            </section>

            <!-- 工作經歷區塊（使用節點式時間軸風格顯示） -->
            <section class="experience timeline-section">
            <h3><i class="fa-solid fa-briefcase"></i> 工作經歷</h3>
            <div class="timeline">

                <!-- 第一段：2025 - 現在 -->
                <div class="timeline-segment">
                <div class="timeline-point">
                    <span class="year-label">2025</span>
                    <div class="dot"></div>
                </div>
                <div class="timeline-line"></div>
                <div class="timeline-point">
                    <span class="year-label">現在</span>
                    <div class="dot"></div>
                </div>
                <div class="timeline-entry">
                    <h4>國立中央大學資訊管理系助理教授</h4>
                    <p>在中央大學資訊管理系任職，教授網頁程式設計以及企業資料通訊和隱私課，同時帶領碩博士進行研究，通常辦公時間為周一和周三。</p>
                </div>
                </div>

            </div>
            </section>




            <h2>我的專案</h2>
            <section class="projects">
                <div class="logo-scroll-container">
                    <div><img src="/螢幕擷取畫面 2025-05-07 001948.png" alt="流量動物視覺化分析" draggable="false">
                        <p>流量動物視覺化分析</p>
                    </div>
                    <div><img src="/螢幕擷取畫面 2025-05-07 001948.png" alt="食安機器人" draggable="false">
                        <p>食安機器人</p>
                    </div>
                    <div><img src="/螢幕擷取畫面 2025-05-07 001948.png" alt="台北通徵服務" draggable="false">
                        <p>台北通徵服務</p>
                    </div>
                    <div><img src="/螢幕擷取畫面 2025-05-07 001948.png" alt="開源" draggable="false">
                        <p>開源</p>
                    </div>
                </div>
            </section>


            <h2>已按讚</h2>
            <section class="companies">
                <div class="logo-scroll-container">
                    <div><img src="/ogimage.png" alt="LINE" draggable="false">
                        <p>LINE</p>
                    </div>
                    <div><img src="/研華科技.jpg" alt="研華科技" draggable="false">
                        <p>研華科技</p>
                    </div>
                    <div><img src="/A-Social-Technology-Company-Meta-1.jpg" alt="Meta" draggable="false">
                        <p>Meta</p>
                    </div>
                    <div><img src="/amazon.png" alt="Amazon" draggable="false">
                        <p>Amazon</p>
                    </div>
                </div>
            </section>

            <h2>已追蹤</h2>
            <section class="technologies">
                <div class="logo-scroll-container">
                    <div><img src="/17061913美簽.jpg" alt="張李治華" draggable="false">
                        <p>張李治華</p>
                    </div>
                    <div><img src="/ycchen.jpg" alt="陳以錚" draggable="false">
                        <p>陳以錚</p>
                    </div>
                    <div><img src="/胡雅涵老師大頭照1121211.jpg" alt="胡雅涵" draggable="false">
                        <p>胡雅涵</p>
                    </div>
                    <div><img src="/官網.jpg" alt="曾筱珽" draggable="false">
                        <p>曾筱珽</p>
                    </div>
                    <div><img src="/T123603300.jpg" alt="周恩頤" draggable="false">
                        <p>周恩頤</p>
                    </div>
                    <div><img src="/F125393020.jpg" alt="柯士文" draggable="false">
                        <p>柯士文</p>
                    </div>
                </div>
            </section>


        </div>
    </div>
</template>

<script>
export default {
    name: 'Profile',

    data() {
    return {
      // 你的資料
    }
  },

  methods: {
    // 你的方法
  },

  mounted() {
    // 這裡寫圖片抓色的邏輯
    const img = this.$refs.avatar;

    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');

      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      ctx.drawImage(img, 0, 0);

      const imageData = ctx.getImageData(0, 0, img.naturalWidth, 50);
      const pixels = imageData.data;

      let r = 0, g = 0, b = 0, count = 0;
      for (let i = 0; i < pixels.length; i += 4) {
        r += pixels[i];
        g += pixels[i + 1];
        b += pixels[i + 2];
        count++;
      }

      r = Math.floor(r / count);
      g = Math.floor(g / count);
      b = Math.floor(b / count);

      const avgColor = `rgb(${r}, ${g}, ${b})`;

      // 改變背景
      const contentEl = document.querySelector('.middle-content');
      contentEl.style.background = `linear-gradient(
                                    to bottom,
                                    ${avgColor} 0%,
                                    #2b2b2b 20%,
                                    #2b2b2b 100%
                                    )`;
    };
  }
}
</script>

<style scoped>
/* middle-content 區塊 */
.middle-content {
    width: 1005px;
    margin-left: auto;   
    background: linear-gradient(to bottom, #bbbbbb 0%, #bbbbbb 160px, #2b2b2b 100%);
    padding: 48px 32px;
    color: #fff;
    box-sizing: border-box;
    border-radius: 12px;
    overflow: hidden;
}



/* middle-content 區塊內的 h2 樣式 */
.middle-content h2 {
    margin-top: 0;
    margin-bottom: -15px;
    /* 你想要的距離，自己調整 */
}

/* container 區塊 */
.container {
    max-width: 900px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 40px;
}

/* 頭像區 */
.profile {
    display: flex;
    align-items: center;
    gap: 40px;
    padding: 0;
    background: none;
    border: none;
    position: relative;
}

/* 頭像圖片 */
.profile .avatar {
    width: 220px;
    height: 220px;
    border-radius: 0px;
    object-fit: cover;
}

/* 姓名樣式 */
.profile .info h1 {
    margin: 0;
    font-size: 32px;
    font-weight: bold;
    color: #ffffff;
}


/* 個人簡介樣式 */
.profile .info p {
    margin-top: 6px;
    font-size: 18px;
    color: #ffffff;
}

/* 編輯 icon 顯示 */
.edit-icon {
    display: block;
    font-size: 20px;
    color: white;
    cursor: pointer;
    margin: 0 0 12px auto;
    /* 自動靠右並與下方區塊有距離 */
    padding-right: 16px;
}


/* 編輯 icon hover 效果 */
.edit-icon:hover {
    opacity: 0.7;
}

/* 區塊標題通用樣式 */
.block-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 8px;
    color: white;
}

/* 每個 section 區塊背景 */
section {
    background: rgba(255, 255, 255, 0.08);
    padding: 20px;
    border-radius: 5px;
    position: relative;
}

/* 關於區塊 */
.about ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.about li {
    color: #ffffff;
    font-size: 16px;
    line-height: 1.8;
}

/* 技能區塊 */
.skills ul {
    list-style: none;
    padding-left: 0;
    font-size: 16px;
    line-height: 2;
}

.skills li {
    color: #ffffff;
}

.skills li::before {
    content: '✔';
    margin-right: 8px;
    color: #00d26a;
}

/* 履歷區塊 */
.resume p {
    font-size: 16px;
    line-height: 1.8;
    color: #ffffff;
}

/* logo 容器 */
.logos {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 24px;
    text-align: center;
}

/* logo 圖片 */
.logos img {
    width: 100px;
    height: 100px;
    object-fit: contain;
    background: white;
    border-radius: 12px;
    padding: 12px;
}


/* logo user-select 設定 */
.logo-scroll-container {
    display: flex;
    overflow-x: auto;
    gap: 24px;
    padding: 12px 0;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
}

/* logo 滾動區 scrollbar 隱藏 */
.logo-scroll-container::-webkit-scrollbar {
    display: none;
}

/* logo 拖曳 cursor */
.logo-scroll-container.dragging {
    cursor: grabbing;
    cursor: -webkit-grabbing;
}

.logo-scroll-container {
    user-select: none;
    -webkit-user-select: none;
    /* Safari */
    -moz-user-select: none;
    /* Firefox */
    -ms-user-select: none;
    /* IE/Edge */
}

.logo-scroll-container>div {
    flex: 0 0 calc(25% - 18px);
    /* 每排 4 個 */
    text-align: center;
    scroll-snap-align: start;
}

.logo-scroll-container>div img {
    width: 100%;
    aspect-ratio: 1 / 1;
    object-fit: cover;
    border-radius: 12px;
    background-color: white;
    box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
}

.logo-scroll-container>div p {
    color: white;
    margin-top: 6px;
    font-size: 14px;
}

.intro h3{
  position: relative;
  padding-left: 20px;
  font-size: 18px;
}

.intro p {
  margin-top: 10px;
  margin-left: 20px;
  padding-left: 20px;
  font-size: 16px;
  color: #ffffff;
}

/* 時間軸區塊通用樣式 */
.timeline {
  position: relative;
  margin-left: 50px;
  margin-top: 25px;
  padding-left: 20px;
}

.timeline-section h3 {
  padding-left: 20px; /* 時間軸區塊內部左邊距離 */
  font-size: 18px;
}

.timeline-segment {
  position: relative;
  margin-bottom: 60px;
}

.timeline-point {
  position: relative;         /* 設定相對定位，供絕對定位子元素參考使用 */
  margin-bottom: 80px;       /* 每個節點與下個節點（或段落）的垂直距離 */
  line-height: 1.4;          /* 行高設定，影響文字的垂直行距 */
  display: flex;             /* 使用 flex 排版，讓年份與圓點並排 */
  align-items: center;       /* 垂直置中對齊年份與圓點 */
  gap: 8px;                  /* 年份與圓點之間的水平間距 */
}

.year-label {
  color: white;              /* 年份文字顏色為白色 */
  font-size: 14px;           /* 年份文字大小 */
  font-weight: bold;         /* 年份字體粗體 */
  width: 50px;        /* ✅ 統一寬度，讓任何文字都不會推擠圓點 */
  text-align: right;  /* ✅ 文字靠右對齊，圓點靠左 */
  flex-shrink: 0;     /* ✅ 防止年份被壓縮 */
}

.dot {
  width: 5px;                /* 圓點寬度 */
  height: 5px;               /* 圓點高度 */
  background-color: white;  /* 圓點內部填白色 */
  border-radius: 50%;        /* 設為圓形（100% 圓角） */
}

.timeline-line {
  position: absolute;         /* 絕對定位，使其可以疊在任意位置 */
  left: 59.5px;                  /* 線條距離容器左邊 59.5px，對齊圓點位置 */
  top: 8px;                   /* 線條從圓點下緣開始畫（根據 dot 高度調整） */
  width: 1.5px;               /* 線條寬度很細 */
  height: 100px;               /* 線條高度為 100px，對應 segment 間距 */
  background-color: #ffffff; /* 線條顏色為白色（在深色背景上看得清） */
  z-index: auto;              /* 圖層順序使用預設值 */
}

/* 文字內容區塊，放在節點右邊 */
.timeline-entry {
  margin-left: 75px;
  margin-top: -197px;
  color: #ffffff;
}

.timeline-entry h4 {
  margin: 0;
  font-size: 18px;
  color: #ffffff;
}

.timeline-entry p {
  margin: 20px 0 0; /* 與標題間距 */
  font-size: 16px;
  line-height: 1.6;
  color: #ffffff;
}
</style>

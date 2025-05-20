<template>
    <div class="middle-content">
        <section class="company-profile">
            <div class="profile-container">
                <div class="profile-grid">
                    <div class="logo-column">
                        <div class="company-logo">
                            <img ref="avatar" src="/company-icon.png" />
                            alt="Company Logo" class="logo-image" />
                        </div>
                    </div>
                    <div class="info-column">
                        <div class="company-info">
                            <span class="info-label">公司</span>
                            <h1 class="company-name">宜得利家居股份有限公司</h1>
                            <p class="company-tags">百大雇主 · 外商 · 新鮮人請進</p>
                            <p class="job-count">26個工作機會</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <section class="job-listings">
            <div class="listings-header">
                <h2 class="section-title">工作機會</h2>
                <div class="page-size">
                    <label for="pageSize" class="size-text">每頁</label>
                    <select id="pageSize" v-model="pageSize" class="size-select">
                        <option :value="5">5 筆</option>
                        <option :value="10">10 筆</option>
                    </select>
                    <img src="https://cdn.builder.io/api/v1/image/assets/11cf996c32eb40d1986fd0fd5ad9dc01/15193d2dbb18d9ce528df6754b8d30f8c835e721?placeholderIfAbsent=true"
                        alt="Arrow" class="arrow-icon" />
                </div>
            </div>
            <JobCard v-for="(job, index) in paginatedJobs" :key="index" :job="job" />
        </section>
        <section class="company-information">
            <h2 class="section-title">關於</h2>
            <div class="cards">
                <div class="info-card">
                    <h3>公司介紹</h3>
                    <div class="company-details">
                        <div>
                            <div class="detail-group">
                                <div class="detail-item">
                                    <div class="label">建材/家具零售業</div>
                                    <div class="value">產業類別</div>
                                </div>
                                <div class="detail-item">
                                    <div class="label">家具、家飾商品零售業</div>
                                    <div class="value">產業描述</div>
                                </div>
                                <div class="detail-item">
                                    <div class="label">1000人</div>
                                    <div class="value">員工人數</div>
                                </div>
                                <div class="detail-item">
                                    <div class="label">9億4000萬元</div>
                                    <div class="value">資本額</div>
                                </div>
                            </div>

                            <div class="detail-group">
                                <div class="detail-item">
                                    <div class="label">陳小姐</div>
                                    <div class="value">聯絡人</div>
                                </div>
                                <div class="detail-item">
                                    <div class="label">暫不提供</div>
                                    <div class="value">電話</div>
                                </div>
                                <div class="detail-item">
                                    <div class="label">暫不提供</div>
                                    <div class="value">傳真</div>
                                </div>
                                <div class="detail-item">
                                    <div class="label">台北市中正區許昌街17號7樓之1</div>
                                    <div class="value">地址</div>
                                </div>
                            </div>

                            <div class="detail-group">
                                <div class="detail-item">
                                    <div class="label">公司連結</div>
                                    <div class="value">相關連結</div>
                                </div>
                                <div class="detail-item">
                                    <div class="label">NITORI人才招募</div>
                                </div>
                                <div class="detail-item">
                                    <div class="label">NITORI人才永續行動</div>
                                </div>
                                <div class="detail-item">
                                    <div class="label">NITORI日本官方網站</div>
                                </div>
                            </div>
                        </div>

                        <div class="description">
                            宜得利家居為株式会社NITORI所獨資的海外子公司。株式会社NITORI在1972年3月以兩家連鎖店創業，到2023年2月為止在日本全國已發展到了767間店舖，從北海道至冲繩均有分店，2002年竣工日本最大規模「關東物流中心」，其物流中心及進口量皆居日本首位。並且成功於2002年10月在日本公開上市。<br><br>
                            NITORI以獨自的「O.T.C.M.(One-House Total Coordination
                            Merchandising)思想」為基礎，亦即本著一個家庭所有空間綜合配色的商品開發的思想來開發商品，並在賣場展示。從原物材料的採購，到製造、物流、銷售以至消費過程都由公司全程規劃。因此NITORI被稱為是日本第一個「居家生活規劃企業」。<br><br>
                            本公司為NITORI首度於海外設立的分店，2007年5月於高雄開設海外第一家店舖，至2025年1月止，於全台灣開設共66間店舖。並計畫2032年前在台灣開設200家分店。<br><br>
                            NITORI致力於全球化事業，除了日本及台灣，陸續於中國、香港、馬來西亞、新加坡、泰國展店，目前全球共有1048間店舖(2025年1月)。採購據點遍佈全球，並於越南設立工廠專門生產NITORI家具產品。<br><br>
                            <strong>經營理念</strong><br>
                            我們的願景：將繽紛的居家生活呈獻給世界上的每一個人<br>
                            我們的藍圖：2032年，連鎖店目標3000家，銷售額目標三兆日元。<br><br>
                            透過獨特的商業模式「製造、物流、IT、零售」，以提供品質穩定且更實惠價格的商品，為顧客打造整體搭配的居家生活。
                        </div>
                    </div>
                </div>

                <div class="info-card">
                    <h3>主要商品</h3>
                    <div class="description">
                        對外：家具、家飾用品門市、倉儲物流、法人事業（商業設施設計規劃）<br>
                        對內：商品開發、貿易、廣告宣傳、總務、人事、財務、資訊管理、人材招募等。<br><br>
                        宜得利家居獨特的配轉教育制度，除了門市的工作之外，亦可以利用輪調的機制進入總公司其他部門。即使是以往不熟悉的領域，也可以透過學習不同部門的工作內容及方式，充實自己的能力。
                    </div>
                </div>

                <div class="info-card">
                    <h3>福利制度</h3>
                    <div class="benefits-grid">
                        <div class="benefit-tags">
                            <div class="benefit-group">
                                <div class="benefit-tag">年終獎金</div>
                                <div class="benefit-tag">節日獎金/禮品</div>
                                <div class="benefit-tag">員工優惠</div>
                                <div class="benefit-tag">津貼/補助</div>
                                <div class="benefit-tag">優於勞基法特休</div>
                            </div>
                            <h4>法定項目</h4>
                            <div class="benefit-group">
                                <div class="benefit-tag">年終獎金</div>
                                <div class="benefit-tag">節日獎金/禮品</div>
                                <div class="benefit-tag">員工優惠</div>
                                <div class="benefit-tag">津貼/補助</div>
                                <div class="benefit-tag">優於勞基法特休</div>
                            </div>
                            <h4>其他福利</h4>
                        </div>

                        <div class="description">
                            <div class="content">
                                <strong>●法定員工保障</strong><br>
                                1. 勞保、健保<br>
                                2. 正職、兼職皆享有團保<br>
                                3. 兼職人員國定假日雙倍薪<br>
                                4. 健全休假制度（周休二日、平均月休8天）<br>
                                5. 各項補助（退休金提撥、結婚禮金、生育津貼等）<br><br>

                                <strong>●員工獎勵</strong><br>
                                1. 夏季獎金、冬季獎金<br>
                                2. 每年績效獎金<br>
                                3. 內部競賽獎金<br>
                                4. 業績評比獎金<br>
                                5. 員工推薦獎金<br><br>

                                <strong>●教育福利</strong><br>
                                1. 商品知識學習網站<br>
                                2. 線上日語教育系統<br>
                                3. 海外研修（日本、美國、越南）<br>
                                4. 證照獎金（日檢、國貿人員等）<br>
                                5. OJT、OFFJT教育研修課程（連鎖店理論、店長研修、物流研修等）<br><br>

                                <strong>●落實CSR維護員工身心健康</strong><br>
                                1. 專業護理師諮詢<br>
                                2. 健檢結果個別追蹤<br><br>

                                <strong>●員工特別福利</strong><br>
                                1. 員工購物優惠<br>
                                2. 年度健康檢查<br>
                                3. 日本觀光地特約會館利用申請（正職）
                            </div>
                        </div>
                    </div>
                </div>

                <div class="gallery">
                    <h3>企業照片</h3>
                    <div class="gallery-scroll-wrapper">
                        <div class="gallery-grid">
                            <div class="gallery-item"><img src="/company-photo1.jpg" alt="Photo 1"></div>
                            <div class="gallery-item"><img src="/company-photo2.jpg" alt="Photo 2"></div>
                            <div class="gallery-item"><img src="/company-photo3.jpg" alt="Photo 3"></div>
                            <div class="gallery-item"><img src="/company-photo4.jpg" alt="Photo 4"></div>
                            <div class="gallery-item"><img src="/company-photo5.jpg" alt="Photo 5"></div>
                        </div>
                    </div>
                </div>

            </div>
        </section>
    </div>

</template>

<script>
  import JobCard from './JobCard.vue'

export default {
    name: 'Company',
    components: {
      JobCard
    },
    data() {
      return {
        pageSize: 5,
        jobs: [
          {
            date: '04/25',
            title: '2025年早期預聘】儲備幹部',
            company: '宜得利家居股份有限公司',
            industry: '家具業',
            location: '台北市中正區',
            experience: '經歷不拘',
            education: '大學以上',
            salary: '月薪35,000~47,000元',
            benefits: ['年終獎金', '節日獎金/禮品', '員工優惠', '津貼/補助', '優於勞基法特休'],
            applicants: '30 人以上應徵',
            actionIcons: ['https://cdn.builder.io/api/v1/image/assets/11cf996c32eb40d1986fd0fd5ad9dc01/26800183c4e6034ee781a38725c95270d9a7214e?placeholderIfAbsent=true', 'https://cdn.builder.io/api/v1/image/assets/11cf996c32eb40d1986fd0fd5ad9dc01/8b7c23aa37dea21af10ae4522bedf47d9dac2483?placeholderIfAbsent=true']
          },
          // Duplicate job for the second listing
          {
            date: '04/25',
            title: '2025年早期預聘】儲備幹部',
            company: '宜得利家居股份有限公司',
            industry: '家具業',
            location: '台北市中正區',
            experience: '經歷不拘',
            education: '大學以上',
            salary: '月薪35,000~47,000元',
            benefits: ['年終獎金', '節日獎金/禮品', '員工優惠', '津貼/補助', '優於勞基法特休'],
            applicants: '30 人以上應徵',
            actionIcons: ['https://cdn.builder.io/api/v1/image/assets/11cf996c32eb40d1986fd0fd5ad9dc01/e8e7fb4bb4ce87067ea6a25a7c888a4f14ad2572?placeholderIfAbsent=true', 'https://cdn.builder.io/api/v1/image/assets/11cf996c32eb40d1986fd0fd5ad9dc01/ec4b9cd0d23733b2da02ac8fe18f393439c6d314?placeholderIfAbsent=true']
          }
        ]
      }
    },
    computed: {
    paginatedJobs() {
      return this.jobs.slice(0, this.pageSize);
    },
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
      console.log(avgColor)

      // 改變背景
      const contentEl = document.querySelector('.middle-content');
      contentEl.style.background = `linear-gradient(
                                    to bottom,
                                    ${avgColor} 0%,
                                    #121212 20%,
                                    #121212 100%
                                    )`;
    };
  }

}
</script>

<style scoped>
.middle-content {
  background-color: #121212;
  border-radius: 10px;
  color: white;
  box-sizing: border-box;
  font-family: 'Roboto', sans-serif;
  font-size: 14px;
}

/* company profile */
.company-profile {
  display: flex;
  width: 100%;
  flex-direction: column;
  padding: 40px 36px 28px 28px;
  overflow: hidden;
  background: transparent;
}

.profile-container {
  padding: 0;
}

.profile-grid {
  display: flex;
  gap: 20px;
  align-items: flex-end;
}

.logo-column {
  width: 239px;
}

.company-logo {
  box-shadow: 0px 0px 24px rgba(0, 0, 0, 0.25);
  height: 239px;
  overflow: hidden;
  display: flex;
  align-items: flex-end; /* 圖片貼底 */
}

.logo-image {
  width: 100%;
  object-fit: contain;
}

.info-column {
  width: 64%;
}

.company-info {
  color: #fff;
  font-family: Roboto, -apple-system, Roboto, Helvetica, sans-serif;
}

.info-label {
  font-size: 16px;
  font-weight: 500;
  letter-spacing: -0.32px;
}

.company-name {
  font-size: 40px;
  font-weight: 900;
  margin: 23px 0 0;
}

.company-tags {
  font-size: 20px;
  font-weight: 400;
  margin: 20px 0 0;
}

.job-count {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.18px;
  margin: 14px 0 0;
}
/* section title for 職缺＆關於*/
.section-title {
    font-family: 'Noto Sans', sans-serif;
    font-size: 32px;
    font-weight: 600;
    margin: 80px 0 30px;
}

/* job listings */
.job-listings {
  margin: 0;
  padding: 28px;
  background: transparent;
}

.listings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  color: #fff;
  font-family: Noto Sans, -apple-system, Roboto, Helvetica, sans-serif;
}

.page-size {
  display: flex;
  gap: 10px;
  border-radius: 40px;
  padding: 3px 12px 3px 3px;
  font-size: 18px;
  font-weight: 400;
  letter-spacing: -0.18px;
}

.size-text {
  margin: auto 0;
}

.arrow-icon {
  width: 16px;
  aspect-ratio: 1;
  object-fit: contain;
  margin: auto 0;
}

/*company information*/
.company-information {
  margin: 0;
  padding: 28px;
  background: transparent;
}

.cards {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  div h3 {
    font-family: 'Noto Sans', sans-serif;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 20px;
  }

  /* Info Cards */
  .info-card {
    background: rgba(255, 255, 255, 0.1);
    margin: 0;
    padding: 24px;
    border-radius: 10px;
  }

  .company-details {
    display: grid;
    grid-template-columns: 227px 1fr;
    gap: 30px;
  }

  .detail-group {
    margin-bottom: 50px;
  }

  .detail-item {
    margin-bottom: 20px;
  }

  .detail-item .label {
    font-size: 16px;
    font-weight: 600;
    font-family: 'Noto Sans', sans-serif;
  }

  .detail-item .value {
    font-size: 14px;
    color: #b3b3b3;
    margin-top: 5px;
  }

  .description {
    font-size: 16px;
    line-height: 1.6;
    color: #b3b3b3;
  }

  .benefits-section {
    background: rgba(255, 255, 255, 0.1);
    margin: 30px 40px;
    padding: 24px;
    border-radius: 10px;
  }

  .benefits-grid {
    display: grid;
    grid-template-columns: 227px 1fr;
    gap: 30px;
  }

  .benefit-tags h4 {
    font-family: 'Noto Sans', sans-serif;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 20px;
  }

  .benefit-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 20px;
  }

  .benefit-tag {
    background: rgba(179, 179, 179, 0.25);
    padding: 5px 10px;
    border-radius: 16px;
    font-size: 14px;
    width: fit-content;
  }

  .benefits-description {
    grid-column: span 2;
    margin-top: 30px;
  }

  .benefits-description h4 {
    font-size: 14px;
    color: #b3b3b3;
    margin-bottom: 10px;
  }

  .benefits-description .content {
    color: #b3b3b3;
    line-height: 1.6;
  }

  /* Gallery */
  .gallery {
    background: rgba(255, 255, 255, 0.1);
    margin: 0;
    padding: 24px;
    border-radius: 10px;
  }

  .gallery-scroll-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.gallery-grid {
  display: flex; /* 改用 flex 排列，讓子項目水平排列 */
  gap: 24px;
  width: max-content; /* 讓寬度隨內容撐開，超出時可滾動 */
  height: 200px;
  background: transparent;
  margin: 0;

}

.gallery-item {
  flex: 0 0 auto; /* 固定寬度，不縮放 */
  aspect-ratio: 3 / 2;
  background: transparent;
  box-shadow: 0 0 24px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

.gallery-item img {
  height: 100%;
  max-height: 200px;      
  width: auto;            
  object-fit: contain;     
  display: block;
}
</style>
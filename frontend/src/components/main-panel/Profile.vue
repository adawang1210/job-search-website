<template>
  <div class="middle-content" v-if="profile">
    <div class="container">
      <!-- 個人資料區 -->
      <section class="profile">
        <img :src="profile.profile.img" ref="avatar" alt="大頭照" class="avatar" />
        <div class="info">
          <h1>{{ profile.profile.user_name }}</h1>
          <p>{{ profile.profile.user_info }}</p>
        </div>
      </section>

      <!-- 編輯 icon -->
      <n-icon :size="30" class="edit-icon">
        <create-outline />
      </n-icon>

      <!-- 關於 -->
      <h2>關於</h2>
      <section class="about">
        <ul>
          <li><strong>姓名：</strong>{{ profile.about.user_name }}</li>
          <li><strong>年齡：</strong>{{ profile.about.age }}</li>
          <li><strong>性別：</strong>{{ profile.about.sex }}</li>
          <li><strong>學歷：</strong>{{ profile.about.education }}</li>
          <li><strong>手機：</strong>{{ profile.about.phone_number }}</li>
          <li><strong>信箱：</strong>{{ profile.about.mail }}</li>
          <li><strong>地址：</strong>{{ profile.about.address }}</li>
          <li><strong>語言：</strong>{{ profile.about.language }}</li>
        </ul>
      </section>

      <!-- 技能 -->
      <h2>技能</h2>
      <section class="skills">
        <ul>
          <li v-for="(skill, index) in profile.skills" :key="index">
            {{ skill.skill }}（熟練度：{{ skill.proficiency }}%）
          </li>
        </ul>
      </section>


      <!-- 簡介 -->
      <h2>履歷表</h2>
      <section class="intro">
        <h3><n-icon :size="25"><person-outline class="person-outline"/></n-icon> 簡介</h3>
        <p>{{ profile.resume.introduction }}</p>
      </section>

      <!-- 學歷 -->
      <section class="education timeline-section">
        <h3><n-icon :size="25"><school-outline class="school-outline"/></n-icon> 學歷</h3>
        <div class="timeline">
          <div class="timeline-segment" v-for="(edu, index) in profile.resume.education" :key="index">
            <div class="timeline-point">
              <span class="year-label">{{ edu.year_start }}</span>
              <div class="dot"></div>
            </div>
            <div class="timeline-line"></div>
            <div class="timeline-point">
              <span class="year-label">{{ edu.year_end }}</span>
              <div class="dot"></div>
            </div>
            <div class="timeline-entry">
              <h4>{{ edu.degree }}</h4>
              <p>{{ edu.content }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 工作經歷 -->
      <section class="experience timeline-section">
        <h3><nIcon :size="25"><BriefcaseOutline class="BriefcaseOutline"/></nIcon> 工作經歷</h3>
        <div class="timeline">
          <div class="timeline-segment" v-for="(work, index) in profile.resume.work_experience" :key="index">
            <div class="timeline-point">
              <span class="year-label">{{ work.year_start }}</span>
              <div class="dot"></div>
            </div>
            <div class="timeline-line"></div>
            <div class="timeline-point">
              <span class="year-label">{{ work.year_end }}</span>
              <div class="dot"></div>
            </div>
            <div class="timeline-entry">
              <h4>{{ work.job_title }}</h4>
              <p>{{ work.content }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 我的專案 -->
      <h2>我的專案</h2>
      <section class="projects">
        <div class="logo-scroll-container">
          <div v-for="(proj, index) in profile.projects" :key="index">
            <img :src="proj.img" :alt="proj.project_name" draggable="false">
            <p>{{ proj.project_name }}</p>
          </div>
        </div>
      </section>

      <!-- 已按讚 -->
      <h2>已按讚</h2>
      <section class="companies">
        <div class="logo-scroll-container">
          <div v-for="(liked, index) in profile.liked" :key="index">
            <img :src="liked.img" :alt="liked.company" draggable="false">
            <p>{{ liked.company }}</p>
          </div>
        </div>
      </section>

      <!-- 已追蹤 -->
      <h2>已追蹤</h2>
      <section class="technologies">
        <div class="logo-scroll-container">
          <div v-for="(person, index) in profile.following" :key="index">
            <img :src="person.img" :alt="person.name" draggable="false">
            <p>{{ person.name }}</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import { NIcon } from 'naive-ui';
import {
  CreateOutline,
  PersonOutline,
  SchoolOutline,
  BriefcaseOutline
} from '@vicons/ionicons5';
import {
  getUserProfile,
  getUserSkills,
  getUserEducation,
  getUserExperience,
  getUserProjects,
  getLikedCompanies,
  getFollowedUsers
} from '@/api/profile'; // 這裡的路徑依你的實際目錄結構調整


export default {
  name: 'Profile',
  components: {
    NIcon, 
    CreateOutline,
    PersonOutline,
    SchoolOutline,
    BriefcaseOutline
  },

  data() {
    return {
      profile: null
    };
  },

  methods: {
    handleImage(img) {
      if (!img) return;
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

      const contentEl = document.querySelector('.middle-content');
      contentEl.style.background = `linear-gradient(
        to bottom,
        ${avgColor} 0%,
        #2b2b2b 20%,
        #2b2b2b 100%
      )`;
    }
  },

  mounted() {
    Promise.all([
      getUserProfile(),
      getUserSkills(),
      getUserEducation(),
      getUserExperience(),
      getUserProjects(),
      //getLikedCompanies(),
      //getFollowedUsers()
    ])
      .then(([profileRes, skillsRes, educationRes, experienceRes, projectRes]) => {
      // ✅ 找出你要顯示的使用者資料（假設目前只抓 id=2）
      console.log('Profile Data:', profileRes);
      const userData = profileRes.find(user => user.id === 2) || {};

      this.profile = {
        profile: {
          img: '/default.jpg',
          user_name: userData.name,
          user_info: userData.city && userData.age && userData.gender
          ? `${userData.city} , ${userData.age} 歲 , ${userData.gender}`
          : ''
        },
        about: {
          user_name: userData.name,
          age: userData.age,
          sex: userData.gender,
          education: userData.highest_education,
          phone_number: userData.phone,
          mail: userData.email,
          address: userData.full_address,
          language: userData.languages
        },
        skills: userData.skills || [],
        resume: {
          introduction: userData.introduction || '',
          education: (userData.educations || []).map(item => ({
            year_start: item.start_date?.slice(0, 4),
            year_end: item.end_date?.slice(0, 4),
            degree: `${item.school}（${item.degree}）`,
            content: `${item.major} - ${item.description}`
          })),
          work_experience: (userData.work_experiences || []).map(item => ({
            year_start: item.start_date?.slice(0, 4),
            year_end: item.end_date?.slice(0, 4),
            job_title: item.job_title,
            content: item.description
          }))
        },
        projects: userData.projects || [],
        liked: [],
        following: []
      };

      this.$nextTick(() => {
        const img = this.$refs.avatar;
        if (img?.complete) {
          this.handleImage(img);
        } else if (img) {
          img.onload = () => this.handleImage(img);
        }
      });
    })
      .catch(error => {
        console.error('Error fetching profile data:', error);
      });
}
};
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
    font-weight: Bold;      /* 粗體 */
    font-size: 21px;       /* 字體大小 */
    letter-spacing: 1.1px; 
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
    cursor: pointer;
    margin: 0 0 12px auto;
    /* 自動靠右並與下方區塊有距離 */
    padding-right: 16px;
}


/* 編輯 icon hover 效果 */
.edit-icon:hover {
    opacity: 0.7;
}

.person-outline {
    position: relative;
    top: 5px; 
    right: 5px; 
}

.school-outline {
    position: relative;
    top: 5px; 
    right: 5px;
}

.BriefcaseOutline {
    position: relative;
    top: 5px; 
    right: 5px;
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



/* 隱藏橫向滾動條（僅針對 Webkit 瀏覽器：Chrome、Safari 等） */
.logo-scroll-container::-webkit-scrollbar {
    display: none;
}

/* 當滑鼠拖曳時，改變滑鼠指標樣式（手抓） */
.logo-scroll-container.dragging {
    cursor: grabbing;
    cursor: -webkit-grabbing;
}

/* Logo 區域的容器設置：水平排列、可滑動 */
.logo-scroll-container {
  display: flex;                           /* 使用 flex 排列橫向 */
  overflow-x: auto;                        /* 允許橫向滾動 */
  gap: 20px;                               /* 每個 logo 間距 */
  padding: 0px 0;                         /* 上下內距 */
  scroll-snap-type: x mandatory;          /* 啟用滾動吸附效果 */
  -webkit-overflow-scrolling: touch;      /* iOS 裝置平滑滾動 */
}

/* 設定每個 logo 項目的寬度 */
.logo-scroll-container > div {
  flex: 0 0 150px;                         /* 固定寬度 150px，不會縮放 */
  scroll-snap-align: start;               /* 滾動時對齊起始位置 */
  text-align: left;                     /* 文字置中 */
}

/* 每個 logo 圖片的樣式設定 */
.logo-scroll-container > div img {
  width: 100%;                            /* 填滿父容器寬度 */
  aspect-ratio: 1 / 1;                    /* 維持 1:1 的方形比例 */
  object-fit: cover;                      /* 填滿但不變形，裁切多餘 */
  border-radius: 5px;                    /* 圓角效果 */
  background-color: white;                /* 背景白色，若圖片透明就會顯示白底 */
}

/* logo 圖片下方的文字樣式 */
.logo-scroll-container > div p {
  margin-top: 6px;                        /* 與圖片的距離 */
  font-size: 15px;                        /* 字體大小 */
  color: white;                           /* 文字顏色白色 */
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

/* 我的專案 */
.projects {
  background: transparent;  /* 透明背景 */
  box-shadow: none;         /* 移除陰影（如果有） */
  border: none;
  border-radius: 0;
  margin-top: -25px;
  margin-left: -20px;
}


/* 已按讚 */
.companies {
  background: transparent;  /* 透明背景 */
  box-shadow: none;         /* 移除陰影（如果有） */
  border: none;
  border-radius: 0;
  margin-top: -25px;
  margin-left: -20px;
}

/* 已追蹤 */
.technologies {
  background: transparent;  /* 透明背景 */
  box-shadow: none;         /* 移除陰影（如果有） */
  border: none;
  border-radius: 0;
  margin-top: -25px;
  margin-left: -20px;
  overflow-x: auto;
}



</style>

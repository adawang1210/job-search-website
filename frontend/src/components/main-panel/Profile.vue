<template>
  <div class="middle-content" v-if="profile">
    <div class="container">
      

      <!-- 個人資料區 -->
      <section class="profile">
        <img :src="profile.profile.img" ref="avatar" alt="大頭照" class="avatar" />
        <div class="info">
          <h2>個人</h2>
          <h1>{{ profile.profile.user_name }}</h1>
          <p>{{ profile.profile.user_info }}</p>
        
        <br>
          <!-- 導覽列 -->
        <n-breadcrumb>
          <n-breadcrumb-item>
            <div class="breadcrumb-link" @click="scrollToSection('aboutSection')">
              <n-icon>
                <img :src="profileIcon" alt="profile icon" style="width: 16px; height: 16px;" />
              </n-icon>
              關於
            </div>
          </n-breadcrumb-item>
          <n-breadcrumb-item>
            <div class="breadcrumb-link" @click="scrollToSection('skillsSection')">
              <n-icon>
                <img :src="skillIcon" alt="skill icon" style="width: 16px; height: 16px;" />
              </n-icon>
              技能
            </div>
          </n-breadcrumb-item>
          <n-breadcrumb-item>
            <div class="breadcrumb-link" @click="scrollToSection('resumeSection')">
              <n-icon>
                <img :src="resumeIcon" alt="resume icon" style="width: 16px; height: 16px;" />
              </n-icon>
              履歷表
            </div>
          </n-breadcrumb-item>
        </n-breadcrumb>
        </div>

        <!-- 編輯 icon -->
        <n-icon :size="30" class="edit-icon">
          <create-outline />
        </n-icon>

    </section>

      <!-- 關於 -->
      <div class="about-container">
        <div class="title-with-icon">
          <h2>About 關於</h2>
        </div>
      </div>
      <section class="about" ref="aboutSection">
        <n-descriptions 
          label-placement="top"
          :column="4"
          :labelStyle="{ color: '#ffffff', fontSize: '18px', fontWeight: 'bold' }"
          :contentStyle="{ color: '#ffffff', fontSize: '16px' }"
        >
          <n-descriptions-item label="姓名">
            {{ profile.about.user_name }}
          </n-descriptions-item>
          <n-descriptions-item label="年齡">
            {{ profile.about.age }}
          </n-descriptions-item>
          <n-descriptions-item label="性別">
            {{ profile.about.sex }}
          </n-descriptions-item>
          <n-descriptions-item label="學歷">
            {{ profile.about.education }}
          </n-descriptions-item>
          <n-descriptions-item label="手機">
            {{ profile.about.phone_number }}
          </n-descriptions-item>
          <n-descriptions-item label="信箱">
            {{ profile.about.mail }}
          </n-descriptions-item>
          <n-descriptions-item label="地址">
            {{ profile.about.address }}
          </n-descriptions-item>
          <n-descriptions-item label="語言">
            {{ profile.about.language }}
          </n-descriptions-item>
        </n-descriptions>
      </section>

      <!-- 技能 -->
      <h2>Skills 技能</h2>
      <section class="skills" ref="skillsSection">
        <div class="skill-grid">
          <div v-for="(skill, index) in profile.skills" :key="index" class="skill-item">
            <div class="skill-icon">
              <n-icon size="32" color="#fff">
                <div v-if="skill.icon_svg" v-html="skill.icon_svg"></div>
                <svg v-else xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 32 32">
                  <!-- 默认图标 -->
                  <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 32 32"><path d="M30 30h-8V4h8zm-6-2h4V6h-4z" fill="currentColor"></path><path d="M20 30h-8V12h8zm-6-2h4V14h-4z" fill="currentColor"></path><path d="M10 30H2V18h8zm-6-2h4v-8H4z" fill="currentColor"></path></svg>  
                </svg>
              </n-icon>
            </div>
            <div class="skill-content">
              <div class="skill-name">{{ skill.skill }}</div>
              <div class="skill-proficiency">
                <n-number-animation
                  ref="numberAnimationRefs"
                  :from="0"
                  :to="skill.proficiency"
                  :active="isSkillsVisible"
                  :precision="0"
                  :duration="2000"
                />
                <span class="percent-sign">%</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 簡介 -->
      <h2>Resume 履歷表</h2>
      <section class="intro" ref="resumeSection">
        <h3><n-icon :size="25"><person-outline class="person-outline"/></n-icon> 簡介</h3>
        <p>{{ profile.resume.introduction }}</p>
      </section>

      <!-- 學歷 -->
      <section class="education timeline-section">
        <h3><n-icon :size="25"><school-outline class="school-outline"/></n-icon> 學歷</h3>
        <div class="timeline">
          <div class="timeline-segment" v-for="(edu, index) in profile.resume.education" :key="index">
            <div class="timeline-content">
              <div class="school-image" v-if="edu.school_image">
                <n-image
                  :src="edu.school_image"
                  object-fit="cover"
                  preview-disabled
                  class="square-image"
                />
              </div>
              <div class="timeline-right">
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
                  <div class="education-content">
                    <div class="education-info">
                      <h4>{{ edu.school }} {{ edu.major }} {{ edu.degree }}</h4>
                      <p class="description">{{ edu.description }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 工作經歷 -->
      <section class="experience timeline-section">
        <h3><nIcon :size="25"><BriefcaseOutline class="BriefcaseOutline"/></nIcon> 工作經歷</h3>
        <div class="timeline">
          <div class="timeline-segment" v-for="(work, index) in profile.resume.work_experience" :key="index">
            <div class="timeline-content">
              <div class="company-image" v-if="work.company_image">
                <n-image
                  :src="work.company_image"
                  object-fit="cover"
                  preview-disabled
                  class="square-image"
                />
              </div>
              <div class="timeline-right">
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
                  <div class="work-content">
                    <div class="work-info">
                      <h4>{{ work.company }} {{ work.title }}</h4>
                      <p class="description" style="white-space: pre-line">{{ work.description }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <h2>我的專案</h2>
      <section class="projects">
        <n-marquee :play-reversed="true" :auto-play="true" :interval="3000">
          <div class="project-group" v-for="(proj, index) in profile.projects" :key="index">
            <div class="project-item">
              <div class="project-cover">
                <n-image
                  width="160"
                  height="100"
                  :src="proj.cover_photo"
                  :alt="proj.title"
                  object-fit="contain"
                  class="project-image"
                />
              </div>
              <div class="project-title">{{ proj.title }}</div>
              <div class="tech-stack">
                <div class="tech-item" v-for="(tech, techIndex) in proj.technologies" :key="techIndex">
                  <n-image
                    width="40"
                    height="40"
                    :src="tech.icon"
                    :alt="tech.name"
                  />
                  <p>{{ tech.name }}</p>
                </div>
              </div>
            </div>
          </div>
        </n-marquee>
      </section>

      <!--isLiked 已按讚 -->
      <h2>Liked 已按讚</h2>
      <section class="companies">
        <div class="logo-scroll-container">
          <template v-if="filteredCompanies.length > 0">
            <div v-for="company in filteredCompanies" :key="company.id">
              <img :src="company.media?.logo" :alt="company.name" draggable="false">
              <p>{{ company.name }}</p>
            </div>
          </template>
          <template v-else>
            <div class="empty-state">
              <p>還沒有按讚的公司</p>
            </div>
          </template>
        </div>
      </section>
      
      <!-- 已追蹤 
      <h2>Following 已追蹤</h2>
      <section class="technologies">
        <div class="logo-scroll-container">
          <div v-for="(person, index) in profile.following" :key="index">
            <img :src="person.img" :alt="person.name" draggable="false">
            <p>{{ person.name }}</p>
          </div>
        </div>
      </section>-->
    </div>
    <Company 
      v-if="company" 
      :id="company.id" 
      @like-status-change="handleLikeStatusChange"
    />
  </div> 

</template>


<script>
import axios from 'axios';
import { NIcon, NDescriptions, NDescriptionsItem, useThemeVars, NStatistic, NNumberAnimation, NButton, NMarquee, NImage, NBreadcrumb, NBreadcrumbItem } from 'naive-ui';
import { ref, onMounted, nextTick, computed } from 'vue';
import {
  CreateOutline,
  PersonOutline,
  SchoolOutline,
  BriefcaseOutline
} from '@vicons/ionicons5';
import profileIcon from '@/assets/icons/profile-icon.svg';
import skillIcon from '@/assets/icons/skill-icon.svg';
import resumeIcon from '@/assets/icons/resume-icon.svg';
import aboutIcon from '@/assets/icons/about-icon.svg';
import {
  getUserProfile,
} from '@/api/profile';
import { getGreatCompanies } from '@/api/home';
import Company from './Company.vue';  // 確保已導入 Company 組件

export default {
  name: 'Profile',
  components: {
    NIcon, 
    CreateOutline,
    PersonOutline,
    SchoolOutline,
    BriefcaseOutline,
    NDescriptions,
    NDescriptionsItem,
    NStatistic,
    NNumberAnimation,
    NButton,
    NMarquee,
    NImage,
    NBreadcrumb,
    NBreadcrumbItem,
    Company
  },
  setup() {
    const themeVars = useThemeVars();
    const numberAnimationRefs = ref([]);
    const skillsSection = ref(null);
    const isSkillsVisible = ref(false);
    let observer = null;
    const aboutSection = ref(null);
    const resumeSection = ref(null);

    const initializeObserver = () => {
      if (!observer) {
        observer = new IntersectionObserver(
          (entries) => {
            entries.forEach((entry) => {
              console.log('Intersection ratio:', entry.intersectionRatio);
              console.log('Is intersecting:', entry.isIntersecting);
              if (entry.isIntersecting) {
                console.log('Animation triggered');
                isSkillsVisible.value = true;
              }
            });
          },
          {
            root: null,
            threshold: 0.1,
            rootMargin: '0px'
          }
        );
      }

      if (skillsSection.value) {
        console.log('Skills section mounted:', skillsSection.value);
        observer.observe(skillsSection.value);
        console.log('Observer started');
      }
    };

    onMounted(() => {
      console.log('Component mounted');
      initializeObserver();
    });

    // 监听 profile 数据变化
    const startObservation = () => {
      nextTick(() => {
        console.log('Profile data loaded, initializing observer');
        initializeObserver();
      });
    };

    const scrollToSection = (refName) => {
      const section = {
        aboutSection,
        skillsSection,
        resumeSection
      }[refName];

      if (section.value) {
        section.value.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        });
      }
    };

    return {
      themeVars,
      numberAnimationRefs,
      skillsSection,
      isSkillsVisible,
      startObservation,
      profileIcon,
      aboutIcon,
      skillIcon,
      resumeIcon,
      aboutSection,
      resumeSection,
      scrollToSection
    };
  },
  data() {
    return {
      profile: null,
      likedCompanies: [],
      isLoadingLikedCompanies: false,
      descriptionThemeOverrides: {
        itemTextColor: '#ffffff',
        labelTextColor: '#ffffff'
      },
      company: null,
      filteredCompanies: []
    };
  },
  computed: {
    filteredLikedCompanies() {
      return this.likedCompanies.filter(company => company.isLiked === true);
    }
  },
  methods: {
    handleImage() {
      // 使用固定的渐变背景
      const contentEl = document.querySelector('.middle-content');
      if (contentEl) {
        contentEl.style.background = `linear-gradient(
          to bottom,
          rgba(187, 187, 187, 0.8) 0%,
          #2b2b2b 20%,
          #2b2b2b 100%
        )`;
      }
    },
    async loadLikedCompanies() {
      this.isLoadingLikedCompanies = true;
      try {
        const response = await getGreatCompanies();
        const companies = response.results || response || [];
        // 更新 likedCompanies 數組
        this.likedCompanies = companies.map(company => ({
          ...company,
          isLiked: company.isLiked || false
        }));
        // 更新過濾後的公司列表
        this.filteredCompanies = this.likedCompanies.filter(company => company.isLiked);
      } catch (error) {
        console.error('Error fetching liked companies:', error);
      } finally {
        this.isLoadingLikedCompanies = false;
      }
    },
    // 新增更新公司按讚狀態的方法
    updateCompanyLikeStatus(companyId, isLiked) {
      const company = this.likedCompanies.find(c => c.id === companyId);
      if (company) {
        company.isLiked = isLiked;
      }
    },
    async loadProfileData() {
      try {
        const profileRes = await getUserProfile();
        const userData = profileRes.find(user => user.id === 2) || {};
        this.profile = {
          profile: {
            img: userData.picture || '/default.jpg',
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
              degree: item.degree,
              school: item.school,
              major: item.major,
              description: item.description,
              school_image: item.school_image
            })),
            work_experience: (userData.work_experiences || []).map(item => ({
              year_start: item.start_date?.slice(0, 4),
              year_end: item.end_date?.slice(0, 4),
              company: item.company,
              title: item.title,
              description: item.description,
              company_image: item.company_image
            }))
          },
          projects: userData.projects || [],
          liked: [],
          following: []
        };
        // 数据加载完成后初始化观察器
        this.startObservation();

        this.$nextTick(() => {
          const img = this.$refs.avatar;
          if (img?.complete) {
            this.handleImage();
          } else if (img) {
            img.onload = () => this.handleImage();
          }
        });
      } catch (error) {
        console.error('Error loading profile data:', error);
      }
    },
    // 處理公司按讚狀態變化
    handleLikeStatusChange({ companyId, isLiked }) {
      this.updateCompanyLikeStatus(companyId, isLiked);
    }
  },
  watch: {
    // 監聽 likedCompanies 中每個公司的 isLiked 狀態
    likedCompanies: {
      deep: true,
      handler(newCompanies) {
        // 當 likedCompanies 發生變化時，重新過濾已按讚的公司
        this.filteredCompanies = newCompanies.filter(company => company.isLiked);
      }
    }
  },
  async mounted() {
    await Promise.all([
      this.loadProfileData(),
      this.loadLikedCompanies()
    ]);
  }
};
</script>


<style scoped>


/* 覆蓋 naive-ui 描述列表樣式 */
.about :deep(.n-descriptions-item-label),
.about :deep(.n-descriptions-item-content),
.about :deep(.n-descriptions-item-content span),
.about :deep(.n-descriptions-item-content div),
.about :deep(.n-descriptions-item) {
  color: #ffffff !important;
}

.about :deep(.n-descriptions) {
  --n-label-text-color: #ffffff !important;
  --n-text-color: #ffffff !important;
  --n-font-color: #ffffff !important;
}

.about :deep(.n-descriptions-item-content),
.about :deep(.n-descriptions-item-label) {
  color: #ffffff !important;
}

.about :deep(.n-descriptions-item-content *) {
  color: #ffffff !important;
}

/* 面包屑导航样式 */
:deep(.n-breadcrumb) {
  margin-bottom: 24px;
  color: #ffffff !important;
}

:deep(.n-breadcrumb-item) {
  color: #ffffff !important;
}

:deep(.n-breadcrumb-item__link) {
  color: #ffffff !important;
}

:deep(.n-breadcrumb-item__link span) {
  color: #ffffff !important;
}

:deep(.n-breadcrumb-item a) {
  color: #ffffff !important;
}

:deep(.n-breadcrumb-item:last-child) {
  color: #ffffff !important;
}

:deep(.n-breadcrumb-item:last-child span) {
  color: #ffffff !important;
}

:deep(.n-breadcrumb .n-icon) {
  color: #ffffff !important;
  margin-right: 4px;
}

:deep(.n-breadcrumb-item__separator) {
  color: #ffffff !important;
}

/* 确保文字在任何情况下都是白色 */
:deep(.n-breadcrumb *) {
  color: #ffffff !important;
  text-shadow: none !important;
}

/* middle-content 區塊 */
.middle-content {
    width: 100%;
    max-width: 1005px;
    margin: 0 auto;   
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
    width: 100%;
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

.profile .info h2 {
    margin: 0;
    margin-top: -10px;
    margin-bottom: -10px;
    font-size: 15px;
    font-weight: bold;
    color: rgba(255, 255, 255, 0.5);
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
    margin: 0 0 -150px auto;
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
    color: #ffffff;
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
.skills {
  padding: 30px;
}

.skill-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.skill-item {
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 8px;
  transition: all 0.3s ease;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 20px;
  min-height: 140px;
}

.skill-item:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

.skill-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 80px;
  width: 60px;
}

.skill-icon :deep(svg) {
  width: 60px;
  height: 60px;
}

.skill-content {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
  padding: 5px 0;
}

.skill-name {
  color: #ffffff !important;
  font-size: 18px;
  font-weight: 500;
}

.skill-proficiency {
  color: #ffffff !important;
  font-size: 40px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 4px;
}

.percent-sign {
  font-size: 28px;
  margin-left: 4px;
}

/* 覆盖 naive-ui 数字动画组件样式 */
:deep(.n-number-animation) {
  color: #ffffff !important;
  font-size: 36px !important;
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
  background: transparent;
  box-shadow: none;
  border: none;
  border-radius: 0;
  margin-top: -25px;
  margin-left: -20px;
  padding: 20px;
  height: 200px;
  overflow: hidden;
}

.project-group {
  display: inline-flex;
  margin-right: 30px;
  height: 200px;
}

.project-item {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 12px;
  width: 200px;
  height: 180px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  box-sizing: border-box;
}

.project-cover {
  width: 170px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 4px;
  margin: 0 auto;
  overflow: hidden;
  box-sizing: border-box;
}

.project-image {
  width: 160px;
  height: 90px;
  object-fit: contain !important;
}

.project-cover :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: contain !important;
  padding: 5px;
  box-sizing: border-box;
}

.project-title {
  font-size: 15px;
  font-weight: bold;
  color: white;
  text-align: center;
  margin: 0;
  padding: 0;
}

.tech-stack {
  display: flex;
  gap: 8px;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  margin: 0;
  padding: 0;
}

.tech-item {
  text-align: center;
}

.tech-item p {
  margin-top: 2px;
  font-size: 11px;
  color: white;
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

:deep(.n-marquee) {
  height: 200px !important;
}

:deep(.n-marquee-content) {
  height: 200px !important;
}

:deep(.n-marquee__slides) {
  height: 200px !important;
}

/* 添加麵包屑連結樣式 */
.breadcrumb-link {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.breadcrumb-link:hover {
  opacity: 0.8;
}

.education-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  width: 100%;
}

.education-info {
  flex: 1;
}

.school-image-container {
  width: 200px;
  height: 150px;
  border-radius: 8px;
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0.1);
}

.school-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.school-image:hover {
  transform: scale(1.05);
}

.timeline-content {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.school-image {
  width: 120px;
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.square-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.timeline-right {
  flex: 1;
  position: relative;
}

.company-image {
  width: 120px;
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.work-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  width: 100%;
}

.work-info {
  flex: 1;
}

.work-info h4 {
  margin-bottom: 12px;
}

.work-info .description {
  color: #ffffff;
  line-height: 1.6;
}

.about-container {
  margin-bottom: 0px;
}

.title-with-icon {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-with-icon h2 {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
  color: #ffffff;
}

.title-with-icon .n-icon {
  display: flex;
  align-items: center;
}

/* 移除 about section 的上邊距 */
.about {
  margin-top: -30px;
  padding-top: 15px;
}

</style>



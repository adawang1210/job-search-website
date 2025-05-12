<template>
  <div class="middle-content">
    <section class="recommend" v-for="(section, index) in sections" :key="index">
      <h1>{{ section.title }}</h1>
      <div class="recommend-content" 
           @mousedown="startDrag" 
           @mousemove="onDrag" 
           @mouseup="stopDrag"
           @mouseleave="stopDrag"
           :class="{ active: isDragging }">
        <div class="content-wrapper" v-for="(job, jobIndex) in section.jobs" :key="jobIndex">
          <div class="content-container">
            <p class="title">{{ job.title }}</p>
            <p class="info">{{ job.location }}</p>
            <p class="info salary-and-like">
              {{ job.salary }}
              <button type="button" 
                      class="like-btn" 
                      :class="{ active: job.isLiked }"
                      @click="toggleLike(section.title, jobIndex)">
                <i class="fa-regular fa-heart"></i>
              </button>
            </p>
          </div>
          <p class="company-name">{{ job.company }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'MainPanel',
  data() {
    return {
      isDragging: false,
      startX: 0,
      scrollLeft: 0,
      sections: [
        {
          title: '為你推薦',
          jobs: [
            {
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false
            },
            {
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false
            },
            {
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false
            },
            {
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false
            },
            {
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false
            }
          ]
        },
        {
          title: '熱門職缺',
          jobs: [
            {
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false
            },
            {
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false
            },
            {
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false
            },
            {
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false
            },
            {
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false
            }
          ]
        },
        {
          title: '熱門職缺',
          jobs: [
            {
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false
            },
            {
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false
            },
            {
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false
            },
            {
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false
            },
            {
              title: '水電半技師、學徒',
              location: '台中市烏日區',
              salary: '月薪33,000元以上',
              company: '百皇電氣工程有限公司',
              isLiked: false
            }
          ]
        }
      ]
    }
  },
  methods: {
    toggleLike(sectionTitle, jobIndex) {
      const section = this.sections.find(s => s.title === sectionTitle);
      if (section) {
        section.jobs[jobIndex].isLiked = !section.jobs[jobIndex].isLiked;
      }
    },
    startDrag(e) {
      this.isDragging = true;
      this.startX = e.pageX - e.currentTarget.offsetLeft;
      this.scrollLeft = e.currentTarget.scrollLeft;
    },
    onDrag(e) {
      if (!this.isDragging) return;
      e.preventDefault();
      const x = e.pageX - e.currentTarget.offsetLeft;
      const walk = (x - this.startX) * 2;
      e.currentTarget.scrollLeft = this.scrollLeft - walk;
    },
    stopDrag() {
      this.isDragging = false;
    }
  }
}
</script>

<style scoped>
.middle-content {
    display: flex;
    flex: 1;
    flex-direction: column;
    background-color: #383333;
    max-width: 100%;
    height: calc(100vh - 72px);
    border-radius: 10px;
    color: white;
    box-sizing: border-box;
    overflow-x: hidden;
    overflow-y: auto;
    position: fixed;
    top: 72px;
    left: 272px;
    right: 16px;
    padding: 16px;
}

.middle-content .recommend {
    display: flex;
    flex-direction: column; 
    overflow-x: hidden;
    white-space: nowrap;
    gap: 8px;
    padding: 0px 25px;
}

.middle-content .recommend .recommend-content .content-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
}

.middle-content .recommend-content {
    display: flex;
    flex-direction: row;
    gap: 25px;
    overflow-x: auto;
    max-width: 100%;
    box-sizing: border-box;
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
    cursor: grab;
    scrollbar-width: none;
    -ms-overflow-style: none;
}

.middle-content .recommend .content-container {
    display: inline-block;
    width: 180px;
    background-color: #594f4f;
    border-radius: 5px;
    box-sizing: border-box;
}

.middle-content .recommend h1 {
    font-size: 18px;
}

.middle-content .recommend .content-container .title {
    font-size: 12px;
    margin: 6px 15px 4px 15px;
}

.middle-content .recommend .content-container .info {
    font-size: 10px;
    margin: 0px 8px -3px 15px;
}

.middle-content .recommend .recommend-content .content-wrapper .company-name {
    font-size: 12px;
    color: white;
    margin-top: 4px;
    text-align: center;
}

.middle-content .recommend .content-container .salary-and-like {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 3px;
}

.middle-content .recommend .content-container .like-btn {
    border: none;
    background: none;
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: transform 0.5s ease;
}

.middle-content .recommend .content-container .like-btn:hover {
    transform: scale(1.1);
}

.middle-content .recommend .content-container .like-btn.active {
    color: #ff9f9f;
}

.middle-content .recommend-content.active {
    cursor: grabbing;
    user-select: none;
}

.recommend-content::-webkit-scrollbar {
    display: none;
}
</style> 
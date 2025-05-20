import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import 'vfonts/Lato.css' // 主字體
import 'vfonts/FiraCode.css' // 程式碼字體

import { library } from '@fortawesome/fontawesome-svg-core'
import { faHouse, faCaretDown, faMagnifyingGlass , faChevronLeft , faChevronRight,  faHeart as fasHeart, faTimes } from '@fortawesome/free-solid-svg-icons'
import { faHeart as farHeart } from '@fortawesome/free-regular-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'


library.add(faHouse, faCaretDown, faMagnifyingGlass, faChevronLeft, faChevronRight, fasHeart, farHeart, faTimes)


const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')

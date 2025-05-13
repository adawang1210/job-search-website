import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import 'vfonts/Lato.css' // 主字體
import 'vfonts/FiraCode.css' // 程式碼字體


const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

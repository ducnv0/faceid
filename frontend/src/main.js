import { createApp } from 'vue'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import axios from 'axios'

import App from './App.vue'
import router from './router'
import { settings } from './env'
import store from './store'

const app = createApp(App)

axios.defaults.baseURL = settings.API_DOMAIN

app.use(router)
app.use(store)
app.mount('#app')

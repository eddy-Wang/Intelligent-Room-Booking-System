import { createApp } from 'vue'
import App from './App.vue'
import router from "@/router/index.js";

const app = createApp(App)

app.config.globalProperties.$user = {
    email: "",
    name: "",
    permission: ""
}

app.use(router).mount('#app')


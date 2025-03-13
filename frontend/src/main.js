import router from './router'
import {createApp} from "vue";
import App from "@/App.vue";
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';

// about Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

// about SvgIcon
import SvgIcon from '@jamescoyle/vue-icon';
import * as mdijs from '@mdi/js';

// create instance of vuetify
const vuetify = createVuetify({
    icons: {
      defaultSet: 'mdi',
      aliases,
      sets: { mdi },
    },
  })

const app = createApp(App)

app.config.globalProperties.$user = {
  email: '',
  name: '',
  permission: '',
};

// use vuetify and router
app.use(vuetify)
app.use(router)
app.use(ElementPlus);

// mount svgicon globally
app.component('SvgIcon', SvgIcon)
app.config.globalProperties.$mdi = mdijs


app.mount('#app')
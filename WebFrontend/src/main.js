import { createApp } from 'vue'
import App from './App.vue'
import './assets/css/custom.css'
import 'bootstrap';
import router from "./router";
import axios from "axios";

const axiosInstance = axios.create()

const app = createApp(App);
app.use(router);
app.config.globalProperties.$axios = axiosInstance
app.mount("#app");

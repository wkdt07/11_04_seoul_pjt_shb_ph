import { createApp } from "vue";
import { createPinia } from "pinia";
import {useKakao} from 'vue3-kakao-maps/@utils'
import App from "./App.vue";
import router from "./router";

const apiKey = 'cfc4774e038a259fabadb213a3fe70a7'
const kakaoMap = useKakao(apiKey,['clusterer', 'services', 'drawing'])
const app = createApp(App);

app.use(createPinia());
app.use(router);

app.mount("#app");

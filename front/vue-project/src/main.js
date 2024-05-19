import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { useKakao } from 'vue3-kakao-maps/@utils'

// API 키와 필요한 라이브러리를 사용하여 카카오 지도 초기화
const mapApiKey = 'cfc4774e038a259fabadb213a3fe70a7';
useKakao(mapApiKey, ['clusterer', 'services', 'drawing']);

const app = createApp(App);

// 지속성 플러그인을 적용하여 Pinia 생성 및 설정
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

// Pinia 스토어와 라우터를 사용하고 앱 마운트
app.use(pinia);
app.use(router);
app.mount("#app");

<!-- <template>

  <div>
    <RouterView />

  </div>
</template>

<script setup>
  import { RouterView, RouterLink } from 'vue-router'
  import { useCounterStore } from '@/stores/counter';
  import { useRouter } from 'vue-router';
  import Map from '@/components/Map.vue'
  // import Map from './components/Map.vue';
  
  const store = useCounterStore()
  const router = useRouter()
  const logOut=function(){
    store.logOut()
    router.push({name:'LoginView'})
  }
  
  console.log(store.userInfo)
  
  // if (store.isLogin) {
  //   store.getUserInfo(); 
  // }
</script>

<style scoped>

</style> -->


<template>
  <div>
    <!-- 기존 헤더 주석 처리 -->
    <!-- <header>
      <nav>
        <RouterLink :to="{ name: 'ArticleView'}">Articles</RouterLink><hr>
        <RouterLink :to="{ name: 'SignUpView'}">SignUpPage</RouterLink><hr>
        <RouterLink :to="{ name: 'LoginView'}">LoginPage</RouterLink><hr>
        <RouterLink :to="{name:'MapView'}">Map</RouterLink><hr>
        <RouterLink :to="{name:'DepositListView'}">금리비교</RouterLink><hr>
        <RouterLink :to="{name:'ExchangeView'}">환율계산기</RouterLink><hr>
        <RouterLink v-if="store.userInfo" :to="{name:'ProfileView',params:{username:store.userInfo.username}}" >
        {{ store.userInfo.username }}의 프로필</RouterLink> <hr>

        <button v-if="store.isLogin" @click.prevent="logOut">로그아웃</button>
      </nav>
    </header> -->

    <!-- Carousel Component -->
    <div class="carousel">
      <div class="carousel-track-container">
        <ul class="carousel-track" :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
          <li class="carousel-slide" v-for="(slide, index) in slides" :key="index">
            <img :src="slide.img" :alt="slide.alt" @click="navigateTo(slide.view)" class="carousel-image">
          </li>
        </ul>
      </div>
    </div>

    <div class="carousel-nav">
      <button class="carousel-button carousel-button--left" @click="prevSlide">&lt;</button>
      <button class="carousel-button carousel-button--right" @click="nextSlide">&gt;</button>
    </div>

    <RouterView />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { RouterView, RouterLink } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import { useRouter } from 'vue-router';
import Map from '@/components/Map.vue';

// 이미지 파일 임포트
import carousel1 from '@/assets/carousel1.png';
import carousel2 from '@/assets/carousel2.png';
import carousel3 from '@/assets/carousel3.png';

const store = useCounterStore();
const router = useRouter();

const logOut = () => {
  store.logOut();
  router.push({ name: 'LoginView' });
};

const navigateTo = (view) => {
  router.push({ name: view });
};

const currentSlide = ref(0);

const slides = [
  {
    img: carousel1,
    alt: 'carousel1',
    view: 'CompareView',
  },
  {
    img: carousel2,
    alt: 'carousel2',
    view: 'ExchangeView',
  },
  {
    img: carousel3,
    alt: 'carousel3',
    view: 'MapView',
  }
];

const prevSlide = () => {
  if (currentSlide.value > 0) {
    currentSlide.value--;
  } else {
    currentSlide.value = slides.length - 1;
  }
};

const nextSlide = () => {
  if (currentSlide.value < slides.length - 1) {
    currentSlide.value++;
  } else {
    currentSlide.value = 0;
  }
};

console.log(store.userInfo);
</script>

<style scoped>
/* 기본 스타일 제거 */

/* Carousel Styles */
.carousel {
  position: relative;
  width: 100%;
  overflow: hidden;
}

.carousel-track-container {
  overflow: hidden;
}

.carousel-track {
  display: flex;
  transition: transform 0.5s ease-in-out;
}

.carousel-slide {
  min-width: 100%;
  box-sizing: border-box;
}

.carousel-image {
  width: 100%;
  cursor: pointer;
}

.carousel-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  z-index: 10;
}

.carousel-button--left {
  left: 10px;
}

.carousel-button--right {
  right: 10px;
}
</style>

  <!--

    <script setup>
    import { RouterView, RouterLink } from 'vue-router'
    import { useCounterStore } from './stores/counter';
    import { useRouter } from 'vue-router';
    import Map from '@/components/Map.vue'
    // import Map from './components/Map.vue';
    
    const store = useCounterStore()
    const router = useRouter()
    const logOut=function(){
      store.logOut()
      router.push({name:'home'})
    }
    
    console.log(store.userInfo)
    
    // // if (store.isLogin) {
      // //   store.getUserInfo(); 
      // // }
      
      import MainPage from './components/MainPage.vue';
    </script>
    
    <template>
    -->
      <!-- <MainPage/> -->
      <!--

        <header>
          <nav>
            <RouterLink :to="{name:'home'}">MainPage</RouterLink><hr>
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
          </header>
          
          <RouterView />
        -->
          <!-- v-if="store.isLogin && store.userInfo"  -->
          <!-- <RouterView/> -->
        <!-- </template>

<style scoped>
  
</style> -->

<!-- 
<script setup>
import { RouterView, RouterLink } from 'vue-router'
import { useCounterStore } from './stores/counter';
import { useRouter } from 'vue-router';
import Map from '@/components/Map.vue'

const store = useCounterStore()
const router = useRouter()
const logOut = function(){
  store.logOut()
  router.push({name:'home'})
}

console.log(store.userInfo)
</script>

<template>
  <header class="-01">
    <nav class="-01">
      <div class="peek_logo_only-removebg-preview-2"></div>
      <RouterLink class="Peek" :to="{name:'home'}">MainPage</RouterLink>
      <RouterLink class="Peek" :to="{ name: 'ArticleView'}">Articles</RouterLink>
      <RouterLink class="Peek" :to="{ name: 'SignUpView'}">SignUpPage</RouterLink>
      <RouterLink class="Peek" :to="{ name: 'LoginView'}">LoginPage</RouterLink>
      <RouterLink class="Peek" :to="{name:'MapView'}">Map</RouterLink>
      <RouterLink class="Peek" :to="{name:'DepositListView'}">금리비교</RouterLink>
      <RouterLink class="Peek" :to="{name:'ExchangeView'}">환율계산기</RouterLink>
      <RouterLink class="Peek" v-if="store.userInfo" :to="{name:'ProfileView',params:{username:store.userInfo.username}}">
        {{ store.userInfo.username }}의 프로필
      </RouterLink>
      <button class="Rectangle-2" v-if="store.isLogin" @click.prevent="logOut">로그아웃</button>
    </nav>
  </header>

  <RouterView />
</template>

<style scoped>
.-01 {
  width: 1536px;
  height: 70px;
  padding: 10px 20px 14px 39px;
  background-color: #fff;
  display: flex;
  align-items: center;
}

.Peek {
  margin: 0 10px;
  font-family: Maplestory;
  font-size: 25px;
  font-weight: bold;
  line-height: 1.51;
  color: #001e44;
}

.Rectangle-2 {
  width: 125px;
  height: 40px;
  margin: 5px;
  border-radius: 5px;
  background-color: #f5f5f5;
}

.peek_logo_only-removebg-preview-2 {
  width: 45px;
  height: 45.3px;
  margin-right: 10px;
}
</style> -->

<script setup>
import { RouterView, RouterLink } from 'vue-router'
import { useCounterStore } from './stores/counter';
import { useRouter } from 'vue-router';

const store = useCounterStore()
const router = useRouter()
const goBack = ()=>{
  router.go(-1)
}
const logOut = function(){
  store.logOut()
  router.push({name:'home'})
}
const ImgURL = `${store.DJANGO_URL}/media/images/logo.png`
console.log(ImgURL)
console.log(store.userInfo)
</script>

<template>
  <header class="navbar">
    <div class="navbar-content">
      <RouterLink :to="{name:'home'}">
        <img class="logo" :src="ImgURL" alt="Peek Logo">
      </RouterLink>
        <span class="peek-title">PEEK!</span>
      <nav class="nav-links">
        <!-- <RouterLink class="nav-link" :to="{name:'home'}">MainPage</RouterLink> -->
        <RouterLink class="nav-link" :to="{ name: 'ArticleView'}">Articles</RouterLink>
        <RouterLink class="nav-link" :to="{ name: 'SignUpView' }" v-if="!store.isLogin">SignUpPage</RouterLink>
        <RouterLink class="nav-link" :to="{ name: 'LoginView'}" v-if="!store.isLogin">LoginPage</RouterLink>
        <RouterLink class="nav-link" :to="{name:'MapView'}">Map</RouterLink>
        <RouterLink class="nav-link" :to="{name:'CompareView'}">금리비교</RouterLink>
        
        <!-- <RouterLink class="nav-link" :to="{name:'SavingListView'}">적금테스트</RouterLink> -->

        <RouterLink class="nav-link" :to="{name:'ExchangeView'}">환율계산기</RouterLink>

        <RouterLink class="nav-link" v-if="store.userInfo" :to="{name:'ProfileView',params:{username:store.userInfo.username}}">
          {{ store.userInfo.username }}의 프로필
        </RouterLink>
      </nav>
      <div class="user-actions">
        <button class="logout-button" v-if="store.isLogin" @click.prevent="logOut">로그아웃</button>
      </div>
      <div class="user-actions">

        <button class="logout-button"@click.prevent="goBack">뒤로가기</button>
      </div>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
.navbar {
  width: 100%;
  background-color: #fff;
  padding: 10px 20px;
  border-bottom: 1px solid #e0e0e0;
}

.navbar-content {
  display: flex;
  align-items: center;
}

.logo {
  width: 45px;
  height: 45px;
  margin-right: 10px;
}

.peek-title {
  font-family: Maplestory;
  font-size: 25px;
  font-weight: bold;
  color: #001e44;
  margin-right: auto;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  font-family: NEXONLv1GothicLowOTF;
  font-size: 16px;
  color: #001c43;
  text-decoration: none;
}

.nav-link:hover {
  text-decoration: underline;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logout-button {
  width: 125px;
  height: 40px;
  border-radius: 5px;
  background-color: #f5f5f5;
  border: none;
  cursor: pointer;
}

.logout-button:hover {
  background-color: #e0e0e0;
}
</style>


<!-- <script setup>
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
       <RouterLink class="nav-link" :to="{name:'home'}">MainPage</RouterLink>
        <RouterLink class="nav-link" :to="{ name: 'ArticleView'}">Articles</RouterLink>
        <RouterLink class="nav-link" :to="{ name: 'SignUpView' }" v-if="!store.isLogin">SignUpPage</RouterLink>
        <RouterLink class="nav-link" :to="{ name: 'LoginView'}" v-if="!store.isLogin">LoginPage</RouterLink>
        <RouterLink class="nav-link" :to="{name:'MapView'}">Map</RouterLink>
        <RouterLink class="nav-link" :to="{name:'CompareView'}">금리비교</RouterLink>
        
        

        <RouterLink class="nav-link" :to="{name:'ExchangeView'}">환율계산기</RouterLink>

        <RouterLink class="nav-link" v-if="store.userInfo" :to="{name:'ProfileView',params:{username:store.userInfo.username}}">
          {{ store.userInfo.username }}의 프로필
        </RouterLink>
        <div class="user-actions">

  <RouterLink class="button-link" :to="{ name: 'SignUpView' }" v-if="!store.isLogin">회원가입</RouterLink>
  <RouterLink class="button-link" :to="{ name: 'LoginView'}" v-if="!store.isLogin">로그인</RouterLink>
  <button class="logout-button" v-if="store.isLogin" @click.prevent="logOut">로그아웃</button>
  <button class="logout-button" @click.prevent="goBack">뒤로가기</button>
</div>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>

.button-link {
  display: inline-block;
  padding: 10px 20px;
  margin: 0 5px;
  border-radius: 5px;
  background-color: #007bff;
  color: #fff;
  text-align: center;
  text-decoration: none;
}

.button-link:hover {
  background-color: #0056b3;
}
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
 -->
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
     <div class="logo-container">
       <RouterLink :to="{ name: 'home' }">
         <img class="logo" :src="ImgURL" alt="Peek Logo">
       </RouterLink>
       <span class="peek-title">EEK!</span>
     </div>
     <div class="nav-links-container">
       <nav class="nav-links">
         <RouterLink class="nav-link" :to="{ name: 'ArticleView' }">유저게시판</RouterLink>
         <RouterLink class="nav-link" :to="{ name: 'MapView' }">은행 점포 검색</RouterLink>
         <RouterLink class="nav-link" :to="{ name: 'CompareView' }">금리비교</RouterLink>
         <RouterLink class="nav-link" :to="{ name: 'ExchangeView' }">환율계산기</RouterLink>
         <RouterLink class="nav-link" :to="{ name: 'RealEstateView' }">부동산 데이터</RouterLink>
         <RouterLink class="nav-link" v-if="store.userInfo"
           :to="{ name: 'ProfileView', params: { username: store.userInfo.username } }">
           {{ store.userInfo.username }}의 프로필
         </RouterLink>
       </nav>
     </div>
     <div class="user-actions">
       <RouterLink class="button-link" :to="{ name: 'SignUpView' }" v-if="!store.isLogin">회원가입</RouterLink>
       <RouterLink class="button-link" :to="{ name: 'LoginView' }" v-if="!store.isLogin">로그인</RouterLink>
       <button class="button-link" v-if="store.isLogin" @click.prevent="logOut">로그아웃</button>
       <button class="button-link" @click.prevent="goBack">뒤로가기</button>
     </div>
   </header>
   <RouterView />
 </template>
 
 
 <style scoped>
 @font-face {
   font-family: 'NEXON Lv1 Gothic Low OTF';
   src: url('@/assets/fonts/NEXON_Lv1_Gothic_Low.otf') format('opentype');
 }
 
 @font-face {
   font-family: 'Maplestory';
   src: url('@/assets/fonts/Maplestory.otf') format('opentype');
 }
 
 .navbar {
   width: 100%;
   background-color: #fff;
   padding: 10px 20px;
   border-bottom: 1px solid #e0e0e0;
   box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
   display: flex;
   align-items: center;
   justify-content: space-between;
 }
 
 .logo-container {
   display: flex;
   align-items: center;
 }
 
 .logo {
   width: 45px;
   height: 45px;
   margin-right: 10px;
 }
 
 .peek-title {
   font-family: 'Maplestory';
   font-size: 25px;
   font-weight: bold;
   color: #001e44;
   margin: 0;
   display: flex;
   align-items: center;
 }
 
 .nav-links-container {
   display: flex;
   justify-content: center;
   flex: 1;
 }
 
 .nav-links {
   display: flex;
   gap: 20px;
   align-items: center;
 }
 
 .nav-link {
   font-family: 'NEXON Lv1 Gothic Low OTF';
   font-size: 16px;
   color: #001c43;
   text-decoration: none;
   padding: 5px 10px;
   border-radius: 5px;
   transition: background-color 0.3s ease, color 0.3s ease;
   font-weight: bold;
 }
 
 .nav-link:hover {
   background-color: #2db2ff;
   color: white;
 }
 
 .user-actions {
   display: flex;
   align-items: center;
   gap: 10px;
   margin-right: 20px;
   /* 우측 끝에서 조금 들여넣기 */
 }
 
 .button-link {
   display: inline-block;
   padding: 10px 20px;
   background-color: #007bff;
   color: #fff;
   border: none;
   border-radius: 5px;
   text-align: center;
   text-decoration: none;
   font-family: 'NEXON Lv1 Gothic Low OTF';
   font-size: 14px;
   cursor: pointer;
   transition: background-color 0.3s ease;
 }
 
 .button-link:hover {
   background-color: #0056b3;
 }
 </style>
 
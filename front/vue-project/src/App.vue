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
    router.push({name:'LogInView'})
  }

  console.log(store.userInfo)
  
  // if (store.isLogin) {
  //   store.getUserInfo(); 
  // }
  
  </script>
  
<template>
  <header>
    <nav>
      <RouterLink :to="{ name: 'ArticleView'}">Articles</RouterLink><hr>
      <RouterLink :to="{ name: 'SignUpView'}">SignUpPage</RouterLink><hr>
      <RouterLink :to="{ name: 'LogInView'}">LogInPage</RouterLink><hr>
      <RouterLink :to="{name:'MapView'}">Map</RouterLink><hr>
      <RouterLink :to="{name:'DepositListView'}">금리비교</RouterLink><hr>
      <RouterLink :to="{name:'ExchangeView'}">환율계산기</RouterLink><hr>
      <RouterLink v-if="store.userInfo" :to="{name:'ProfileView',params:{username:store.userInfo.username}}" >
      {{ store.userInfo.username }}의 프로필</RouterLink> <hr>

      
      <button v-if="store.isLogin" @click.prevent="logOut">로그아웃</button>
      
    </nav>
  </header>
  <!-- <Map/> -->
  <RouterView />
  <!-- v-if="store.isLogin && store.userInfo"  -->

</template>

<!-- <script setup>
import { RouterView, RouterLink } from 'vue-router'
import { useCounterStore } from './stores/counter';
import { useRouter } from 'vue-router';
import Map from '@/components/Map.vue'
// import Map from './components/Map.vue';

const store = useCounterStore()
const router = useRouter()
const logOut=function(){
  store.logOut()
  router.push({name:'LogInView'})
}
</script> -->

<style scoped>

</style>

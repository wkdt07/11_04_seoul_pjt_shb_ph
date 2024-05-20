<!-- <template>
  <div>
    {{ user }}
    <h1 v-if="user">{{ user.username }} 프로필 페이지</h1>
    <p v-if="user">이름: {{ user.name }}</p>
    <p v-if="user">이메일: {{ user.email }}</p>
    <p v-if="user">나이: {{ user.age }}</p>
    <p v-if="user">현재 자산: {{ user.now_money }}</p>
    <p v-if="user">연봉: {{ user.money_per_year }}</p>
    <p v-if="user">선호 장소: {{ user.fav_place }}</p>
    <img :src="user.profile_img" alt="Profile Image" v-if="user && user.profile_img">

    <h2 v-if="user && user.contract_deposit">계약된 예금</h2>
    <ul v-if="user && user.contract_deposit">
      <li v-for="deposit in user.contract_deposit" :key="deposit.id">{{ deposit.name }}</li>
    </ul>

    <h2 v-if="user && user.contract_saving">계약된 적금</h2>
    <ul v-if="user && user.contract_saving">
      <li v-for="saving in user.contract_saving" :key="saving.id">{{ saving.name }}</li>
    </ul>-->

    <!-- <h2 v-if="userArticles && userArticles.length">작성한 글</h2> -->
    <!-- <h2 v-if="userArticles">작성한 글</h2>
    <ul v-if="userArticles && userArticles.length">
      <li v-for="article in userArticles" :key="article.id">
      <h2>{{article.title}}</h2>
      <p>{{ article.content }}</p>
      <br>
      </li>
    </ul>

    <h2 v-if="userComments">작성한 댓글</h2>
    <ul v-if="userComments">
      <li v-for="comment in userComments" :key="comment.id">
        <h2>{{ articleTitle(comment.article) }}에 달린 댓글</h2>
        {{ comment.content }}</li>
        <br>
    </ul>

    <p v-if="error">{{ error }}</p>
    <p v-if="loading">로딩 중...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const route = useRoute();
const store = useCounterStore();
const user = ref(null);
const userArticles = ref([]);
const userComments = ref([]);
const error = ref(null);
const loading = ref(false);

// 우선적으로 처리
const fetchUserInfo = async () => {
  loading.value = true;
  error.value = null;
  try {
    // await store.getUserInfo(route.params.username);
    const username = route.params.username
    await store.getUserInfo(username)
    user.value = store.userInfo;
  

    if (user.value) {
      console.log('유저는',user.value)
      // console.log('유저 타겟은',user.value.target)
      await store.getUserArticles(user.value.id);
      userArticles.value = store.userArticles || [];
      console.log("vue에서 userArticles: ", userArticles.value);
      console.log("store에서 userArticles: ",store.userArticles) //undefined -> return 안 하면 이렇게 된다. 

      await store.getUserComments(user.value.id);
      userComments.value = store.userComments || [];
      console.log("Comments: ", userComments.value);
    }
  } catch (err) {
    error.value = '사용자 정보를 가져오지 못했습니다.';
  } finally {
    loading.value = false;
  }
};
const articleTitle = async (articlePk) => {
  const article = await store.getArticle(articlePk);
  console.log('articleTitle:',article.title)
  console.log('articlePK:',articlePk)
  return article.title ? article.title : '알 수 없는 글';

};
onMounted(fetchUserInfo);

watch(() => route.params.username, fetchUserInfo);
</script>

<style scoped>
/* 스타일을 여기에 추가하세요 */
</style> --> 

<template>
  <div>
    <h1 v-if="user">{{ user.username }} 프로필 페이지</h1>
    <p v-if="user">이름: {{ user.name }}</p>
    <p v-if="user">이메일: {{ user.email }}</p>
    <p v-if="user">나이: {{ user.age }}</p>
    <p v-if="user">현재 자산: {{ user.now_money }}</p>
    <p v-if="user">연봉: {{ user.money_per_year }}</p>
    <p v-if="user">선호 장소: {{ user.fav_place }}</p>
    <img :src="user.profile_img" alt="Profile Image" v-if="user && user.profile_img">

    <h2 v-if="user && user.contract_deposit">계약된 예금</h2>
    <ul v-if="user && user.contract_deposit">
      <li v-for="deposit in user.contract_deposit" :key="deposit.id">{{ deposit.name }}</li>
    </ul>

    <h2 v-if="user && user.contract_saving">계약된 적금</h2>
    <ul v-if="user && user.contract_saving">
      <li v-for="saving in user.contract_saving" :key="saving.id">{{ saving.name }}</li>
    </ul>

    <h2 v-if="userArticles">작성한 글</h2>
    <ul v-if="userArticles && userArticles.length">
      <li v-for="article in userArticles" :key="article.id">
        <h2>{{ article.title }}</h2>
        <p>{{ article.content }}</p>
        <br>
      </li>
    </ul>

    <h2 v-if="userComments">작성한 댓글</h2>
    <ul v-if="userComments.length">
      <li v-for="comment in userComments" :key="comment.id">

        <h2><RouterLink :to="{name:'DetailView',params:{id:comment.article}}">{{ getArticleTitle(comment.article) }}</RouterLink>에 달린 댓글</h2>
        
        {{ comment.content }}
        <br>
      </li>
    </ul>

    <p v-if="error">{{ error }}</p>
    <p v-if="loading">로딩 중...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, watchEffect } from 'vue';
import { useRoute } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import { RouterLink } from 'vue-router';

const route = useRoute();
const store = useCounterStore();
const user = ref(null);
const userArticles = ref([]);
const userComments = ref([]);
const articleTitles = ref({});
const error = ref(null);
const loading = ref(false);

const fetchUserInfo = async () => {
  loading.value = true;
  error.value = null;
  try {
    const username = route.params.username;
    await store.getUserInfo(username);
    user.value = store.userInfo;
    console.log('fetchUserInfo 결괴',user.value)
    if (user.value) {
      await store.getUserArticles(user.value.id);
      userArticles.value = store.userArticles || [];
      console.log('vue에서 userArticles:',userArticles.value)

      await store.getUserComments(user.value.id);
      userComments.value = store.userComments || [];
      console.log('vue에서 userComments:',userComments.value)
    }
  } catch (err) {
    error.value = '사용자 정보를 가져오지 못했습니다.';
  } finally {
    loading.value = false;
  }
};

const getArticleTitle = (articlePk) => {
  console.log(articleTitles.value)
  return articleTitles.value[articlePk] || '알 수 없는 글';
};

const fetchArticleTitles = async () => {
  for (const comment of userComments.value) {
    if (!articleTitles.value[comment.article]) {
      const article = await store.getArticle(comment.article);
      articleTitles.value[comment.article] = article.title || '알 수 없는 글';
    }
  }
};

onMounted(fetchUserInfo);

watch(() => route.params.username, fetchUserInfo);

watchEffect(() => {
  if (userComments.value.length) {
    fetchArticleTitles();
  }
});
</script>

<style scoped>
/* 스타일을 여기에 추가하세요 */
</style>


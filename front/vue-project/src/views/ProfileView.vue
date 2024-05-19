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

    <h2 v-if="user">계약된 예금</h2>
    <ul v-if="user">
      <li v-for="deposit in user.contract_deposit" :key="deposit.id">{{ deposit.name }}</li>
    </ul>

    <h2 v-if="user">계약된 적금</h2>
    <ul v-if="user">
      <li v-for="saving in user.contract_saving" :key="saving.id">{{ saving.name }}</li>
    </ul>

    <h2 v-if="user">작성한 글</h2>
    <ul v-if="user">
      <li v-for="article in articles" :key="article.id">{{ article.title }}</li>
    </ul>

    <h2 v-if="user">작성한 댓글</h2>
    <ul v-if="user">
      <li v-for="comment in comments" :key="comment.id">{{ comment.content }}</li>
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
const articles = ref([]);
const comments = ref([]);
const error = ref(null);
const loading = ref(false);

const fetchUserInfo = async () => {
  loading.value = true;
  error.value = null;
  try {
    await store.getUserInfo(route.params.username);
    user.value = store.userInfo;
    await store.getUserArticles(user.value.id);
    articles.value = store.articles;
    await store.getUserComments(user.value.id);
    comments.value = store.comments;
  } catch (err) {
    error.value = '사용자 정보를 가져오지 못했습니다.';
  } finally {
    loading.value = false;
  }
};

onMounted(fetchUserInfo);

watch(() => route.params.username, fetchUserInfo);
</script>

<style scoped>
/* 스타일을 여기에 추가하세요 */
</style>

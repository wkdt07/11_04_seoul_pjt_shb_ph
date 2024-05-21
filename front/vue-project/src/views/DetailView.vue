   <template>
    <div v-if="article">
      <h1>{{article.title }}</h1>
      <div v-if="article">
        <p>user: {{ article.user }}</p>
        <!-- <h2>제목: {{ article.title }}</h2> -->
        <p>{{ article.id }} 번 째 게시글</p>
        <p>{{ article.content }}</p>
        <p>{{ article.created_at }}</p>
        <p>{{ article.updated_at }}</p>
        <img v-if="article.image" :src="getImageUrl(article.image)" alt="게시글 이미지">
        <!-- {{ article }} -->
        <button @click="deleteArticle" v-if="store.userInfo.id===article.user">삭제하기</button>
    <RouterLink :to="{ name: 'EditView', params: { article_pk: article.id }}" v-if="store.userInfo.id===article.user">수정하기</RouterLink>
      </div>
      <RouterLink :to="{ name: 'createComment', params: { article_pk: article.id }}">Create Comment</RouterLink>
    </div>
    <div v-if="article">
      <!-- 조회용 -->
      <CommentList :articleId="article.id" />
    </div>
  </template>
  
  <script setup>
  import axios from 'axios';
  import { onMounted, ref } from 'vue';
  import { useCounterStore } from '@/stores/counter';
  import { useRoute } from 'vue-router';
  import { RouterLink } from 'vue-router';
  import CommentList from '@/components/CommentList.vue'; // CommentList 컴포넌트 임포트
  import { useRouter } from 'vue-router';
  const store = useCounterStore();
  const route = useRoute();
  const article = ref(null);
  const router = useRouter()
  const userInfo = store.userInfo
  const deleteArticle = async () => {
  const articleId = route.params.id
  try {
    await axios.delete(`${store.DJANGO_URL}/articles/${articleId}/`, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    console.log(articleId)
    router.push({ name: 'ArticleView' })
  } catch (error) {
    alert('삭제할 수 없습니다.')
    console.log(error)
  }
}
console.log('UserInfo=',userInfo)
const getImageUrl = (imagePath) => {
  console.log(`${store.DJANGO_URL}${imagePath}`)
  return `${store.DJANGO_URL}${imagePath}`;
};

  onMounted(async () => {
  article.value = await store.getArticle(route.params.id);
});
  </script>
  
  <style>
  </style>
  

   
<!-- <template>
    <div>
      <h1>DetailView</h1>
      <div v-if="article">
        <p>user: {{ article.user }}</p>
        <h2>제목: {{ article.title }}</h2>
        <p>{{ article.id }} 번 째 게시글</p>
        <p>{{ article.content }}</p>
        <p>{{ article.created_at }}</p>
        <p>{{ article.updated_at }}</p>
        {{ article }}
      </div>
      <RouterLink :to="{name:'createComment',params: { article_pk: article.id }}"></RouterLink>
    </div>
    <div>
    조회용 -->
       <!-- <CommentList
      :article="article"
      />
    </div>
  </template>
  
  <script setup>
  import axios from 'axios'
  import { onMounted, ref } from 'vue'
  import { useCounterStore } from '@/stores/counter'
  import { useRoute } from 'vue-router'
  import { RouterLink } from 'vue-router'
  const store = useCounterStore()
  const route = useRoute()
  const article = ref(null)
  
  onMounted(() => {
    axios({
      method: 'get',
      url: `${store.DJANGO_URL}/articles/${route.params.id}/`
    })
      .then((response) => {
        // console.log(response.data)
        article.value = response.data
      })
      .catch((error) => {
        console.log(error)
      })
  })
  
  </script>
  
  <style>
  
  </style>
   -->



   <template>
    <div v-if="article">
      <h1>DetailView</h1>
      <div v-if="article">
        <p>user: {{ article.user }}</p>
        <h2>제목: {{ article.title }}</h2>
        <p>{{ article.id }} 번 째 게시글</p>
        <p>{{ article.content }}</p>
        <p>{{ article.created_at }}</p>
        <p>{{ article.updated_at }}</p>
        {{ article }}
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
  
  const store = useCounterStore();
  const route = useRoute();
  const article = ref(null);
  
  // onMounted(() => {
  //   axios({
  //     method: 'get',
  //     url: `${store.DJANGO_URL}/articles/${route.params.id}/`
  //   })
  //     .then((response) => {
  //       article.value = response.data;
  //     })
  //     .catch((error) => {
  //       console.log(error);
  //     });
  // });

  onMounted(async () => {
  article.value = await store.getArticle(route.params.id);
});
  </script>
  
  <style>
  </style>
  

   
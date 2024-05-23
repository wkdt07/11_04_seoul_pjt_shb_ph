<!-- <template>
    <div>
      <h1>Article Page</h1>
      <RouterLink :to="{ name:'CreateView' }">
        [CREATE]
      </RouterLink>
      <ArticleList />
    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue'
  import { useCounterStore } from '@/stores/counter'
  import { RouterLink } from 'vue-router'
  import ArticleList from '@/components/ArticleList.vue'
  
  const store = useCounterStore()
  
  onMounted(() => {
    store.getArticles()
  })
  
  </script>
  
  <style>
  
  </style>
   -->


   <template>
    <div class="article-page">
      <header>
        <h1>유저 게시판</h1>
        <RouterLink class="create-link" :to="{ name: 'CreateView' }">
          글 쓰기
        </RouterLink>
      </header>
      <table class="article-table">
        <thead>
          <tr>
            <th class="narrow">번호</th>
            <th>닉네임</th>
            <th>게시글 제목</th>
            <th>댓글 수</th>
            <th>등록 날짜</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(article, index) in articles" :key="article.id">
            <td class="narrow">{{ index + 1 }}</td>
            <td>{{ article.user }}</td>
            <td>{{ article.title }}</td>
            <td>{{ article.comments ? article.comments.length : 0 }}</td>
            <td>{{ new Date(article.created_at).toLocaleDateString() }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useCounterStore } from '@/stores/counter'
  import { RouterLink } from 'vue-router'
  
  const store = useCounterStore()
  const articles = ref([])
  
  onMounted(async () => {
    await store.getArticles()
    articles.value = store.articles
  })
  </script>
  
  <style scoped>
  .article-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    background-color: #fff;
    font-size: 16px;
    color: #333;
    font-family: 'NEXON Lv1 Gothic Low OTF';
    padding: 20px;
    box-sizing: border-box;
  }
  
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin-bottom: 20px;
  }
  
  h1 {
    font-size: 35px;
  }
  
  .create-link {
    border-radius: 3px;
    background-color: #2db2ff;
    color: white;
    width: 120px;
    height: 35px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 9px 14px;
    box-sizing: border-box;
    font-size: 14px;
    text-decoration: none;
    cursor: pointer;
    opacity: 0.8;
  }
  
  .create-link:hover {
    opacity: 1;
  }
  
  .article-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  
  .article-table th,
  .article-table td {
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
  }
  
  .article-table th {
    background-color: #f2f2f2;
  }
  
  .article-table td {
    font-size: 14px;
  }
  
  .article-table .narrow {
    width: 50px;
    /* 좁은 열의 너비 조정 */
  }
  </style>
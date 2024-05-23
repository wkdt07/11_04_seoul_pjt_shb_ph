   <!-- <template>
    <div v-if="article">
      <h1>{{article.title }}</h1>
      <div v-if="article">
        <p>user: {{ article.user }}</p>
     
        <p>{{ article.id }} 번 째 게시글</p>
        <p>{{ article.content }}</p>
        <p>{{ article.created_at }}</p>
        <p>{{ article.updated_at }}</p>
        <img v-if="article.image" :src="getImageUrl(article.image)" alt="게시글 이미지">
     
        <button @click="deleteArticle" v-if="store.userInfo.id===article.user">삭제하기</button>
    <RouterLink :to="{ name: 'EditView', params: { article_pk: article.id }}" v-if="store.userInfo.id===article.user">수정하기</RouterLink>
      </div>
      <RouterLink :to="{ name: 'createComment', params: { article_pk: article.id }}">Create Comment</RouterLink>
    </div>
    <div v-if="article">
    
      <CommentList :articleId="article.id" />
    </div>
  </template>
  
  <script setup>
  import axios from 'axios';
  import { onMounted, ref } from 'vue';
  import { useCounterStore } from '@/stores/counter';
  import { useRoute } from 'vue-router';
  import { RouterLink } from 'vue-router';
  import CommentList from '@/components/CommentList.vue'; 
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
  

    -->

    <!-- =========================================================== -->
    <!-- <template>
      <div v-if="article">
        <h1>{{ article.title }}</h1>
        <div v-if="article">
          <p>user: {{ article.user }}</p>
          
          <p>{{ article.id }} 번 째 게시글</p>
          <p>{{ article.content }}</p>
          <p>{{ article.created_at }}</p>
          <p>{{ article.updated_at }}</p>
          <img v-if="article.image" :src="getImageUrl(article.image)" alt="게시글 이미지">
          
          <button @click="deleteArticle" v-if="store.userInfo.id === article.user">삭제하기</button>
          <RouterLink :to="{ name: 'EditView', params: { article_pk: article.id } }" v-if="store.userInfo.id === article.user">
            수정하기</RouterLink>
        </div>
        <RouterLink :to="{ name: 'createComment', params: { article_pk: article.id } }">Create Comment</RouterLink>
      </div>
      <div v-if="article">
        
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
    console.log('UserInfo=', userInfo)
    const getImageUrl = (imagePath) => {
      console.log(`${store.DJANGO_URL}${imagePath}`)
      return `${store.DJANGO_URL}${imagePath}`;
    };
    
    onMounted(async () => {
      article.value = await store.getArticle(route.params.id);
    });
    </script>
      
    <style>
    @font-face {
      font-family: 'NEXON Lv1 Gothic Low OTF';
      src: url('@/assets/NEXON_Lv1_Gothic_Low.otf') format('opentype');
    }
    </style> -->


    <!--  ===================집 가기 전 -->


    <template>
      <div v-if="article" class="article-container">
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="article-details">
          <p class="article-user">작성자: {{ nickname }}</p>
          <p class="article-id">{{ article.id }} 번 째 게시글</p>
          <p class="article-content">{{ article.content }}</p>
          <p class="article-timestamp">작성일: {{ formatDate(article.created_at) }}</p>
          <p class="article-timestamp">수정일: {{ formatDate(article.updated_at) }}</p>
          <img v-if="article.image" :src="getImageUrl(article.image)" alt="게시글 이미지" class="article-image">
          <div class="article-actions" v-if="store.userInfo.id === article.user">
            <button @click="deleteArticle" class="article-button">삭제하기</button>
            <RouterLink :to="{ name: 'EditView', params: { article_pk: article.id } }" class="article-button">
              수정하기
            </RouterLink>
          </div>
        </div>
        <RouterLink :to="{ name: 'createComment', params: { article_pk: article.id } }" class="create-comment-link">
          Create Comment
        </RouterLink>
        <CommentList :articleId="article.id" />
      </div>
    </template>
        
    <script setup>
    import axios from 'axios';
    import { onMounted, ref } from 'vue';
    import { useCounterStore } from '@/stores/counter';
    import { useRoute, useRouter } from 'vue-router';
    import CommentList from '@/components/CommentList.vue';
    
    const store = useCounterStore();
    const route = useRoute();
    const router = useRouter();
    const article = ref(null);
    const nickname = ref('');
    
    const deleteArticle = async () => {
      const articleId = route.params.id;
      try {
        await axios.delete(`${store.DJANGO_URL}/articles/${articleId}/`, {
          headers: {
            Authorization: `Token ${store.token}`
          }
        });
        router.push({ name: 'ArticleView' });
      } catch (error) {
        alert('삭제할 수 없습니다.');
        console.log(error);
      }
    };
    
    const getImageUrl = (imagePath) => `${store.DJANGO_URL}${imagePath}`;
    
    const formatDate = (timestamp) => {
      const date = new Date(timestamp);
      return date.toLocaleString();
    };
    
    const fetchArticle = async () => {
      article.value = await store.getArticle(route.params.id);
      nickname.value = await store.getUserNickname(article.value.user); // 사용자 닉네임 가져오기
    };
    
    onMounted(async () => {
      await store.getUserInfo(); // 사용자 정보 가져오기
      await fetchArticle(); // fetchArticle 함수 호출
    });
    // ,
    </script>
        
    <style scoped>
    @font-face {
      font-family: 'NEXON Lv1 Gothic Low OTF';
      src: url('@/assets/fonts/NEXON_Lv1_Gothic_Low.otf') format('opentype');
    }
    
    .article-container {
      padding: 20px;
      font-family: 'NEXON Lv1 Gothic Low OTF';
    }
    
    .article-title {
      font-size: 24px;
      font-weight: bold;
      margin-bottom: 15px;
    }
    
    .article-details {
      margin-bottom: 20px;
    }
    
    .article-user,
    .article-id,
    .article-content,
    .article-timestamp {
      margin-bottom: 10px;
    }
    
    .article-image {
      max-width: 100%;
      height: auto;
      margin-bottom: 15px;
    }
    
    .article-actions {
      display: flex;
      gap: 10px;
    }
    
    .article-button {
      padding: 8px 12px;
      background-color: #2db2ff;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-family: 'NEXON Lv1 Gothic Low OTF';
      font-size: 14px;
      transition: background-color 0.3s ease;
    }
    
    .article-button:hover {
      background-color: #0a73d9;
    }
    
    .create-comment-link {
      display: inline-block;
      margin-top: 10px;
      font-size: 16px;
      color: #2db2ff;
      text-decoration: none;
    }
    
    .create-comment-link:hover {
      text-decoration: underline;
    }
    </style>
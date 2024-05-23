<!-- <template>
  <div>
    <form @submit.prevent="createComment">
      <label for="content" id="content">댓글:</label>
      <input type="text" id="content" v-model="content">
      <input type="submit" value="작성">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '../stores/counter';
import { useRouter, useRoute } from 'vue-router';

const store = useCounterStore();
const content = ref('');
const router = useRouter();
const route = useRoute();

const createComment = async () => {
  const payload = {
    content: content.value,
    article_pk: route.params.article_pk,
  };
  await store.createComment(payload);
  content.value = ''; // 댓글 작성 후 입력 필드 초기화
  router.push({ name: 'DetailView', params: { id: route.params.article_pk } }); // 댓글 작성 후 상세 페이지로 이동
};
</script>

<style scoped>
</style> -->
<!-- ================================ -->
<!-- <template>
  <div>
    <form @submit.prevent="createComment">
      <label for="content" id="content">댓글:</label>
      <input type="text" id="content" v-model="content">
      <input type="submit" value="작성">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '../stores/counter';
import { useRouter, useRoute } from 'vue-router';

const store = useCounterStore();
const content = ref('');
const router = useRouter();
const route = useRoute();

const createComment = async () => {
  const payload = {
    content: content.value,
    article_pk: route.params.article_pk,
  };
  await store.createComment(payload);
  content.value = ''; // 댓글 작성 후 입력 필드 초기화
  router.push({ name: 'DetailView', params: { id: route.params.article_pk } }); // 댓글 작성 후 상세 페이지로 이동
};
</script>

<style scoped>
@font-face {
  font-family: 'NEXON Lv1 Gothic Low OTF';
  src: url('@/assets/NEXON_Lv1_Gothic_Low.otf') format('opentype');
}
</style> -->

<!-- 집 가기 전 수정 -->


<template>
  <div class="comment-form">
    <h2>댓글 작성</h2>
    <form @submit.prevent="createComment">
      <div class="form-group">
        <label for="content">내용</label>
        <textarea id="content" v-model="content" class="form-control" placeholder="댓글을 입력하세요"></textarea>
      </div>
      <button type="submit" class="submit-button">작성</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '../stores/counter';
import { useRouter, useRoute } from 'vue-router';

const store = useCounterStore();
const content = ref('');
const router = useRouter();
const route = useRoute();

const createComment = async () => {
  const payload = {
    content: content.value,
    article_pk: route.params.article_pk,
  };
  await store.createComment(payload);
  content.value = ''; // 댓글 작성 후 입력 필드 초기화
  router.push({ name: 'DetailView', params: { id: route.params.article_pk } }); // 댓글 작성 후 상세 페이지로 이동
};
</script>

<style scoped>
@font-face {
  font-family: 'NEXON Lv1 Gothic Low OTF';
  src: url('@/assets/fonts/NEXON_Lv1_Gothic_Low.otf') format('opentype');
}

.comment-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 800px;
  /* 최대 너비를 800px로 넓힘 */
  margin: 0 auto;
  background-color: #fff;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  font-family: 'NEXON Lv1 Gothic Low OTF';
  margin-top: 60px;
}

.comment-form h2 {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.form-group {
  width: 100%;
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.form-control {
  width: 822px;
  height: 563px;
  padding: 16px;
  /* 패딩을 16px로 조정하여 입력 필드를 더 넓게 보이게 함 */
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  font-family: 'NEXON Lv1 Gothic Low OTF';
  box-sizing: border-box;
}

.form-control::placeholder {
  color: #bbb;
}

.submit-button {
  width: 100%;
  padding: 14px;
  /* 패딩을 14px로 조정하여 버튼을 더 넓게 보이게 함 */
  background-color: #2db2ff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #0a73d9;
}
</style>

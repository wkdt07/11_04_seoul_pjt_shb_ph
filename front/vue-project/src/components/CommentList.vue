<!-- <template>
  <div v-if="comments.length">
    <hr>
    <div v-for="comment in comments" :key="comment.id">
      <br>
      <p>{{ comment.content }} by {{ comment.user }}</p>
      <button @click="editComment(comment.id)" v-if="store.userInfo.id===comment.user">수정하기</button>
      <button @click="deleteComment(comment.id)" v-if="store.userInfo.id===comment.user">삭제하기</button>
      <hr>
  
      
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useCounterStore } from '@/stores/counter';

const props = defineProps({
  articleId: Number
});

const store = useCounterStore();
const comments = ref([]);

const getComments = async () => {
  await store.getComments(props.articleId);
  comments.value = store.comments;
};

const editComment = async (commentId) => {
  const newContent = prompt('댓글을 수정하세요:');
  if (newContent) {
    await store.editComment(commentId, newContent);
    await getComments(); // 댓글 목록 갱신
  }
};

const deleteComment = async (commentId) => {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    await store.deleteComment(commentId);
    await getComments(); // 댓글 목록 갱신
  }
};

onMounted(getComments);

// 댓글 목록이 변경될 때마다 댓글을 업데이트합니다.
watch(() => store.comments, (newComments) => {
  comments.value = newComments;
});
</script>

<style scoped>
</style> -->

<!-- =========================================================================== -->
<!-- <template>
  <div v-if="comments.length">
    <hr>
    <div v-for="comment in comments" :key="comment.id">
      <br>
      <p>{{ comment.content }} by {{ comment.user }}</p>
      <button @click="editComment(comment.id)" v-if="store.userInfo.id === comment.user">수정하기</button>
      <button @click="deleteComment(comment.id)" v-if="store.userInfo.id === comment.user">삭제하기</button>
      <hr>
  
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useCounterStore } from '@/stores/counter';

const props = defineProps({
  articleId: Number
});

const store = useCounterStore();
const comments = ref([]);

const getComments = async () => {
  await store.getComments(props.articleId);
  comments.value = store.comments;
};

const editComment = async (commentId) => {
  const newContent = prompt('댓글을 수정하세요:');
  if (newContent) {
    await store.editComment(commentId, newContent);
    await getComments(); // 댓글 목록 갱신
  }
};

const deleteComment = async (commentId) => {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    await store.deleteComment(commentId);
    await getComments(); // 댓글 목록 갱신
  }
};

onMounted(getComments);

// 댓글 목록이 변경될 때마다 댓글을 업데이트합니다.
watch(() => store.comments, (newComments) => {
  comments.value = newComments;
});
</script>

<style scoped>
@font-face {
  font-family: 'NEXON Lv1 Gothic Low OTF';
  src: url('@/assets/NEXON_Lv1_Gothic_Low.otf') format('opentype');
}
</style> -->

<!-- 집 가기 전 수정 -->

<template>
  <div v-if="comments.length" class="comments-container">
    <hr>
    <div v-for="comment in comments" :key="comment.id" class="comment-item">
      <p class="comment-content">{{ comment.content }} <span class="comment-user">by {{ comment.user }}</span></p>
      <div class="comment-actions" v-if="store.userInfo.id === comment.user">
        <button @click="editComment(comment.id)" class="comment-button">수정하기</button>
        <button @click="deleteComment(comment.id)" class="comment-button">삭제하기</button>
      </div>
      <hr>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useCounterStore } from '@/stores/counter';

const props = defineProps({
  articleId: Number
});

const store = useCounterStore();
const comments = ref([]);

const getComments = async () => {
  await store.getComments(props.articleId);
  comments.value = store.comments;
};

const editComment = async (commentId) => {
  const newContent = prompt('댓글을 수정하세요:');
  if (newContent) {
    await store.editComment(commentId, newContent);
    await getComments(); // 댓글 목록 갱신
  }
};

const deleteComment = async (commentId) => {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    await store.deleteComment(commentId);
    await getComments(); // 댓글 목록 갱신
  }
};

onMounted(getComments);

// 댓글 목록이 변경될 때마다 댓글을 업데이트합니다.
watch(() => store.comments, (newComments) => {
  comments.value = newComments;
});
</script>

<style scoped>
@font-face {
  font-family: 'NEXON Lv1 Gothic Low OTF';
  src: url('@/assets/fonts/NEXON_Lv1_Gothic_Low.otf') format('opentype');
}

.comments-container {
  max-width: 800px;
  width: 100%;
  padding: 20px;
  font-family: 'NEXON Lv1 Gothic Low OTF';
}

.comment-item {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.comment-content {
  font-size: 16px;
  margin-bottom: 10px;
}

.comment-user {
  font-weight: bold;
  color: #2db2ff;
}

.comment-actions {
  display: flex;
  gap: 10px;
}

.comment-button {
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

.comment-button:hover {
  background-color: #0a73d9;
}
</style>
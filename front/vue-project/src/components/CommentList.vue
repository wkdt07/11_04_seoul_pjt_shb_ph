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


<template>
  <div v-if="comments.length">
    <hr>
    <div v-for="comment in comments" :key="comment.id">
      <br>
      <p>{{ comment.content }} by {{ comment.user }}</p>
      <button @click="editComment(comment.id)" v-if="store.userInfo.id === comment.user">수정하기</button>
      <button @click="deleteComment(comment.id)" v-if="store.userInfo.id === comment.user">삭제하기</button>
      <hr>
      <!-- {{ comment }} -->

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
</style>
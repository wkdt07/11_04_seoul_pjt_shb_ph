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
import { useCounterStore } from '../stores/counter';
import { useRouter } from 'vue-router'
const store = useCounterStore()
const content=ref('')
router = useRouter()
const comment_pk=ref(null)
const createComment=function(){
  const payload = {
    content : content.value,
    article_pk:router.params.article_pk,
  }
  store.createComment(payload)
}
</script>

<style scoped>

</style> -->

<template>
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
</style>

<!-- <template>
  <div v-if="store.comments.length">
  <div v-for="comment in store.comments">    
    <p>{{ comment.content }}</p>
    <p>{{ comment.user }}</p>   
  </div></div>
  <RouterLink :to="{name:'createComment',params: { article_pk: article.id }}"></RouterLink>
</template> 

<script setup>
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router';

const store = useCounterStore()

defineProps({
  article : Object
})

const article_pk = article.id


const getComments = function(){
  store.getComments(article_pk)
}
</script>

<style scoped>

</style> -->


<template>
  <div v-if="comments.length">
    <div v-for="comment in comments" :key="comment.id">
      <br>
      <p>작성자: {{ comment.user }}, {{ comment.id }}번째 댓글: {{ comment.content }}</p>
      {{ comment }}
      
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



onMounted(getComments);

// 댓글 목록이 변경될 때마다 댓글을 업데이트합니다.
watch(() => store.comments, (newComments) => {
  comments.value = newComments;
});
</script>

<style scoped>
</style>

<!-- <template>
  <div>

 

    {{ store.userInfo }}
    <h1 v-if="user">{{ user.username }} 프로필 페이지</h1>
    <img :src="getProfileImgUrl(user.profile_img)" alt="Profile Image" v-if="user && user.profile_img">
    <p v-if="user">이름: {{ user.name }}</p>
    <p v-if="user">이메일: {{ user.email }}</p>
    <p v-if="user">닉네임: {{ user.nickname }}</p>
    <p v-if="user">나이: {{ user.age }}</p>
    <p v-if="user">현재 자산: {{ user.now_money }}</p>
    <p v-if="user">연봉: {{ user.money_per_year }}</p>
    <p v-if="user">선호 장소: {{ user.fav_place }}</p>
    
    <div><button v-if="isCurrentUser" @click="editProfile">프로필 수정</button></div>

    <h2 v-if="user && user.deposits">계약된 예금</h2>
    <ul v-if="user && user.deposits">
      <li v-for="deposit in user.deposits" :key="deposit.id">{{ deposit.fin_prdt_nm}}</li>
    </ul>
    
    <h2 v-if="user && user.savings">계약된 적금</h2>
    <ul v-if="user && user.savings">
      <li v-for="saving in user.savings" :key="saving.id">{{ saving.fin_prdt_nm }}</li>
    </ul> 
    
    <h2 v-if="userArticles">작성한 글</h2>
    <ul v-if="userArticles && userArticles.length">
      <li v-for="article in userArticles" :key="article.id">
        <h2>{{ article.title }}</h2>
        <p>{{ article.content }}</p>
        <br>
      </li>
    </ul>
    
    <h2 v-if="userComments">작성한 댓글</h2>
    <ul v-if="userComments.length">
      <li v-for="comment in userComments" :key="comment.id">

        <h2><RouterLink :to="{name:'DetailView',params:{id:comment.article}}">{{ getArticleTitle(comment.article) }}</RouterLink>에 달린 댓글</h2>
        
        {{ comment.content }}
        <br>
      </li>
    </ul>

    <p v-if="error">{{ error }}</p>
    <p v-if="loading">로딩 중...</p>
  </div>
</template>

<script setup>
import { ref, onMounted,computed, watch, watchEffect } from 'vue';
import { useRoute,useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import { RouterLink } from 'vue-router';
import BarChartDetail from '@/components/BarChartDetailView.vue';
import axios from 'axios';

const router = useRouter()
const route = useRoute();
const store = useCounterStore();
const user = ref(null);
const userArticles = ref([]);
const userComments = ref([]);
const articleTitles = ref({});
const error = ref(null);
const loading = ref(false);

const selectedDepositSimple = ref(null);
const selectedDeposit = ref(null);
const selectedDepositCode = computed(() => selectedDepositSimple.value?.fin_prdt_cd);
const dialog = ref(false);
const averageIntrRate = [3.45, 4.08, 3.4, 3.35];
const intrRate = ref([null, null, null, null]);
const intrRate2 = ref([null, null, null, null]);
const dataLoaded = ref(false);

const getProfileImgUrl = (imgPath) => {
  console.log(`이미지URL:${imgPath}`)
  console.log(`결과값:${store.DJANGO_URL}${imgPath}}`)
  return `${store.DJANGO_URL}${imgPath}`;
  
};

const fetchUserInfo = async () => {
  loading.value = true;
  error.value = null;
  try {
    const username = route.params.username;
    await store.getUserInfo(username);
    user.value = store.userInfo;
    console.log('fetchUserInfo 결과',user.value)
    if (user.value) {
      await store.getUserArticles(user.value.id);
      userArticles.value = store.userArticles || [];
      console.log('vue에서 userArticles:',userArticles.value)

      await store.getUserComments(user.value.id);
      userComments.value = store.userComments || [];
      console.log('vue에서 userComments:',userComments.value)
    }
  } catch (err) {
    error.value = '사용자 정보를 가져오지 못했습니다.';
  } finally {
    loading.value = false;
  }
};

const getArticleTitle = (articlePk) => {
  console.log(articleTitles.value)
  return articleTitles.value[articlePk] || '알 수 없는 글';
};

const fetchArticleTitles = async () => {
  for (const comment of userComments.value) {
    if (!articleTitles.value[comment.article]) {
      const article = await store.getArticle(comment.article);
      articleTitles.value[comment.article] = article.title || '알 수 없는 글';
    }
  }
};

const isCurrentUser = computed(() => {
  return store.userInfo && store.userInfo.username === route.params.username;
});

const editProfile = () => {
  router.push({ name: 'ProfileEditView', params: { username: route.params.username } });
};

const getDeposit = async () => {
  if (!selectedDepositCode.value) {
    console.error('selectedDepositCode is null or undefined');
    return;
  }

  try {
    const res = await axios.get(`${store.DJANGO_URL}/financial/deposit_list/${selectedDepositCode.value}/`);
    const data = res.data;
    selectedDeposit.value = {
      '금융 상품명': data.fin_prdt_nm,
      '공시 제출월': data.dcls_month,
      '금융 회사명': data.kor_co_nm,
      '가입 방법': data.join_way,
      '만기 후 이자율': data.mtrt_int,
      '우대 조건': data.spcl_cnd,
      '가입 대상': data.join_member,
      '가입 제한': data.join_deny === 1 ? '제한없음' : data.join_deny === 2 ? '서민전용' : '일부제한',
      '최고 한도': data.max_limit,
      '기타 유의사항': data.etc_note
    };
    const optionList = data.options;

    intrRate.value = [null, null, null, null];
    intrRate2.value = [null, null, null, null];

    for (const option of optionList) {
      if (option.save_trm === "6") {
        intrRate.value[0] = option.intr_rate;
        intrRate2.value[0] = option.intr_rate2;
      } else if (option.save_trm === "12") {
        intrRate.value[1] = option.intr_rate;
        intrRate2.value[1] = option.intr_rate2;
      } else if (option.save_trm === "24") {
        intrRate.value[2] = option.intr_rate;
        intrRate2.value[2] = option.intr_rate2;
      } else if (option.save_trm === "36") {
        intrRate.value[3] = option.intr_rate;
        intrRate2.value[3] = option.intr_rate2;
      }
    }

    dataLoaded.value = true;
  } catch (err) {
    console.log(err);
  }
};

const close = () => {
  dialog.value = false;
};

onMounted(fetchUserInfo);

watch(() => route.params.username, fetchUserInfo);

watchEffect(() => {
  if (userComments.value.length) {
    fetchArticleTitles();
  }
});
</script>

<style scoped>
/* 스타일을 여기에 추가하세요 */

.loading {
  display: flex;
  height: 80vh;
  align-items: center;
  justify-content: center;
}

.progress-circular {
  width: 80px;
  height: 80px;
  border: 5px solid #1089FF;
  border-radius: 50%;
  border-top: 5px solid transparent;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
}

.dialog-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 800px;
  max-width: 90%;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

tbody>tr {
  transition: 200ms;
  cursor: pointer;
}

tbody>tr:hover {
  background-color: rgb(247, 250, 253);
  color: #1089FF;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.table th,
.table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.table th {
  background-color: #f2f2f2;
  text-align: left;
}

.bank-select {
  padding: 10px;
  border: 1px solid #1089FF;
  border-radius: 4px;
}
</style>
</style>
 -->
 

 <!-- <template>
  <div>
    <h1 v-if="user">{{ user.username }} 프로필 페이지</h1>
    <img :src="getProfileImgUrl(user.profile_img)" alt="Profile Image" v-if="user && user.profile_img">
    <p v-if="user">이름: {{ user.name }}</p>
    <p v-if="user">이메일: {{ user.email }}</p>
    <p v-if="user">닉네임: {{ user.nickname }}</p>
    <p v-if="user">나이: {{ user.age }}</p>
    <p v-if="user">현재 자산: {{ user.now_money }}</p>
    <p v-if="user">연봉: {{ user.money_per_year }}</p>
    <p v-if="user">선호 장소: {{ user.fav_place }}</p>
    
    <div><button v-if="isCurrentUser" @click="editProfile">프로필 수정</button></div>

    <h2 v-if="user && user.deposits">계약된 예금</h2>
    <ul v-if="user && user.deposits">
      <li v-for="deposit in user.deposits" :key="deposit.fin_prdt_cd" @click="clickDeposit(deposit)">
        {{ deposit.fin_prdt_nm }}
      </li>
    </ul>
    
    <h2 v-if="user && user.savings">계약된 적금</h2>
    <ul v-if="user && user.savings">
      <li v-for="saving in user.savings" :key="saving.fin_prdt_cd" @click="clickSaving(saving)">
        {{ saving.fin_prdt_nm }}
      </li>
    </ul>
    
    <h2 v-if="userArticles">작성한 글</h2>
    <ul v-if="userArticles && userArticles.length">
      <li v-for="article in userArticles" :key="article.id">
        <h2>{{ article.title }}</h2>
        <p>{{ article.content }}</p>
        <br>
      </li>
    </ul>
    
    <h2 v-if="userComments">작성한 댓글</h2>
    <ul v-if="userComments.length">
      <li v-for="comment in userComments" :key="comment.id">
        <h2><RouterLink :to="{name:'DetailView',params:{id:comment.article}}">{{ getArticleTitle(comment.article) }}</RouterLink>에 달린 댓글</h2>
        {{ comment.content }}
        <br>
      </li>
    </ul>

    <p v-if="error">{{ error }}</p>
    <p v-if="loading">로딩 중...</p>


    <div v-if="dialog" class="dialog">
      <div class="dialog-content">
        <h3>{{ selectedDeposit?.fin_prdt_nm }}</h3>
        <div v-if="store.isLogin">
          <button v-if="isDeposit" @click.prevent="deleteDepositUser">가입 취소하기</button>
          <button v-if="!isDeposit" @click.prevent="deleteSavingUser">가입 취소하기</button>
        </div>

        <table>
          <tbody>
            <tr v-for="(value, key) in selectedDeposit" :key="key">
              <td width="28%" class="font-weight-bold">{{ key }}</td>
              <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
              <td v-else>{{ value }}</td>
            </tr>
          </tbody>
        </table>
        <hr class="my-3">
        <div class="mx-auto" v-if="dataLoaded">
          <BarChartDetail
            :title="selectedDepositSimple.fin_prdt_nm"
            :average-intr-rate="averageIntrRate"
            :intr-rate="intrRate"
            :intr-rate2="intrRate2"
          />
          <p class="text-caption">* 개월별 평균 예금 금리는 2023년 11월 기준입니다.</p>
          <p class="text-caption">* 차트에 없는 이자율은 상품에 존재하지 않는 옵션입니다.</p>
        </div>

        <div class="dialog-actions">
          <button @click="close">닫기</button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="progress-circular"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import { RouterLink } from 'vue-router';
import BarChartDetail from '@/components/BarChartDetailView.vue';
import axios from 'axios';


const router = useRouter();
const route = useRoute();
const store = useCounterStore();
const user = ref(null);
const userArticles = ref([]);
const userComments = ref([]);
const articleTitles = ref({});
const error = ref(null);
const loading = ref(false);

const selectedDepositSimple = ref(null);
const selectedDeposit = ref(null);
const selectedDepositCode = computed(() => selectedDepositSimple.value?.fin_prdt_cd);
const dialog = ref(false);
const averageIntrRate = [3.45, 4.08, 3.4, 3.35];
const intrRate = ref([null, null, null, null]);
const intrRate2 = ref([null, null, null, null]);
const dataLoaded = ref(false);

const isDeposit = ref(true);

const getProfileImgUrl = (imgPath) => {
  return `${store.DJANGO_URL}${imgPath}`;
};

const fetchUserInfo = async () => {
  loading.value = true;
  error.value = null;
  try {
    const username = route.params.username;
    await store.getUserInfo(username);
    user.value = store.userInfo;
    if (user.value) {
      await store.getUserArticles(user.value.id);
      userArticles.value = store.userArticles || [];

      await store.getUserComments(user.value.id);
      userComments.value = store.userComments || [];
    }
  } catch (err) {
    error.value = '사용자 정보를 가져오지 못했습니다.';
  } finally {
    loading.value = false;
  }
};

const deleteDepositUser = async () => {
  try {
    await axios.delete(`${store.DJANGO_URL}/financial/deposit_list/${selectedDepositCode.value}/contract/`, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    });
    store.userInfo.deposits = store.userInfo.deposits.filter(deposit => deposit.fin_prdt_cd !== selectedDepositCode.value);
    user.value = store.userInfo;
    dialog.value = false;
  } catch (error) {
    console.error('Failed to delete deposit:', error);
  }
};

const deleteSavingUser = async () => {
  try {
    await axios.delete(`${store.DJANGO_URL}/financial/saving_list/${selectedDepositCode.value}/contract/`, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    });
    store.userInfo.savings = store.userInfo.savings.filter(saving => saving.fin_prdt_cd !== selectedDepositCode.value);
    user.value = store.userInfo;
    dialog.value = false;
  } catch (error) {
    console.error('Failed to delete saving:', error);
  }
};

const getArticleTitle = (articlePk) => {
  return articleTitles.value[articlePk] || '알 수 없는 글';
};

const fetchArticleTitles = async () => {
  for (const comment of userComments.value) {
    if (!articleTitles.value[comment.article]) {
      const article = await store.getArticle(comment.article);
      articleTitles.value[comment.article] = article.title || '알 수 없는 글';
    }
  }
};

const isCurrentUser = computed(() => {
  return store.userInfo && store.userInfo.username === route.params.username;
});

const editProfile = () => {
  router.push({ name: 'ProfileEditView', params: { username: route.params.username } });
};

const clickDeposit = async (deposit) => {
  selectedDepositSimple.value = deposit;
  isDeposit.value = true;
  intrRate.value = [];
  intrRate2.value = [];
  dataLoaded.value = false;
  await getDeposit();
  dialog.value = true;
};

const clickSaving = async (saving) => {
  selectedDepositSimple.value = saving;
  isDeposit.value = false;
  intrRate.value = [];
  intrRate2.value = [];
  dataLoaded.value = false;
  await getSaving();
  dialog.value = true;
};

const getDeposit = async () => {
  if (!selectedDepositCode.value) {
    console.error('selectedDepositCode is null or undefined');
    return;
  }

  try {
    const res = await axios.get(`${store.DJANGO_URL}/financial/deposit_list/${selectedDepositCode.value}/`);
    const data = res.data;
    selectedDeposit.value = {
      '금융 상품명': data.fin_prdt_nm,
      '공시 제출월': data.dcls_month,
      '금융 회사명': data.kor_co_nm,
      '가입 방법': data.join_way,
      '만기 후 이자율': data.mtrt_int,
      '우대 조건': data.spcl_cnd,
      '가입 대상': data.join_member,
      '가입 제한': data.join_deny === 1 ? '제한없음' : data.join_deny === 2 ? '서민전용' : '일부제한',
      '최고 한도': data.max_limit,
      '기타 유의사항': data.etc_note
    };
    const optionList = data.options;

    intrRate.value = [null, null, null, null];
    intrRate2.value = [null, null, null, null];

    for (const option of optionList) {
      if (option.save_trm === "6") {
        intrRate.value[0] = option.intr_rate;
        intrRate2.value[0] = option.intr_rate2;
      } else if (option.save_trm === "12") {
        intrRate.value[1] = option.intr_rate;
        intrRate2.value[1] = option.intr_rate2;
      } else if (option.save_trm === "24") {
        intrRate.value[2] = option.intr_rate;
        intrRate2.value[2] = option.intr_rate2;
      } else if (option.save_trm === "36") {
        intrRate.value[3] = option.intr_rate;
        intrRate2.value[3] = option.intr_rate2;
      }
    }

    dataLoaded.value = true;
  } catch (err) {
    console.log(err);
  }
};

const getSaving = async () => {
  if (!selectedDepositCode.value) {
    console.error('selectedDepositCode is null or undefined');
    return;
  }

  try {
    const res = await axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedDepositCode.value}/`);
    const data = res.data;
    selectedDeposit.value = {
      '금융 상품명': data.fin_prdt_nm,
      '공시 제출월': data.dcls_month,
      '금융 회사명': data.kor_co_nm,
      '가입 방법': data.join_way,
      '만기 후 이자율': data.mtrt_int,
      '우대 조건': data.spcl_cnd,
      '가입 대상': data.join_member,
      '가입 제한': data.join_deny === 1 ? '제한없음' : data.join_deny === 2 ? '서민전용' : '일부제한',
      '최고 한도': data.max_limit,
      '기타 유의사항': data.etc_note
    };
    const optionList = data.options;

    intrRate.value = [null, null, null, null];
    intrRate2.value = [null, null, null, null];

    for (const option of optionList) {
      if (option.save_trm === "6") {
        intrRate.value[0] = option.intr_rate;
        intrRate2.value[0] = option.intr_rate2;
      } else if (option.save_trm === "12") {
        intrRate.value[1] = option.intr_rate;
        intrRate2.value[1] = option.intr_rate2;
      } else if (option.save_trm === "24") {
        intrRate.value[2] = option.intr_rate;
        intrRate2.value[2] = option.intr_rate2;
      } else if (option.save_trm === "36") {
        intrRate.value[3] = option.intr_rate;
        intrRate2.value[3] = option.intr_rate2;
      }
    }

    dataLoaded.value = true;
  } catch (err) {
    console.log(err);
  }
};

const close = () => {
  dialog.value = false;
};

onMounted(fetchUserInfo);

watch(() => route.params.username, fetchUserInfo);

watchEffect(() => {
  if (userComments.value.length) {
    fetchArticleTitles();
  }
});
</script>

<style scoped>
.loading {
  display: flex;
  height: 80vh;
  align-items: center;
  justify-content: center;
}

.progress-circular {
  width: 80px;
  height: 80px;
  border: 5px solid #1089FF;
  border-radius: 50%;
  border-top: 5px solid transparent;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
}

.dialog-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 800px;
  max-width: 90%;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

tbody>tr {
  transition: 200ms;
  cursor: pointer;
}

tbody>tr:hover {
  background-color: rgb(247, 250, 253);
  color: #1089FF;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.table th,
.table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.table th {
  background-color: #f2f2f2;
  text-align: left;
}

.bank-select {
  padding: 10px;
  border: 1px solid #1089FF;
  border-radius: 4px;
}
</style> -->


<!-- ================================================================================================================= -->
<!-- 
<template>
  <div>
    <h1 v-if="user">{{ user.username }} 프로필 페이지</h1>
    <img :src="getProfileImgUrl(user.profile_img)" alt="Profile Image" v-if="user && user.profile_img">
    <p v-if="user">이름: {{ user.name }}</p>
    <p v-if="user">이메일: {{ user.email }}</p>
    <p v-if="user">닉네임: {{ user.nickname }}</p>
    <p v-if="user">나이: {{ user.age }}</p>
    <p v-if="user">현재 자산: {{ user.now_money }}</p>
    <p v-if="user">연봉: {{ user.money_per_year }}</p>
    <p v-if="user">선호 장소: {{ user.fav_place }}</p>
    
    <div><button v-if="isCurrentUser" @click="editProfile">프로필 수정</button></div>

    <ContractedProductView v-if="user" :products="user.deposits" title="계약된 예금" />
    <ContractedProductView v-if="user" :products="user.savings" title="계약된 적금" />


    <h2 v-if="userArticles">작성한 글</h2>
    <ul v-if="userArticles && userArticles.length">
      <li v-for="article in userArticles" :key="article.id">
        <h2>{{ article.title }}</h2>
        <p>{{ article.content }}</p>
        <br>
      </li>
    </ul>
    
    <h2 v-if="userComments">작성한 댓글</h2>
    <ul v-if="userComments.length">
      <li v-for="comment in userComments" :key="comment.id">
        <h2><RouterLink :to="{name:'DetailView',params:{id:comment.article}}">{{ getArticleTitle(comment.article) }}</RouterLink>에 달린 댓글</h2>
        {{ comment.content }}
        <br>
      </li>
    </ul>

    <p v-if="error">{{ error }}</p>
    <p v-if="loading">로딩 중...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import { RouterLink } from 'vue-router';
import ContractedProductView from '@/views/ContractedProductView.vue'; // 새로운 컴포넌트를 임포트

const router = useRouter();
const route = useRoute();
const store = useCounterStore();
const user = ref(null);
const userArticles = ref([]);
const userComments = ref([]);
const articleTitles = ref({});
const error = ref(null);
const loading = ref(false);

const getProfileImgUrl = (imgPath) => {
  return `${store.DJANGO_URL}${imgPath}`;
};

const fetchUserInfo = async () => {
  loading.value = true;
  error.value = null;
  try {
    const username = route.params.username;
    await store.getUserInfo(username);
    user.value = store.userInfo;
    if (user.value) {
      await store.getUserArticles(user.value.id);
      userArticles.value = store.userArticles || [];

      await store.getUserComments(user.value.id);
      userComments.value = store.userComments || [];
    }
  } catch (err) {
    error.value = '사용자 정보를 가져오지 못했습니다.';
  } finally {
    loading.value = false;
  }
};

const getArticleTitle = (articlePk) => {
  return articleTitles.value[articlePk] || '알 수 없는 글';
};

const fetchArticleTitles = async () => {
  for (const comment of userComments.value) {
    if (!articleTitles.value[comment.article]) {
      const article = await store.getArticle(comment.article);
      articleTitles.value[comment.article] = article.title || '알 수 없는 글';
    }
  }
};

const isCurrentUser = computed(() => {
  return store.userInfo && store.userInfo.username === route.params.username;
});

const editProfile = () => {
  router.push({ name: 'ProfileEditView', params: { username: route.params.username } });
};

onMounted(fetchUserInfo);

watch(() => route.params.username, fetchUserInfo);

watchEffect(() => {
  if (userComments.value.length) {
    fetchArticleTitles();
  }
});
</script>

<style scoped>
.loading {
  display: flex;
  height: 80vh;
  align-items: center;
  justify-content: center;
}

.progress-circular {
  width: 80px;
  height: 80px;
  border: 5px solid #1089FF;
  border-radius: 50%;
  border-top: 5px solid transparent;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style> -->





<!-- <template>
  <div>
    <h1 v-if="user">{{ user.username }} 프로필 페이지</h1>
    <img :src="getProfileImgUrl(user.profile_img)" alt="Profile Image" v-if="user && user.profile_img">
    <p v-if="user">이름: {{ user.name }}</p>
    <p v-if="user">이메일: {{ user.email }}</p>
    <p v-if="user">닉네임: {{ user.nickname }}</p>
    <p v-if="user">나이: {{ user.age }}</p>
    <p v-if="user">현재 자산: {{ user.now_money }}</p>
    <p v-if="user">연봉: {{ user.money_per_year }}</p>
    <p v-if="user">선호 장소: {{ user.fav_place }}</p>
    
    <div><button v-if="isCurrentUser" @click="editProfile">프로필 수정</button></div>

    <ContractedProductView v-if="user" :products="user.deposits" title="계약된 예금" />
    <ContractedProductView v-if="user" :products="user.savings" title="계약된 적금" />

    <h2 v-if="userArticles">작성한 글</h2>
    <ul v-if="userArticles && userArticles.length">
      <li v-for="article in userArticles" :key="article.id">
        <h2>{{ article.title }}</h2>
        <p>{{ article.content }}</p>
        <br>
      </li>
    </ul>
    
    <h2 v-if="userComments">작성한 댓글</h2>
    <ul v-if="userComments.length">
      <li v-for="comment in userComments" :key="comment.id">
        <h2><RouterLink :to="{name:'DetailView',params:{id:comment.article}}">{{ getArticleTitle(comment.article) }}</RouterLink>에 달린 댓글</h2>
        {{ comment.content }}
        <br>
      </li>
    </ul>

    <p v-if="error">{{ error }}</p>
    <p v-if="loading">로딩 중...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import { RouterLink } from 'vue-router';
import ContractedProductView from '@/views/ContractedProductView.vue'; // 새로운 컴포넌트를 임포트

const router = useRouter();
const route = useRoute();
const store = useCounterStore();
const user = ref(null);
const userArticles = ref([]);
const userComments = ref([]);
const articleTitles = ref({});
const error = ref(null);
const loading = ref(false);

const getProfileImgUrl = (imgPath) => {
  return `${store.DJANGO_URL}${imgPath}`;
};

const fetchUserInfo = async () => {
  loading.value = true;
  error.value = null;
  try {
    const username = route.params.username;
    await store.getUserInfo(username);
    user.value = store.userInfo;
    if (user.value) {
      await store.getUserArticles(user.value.id);
      userArticles.value = store.userArticles || [];

      await store.getUserComments(user.value.id);
      userComments.value = store.userComments || [];
    }
  } catch (err) {
    error.value = '사용자 정보를 가져오지 못했습니다.';
  } finally {
    loading.value = false;
  }
};

const getArticleTitle = (articlePk) => {
  return articleTitles.value[articlePk] || '알 수 없는 글';
};

const fetchArticleTitles = async () => {
  for (const comment of userComments.value) {
    if (!articleTitles.value[comment.article]) {
      const article = await store.getArticle(comment.article);
      articleTitles.value[comment.article] = article.title || '알 수 없는 글';
    }
  }
};

const isCurrentUser = computed(() => {
  return store.userInfo && store.userInfo.username === route.params.username;
});

const editProfile = () => {
  router.push({ name: 'ProfileEditView', params: { username: route.params.username } });
};

onMounted(fetchUserInfo);

watch(() => route.params.username, fetchUserInfo);

watchEffect(() => {
  if (userComments.value.length) {
    fetchArticleTitles();
  }
});
</script>

<style scoped>
.loading {
  display: flex;
  height: 80vh;
  align-items: center;
  justify-content: center;
}

.progress-circular {
  width: 80px;
  height: 80px;
  border: 5px solid #1089FF;
  border-radius: 50%;
  border-top: 5px solid transparent;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style> -->


<!-- =============================================================================================================================================== -->

<!-- <template>
  <div>
    <h1 v-if="user">{{ user.username }} 프로필 페이지</h1>
    <img :src="getProfileImgUrl(user.profile_img)" alt="Profile Image" v-if="user && user.profile_img">
    <p v-if="user">이름: {{ user.name }}</p>
    <p v-if="user">이메일: {{ user.email }}</p>
    <p v-if="user">닉네임: {{ user.nickname }}</p>
    <p v-if="user">나이: {{ user.age }}</p>
    <p v-if="user">현재 자산: {{ user.now_money }}</p>
    <p v-if="user">연봉: {{ user.money_per_year }}</p>
    <p v-if="user">선호 장소: {{ user.fav_place }}</p>
    
    <div><button v-if="isCurrentUser" @click="editProfile">프로필 수정</button></div>

    <ContractedProductView v-if="user" :products="user.deposits" title="계약된 예금" />
    <ContractedProductView v-if="user" :products="user.savings" title="계약된 적금" />

    <h2 v-if="userArticles">작성한 글</h2>
    <ul v-if="userArticles && userArticles.length">
      <li v-for="article in userArticles" :key="article.id">
        <h2>{{ article.title }}</h2>
        <p>{{ article.content }}</p>
        <br>
      </li>
    </ul>
    
    <h2 v-if="userComments">작성한 댓글</h2>
    <ul v-if="userComments.length">
      <li v-for="comment in userComments" :key="comment.id">
        <h2><RouterLink :to="{name:'DetailView',params:{id:comment.article}}">{{ getArticleTitle(comment.article) }}</RouterLink>에 달린 댓글</h2>
        {{ comment.content }}
        <br>
      </li>
    </ul>

    <p v-if="error">{{ error }}</p>
    <p v-if="loading">로딩 중...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import { RouterLink } from 'vue-router';
import ContractedProductView from '@/views/ContractedProductView.vue'; // 새로운 컴포넌트를 임포트

const router = useRouter();
const route = useRoute();
const store = useCounterStore();
const user = ref(null);
const userArticles = ref([]);
const userComments = ref([]);
const articleTitles = ref({});
const error = ref(null);
const loading = ref(false);

const getProfileImgUrl = (imgPath) => {
  return `${store.DJANGO_URL}${imgPath}`;
};

const fetchUserInfo = async () => {
  loading.value = true;
  error.value = null;
  try {
    const username = route.params.username;
    await store.getUserInfo(username);
    user.value = store.userInfo;
    if (user.value) {
      await store.getUserArticles(user.value.id);
      userArticles.value = store.userArticles || [];

      await store.getUserComments(user.value.id);
      userComments.value = store.userComments || [];
    }
  } catch (err) {
    error.value = '사용자 정보를 가져오지 못했습니다.';
  } finally {
    loading.value = false;
  }
};

const getArticleTitle = (articlePk) => {
  return articleTitles.value[articlePk] || '알 수 없는 글';
};

const fetchArticleTitles = async () => {
  for (const comment of userComments.value) {
    if (!articleTitles.value[comment.article]) {
      const article = await store.getArticle(comment.article);
      articleTitles.value[comment.article] = article.title || '알 수 없는 글';
    }
  }
};

const isCurrentUser = computed(() => {
  return store.userInfo && store.userInfo.username === route.params.username;
});

const editProfile = () => {
  router.push({ name: 'ProfileEditView', params: { username: route.params.username } });
};

onMounted(fetchUserInfo);

watch(() => route.params.username, fetchUserInfo);

watchEffect(() => {
  if (userComments.value.length) {
    fetchArticleTitles();
  }
});
</script>

<style scoped>
.loading {
  display: flex;
  height: 80vh;
  align-items: center;
  justify-content: center;
}

.progress-circular {
  width: 80px;
  height: 80px;
  border: 5px solid #1089FF;
  border-radius: 50%;
  border-top: 5px solid transparent;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style> -->



<!-- <template>
  <div>
    <h1 v-if="user">{{ user.username }} 프로필 페이지</h1>
    <img :src="getProfileImgUrl(user.profile_img)" alt="Profile Image" v-if="user && user.profile_img">
    <p v-if="user">이름: {{ user.name }}</p>
    <p v-if="user">이메일: {{ user.email }}</p>
    <p v-if="user">닉네임: {{ user.nickname }}</p>
    <p v-if="user">나이: {{ user.age }}</p>
    <p v-if="user">현재 자산: {{ user.now_money }}</p>
    <p v-if="user">연봉: {{ user.money_per_year }}</p>
    <p v-if="user">선호 장소: {{ user.fav_place }}</p>
    
    <div><button v-if="isCurrentUser" @click="editProfile">프로필 수정</button></div>

    <ContractedProductView v-if="user && user.deposits.length" :products="user.deposits" title="계약된 예금" />
    <ContractedProductView v-if="user && user.savings.length" :products="user.savings" title="계약된 적금" />

    <h2 v-if="userArticles">작성한 글</h2>
    <ul v-if="userArticles && userArticles.length">
      <li v-for="article in userArticles" :key="article.id">
        <h2>{{ article.title }}</h2>
        <p>{{ article.content }}</p>
        <br>
      </li>
    </ul>
    
    <h2 v-if="userComments">작성한 댓글</h2>
    <ul v-if="userComments.length">
      <li v-for="comment in userComments" :key="comment.id">
        <h2><RouterLink :to="{name:'DetailView',params:{id:comment.article}}">{{ getArticleTitle(comment.article) }}</RouterLink>에 달린 댓글</h2>
        {{ comment.content }}
        <br>
      </li>
    </ul>

    <p v-if="error">{{ error }}</p>
    <p v-if="loading">로딩 중...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import { RouterLink } from 'vue-router';
import ContractedProductView from '@/views/ContractedProductView.vue';

const router = useRouter();
const route = useRoute();
const store = useCounterStore();
const user = ref(null);
const userArticles = ref([]);
const userComments = ref([]);
const articleTitles = ref({});
const error = ref(null);
const loading = ref(false);

const getProfileImgUrl = (imgPath) => {
  return `${store.DJANGO_URL}${imgPath}`;
};

const fetchUserInfo = async () => {
  loading.value = true;
  error.value = null;
  try {
    const username = route.params.username;
    await store.getUserInfo(username);
    user.value = store.userInfo;
    if (user.value) {
      await store.getUserArticles(user.value.id);
      userArticles.value = store.userArticles || [];

      await store.getUserComments(user.value.id);
      userComments.value = store.userComments || [];
    }
  } catch (err) {
    error.value = '사용자 정보를 가져오지 못했습니다.';
  } finally {
    loading.value = false;
  }
};

const getArticleTitle = (articlePk) => {
  return articleTitles.value[articlePk] || '알 수 없는 글';
};

const fetchArticleTitles = async () => {
  for (const comment of userComments.value) {
    if (!articleTitles.value[comment.article]) {
      const article = await store.getArticle(comment.article);
      articleTitles.value[comment.article] = article.title || '알 수 없는 글';
    }
  }
};

const isCurrentUser = computed(() => {
  return store.userInfo && store.userInfo.username === route.params.username;
});

const editProfile = () => {
  router.push({ name: 'ProfileEditView', params: { username: route.params.username } });
};

onMounted(fetchUserInfo);

watch(() => route.params.username, fetchUserInfo);

watchEffect(() => {
  if (userComments.value.length) {
    fetchArticleTitles();
  }
});
</script>

<style scoped>
.loading {
  display: flex;
  height: 80vh;
  align-items: center;
  justify-content: center;
}

.progress-circular {
  width: 80px;
  height: 80px;
  border: 5px solid #1089FF;
  border-radius: 50%;
  border-top: 5px solid transparent;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style> -->


<!-- <template>
  <div>
    <h1 v-if="user">{{ user.username }} 프로필 페이지</h1>
    <img :src="getProfileImgUrl(user.profile_img)" alt="Profile Image" v-if="user && user.profile_img">
    <p v-if="user">이름: {{ user.name }}</p>
    <p v-if="user">이메일: {{ user.email }}</p>
    <p v-if="user">닉네임: {{ user.nickname }}</p>
    <p v-if="user">나이: {{ user.age }}</p>
    <p v-if="user">현재 자산: {{ user.now_money }}</p>
    <p v-if="user">연봉: {{ user.money_per_year }}</p>
    <p v-if="user">선호 장소: {{ user.fav_place }}</p>
    
    <div><button v-if="isCurrentUser" @click="editProfile">프로필 수정</button></div>

    <ContractedProductView
      v-if="user"
      :products="user.deposits"
      title="계약된 예금"
      type="deposit"
    />
    <ContractedProductView
      v-if="user"
      :products="user.savings"
      title="계약된 적금"
      type="saving"
    />

    <h2 v-if="userArticles">작성한 글</h2>
    <ul v-if="userArticles && userArticles.length">
      <li v-for="article in userArticles" :key="article.id">
        <h2>{{ article.title }}</h2>
        <p>{{ article.content }}</p>
        <br>
      </li>
    </ul>
    
    <h2 v-if="userComments">작성한 댓글</h2>
    <ul v-if="userComments.length">
      <li v-for="comment in userComments" :key="comment.id">
        <h2><RouterLink :to="{name:'DetailView',params:{id:comment.article}}">{{ getArticleTitle(comment.article) }}</RouterLink>에 달린 댓글</h2>
        {{ comment.content }}
        <br>
      </li>
    </ul>

    <p v-if="error">{{ error }}</p>
    <p v-if="loading">로딩 중...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import { RouterLink } from 'vue-router';
import ContractedProductView from '@/views/ContractedProductView.vue';

const router = useRouter();
const route = useRoute();
const store = useCounterStore();
const user = ref(null);
const userArticles = ref([]);
const userComments = ref([]);
const articleTitles = ref({});
const error = ref(null);
const loading = ref(false);

const getProfileImgUrl = (imgPath) => {
  return `${store.DJANGO_URL}${imgPath}`;
};

const fetchUserInfo = async () => {
  loading.value = true;
  error.value = null;
  try {
    const username = route.params.username;
    await store.getUserInfo(username);
    user.value = store.userInfo;
    if (user.value) {
      await store.getUserArticles(user.value.id);
      userArticles.value = store.userArticles || [];

      await store.getUserComments(user.value.id);
      userComments.value = store.userComments || [];
    }
  } catch (err) {
    error.value = '사용자 정보를 가져오지 못했습니다.';
  } finally {
    loading.value = false;
  }
};

const getArticleTitle = (articlePk) => {
  return articleTitles.value[articlePk] || '알 수 없는 글';
};

const fetchArticleTitles = async () => {
  for (const comment of userComments.value) {
    if (!articleTitles.value[comment.article]) {
      const article = await store.getArticle(comment.article);
      articleTitles.value[comment.article] = article.title || '알 수 없는 글';
    }
  }
};

const isCurrentUser = computed(() => {
  return store.userInfo && store.userInfo.username === route.params.username;
});

const editProfile = () => {
  router.push({ name: 'ProfileEditView', params: { username: route.params.username } });
};

onMounted(fetchUserInfo);

watch(() => route.params.username, fetchUserInfo);

watchEffect(() => {
  if (userComments.value.length) {
    fetchArticleTitles();
  }
});
</script>

<style scoped>
.loading {
  display: flex;
  height: 80vh;
  align-items: center;
  justify-content: center;
}

.progress-circular {
  width: 80px;
  height: 80px;
  border: 5px solid #1089FF;
  border-radius: 50%;
  border-top: 5px solid transparent;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style> -->


<template>
  <div class="profile-page">
    <div class="profile-header">
      <img :src="getProfileImgUrl(user.profile_img)" alt="Profile Image" class="profile-img" v-if="user && user.profile_img">
      <div class="profile-info">
        <h1 v-if="user">{{ user.username }}의 프로필 페이지</h1>
        <p v-if="user">이름: {{ user.name }}</p>
        <p v-if="user">이메일: {{ user.email }}</p>
        <p v-if="user">닉네임: {{ user.nickname }}</p>
        <p v-if="user">나이: {{ user.age }}</p>
        <p v-if="user">현재 자산: {{ user.now_money }}</p>
        <p v-if="user">연봉: {{ user.money_per_year }}</p>
        <p v-if="user">선호 장소: {{ user.fav_place }}</p>
        <button v-if="isCurrentUser" @click="editProfile" class="edit-profile-button">프로필 수정</button>
      </div>
    </div>

    <div class="contracted-products">
      <ContractedProductView v-if="user" :products="user.deposits" title="계약된 예금" type="deposit" />
      <ContractedProductView v-if="user" :products="user.savings" title="계약된 적금" type="saving" />
    </div>

    <div class="user-articles-comments">
      <div class="user-articles">
        <h2 v-if="userArticles.length">작성한 글</h2>
        <ul v-if="userArticles.length">
          <li v-for="article in userArticles" :key="article.id">
            <h3>{{ article.title }}</h3>
            <p>{{ article.content }}</p>
          </li>
        </ul>
      </div>

      <div class="user-comments">
        <h2 v-if="userComments.length">작성한 댓글</h2>
        <ul v-if="userComments.length">
          <li v-for="comment in userComments" :key="comment.id">
            <h3>
              <RouterLink :to="{ name: 'DetailView', params: { id: comment.article } }">
                {{ getArticleTitle(comment.article) }}
              </RouterLink>에 달린 댓글
            </h3>
            <p>{{ comment.content }}</p>
          </li>
        </ul>
      </div>
    </div>

    <p v-if="error">{{ error }}</p>
    <p v-if="loading">로딩 중...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import { RouterLink } from 'vue-router';
import ContractedProductView from '@/views/ContractedProductView.vue';

const router = useRouter();
const route = useRoute();
const store = useCounterStore();
const user = ref(null);
const userArticles = ref([]);
const userComments = ref([]);
const articleTitles = ref({});
const error = ref(null);
const loading = ref(false);

const getProfileImgUrl = (imgPath) => {
  return `${store.DJANGO_URL}${imgPath}`;
};

const fetchUserInfo = async () => {
  loading.value = true;
  error.value = null;
  try {
    const username = route.params.username;
    await store.getUserInfo(username);
    user.value = store.userInfo;
    if (user.value) {
      await store.getUserArticles(user.value.id);
      userArticles.value = store.userArticles || [];

      await store.getUserComments(user.value.id);
      userComments.value = store.userComments || [];
    }
  } catch (err) {
    error.value = '사용자 정보를 가져오지 못했습니다.';
  } finally {
    loading.value = false;
  }
};

const getArticleTitle = (articlePk) => {
  return articleTitles.value[articlePk] || '알 수 없는 글';
};

const fetchArticleTitles = async () => {
  for (const comment of userComments.value) {
    if (!articleTitles.value[comment.article]) {
      const article = await store.getArticle(comment.article);
      articleTitles.value[comment.article] = article.title || '알 수 없는 글';
    }
  }
};

const isCurrentUser = computed(() => {
  return store.userInfo && store.userInfo.username === route.params.username;
});

const editProfile = () => {
  router.push({ name: 'ProfileEditView', params: { username: route.params.username } });
};

onMounted(fetchUserInfo);

watch(() => route.params.username, fetchUserInfo);

watchEffect(() => {
  if (userComments.value.length) {
    fetchArticleTitles();
  }
});
</script>

<style scoped>
@font-face {
  font-family: 'NEXON Lv1 Gothic Low OTF';
  src: url('@/assets/fonts/NEXON_Lv1_Gothic_Low.otf') format('opentype');
}

.profile-page {
  font-family: 'NEXON Lv1 Gothic Low OTF', sans-serif;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.profile-img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  margin-right: 20px;
}

.profile-info {
  max-width: 600px;
}

.profile-info h1 {
  margin: 0 0 10px;
  font-size: 32px;
}

.profile-info p {
  margin: 8px 0;
  font-size: 18px;
}

.edit-profile-button {
  background-color: #2db2ff;
  color: white;
  border: none;
  padding: 10px 15px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

.edit-profile-button:hover {
  background-color: #0a73d9;
}

.contracted-products {
  margin-top: 20px;
  width: 100%;
}

.user-articles-comments {
  margin-top: 40px;
  width: 100%;
}

.user-articles,
.user-comments {
  margin-bottom: 20px;
}

.user-articles h2,
.user-comments h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

.user-articles ul,
.user-comments ul {
  list-style: none;
  padding: 0;
}

.user-articles li,
.user-comments li {
  margin-bottom: 15px;
}

.user-articles h3,
.user-comments h3 {
  font-size: 20px;
  margin: 0 0 5px;
}
</style>


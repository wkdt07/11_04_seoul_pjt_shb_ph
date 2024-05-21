<template>
  <div>
    <h1>프로필 수정</h1>
    <form @submit.prevent="updateProfile">
      <label for="username">사용자 이름: </label>
      <input type="text" id="username" v-model.trim="form.username" readonly><br>

      <label for="name">이름: </label>
      <input type="text" id="name" v-model.trim="form.name"><br>

      <label for="email">이메일: </label>
      <input type="email" id="email" v-model.trim="form.email"><br>

      <label for="nickname">닉네임: </label>
      <input type="text" id="nickname" v-model.trim="form.nickname"><br>

      <label for="age">나이: </label>
      <input type="number" id="age" v-model.number="form.age"><br>
      
      <label for="now_money">현재 자산: </label>
      <input type="number" id="now_money" v-model.number="form.now_money"><br>
      
      <label for="money_per_year">연봉: </label>
      <input type="number" id="money_per_year" v-model.number="form.money_per_year"><br>

      <label for="fav_place">거주 선호 지역: </label>
      <input type="text" id="fav_place" v-model.trim="form.fav_place"><br>
      
      <label for="desire_amount_saving">저축 목표 금액: </label>
      <input type="number" id="desire_amount_saving" v-model.number="form.desire_amount_saving"><br>
      
      <label for="desire_amount_deposit">예금 목표 금액: </label>
      <input type="number" id="desire_amount_deposit" v-model.number="form.desire_amount_deposit"><br>
      
      <label for="deposit_period">예금 기간: </label>
      <input type="number" id="deposit_period" v-model.number="form.deposit_period"><br>
      
      <label for="saving_period">저축 기간: </label>
      <input type="number" id="saving_period" v-model.number="form.saving_period"><br>

      <label for="profile_img">프로필 이미지: </label>
      <input type="file" id="profile_img" @change="onFileChange"><br>
      
      <input type="submit" value="Update Profile">
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { useRouter } from 'vue-router';  // 라우터 가져오기
const store = useCounterStore();
const form = ref({
  username: '',
  name: '',
  email: '',
  nickname: '',
  age: null,
  now_money: null,
  money_per_year: null,
  fav_place: '',
  desire_amount_saving: null,
  desire_amount_deposit: null,
  deposit_period: null,
  saving_period: null,
  profile_img: null
});

const loadUserProfile = async () => {
  await store.getUserInfo(store.userInfo.username);
  const userInfo = store.userInfo;
  
  form.value.username = userInfo.username;
  form.value.name = userInfo.name;
  form.value.email = userInfo.email;
  form.value.nickname = userInfo.nickname;
  form.value.age = userInfo.age;
  form.value.now_money = userInfo.now_money;
  form.value.money_per_year = userInfo.money_per_year;
  form.value.fav_place = userInfo.fav_place;
  form.value.desire_amount_saving = userInfo.desire_amount_saving;
  form.value.desire_amount_deposit = userInfo.desire_amount_deposit;
  form.value.deposit_period = userInfo.deposit_period;
  form.value.saving_period = userInfo.saving_period;
};

const onFileChange = (event) => {
  form.value.profile_img = event.target.files[0];
};

const router = useRouter()
const updateProfile = async () => {
  const formData = new FormData();
  formData.append('username', form.value.username); // username 필드는 비활성화되지만 포함
  formData.append('name', form.value.name);
  formData.append('email', form.value.email);
  formData.append('nickname', form.value.nickname);
  formData.append('age', form.value.age);
  formData.append('now_money', form.value.now_money);
  formData.append('money_per_year', form.value.money_per_year);
  formData.append('fav_place', form.value.fav_place);
  formData.append('desire_amount_saving', form.value.desire_amount_saving);
  formData.append('desire_amount_deposit', form.value.desire_amount_deposit);
  formData.append('deposit_period', form.value.deposit_period);
  formData.append('saving_period', form.value.saving_period);

  if (form.value.profile_img) {
    formData.append('profile_img', form.value.profile_img);
  }

  await store.updateProfile(formData);
  router.push(`/profile/${form.value.username}`);  // 프로필 페이지로 리디렉션
};

onMounted(loadUserProfile);
</script>

<style scoped>
/* 스타일을 여기에 추가하세요 */
</style>

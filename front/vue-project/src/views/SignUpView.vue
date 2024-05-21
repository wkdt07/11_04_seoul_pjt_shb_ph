<template>
  <div>
    <form @submit.prevent="signUp">
      <label for="username">username : </label>
      <input type="text" id="username" v-model.trim="username"><br>
      <label for="password1">password : </label>
      <input type="password" id="password1" v-model.trim="password1"><br>
      <label for="password2">password confirmation: </label>
      <input type="password" id="password2" v-model.trim="password2"><br>

      <label for="email">이메일: </label>
      <input type="email" id="email" v-model.trim="email"><br>

      <label for="name">이름: </label>
      <input type="text" id="name" v-model.trim="name"><br>

      <label for="nickname">닉네임: </label>
      <input type="text" id="nickname" v-model.trim="nickname"><br>

      <label for="age">나이: </label>
      <input type="number" id="age" v-model.trim="age"><br>
      
      <label for="now_money">현재 자산: </label>
      <input type="number" id="now_money" v-model.trim="now_money"><br>
      
      <label for="money_per_year">연봉: </label>
      <input type="number" id="money_per_year" v-model.trim="money_per_year"><br>

      <label for="fav_place">거주 선호 지역(옵션): </label>
      <input type="text" id="fav_place" v-model.trim="fav_place"><br>

      <label for="profile_img">프로필 이미지(옵션): </label>
      <input type="file" id="profile_img" @change="onFileChange"><br>
      
      <input type="submit" value="SignUp">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';

const username = ref('');
const password1 = ref('');
const password2 = ref('');
const email = ref('');
const name = ref('');
const age = ref('');
const now_money = ref('');
const money_per_year = ref('');
const fav_place = ref('');
const nickname = ref('');
const profile_img = ref(null);

const store = useCounterStore();

const onFileChange = (event) => {
  profile_img.value = event.target.files[0];
};

const signUp = async () => {
  if (password1.value !== password2.value) {
    alert('비밀번호와 비밀번호 확인이 일치하지 않습니다.');
    return;
  }

  if (isNaN(age.value) || isNaN(now_money.value) || isNaN(money_per_year.value)) {
    alert('나이, 현재 자산, 연봉은 숫자여야 합니다.');
    return;
  }

  const formData = new FormData();
  formData.append('username', username.value);
  formData.append('password1', password1.value);
  formData.append('password2', password2.value);
  formData.append('email', email.value);
  formData.append('name', name.value);
  formData.append('age', parseInt(age.value, 10));
  formData.append('now_money', parseInt(now_money.value, 10));
  formData.append('money_per_year', parseInt(money_per_year.value, 10));
  formData.append('fav_place', fav_place.value);
  formData.append('nickname', nickname.value);

  if (profile_img.value) {
    formData.append('profile_img', profile_img.value);
  }

  try {
    await store.signUp(formData);
  } catch (error) {
    console.error('회원가입 중 오류 발생:', error);
  }
};
</script>

<style>

</style>

<!-- <template>
  <div>
    <form @submit.prevent="signUp">
      <label for="username">username : </label>
      <input type="text" id="username" v-model.trim="username"><br>
      <label for="password1">password : </label>
      <input type="password" id="password1" v-model.trim="password1"><br>
      <label for="password2">password confirmation: </label>
      <input type="password" id="password2" v-model.trim="password2"><br>

      <label for="Email"> 이메일(옵션): </label>
      <input type="email" id="Email" v-model.trim="Email"><br>

      <label for="Name">이름: </label>
      <input type="text" id="Name" v-model.trim="Name"><br>

      <label for="Age">나이: </label>
      <input type="text" id="Age" v-model.trim="Age"><br>
      
      <label for="NowMoney">현재 자산: </label>
      <input type="text" id="NowMoney" v-model.trim="NowMoney"><br>
      
      <label for="MoneyPerYear">연봉: </label>
      <input type="text" id="MoneyPerYear" v-model.trim="MoneyPerYear"><br>

      <label for="FavPlace">거주 선호 지역(옵션): </label>
      <input type="text" id="FavPlace" v-model.trim="FavPlace"><br>
      
      <input type="submit" value="SignUp">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';

const username = ref(null);
const password1 = ref(null);
const password2 = ref(null);
const Email = ref(null);
const Name = ref(null);
const Age = ref(null);
const NowMoney = ref(null);
const MoneyPerYear = ref(null);
const FavPlace = ref(null);

const store = useCounterStore();

const signUp = function() {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    email: Email.value,
    name: Name.value,
    age: Age.value,
    now_money: NowMoney.value,
    money_per_year: MoneyPerYear.value,
    fav_place: FavPlace.value,
  };
  store.signUp(payload);
};
</script>

<style>

</style> -->
<template>
  <div>
    <form @submit.prevent="signUp">
      <label for="username">username : </label>
      <input type="text" id="username" v-model.trim="username"><br>
      <label for="password1">password : </label>
      <input type="password" id="password1" v-model.trim="password1"><br>
      <label for="password2">password confirmation: </label>
      <input type="password" id="password2" v-model.trim="password2"><br>

      <label for="Email"> 이메일(옵션): </label>
      <input type="email" id="Email" v-model.trim="Email"><br>

      <label for="Name">이름: </label>
      <input type="text" id="Name" v-model.trim="Name"><br>

      <label for="Age">나이: </label>
      <input type="text" id="Age" v-model.trim="Age"><br>
      
      <label for="NowMoney">현재 자산: </label>
      <input type="text" id="NowMoney" v-model.trim="NowMoney"><br>
      
      <label for="MoneyPerYear">연봉: </label>
      <input type="text" id="MoneyPerYear" v-model.trim="MoneyPerYear"><br>

      <label for="FavPlace">거주 선호 지역(옵션): </label>
      <input type="text" id="FavPlace" v-model.trim="FavPlace"><br>
      
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
const Email = ref('');  // 초기값을 빈 문자열로 설정
const Name = ref('');
const Age = ref('');
const NowMoney = ref('');
const MoneyPerYear = ref('');
const FavPlace = ref('');  // 초기값을 빈 문자열로 설정

const store = useCounterStore();

const signUp = function() {
  if (password1.value !== password2.value) {
    alert('비밀번호와 비밀번호 확인이 일치하지 않습니다.');
    return;
  }

  if (isNaN(Age.value) || isNaN(NowMoney.value) || isNaN(MoneyPerYear.value)) {
    alert('나이, 현재 자산, 연봉은 숫자여야 합니다.');
    return;
  }

  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    email: Email.value || '',  // null 값 대신 빈 문자열을 사용
    name: Name.value,
    age: Age.value || 0,  // null 값 대신 기본값 설정
    now_money: NowMoney.value || 0,  // null 값 대신 기본값 설정
    money_per_year: MoneyPerYear.value || 0,  // null 값 대신 기본값 설정
    fav_place: FavPlace.value || ''  // null 값 대신 빈 문자열을 사용
  };
  
  store.signUp(payload);
};
</script>

<style>

</style>

<!-- <template>
  <div>
    <form @submit.prevent="login">
      <label for="username">username : </label>
      <input
        type="text"
        id="username"
        v-model.trim="username"
      /><br />
      <label for="password">password : </label>
      <input type="password" id="password" v-model.trim="password" /><br />

      <input type="submit" value="login" />
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
const store = useCounterStore();
const username = ref(null);
const password = ref(null);

const login = function () {
  const payload = {
    username: username.value,
    password: password.value,
  };
  store.login(payload);
};
</script>

<style></style> -->

<!-- <template>
  <div class="login-container">
    <div class="logo">
      <img :src="ImgURL" alt="Peek! Logo" />
    </div>
    <span class="Peek">
  Peek!
</span>
    <form @submit.prevent="login" class="login-form">
      <label for="username">유저이름</label>
      <input
        type="text"
        id="username"
        v-model.trim="username"
        placeholder="유저이름을 입력하세요"
      /><br />
      <label for="password">비밀번호</label>
      <input
        type="password"
        id="password"
        v-model.trim="password"
        placeholder="비밀번호를 입력하세요"
      /><br />

      <input type="submit" value="LOG IN" class="login-button" />
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
const store = useCounterStore();
const username = ref(null);
const password = ref(null);
const ImgURL = `${store.DJANGO_URL}/media/images/logo.png`
const login = function () {
  const payload = {
    username: username.value,
    password: password.value,
  };
  store.login(payload);
};
</script>

<style>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f0f2f5;
}

.logo img {
  width: 150px;
  margin-bottom: 20px;
}

.login-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 300px;
  padding: 20px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.login-form label {
  align-self: flex-start;
  margin-bottom: 8px;
  font-size: 14px;
  color: #333333;
}

.login-form input[type="text"],
.login-form input[type="password"] {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.login-form input::placeholder {
  color: #dcdfe6;
}

.login-button {
  width: 100%;
  padding: 10px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}
.Peek {
  /* width: 439px;
  height: 147px;
  margin: 382px 10px 0 0; */
  font-family: Maplestory;
  font-size: 100px;
  font-weight: bold;
  font-stretch: normal;
  font-style: normal;
  line-height: 1.5;
  letter-spacing: normal;
  text-align: center;
  color: #001c43;
}
.login-button:hover {
  background-color: #40a9ff;
}
</style> -->



<template>
  <div class="login-container">
    <div class="logo">
      <img :src="ImgURL" alt="Peek! Logo" />
    </div>
    <span class="peek">
      Peek!
    </span>
    <form @submit.prevent="login" class="login-form">
      <div class="form-group">
        <label for="username">유저이름</label>
        <input type="text" id="username" v-model.trim="username" placeholder="유저이름을 입력하세요" />
      </div>
      <div class="form-group">
        <label for="password">비밀번호</label>
        <input type="password" id="password" v-model.trim="password" placeholder="비밀번호를 입력하세요" />
      </div>
      <input type="submit" value="LOG IN" class="login-button" />
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
const store = useCounterStore();
const username = ref(null);
const password = ref(null);
const ImgURL = `${store.DJANGO_URL}/media/images/logo.png`;
const login = function () {
  const payload = {
    username: username.value,
    password: password.value,
  };
  store.login(payload);
};
</script>

<style>
@font-face {
  font-family: 'NEXON Lv1 Gothic Low OTF';
  src: url('@/assets/NEXON_Lv1_Gothic_Low.otf') format('opentype');
}

@font-face {
  font-family: 'Maplestory';
  src: url('@/assets/fonts/Maplestory.otf') format('opentype');
}

.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f0f2f5;
  font-family: 'NEXON Lv1 Gothic Low OTF';
}

.logo img {
  width: 200px;
  /* 로고 크기 확대 */
  margin-bottom: 20px;
}

.peek {
  font-family: 'Maplestory';
  font-size: 120px;
  /* Peek! 텍스트 크기 확대 */
  font-weight: bold;
  color: #001c43;
  margin-bottom: 20px;
}

.login-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 350px;
  /* 로그인 폼 너비 확대 */
  padding: 30px;
  /* 로그인 폼 패딩 확대 */
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  width: 100%;
  margin-bottom: 20px;
  /* 폼 그룹 간의 간격 확대 */
}

.login-form label {
  display: block;
  margin-bottom: 8px;
  font-size: 18px;
  /* 레이블 텍스트 크기 확대 */
  color: #333333;
}

.login-form input[type="text"],
.login-form input[type="password"] {
  width: 100%;
  padding: 15px;
  /* 입력 필드 패딩 확대 */
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 18px;
  /* 입력 필드 텍스트 크기 확대 */
  box-sizing: border-box;
}

.login-form input::placeholder {
  color: #dcdfe6;
}

.login-button {
  width: 100%;
  padding: 15px;
  /* 로그인 버튼 패딩 확대 */
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 20px;
  /* 로그인 버튼 텍스트 크기 확대 */
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #40a9ff;
}</style>
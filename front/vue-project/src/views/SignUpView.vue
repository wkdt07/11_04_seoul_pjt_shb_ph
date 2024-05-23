<!-- <template>
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

</style> -->

<!-- 
<template>
  <div class="signupview">
    <div>
      <div class="sign-up-to-peek-wrapper">
        <span>Sign up to <span class="peek">Peek!</span></span>
      </div>
      <div class="form-elements">
        <form @submit.prevent="signUp">
          <div class="form-group">
            <label for="username" class="label">유저이름*</label>
            <div class="username">
              <input type="text" id="username" v-model.trim="username" placeholder="유저이름을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="password1" class="label">비밀번호*</label>
            <div class="password">
              <input type="password" id="password1" v-model.trim="password1" placeholder="비밀번호를 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="password2" class="label">비밀번호 확인*</label>
            <div class="password">
              <input type="password" id="password2" v-model.trim="password2" placeholder="비밀번호를 한 번 더 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="email" class="label">이메일*</label>
            <div class="email">
              <input type="email" id="email" v-model.trim="email" placeholder="이메일을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="name" class="label">이름</label>
            <div class="username">
              <input type="text" id="name" v-model.trim="name" placeholder="이름을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="nickname" class="label">닉네임*</label>
            <div class="username">
              <input type="text" id="nickname" v-model.trim="nickname" placeholder="닉네임을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="age" class="label">나이*</label>
            <div class="username">
              <input type="number" id="age" v-model.trim="age" placeholder="나이를 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="now_money" class="label">현재 자산*</label>
            <div class="username">
              <input type="number" id="now_money" v-model.trim="now_money" placeholder="현재 자산을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="money_per_year" class="label">연봉*</label>
            <div class="username">
              <input type="number" id="money_per_year" v-model.trim="money_per_year" placeholder="연봉을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="fav_place" class="label">거주 선호 지역(옵션)</label>
            <div class="username">
              <input type="text" id="fav_place" v-model.trim="fav_place" placeholder="거주 선호 지역을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="profile_img" class="label">프로필 이미지(옵션)</label>
            <div class="username">
              <input type="file" id="profile_img" @change="onFileChange">
            </div>
          </div>

         

          <div class="cta" @click="signUp">
            <span>SIGN UP</span>
          </div>
        </form>
      </div>
    </div>
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

const chooseProfileFile = () => {
  document.getElementById('profile_img').click();
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

<style scoped>
.signupview {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100vh;
  background-color: #fff;
  font-size: 12px;
  color: #333;
  font-family: 'NEXON Lv1 Gothic Low OTF';
}

.sign-up-to-peek-wrapper {
  text-align: center;
  margin-bottom: 20px;
  font-size: 35px;
}

.peek {
  font-family: Maplestory;
  color: #2db2ff;
}

.cta1 {
  border-radius: 3px;
  background-color: #2db2ff;
  width: 263px;
  height: 35px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 9px 14px;
  box-sizing: border-box;
  opacity: 0.5;
  font-size: 14px;
  margin-top: 20px;
  cursor: pointer;
}

.form-elements {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: #333;
}

.form-group {
  width: 375px;
}

.label {
  position: relative;
  line-height: 18px;
  text-transform: uppercase;
  margin-bottom: 5px;
}

.username,
.email,
.password {
  width: 100%;
  border-radius: 3px;
  background-color: #f2f2f2;
  height: 35px;
  display: flex;
  align-items: center;
  padding: 0px 12px;
  box-sizing: border-box;
  color: #757575;
}

.cta {
  border-radius: 3px;
  background-color: #2db2ff;
  width: 375px;
  height: 49.4px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 9px 14px;
  box-sizing: border-box;
  font-size: 14px;
  margin-top: 20px;
  cursor: pointer;
}
</style> -->

<!-- <template>
  <div class="signupview">
    <div>
      <div class="sign-up-to-peek-wrapper">
        <span>Sign up to <span class="peek">Peek!</span></span>
      </div>
      <div class="form-elements">
        <form @submit.prevent="signUp">
          <div class="form-group">
            <label for="username" class="label">유저이름*</label>
            <div class="username">
              <input type="text" id="username" v-model.trim="username" placeholder="유저이름을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="password1" class="label">비밀번호*</label>
            <div class="password">
              <input type="password" id="password1" v-model.trim="password1" placeholder="비밀번호를 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="password2" class="label">비밀번호 확인*</label>
            <div class="password">
              <input type="password" id="password2" v-model.trim="password2" placeholder="비밀번호를 한 번 더 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="email" class="label">이메일*</label>
            <div class="email">
              <input type="email" id="email" v-model.trim="email" placeholder="이메일을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="name" class="label">이름</label>
            <div class="username">
              <input type="text" id="name" v-model.trim="name" placeholder="이름을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="nickname" class="label">닉네임*</label>
            <div class="username">
              <input type="text" id="nickname" v-model.trim="nickname" placeholder="닉네임을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="age" class="label">나이*</label>
            <div class="username">
              <input type="number" id="age" v-model.trim="age" placeholder="나이를 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="now_money" class="label">현재 자산*</label>
            <div class="username">
              <input type="number" id="now_money" v-model.trim="now_money" placeholder="현재 자산을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="money_per_year" class="label">연봉*</label>
            <div class="username">
              <input type="number" id="money_per_year" v-model.trim="money_per_year" placeholder="연봉을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="fav_place" class="label">거주 선호 지역(옵션)</label>
            <div class="username">
              <select id="fav_place" v-model="fav_place">
                <option value="" disabled selected>거주 선호 지역을 선택하세요</option>
                <option v-for="region in store.regions" :key="region" :value="region">{{ region }}</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label for="profile_img" class="label">프로필 이미지(옵션)</label>
            <div class="username">
              <input type="file" id="profile_img" @change="onFileChange">
            </div>
          </div>

          <div class="cta" @click="signUp">
            <span>SIGN UP</span>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
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

    if (fav_place.value) {
      const response = await axios.get(`${DJANGO_URL}/real_estate/get_recent_real_estate/${fav_place.value}/`);
      const recentRealEstate = response.data;
      if (recentRealEstate && recentRealEstate.id) {
        await axios.post(`${DJANGO_URL}/real_estate/link_real_estate_to_user/`, 
          { real_estate_id: recentRealEstate.id }, 
          { headers: { Authorization: `Token ${store.token}` } }
        );
      }
    }

    alert(`${formData.get('username')}님, 성공적으로 회원가입이 완료되었습니다!`);
    await store.login({ username: formData.get('username'), password: formData.get('password1') });
  } catch (err) {
    if (err.response && err.response.data) {
      alert(`회원가입 실패: ${JSON.stringify(err.response.data)}`);
    } else {
      alert('회원가입 요청에 실패했습니다. 다시 시도해 주세요.');
    }
  }
};

onMounted(() => {
  store.fetchRegions();  // store에서 regions를 가져옵니다.
});
</script>

<style scoped>
.signupview {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100vh;
  background-color: #fff;
  font-size: 12px;
  color: #333;
  font-family: 'NEXON Lv1 Gothic Low OTF';
}

.sign-up-to-peek-wrapper {
  text-align: center;
  margin-bottom: 20px;
  font-size: 35px;
}

.peek {
  font-family: Maplestory;
  color: #2db2ff;
}

.cta1 {
  border-radius: 3px;
  background-color: #2db2ff;
  width: 263px;
  height: 35px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 9px 14px;
  box-sizing: border-box;
  opacity: 0.5;
  font-size: 14px;
  margin-top: 20px;
  cursor: pointer;
}

.form-elements {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: #333;
}

.form-group {
  width: 375px;
}

.label {
  position: relative;
  line-height: 18px;
  text-transform: uppercase;
  margin-bottom: 5px;
}

.username,
.email,
.password {
  width: 100%;
  border-radius: 3px;
  background-color: #f2f2f2;
  height: 35px;
  display: flex;
  align-items: center;
  padding: 0px 12px;
  box-sizing: border-box;
  color: #757575;
}

.cta {
  border-radius: 3px;
  background-color: #2db2ff;
  width: 375px;
  height: 49.4px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 9px 14px;
  box-sizing: border-box;
  font-size: 14px;
  margin-top: 20px;
  cursor: pointer;
}
</style> -->


<template>
  <div class="signupview">
    <div>
      <div class="form-elements">
        <form @submit.prevent="signUp">
          <div class="form-group">
            <label for="username" class="label">유저이름*</label>
            <div class="input-container">
              <input type="text" id="username" v-model.trim="username" class="input" placeholder="유저이름을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="password1" class="label">비밀번호*</label>
            <div class="input-container">
              <input type="password" id="password1" v-model.trim="password1" class="input" placeholder="비밀번호를 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="password2" class="label">비밀번호 확인*</label>
            <div class="input-container">
              <input type="password" id="password2" v-model.trim="password2" class="input"
                placeholder="비밀번호를 한 번 더 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="email" class="label">이메일*</label>
            <div class="input-container">
              <input type="email" id="email" v-model.trim="email" class="input" placeholder="이메일을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="name" class="label">이름</label>
            <div class="input-container">
              <input type="text" id="name" v-model.trim="name" class="input" placeholder="이름을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="nickname" class="label">닉네임*</label>
            <div class="input-container">
              <input type="text" id="nickname" v-model.trim="nickname" class="input" placeholder="닉네임을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="age" class="label">나이*</label>
            <div class="input-container">
              <input type="number" id="age" v-model.trim="age" class="input" placeholder="나이를 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="now_money" class="label">현재 자산*</label>
            <div class="input-container">
              <input type="number" id="now_money" v-model.trim="now_money" class="input" placeholder="현재 자산을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="money_per_year" class="label">연봉*</label>
            <div class="input-container">
              <input type="number" id="money_per_year" v-model.trim="money_per_year" class="input"
                placeholder="연봉을 입력하세요">
            </div>
          </div>

          <div class="form-group">
            <label for="fav_place" class="label">거주 선호 지역(옵션)</label>
            <div class="input-container">
              <select id="fav_place" v-model="fav_place" class="input">
                <option value="" disabled selected>거주 선호 지역을 선택하세요</option>
                <option v-for="region in store.regions" :key="region" :value="region">{{ region }}</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label for="profile_img" class="label">프로필 이미지(옵션)</label>
            <div class="input-container">
              <input type="file" id="profile_img" @change="onFileChange" class="input">
            </div>
          </div>

          <button type="submit" class="submit-button">SIGN UP</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
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
  } catch (err) {
    if (err.response && err.response.data) {
      alert(`회원가입 실패: ${JSON.stringify(err.response.data)}`);
    } 
  }
};

onMounted(() => {
  store.fetchRegions();  // store에서 regions를 가져옵니다.
});
</script>

<style scoped>
@font-face {
  font-family: 'NEXON Lv1 Gothic Low OTF';
  src: url('@/assets/fonts/NEXON_Lv1_Gothic_Low.otf') format('opentype');
}

.signupview {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100vh;
  background-color: #fff;
  font-size: 14px;
  color: #333;
  font-family: 'NEXON Lv1 Gothic Low OTF';
  padding: 20px;
  box-sizing: border-box;
}

.sign-up-to-peek-wrapper {
  text-align: center;
  margin-bottom: 20px;
  font-size: 35px;
  font-weight: bold;
}

.peek {
  font-family: Maplestory;
  color: #2db2ff;
}

.form-elements {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  width: 100%;
  max-width: 500px;
  margin-top: 40px;
}

.form-group {
  width: 100%;
  margin-bottom: 20px;
}

.label {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 8px;
}

.input-container {
  display: flex;
  flex-direction: column;
}

.input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  font-family: 'NEXON Lv1 Gothic Low OTF';
  box-sizing: border-box;
}

.submit-button {
  width: 100%;
  padding: 12px;
  background-color: #2db2ff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 18px;
  font-family: 'NEXON Lv1 Gothic Low OTF';
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #0a73d9;
}
</style>

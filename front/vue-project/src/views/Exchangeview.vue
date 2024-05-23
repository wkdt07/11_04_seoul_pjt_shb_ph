<!-- <script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useCounterStore } from '../stores/counter';
import Map from '@/components/Map.vue'
import { RouterView, RouterLink } from 'vue-router'



const store = useCounterStore()

const currency = ref([])
const response = ref([])
const getorgive = ref('송금 받을 때')
const selectCur = ref('미 달러')
const selectCurUnit = ref('USD')
const Ttb = ref(0)
const Tts = ref(0)
const Deal = ref(0)

const carculate = ref(0)
const inputwon = ref(0)
const others = ref(0)

const selections = ['송금 받을 때', '송금 보낼 때', '매매 기준율']

const emit = defineEmits(['ExCurrency'])

onMounted(async () => {
  try {
    const res = await axios.get(`${store.DJANGO_URL}/exchange/get_exchange_data/`) // API URL 수정
    console.log('API 응답:', res.data) // 디버그: API 응답 확인

    response.value = res.data.filter(data => data['ttb'] !== '0')
    console.log('필터링된 응답:', response.value) // 디버그: 필터링된 응답 확인

    if (response.value.length > 0) {
      currency.value = response.value.map(item => item['cur_nm'])
      const units = response.value.map(item => item['cur_unit'])
      emit('ExCurrency', currency.value, units)

      // '미 달러' 정보를 초기 설정
      const usdInfo = response.value.find(item => item['cur_nm'] === '미국 달러')
      if (usdInfo) {
        selectCurUnit.value = usdInfo['cur_unit']
        Ttb.value = Number(usdInfo['ttb'].replaceAll(',', ''))
        Tts.value = Number(usdInfo['tts'].replaceAll(',', ''))
        Deal.value = Number(usdInfo['deal_bas_r'].replaceAll(',', ''))
        // 초기 값 설정 (선택된 통화와 상관 없이 Ttb로 설정하지 않음)
        updateCarculate()
      } else {
        console.error('USD 정보를 응답에서 찾을 수 없습니다.') // 오류 처리: USD 정보를 찾을 수 없음
      }
    } else {
      console.error('필터링 후 데이터를 찾을 수 없습니다.') // 오류 처리: 필터링 후 데이터를 찾을 수 없음
    }
  } catch (error) {
    console.error('환율 데이터를 가져오는 중 오류가 발생했습니다:', error) // 오류 처리: 오류 로그 출력
  }
})

watch([selectCur, getorgive], () => {
  const selectedData = response.value.find(item => item['cur_nm'] === selectCur.value)
  if (selectedData) {
    selectCurUnit.value = selectedData['cur_unit']
    if (selectCur.value === '일본 옌' || selectCur.value === '인도네시아 루피아') {
      Ttb.value = Number(selectedData['ttb'].replaceAll(',', '')) / 100
      Tts.value = Number(selectedData['tts'].replaceAll(',', '')) / 100
      Deal.value = Number(selectedData['deal_bas_r'].replaceAll(',', '')) / 100
    } else {
      Ttb.value = Number(selectedData['ttb'].replaceAll(',', ''))
      Tts.value = Number(selectedData['tts'].replaceAll(',', ''))
      Deal.value = Number(selectedData['deal_bas_r'].replaceAll(',', ''))
    }
    updateCarculate()
    inputEventOther()
  } else {
    console.error('선택된 통화 데이터를 찾을 수 없습니다.') // 오류 처리: 선택된 통화 데이터를 찾을 수 없음
  }
})

const updateCarculate = () => {
  if (getorgive.value === '송금 받을 때') {
    carculate.value = Ttb.value
  } else if (getorgive.value === '송금 보낼 때') {
    carculate.value = Tts.value
  } else {
    carculate.value = Deal.value
  }
}

const inputEventOther = () => {
  inputwon.value = others.value * carculate.value
}

const inputEventKrw = () => {
  others.value = inputwon.value / carculate.value
}

</script>



<template>
  <div class="card">
    <form @submit.prevent="submitForm">
      <div class="container">
        <div class="row">
          <div class="col" :class="{ 'offset-9': true, 'col-3': true }">
            <label for="state-select">기준</label>
            <select id="state-select" v-model="getorgive">
              <option v-for="state in selections" :key="state" :value="state">{{ state }}</option>
            </select>
          </div>
        </div>
        <div class="row">
          <div class="col-3">
            <label for="currency-select">통화 선택</label>
            <select id="currency-select" v-model="selectCur">
              <option v-for="cur in currency" :key="cur" :value="cur">{{ cur }}</option>
            </select>
          </div>
          <div class="col-9">
            <label :for="selectCurUnit">금액</label>
            <input type="number" :id="selectCurUnit" v-model="others" @input="inputEventOther" />
          </div>
        </div>
        <div class="row">
          <div class="col-12">
            <label for="krw-input">KRW</label>
            <input type="number" id="krw-input" v-model="inputwon" @input="inputEventKrw" />
          </div>
        </div>
      </div>
    </form>
  </div>

<Map/>


</template>


<style scoped>
.card {
  border: 1px solid #ddd;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.container {
  display: flex;
  flex-direction: column;
}

.row {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.col {
  flex: 1;
  padding: 8px;
}

.offset-9 {
  margin-left: 75%;
}

input,
select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

label {
  margin-bottom: 4px;
  display: block;
}

input[type="number"] {
  -webkit-appearance: none;
  /* Webkit 브라우저 (Chrome, Safari) */
  -moz-appearance: textfield;
  /* Firefox 브라우저 */
  appearance: none;
  /* 표준 속성 */
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style> -->
<!-- <template>
  <div class="exchange-container">
    <h1 class="page-title">환율 계산기</h1>
    <div class="card">
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="state-select">기준</label>
          <select id="state-select" v-model="getorgive">
            <option v-for="state in selections" :key="state" :value="state">{{ state }}</option>
          </select>
        </div>
        <div class="form-group">
          <label for="currency-select">통화 선택</label>
          <select id="currency-select" v-model="selectCur">
            <option v-for="cur in currency" :key="cur" :value="cur">{{ cur }}</option>
          </select>
        </div>
        <div class="form-group">
          <label :for="selectCurUnit">금액</label>
          <input type="number" :id="selectCurUnit" v-model="others" @input="inputEventOther" placeholder="금액을 입력하세요" />
        </div>
        <div class="form-group">
          <label for="krw-input">KRW</label>
          <input type="number" id="krw-input" v-model="inputwon" @input="inputEventKrw" placeholder="KRW를 입력하세요" />
        </div>
        <button type="submit" class="submit-button">계산</button>
      </form>
    </div>
    <Map />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useCounterStore } from '../stores/counter';
import Map from '@/components/Map.vue'

const store = useCounterStore()

const currency = ref([])
const response = ref([])
const getorgive = ref('송금 받을 때')
const selectCur = ref('미 달러')
const selectCurUnit = ref('USD')
const Ttb = ref(0)
const Tts = ref(0)
const Deal = ref(0)

const carculate = ref(0)
const inputwon = ref(0)
const others = ref(0)

const selections = ['송금 받을 때', '송금 보낼 때', '매매 기준율']

const emit = defineEmits(['ExCurrency'])

onMounted(async () => {
  try {
    const res = await axios.get(`${store.DJANGO_URL}/exchange/get_exchange_data/`)
    response.value = res.data.filter(data => data['ttb'] !== '0')
    if (response.value.length > 0) {
      currency.value = response.value.map(item => item['cur_nm'])
      const units = response.value.map(item => item['cur_unit'])
      emit('ExCurrency', currency.value, units)

      const usdInfo = response.value.find(item => item['cur_nm'] === '미국 달러')
      if (usdInfo) {
        selectCurUnit.value = usdInfo['cur_unit']
        Ttb.value = Number(usdInfo['ttb'].replaceAll(',', ''))
        Tts.value = Number(usdInfo['tts'].replaceAll(',', ''))
        Deal.value = Number(usdInfo['deal_bas_r'].replaceAll(',', ''))
        updateCarculate()
      }
    }
  } catch (error) {
    console.error('환율 데이터를 가져오는 중 오류가 발생했습니다:', error)
  }
})

watch([selectCur, getorgive], () => {
  const selectedData = response.value.find(item => item['cur_nm'] === selectCur.value)
  if (selectedData) {
    selectCurUnit.value = selectedData['cur_unit']
    if (selectCur.value === '일본 옌' || selectCur.value === '인도네시아 루피아') {
      Ttb.value = Number(selectedData['ttb'].replaceAll(',', '')) / 100
      Tts.value = Number(selectedData['tts'].replaceAll(',', '')) / 100
      Deal.value = Number(selectedData['deal_bas_r'].replaceAll(',', '')) / 100
    } else {
      Ttb.value = Number(selectedData['ttb'].replaceAll(',', ''))
      Tts.value = Number(selectedData['tts'].replaceAll(',', ''))
      Deal.value = Number(selectedData['deal_bas_r'].replaceAll(',', ''))
    }
    updateCarculate()
    inputEventOther()
  }
})

const updateCarculate = () => {
  if (getorgive.value === '송금 받을 때') {
    carculate.value = Ttb.value
  } else if (getorgive.value === '송금 보낼 때') {
    carculate.value = Tts.value
  } else {
    carculate.value = Deal.value
  }
}

const inputEventOther = () => {
  inputwon.value = others.value * carculate.value
}

const inputEventKrw = () => {
  others.value = inputwon.value / carculate.value
}
</script>

<style scoped>
@font-face {
  font-family: 'NEXON Lv1 Gothic Low';
  src: url('@/assets/fonts/NEXON_Lv1_Gothic_Low.otf') format('opentype');
}

.exchange-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f0f2f5;
  min-height: 100vh;
  font-family: 'NEXON Lv1 Gothic Low', sans-serif;
}

.page-title {
  font-size: 2em;
  color: #333;
  margin-bottom: 20px;
}

.card {
  background: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #333;
}

input,
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 14px;
}

input[type="number"] {
  -webkit-appearance: none;
  -moz-appearance: textfield;
  appearance: none;
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.submit-button {
  width: 100%;
  padding: 10px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
}

.submit-button:hover {
  background-color: #40a9ff;
}
</style> -->

<template>
  <div class="exchange-container">
    <h1 class="page-title">환율 계산기</h1>
    <div class="card">
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="state-select">기준</label>
          <select id="state-select" v-model="getorgive">
            <option v-for="state in selections" :key="state" :value="state">{{ state }}</option>
          </select>
        </div>
        <div class="form-group">
          <label for="currency-select">통화 선택</label>
          <select id="currency-select" v-model="selectCur">
            <option v-for="cur in currency" :key="cur" :value="cur">{{ cur }}</option>
          </select>
        </div>
        <div class="form-group">
          <label :for="selectCurUnit">금액</label>
          <input type="number" :id="selectCurUnit" v-model="others" @input="inputEventOther" placeholder="금액을 입력하세요" />
        </div>
        <div class="form-group">
          <label for="krw-input">KRW</label>
          <input type="number" id="krw-input" v-model="inputwon" @input="inputEventKrw" placeholder="KRW를 입력하세요" />
        </div>
        <button type="submit" class="submit-button">계산</button>
      </form>
    </div>
    <Map />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useCounterStore } from '../stores/counter';
import Map from '@/components/Map.vue'

const store = useCounterStore()

const currency = ref([])
const response = ref([])
const getorgive = ref('송금 받을 때')
const selectCur = ref('미 달러')
const selectCurUnit = ref('USD')
const Ttb = ref(0)
const Tts = ref(0)
const Deal = ref(0)

const carculate = ref(0)
const inputwon = ref(0)
const others = ref(0)

const selections = ['송금 받을 때', '송금 보낼 때', '매매 기준율']

const emit = defineEmits(['ExCurrency'])

onMounted(async () => {
  try {
    const res = await axios.get(`${store.DJANGO_URL}/exchange/get_exchange_data/`)
    response.value = res.data.filter(data => data['ttb'] !== '0')
    if (response.value.length > 0) {
      currency.value = response.value.map(item => item['cur_nm'])
      const units = response.value.map(item => item['cur_unit'])
      emit('ExCurrency', currency.value, units)

      const usdInfo = response.value.find(item => item['cur_nm'] === '미국 달러')
      if (usdInfo) {
        selectCurUnit.value = usdInfo['cur_unit']
        Ttb.value = Number(usdInfo['ttb'].replaceAll(',', ''))
        Tts.value = Number(usdInfo['tts'].replaceAll(',', ''))
        Deal.value = Number(usdInfo['deal_bas_r'].replaceAll(',', ''))
        updateCarculate()
      }
    }
  } catch (error) {
    console.error('환율 데이터를 가져오는 중 오류가 발생했습니다:', error)
  }
})

watch([selectCur, getorgive], () => {
  const selectedData = response.value.find(item => item['cur_nm'] === selectCur.value)
  if (selectedData) {
    selectCurUnit.value = selectedData['cur_unit']
    if (selectCur.value === '일본 옌' || selectCur.value === '인도네시아 루피아') {
      Ttb.value = Number(selectedData['ttb'].replaceAll(',', '')) / 100
      Tts.value = Number(selectedData['tts'].replaceAll(',', '')) / 100
      Deal.value = Number(selectedData['deal_bas_r'].replaceAll(',', '')) / 100
    } else {
      Ttb.value = Number(selectedData['ttb'].replaceAll(',', ''))
      Tts.value = Number(selectedData['tts'].replaceAll(',', ''))
      Deal.value = Number(selectedData['deal_bas_r'].replaceAll(',', ''))
    }
    updateCarculate()
    inputEventOther()
  }
})

const updateCarculate = () => {
  if (getorgive.value === '송금 받을 때') {
    carculate.value = Ttb.value
  } else if (getorgive.value === '송금 보낼 때') {
    carculate.value = Tts.value
  } else {
    carculate.value = Deal.value
  }
}

const inputEventOther = () => {
  inputwon.value = others.value * carculate.value
}

const inputEventKrw = () => {
  others.value = inputwon.value / carculate.value
}
</script>

<style scoped>
@font-face {
  font-family: 'NEXON Lv1 Gothic Low OTF';
  src: url('@/assets/NEXON_Lv1_Gothic_Low.otf') format('opentype');
}

.exchange-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f0f2f5;
  min-height: 100vh;
  font-family: 'NEXON Lv1 Gothic Low OTF';
  font-weight: bold;
}

.page-title {
  font-size: 2em;
  color: #333;
  margin-bottom: 20px;
  font-family: 'NEXON Lv1 Gothic Low OTF';
  font-weight: bold;

}

.card {
  background: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
  margin-bottom: 20px;
  font-family: 'NEXON Lv1 Gothic Low OTF';
  font-weight: bold;

}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #333;
  font-family: 'NEXON Lv1 Gothic Low OTF';
  font-weight: light;
}

input,
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 14px;
  font-family: 'NEXON Lv1 Gothic Low OTF';
  font-weight: bold;
}

input[type="number"] {
  -webkit-appearance: none;
  -moz-appearance: textfield;
  appearance: none;
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.submit-button {
  width: 100%;
  padding: 10px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-family: 'NEXON Lv1 Gothic Low OTF';

  font-weight: bold;

}

.submit-button:hover {
  font-family: 'NEXON Lv1 Gothic Low OTF';

  background-color: #40a9ff;
}
</style>
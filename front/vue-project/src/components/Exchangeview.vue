
<script setup>
import { useCounterStore } from '../stores/counter'
import {ref, onMounted, watch} from 'vue'
import axios from 'axios'


const store = useCounterStore()

const currency = ref()
const response = ref()
const getorgive = ref('송금 받을 때')
const selectCur  = ref('미 달러')
const selectCurUnit = ref('USD')
const Ttb = ref()
const Tts = ref() 
const Deal = ref() 


const carculate = ref()
const inputwon = ref()
const others = ref()

const selections = ['현찰 살 때', '현찰 팔 때', '매매 기준율']

const emit = defineEmits(['ExCurrency'])


onMounted(() => {
  axios({
    method: 'get',
    url: `${useCounterStore.API_URL}/exchange/`
  })
    .then((res) => {
      response.value = res.data.filter(data => data['ttb'] !== '0')

      currency.value = response.value.map(item => item['cur_nm'])
      const units = response.value.map(item => item['cur_unit'])
      emit('ExCurrency', currency.value, units)
      const usdInfo = response.value.find(item => item['cur_nm'] === '미 달러')
      Ttb.value = Number(usdInfo['ttb'].replaceAll(',', ''))
      Tts.value = Number(usdInfo['tts'].replaceAll(',', ''))
      Deal.value = Number(usdInfo['deal_bas_r'].replaceAll(',', ''))
      carculate.value = Ttb.value
    })
})

watch(selectCur, () => {
  const selectedData = response.value.find(item => item['cur_nm']=== selectCur.value)
  selectCur.value = selectedData['cur_unit']
  if(selectCur.value === '일본 옌' || selectCur.value === '인도네시아 루피아'){
    selectCurUnit.value = selectCurUnit.value.replace('(100)', '')
    Ttb.value = Number(selectedData['ttb'].replaceAll(',', '')) / 100
    Tts.value = Number(selectedData['tts'].replaceAll(',', '')) / 100
    Deal.value = Number(selectedData['deal_bas_r'].replaceAll(',', '')) / 100
  } else {
    Ttb.value = Number(selectedData['ttb'].replaceAll(',',''))
    Tts.value = Number(selectedData['tts'].replaceAll(',',''))
    Deal.value = Number(selectedData['deal_bas_r'].replaceAll(',',''))
  }
  if (getorgive.value === '송금 받으실 때') {
    carculate.value = Ttb.value
  } else if (getorgive.value === '송금 보내실 때') {
    carculate.value = Tts.value
  } else {
    carculate.value = Deal.value
  }
  inputEventOther()
})

</script>


<template>
  <div class="card">
    <!-- 카드를 사용하여 콘텐츠를 감싸는 컨테이너를 만듭니다 -->
    <form @submit.prevent="submitForm">
      <!-- 폼을 만듭니다 -->
      <div class="container">
        <!-- 레이아웃을 위한 컨테이너 -->
        <div class="row">
          <!-- 한 줄을 만듭니다 -->
          <div class="col" :class="{ 'offset-9': true, 'col-3': true }">
            <!-- 3칸을 차지하며 오른쪽으로 9칸 오프셋되는 열을 만듭니다 -->
            <label for="state-select">기준</label>
            <select id="state-select" v-model="getorgive">
              <option v-for="state in selections" :key="state" :value="state">{{ state }}</option>
            </select>
            <!-- 기준을 선택하는 드롭다운 메뉴 -->
          </div>
        </div>

        <div class="row">
          <!-- 한 줄을 만듭니다 -->
          <div class="col-3">
            <!-- 3칸을 차지하는 열을 만듭니다 -->
            <label for="currency-select">통화 선택</label>
            <select id="currency-select" v-model="selectCur">
              <option v-for="cur in currency" :key="cur" :value="cur">{{ cur }}</option>
            </select>
            <!-- 통화를 선택하는 드롭다운 메뉴 -->
          </div>
          <div class="col-9">
            <!-- 9칸을 차지하는 열을 만듭니다 -->
            <label :for="selectCurUnit">금액</label>
            <input
              type="number"
              :id="selectCurUnit"
              v-model="others"
              @input="inputEventOther"
            />
            <!-- 통화 금액을 입력하는 입력 필드 -->
          </div>
        </div>

        <div class="row">
          <!-- 한 줄을 만듭니다 -->
          <div class="col-12">
            <label for="krw-input">KRW</label>
            <input
              type="number"
              id="krw-input"
              v-model="inputwon"
              @input="inputEventKrw"
            />
            <!-- 원화 금액을 입력하는 입력 필드 -->
          </div>
        </div>
      </div>
    </form>
  </div>
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
  -webkit-appearance: none; /* Webkit 브라우저 (Chrome, Safari) */
  -moz-appearance: textfield; /* Firefox 브라우저 */
  appearance: none; /* 표준 속성 */
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>

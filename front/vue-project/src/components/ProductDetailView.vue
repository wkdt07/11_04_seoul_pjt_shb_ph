<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import BarChart from '@/components/BarChart.vue'
import BarChartDetail from '@/components/BarChartDetail.vue'
import axios from 'axios'
import { useCounterStore } from '../stores/counter'

const store = useCounterStore()

const products = ref([])
const dialog = ref(false)
const loading = ref(true)
const chartReady = ref(false)
const detailChartReady = ref(false)
const isDeposit = ref(false)

const selectedProduct = ref()
const selectedProductSimple = ref()
const selectedProductCode = computed(() => {
  return selectedProductSimple.value?.code
})
const isContractProduct = computed(() => {
  if (selectedProductSimple.value?.type === '정기예금'){
    return store.userInfo?.contract_deposit.some(e => e['deposit_code'] === selectedProductCode.value)
  } else if (selectedProductSimple.value?.type === '정기적금'){
    return store.userInfo?.contract_saving.some(e => e['saving_code'] === selectedProductCode.value)
  }
})

const averageIntrRateDeposit = [3.45, 4.08, 3.4, 3.35]
const intrRateDeposit = ref([null, null, null, null])
const intrRate2Deposit = ref([null, null, null, null])

const averageIntrRateSaving = [2.78, 3.62, 3.57, 3.52]
const intrRateF = ref([null, null, null, null])
const intrRate2F = ref([null, null, null, null])
const intrRateS = ref([null, null, null, null])
const intrRate2S = ref([null, null, null, null])

const months = [
  { title: '6개월 금리', value: 6 }, 
  { title: '12개월 금리', value: 12 }, 
  { title: '24개월 금리', value: 24 }, 
  { title: '36개월 금리', value: 36 }
]

const selectedMonth = ref({ title: '6개월 금리', value: 6 })
const averageIntrRate = computed(() => {
  if (selectedMonth.value.value === 6) {
    return 3.45
  } else if (selectedMonth.value.value === 12) {
    return 4.08
  } else if (selectedMonth.value.value === 24) {
    return 3.4
  } else if (selectedMonth.value.value === 36) {
    return 3.35
  } else {
    return 3.45
  }
})

const labels = ref(['평균 금리'])
const filterLabels = function () {
  for (const product of products.value) {
    labels.value.push(product.name)
  }
}
watch(products, () => {
  chartReady.value = false
  loading.value = true
  labels.value = ['평균 금리']
  intrRate.value = [averageIntrRate.value]
  intrRate2.value = [undefined]
  setTimeout(() => {
    Promise.all([changeMonth(), filterLabels()])
      .then(() => {
        loading.value = false
        chartReady.value = true
      })
  }, 300)
})

const intrRate = ref([averageIntrRate.value])
const intrRate2 = ref([undefined])

const changeMonth = function () {
  const filteredProduct = products.value.map(e => {
    const tempMonth = selectedMonth.value.value || selectedMonth.value
    return e.options.filter(ele => ele.saveTrm == tempMonth)[0]
  })
  
  for (const product of filteredProduct) {
    intrRate.value.push(product?.intrRate)
    intrRate2.value.push(product?.intrRate2)
  }
}

watch(selectedMonth, () => {
  chartReady.value = false
  loading.value = true
  labels.value = ['평균 금리']

  intrRate.value = [averageIntrRate.value]
  intrRate2.value = [undefined]
  setTimeout(() => {
    Promise.all([changeMonth(), filterLabels()])
      .then(() => {
        loading.value = false
        chartReady.value = true
      })
  }, 300)
})

const getProducts = function () {
  const deposits = store.userContractDeposits
  const savings = store.userContractSavings
  let id = 1

  for (const deposit of deposits) {
    const temp = {
      id: id++,
      code: deposit.deposit_code,
      type: '정기예금',
      bankName: deposit.kor_co_nm,
      name: deposit.name,
      options: []
    }

    for (const option of deposit.depositoption_set) {
      const optionTemp = {
        'intrRate': option.intr_rate,
        'intrRate2': option.intr_rate2,
        'intrRateTypeNm': option.intr_rate_type_nm,
        saveTrm: option.save_trm
      }
      temp.options.push(optionTemp)
    }

    products.value.push(temp)
  }

  for (const saving of savings) {
    const temp = {
      id: id++,
      code: saving.saving_code,
      type: '정기적금',
      bankName: saving.kor_co_nm,
      name: saving.fin_prdt_nm,
      options: []
    }

    for (const option of saving.options) {
      const optionTemp = {
        'intrRate': option.intr_rate,
        'intrRate2': option.intr_rate2,
        'intrRateTypeNm': option.intr_rate_type_nm,
        saveTrm: option.save_trm,
        rsrvTypeNm: option.rsrv_type_nm
      }
      temp.options.push(optionTemp)
    }
    products.value.push(temp)
  }
}

onMounted(() => {
  getProducts()
  Promise.all([changeMonth(), filterLabels()])
    .then(() => {
      loading.value = false
      chartReady.value = true
    })
})

const close = function () {
  dialog.value = false
}

const clickDetail = function (data) {
  detailChartReady.value = false
  selectedProductSimple.value = data
  isDeposit.value = data.type === '정기예금' ? true : false
  intrRateDeposit.value = []
  intrRate2Deposit.value = []
  intrRateF.value = []
  intrRate2F.value = []
  intrRateS.value = []
  intrRate2S.value = []
  getProduct()
  dialog.value = true
}

const getProduct = function () {
  let url = ''
  if (isDeposit.value) {
    url = `${store.API_URL}/financial/deposit_list/${selectedProductCode.value}/`
  } else {
    url = `${store.API_URL}/financial/saving_list/${selectedProductCode.value}/`
  }

  axios.get(url)
    .then((res) => {
      const data = res.data
      const userCount = data.conteact_users || 0
      selectedProduct.value = {
        '가입자 수' : userCount,
        '공시 제출월': data['dcls_month'],
        '금융 회사명': data['kor_co_nm'],
        '금융 상품명': data['fin_prdt_nm'],
        '가입 방법': data['join_way'],
        '만기 후 이자율': data['mtrt_int'],
        '우대 조건': data['spcl_cnd'],
        '가입 대상': data['join_member'],
        '가입 제한': data['join_deny'] === 1 ? '제한없음' : data['join_deny'] === 2 ? '서민전용' : '일부제한',
        '최고 한도': data['max_limit'],
        '기타 유의사항': data['etc_note']
      }

      if (isDeposit.value) {
        const optionList = res.data.options

        for (const option of optionList) {
          if (option.save_trm === "6") {
            intrRateDeposit.value[0] = option.intr_rate
            intrRate2Deposit.value[0] = option.intr_rate2
          } else if (option.save_trm === "12") {
            intrRateDeposit.value[1] = option.intr_rate
            intrRate2Deposit.value[1] = option.intr_rate2
          } else if (option.save_trm === "24") {
            intrRateDeposit.value[2] = option.intr_rate
            intrRate2Deposit.value[2] = option.intr_rate2
          } else if (option.save_trm === "36") {
            intrRateDeposit.value[3] = option.intr_rate
            intrRate2Deposit.value[3] = option.intr_rate2
          }
        }
      } else {
        const optionList = res.data.options

        for (const option of optionList) {
          if (option.rsrv_type_nm === '자유적립식') {
            if (option.save_trm === "6") {
              intrRateF.value[0] = option.intr_rate
              intrRate2F.value[0] = option.intr_rate2
            } else if (option.save_trm === "12") {
              intrRateF.value[1] = option.intr_rate
              intrRate2F.value[1] = option.intr_rate2
            } else if (option.save_trm === "24") {
              intrRateF.value[2] = option.intr_rate
              intrRate2F.value[2] = option.intr_rate2
            } else if (option.save_trm === "36") {
              intrRateF.value[3] = option.intr_rate
              intrRate2F.value[3] = option.intr_rate2
            }
          } else {
            if (option.save_trm === "6") {
              intrRateS.value[0] = option.intr_rate
              intrRate2S.value[0] = option.intr_rate2
            } else if (option.save_trm === "12") {
              intrRateS.value[1] = option.intr_rate
              intrRate2S.value[1] = option.intr_rate2
            } else if (option.save_trm === "24") {
              intrRateS.value[2] = option.intr_rate
              intrRate2S.value[2] = option.intr_rate2
            } else if (option.save_trm === "36") {
              intrRateS.value[3] = option.intr_rate
              intrRate2S.value[3] = option.intr_rate2
            }
          }
        }
      }
      detailChartReady.value = true
    })
    .catch((err) => {
      console.log(err)
    })
}

const deleteProductUser = function (data) {
  const answer = window.confirm('정말 가입을 취소하시겠습니까?')
  isDeposit.value = data.type === '정기예금' ? true : false

  if (answer) {
    selectedProductSimple.value = data
    let url = ''
    if (isDeposit.value) {
      url = `${store.API_URL}/financial/deposit_list/${selectedProductCode.value}/contract/`
    } else {
      url = `${store.API_URL}/financial/saving_list/${selectedProductCode.value}/contract/`
    }

    axios.delete(url, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    .then(() => {
      loading.value = true
      store.getUserInfo(store.userInfo.username)
      products.value = []
      dialog.value = false
      setTimeout(() => {
        getProducts()
        loading.value = false
      }, 300)
    })
    .catch((err) => {
      console.log(err)
    })
  }
}
</script>

<template>
  <div>
    <h1><span class="color">{{ store.userInfo.name }}</span>님의 가입 상품 관리 페이지</h1>
    <hr class="my-3">

    <div v-if="dialog" class="dialog" @click.self="close">
      <div v-if="selectedProduct" class="card py-5 px-3">
        <div class="card-title d-flex align-center justify-space-between">
          <h3>{{ selectedProduct['금융 상품명'] }}</h3>
          <div v-if="store.isLogin">
            <button
              v-if="isContractProduct"
              class="btn btn-flat red"
              @click.prevent="deleteProductUser(selectedProductSimple)"
            >가입 취소하기</button>
          </div>
        </div>

        <div class="card-text">
          <table>
            <tbody>
              <tr v-for="(value, key) in selectedProduct" :key="key">
                <td width="25%" class="font-weight-bold">{{ key }}</td>
                <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
                <td v-else>{{ value }}</td>
              </tr>
            </tbody>
          </table>
          <hr class="my-3">

          <div v-if="detailChartReady">
            <div v-if="isDeposit" class="mx-auto">
              <BarChartDetail
                :title="selectedProductSimple.name"
                :average-intr-rate="averageIntrRateDeposit"
                :intr-rate="intrRateDeposit"
                :intr-rate2="intrRate2Deposit"
              />
              <p class="text-caption">* 개월별 평균 예금 금리는 2023년 11월 기준입니다.</p>
            </div>

            <div v-else class="mx-auto">
              <BarChartDetail
                :title="`${selectedProductSimple.name} (자유적립식)`"
                :average-intr-rate="averageIntrRateSaving"
                :intr-rate="intrRateF"
                :intr-rate2="intrRate2F"
              />
              <BarChartDetail
                :title="`${selectedProductSimple.name} (정액적립식)`"
                :average-intr-rate="averageIntrRateSaving"
                :intr-rate="intrRateS"
                :intr-rate2="intrRate2S"
              />
              <p class="text-caption">* 개월별 평균 예금 금리는 2023년 11월 기준입니다.</p>
            </div>
          </div>
        </div>

        <div class="card-actions">
          <span class="spacer"></span>
          <button class="btn btn-text" @click="close">닫기</button>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="row">
        <div class="col-3">
          <h2>가입한 상품들</h2>
        </div>
        <div class="col-9 d-flex flex-column">
          <p v-if="products.length !== 0" v-for="product in products" :key="product.code" class="mb-2">
            {{ product.id }} : ({{ product.type }}) {{ product.bankName }} - <span class="color">{{ product.name }}</span>
            <button
              class="btn btn-tonal blue-grey mx-2"
              @click.prevent="clickDetail(product)"
            >상세 보기</button>
            <button
              class="btn btn-tonal red"
              @click.prevent="deleteProductUser(product)"
            >가입 취소하기</button>
          </p>
          <p v-else class="mb-15">MIFI에서 가입한 상품이 없습니다! 금리 비교 탭에서 마음에 드는 상품을 선택해보세요 😊</p>
        </div>
      </div>

      <div class="row">
        <div class="col-3">
          <h2>가입한 상품 금리</h2>
          <select
            v-model="selectedMonth"
            class="form-select my-3"
          >
            <option v-for="month in months" :value="month" :key="month.value">{{ month.title }}</option>
          </select>
        </div>
        <div v-if="chartReady" class="col-9">
          <BarChart
            :selected-month="selectedMonth"
            :labels="labels"
            :intr-rate="intrRate"
            :intr-rate2="intrRate2"
          />
          <p class="text-caption">* 개월별 평균 금리는 2023년 11월 기준입니다.</p>
        </div>
        <div v-else class="col-9" style="height: 405px;"></div>
      </div>
    </div>
    <div v-if="loading" class="loading">
      <div class="progress-circular">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.loading {
  position: absolute;
  left: 0;
  top: 0;
  background-color: rgba(255, 255, 255, 0.6);
  display: flex;
  width: 100vw;
  height: 100vh;
  align-items: center;
  justify-content: center;
}

tbody > tr {
  transition: 200ms;
  cursor: pointer;
}

tbody > tr:hover {
  background-color: rgb(247, 250, 253);
  color: #1089FF;
}

.dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  width: 100%;
  padding: 20px;
}

.card-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-text {
  margin-top: 20px;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.btn {
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-flat {
  background: none;
  color: inherit;
}

.btn-red {
  background: red;
  color: white;
}

.btn-blue-grey {
  background: blue-grey;
  color: white;
}

.btn-tonal {
  background: rgba(0, 0, 0, 0.1);
  color: inherit;
}

.btn-text {
  background: none;
  color: #1089FF;
}

.container {
  padding: 20px;
}

.row {
  display: flex;
  margin-bottom: 20px;
}

.col-3 {
  flex: 0 0 25%;
}

.col-9 {
  flex: 0 0 75%;
}

.d-flex {
  display: flex;
}

.flex-column {
  flex-direction: column;
}

.mx-2 {
  margin-left: 8px;
  margin-right: 8px;
}

.my-3 {
  margin-top: 12px;
  margin-bottom: 12px;
}

.mb-2 {
  margin-bottom: 8px;
}

.mb-15 {
  margin-bottom: 15px;
}

.color {
  color: #1089FF;
}

.text-caption {
  font-size: 12px;
  color: grey;
}

.progress-circular {
  color: #1089FF;
}

.spinner-border {
  width: 80px;
  height: 80px;
  border-width: 5px;
}
</style>

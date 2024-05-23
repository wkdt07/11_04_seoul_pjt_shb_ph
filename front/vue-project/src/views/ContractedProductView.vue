<!-- <template>
  <div>
    <h2 v-if="products && products.length">{{ title }}</h2>
    <ul v-if="products && products.length">
      <li v-for="product in products" :key="product.fin_prdt_cd" @click="clickProduct(product)">
        {{ product.fin_prdt_nm }}
      </li>
    </ul>

    <div v-if="dialog" class="dialog">
      <div class="dialog-content">
        <h3>{{ selectedProduct?.fin_prdt_nm }}</h3>
        <div v-if="store.isLogin">
          <button @click.prevent="deleteProduct">가입 취소하기</button>
        </div>

        <table>
          <tbody>
            <tr v-for="(value, key) in selectedProductDetails" :key="key">
              <td width="28%" class="font-weight-bold">{{ key }}</td>
              <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
              <td v-else>{{ value }}</td>
            </tr>
          </tbody>
        </table>
        <hr class="my-3">
        <div class="mx-auto" v-if="dataLoaded">
          <BarChartDetail
            :title="selectedProduct.fin_prdt_nm"
            :average-intr-rate="averageIntrRate"
            :intr-rate="intrRate"
            :intr-rate2="intrRate2"
          />
          <p class="text-caption">* 개월별 평균 금리는 2023년 11월 기준입니다.</p>
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
import { ref, computed } from 'vue';
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';
import BarChartDetail from '@/components/BarChartDetailView.vue';

const props = defineProps({
  products: {
    type: Array,
    required: true
  },
  title: {
    type: String,
    required: true
  }
});

const store = useCounterStore();
const selectedProduct = ref(null);
const selectedProductCode = computed(() => selectedProduct.value?.fin_prdt_cd);
const selectedProductDetails = ref({});
const dialog = ref(false);
const averageIntrRate = [3.45, 4.08, 3.4, 3.35];
const intrRate = ref([null, null, null, null]);
const intrRate2 = ref([null, null, null, null]);
const dataLoaded = ref(false);
const loading = ref(false);

const clickProduct = async (product) => {
  selectedProduct.value = product;
  intrRate.value = [];
  intrRate2.value = [];
  dataLoaded.value = false;
  await getProductDetails();
  dialog.value = true;
};

const getProductDetails = async () => {
  if (!selectedProductCode.value) {
    console.error('selectedProductCode is null or undefined');
    return;
  }

  const url = props.title.includes('예금')
    ? `${store.DJANGO_URL}/financial/deposit_list/${selectedProductCode.value}/`
    : `${store.DJANGO_URL}/financial/saving_list/${selectedProductCode.value}/`;

  try {
    const res = await axios.get(url);
    const data = res.data;
    selectedProductDetails.value = {
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
      const term = parseInt(option.save_trm) / 6 - 1;
      if (term >= 0 && term < 4) {
        intrRate.value[term] = option.intr_rate;
        intrRate2.value[term] = option.intr_rate2;
      }
    }

    dataLoaded.value = true;
  } catch (err) {
    console.log(err);
  }
};

const deleteProduct = async () => {
  const url = props.title.includes('예금')
    ? `${store.DJANGO_URL}/financial/deposit_list/${selectedProductCode.value}/contract/`
    : `${store.DJANGO_URL}/financial/saving_list/${selectedProductCode.value}/contract/`;

  try {
    await axios.delete(url, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    });

    if (props.title.includes('예금')) {
      store.userInfo.deposits = store.userInfo.deposits.filter(deposit => deposit.fin_prdt_cd !== selectedProductCode.value);
    } else {
      store.userInfo.savings = store.userInfo.savings.filter(saving => saving.fin_prdt_cd !== selectedProductCode.value);
    }

    dialog.value = false;
  } catch (error) {
    console.error('Failed to delete product:', error);
  }
};

const close = () => {
  dialog.value = false;
};
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
</style> -->
<!-- <template>
  <div>
    <h2 v-if="products && products.length">{{ title }}</h2>
    <table v-if="products && products.length" class="table">
      <thead>
        <tr>
          <th v-for="header in headers" :key="header.key" :align="header.align" :width="header.width">
            {{ header.title }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.fin_prdt_cd" @click="clickProduct(product)">
          <td>{{ product.dcls_month }}</td>
          <td>{{ product.kor_co_nm }}</td>
          <td align="center">{{ product.fin_prdt_nm }}</td>
          <td align="center">{{ getRate(product, '6') }}</td>
          <td align="center">{{ getRate(product, '12') }}</td>
          <td align="center">{{ getRate(product, '24') }}</td>
          <td align="center">{{ getRate(product, '36') }}</td>
        </tr>
      </tbody>
    </table>

    <div v-if="dialog" class="dialog">
      <div class="dialog-content">
        <h3>{{ selectedProduct?.fin_prdt_nm }}</h3>
        <div v-if="store.isLogin">
          <button @click.prevent="deleteProduct">가입 취소하기</button>
        </div>

        <table>
          <tbody>
            <tr v-for="(value, key) in selectedProductDetails" :key="key">
              <td width="28%" class="font-weight-bold">{{ key }}</td>
              <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
              <td v-else>{{ value }}</td>
            </tr>
          </tbody>
        </table>
        <hr class="my-3">
        <div class="mx-auto" v-if="dataLoaded">
          <BarChartDetail
            :title="selectedProduct.fin_prdt_nm"
            :average-intr-rate="averageIntrRate"
            :intr-rate="intrRate"
            :intr-rate2="intrRate2"
          />
          <p class="text-caption">* 개월별 평균 금리는 2023년 11월 기준입니다.</p>
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
import { ref, computed } from 'vue';
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';
import BarChartDetail from '@/components/BarChartDetailView.vue';

const props = defineProps({
  products: {
    type: Array,
    required: true
  },
  title: {
    type: String,
    required: true
  }
});

const headers = [
  { title: '공시 제출일', align: 'start', sortable: false, width: '10%', key: 'dcls_month' },
  { title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
  { title: '상품명', align: 'center', sortable: false, width: '32%', key: 'fin_prdt_nm' },
  { title: '6개월', align: 'end', width: '12%', key: '6month' },
  { title: '12개월', align: 'end', width: '12%', key: '12month' },
  { title: '24개월', align: 'end', width: '12%', key: '24month' },
  { title: '36개월', align: 'end', width: '12%', key: '36month' },
];

const store = useCounterStore();
const selectedProduct = ref(null);
const selectedProductCode = computed(() => selectedProduct.value?.fin_prdt_cd);
const selectedProductDetails = ref({});
const dialog = ref(false);
const averageIntrRate = [3.45, 4.08, 3.4, 3.35];
const intrRate = ref([null, null, null, null]);
const intrRate2 = ref([null, null, null, null]);
const dataLoaded = ref(false);
const loading = ref(false);

const clickProduct = async (product) => {
  selectedProduct.value = product;
  intrRate.value = [];
  intrRate2.value = [];
  dataLoaded.value = false;
  await getProductDetails();
  dialog.value = true;
};

const getProductDetails = async () => {
  if (!selectedProductCode.value) {
    console.error('selectedProductCode is null or undefined');
    return;
  }

  const url = props.title.includes('예금')
    ? `${store.DJANGO_URL}/financial/deposit_list/${selectedProductCode.value}/`
    : `${store.DJANGO_URL}/financial/saving_list/${selectedProductCode.value}/`;

  try {
    const res = await axios.get(url);
    const data = res.data;
    selectedProductDetails.value = {
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
      const term = parseInt(option.save_trm) / 6 - 1;
      if (term >= 0 && term < 4) {
        intrRate.value[term] = option.intr_rate;
        intrRate2.value[term] = option.intr_rate2;
      }
    }

    dataLoaded.value = true;
  } catch (err) {
    console.log(err);
  }
};

const deleteProduct = async () => {
  const url = props.title.includes('예금')
    ? `${store.DJANGO_URL}/financial/deposit_list/${selectedProductCode.value}/contract/`
    : `${store.DJANGO_URL}/financial/saving_list/${selectedProductCode.value}/contract/`;

  try {
    await axios.delete(url, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    });

    if (props.title.includes('예금')) {
      store.userInfo.deposits = store.userInfo.deposits.filter(deposit => deposit.fin_prdt_cd !== selectedProductCode.value);
    } else {
      store.userInfo.savings = store.userInfo.savings.filter(saving => saving.fin_prdt_cd !== selectedProductCode.value);
    }

    dialog.value = false;
  } catch (error) {
    console.error('Failed to delete product:', error);
  }
};

const close = () => {
  dialog.value = false;
};

const getRate = (product, term) => {
  const option = product.options.find(option => option.save_trm === term);
  return option ? option.intr_rate : '-';
};
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
</style> -->
<!-- <template>
  <div>
    <p>{{ products }}</p>
    <h2 v-if="products && products.length">{{ title }}</h2>
    <table v-if="products && products.length" class="table">
      <thead>
        <tr>
          <th v-for="header in headers" :key="header.key" :align="header.align" :width="header.width">
            {{ header.title }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.fin_prdt_cd" @click="clickProduct(product)">
        
          <td>{{ product.dcls_month }}</td>
          <td>{{ product.kor_co_nm }}</td>
          <td align="center">{{ product.fin_prdt_nm }}</td>
          <td align="center">{{ getRate(product, '6') }}</td>
          <td align="center">{{ getRate(product, '12') }}</td>
          <td align="center">{{ getRate(product, '24') }}</td>
          <td align="center">{{ getRate(product, '36') }}</td>
        </tr>
      </tbody>
    </table>


    <div v-if="dialog" class="dialog">
      <div class="dialog-content">
        <h3>{{ selectedProduct?.fin_prdt_nm }}</h3>
        <div v-if="store.isLogin">
          <button @click.prevent="deleteProduct">가입 취소하기</button>
        </div>

        <table>
          <tbody>
            <tr v-for="(value, key) in selectedProductDetails" :key="key">
              <td width="28%" class="font-weight-bold">{{ key }}</td>
              <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
              <td v-else>{{ value }}</td>
            </tr>
          </tbody>
        </table>
        <hr class="my-3">
        <div class="mx-auto" v-if="dataLoaded">
          <BarChartDetail
            :title="selectedProduct.fin_prdt_nm"
            :average-intr-rate="averageIntrRate"
            :intr-rate="intrRate"
            :intr-rate2="intrRate2"
          />
          <p class="text-caption">* 개월별 평균 금리는 2023년 11월 기준입니다.</p>
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
import { ref, computed } from 'vue';
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';
import BarChartDetail from '@/components/BarChartDetailView.vue';

const props = defineProps({
  products: {
    type: Array,
    required: true
  },
  title: {
    type: String,
    required: true
  }
});

const headers = [
  { title: '공시 제출일', align: 'start', sortable: false, width: '10%', key: 'dcls_month' },
  { title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
  { title: '상품명', align: 'center', sortable: false, width: '32%', key: 'fin_prdt_nm' },
  { title: '6개월', align: 'end', width: '12%', key: '6month' },
  { title: '12개월', align: 'end', width: '12%', key: '12month' },
  { title: '24개월', align: 'end', width: '12%', key: '24month' },
  { title: '36개월', align: 'end', width: '12%', key: '36month' },
];

const store = useCounterStore();
const selectedProduct = ref(null);
const selectedProductCode = computed(() => selectedProduct.value?.fin_prdt_cd);
const selectedProductDetails = ref({});
const dialog = ref(false);
const averageIntrRate = [3.45, 4.08, 3.4, 3.35];
const intrRate = ref([null, null, null, null]);
const intrRate2 = ref([null, null, null, null]);
const dataLoaded = ref(false);
const loading = ref(false);

const clickProduct = async (product) => {
  selectedProduct.value = product;
  intrRate.value = [];
  intrRate2.value = [];
  dataLoaded.value = false;
  await getProductDetails();
  dialog.value = true;

};

const getProductDetails = async () => {
  if (!selectedProductCode.value) {
    console.error('selectedProductCode is null or undefined');
    return;
  }

  const url = props.title.includes('예금')
    ? `${store.DJANGO_URL}/financial/deposit_list/${selectedProductCode.value}/`
    : `${store.DJANGO_URL}/financial/saving_list/${selectedProductCode.value}/`;

  try {
    const res = await axios.get(url);
    const data = res.data;
    selectedProductDetails.value = {
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
      const term = parseInt(option.save_trm) / 6 - 1;
      if (term >= 0 && term < 4) {
        intrRate.value[term] = option.intr_rate;
        intrRate2.value[term] = option.intr_rate2;
      }
    }

    dataLoaded.value = true;
  
  } catch (err) {
    console.log(err);
  }
};

const deleteProduct = async () => {
  const url = props.title.includes('예금')
    ? `${store.DJANGO_URL}/financial/deposit_list/${selectedProductCode.value}/contract/`
    : `${store.DJANGO_URL}/financial/saving_list/${selectedProductCode.value}/contract/`;

  try {
    await axios.delete(url, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    });

    if (props.title.includes('예금')) {
      store.userInfo.deposits = store.userInfo.deposits.filter(deposit => deposit.fin_prdt_cd !== selectedProductCode.value);
    } else {
      store.userInfo.savings = store.userInfo.savings.filter(saving => saving.fin_prdt_cd !== selectedProductCode.value);
    }

    dialog.value = false;
  } catch (error) {
    console.error('Failed to delete product:', error);
  }
};

const close = () => {
  dialog.value = false;
};

const getRate = (product, term) => {
  const option = product.options.find(option => option.save_trm === term);
  return option ? option.intr_rate : '-';
};
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
</style> -->
<!-- <template>
  <div>
    <h2>{{ title }}</h2>
    <ul>
      <li v-for="product in products" :key="product.fin_prdt_cd" @click="clickProduct(product)">
        {{ product.fin_prdt_nm }}
      </li>
    </ul>
    
    <div v-if="dialog" class="dialog">
      <div class="dialog-content">
        <h3>{{ selectedProduct?.fin_prdt_nm }}</h3>
        <div v-if="store.isLogin">
          <button @click.prevent="deleteProductUser">가입 취소하기</button>
        </div>

        <table>
          <tbody>
            <tr v-for="(value, key) in selectedProductDetails" :key="key">
              <td width="28%" class="font-weight-bold">{{ key }}</td>
              <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
              <td v-else>{{ value }}</td>
            </tr>
          </tbody>
        </table>
        <hr class="my-3">
        <div class="mx-auto" v-if="dataLoaded">
          <BarChartDetail
            v-if="isDeposit"
            :title="selectedProductSimple.fin_prdt_nm"
            :average-intr-rate="averageIntrRate"
            :intr-rate="intrRate"
            :intr-rate2="intrRate2"
          />
          <BarChartDetailSaving
            v-else
            :title="selectedProductSimple.fin_prdt_nm"
            :labels="selectedProductLabels"
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
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCounterStore } from '@/stores/counter';
import BarChartDetail from '@/components/BarChartDetailView.vue';
import BarChartDetailSaving from '@/components/BarChartDetailSaving.vue';
import axios from 'axios';

const props = defineProps({
  products: Array,
  title: String
});

const dialog = ref(false);
const selectedProductSimple = ref(null);
const selectedProduct = ref(null);
const selectedProductCode = computed(() => selectedProductSimple.value?.fin_prdt_cd);
const selectedProductLabels = ref([]);
const selectedProductDetails = ref({});
const intrRate = ref([]);
const intrRate2 = ref([]);
const dataLoaded = ref(false);
const isDeposit = ref(true);
const averageIntrRate = ref([3.45, 4.08, 3.4, 3.35]); // 예시 데이터
const store = useCounterStore();

const clickProduct = async (product) => {
  selectedProductSimple.value = product;
  isDeposit.value = props.title === '계약된 예금';
  intrRate.value = [];
  intrRate2.value = [];
  selectedProductLabels.value = [];
  dataLoaded.value = false;
  
  if (isDeposit.value) {
    await getDeposit();
  } else {
    await getSaving();
  }
  
  dialog.value = true;
};

const getDeposit = async () => {
  if (!selectedProductCode.value) {
    console.error('selectedProductCode is null or undefined');
    return;
  }

  try {
    const res = await axios.get(`${store.DJANGO_URL}/financial/deposit_list/${selectedProductCode.value}/`);
    const data = res.data;
    selectedProductDetails.value = {
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
      const saveTrm = parseInt(option.save_trm, 10);
      if (saveTrm === 6) {
        intrRate.value[0] = option.intr_rate;
        intrRate2.value[0] = option.intr_rate2;
      } else if (saveTrm === 12) {
        intrRate.value[1] = option.intr_rate;
        intrRate2.value[1] = option.intr_rate2;
      } else if (saveTrm === 24) {
        intrRate.value[2] = option.intr_rate;
        intrRate2.value[2] = option.intr_rate2;
      } else if (saveTrm === 36) {
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
  if (!selectedProductCode.value) {
    console.error('selectedProductCode is null or undefined');
    return;
  }

  try {
    const res = await axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedProductCode.value}/`);
    const data = res.data;
    selectedProductDetails.value = {
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

    intrRate.value = [];
    intrRate2.value = [];
    selectedProductLabels.value = [];

    for (const option of optionList) {
      selectedProductLabels.value.push(`${option.save_trm}개월 금리`);
      intrRate.value.push(option.intr_rate);
      intrRate2.value.push(option.intr_rate2);
    }

    dataLoaded.value = true;
  } catch (err) {
    console.log(err);
  }
};

const deleteProductUser = async () => {
  try {
    const url = isDeposit.value
      ? `${store.DJANGO_URL}/financial/deposit_list/${selectedProductCode.value}/contract/`
      : `${store.DJANGO_URL}/financial/saving_list/${selectedProductCode.value}/contract/`;

    await axios.delete(url, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    });

    if (isDeposit.value) {
      store.userInfo.deposits = store.userInfo.deposits.filter(deposit => deposit.fin_prdt_cd !== selectedProductCode.value);
    } else {
      store.userInfo.savings = store.userInfo.savings.filter(saving => saving.fin_prdt_cd !== selectedProductCode.value);
    }

    dialog.value = false;
  } catch (error) {
    console.error('Failed to delete product:', error);
  }
};

const close = () => {
  dialog.value = false;
};
</script>

<style scoped>
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
  width: 70%;
  max-width: 90%;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

tbody > tr {
  transition: 200ms;
  cursor: pointer;
}

tbody > tr:hover {
  background-color: rgb(247, 250, 253);
  color: #1089FF;
}
</style> -->


<template>
  <div>
    <h2>{{ title }}</h2>
    <ul class="product-list">
      <li v-for="product in products" :key="product.fin_prdt_cd" @click="clickProduct(product)" class="product-item">
        {{ product.fin_prdt_nm }}
      </li>
    </ul>

    <div v-if="dialog" class="dialog">
      <div class="dialog-content">
        <div class="dialog-header">
          <h3>{{ selectedProduct?.fin_prdt_nm }}</h3>
          <button @click="close" class="close-button">×</button>
        </div>
        <div v-if="store.isLogin" class="dialog-buttons">
          <button @click.prevent="deleteProductUser" class="action-button">가입 취소하기</button>
        </div>

        <table class="dialog-table">
          <tbody>
            <tr v-for="(value, key) in selectedProductDetails" :key="key">
              <td class="dialog-table-key">{{ key }}</td>
              <td class="dialog-table-value" v-if="key === '최고 한도'">
                {{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}
              </td>
              <td class="dialog-table-value" v-else>{{ value }}</td>
            </tr>
          </tbody>
        </table>

        <div class="chart-container" v-if="dataLoaded">
          <BarChartDetail v-if="isDeposit" :title="selectedProductSimple.fin_prdt_nm" :average-intr-rate="averageIntrRate"
            :intr-rate="intrRate" :intr-rate2="intrRate2" />
          <BarChartDetailSaving v-else :title="selectedProductSimple.fin_prdt_nm" :labels="selectedProductLabels"
            :intr-rate="intrRate" :intr-rate2="intrRate2" />
          <p class="text-caption">* 개월별 평균 예금 금리는 2023년 11월 기준입니다.</p>
          <p class="text-caption">* 차트에 없는 이자율은 상품에 존재하지 않는 옵션입니다.</p>
        </div>

        <div class="dialog-actions">
          <button @click="close" class="action-button">닫기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCounterStore } from '@/stores/counter';
import BarChartDetail from '@/components/BarChartDetailView.vue';
import BarChartDetailSaving from '@/components/BarChartDetailSaving.vue';
import axios from 'axios';

const props = defineProps({
  products: Array,
  title: String
});

const dialog = ref(false);
const selectedProductSimple = ref(null);
const selectedProduct = ref(null);
const selectedProductCode = computed(() => selectedProductSimple.value?.fin_prdt_cd);
const selectedProductLabels = ref([]);
const selectedProductDetails = ref({});
const intrRate = ref([]);
const intrRate2 = ref([]);
const dataLoaded = ref(false);
const isDeposit = ref(true);
const averageIntrRate = ref([3.45, 4.08, 3.4, 3.35]); // 예시 데이터
const store = useCounterStore();

const clickProduct = async (product) => {
  selectedProductSimple.value = product;
  isDeposit.value = props.title === '계약된 예금';
  intrRate.value = [];
  intrRate2.value = [];
  selectedProductLabels.value = [];
  dataLoaded.value = false;

  if (isDeposit.value) {
    await getDeposit();
  } else {
    await getSaving();
  }

  dialog.value = true;
};

const getDeposit = async () => {
  if (!selectedProductCode.value) {
    console.error('selectedProductCode is null or undefined');
    return;
  }

  try {
    const res = await axios.get(`${store.DJANGO_URL}/financial/deposit_list/${selectedProductCode.value}/`);
    const data = res.data;
    selectedProductDetails.value = {
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
      const saveTrm = parseInt(option.save_trm, 10);
      if (saveTrm === 6) {
        intrRate.value[0] = option.intr_rate;
        intrRate2.value[0] = option.intr_rate2;
      } else if (saveTrm === 12) {
        intrRate.value[1] = option.intr_rate;
        intrRate2.value[1] = option.intr_rate2;
      } else if (saveTrm === 24) {
        intrRate.value[2] = option.intr_rate;
        intrRate2.value[2] = option.intr_rate2;
      } else if (saveTrm === 36) {
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
  if (!selectedProductCode.value) {
    console.error('selectedProductCode is null or undefined');
    return;
  }

  try {
    const res = await axios.get(`${store.DJANGO_URL}/financial/saving_list/${selectedProductCode.value}/`);
    const data = res.data;
    selectedProductDetails.value = {
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

    intrRate.value = [];
    intrRate2.value = [];
    selectedProductLabels.value = [];

    for (const option of optionList) {
      selectedProductLabels.value.push(`${option.save_trm}개월 금리`);
      intrRate.value.push(option.intr_rate);
      intrRate2.value.push(option.intr_rate2);
    }

    dataLoaded.value = true;
  } catch (err) {
    console.log(err);
  }
};

const deleteProductUser = async () => {
  try {
    const url = isDeposit.value
      ? `${store.DJANGO_URL}/financial/deposit_list/${selectedProductCode.value}/contract/`
      : `${store.DJANGO_URL}/financial/saving_list/${selectedProductCode.value}/contract/`;

    await axios.delete(url, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    });

    if (isDeposit.value) {
      store.userInfo.deposits = store.userInfo.deposits.filter(deposit => deposit.fin_prdt_cd !== selectedProductCode.value);
    } else {
      store.userInfo.savings = store.userInfo.savings.filter(saving => saving.fin_prdt_cd !== selectedProductCode.value);
    }

    dialog.value = false;
  } catch (error) {
    console.error('Failed to delete product:', error);
  }
};

const close = () => {
  dialog.value = false;
};
</script>

<style scoped>
@font-face {
  font-family: 'NEXON Lv1 Gothic Low OTF';
  src: url('@/assets/fonts/NEXON_Lv1_Gothic_Low.otf') format('opentype');
}

.product-list {
  list-style: none;
  padding: 0;
}

.product-item {
  cursor: pointer;
  padding: 10px;
  margin: 5px 0;
  background-color: #f2f2f2;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.product-item:hover {
  background-color: #d0eaff;
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
  width: 80%;
  max-width: 600px;
  max-height: 80%;
  overflow-y: auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  position: relative;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.dialog-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.action-button {
  background-color: #2db2ff;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  font-family: 'NEXON Lv1 Gothic Low OTF';
  border-radius: 4px;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.action-button:hover {
  background-color: #0a73d9;
}

.dialog-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.dialog-table td {
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.dialog-table-key {
  font-weight: bold;
  background-color: #f2f2f2;
}

.chart-container {
  margin-top: 20px;
}

.text-caption {
  font-size: 12px;
  color: #666;
  text-align: center;
  margin-top: 10px;
}

.dialog-actions {
  display: flex;
  justify-content: center;
}
</style>
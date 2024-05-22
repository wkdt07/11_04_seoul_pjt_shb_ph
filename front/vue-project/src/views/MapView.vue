<!-- <template>
    <form @submit.prevent="search(keyWord)">
      <div>
        <label>지역 선택</label>
        <select v-model="selectedRegion" @change="updateDistricts">
          <option disabled value="">지역을 선택하세요</option>
          <option v-for="region in regions" :key="region" :value="region">{{ region }}</option>
        </select>
      </div>
      <div v-if="districts.length">
        <label>구 선택</label>
        <select v-model="selectedDistrict" @change="updateNeighborhoods">
          <option disabled value="">구를 선택하세요</option>
          <option v-for="district in districts" :key="district" :value="district">{{ district }}</option>
        </select>
      </div>
      <div v-if="neighborhoods.length">
        <label>동 선택</label>
        <select v-model="selectedNeighborhood" @change="updateKeyword">
          <option disabled value="">동을 선택하세요</option>
          <option v-for="neighborhood in neighborhoods" :key="neighborhood" :value="neighborhood">{{ neighborhood }}</option>
        </select>
      </div>
      <div>
        <label>은행 종류 (선택 사항)</label>
        <select v-model="bankType" @change="updateKeyword">
          <option value="">은행 종류를 선택하세요 (선택 사항)</option>
          <option v-for="bank in banks" :key="bank" :value="bank">{{ bank }}</option>
        </select>
      </div>
      <input type="submit" value="검색">
    </form>
    <div>
      <label>직접 검색:</label>
      <input type="text" v-model="manualKeyword" @input="updateManualKeyword" placeholder="검색어를 입력하세요">
      <button @click="search(manualKeyword)">검색</button>
    </div>

    <KakaoMap v-if="currentLat && currentLng" :lat="currentLat" :lng="currentLng" @onLoadKakaoMap="onLoadKakaoMap">
  <KakaoMapMarker
    v-for="(marker, index) in markerList"
    :key="index"
    :lat="marker.lat"
    :lng="marker.lng"
    :infoWindow="marker.infoWindow"
    :clickable="true"
    @onClickKakaoMapMarker="() => onClickMapMarker(marker)"
  />
</KakaoMap>

    <div v-if="markerList.length">
    <h2>검색 결과</h2>
    <ul>
      <li v-for="(marker, index) in markerList" :key="index" @click="toggleInfoWindow(marker)">
        <h2>{{ marker.infoWindow.place_name }}</h2>
      <p>{{ marker.infoWindow.address_name }}</p>
      <p>{{ marker.infoWindow.road_address_name }}</p>
      <p><a :href="marker.infoWindow.place_url" target="_blank">{{ marker.infoWindow.place_url }}</a></p>
           

      </li>
    </ul>
  </div>
  </template>
  
  <script setup>
  import { KakaoMap, KakaoMapMarker } from 'vue3-kakao-maps';
  import { ref,onMounted } from 'vue';
  
  const map = ref();
  const markerList = ref([]);
  const keyWord = ref('');
  const manualKeyword = ref('');
  const currentLat = ref(null);
  const currentLng = ref(null);
  const regions = ['서울특별시', '경기도', '전라도', '경상도', '충청도', '제주특별시'];
  const districtsMap = {
    '서울특별시': [
            '강남구',
            '강동구',
            '강북구',
            '강서구',
            '관악구',
            '광진구',
            '구로구',
            '금천구',
            '노원구',
            '도봉구',
            '동대문구',
            '동작구',
            '마포구',
            '서대문구',
            '서초구',
            '성동구',
            '성북구',
            '송파구',
            '양천구',
            '영등포구',
            '용산구',
            '은평구',
            '종로구',
            '중구',
            '중랑구'
        ],
        '경기도': [
            '수원시',
            '성남시',
            '안양시',
            '안산시',
            '용인시',
            '부천시',
            '광명시',
            '평택시',
            '과천시',
            '의왕시',
            '시흥시',
            '군포시',
            '하남시',
            '오산시',
            '이천시',
            '안성시',
            '김포시',
            '화성시',
            '광주시',
            '양주시',
            '포천시',
            '여주시',
            '연천군',
            '가평군',
            '양평군'
        ],
        '부산광역시': [
            '중구',
            '서구',
            '동구',
            '영도구',
            '부산진구',
            '동래구',
            '남구',
            '북구',
            '해운대구',
            '사하구',
            '금정구',
            '강서구',
            '연제구',
            '수영구',
            '사상구',
            '기장군'
        ],
        '경상북도': [
            '포항시',
            '경주시',
            '김천시',
            '안동시',
            '구미시',
            '영주시',
            '영천시',
            '상주시',
            '문경시',
            '경산시',
            '군위군',
            '의성군',
            '청송군',
            '영양군',
            '영덕군',
            '청도군',
            '고령군',
            '성주군',
            '칠곡군',
            '예천군',
            '봉화군',
            '울진군',
            '울릉군'
        ],
        '인천광역시': [
            '중구',
            '동구',
            '미추홀구',
            '연수구',
            '남동구',
            '부평구',
            '계양구',
            '서구',
            '강화군',
            '옹진군'
        ],
        '대구광역시': [
            '중구',
            '동구',
            '서구',
            '남구',
            '북구',
            '수성구',
            '달서구',
            '달성군'
        ],
        '대전광역시': [
            '동구',
            '중구',
            '서구',
            '유성구',
            '대덕구'
        ],
        '광주광역시': [
            '동구',
            '서구',
            '남구',
            '북구',
            '광산구'
        ],
        '울산광역시': [
            '중구',
            '남구',
            '동구',
            '북구',
            '울주군'
        ],
        '세종특별자치시': [
            '세종시'
        ],
        '강원도': [
            '춘천시',
            '원주시',
            '강릉시',
            '동해시',
            '태백시',
            '속초시',
            '삼척시',
            '홍천군',
            '횡성군',
            '영월군',
            '평창군',
            '정선군',
            '철원군',
            '화천군',
            '양구군',
            '인제군',
            '고성군',
            '양양군'
        ],
        '충청북도': [
            '청주시',
            '충주시',
            '제천시',
            '보은군',
            '옥천군',
            '영동군',
            '증평군',
            '진천군',
            '괴산군',
            '음성군',
            '단양군'
        ],
        '충청남도': [
            '천안시',
            '공주시',
            '보령시',
            '아산시',
            '서산시',
            '논산시',
            '계룡시',
            '당진시',
            '금산군',
            '부여군',
            '서천군',
            '청양군',
            '홍성군',
            '예산군',
            '태안군'
        ],
        '전라북도': [
            '전주시',
            '군산시',
            '익산시',
            '정읍시',
            '남원시',
            '김제시',
            '완주군',
            '진안군',
            '무주군',
            '장수군',
            '임실군',
            '순창군',
            '고창군',
            '부안군'
        ],
        '전라남도': [
            '목포시',
            '여수시',
            '순천시',
            '나주시',
            '광양시',
            '담양군',
            '곡성군',
            '구례군',
            '고흥군',
            '보성군',
            '화순군',
            '장흥군',
            '강진군',
            '해남군',
            '영암군',
            '무안군',
            '함평군',
            '영광군',
            '장성군',
            '완도군',
            '진도군',
            '신안군'
        ],
        '제주특별자치도': [
            '제주시',
            '서귀포시'
        ]
  };
  const neighborhoodsMap = {
    '강남구': ['역삼동', '한남동', '강남동'],
    '강서구': ['화곡동', '방화동'],
    '성남시': ['분당동', '야탑동'],
    '수원시': ['팔달동', '영통동'],
    '전주시': ['덕진동', '완산동'],
    '광주시': ['광산동', '서구'],
    '부산시': ['해운대구', '서구'],
    '대구시': ['중구', '동구'],
    '청주시': ['상당구', '흥덕구'],
    '대전시': ['서구', '유성구'],
    '제주시': ['제주시내', '구좌읍'],
    '서귀포시': ['서귀동', '대정읍'],
    // 기타 구의 동을 여기에 추가
  };
  
  const banks = ['국민은행', '우리은행', '신한은행', '하나은행', '농협은행'];
  
  const selectedRegion = ref('');
  const selectedDistrict = ref('');
  const selectedNeighborhood = ref('');
  const bankType = ref('');
  
  const districts = ref([]);
  const neighborhoods = ref([]);
  
  const onLoadKakaoMap = (mapRef) => {
    map.value = mapRef;
  };
  
  const updateDistricts = () => {
    districts.value = districtsMap[selectedRegion.value] || [];
    selectedDistrict.value = '';
    neighborhoods.value = [];
    selectedNeighborhood.value = '';
    updateKeyword();
    console.log(keyWord.value)
  };
  
  const updateNeighborhoods = () => {
    neighborhoods.value = neighborhoodsMap[selectedDistrict.value] || [];
    selectedNeighborhood.value = '';
    updateKeyword();
    console.log(keyWord.value)

  };
  
  const updateKeyword = () => {
    keyWord.value = `${selectedRegion.value} ${selectedDistrict.value} ${selectedNeighborhood.value} ${bankType.value}은행`;
  };
  
  const updateManualKeyword = () => {
    keyWord.value = manualKeyword.value.trim();
  };
  
  const search = (keyWord) => {
    // 기존 마커 리스트를 초기화합니다
    markerList.value = [];
    const ps = new kakao.maps.services.Places();
    ps.keywordSearch(keyWord, placesSearchCB);
  };
  
  const placesSearchCB = (data, status) => {
    if (status === kakao.maps.services.Status.OK) {
      const bounds = new kakao.maps.LatLngBounds();
        
      for (let place of data) {
        const markerItem = {
          lat: place.y,
          lng: place.x,
          infoWindow: {
            place_name: place.place_name,
          address_name: place.address_name,
          road_address_name: place.road_address_name,
          place_url: place.place_url,
            content: `<div
        style="
          padding: 10px;
          background-color: white;
          border: 1px solid #ccc;
          border-radius: 5px;
          display: flex;
          flex-direction: column;
          align-items: flex-start;
        "
      >
        <div style="font-weight: bold; margin-bottom: 5px">${place.place_name}</div>
        <div style="display: flex">
          <div style="margin-right: 10px">
            <img src="https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/thumnail.png" width="73" height="70" />
          </div>
          <div style="display: flex; flex-direction: column; align-items: flex-start">
            <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap">${place.address_name}</div>
            <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap">${place.road_address_name}</div>
            <div><a href="${place.place_url}" target="_blank" style="color: blue">홈페이지</a></div>
          </div>
        </div>
      </div>`,
            visible: false
          }
        };
        console.log(place)
        markerList.value.push(markerItem);
        bounds.extend(new kakao.maps.LatLng(Number(place.y), Number(place.x)));
      }
  
      map.value?.setBounds(bounds);
    }
  };
  
  const onClickMapMarker = (markerItem) => {
    markerItem.infoWindow.visible = !markerItem.infoWindow.visible;
  };

  const toggleInfoWindow = (markerItem) => {
  markerItem.infoWindow.visible = !markerItem.infoWindow.visible;
};

const setDefaultLocation = () => {
  currentLat.value = 37.566826;
  currentLng.value = 126.9786567;
  updateMapCenter();
};

const updateMapCenter = () => {
  if (map.value) {
    map.value.setCenter(new kakao.maps.LatLng(currentLat.value, currentLng.value));
  }
};

onMounted(() => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      currentLat.value = position.coords.latitude;
      currentLng.value = position.coords.longitude;
      console.log(position);
      updateMapCenter();
    }, () => {
      // 현재 위치를 가져오지 못했을 때 기본 위치 설정 (서울 시청)
      setDefaultLocation();
    });
  } else {
    // 브라우저가 Geolocation API를 지원하지 않을 때 기본 위치 설정 (서울 시청)
    setDefaultLocation();
  }
});

  </script>
   -->


   <template>
    <div class="mapview-container">
      <div class="left-panel">
        <form @submit.prevent="search(keyWord)" class="card form-card">
          <div class="form-group">
            <label>지역 선택</label>
            <select v-model="selectedRegion" @change="updateDistricts">
              <option disabled value="">지역을 선택하세요</option>
              <option v-for="region in regions" :key="region" :value="region">{{ region }}</option>
            </select>
          </div>
          <div v-if="districts.length" class="form-group">
            <label>구 선택</label>
            <select v-model="selectedDistrict" @change="updateNeighborhoods">
              <option disabled value="">구를 선택하세요</option>
              <option v-for="district in districts" :key="district" :value="district">{{ district }}</option>
            </select>
          </div>
          <div v-if="neighborhoods.length" class="form-group">
            <label>동 선택</label>
            <select v-model="selectedNeighborhood" @change="updateKeyword">
              <option disabled value="">동을 선택하세요</option>
              <option v-for="neighborhood in neighborhoods" :key="neighborhood" :value="neighborhood">{{ neighborhood }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>은행 종류 (선택 사항)</label>
            <select v-model="bankType" @change="updateKeyword">
              <option value="">은행 종류를 선택하세요 (선택 사항)</option>
              <option v-for="bank in banks" :key="bank" :value="bank">{{ bank }}</option>
            </select>
          </div>
          <button type="submit" class="submit-button">검색</button>
        </form>
        <div class="card form-card">
          <label>직접 검색:</label>
          <input type="text" v-model="manualKeyword" @input="updateManualKeyword" placeholder="검색어를 입력하세요">
          <button @click="search(manualKeyword)" class="search-button">검색</button>
        </div>
        <KakaoMap v-if="currentLat && currentLng" class="map" :lat="currentLat" :lng="currentLng"
          @onLoadKakaoMap="onLoadKakaoMap">
          <KakaoMapMarker v-for="(marker, index) in markerList" :key="index" :lat="marker.lat" :lng="marker.lng"
            :infoWindow="marker.infoWindow" :clickable="true" @onClickKakaoMapMarker="() => onClickMapMarker(marker)" />
        </KakaoMap>
      </div>
      <div class="right-panel">
        <div v-if="markerList.length" class="card result-card">
          <h2 class="result-title">검색 결과</h2>
          <ul class="result-list">
            <li v-for="(marker, index) in markerList" :key="index" class="result-item" @click="toggleInfoWindow(marker)">
              <h3>{{ marker.infoWindow.place_name }}</h3>
              <p>{{ marker.infoWindow.address_name }}</p>
              <p>{{ marker.infoWindow.road_address_name }}</p>
              <p><a :href="marker.infoWindow.place_url" target="_blank">{{ marker.infoWindow.place_url }}</a></p>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
    
  <script setup>
  import { KakaoMap, KakaoMapMarker } from 'vue3-kakao-maps';
  import { ref, onMounted } from 'vue';
  
  const map = ref();
  const markerList = ref([]);
  const keyWord = ref('');
  const manualKeyword = ref('');
  const currentLat = ref(null);
  const currentLng = ref(null);
  const regions = ['서울특별시', '경기도', '전라도', '경상도', '충청도', '제주특별시'];
  const districtsMap = {
    '서울특별시': [
      '강남구',
      '강동구',
      '강북구',
      '강서구',
      '관악구',
      '광진구',
      '구로구',
      '금천구',
      '노원구',
      '도봉구',
      '동대문구',
      '동작구',
      '마포구',
      '서대문구',
      '서초구',
      '성동구',
      '성북구',
      '송파구',
      '양천구',
      '영등포구',
      '용산구',
      '은평구',
      '종로구',
      '중구',
      '중랑구'
    ],
    '경기도': [
      '수원시',
      '성남시',
      '안양시',
      '안산시',
      '용인시',
      '부천시',
      '광명시',
      '평택시',
      '과천시',
      '의왕시',
      '시흥시',
      '군포시',
      '하남시',
      '오산시',
      '이천시',
      '안성시',
      '김포시',
      '화성시',
      '광주시',
      '양주시',
      '포천시',
      '여주시',
      '연천군',
      '가평군',
      '양평군'
    ],
    '부산광역시': [
      '중구',
      '서구',
      '동구',
      '영도구',
      '부산진구',
      '동래구',
      '남구',
      '북구',
      '해운대구',
      '사하구',
      '금정구',
      '강서구',
      '연제구',
      '수영구',
      '사상구',
      '기장군'
    ],
    '경상북도': [
      '포항시',
      '경주시',
      '김천시',
      '안동시',
      '구미시',
      '영주시',
      '영천시',
      '상주시',
      '문경시',
      '경산시',
      '군위군',
      '의성군',
      '청송군',
      '영양군',
      '영덕군',
      '청도군',
      '고령군',
      '성주군',
      '칠곡군',
      '예천군',
      '봉화군',
      '울진군',
      '울릉군'
    ],
    '인천광역시': [
      '중구',
      '동구',
      '미추홀구',
      '연수구',
      '남동구',
      '부평구',
      '계양구',
      '서구',
      '강화군',
      '옹진군'
    ],
    '대구광역시': [
      '중구',
      '동구',
      '서구',
      '남구',
      '북구',
      '수성구',
      '달서구',
      '달성군'
    ],
    '대전광역시': [
      '동구',
      '중구',
      '서구',
      '유성구',
      '대덕구'
    ],
    '광주광역시': [
      '동구',
      '서구',
      '남구',
      '북구',
      '광산구'
    ],
    '울산광역시': [
      '중구',
      '남구',
      '동구',
      '북구',
      '울주군'
    ],
    '세종특별자치시': [
      '세종시'
    ],
    '강원도': [
      '춘천시',
      '원주시',
      '강릉시',
      '동해시',
      '태백시',
      '속초시',
      '삼척시',
      '홍천군',
      '횡성군',
      '영월군',
      '평창군',
      '정선군',
      '철원군',
      '화천군',
      '양구군',
      '인제군',
      '고성군',
      '양양군'
    ],
    '충청북도': [
      '청주시',
      '충주시',
      '제천시',
      '보은군',
      '옥천군',
      '영동군',
      '증평군',
      '진천군',
      '괴산군',
      '음성군',
      '단양군'
    ],
    '충청남도': [
      '천안시',
      '공주시',
      '보령시',
      '아산시',
      '서산시',
      '논산시',
      '계룡시',
      '당진시',
      '금산군',
      '부여군',
      '서천군',
      '청양군',
      '홍성군',
      '예산군',
      '태안군'
    ],
    '전라북도': [
      '전주시',
      '군산시',
      '익산시',
      '정읍시',
      '남원시',
      '김제시',
      '완주군',
      '진안군',
      '무주군',
      '장수군',
      '임실군',
      '순창군',
      '고창군',
      '부안군'
    ],
    '전라남도': [
      '목포시',
      '여수시',
      '순천시',
      '나주시',
      '광양시',
      '담양군',
      '곡성군',
      '구례군',
      '고흥군',
      '보성군',
      '화순군',
      '장흥군',
      '강진군',
      '해남군',
      '영암군',
      '무안군',
      '함평군',
      '영광군',
      '장성군',
      '완도군',
      '진도군',
      '신안군'
    ],
    '제주특별자치도': [
      '제주시',
      '서귀포시'
    ]
  };
  const neighborhoodsMap = {
    '강남구': ['역삼동', '한남동', '강남동'],
    '강서구': ['화곡동', '방화동'],
    '성남시': ['분당동', '야탑동'],
    '수원시': ['팔달동', '영통동'],
    '전주시': ['덕진동', '완산동'],
    '광주시': ['광산동', '서구'],
    '부산시': ['해운대구', '서구'],
    '대구시': ['중구', '동구'],
    '청주시': ['상당구', '흥덕구'],
    '대전시': ['서구', '유성구'],
    '제주시': ['제주시내', '구좌읍'],
    '서귀포시': ['서귀동', '대정읍'],
    // 기타 구의 동을 여기에 추가
  };
  
  const banks = ['국민은행', '우리은행', '신한은행', '하나은행', '농협은행'];
  
  const selectedRegion = ref('');
  const selectedDistrict = ref('');
  const selectedNeighborhood = ref('');
  const bankType = ref('');
  
  const districts = ref([]);
  const neighborhoods = ref([]);
  
  const onLoadKakaoMap = (mapRef) => {
    map.value = mapRef;
  };
  
  const updateDistricts = () => {
    districts.value = districtsMap[selectedRegion.value] || [];
    selectedDistrict.value = '';
    neighborhoods.value = [];
    selectedNeighborhood.value = '';
    updateKeyword();
    console.log(keyWord.value)
  };
  
  const updateNeighborhoods = () => {
    neighborhoods.value = neighborhoodsMap[selectedDistrict.value] || [];
    selectedNeighborhood.value = '';
    updateKeyword();
    console.log(keyWord.value)
  
  };
  
  const updateKeyword = () => {
    keyWord.value = `${selectedRegion.value} ${selectedDistrict.value} ${selectedNeighborhood.value} ${bankType.value}은행`;
  };
  
  const updateManualKeyword = () => {
    keyWord.value = manualKeyword.value.trim();
  };
  
  const search = (keyWord) => {
    // 기존 마커 리스트를 초기화합니다
    markerList.value = [];
    const ps = new kakao.maps.services.Places();
    ps.keywordSearch(keyWord, placesSearchCB);
  };
  
  const placesSearchCB = (data, status) => {
    if (status === kakao.maps.services.Status.OK) {
      const bounds = new kakao.maps.LatLngBounds();
  
      for (let place of data) {
        const markerItem = {
          lat: place.y,
          lng: place.x,
          infoWindow: {
            place_name: place.place_name,
            address_name: place.address_name,
            road_address_name: place.road_address_name,
            place_url: place.place_url,
            content: `<div
          style="
            padding: 10px;
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 5px;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
          "
        >
          <div style="font-weight: bold; margin-bottom: 5px">${place.place_name}</div>
          <div style="display: flex">
            <div style="margin-right: 10px">
              <img src="https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/thumnail.png" width="73" height="70" />
            </div>
            <div style="display: flex; flex-direction: column; align-items: flex-start">
              <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap">${place.address_name}</div>
              <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap">${place.road_address_name}</div>
              <div><a href="${place.place_url}" target="_blank" style="color: blue">홈페이지</a></div>
            </div>
          </div>
        </div>`,
            visible: false
          }
        };
        console.log(place)
        markerList.value.push(markerItem);
        bounds.extend(new kakao.maps.LatLng(Number(place.y), Number(place.x)));
      }
  
      map.value?.setBounds(bounds);
    }
  };
  
  const onClickMapMarker = (markerItem) => {
    markerItem.infoWindow.visible = !markerItem.infoWindow.visible;
  };
  
  const toggleInfoWindow = (markerItem) => {
    markerItem.infoWindow.visible = !markerItem.infoWindow.visible;
  };
  
  const setDefaultLocation = () => {
    currentLat.value = 37.566826;
    currentLng.value = 126.9786567;
    updateMapCenter();
  };
  
  const updateMapCenter = () => {
    if (map.value) {
      map.value.setCenter(new kakao.maps.LatLng(currentLat.value, currentLng.value));
    }
  };
  
  onMounted(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        currentLat.value = position.coords.latitude;
        currentLng.value = position.coords.longitude;
        console.log(position);
        updateMapCenter();
      }, () => {
        // 현재 위치를 가져오지 못했을 때 기본 위치 설정 (서울 시청)
        setDefaultLocation();
      });
    } else {
      // 브라우저가 Geolocation API를 지원하지 않을 때 기본 위치 설정 (서울 시청)
      setDefaultLocation();
    }
  });
  
  </script>
  <style scoped>
  @font-face {
    font-family: 'NEXON Lv1 Gothic Low';
    src: url('@/assets/fonts/NEXON_Lv1_Gothic_Low.otf') format('opentype');
  }
  
  .mapview-container {
    display: flex;
    justify-content: space-between;
    padding: 20px;
    background-color: #f0f2f5;
    min-height: 100vh;
    font-family: 'NEXON Lv1 Gothic Low', sans-serif;
  }
  
  .left-panel {
    width: 55%;
    /* Reduce width to allow more space for the right panel */
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .right-panel {
    width: 40%;
    /* Increase width to occupy the remaining space */
    display: flex;
    flex-direction: column;
    margin-right: 100px;
  
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
    margin-bottom: 20px;
  }
  
  .form-card {
    max-width: 500px;
    /* Limit the width of form cards */
    width: 100%;
  }
  
  .map {
    width: 100%;
    /* Make the map full width */
    height: 500px;
    /* Set a fixed height for the map */
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
  
  .submit-button,
  .search-button {
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
  
  .submit-button:hover,
  .search-button:hover {
    background-color: #40a9ff;
  }
  
  .result-card {
    padding: 15px;
  }
  
  .result-title {
    font-size: 1.5em;
    margin-bottom: 10px;
    color: #333;
  }
  
  .result-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .result-item {
    padding: 10px;
    border-bottom: 1px solid #ddd;
  }
  
  .result-item h3 {
    margin: 0;
    font-size: 1.2em;
    color: #333;
  }
  
  .result-item p {
    margin: 5px 0;
    font-size: 14px;
    color: #666;
  }
  
  .result-item a {
    color: #1890ff;
    text-decoration: none;
  }
  
  .result-item a:hover {
    text-decoration: underline;
  }
  </style>
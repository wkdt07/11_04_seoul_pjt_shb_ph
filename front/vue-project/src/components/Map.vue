<template>
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
    <KakaoMap :lat="37.566826" :lng="126.9786567" @onLoadKakaoMap="onLoadKakaoMap">
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
  </template>
  
  <script setup>
  import { KakaoMap, KakaoMapMarker } from 'vue3-kakao-maps';
  import { ref } from 'vue';
  
  const map = ref();
  const markerList = ref([]);
  const keyWord = ref('');
  const manualKeyword = ref('');
  
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
  </script>
  
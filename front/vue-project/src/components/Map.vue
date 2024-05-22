<!-- <script setup>
import { KakaoMap, KakaoMapMarker } from 'vue3-kakao-maps';
import { ref } from 'vue';

const map = ref();
const markerList = ref([]);

const keyWord = ref('');

const onLoadKakaoMap = (mapRef) => {
  map.value = mapRef;
  // search(keyWord.value);
};

const search = function (keyWord) {
  // 기존 마커 리스트를 초기화합니다
  markerList.value = [];
  const ps = new kakao.maps.services.Places();
  ps.keywordSearch(keyWord, placesSearchCB);
};

const placesSearchCB = (data, status) => {
  if (status === kakao.maps.services.Status.OK) {
    const bounds = new kakao.maps.LatLngBounds();

    for (let marker of data) {
      const markerItem = {
        lat: marker.y,
        lng: marker.x,
        infoWindow: {
          content: marker.place_name,
          visible: false
        }
      };
      markerList.value.push(markerItem);
      bounds.extend(new kakao.maps.LatLng(Number(marker.y), Number(marker.x)));
    }

    map.value?.setBounds(bounds);
  }
};

const onClickMapMarker = (markerItem) => {
  if (markerItem.infoWindow?.visible !== null && markerItem.infoWindow?.visible !== undefined) {
    markerItem.infoWindow.visible = !markerItem.infoWindow.visible;
  } else {
    markerItem.infoWindow.visible = true;
  }
};
</script>

<template>
  <form @submit.prevent="search(keyWord);"> 
    <input type="text" v-model="keyWord">
    <input type="submit" value="검색">
  </form>
  <KakaoMap :lat="37.566826" :lng="126.9786567" @onLoadKakaoMap="onLoadKakaoMap">
    <KakaoMapMarker
      v-for="(marker, index) in markerList"
      :key="index"
      :lat="marker.lat"
      :lng="marker.lng"
      :infoWindow="marker.infoWindow"
      :clickable="true"
      @onClickKakaoMapMarker="onClickMapMarker(marker)"
    />
  </KakaoMap>
</template> -->
<template>
  <div class="map-container">
    <div class="search-card">
      <form @submit.prevent="search(keyWord);">
        <h2 class="search-title">은행 검색</h2>
        <input type="text" v-model="keyWord" placeholder="은행 이름을 입력하세요" class="search-input" />
        <button type="submit" class="search-button">검색</button>
      </form>
    </div>
    <KakaoMap :lat="37.566826" :lng="126.9786567" @onLoadKakaoMap="onLoadKakaoMap">
      <KakaoMapMarker v-for="(marker, index) in markerList" :key="index" :lat="marker.lat" :lng="marker.lng"
        :infoWindow="marker.infoWindow" :clickable="true" @onClickKakaoMapMarker="onClickMapMarker(marker)" />
    </KakaoMap>
  </div>
</template>

<script setup>
import { KakaoMap, KakaoMapMarker } from 'vue3-kakao-maps';
import { ref } from 'vue';

const map = ref();
const markerList = ref([]);

const keyWord = ref('');

const onLoadKakaoMap = (mapRef) => {
  map.value = mapRef;
  // search(keyWord.value);
};

const search = function (keyWord) {
  // 기존 마커 리스트를 초기화합니다
  markerList.value = [];
  const ps = new kakao.maps.services.Places();
  ps.keywordSearch(keyWord, placesSearchCB);
};

const placesSearchCB = (data, status) => {
  if (status === kakao.maps.services.Status.OK) {
    const bounds = new kakao.maps.LatLngBounds();

    for (let marker of data) {
      const markerItem = {
        lat: marker.y,
        lng: marker.x,
        infoWindow: {
          content: marker.place_name,
          visible: false
        }
      };
      markerList.value.push(markerItem);
      bounds.extend(new kakao.maps.LatLng(Number(marker.y), Number(marker.x)));
    }

    map.value?.setBounds(bounds);
  }
};

const onClickMapMarker = (markerItem) => {
  if (markerItem.infoWindow?.visible !== null && markerItem.infoWindow?.visible !== undefined) {
    markerItem.infoWindow.visible = !markerItem.infoWindow.visible;
  } else {
    markerItem.infoWindow.visible = true;
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

.map-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f0f2f5;
  min-height: 100vh;
  font-family: 'NEXON Lv1 Gothic Low', sans-serif;
}

.search-card {
  background: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
  margin-bottom: 20px;
}

.search-title {
  font-size: 1.5em;
  color: #333;
  margin-bottom: 10px;
}

.search-input {
  width: calc(100% - 20px);
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 14px;
  margin-bottom: 10px;
}

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

.search-button:hover {
  background-color: #40a9ff;
}
</style>

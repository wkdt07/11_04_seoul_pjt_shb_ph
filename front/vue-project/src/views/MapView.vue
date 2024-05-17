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
</template>

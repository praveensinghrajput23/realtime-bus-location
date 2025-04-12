var map = L.map('mapid').setView([28.6077, 77.07918], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);



mapMarkers1 = [];
mapMarkers2 = [];
mapMarkers3 = [];

var source = new EventSource('/topic/bus-coordinates'); //ENTER YOUR TOPICNAME HERE
source.addEventListener('message', function(e){

  console.log('Message');
  obj = JSON.parse(e.data);
  console.log(obj);

  if(obj.busline == '0001') {
    for (var i = 0; i < mapMarkers1.length; i++) {
      map.removeLayer(mapMarkers1[i]);
    }
    marker1 = L.marker([obj.latitude, obj.longitude]).addTo(map);
    mapMarkers1.push(marker1);
  }

//   if(obj.busline == '00002') {
//     for (var i = 0; i < mapMarkers2.length; i++) {
//       map.removeLayer(mapMarkers2[i]);
//     }
//     marker2 = L.marker([obj.latitude, obj.longitude]).addTo(map);
//     mapMarkers2.push(marker2);
//   }

//   if(obj.busline == '00003') {
//     for (var i = 0; i < mapMarkers3.length; i++) {
//       map.removeLayer(mapMarkers3[i]);
//     }
//     marker3 = L.marker([obj.latitude, obj.longitude]).addTo(map);
//     mapMarkers3.push(marker3);
//   }
}, false);
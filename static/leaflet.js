var map = L.map('mapid').setView([28.60805, 77.08519], 14);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var redIcon = L.AwesomeMarkers.icon({
    icon: 'bus',
    prefix: 'fa',
    markerColor: 'red'
});

var blueIcon = L.AwesomeMarkers.icon({
    icon: 'bus',
    prefix: 'fa',
    markerColor: 'blue'
});

var greenIcon = L.AwesomeMarkers.icon({
    icon: 'bus',
    prefix: 'fa',
    markerColor: 'green'
});

mapMarkers1 = [];
mapMarkers2 = [];
mapMarkers3 = [];



function connectEventSource() {
  var source = new EventSource('/topic/bus-coordinates');

  console.log(source)
  
  source.onmessage = function(e) {
    console.log('Message');
    obj = JSON.parse(e.data);
    console.log(obj);
  
    if(obj.busline == '0001') {
      for (var i = 0; i < mapMarkers1.length; i++) {
        map.removeLayer(mapMarkers1[i]);
      }
      marker1 = L.marker([obj.latitude, obj.longitude],{ icon: redIcon }).addTo(map).bindTooltip("Bus No: " + obj.busline, { permanent: false, direction: "top" });
      mapMarkers1.push(marker1);
    }
    if(obj.busline == '0002') {
      for (var i = 0; i < mapMarkers2.length; i++) {
        map.removeLayer(mapMarkers2[i]);
      }
      marker2 = L.marker([obj.latitude, obj.longitude],{ icon: blueIcon }).addTo(map).bindTooltip("Bus No: " + obj.busline, { permanent: false, direction: "top" });
      mapMarkers2.push(marker2);
    }
    if(obj.busline == '0003') {
      for (var i = 0; i < mapMarkers3.length; i++) {
        map.removeLayer(mapMarkers3[i]);
      }
      marker3 = L.marker([obj.latitude, obj.longitude],{ icon: greenIcon }).addTo(map).bindTooltip("Bus No: " + obj.busline, { permanent: false, direction: "top" });
      mapMarkers3.push(marker3);
    }
  };

  source.onerror = function(err) {
      console.error("EventSource failed, retrying in 5 seconds", err);
      source.close();
      setTimeout(connectEventSource, 5000);
  };
}

connectEventSource();  // initialize it



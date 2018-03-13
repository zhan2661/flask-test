var map
var x;
var y;
//navigator.geolocation.getCurrentPosition(showMap);
//function showMap(position) {
        // x =position.coords.latitude;
        // y =position.coords.longitude;
      //}
function initMap() {
        map = new google.maps.Map(document.getElementById('map-container'), {
          center: {lat: 44.9727, lng: -93.23540000000003},
          zoom: 14
        });

        var marker = new google.maps.Marker({
		      map: map,
                      animation: google.maps.Animation.BOUNCE,
		      position: {lat: 44.9727, lng: -93.23540000000003}
		    });

      google.maps.event.addListener(marker,'click',function() {
		     infowindow = new google.maps.InfoWindow({
		          content: 'You found me !'
			});
			 infowindow.open(map,marker);
		       });   
}




var map;

var feature;

function load_map(){
	map = new L.map('map', {zoomControl: true})

	var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',

	osmAttribution = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'

	osm = new L.TileLayer(osmUrl, {maxZoom: 18, attribution: osmAttribution});

	map.setView(new L.LatLng(51.538594, -0.198075), 12).addLayer(osm);

	L.control.scale().addTo(map);
}

function addr_search(){

	// map = new L.map('map', {zoomControl: true})

	// var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',

	// osmAttribution = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'

	// osm = new L.TileLayer(osmUrl, {maxZoom: 18, attribution: osmAttribution});

	// map.setView(new L.LatLng(51.538594, -0.198075), 12).addLayer(osm);

	// L.control.scale().addTo(map);

	var searchControl = new L.esri.Controls.Geosearch().addTo(map);

	var results = new L.LayerGroup().addTo(map);

	searchControl.on('results', function(data){
		results.clearLayers();
		for (var i = data.results.length - 1; i >= 0; i--) {
		results.addLayer(L.marker(data.results[i].latlng));
		}
	});

	setTimeout(function(){$('.pointer').fadeOut('slow');},3400);

}

function chooseAddr(lat1, lng1, lat2, lng2, osm_type) {

	var loc1 = new L.LatLng(lat1, lng1);

	var loc2 = new L.LatLng(lat2, lng2);

	var bounds = new L.LatLngBounds(loc1, loc2);



	if (feature) {

		map.removeLayer(feature);

	}

	if (osm_type == "node") {

		feature = L.circle( loc1, 25, {color: 'green', fill: false}).addTo(map);

		map.fitBounds(bounds);

		map.setZoom(18);

	} else {

		var loc3 = new L.LatLng(lat1, lng2);

		var loc4 = new L.LatLng(lat2, lng1);



		feature = L.polyline( [loc1, loc4, loc2, loc3, loc1], {color: 'red'}).addTo(map);

		map.fitBounds(bounds);

	}

}


window.onload = load_map;


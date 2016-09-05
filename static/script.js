

var eventOutputContainer = document.getElementById("message");
var eventSrc = new EventSource("/eventSource");

eventSrc.onmessage = function(e) {
    console.log(e);
    eventOutputContainer.innerHTML = e.data;
};

var tooltip = d3.select("div.tooltip");
var tooltip_text = d3.select("#text");
var tooltip_latlng = d3.select("#latlng");


var map = L.map('map').setView([22.941322,113.676795], 16);

L.tileLayer('https://api.tiles.mapbox.com/v4/{mapid}/{z}/{x}/{y}.png?access_token={accessToken}', {
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',mapid: 'mapbox.light',accessToken: 'pk.eyJ1IjoibXVzb2ZhbiIsImEiOiJCQ0c0cGVnIn0.zMLchQ_sTFmn8ZDfp59YSA'
	 }).addTo(map);

//create variables to store a reference to svg and g elements

var svg = d3.select(map.getPanes().overlayPane).append("svg");
var g = svg.append("g").attr("class", "leaflet-zoom-hide")
	.attr("id","g");
var g_line = svg.append("g").attr("class", "leaflet-zoom-hide").attr("id","g_line");

function projectPoint(lat, lng) {
	return map.latLngToLayerPoint(new L.LatLng(lat, lng));
	}

function projectStream(lat, lng) {
	var point = projectPoint(lat,lng);
	this.stream.point(point.x, point.y);
	}

var transform = d3.geo.transform({point: projectStream});
var path = d3.geo.path().projection(transform);



function updateData(){

	var mapBounds = map.getBounds();
	var lat1 = mapBounds["_southWest"]["lat"];
	var lat2 = mapBounds["_northEast"]["lat"];
	var lng1 = mapBounds["_southWest"]["lng"];
	var lng2 = mapBounds["_northEast"]["lng"];

	request = "/getData?lat1=" + lat1 + "&lat2=" + lat2 + "&lng1=" + lng1 + "&lng2=" + lng2

	console.log(request);

	g.selectAll("circle").remove()
	g_line.selectAll("line").remove()

  	d3.json(request, function(data) {

		//create placeholder circle geometry and bind it to data
		var originP = g.selectAll("circle").data(data.features);
		var connectedP = g.selectAll("circle").data(data.features1);
		var lines = g_line.selectAll("line").data(data.lines);
		
		lines.enter()
			.append("line")
			.transition()
			.duration(2000)
			.style("stroke","black")
			.style("stroke-opacity",0.2)
			.style("stroke-width",1.0);

		connectedP.enter()
			.append("circle")
			.transition()
			.duration(2000)
		    .attr("r", 20)
		    .style("fill","#A7A9AB")
		    .style("fill-opacity","0.5")
		 //    .on("mouseover", function(d){
			// 	tooltip.style("visibility", "visible");
			// 	tooltip_title.text("Text:" + d.properties.text);
			// 	tooltip_latlng.text("Coordinates：" + d.geometry.coordinates);
			// })
			// .on("mousemove", function(){
			// 	tooltip.style("top", (d3.event.pageY-10)+"px")
			// 	tooltip.style("left",(d3.event.pageX+10)+"px");
			// })
			// .on("mouseout", function(){
			// 	tooltip.style("visibility", "hidden");					
			// })
		    ;			

		originP.enter()
			.append("circle")
			.transition()
			.duration(2000)
		    .attr("r", 7)
		    .style("fill","red")
			// .on("mouseover", function(d){
		 //        tooltip.style("visibility", "visible");
		 //        tooltip_text.text(d.properties.text);
		 //        tooltip_latlng.text("Coordinates: " + d.properties.coordinates);
		 //    })
		 //    .on("mousemove", function(){
		 //        return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");
		 //    })
		 //    .on("mouseout", function(){
		 //        return tooltip.style("visibility", "hidden");
// 			})

			;
		    

		// function to update the data
		function update() {

			// get bounding box of data
		    var bounds = path.bounds(data),
		        topLeft = bounds[0],
		        bottomRight = bounds[1];

		    var buffer = 50000;

		    // reposition the SVG to cover the features.
		    svg.attr("width", bottomRight[0] - topLeft[0] + (buffer * 2))
		       .attr("height", bottomRight[1] - topLeft[1] + (buffer * 2))
		       .style("left", (topLeft[0] - buffer) + "px")
		       .style("top", (topLeft[1] - buffer) + "px");

		    g_line.attr("transform", "translate(" + (-topLeft[0] + buffer) + "," + (-topLeft[1] + buffer) + ")");
		    // update circle position

		    g.attr("transform", "translate(" + (-topLeft[0] + buffer) + "," + (-topLeft[1] + buffer) + ")");

			lines
				.attr("x1", function(d) { return projectPoint(d.coordinates[0], d.coordinates[1]).x; })
				.attr("y1", function(d) { return projectPoint(d.coordinates[0], d.coordinates[1]).y; })
				.attr("x2", function(d) { return projectPoint(d.coordinates[2], d.coordinates[3]).x; })
				.attr("y2", function(d) { return projectPoint(d.coordinates[2], d.coordinates[3]).y; });

		    connectedP
		    	.attr("cx", function(d) { return projectPoint(d.geometry.coordinates[0], d.geometry.coordinates[1]).x; })
		    	.attr("cy", function(d) { return projectPoint(d.geometry.coordinates[0], d.geometry.coordinates[1]).y; });


		    originP
		    	.attr("cx", function(d) { return projectPoint(d.geometry.coordinates[0], d.geometry.coordinates[1]).x; })
		    	.attr("cy", function(d) { return projectPoint(d.geometry.coordinates[0], d.geometry.coordinates[1]).y; });
		    	//.attr("r", function(d) { return projectPoint(d.properites.price)})				
		};

		// call function to 
		update();

		map.on("viewreset", update);

	});
};

updateData();

var structure = null;
var refreshPeriod = 40;
var postVisitorPositionEnabled = true;
var getStatusEnabled = true;
var mousePos = null;

$( document ).ready(function() {
    console.log( "ready!" );
	
	$.get( 'http://localhost:5000/sensors', function( data ) {
		//alert( "Sensors: " + JSON.stringify( data ) );
		structure = data;
		
		var c = document.getElementById("myCanvas");
		var ctx = c.getContext("2d");
		
		c.addEventListener('mousemove', function(evt) {
				mousePos = getMousePos(c, evt);
			}, false
		);
		
		for (var key in data) {
			if (data.hasOwnProperty(key)) {
				//console.log(key + " -> " + p[key]);
				var sensors = data[key];
				for (var i = 0; i < sensors.length; ++i) {
					//alert(myStringArray[i]);
					var sensor = sensors[i];
					
					ctx.fillStyle="#0000FF";
					ctx.beginPath();
					ctx.arc(sensor.x * 500.0,sensor.y * 500.0,0.2 * 500.0,0,2*Math.PI);
					ctx.fill();
				}
			}
		}
		
		setTimeout(onTimer, refreshPeriod);
	});
});

function getMousePos(canvas, evt) {
	var rect = canvas.getBoundingClientRect();
	return {
		x: (evt.clientX - rect.left) / 500.0,
		y: (evt.clientY - rect.top) / 500.0
	};
}

function updateMousePos() {
	if( mousePos == null )
		return;
	
	if( !postVisitorPositionEnabled )
		return;

	postVisitorPositionEnabled = false;
	//console.log('Mouse position: ' + mousePos.x + ',' + mousePos.y);
	$.ajax({
		type: 'POST', 
		contentType: 'application/json',
		url: "http://localhost:5000/visitor_position",
		dataType: "json",
		data: JSON.stringify(mousePos),
		complete: function (response, textStatus, jqXHR) {
			postVisitorPositionEnabled = true;
		}
	});	
}

function refreshStatus() {
	if( !getStatusEnabled )
		return;
		
	getStatusEnabled = false
	$.ajax({
		type: 'GET', 
		contentType: 'application/json',
		url: "http://localhost:5000/status",
		dataType: "json",
		success: function( data ) {
			var c = document.getElementById("myCanvas");
			var ctx = c.getContext("2d");
			for (var key in data) {
				if (data.hasOwnProperty(key)) {
					var sensors = data[key];
					for (var name in sensors) {
						if (sensors.hasOwnProperty(name)) {
							value = sensors[name];
							if( value > 0.0 ) {
								ctx.fillStyle="#FF0000";
							}
							else {
								ctx.fillStyle="#0000FF";							
							}
							
							sensor = findSensor( key, name );
							if( sensor != null ) {
								ctx.beginPath();
								ctx.arc(sensor.x * 500.0,sensor.y * 500.0,0.2 * 500.0,0,2*Math.PI);
								ctx.fill();
							}							
						}
					}
				}
			}
		},
		complete: function (response, textStatus, jqXHR) {
			getStatusEnabled = true;
		}
	});
}

function onTimer() {
	updateMousePos();
	refreshStatus();
	
	setTimeout(onTimer, refreshPeriod);
}

function findSensor( type, name ) {
	if (structure.hasOwnProperty(type)) {
		var sensors = structure[type];
		for (var i = 0; i < sensors.length; ++i) {
			//alert(myStringArray[i]);
			var sensor = sensors[i];
			if( sensor.name == name )
				return sensor;
		}
	}
	
	return null;
}
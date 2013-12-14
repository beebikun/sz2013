function getMouse(e, el){
	var box = el.getBoundingClientRect(),
	body = document.body
	docElem = document.documentElement,
	scrollTop = window.pageYOffset || docElem.scrollTop || body.scrollTop,
	scrollLeft = window.pageXOffset || docElem.scrollLeft || body.scrollLeft,
	clientTop = docElem.clientTop || body.clientTop || 0,
	clientLeft = docElem.clientLeft || body.clientLeft || 0,
	y = box.top +  scrollTop - clientTop,
	x = box.left + scrollLeft - clientLeft;
	elementPos = { y: Math.round(y), x: Math.round(x)}
	var bodyScroll = document.body.scrollTop;
	var top =  (bodyScroll) ? bodyScroll : document.documentElement.scrollTop;					
	var mouse = {
		x: e.clientX - elementPos.x,
		y: e.clientY - elementPos.y + top
	}
	return mouse
}

function spriteName(name){
	return '../static/leboski/sprites/' + name
}

function drawTartanOnCanvas(){
	var dark = '#444';
	var light = '#f8f8f8';		
	function drawTartanBox(color, x, y){
		var x = x || 0; var y = y || 0;
		/*var color = (color===undefined || color==light) ? dark : light*/
		/*ctx.fillStyle = color;
		ctx.fillRect(x, y, boxW, boxH)*/
		var color = light;
		ctx.strokeStyle = color;
		ctx.strokeRect(x, y, boxW, boxH)
		if(x<(canvas.width-boxW)) return drawTartanBox(color, x+boxW, y)
		else{
			if(y<(canvas.height-boxH)) return drawTartanBox(color, 0, y+boxH)
			else return
		}
	}
	drawTartanBox()
}

function getRandomInt (max) {
	return Math.floor(Math.random() * (max + 1));
}
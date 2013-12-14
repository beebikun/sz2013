var api = {}
api.root = window.location.protocol+'//'+window.location.host + '/'
api.sz = {}
api.sz.root = api.root + 'api/'
api.sz.generatePlaces = api.sz.root + 'testmode/generate-places/'
api.sz.places = api.sz.root + 'testmode/places/'

function testImage(){
	var realSize = [100, 100]
	var needSize = [32, 32]
	var imgsrc = '../static/lebowski/sprites/t1.png'
	var pic     = new Image();
	pic.src = imgsrc;
    pic.onload = function () {
        // Иллюстрация для пример №1
       /* ctx.drawImage(pic, 0, 0);*/
        // Иллюстрация для пример №2
        ctx.drawImage(pic, 0, 130, needSize[0], needSize[1]);
        // Иллюстрация для пример №3
        ctx.drawImage(pic, 100, 0, realSize[0], realSize[1], 0, 0, needSize[0], needSize[1]);
    }
}

$(document).ready(function(){
	$('input').filter('[name=searchPlace]').keydown(function(){
		var val = $(this).val()
		towers_list.search_t_by_val(val)
	})

	canvas.addEventListener('click', function(e) { 
		var mouse =  getMouse(e, this);
		var t = towers_list.find_t_in_pos(mouse)
		if(t) t.set_active()
		else towers_list.unactive_all()
	}, false);		

	
	drawTartanOnCanvas()	
	

	resources.load([
	    spriteName('t1.png'),
	    spriteName('t1_active.png'),
	]);
	resources.onReady(init);
	
	/*testImage();*/


	/*$("#startBtn").click(function(){
		var txt = $(this).text()
		var $btn = $(this)
		if(txt=='Начать'){
			$btn.addClass('disabled')
			$.getJSON(api.sz.places,{},function(data){
				var places_list = data.data.venues
				$.each(places_list,function(i,p){
					drawTower(p.place_name,p.place_longitude,p.place_latitude)
				})
				$btn.removeClass('disabled')
				$btn.text('Пауза')
			})
		}
		else if(txt=='Пауза'){
			$btn.addClass('disabled')
			//do something
			$btn.removeClass('disabled')
			$btn.text('Продолжить')
		}
		else if(txt=='Продолжить'){
			$btn.addClass('disabled')
			//do something
			$btn.removeClass('disabled')
			$btn.text('Пауза')	
		}
		else{
			//??
		}
	})*/
});
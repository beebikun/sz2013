var requestAnimFrame = (function(){
    return window.requestAnimationFrame    ||  
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame    ||
        window.oRequestAnimationFrame      ||
        window.msRequestAnimationFrame     ||
        function(callback){
            window.setTimeout(callback, 1000 / 60);
        };
})();


var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
canvas.width = 1000;
canvas.height = 1000;
var boxCount = 30;
var boxStep = 0.00033;
var boxW = canvas.width/boxCount;
var boxH = canvas.height/boxCount;


var towers_list = new Towers;

var users = [];
var gameTime = 0;
var isGamePause;
var lastTime;

// Update game objects
function update(dt) {
	gameTime += dt;
	updateEntities(dt)
}
function updateEntities(dt) {
	//update all objects
	$.each(towers_list.list, function(i, t){			
    	t.update(dt)
    })
}
// Draw everything
function render() {
    $.each(towers_list.list, function(i, t){
    	ctx.save();
    	t.render();
    	ctx.restore();
    })
};
//main loop
function main() {
    if(!isGamePause){
	    var now = Date.now();
	    var dt = (now - lastTime) / 1000.0;

	    update(dt);
	    render();

	    lastTime = now;	    	
    }
    requestAnimFrame(main);
};

function init(){
	$.getJSON(api.sz.places,{},function(data){
		var places_list = data.data.venues
		$.each(places_list,function(i,p){
			var lid =  't' + i
			var placeStr = '<p class="tower-items" id="'+ lid +'">' +
								'<a>' +
									p.place_name + 
								'</a>' +
							'</p>'
			$('#places .obj-list').append(placeStr)
			var $placeStr = $('#places .obj-list').find('#'+lid)
			var x = Math.floor((p.place_longitude*boxCount/100)/boxStep)*boxW;
			var y = Math.floor((p.place_latitude*boxCount/100)/boxStep)*boxH;	
			var tower = new Tower([x, y], [p.place_longitude, p.place_latitude], p.place_name, lid, undefined)
			towers_list.list.push(tower)
			$placeStr.click(function(){tower.set_active()})
			lastTime = Date.now();
			main();
		})
	})	
}
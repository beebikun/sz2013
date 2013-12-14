function Tower(pos, coordinates, name, lid, race){
	this.active = false
	this.show = true
	this.coordinates = coordinates //real coordinates
	this.name = name
	this.lid = lid
	this.sprite = new Sprite(spriteName('t1.png'), pos, [boxW, boxH],[100,100], 0, [0,1])	
	this.render = function(){
		this.sprite.render(ctx)
	}
	this.update = function(dt){
		this.sprite.speed = this.active ? 2 : 0
		/*this.sprite.size = this.show ? [boxW, boxH] : [0, 0]*/
		this.sprite.pos = this.show ? this.sprite.pos : [this.sprite.pos[0]-boxW, this.sprite.pos[1]-boxH]
		this.sprite.update(dt)
	}
	this.set_active = function(){
		/*var $li = $('#places .obj-list').find('#'+this.lid)
		$li.siblings().removeClass('active')
		$li.addClass('active')*/
		$('#places .obj-detail .obj-detail-name').text(this.name)
		$('#places .obj-detail .obj-detail-coordinates').text(this.coordinates)
		$('#places .obj-list').slideUp(200)
		$('#places .obj-detail').slideDown(200)
		$.each(towers_list.list, function(i, t){t.active = false })
		this.active = true
	}
	this.hide_show = function(show){		
		var $li = $('#places .obj-list #'+this.lid)
		if(show){
			$li.show();
			this.show = true
		}
		else{
			$li.hide();
			this.show = false
		}
	}
}

function Towers(){
	this.list = []
	this.unactive_all = function(){
		$.each(this.list, function(i, t){t.active = false;})
		$('#places .obj-list').slideDown(200)
		$('#places .obj-detail').slideUp(200)
	};
	this.find_t_in_pos = function(pos){
		var this_t;
		$.each(this.list, function(i, t){
			var x = t.sprite.pos[0];
			var maxX = x + t.sprite.size[0];
			var y = t.sprite.pos[1];
			var maxY = y + t.sprite.size[1];
			if((x<=pos.x&&pos.x<=maxX) && (y<=pos.y&& pos.y<=maxY)) {
				this_t = t
				return false
			}
		})
		return this_t
	};
	this.search_t_by_val = function(val){
		$.each(this.list, function(i, t){
			if(!val)t.hide_show(true);
			else{
				if(t.name.toLowerCase().indexOf(val.toLowerCase())>=0) t.hide_show(true)
				else t.hide_show(false)
			}
		})
	}
}
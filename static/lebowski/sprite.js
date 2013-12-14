function spriteName(name){
	return '../static/lebowski/sprites/' + name
}
function Sprite(url, pos, size, realsize, speed, frames, dir, once) {	
    this.pos = pos;
    this.size = size;
    this.realsize = realsize || size;
    this.speed = typeof speed === 'number' ? speed : 0;
    this.frames = frames;
    this._index = 0;
    this.url = url;
    this.dir = dir || 'horizontal';
    this.once = once;
};
Sprite.prototype.update = function(dt) {
    this._index += this.speed*dt;
}
Sprite.prototype.render = function(ctx) {
    var frame;
    if(this.speed > 0) {
        var max = this.frames.length;
        var idx = Math.floor(this._index);
        frame = this.frames[idx % max];

        if(this.once && idx >= max) {
            this.done = true;
            return;
        }
    }
    else {
        frame = 0;
    }


    var x = this.pos[0];
    var y = this.pos[1];
    var in_x = 0;
    var in_y = 0

    if(this.dir == 'vertical') {
        in_y += frame * this.realsize[1];
    }
    else {
        in_x += frame * this.realsize[0];
    }
    ctx.drawImage(resources.get(this.url),
                  in_x, in_y,
                  this.realsize[0], this.realsize[1],
                  x, y,
                  this.size[0], this.size[1]);
}
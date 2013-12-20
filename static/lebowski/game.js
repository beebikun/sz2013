

function get_boxes_without_t(list){
    return list.filter(function(b){return })
}

function get_clear_boxes(){
    return MAP.filter(function(b){return  !TOWERS.list.filter(function(t){return t.box.id==b.id}).length})
}
function get_neirby_boxes(box){
    //find 8 nearby boxes
    return MAP.filter(function(b){
            if( (box.rx - BOX_WIDTH) == b.rx && (box.ry - BOX_HEIGHT) == b.ry) return true  //left top box
            if( box.rx == b.rx && (box.ry - BOX_HEIGHT) == b.ry) return true                //top box
            if( (box.rx + BOX_WIDTH) == b.rx && (box.ry - BOX_HEIGHT) == b.ry) return true  //right top box                
            if( (box.rx - BOX_WIDTH) == b.rx && box.ry == b.ry) return true                 //left box
            if( (box.rx + BOX_WIDTH) == b.rx && box.ry == b.ry) return true                 //right box
            if( (box.rx - BOX_WIDTH) == b.rx && (box.ry + BOX_HEIGHT) == b.ry) return true  //left bottom box
            if( box.rx == b.rx && (box.ry + BOX_HEIGHT) == b.ry) return true                //bottom box
            if( (box.rx + BOX_WIDTH) == b.rx && (box.ry + BOX_HEIGHT) == b.ry) return true  //right bottom box
            return false
        })
}

TOWERS = {
    list : [],
    deselect: function(){TOWERS.list.forEach(function(t){t.set_unactive()});},
    remove: function(){
        TOWERS.list.forEach(function(t){t.el.remove();})
        TOWERS.list = [];
    },
    created:function(){
        return TOWERS.list.filter(function(t){return t.is_create})
    }

}
function newTower(name, location){    
    var tower = {
        name:name, 
        location:location, 
        users:[], 
        /*is_create: false,*/
        is_create: true,
        level:get_random_num(5,1)
    }
    var box = get_clear_boxes().filter(function(b){
        return (location.lat>=b.lat&&location.lat<=b.lat+BOX_STEP&&location.lng>=b.lng&&location.lng<=b.lng+BOX_STEP)
    });
    if(!box.length) return
    tower.box = box[0]
    tower.id = 'tower_' + (TOWERS.list.length + 1)
    if( $("#"+tower.id).length ) return 
    var el =  '<div id="' + tower.id  + '" class="map-obj place place-unknown">' + 
                '<div class="obj-circle"></div>' + 
                '<i class="fa fa-flag " ></i>' + 
              '</div>';
    $( "#map-towers" ).append(el)
    tower.el = $("#"+tower.id)
    tower.el
        .css({top:tower.box.ry+'px', left:tower.box.rx+'px', fontSize:Math.ceil(BOX_HEIGHT*0.6)+'px'})
        .width(BOX_WIDTH).height(BOX_HEIGHT)
        .click(function(){tower.set_active()});
    tower.set_active = function(){
        TOWERS.deselect();
        tower.el.children('.obj-circle').animate({opacity:1,width:'100%',height:'100%',marginTop:0,marginLeft:0},200);

        tower.push_users();

        $( "#main-settings" ).hide();
        var m = $( "#settings" ).data("margin");
        if( m===undefined || parseInt($( "#settings" ).css(m.d))!=0) $( "#settings .unwrap-menu i" ).click();        
        $( "#place-settings #place-header-name" ).text(tower.name)
        $( "#place-settings #place-location p:first-child span" ).text(tower.location.lng)
        $( "#place-settings #place-location p:last-child span" ).text(tower.location.lat)
        $( "#place-settings" ).show();
    }
    tower.set_unactive = function(){tower.el.children('.obj-circle').css({opacity:0,width:0,height:0,marginTop:'50%',marginLeft:'50%'}) }
    tower.push_users = function(){
        $( "#place-userslist" ).empty();
        for (var i = tower.users.length - 1; i >= 0; i--) {$( "#place-userslist" ).append(get_user_li_elemets(userlist[i], true)) };
    }     
    function create_in_db(){
        //
    }
    /*add_log_element('client', 'Create a new Tower "' + tower.name +'"')*/
    return tower
}

var USERS = {
    list:[],
    is_live:true,
    live:function(){
        USERS.list.forEach(function(u){u.live()})        
    }
}

function newUser(params){
    //race is Array, gender is Array, speed, activity
    var user = {
        race     : params.race,
        gender   : params.gender,
        speed    : parseInt(params.speed),
        activity : parseInt(params.activity),
        name     : get_random_name()
    }; 
    //get a random free point on map
    user.box = get_random(get_clear_boxes());
    user.id = 'user_' + (USERS.list.length + 1)

    var el =  '<div id="' + user.id  + '" class="map-obj user user-' + user.race[0] + '">' + 
                '<div class="obj-circle"></div>' + 
                '<i class="fa fa-' + ( user.gender[0]=='f' ? 'female' : user.gender[0]=='m' ? 'male' : 'smile-o') + '" ></i>' + 
              '</div>';
    $( "#map-users" ).append(el);
    user.el = $("#"+user.id)
    user.el
        .css({top:user.box.ry+'px', left:user.box.rx+'px', fontSize:Math.ceil(BOX_HEIGHT*0.8)+'px'})
        .width(BOX_WIDTH).height(BOX_HEIGHT)
    
    user.lastMessage = Date.now();
    function _explore(){
        //explore code here//
    }
    function _message(){
        var dev = 200;
        if((Date.now() - user.lastMessage) < ( get_random_num(1000+dev, 1000-dev)*360/user.activity ) ) return

        _explore()

        //send message code here//
        var target = get_random( TOWERS.created() )
        var message = get_random_text()

        //animate sending message        
        var color = get_random( COLOR_LIST )
        function _message_animate(i){            
            i.el.find('i').css({ borderColor: color })
            window.setTimeout(function(){i.el.find('i').removeAttr('style')}, 400)
        }
        _message_animate(target)
        _message_animate(user)

        user.lastMessage = Date.now();
    }
    user.live = function(){
        //move on one box with speed user.speed*1000/60
        var nearby_list = get_neirby_boxes(user.box);
        var next_box = get_random(nearby_list);
        user.box = next_box || user.box;        
        user.el.stop().animate({top:user.box.ry+'px', left:user.box.rx+'px'}, 360*100/user.speed, function(){            
            _message();
            user.live();
        })
    }

    function _create_in_db(){
        $.getJSON(API.user.users_registration, function(data){
            console.log(data)
        })
        return true
    }
    var is_create = _create_in_db();

    /*add_log_element('client', 'Create a new User "' + user.name +'"')  */ 
    return is_create ? user : is_create
}

function create_new_users(preUsers){    
    var old_len = USERS.list.length;
    preUsers.forEach(function(params){
        var u = newUser(params);
        if(u) USERS.list.push( u )
    });
    add_log_element('client', 'Create new ' + ( USERS.list.length - old_len ) +' users on map');
    update_all_users_list();
    USERS.live();
}

var MAP;
function newBox(x,y){
    var box = {
        id:"box_" + (MAP.length + 1),
        lng:x*BOX_STEP,
        lat:y*BOX_STEP,
        rx:Math.floor(x*BOX_WIDTH),
        ry:Math.floor(y*BOX_HEIGHT)
    }
    $( "#map-boxes" ).append('<div class="box" id="'+ box.id +'"></div>');
    box.el = $( "#" + box.id );
    box.el.css({ top:box.ry+'px', left:box.rx +'px' }).width(BOX_WIDTH).height(BOX_HEIGHT);
    return box
}

function init(){
    MAP = new Array;
    TOWERS.list = new Array;
    USERS.list = new Array;
    var mapBox = document.getElementById("map").getBoundingClientRect();
    for (var x=0; x <= BOX_VALUE-1; x++) {
        for (var y=0; y <= BOX_VALUE-1; y++) {
            var box = newBox(x, y)
            MAP.push(box);
        }
    };
    PLACES_LIST.forEach(function(p){
        var t = newTower(p.name, p.location)
        if(t) TOWERS.list.push( t )
    })
    update_all_places_list();
    update_all_users_list();
    add_log_element('client', 'Create new ' + TOWERS.list.length +' towers on map')
}
function MasterPageController($scope,$cookies, $http) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;


    var getCurrentPosition = function (onSuccess, onError, options) {
        navigator.geolocation.getCurrentPosition(function () {
                var that = this,
                    args = arguments;

                if (onSuccess) {
                    $scope.$apply(function () {
                        onSuccess.apply(that, args);
                    });
                }
            }, function () {
                var that = this,
                    args = arguments;

                if (onError) {
                    $scope.$apply(function () {
                        onError.apply(that, args);
                    });
                }
            },
            options);
    }
    getCurrentPosition(
        function (position) { $scope.coordinates = position.coords; },
        function (error) { $scope.coordinates = { longitude: 128, latitude: 56 };}
    )
}

var events = {}

MasterPageController.$inject = ['$scope','$cookies', '$http', '$location'];

function HomeController($scope){}

function PlaceCreateController($scope,placeService){    
    $scope.blockPlacesList = []

    $scope.exploreThisBlock = function(){
        var params = {'latitude':$scope.coordinates.latitude,'longitude':$scope.coordinates.longitude}
        var blockPlacesList = placeService.exploreInVenues(params,function(){$scope.blockPlacesList = blockPlacesList})
    }

}
function MessageCreateController($scope){}
/*2 controllers for message-create*/
function MessageEditorController($scope, messagePreviewService, $routeParams, $location){
    /*for stage1*/    
    if (angular.isDefined($routeParams.placeId))
        placeService.get({placeId: $routeParams.placeId}, function(resp){ $scope.placeHeader = resp; })    
/*    if (angular.isDefined($routeParams.previewId))
        messagePreviewService.get({previewId: $routeParams.previewId}, function(response){
            $scope.text = response.text;
            $scope.photoUrl = response.photo.thumbnail;
            $scope.placeHeader = response.place;
        });*/
    $scope.text = "Английские воины ходят в брюках\nпод которыми есть трусы,\nони храбрее всех на свете,\nим не страшны шотландские псы."
    $scope.photo = {'name':''};

    $scope.remove = function(){
        $scope.photo = $scope.photo
    }

    $scope.send = function() {    
        $scope.inProgress = true;
        var message = new FormData();
        
        message.append( 'place', /*$routeParams.placeId*/150);
        message.append( 'text', $scope.text);
        if($scope.photo.name){message.append( 'photo', $scope.photo);}
        message.append( 'face', 5);

        var redirectToPublish = function(previewId){
            var pub_page_url = '/message-create/' + previewId + '/publish';
            $location.path(pub_page_url);
        }

        if (angular.isUndefined($routeParams.previewId))
            messagePreviewService.create(message,
                function(response){
                    $scope.inProgress = false;
                    $scope.response = response;
                  /*  var edit_page_url = '/message-create/' + $scope.response.id + '/edit';
                    history.replaceState(null, "SZ - Edit message", '#' + edit_page_url);
                    redirectToPublish(response.id);*/
                },
                function(error){alert(angular.toJson(error, true));});
        else
            messagePreviewService.update($routeParams.previewId, message,
                function(response){
                    $scope.inProgress = false;
                    $scope.response = response;
                    /*redirectToPublish(response.id);*/
                },
                function(error){alert(angular.toJson(error, true));});
    }
    $scope.next = function(){
        var previewId = $scope.response.id;
        var pub_page_url = '/message-create/' + previewId + '/publish';
        $location.path(pub_page_url);
    }
}

function MessagePublisherController($scope, messagePreviewService, $routeParams){
    /*for stage2*/
    $scope.photoSrc = ''
        if (angular.isDefined($routeParams.previewId))
        var preview = messagePreviewService.get({previewId: $routeParams.previewId}, function(){
            $scope.preview = preview;
            $scope.placeHeader = preview.place;
            $scope.add_categories = []
            $scope.photoSrc = preview.photo.reduced
        /*    $.each($scope.categories, function(index,cat){$scope.add_categories.push(cat)});
            $.each($scope.preview.categories, function(index,catID){
                $.each($scope.categories,function(index,cat){
                    if(catID == cat.id){
                        $scope.new_message_categories.push(cat)
                    }
                });
            });  */          
         /*   for (i in $scope.add_categories){
                var cat = $scope.add_categories[i];
                for (j in $scope.preview.categories){
                    var catID = $scope.preview.categories[j]
                    if(catID==cat.id){$scope.add_categories.splice(i,1)}
                }
            } */               
            
        });    
    $scope.action = 1;
    $scope.facesPositionList = {'faces':[],'photoBox':{}}
    $scope.isSend = false;
    $scope.send = function(){
        $scope.isSend = true;
        $scope.$watch($scope.facesPositionList.faces.length,function(){
            $scope.preview.photo.faces = $scope.facesPositionList       
            $scope.preview.latitude = 
            $scope.preview.longitude = $scope.coordinates.longitude
            $scope.preview.$publish(
                {},
                function(response){
                    $scope.response = response
                    /*var path = '/places/' + $scope.preview.place.id;
                    $location.path(path);*/
                },
                function(error){
                    $scope.inProgress = false;
                    throw "can't publish";
                }
            )
        })        
    }
}

function RegistrationController($scope,userService){
	$scope.user = {}
	var alphabet = 'abcdefghiklmnopqrstvxyz'
    	function RandomEmail(l,s){
    		var s = s || alphabet[Math.floor(Math.random()*23)];
    		var s = s + alphabet[Math.floor(Math.random()*23)];
    		if(s.length<l){return RandomEmail(l,s)}
    		else{return s+'@shzh.me'} 
    	}
    
    $scope.user = {
    	'email':RandomEmail(5),
    	'password1':'12345',
    	'password2':'12345',
    	'gender':2,
    	'race':2
    }


    $scope.registration = function(){
    	userService.register($scope.user,
            function(response){
                $scope.response = response
            },
            function(error){
                $scope.response = error
        })
    }

    $scope.confirmation = function(){
    	userService.resend_activation_key({'email': $scope.user.email},
	        function(response){
	            $scope.key = response
	        },
	        function(error){
	            $scope.key = ':('
        });
    }
}

function NewsFeedController($scope, placeService, $routeParams, $location){
    $scope.category = '';
    $scope.radiusActive = 0
    $scope.$watch('coordinates', function(newValue, oldValue) {
        if (angular.isDefined($scope.coordinates)){
            var params = {};
            if($routeParams.radius){
                params.radius = $routeParams.radius
                $scope.radiusActive = params.radius
            }
            if($routeParams.query){params.query = $routeParams.query}
            if($routeParams.category>0){
                params.category = $routeParams.category
                $.each($scope.categories,function(index,cat){
                    if(cat.id==params.category){
                        $scope.category = cat;
                    }
                })
            }
            params.longitude = $scope.coordinates.longitude;
            params.latitude = $scope.coordinates.latitude;
            $scope.feed = placeService.newsfeed(
                params
            );
        }
    });
    $scope.setRadius = function(radius){
        var params = {}
        if(radius){params.radius = radius};
        if($routeParams.category>0){params.category = $routeParams.category;}
        $location.path('/newsfeed').search(params)
    }
    $scope.$watch('category',function(){
        var params = {}
        if($scope.category){
            params.category = $scope.category.id
        }       
        if($routeParams.radius){
            params.radius = $routeParams.radius
        }
        $location.path('/newsfeed').search(params)
    })
    $scope.loadMorePlaces = function(){
        if ($scope.feed.params.offset + $scope.feed.params.limit < $scope.feed.count)
        {
            $scope.feed.params.offset += $scope.feed.params.limit;
            var feed = placeService.newsfeed($scope.feed.params, function() {
                    if(feed.results.length>0){
                        $.each(feed.results,function(index,r){
                            $scope.feed.results.push(r)
                        });
                        $scope.feed.params = feed.params;
                    }
                    else{$scope.$emit($scope.scrollToTop.top=true);}
                }
            );
        }
    }
    $scope.placeMessagesLimit = 1;
}
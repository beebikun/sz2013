'use strict';

/* Directives */

angular.module('sz.client.directives', [])
	.directive('szFileModel', function() {
        return function(scope, element, attrs) {
            var $photoNameCont = $("#photoPrevName");
            var $photoCont = document.getElementById('photoPrev');
            var $photoBigCont = $('#photoBigCont')
            scope.$watch(attrs.szFileModel, function() {
                angular.element(element[0]).bind('change', function(){
                    if (angular.isUndefined(element[0].files))
                    {throw new Error("This browser does not support HTML5 File API.");}
                    if (element[0].files.length == 1){
                        scope[attrs.szFileModel] = element[0].files[0]
                        var photo = element[0].files[0];
                        var photoName = photo.name;
                        $photoNameCont.text(photoName)
                        if (photo.type.match('image.*')) {
                            var reader = new FileReader();
                            reader.onload = (function(theFile) {
                                return function(e) {
                                    $photoCont.innerHTML = ['<img  src="', e.target.result,
                                                        '" title="', escape(photoName), '" style="width:100%"/>'].join('');
                                };                                
                            })(photo);      
                            reader.readAsDataURL(photo);
                            $photoBigCont.show()

                        }
                        else{photoNameCont.innerHTML = ['Недопустимый формат'].join('');}
                    }
                });            
            });

            scope.$watch('photo.name',function(){
                if(scope.photo.name){
                    $photoNameCont.text('')
                    $photoCont.innerHTML = [].join('');
                    scope.photo = {'name':''}
                    $photoBigCont.hide()
                }
            })
        }
    })
	.directive('szDrawFaces', function() {
        return function(scope,element,attr){
        		var photoWithoutFaces = function(){
					if(scope.photoSrc){
						var img = element[0],
							imgSrc = scope.photoSrc,
			        		canvasWidth = $(img).width(),
			        		canvasHeight = $(img).height(),
			        		canvasTop = $(img).offset().top,
			        		canvasLeft = $(img).offset().left,
			        		faceHeight = 50,
			        		faceWidth = 50,
			        		minFaceWidth = 30,
			        		minFaceHeight = 30,
			        		faceStep = 15, //приростание в размере за один хоп
			        		faceSrc = 'img/face.png';	
		        		scope.facesList = new Array;
		        		$(img).parent().width(canvasWidth).height(canvasHeight)        		
			    		img.style.display = "none";			    		
						var paper = Raphael(canvasLeft, canvasTop, canvasWidth, canvasHeight);
						scope.photo = paper.image(imgSrc, 0, 0, canvasWidth, canvasHeight);
						var convertPositionInCanvas = function(globalX,globalY){
							var bodyScroll = document.body.scrollTop;
							var top =  bodyScroll && bodyScroll || document.documentElement.scrollTop;
							return {'x':globalX - canvasLeft, 'y':globalY - canvasTop + top}
						}
						var drawNewFace = function(x,y,t){											
							var faceX = x - faceWidth/2, faceY = y - faceHeight/2,
								face = paper.image(faceSrc,faceX,faceY,faceWidth,faceHeight);
							function changeVal(obj,step){
								var oldX = obj.attr('x'), oldY = obj.attr('y'),
									newW = obj.attr('width') + step, newH = obj.attr('height') + step,
									newX = oldX - step/2, newY = oldY - step/2;
								obj.animate({width:newW, height:newH, x:newX, y:newY}, obj.t, "backIn"
								);
							};	
							function canEnlarge(obj){
								var left = obj.attr('x'),
									right = obj.attr('x') + obj.attr('width'),
									top = obj.attr('y'),
									bottom = obj.attr('y') + obj.attr('height');
								return left>0&&right<canvasWidth&&top>0&&bottom<canvasHeight
							}
							function canReduce(obj,step){return obj.attr('height')>minFaceHeight&&obj.attr('width')>minFaceWidth }
							face.enlarge = function(){if(canEnlarge(this)){changeVal(this,faceStep)} }
							face.reduce = function(){
								if(canReduce(this,faceStep)){changeVal(this, faceStep*-1)}
								else{
									var thisFace = this
									$.each(scope.facesList,function(num,f){
										if(f==thisFace){									
											scope.facesList.pop(num)
											return false
										}
									})							
									face.remove()
								}
							}					
							face.mousedown(function(e){
								var intervalID = setInterval(function(){
										if(scope.action==1){face.enlarge()}
										else{face.reduce()}
									},face.t);
								$(this).data('intervalID', intervalID)})
							face.mouseup(function(e){
								if(this.i){
									clearInterval(this.i);
									this.i = false;
								}
								var intervalID = $(this).data('intervalID');
								clearInterval(intervalID)
							})
							scope.facesList.push(face)					
							return face
						};							
						
						scope.photo.mousedown(function(e){								
							var mouse = convertPositionInCanvas(e.clientX, e.clientY),
								t = 500;
							if(scope.action==1){
								var newface = drawNewFace(mouse.x,mouse.y),
								intervalID = setInterval(function(){newface.enlarge()},t);
								newface.i = intervalID
								newface.t = t
							}
						})						
					}
				}
				scope.$watch('photoSrc', photoWithoutFaces);
//Это какой-тло ацкий костыль из-за того что я слишком тупая чтобы читать документацию
//но все равно странно получается - вот я работаю с scope.facesList - меняю в одной функции и вижу изменения в другой
//А в скопе выше уже не вижу. Хотя если делать изменения здесь же, но не в теле функции - то все вижу
//Вообщем сейчас, когда нажимаешь кнопку сенд на странице меняется вспомогательная переменная isSend на тру. И вот тут есть вотч, который за ней следит
//и когда она тру - запихивает массивы из scope.facesList в scope.facesPositionList
//а в котроллере вотч следит за длинной массива scope.facesPositionList и вот когда в нем что-то появиться - тогда и делает пост
				scope.$watch('isSend',function(){
					if(scope.isSend){						
						var img = element[0];
						scope.facesPositionList.photoBox = scope.photo.getBBox()
						$.each(scope.facesList,function(n,f){
							var box = f.getBBox()
							if(box) {
								box.face = 2
								scope.facesPositionList.faces.push(box)
							}
						})			
						if(scope.facesPositionList.faces.length==0){
							scope.facesPositionList.faces = [{}]
						}			
					}					
				});

			
        }
    })

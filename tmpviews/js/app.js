'use strict';
var szApp = angular.module('sz.client', ['sz.client.directives', 'sz.client.services', 'ngResource', 'ngCookies'])

szApp.config(['$routeProvider', function($routeProvider) {
    $routeProvider
        .when('/', {templateUrl: 'home.html', controller: HomeController})
        .when('/user-registration', {templateUrl: 'user-registration.html', controller: RegistrationController})
        .when('/place-create', {templateUrl: 'place-create.html', controller: PlaceCreateController})
        .when('/message-create/', {templateUrl: 'message-create.html', controller: MessageEditorController})
        .when('/message-create/:previewId/publish', {templateUrl: 'message-create-publish.html', controller: MessagePublisherController})
        .when('/newsfeed', {templateUrl: 'newsfeed.html', controller: NewsFeedController})
        .otherwise({redirectTo: '/'});
}]);

szApp.config(['$httpProvider', function($httpProvider){
    $httpProvider.responseInterceptors.push(function($q) {
        return function(promise){
            return promise.then(function(response) {
                if (angular.isDefined(response.data.data))
                    response.data = response.data.data;
                return response;
            }, function(response) {
                console.error(angular.toJson(response.data));
                return $q.reject(response);
            });
        }
    });
}]);

szApp.constant('ENDPOINT','LOCAL');
'use strict';

angular.module('myApp.view2', ['ngRoute'])

.config(['$routeProvider', function ($routeProvider) {
	$routeProvider.when('/view2', {
		templateUrl: 'view2/view2.html',
		controller: 'View2Ctrl'
	});
}])

.controller('View2Ctrl', ["$scope", "$http", "$location", function ($scope, $http, $location) {
	$scope.swap = function () {
		console.log($('form'));
		$('form').animate({ "height": 'toggle', "opacity": 'toggle' }, "slow", function(){});
	};
	$scope.go = function (path) {
		$location.path(path);
	};
}]);
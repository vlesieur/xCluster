'use strict';

angular.module('myApp.view2', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view2', {
    templateUrl: 'view2/view2.html',
    controller: 'View2Ctrl'
  });
}])

.controller('View2Ctrl', function($scope, $http) {
	
	$http({
        method : "GET",
        url : "http://127.0.0.1:3000/"
    }).then(
		function mySucces(response) {
			$scope.test = response.data;
    },  function myError(response) {
			$scope.test = response.statusText;
    });
});
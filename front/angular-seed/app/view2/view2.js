'use strict';

angular.module('myApp.view2', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view2', {
    templateUrl: 'view2/view2.html',
    controller: 'View2Ctrl'
  });
}])

.controller('View2Ctrl', function($scope, $http) {
	
	$scope.test = function(){
		$http({
			method : "GET",
			url : "http://127.0.0.1:3000/"
		}).then(
			function succes(response) {
				$scope.row = $scope.$eval("row",response.data);
				$scope.column = $scope.$eval("column",response.data);
				$scope.img = "../storage/user/" + $scope.$eval("img",response.data)+".png";
		},
			function error(response) {
				$scope.err = response.statusText;
		});	
	}
});


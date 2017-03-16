'use strict';

angular.module('myApp.view2', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view2', {
    templateUrl: 'view2/view2.html',
    controller: 'View2Ctrl'
  });
}])

.controller('View2Ctrl', function($scope, $http) {
	$scope.img = null;
	$scope.row = null;
	$scope.err = null;
	$http({
        method : "GET",
        url : "http://127.0.0.1:3000/"
    }).then(
		function mySucces(response) {
			$scope.row = $scope.$eval("row",response.data);
			var imgSrc = $scope.$eval("img",response.data)+".png";//TODO imgSrc
			//imgSrc = "bower_components/angular-filemanager/bridges/php-local/index.php?action=download&path=%2Fuser%2"+imgSrc;
			//imgSrc = "bower_components/angular-filemanager/bridges/php-local/index.php?action=download&path=%2Fuser%2"+imgSrc;
			
			$scope.img =  imgSrc;
    },  function myError(response) {
			$scope.err = response.statusText;
    });	

});





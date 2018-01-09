'use strict';

angular.module('myApp.view2', ['ngRoute'])
	.config(['$routeProvider', function ($routeProvider) {
		$routeProvider.when('/view2', {
			templateUrl: 'view2/view2.html',
			controller: 'View2Ctrl'
		});
	}])

	.controller('View2Ctrl', ["$scope", "$http", "$location", "$window", function ($scope, $http, $location, $window) {

		if (sessionStorage.getItem("token") != null && sessionStorage.getItem("login") != null) {
			console.log("user " + sessionStorage.getItem("login") + " already logged ! redirecting...");
			$location.path('/view1');
		}

		$scope.swap = function ($event) {
			$('form').animate({ height: "toggle", opacity: "toggle" }, "slow");
			$event.preventDefault();
		};

		$scope.go = function (path) {
			$location.path(path);
		};

		$scope.authenticate = function ($event) {
			$http.post('http://localhost:8090/api/authenticate', { login: $scope.login, password: $scope.password }).then(function (response) {
				console.log("response data authenticate : "+response.data.token);
				if (response.data.success == true) {
					sessionStorage.setItem("token", response.data.token);
					sessionStorage.setItem("login", $scope.login);
					$window.location.reload();
					$scope.go('/view1');
					$event.preventDefault();
				}
				else {
					$scope.msg = response.data.msg;
				}
			});
		}

		$scope.createAccount = function ($event) {
			$http.post('http://localhost:8090/api/signup', { login: $scope.login, password: $scope.password, mail: $scope.email }).then(function (response) {
				console.log("response data create account : "+response.data);
				if (response.data.success == true) {
					sessionStorage.setItem("newUser", "true");
					$scope.authenticate();
					$event.preventDefault();
				}
				else {
					$scope.msg = response.data.msg;
				}
			});
		}
	}]);

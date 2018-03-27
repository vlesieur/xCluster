'use strict';

// Declare app level module which depends on views, and components
angular.module('constants', []) 
.constant('env', {
  API_URL: "http://whispering-shore-32638.herokuapp.com/"
}
)
// For Heroku local, use "http://localhost:5000/"

angular.module('myApp', [
  'constants',
  'ngRoute',
  'myApp.view1',
  'myApp.view2',
  'myApp.version',
  'FileManagerApp'
])
  .config(['$locationProvider', '$routeProvider', function ($locationProvider, $routeProvider) {
    $locationProvider.hashPrefix('!');
    $routeProvider.otherwise({ redirectTo: '/view2' });
  }])
  .controller('View1Ctrl', [function () { }])
  .run(function ($rootScope, $location) {
    document.getElementById('start').style.visibility='hidden';
    $rootScope.$on("$routeChangeStart", function (event, next, current) {
      console.log("route change detected !");
      if (sessionStorage.getItem('token') == null) {
        $location.path("/view2");
      }
    })
  });

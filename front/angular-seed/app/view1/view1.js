'use strict';

angular.module('myApp.view1', ['ngRoute', 'FileManagerApp'])

  .config(['$routeProvider', 'fileManagerConfigProvider', function ($routeProvider, config) {
    $routeProvider.when('/view1', {
      templateUrl: 'view1/view1.html',
      controller: 'View1Ctrl'
    });
    var sessionLogin = sessionStorage.getItem("login");
    var defaults = config.$get();
    console.log("session login : " + sessionLogin);
    console.log("default basePath : " + defaults.basePath);
    config.set({
      appName: 'xcluster-filemanager',
      basePath: sessionLogin != null ? sessionLogin : '/',
      listUrl: 'http://127.0.0.1:8090/lists',
      uploadUrl: 'bower_components/angular-filemanager/bridges/php-local/index.php',
      renameUrl: 'http://127.0.0.1:8090/rename',
      copyUrl: 'bower_components/angular-filemanager/bridges/php-local/index.php',
      moveUrl: 'bower_components/angular-filemanager/bridges/php-local/index.php',
      removeUrl: 'bower_components/angular-filemanager/bridges/php-local/index.php',
      editUrl: 'bower_components/angular-filemanager/bridges/php-local/index.php',
      getContentUrl: 'bower_components/angular-filemanager/bridges/php-local/index.php',
      createFolderUrl: 'http://127.0.0.1:8090/create',
      downloadFileUrl: 'bower_components/angular-filemanager/bridges/php-local/index.php',
      downloadMultipleUrl: 'bower_components/angular-filemanager/bridges/php-local/index.php',
      compressUrl: 'bower_components/angular-filemanager/bridges/php-local/index.php',
      extractUrl: 'bower_components/angular-filemanager/bridges/php-local/index.php',
      permissionsUrl: 'bower_components/angular-filemanager/bridges/php-local/index.php',
	    coclustModUrl: 'http://127.0.0.1:3000/coclust/mod',
	    coclustSpecModUrl: 'http://127.0.0.1:3000/coclust/spec',
	    coclustInfoUrl: 'http://127.0.0.1:3000/coclust/info'
    });
    var newDefaults = config.$get();
    console.log("new basePath : " + newDefaults.basePath);
  }])

  .controller('View1Ctrl', [function ($location) {
    if (sessionStorage.getItem('token') == null) {
      $location.path("/view2");
    }
  }]);
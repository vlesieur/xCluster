'use strict';


angular.module('myApp.view1', ['constants', 'ngRoute', 'FileManagerApp'])

  .config(['$routeProvider', 'fileManagerConfigProvider', 'env', function ($routeProvider, config, env) {
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
      listUrl: env.API_URL+'lists',
      uploadUrl: env.API_URL+'upload',
      renameUrl: env.API_URL+'rename',
      copyUrl: env.API_URL+'copy',
      moveUrl: env.API_URL+'move',
      removeUrl: env.API_URL+'remove',
      editUrl: env.API_URL+'edit',
      getContentUrl: env.API_URL+'read',
      createFolderUrl: env.API_URL+'folder',
      downloadFileUrl: env.API_URL+'download',
      downloadMultipleUrl: '',
      compressUrl: env.API_URL+'compress',
      extractUrl: env.API_URL+'extract',
      permissionsUrl: env.API_URL+'permissions',
      coclustModUrl: env.API_URL+'coclust/mod',
	    coclustSpecModUrl: env.API_URL+'coclust/spec',
	    coclustInfoUrl: env.API_URL+'coclust/info'
    });
    var newDefaults = config.$get();
    console.log("new basePath : " + newDefaults.basePath);
  }])

  .controller('View1Ctrl', [function ($location) {
    if (sessionStorage.getItem('token') == null) {
      $location.path("/view2");
    }
  }]);
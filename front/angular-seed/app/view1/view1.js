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
      uploadUrl: 'http://127.0.0.1:8090/upload',
      renameUrl: 'http://127.0.0.1:8090/rename',
      copyUrl: 'http://127.0.0.1:8090/copy',
      moveUrl: 'http://127.0.0.1:8090/move',
      removeUrl: 'http://127.0.0.1:8090/remove',
      editUrl: 'http://127.0.0.1:8090/edit',
      getContentUrl: 'http://127.0.0.1:8090/read',
      createFolderUrl: 'http://127.0.0.1:8090/folder',
      downloadFileUrl: 'http://127.0.0.1:8090/download',
      downloadMultipleUrl: 'http://127.0.0.1:8090/',
      compressUrl: 'http://127.0.0.1:8090/compress',
      extractUrl: 'http://127.0.0.1:8090/extract',
      permissionsUrl: 'http://127.0.0.1:8090/permissions',
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
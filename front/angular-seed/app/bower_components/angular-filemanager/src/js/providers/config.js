(function(angular) {
    'use strict';
    angular.module('FileManagerApp').provider('fileManagerConfig', function() {

        var values = {
            appName: 'angular-filemanager v1.5',
            defaultLang: 'en',

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
            coclustModUrl: 'http://127.0.0.1:8090/coclust/mod',
            coclustSpecModUrl: 'http://127.0.0.1:8090/coclust/spec',
            coclustInfoUrl: 'http://127.0.0.1:8090/coclust/info',
            basePath: '/',

            searchForm: true,
            sidebar: true,
            breadcrumb: true,
            allowedActions: {
                upload: true,
                rename: true,
                move: true,
                copy: true,
                edit: true,
                changePermissions: true,
                compress: true,
                compressChooseName: true,
                extract: true,
                download: true,
                downloadMultiple: true,
                preview: true,
                remove: true,
                createFolder: true,
                pickFiles: false,
                pickFolders: false,
				coclustMod:true,
				coclustSpecMod:true,
				coclustInfo:true,
            },

            multipleDownloadFileName: 'xCluster_datas.zip',
            filterFileExtensions: [],
            showExtensionIcons: true,
            showSizeForDirectories: true,
            useBinarySizePrefixes: false,
            downloadFilesByAjax: true,
            previewImagesInModal: true,
            enablePermissionsRecursive: true,
            compressAsync: false,
            extractAsync: false,
            pickCallback: null,

            isEditableFilePattern: /\.(txt|diff?|patch|svg|asc|cnf|cfg|conf|html?|.html|cfm|cgi|aspx?|ini|pl|py|md|css|cs|js|jsp|log|htaccess|htpasswd|gitignore|gitattributes|env|json|atom|eml|rss|markdown|sql|xml|xslt?|sh|rb|as|bat|cmd|cob|for|ftn|frm|frx|inc|lisp|scm|coffee|php[3-6]?|java|c|cbl|go|h|scala|vb|tmpl|lock|go|yml|yaml|tsv|lst)$/i,
            isImageFilePattern: /\.(jpe?g|gif|bmp|png|svg|tiff?)$/i,
            isCoclustFilePattern: /\.(mat|xls|csv|tsv|txt)$/i,
            isExtractableFilePattern: /\.(gz|tar|rar|g?zip)$/i,
            isCoclustFormatPattern : /.*_coclustFormat\.(mat|xls|csv|tsv|txt)$/i,
            tplPath: 'src/templates'
        };

        return {
            $get: function() {
                return values;
            },
            set: function (constants) {
                angular.extend(values, constants);
            }
        };

    });
})(angular);

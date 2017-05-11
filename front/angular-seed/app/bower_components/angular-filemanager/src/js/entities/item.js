(function(angular) {
    'use strict';
    angular.module('FileManagerApp').factory('item', ['fileManagerConfig', 'chmod', function(fileManagerConfig, Chmod) {

        var Item = function(model, path) {
            var rawModel = {
                name: model && model.name || '',
                path: path || [],
                type: model && model.type || 'file',
                size: model && parseInt(model.size || 0),
                date: parseMySQLDate(model && model.date),
                perms: new Chmod(model && model.rights),
                content: model && model.content || '',
                recursive: false,
                fullPath: function() {
                    var path = this.path.filter(Boolean);
                    return ('/' + path.join('/') + '/' + this.name).replace(/\/\//, '/');
                },
				n_clusters: model && model.n_clusters || 2, 
				n_row_clusters: model && model.n_row_clusters || 2, 
				n_col_clusters: model && model.n_col_clusters || 2, 
				init: model && model.init || null, 
				max_iter: model && model.max_iter || 20, 
				n_init: model && model.n_init || 1, 
				random_state: model && model.random_state || null, 
				tol: model && model.tol || 0.000000001,
                dict: model && model.dict || 'fea',
                n_terms : model && model.n_terms || 10
				
            };

            this.error = '';
            this.processing = false;

            this.model = angular.copy(rawModel);
            this.tempModel = angular.copy(rawModel);

            function parseMySQLDate(mysqlDate) {
                var d = (mysqlDate || '').toString().split(/[- :]/);
                return new Date(d[0], d[1] - 1, d[2], d[3], d[4], d[5]);
            }
        };

        Item.prototype.update = function() {
            angular.extend(this.model, angular.copy(this.tempModel));
        };

        Item.prototype.revert = function() {
            angular.extend(this.tempModel, angular.copy(this.model));
            this.error = '';
        };

        Item.prototype.isFolder = function() {
            return this.model.type === 'dir';
        };

        Item.prototype.isEditable = function() {
            return !this.isFolder() && fileManagerConfig.isEditableFilePattern.test(this.model.name);
        };

        Item.prototype.isImage = function() {
            return fileManagerConfig.isImageFilePattern.test(this.model.name);
        };

        Item.prototype.isCompressible = function() {
            return this.isFolder();
        };

        Item.prototype.isExtractable = function() {
            return !this.isFolder() && fileManagerConfig.isExtractableFilePattern.test(this.model.name);
        };

        Item.prototype.isSelectable = function() {
            return (this.isFolder() && fileManagerConfig.allowedActions.pickFolders) || (!this.isFolder() && fileManagerConfig.allowedActions.pickFiles);
        };
		
		Item.prototype.isCoclustCompatible = function() {
			return fileManagerConfig.isCoclustFilePattern.test(this.model.name);
		};

        Item.prototype.isCoclustFormatCompatible = function() {
			return fileManagerConfig.isCoclustFormatPattern.test(this.model.name);
		};

        return Item;
    }]);
})(angular);
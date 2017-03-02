/*var addFilm = function (filmToAdd){
	var film = new Film(filmToAdd);
	film.save(function(err){
		if (err) throw err;
	});
}
var updateFilm = function(filmToUpdate){
	mongoose.modele('film').find(movieToUpdate, function(err, movie){
		var film = new Film(filmToAdd);
		movie = film;
		movie.save(function(err){
			if (err) throw err;
		});
	});
}*/
var id, title;
var showDeleteModal = function (idFilm, titleFilm) {
	id = idFilm;
	title = titleFilm;
	document.getElementById('diag').innerHTML = "Voulez-vous vraiment supprimer le film " + title + " ?";
	document.getElementById('form-delete').style.display = "block";
	document.getElementById('cancel').addEventListener('click', cancelDeleteHandler);
	document.getElementById('confirm').addEventListener('click', confirmDeleteHandler);
	document.getElementById('form-delete').showModal();
};
var confirmDeleteHandler = function () {
	deleteFilm(id);
	document.getElementById('form-delete').style.display = "none";
	document.getElementById('form-delete').close();
	var snackbarContainer = document.querySelector('#demo-toast-example');
	var showToastButton = document.querySelector('#demo-show-toast');
	var data = { message: 'Le film ' + title + ' a bien été supprimé' };
	snackbarContainer.MaterialSnackbar.showSnackbar(data);
	document.getElementById('confirm').removeEventListener('click', confirmDeleteHandler);
}
var cancelDeleteHandler = function () {
	document.getElementById('form-delete').style.display = "none";
	document.getElementById('form-delete').close();
	document.getElementById('cancel').removeEventListener('click', cancelDeleteHandler);
}
var deleteFilm = function (filmToDelete) {
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open("DELETE", '/films/'+filmToDelete, true);
	xmlHttp.send();
	document.getElementById(filmToDelete).remove();
};

/* FORMULAIRE AJOUT */

var showAjoutForm = function () {
	document.getElementById('form-ajout').style.display = "block";
	document.getElementById('cancel-ajout').addEventListener('click', cancelAjout);
	document.getElementById('confirm-ajout').addEventListener('click', confirmAjout);
	document.getElementById('form-ajout').showModal();
};

var confirmAjout = function () {
	//deleteFilm(id);
	document.getElementById("formAddFilm").submit();
	document.getElementById('form-ajout').style.display = "none";
	document.getElementById('form-ajout').close();
	var snackbarContainer = document.querySelector('#demo-toast-example');
	var showToastButton = document.querySelector('#demo-show-toast');
	//var data = {message: 'Le film '+title+' a bien été supprimé'};
	snackbarContainer.MaterialSnackbar.showSnackbar(data);
	document.getElementById('confirm-ajout').removeEventListener('click', confirmAjout);
}

var cancelAjout = function(){
	  document.getElementById('form-ajout').style.display="none";
      document.getElementById('form-ajout').close();
	  document.getElementById('cancel-ajout').removeEventListener('click', cancelAjout);
}

/* FORMULAIRE IMPORT */

var showImportForm = function(){
	document.getElementById('form-import').style.display="block";
	document.getElementById('cancel-import').addEventListener('click', cancelImport);
	document.getElementById('confirm-import').addEventListener('click', confirmImport);
	document.getElementById('form-import').showModal();
};

var confirmImport = function(){
	  document.getElementById("formImportFilm").submit();
	  document.getElementById('form-import').style.display="none";
	  document.getElementById('form-import').close();
	  var snackbarContainer = document.querySelector('#demo-toast-example');
	  var showToastButton = document.querySelector('#demo-show-toast');
      snackbarContainer.MaterialSnackbar.showSnackbar("test");
	  document.getElementById('confirm-import').removeEventListener('click', confirmImport);
}

var cancelImport = function(){
	  document.getElementById('form-import').style.display="none";
      document.getElementById('form-import').close();
	  document.getElementById('cancel-import').removeEventListener('click', cancelImport);
}

/* Formulaire Edition */

var showEditModal = function (film) {
	document.getElementById('form-edit').style.display = "block";
	document.getElementById('inputEditID').value = film._id;
	document.getElementById('inputEditTitle').value = film.title;
	document.getElementById('inputEditAnnee').value = film.year;
	document.getElementById('inputEditGenre').value = film.genre;
	document.getElementById('inputEditNationalite').value = film.country;
	document.getElementById('inputEditSummary').value = film.summary;
	document.getElementById('inputEditDNom').value = film.director.last_name;
	document.getElementById('inputEditDPrenom').value = film.director.first_name;
	document.getElementById('inputEditDDdn').value = film.director.birth_date;

	var acteurs = film.actors;
	var acteursString = "";

	acteurs.forEach(function (acteur) {
		acteursString += acteur.first_name + " " + acteur.last_name + ";";
	}, this);

	acteursString = acteursString.slice(0, -1);


	document.getElementById('inputEditActorsList').value = acteursString;

	var dialogInputs = document.querySelectorAll('.dialog-inputs');
	for (var i = 0, l = dialogInputs.length; i < l; i++) {
		dialogInputs[i].MaterialTextfield.checkDirty();
	}

	document.getElementById('cancel-edit').addEventListener('click', cancelEdit);
	document.getElementById('confirm-edit').addEventListener('click', confirmEdit);
	document.getElementById('form-edit').showModal();
};

var confirmEdit = function () {
	 document.getElementById("formEditFilm").submit();
	 document.getElementById('form-edit').style.display="none";
	 document.getElementById('form-edit').close();
	 document.getElementById('confirm-edit').removeEventListener('click', confirmAjout);
}
var cancelEdit = function () {
	document.getElementById('form-edit').style.display = "none";
	document.getElementById('form-edit').close();
	document.getElementById('cancel-edit').removeEventListener('click', cancelEdit);
}
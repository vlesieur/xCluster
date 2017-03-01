var express = require('express'),
    router = express.Router(),
    mongoose = require('mongoose'),
    bodyParser = require('body-parser'),
    methodOverride = require('method-override'),
    fs = require("fs"),
    path = require('path');

router.use(bodyParser.urlencoded({ extended: true })) 
router.use(methodOverride(function (req, res) {
    if (req.body && typeof req.body === 'object' && '_method' in req.body) {
        var method = req.body._method
        delete req.body._method
        return method
    }
}))

router.route('/')
    .get(function (req, res, next) {
        mongoose.model('film').find({}, function (err, films) {
            if (err) {
                throw err;
            } else {
                res.format({
			html: function () {
                        res.render('films', {
                            tagline: 'All my films',
                            "films": films
                        });
                    },
                    json: function () {
                        res.json(films);
                    }
                });
            }
        });
    })
    .post(function (req, res) {
        var _id;
        var title = req.body.title;
        var year = req.body.year;
        var genre = req.body.genre;
        var summary = req.body.resume;
        var country = req.body.nationalite;
        var director = {
            last_name: req.body.directorLastname,
            first_name: req.body.directorFirstname,
            birth_date: req.body.directorBirth_date,
        };
        var actorsString = req.body.actorsList;
        var acteurs = actorsString.split(";");
        var actors = [];
        var temp;
        acteurs.forEach(function (acteur) {
            temp = acteur.split(" ");
            actors.push({ last_name: temp[1], first_name: temp[0] });
        }, this);

        var movie = {   
            "title": req.body.title,
            "year": req.body.year,
            "genre": req.body.genre,
            "summary": req.body.resume,
            "country": req.body.nationalite,
            "director": 	{
                "last_name": req.body.directorLastname,
                "first_name": req.body.directorFirstname,
                "birth_date": req.body.directorBirth_date	
                },
            "actors": actors
        };
   
 
        insertFilm(movie, res, 0, true);

    });

function insertFilm(movie, res, cpt, isLast){
        var title = movie["title"];
        var year = movie["year"];
        var genre = movie["genre"];
        var summary = movie["summary"];
        var country = movie["country"];

        var director = {
            last_name: movie["director"]["last_name"],
            first_name: movie["director"]["first_name"],
            birth_date: movie["director"]["birth_date"]
        };

        var acteurs = movie["actors"];
        var actors = [];
         acteurs.forEach(function (acteur) {
            actors.push({ last_name: acteur["last_name"], first_name: acteur["first_name"] });
        }, this);

        mongoose.model('film').find({}, function (err, films) {
            if (err) {
                throw err;
            } else {
                films.sort(compareInteger);
                var movie_id = films[films.length-1]._id;
                console.log(movie_id);
                var id = parseInt(movie_id.split(":")[1])+1;
                id = id + cpt;
                console.log(id);
                var _id = "movie:" + id;
                mongoose.model('film').create({
                    _id: _id,
                    title: title,
                    year: year,
                    genre: genre,
                    summary: summary,
                    country: country,
                    director: director,
                    actors: actors
                }, function (err, film) {
                    if (err) {
                        throw err;
                    } else{
                        console.log('POST creating new film: ' + film);
                        if(isLast){
                            res.format({
                                html: function () {
                                    res.location("films");
                                    res.redirect("/films");
                                },
                                json: function () {
                                    res.json(film);
                                }
                            });    
                        }
                    }
                });
            }
        });
}
router.route('/search')
	.post(function (req, res) {
        var search = new Object();
		if(req.body.options == "year") {
			search["$where"] = "function() { return this.year.toString().match(/"+req.body.rechercher+"/) != null; }";
		} else {
			search[req.body.options] = new RegExp('.*'+req.body.rechercher+'.*','i');
		}
		console.log(search);
        mongoose.model('film').find(search, function (err, films) {
            if (err) {
                throw err;
            } else {
                res.format({
                    html: function () {
                        res.render('films', {
                            tagline: 'All my films',
                            "films": films
                        });
                    },
                    json: function () {
                        res.json(films);
                    }
                });
            }
        });
    });
router.route('/:id')
    .delete(function (req, res) {
        mongoose.model('film').findById(req.params.id, function (err, film) {
            if (err) {
                throw err;
            } else {
                film.remove(function (err) {
                    if (err) throw err;
                });
                res.send('OK');
            }
        });
    });
router.route('/import')
        .post(function (req, res) {
            var uploadFile = req.body.uploadFile;
            console.log("\n *START* \n");
            var content = fs.readFileSync(uploadFile);
            var aMovies = JSON.parse(content);
            for(var i=0;i<aMovies.length-1;++i){
                console.log("\n" + i);
                console.log("Output Content : \n"+ aMovies[i]["title"].toString()); 
                insertFilm(aMovies[i], res, i,false);
            }
            insertFilm(aMovies[aMovies.length-1], res, aMovies.length-1, true);
            console.log("\n *EXIT* \n");
        });

function compareInteger(a,b) {              
  if (parseInt(a._id.split(":")[1]) < parseInt(b._id.split(":")[1]))
    return -1;
  if (parseInt(a._id.split(":")[1]) > parseInt(b._id.split(":")[1]))
    return 1;
  return 0;
}

router.route('/update')
    .post(function (req, res) {
        var _id = req.body._id;
        var title = req.body.title;
        var year = req.body.year;
        var genre = req.body.genre;
        var summary = req.body.resume;
        var country = req.body.nationalite;

        var director = {
            last_name: req.body.directorLastname,
            first_name: req.body.directorFirstname,
            birth_date: req.body.directorBirth_date,
        };

        var actorsString = req.body.actorsList;
        var acteurs = actorsString.split(";");
        var actors = [];
        var temp;
        acteurs.forEach(function (acteur) {
            temp = acteur.split(" ");
            actors.push({ last_name: temp[1], first_name: temp[0] });
        }, this);
        mongoose.model('film').find({}, function (err, films) {
            if (err) {
                console.log(err);
                res.send("There was a problem updating the information to the database.");
            } else {
                mongoose.model('film').update({
                    _id: _id
                },{$set : {
                    title: title,
                    year: year,
                    genre: genre,
                    summary: summary,
                    country: country,
                    director: director,
                    actors: actors
                }}, function (err, film) {
                    if (err) {
                        console.log(err);
                        res.send("There was a problem updating the information to the database.");
                    } else {
                        console.log('PATCH updating new film: ' + film);
                        res.format({
                            html: function () {
                                res.location("films");
                                res.redirect("/films");
                            },
                            json: function () {
                                res.json(film);
                            }
                        });
                    }
                });
            }
        });
    });
module.exports = router;

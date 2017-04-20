var express = require('express'),
    path = require('path'),
    favicon = require('serve-favicon'),
    logger = require('morgan'),
    cookieParser = require('cookie-parser'),
    bodyParser = require('body-parser');


var routes = require('./routes/index');

var app = express();

var morgan = require('morgan');
var mongoose = require('mongoose');
var passport = require('passport');
var config = require('./config/database'); // get db config file
var User = require('./model/users'); // get the mongoose model
var jwt = require('jwt-simple');

// get our request parameters
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// log to console
app.use(morgan('dev'));

// Use the passport package in our application
app.use(passport.initialize());

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.listen(3000, function () {
    console.log('API listening on port 3000!');
});

app.all("/*", function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Cache-Control, Pragma, Origin, Authorization, Content-Type, X-Requested-With");
    res.header("Access-Control-Allow-Methods", "GET, PUT, POST");
    return next();
});

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', routes);

/* app.use(function(req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});*/

if (app.get('env') === 'development') {
    app.use(function (err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

app.use(function (err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});

/* MONGO */

// connect to database
mongoose.connect(config.database, function (error, db) {
    if (error) {
        console.log("Erreur de connexion à la base xclusterdb");
    } else {
        console.log("Connecté à la base de données 'xclusterdb'");
    }
});

// pass passport for configuration
require('./config/passport')(passport);

// bundle our routes
var apiRoutes = express.Router();

// create a new user account (POST http://localhost:8080/api/signup)
apiRoutes.post('/signup', function (req, res) {
    if (!req.body.login || !req.body.password || !req.body.mail) {
        res.json({ success: false, msg: 'Veuiller saisir votre nom d\'utilisateur et votre mot de passe.' });
    } else {
        var newUser = new User({
            login: req.body.login,
            password: req.body.password,
            mail: req.body.mail
        });

        // save the user
        newUser.save(function (err) {
            if (err) {
                console.log(err);
                return res.json({ success: false, msg: 'Utilisateur déjà existant.' });
            }
            res.json({ success: true, msg: 'Compte enregistré !' });
        });
    }
});

// route to authenticate a user (POST http://localhost:8080/api/authenticate)
apiRoutes.post('/authenticate', function (req, res) {
    var mail = req.body.mail;
    console.log(mail);
    User.findOne({
        mail: req.body.mail
    }, function (err, user) {
        if (err) {
            throw err;
        }

        if (!user) {
            res.send({ success: false, msg: 'Echec de l\'authentification. Utilisateur non trouvé.' });
        } else {
            // check if password matches
            user.comparePassword(req.body.password, function (err, isMatch) {
                if (isMatch && !err) {
                    // if user is found and password is right create a token
                    var token = jwt.encode(user, config.secret);
                    // return the information including token as JSON
                    res.json({ success: true, token: 'JWT ' + token });
                } else {
                    res.send({ success: false, msg: 'Echec de l\'authentification. Adresse email ou mot de passe invalide.' });
                }
            });
        }
    });
});

// route to authenticate a user (POST http://localhost:8080/api/authenticate)
// ...

// route to a restricted info (GET http://localhost:8080/api/memberinfo)
apiRoutes.get('/authorize', passport.authenticate('jwt', { session: false }), function (req, res) {
    var token = getToken(req.headers);
    if (token) {
        var decoded = jwt.decode(token, config.secret);
        console.log(decoded);
        User.findOne({
            login: decoded.login
        }, function (err, user) {
            if (err) throw err;

            if (!user) {
                return res.status(403).send({ success: false, msg: 'Echec d\'authentification. Utilisateur non trouvé.' });
            } else {
                res.json({ success: true, msg: 'Utilisateur ' + user.login + ' autorisé !' });
            }
        });
    } else {
        return res.status(403).send({ success: false, msg: 'Token non fourni.' });
    }
});

getToken = function (headers) {
    if (headers && headers.authorization) {
        var parted = headers.authorization.split(' ');
        if (parted.length === 2) {
            return parted[1];
        } else {
            return null;
        }
    } else {
        return null;
    }
};

// connect the api routes under /api/*
app.use('/api', apiRoutes);

module.exports = app;

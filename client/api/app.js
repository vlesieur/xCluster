var express = require('express'),
    path = require('path'),
    favicon = require('serve-favicon'),
    logger = require('morgan'),
    cookieParser = require('cookie-parser'),
    bodyParser = require('body-parser');

//var routes = require('./routes/index');
var routes = express.Router();

const zerorpc = require('zerorpc');
const uri = "tcp://127.0.0.1:4242";

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

var callbackFunction = function (err, result, start) {
    const end = new Date() - start;
    if (err) {
        console.log('ERREUR: ', err)
        return result;
    }
    if (typeof result == 'string') {
        console.log('Execution en: ' + end + " ms" + "\r\nresultat: " + result + "\n\n")
        return result;
    } else {
        console.log('Execution en: ' + end + " ms" + "\r\nresultat: " + result[0] + "\n\n" + result[1] + "\n\n" + result[2]);
        return result;
    }
};

var createClient = function () {
    var client = new zerorpc.Client({
        timeout: 360,
        heartbeatInterval: 360000
    });
    return client;
};

var connectClient = function (client) {
    console.log("Connexion au RPC avec ", uri);
    client.connect(uri);
    return client;
};

var callCoclust = function (client, req, res, fn) {
    const start = new Date();
    var response = "";
    client.invoke(fn, req.body.path, req.body.name, req.body.n_clusters, req.body.init, req.body.max_iter, req.body.n_init, req.body.random_state, req.body.tol, req.body.dict, req.body.label_matrix, req.body.n_terms,
        function (error, result, more) {
            response = callbackFunction(error, result, start);
            if(response) {
                res.json({ row: response[0], column: response[1], img: response[2], topTermImg: response[3] });
            } else {
                res.json({ row: 'Erreur dans le traitement de la demande...', column: error, img: 'Visualisation indisponible' });
            }
        });
};

var callCoclustInfo = function (client, req, res) {
    const start = new Date();
    var response = "";
    client.invoke("coclustInfo", req.body.path, req.body.name, req.body.n_row_clusters, req.body.n_col_clusters, req.body.init, req.body.max_iter, req.body.n_init, req.body.tol, req.body.random_state, req.body.dict, req.body.label_matrix, req.body.n_terms,
        function (error, result, more) {
            response = callbackFunction(error, result, start);
            if (response) {
                res.json({ row: response[0], column: response[1], img: response[2], topTermImg: response[3] });
            }
            else {
                res.json({ row: 'Erreur dans le traitement de la demande...', column: error, img: 'Visualisation indisponible' });
            }
        });
};

var callCreateFolder = function (client, login, res) {
    const start = new Date();
    var response = "";
    client.invoke("createUserDirectory", login,
        function (error, result, more) {
            response = callbackFunction(error, result, start);
            if (response) {
                res.json({ success: true, msg: 'Compte enregistré !' });
            } else {
                res.json({ success: false, msg: 'Impossible de créer le repertoire !' })
            }
        });
};

routes.post('/mod', function (req, res) {
    var isAuthorized = checkAuthorize(req, res);
    console.log("isAuthorized value : " + isAuthorized);
    if (isAuthorized) {
        console.log("request : " + req);
        var client = createClient();
        client = connectClient(client);
        callCoclust(client, req, res, "coclustMod");
    } else {
        res.status(403).send({ success: false, msg: 'Non autorisé !' });
    }
});

routes.post('/spec', function (req, res) {
    var isAuthorized = checkAuthorize(req, res);
    console.log("isAuthorized value : " + isAuthorized);
    if (isAuthorized) {
        console.log(req);
        var client = createClient();
        client = connectClient(client);
        callCoclust(client, req, res, "coclustSpecMod");
    } else {
        res.status(403).send({ success: false, msg: 'Non autorisé !' });
    }
});

routes.post('/info', function (req, res) {
    var isAuthorized = checkAuthorize(req, res);
    console.log("isAuthorized value : " + isAuthorized);
    if (isAuthorized) {
        console.log(req);
        var client = createClient();
        client = connectClient(client);
        callCoclustInfo(client, req, res);
    } else {
        res.status(403).send({ success: false, msg: 'Non autorisé !' });
    }
});

app.use('/coclust', routes);

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
var options = { db: { native_parser: true }, server: { autoReconnect: false, socketOptions: { keepAlive: 120 } }, replset: { socketOptions: { keepAlive: 120 } } };
var mongoDB = mongoose.connect(config.database, options).connection;

// CONNECTION EVENTS
mongoDB.once('open', function () {
    console.log("mongodb connection open");
});

// When successfully connected
mongoDB.on('connected', function () {
    console.log('Mongoose default connection open to ' + config.database);
});

// If the connection throws an error
mongoDB.on('error', function (err) {
    console.log('Mongoose default connection error: ' + err.message);
});

// When the connection is disconnected
mongoDB.on('disconnected', function () {
    console.log('Mongoose default connection disconnected');
});

// If the Node process ends, close the Mongoose connection 
process.on('SIGINT', function () {
    mongoose.connection.close(function () {
        console.log('Mongoose default connection disconnected through app termination');
        process.exit(0);
    });
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
            var client = createClient();
            client = connectClient(client);
            callCreateFolder(client, req.body.login, res);
        });
    }
});

// route to authenticate a user (POST http://localhost:8080/api/authenticate)
apiRoutes.post('/authenticate', function (req, res) {
    var login = req.body.login;
    User.findOne({
        login: req.body.login
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
                    res.send({ success: false, msg: 'Echec de l\'authentification. Login ou mot de passe invalide.' });
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
        User.findOne({
            login: decoded.login
        }, function (err, user) {
            if (err) throw err;

            if (!user) {
                console.log('Echec d\'authentification. Utilisateur non trouvé.');
                return res.status(403).send({ success: false, msg: 'Echec d\'authentification. Utilisateur non trouvé.' });
            } else {
                console.log('Utilisateur ' + user.login + ' autorisé !');
                res.json({ success: true, msg: 'Utilisateur ' + user.login + ' autorisé !' });
            }
        });
    } else {
        console.log('Token non fourni.');
        return res.status(403).send({ success: false, msg: 'Token non fourni.' });
    }
});

checkAuthorize = function (req, res) {
    var token = getToken(req.headers);
    if (token) {
        var decoded = jwt.decode(token, config.secret);
        return User.findOne({
            login: decoded.login
        }, function (err, user) {

            if (err) {
                console.log(err);
                return false;
            }

            if (!user) {
                console.log("Echec d\'authentification. Utilisateur non trouvé.");
                return false;
            } else {
                console.log("Utilisateur " + user.login + " autorisé !");
                return true;
            }
        });
    } else {
        console.log("Token non fourni.");
        return false;
    }
}

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

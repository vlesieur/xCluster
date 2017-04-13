var express = require('express');
var router = express.Router();

const zerorpc = require('zerorpc');
const uri = "tcp://127.0.0.1:4242";

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
  client.invoke(fn, "user", req.body.path, req.body.name, req.body.n_clusters, req.body.init, req.body.max_iter, req.body.n_init, req.body.random_state, req.body.tol, 
  function (error, result, more) {
	response = callbackFunction(error, result, start);
	res.json({ row: response[0], column: response[1], img: response[2]});
  });
};

var callCoclustInfo = function (client, req, res, fn) {
  const start = new Date();
  var response = "";
  client.invoke(fn, "user", req.body.path, req.body.name, req.body.n_row_clusters, req.body.n_col_clusters, req.body.init, req.body.max_iter, req.body.n_init, req.body.tol, req.body.random_state,  
  function (error, result, more) {
	response = callbackFunction(error, result, start);
	res.json({ row: response[0], column: response[1], img: response[2]});
  });
};

/* GET home page. */
router.post('/', function (req, res) {
  console.log(req);
  var client = createClient();
  client = connectClient(client);
  callCoclust(client, req, res, "coclustMod");
});

router.post('/spec', function (req, res) {
  console.log(req);
  var client = createClient();
  client = connectClient(client);
  callCoclust(client, req, res, "coclustSpecMod");
});

router.post('/info', function (req, res) {
  console.log(req);
  var client = createClient();
  client = connectClient(client);
  callCoclustInfo(client, req, res, "coclustInfo");
});

module.exports = router;

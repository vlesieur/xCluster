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

var callCoclust = function (client, toSend) {
  const start = new Date();
  var response = "";
  client.invoke("coclustMod", "user", "cstr.mat", function (error, res, more) {
	response = callbackFunction(error, res, start);
	toSend.json({ row: response[0], column: response[1], img: response[2]});
  });
};

/* GET home page. */
router.get('/', function (req, res, next) {
  var client = createClient();
  client = connectClient(client);
  callCoclust(client, res);
});

module.exports = router;

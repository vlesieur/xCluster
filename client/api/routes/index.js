var express = require('express');
var router = express.Router();

const zerorpc = require('zerorpc');
const uri = "tcp://127.0.0.1:4242";

var result = "";
const setGlobalResult = function(str){
  result=str;
}

const callbackFunction = function (err, result, start) {
  const end = new Date() - start;
  if (err) {
    console.log('ERREUR: ', err)
    return err;
  }
  if (typeof result == 'string') {
    console.log('Execution en: ' + end + " ms" + "\r\nresultat: " + result + "\n\n")
    return result;
  } else {
    console.log('Execution en: ' + end + " ms" + "\r\nresultat: " + result[0] + "\n\n" + result[1] + "\n\n" + result[2]);
    return result;
  }
};

const createClient = function () {
  var client = new zerorpc.Client({
    timeout: 360,
    heartbeatInterval: 360000
  });
  return client;
};

const connectClient = function (client) {
  console.log("Connexion au RPC avec ", uri);
  client.connect(uri);
  return client;
};

const callCoclust = function (client) {
  const start = new Date();
  var response ="";
  client.invoke("coclustMod", "user", "cstr.mat", function (error, res, more) {
    response = callbackFunction(error, res, start);
  });
  setTimeout(function () {
    setGlobalResult(response);
    return response;
  }, 2500);
  return response;
};

/* GET home page. */
router.get('/', function (req, res, next) {
  var client = createClient();
  client = connectClient(client);
  callCoclust(client);
  setTimeout(function () {
    res.render('index', { title: result });
  }, 3000);

});

module.exports = router;

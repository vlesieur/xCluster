const zerorpc = require('zerorpc');
const uri = "tcp://127.0.0.1:4242";

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
    var response = "";
    client.invoke("coclustMod", "user", "cstr.mat", function (error, res, more) {
        response = callbackFunction(error, res, start);
    });
    return response;
};

//console.log("Debut des invokes python...");

/*client.invoke("hello", "Classification croisée", function (error, res, more) {
    callbackFunction(error, res, start);
});*/

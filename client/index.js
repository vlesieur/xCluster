const callbackFunction = function(err, result, start) {
    const end = new Date() - start;
    if(err){
        console.log('ERREUR: ',err)
    }
	if (typeof result == 'string') {
		console.log('Execution en: ' + end + " ms" + "\r\nresultat: " + result + "\n\n")
	} else {
		console.log('Execution en: ' + end + " ms" + "\r\nresultat: " + result[0] + "\n\n" + result[1]);
	}
}
const zerorpc = require('zerorpc');
const client = new zerorpc.Client({
        timeout: 360,
        heartbeatInterval: 360000
    });
const uri = "tcp://127.0.0.1:4242";
console.log("Connexion au RPC avec ", uri);
client.connect(uri);
const start = new Date();
console.log("Debut des invokes python...");

client.invoke("hello", "Classification croisée", function(error, res, more) {
        callbackFunction(error, res, start);
});

client.invoke("coclustMod", "user", "cstr.mat", function(error, res, more) {
    callbackFunction(error, res, start);
});
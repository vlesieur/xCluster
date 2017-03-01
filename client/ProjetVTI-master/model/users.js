var mongoose = require('mongoose');  
var userSchema = new mongoose.Schema({  
  _id: String,
  login: String,
  password: String,
  mail : String 
});
mongoose.model('user', userSchema, 'user');






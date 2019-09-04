var express = require('express');
var router = express.Router();
var mongoose = require('mongoose');
var tunnel = require('tunnel-ssh');
const utf8 = require('utf8');
//mongoose.connect('localhost:27017/test');
//mongoose.connect('localhost:27017/tutorial');

var config = {
    username:'root',
    host:'45.119.82.50',
    agent : process.env.SSH_AUTH_SOCK,
    //privateKey:require('fs').readFileSync('/Users/myusername/.ssh/id_rsa'),
    port:22,
    dstPort:27017,
    password:'RgQpda7T58WSL@Vj'
};

var server = tunnel(config, function (error, server) {
    if(error){
        console.log("SSH connection error: " + error);
    }
    mongoose.connect('localhost:27017/cool_db');

    var dbs = mongoose.connection;
    dbs.on('error', console.error.bind(console, 'DB connection error:'));
    dbs.once('open', function() {
        // we're connected!
        console.log("DB connection successful");
    });
});

var Schema = mongoose.Schema;

var posts = new Schema({
  title: {type: String, required: true},
  content: String,
  author: String
}, {collection: 'posts'});

var dbSchema = new Schema({}, {strict: false});
var db = mongoose.model('db', dbSchema, 'posts');

var Posts = mongoose.model('Posts', posts);

/* GET home page. */
router.get('/map', function(req, res, next) {
  //res.render('index');
  db.find()
      .then(function(doc) {
        res.render('test', {items: doc});
      });
});

/* GET chart page. */
router.get('/chart', function(req, res, next) {
  //res.render('index');
  res.render('chart');
});

/* GET data table page. */
router.get('/', function(req, res, next) {
  db.find()
      .then(function(doc) {
        //console.log(doc.toString());
        res.render('datatable', {items: doc });
      });
  //res.render('datatable', {tests: dataSet});
});

router.get('/get-data', function(req, res, next) {
  UserData.find()
      .then(function(doc) {
        res.render('index', {items: doc});
      });
});

router.post('/insert', function(req, res, next) {
  var item = {
    title: req.body.title,
    content: req.body.content,
    author: req.body.author
  };

  var data = new UserData(item);
  data.save();

  res.redirect('/');
});

router.post('/update', function(req, res, next) {
  var id = req.body.id;

  UserData.findById(id, function(err, doc) {
    if (err) {
      console.error('error, no entry found');
    }
    doc.title = req.body.title;
    doc.content = req.body.content;
    doc.author = req.body.author;
    doc.save();
  })
  res.redirect('/');
});

router.post('/delete', function(req, res, next) {
  var id = req.body.id;
  UserData.findByIdAndRemove(id).exec();
  res.redirect('/');
});

module.exports = router;

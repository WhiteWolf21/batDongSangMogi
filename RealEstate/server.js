var express = require("express");
var path = require("path");
var bodyParser = require("body-parser");
var mongo = require("mongoose");

var host = "localhost";
var mongoDBPort = "27017";
var database = "real_estate";
var databaseUrl = "mongodb://"+host+":"+mongoDBPort+"/"+database
mongo.connect(
    databaseUrl, 
    { useNewUrlParser: true }, 
    function(err, res) {
        if(err) { console.log(err); }
        else { console.log("Connected to ", database, " + ", res); }
});

var app = express();
app.use(bodyParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:true}))

app.use(function (req, res, next) {
    res.setHeader("Access-Control-Allow-Origin", "http://localhost:4200");  // ANGULAR localhost
    res.setHeader("Access-Control-Allow-Methods", "GET,POST,PUT,OPTIONS,PATCH,DELETE");
    res.setHeader("Access-Control-Allow-Headers", "X-Requested-With,Content-Type");
    res.setHeader("Access-Control-Allow-Credentials", true);
    next();
});

var mongoSchema = mongo.Schema;

//USER
var userSchema = new mongoSchema({}, { versionKey: false});

var model = mongo.model("user_posts", userSchema, "user_posts");


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////                      USER POSTS
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var itemsPerPage = 10;
var buyCount;
var sellCount;
var countLimit;
model.find({title: {$regex: "mua",$options:"i"}})
    .countDocuments()
    .exec(function(err,count) {
        if (!err) {
            buyCount = count;
        }
    });
model.find({title: {$regex: "b.{1}n",$options:"i"}})
    .countDocuments()
    .exec(function(err,count) {
        if (!err) {
            sellCount = count;
            countLimit = buyCount <= sellCount ? buyCount : sellCount;
        }
    });
// Buy Posts    
app.get("/api/get-user/buy/:pageNum", function (req, res) {
    model.find({title: new RegExp("mua", "i")})
        .skip(+req.params.pageNum > 0 ? (+req.params.pageNum-1)*itemsPerPage : 0)
        .limit(itemsPerPage)
        .exec(function(err, data) {
            if (err) { res.send(err); }
            else {
                var currentPage = req.params.pageNum;
                var userBuyPosts = data;
                res.send({userBuyPosts,currentPage,countLimit});
            }
        });
});

// Sell Posts
app.get("/api/get-user/sell/:pageNum", function (req, res) {
    model.find({title: {$regex: "b.{1}n",$options:"i"}})
        .skip(+req.params.pageNum > 0 ? (+req.params.pageNum-1)*itemsPerPage : 0)
        .limit(itemsPerPage)
        .exec(function(err, data) {
            if (err) { res.send(err); }
            else {
                var currentPage = req.params.pageNum;
                var userSellPosts = data;
                res.send({userSellPosts,currentPage,countLimit});
            }
        });
});

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

app.listen(8080, function () {
    console.log("Server is running on port 8080...");
});

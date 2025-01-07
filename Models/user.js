const mongoose = require("mongoose")

const userSchema = new mongoose.Schema({
    // name : String;
    email:String,
    password:String,
})

const users = mongoose.model("UserDb",userSchema)
module.exports = users
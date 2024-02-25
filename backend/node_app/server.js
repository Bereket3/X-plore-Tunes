const express = require("express");
const fs = require("fs");
const path = require('path')
const mysql = require('mysql2')
const crypto = require('crypto')


const app = express();


var connection = mysql.createPool({
    database: process.env.NAME,
    user: process.env.USER,
    password: process.env.PASSWORD,
    host: process.env.HOST,
    port: process.env.POST,
});



app.get("/video/:audio", function (req, res) {
    /**
     * end point to send all music files 
     * It will take in a file name and return the music file by small chunk of size 1MB
     * 
     * 
     * Will have a header named Range
     * These parameter spacify the start of the music file
     */
    
    const range = req.headers.range;
    const param = req.params.audio;
    const isLogdIn = handelAuth(req.headers);


    if(!isLogdIn){
        return res.status(401).send("Invalid Token");
    }

    if (!range) {
        res.status(400).send("Requires Range header");
    }

    const videoPath = path.resolve(__dirname, "../", `media/music_files/audio/${param}`);

    if(!fs.existsSync(videoPath)) {
        res.status(404).send("The file you are looking for doesn't exist in the database");
    }

    const videoSize = fs.statSync(videoPath).size;
    const CHUNK_SIZE = 1024*1024;

    const start = Number(range.replace(/\D/g, ""));
    const end = Math.min(start + CHUNK_SIZE, videoSize - 1);
    
    const contentLength = end - start + 1;
    const headers = {
        "Content-Range": `bytes ${start}-${end}/${videoSize}`,
        "Accept-Ranges": "bytes",
        "Content-Length": contentLength,
        "Content-Type": "audio/mp3",
    };
    res.writeHead(206, headers);
    const videoStream = fs.createReadStream(videoPath, { start, end });
    videoStream.pipe(res);
    
});


function handelAuth (headers) {
    /**
     * 
     * extract the header and check its token
     */
    const Bearer = headers.authorization;
    if (!Bearer) {
        return 'Authentication credentials were not provided.';
    }
    token = Bearer.split(' ')
    if(token.length < 2){
        return 'Invalid token';
    }
    
    const queryObject = connection.query('SELECT * FROM oauth2_provider_accesstoken WHERE `token` = ?', 
        token[1], 
        function (err, result, fields) {
            if (err) {
                return false;
            };
            return result;
    });
    return queryObject;
    
}

app.listen(8000, function () {
    console.log("Listening on port 8000!");
});
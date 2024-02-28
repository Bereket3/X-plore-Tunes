const express = require("express");
const fs = require("fs");
const path = require('path')


const app = express();


app.get("/video/:audio", async function (req, res) {
    /**
     * End point to send all music files
     * It will take in a file name and return the music file by small chunk of size 1MB
     * 
     * 
     * Will have a header named Range
     * These parameter spacify the start of the music file
     */
    
    const range = req.headers.range;
    const param = req.params.audio;
    const Bearer = req.headers.authorization;

    if (!Bearer) {
        return 'Authentication credentials were not provided.';
    }

    token = Bearer.split(' ');

    if(token.length < 2){
        return 'Invalid token';
    }

    const isLogdIn = await handelAuth(token);

    if(!isLogdIn){
        return res.status(401).send("Invalid Token");
    }

    if (!range) {
        return res.status(400).send("Requires Range header");
    }

    const videoPath = path.resolve(__dirname, "../", `media/music_files/audio/${param}`);

    if(!fs.existsSync(videoPath)) {
        return res.status(404).send({"detail":"The file you are looking for doesn't exist in the database"});
    }

    const videoSize = fs.statSync(videoPath).size;
    const CHUNK_SIZE = 1024*1024;
    const _splited = range.replace(/\D/g, ' ').split();
    const start = Number(_splited[0]);
    const end = Math.min(start + CHUNK_SIZE, videoSize - 1);

    if(start >= videoSize){
        return res.status(404).send({"detail":"Out of range"});
    }
    
    const contentLength = end - start + 1;
    const headers = {
        "Content-Range": `bytes ${start}-${end}/${videoSize}`,
        "Accept-Ranges": "bytes",
        "Content-Length": contentLength,
        "Content-Type": "audio/mp3",
    };

    res.writeHead(206, headers);
    const videoStream = fs.createReadStream(videoPath, {start, end });
    videoStream.pipe(res);
    
});


async function handelAuth (token) {
    /**
     * 
     * extract the header and check if the token is valid and return true if it is
     * and false else wise
     * 
     * @param token: string
     * 
     * @returns boolean
     */

    const BASE_URL = 'http://localhost:9100/api_root/auth/validate/';

    const Options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            'token': token[1],
        })
    };

    const message = await fetch(BASE_URL, Options)

    .then((response) => {
        return response.json()
    })
    .catch(err=> {
        console.log('err', err)
    })
    
    if(message['message'] == true){
        return true;
    }
    return false;
}

app.listen(8000, function () {
    console.log("Listening on port 8000!");
});
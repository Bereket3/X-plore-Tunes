import React from "react";

import 'react-h5-audio-player/lib/styles.css';


async function loadmusic() {
    const BASE_URL = 'http://localhost:8000/video/Diplo__HUGEL_Stay_High_feat_Julia_Church_MAKJ_Remix.mp3';


    const options = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            'range':'bytes=1000000-',
        },
    }
    const audioContext = new window.AudioContext();
    const response = await fetch(BASE_URL, options);
    const reader = await response.arrayBuffer();
    const source = await audioContext.createBufferSource();
    source.connect(audioContext.destination);
    audioContext.decodeAudioData(await reader)

    // const pump = () => {
    //     reader.read().then(({ value, done }) => {
    //         if (value) {
    //             audioContext.decodeAudioData(value.buffer);
    //         }
    //         if (!done) pump();
    //     })
    // }
    // await pump()
    return source
} 

class Audio extends React.Component {
    
render(){ 
	return( 
    <div className='card'>
        <div className=' card-header'>music player</div>
        <div className='card-body'>
        <button className="btn btn-primary" onClick={
            async function () {
                const loaded = await loadmusic();
                loaded.start()
            }}
  >play</button>
        </div>
    </div>
	)} 
}
  

export default Audio;
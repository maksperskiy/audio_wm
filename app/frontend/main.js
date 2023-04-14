let AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx;

// Stereo

function init() {
    audioCtx = new AudioContext();
}

let result;

const getButton = document.querySelector('#get-sound');
const playOrigButton = document.querySelector('#play-original');
const palyInjectedButton = document.querySelector('#play-injected');


let message = document.getElementById('message');
let eMessage = document.getElementById('extracted-message');
let snRatio = document.getElementById('sound-noise-ratio');
let sRatio = document.getElementById('success-ratio');


const play = (sound, rate) => {
    let channels = 1;
    
    if (typeof sound[0] !== 'number') {
        channels = 2;
    }
    
    let myArrayBuffer = audioCtx.createBuffer(channels, sound.length, rate);

    for (let channel = 0; channel < channels; channel++) {
        let nowBuffering = myArrayBuffer.getChannelData(channel);
        for (let i = 0; i < sound.length; i++) {
            let value;
            if (typeof sound[i] === 'number') {
                value = sound[i];
            } else {
                value = sound[i][channel];
            }
            nowBuffering[i] = value / 32767.0;
        }
    }

    let source = audioCtx.createBufferSource();
    source.buffer = myArrayBuffer;
    source.connect(audioCtx.destination);
    
    source.start();

    source.onended = () => {
        console.log('Sound finished');
    }
}

getButton.onclick = function () {
    if (!audioCtx) {
        init();
    }

    let label = "Music";
    fetch("http://localhost:8081/api/v1/audio?label=" + label).then(function (response) {
        return response.json();
    }).then(function (data) {
        console.log(data);
        result = data;
        message.innerHTML = data.message;
        eMessage.innerHTML = data.extractedMessage;
        snRatio.innerHTML = data.soundNoiseRatio;
        sRatio.innerHTML = data.successRatio;
    }).catch(function (err) {
        console.log('Fetch Error :-S', err);
    });
}

playOrigButton.onclick = function () {
    if (!result) {
        return;
    }
    play(result.soundArray, result.samplerate);
}

palyInjectedButton.onclick = function () {
    if (!result) {
        return;
    }

    play(result.injectedSoundArray, result.samplerate);
}
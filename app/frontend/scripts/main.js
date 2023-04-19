let backend_url = "http://localhost:8081"

let AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx;


function init() {
    audioCtx = new AudioContext();
}

let result;

const getButton = document.querySelector('#get-sound');
const playOrigButton = document.querySelector('#play-original');
const palyInjectedButton = document.querySelector('#play-injected');
const estimateButton = document.querySelector('#estimate');

const getButtonSpinner = document.querySelector('#get-sound-spinner');


let messageEl = document.getElementById('message');
let snRatieEl = document.getElementById('sound-noise-ratio');

let resetInputEl = document.getElementById('reset-input');
let resetButtonEl = document.getElementById("reset-button");
let resetModalButtonEl = document.getElementById("reset-modal-button");


let message;
let eMessage;
let snRatio;
let sRatio;

let listened = 0;

let label;

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
    estimateButton.disabled = true;
    playOrigButton.disabled = true;
    palyInjectedButton.disabled = true;
    getButton.disabled = true;
    getButtonSpinner.style.display = 'inline-block';
    listened = 0;

    fetch(backend_url + "/api/v1/audio/?label=" + label).then(function (response) {
        return response.json();
    }).then(function (data) {
        console.log(data);
        result = data;

        messageEl.innerHTML = data.message.toString() + (data.successRatio ? " = " : " ≠ ") + data.extractedMessage.toString();
        if (data.successRatio) {
            messageEl.className = "badge badge-success badge-pill";
        } else {
            messageEl.className = "badge badge-danger badge-pill";
        }
        snRatieEl.innerHTML = Math.round(data.soundNoiseRatio * 100) / 100;
        message = data.message;
        eMessage = data.extractedMessage;
        snRatio = data.soundNoiseRatio;
        sRatio = data.successRatio;

        playOrigButton.disabled = false;
        palyInjectedButton.disabled = false;

        getButton.disabled = false;
        getButtonSpinner.style.display = 'none';
    }).catch(function (err) {
        console.log('Fetch Error :-S', err);
        getButton.disabled = false;
        getButtonSpinner.style.display = 'none';
    });
}

playOrigButton.onclick = function () {
    if (!result) {
        return;
    }
    play(result.soundArray, result.samplerate);
    listened += 1;
    if (listened == 2) {
        estimateButton.disabled = false;
    }
}

palyInjectedButton.onclick = function () {
    if (!result) {
        return;
    }

    play(result.injectedSoundArray, result.samplerate);
    listened += 1;
    if (listened == 2) {
        estimateButton.disabled = false;
    }
}


estimateButton.onclick = () => {
    let value = document.querySelector('input[name="score"]:checked').value;

    request_body = {
        label: label,
        expertScore: value,
        soundNoiseRatio: snRatio,
        successRatio: sRatio
    }

    fetch(backend_url + "/api/v1/audio/estimate/", {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(request_body)
    })
        .then((response) => {

        });
    estimateButton.disabled = true;
}


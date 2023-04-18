let labelListEl = document.getElementById('labelList');


const changeLabel = () => {
    label = document.getElementById('label').value;
}

document.getElementById("label").addEventListener('change', changeLabel);


fetch(backend_url + "/api/v1/audio/labels/").then(function (response) {
    return response.json();
}).then(function (data) {
    console.log(data);
    data.labels.forEach(label => {
        let option = document.createElement("option");
        option.value = label;
        option.innerText = label;
        labelListEl.appendChild(option);
    });
}).catch(function (err) {
    console.log('Fetch Error :-S', err);
});



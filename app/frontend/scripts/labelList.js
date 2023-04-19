let labelListEl = document.getElementById('labelList');
let labelEl = document.getElementById("label");

const changeLabel = () => {
    label = labelEl.value;
}

labelEl.addEventListener('change', changeLabel);


function success() {
    if (labelEl.value === "") {
        getButton.disabled = true;
        resetModalButtonEl.disabled = true;
        labelEl.classList.add("is-invalid");
    } else {
        getButton.disabled = false;
        resetModalButtonEl.disabled = false;
        labelEl.classList.remove("is-invalid");
    }
}
success();


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



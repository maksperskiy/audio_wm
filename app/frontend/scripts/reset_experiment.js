
function successReset() {
    if (resetInputEl.value !== label) {
        resetButtonEl.disabled = true;
        resetInputEl.classList.add("is-invalid");
    } else {
        resetButtonEl.disabled = false;
        resetInputEl.classList.remove("is-invalid");
    }
}
successReset();

$('#myModal').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
})


resetButtonEl.onclick = () => {
    fetch(backend_url + "/api/v1/audio/reset/?label=" + label).then(function (response) {
        return response.json();
    }).then(function (data) {
        window.location.reload();
    }).catch(function (err) {
        console.log('Fetch Error :-S', err);
    });
}

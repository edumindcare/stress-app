// Upload Image
function uploadImage() {
    let fileInput = document.getElementById("imageUpload");
    let file = fileInput.files[0];

    let formData = new FormData();
    formData.append("image", file);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText = data.emotion;
    });
}

// Webcam
navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    document.getElementById("video").srcObject = stream;
});

function takePhoto() {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    let dataURL = canvas.toDataURL("image/jpeg");

    let formData = new FormData();
    formData.append("image", dataURL);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText = data.emotion;
    });
}

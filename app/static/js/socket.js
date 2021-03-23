var socket = io('http://localhost:5000');

socket.on('connect', function(){
    console.log("Connected...!", socket.connected)
});

const video = document.querySelector("#videoElement");
video.width = 600;
video.height = 400;


if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
        video.srcObject = stream;
        video.play();
    })
    .catch(function (err0r) {
        console.log(err0r)
        console.log("Something went wrong!");
    });
}

const FPS = 22;

setInterval(() => {
    var type = "image/png"
    let canvas = document.getElementById("canvasOutput")
    canvas.width = video.width;
    canvas.height = video.height;

    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    var data = canvas.toDataURL(type);

    data = data.replace('data:' + type + ';base64,', ''); //split off junk
    
    socket.emit('image', data);
}, 10000/FPS);


socket.on('response_back', function(image){
    const image_id = document.getElementById('image');
    image_id.src = image;
});

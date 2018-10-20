
//Define object constants
const player = document.getElementById('player');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const captureButton = document.getElementById('capture');
const constraints = { video: true };
var image;

//Hook into button event to display image to canvas
captureButton.addEventListener('click', () => {
    // Draw the video frame to the canvas.
    context.drawImage(player, 0, 0, canvas.width, canvas.height);
    //Put image data into image
    image = context.getImageData(0, 0, canvas.width, canvas.height);
  });

// Attach the video stream to the video element and autoplay.
navigator.mediaDevices.getUserMedia(constraints)
    .then((stream) => {
      player.srcObject = stream;
    });

/*function postImage () {
    const Http = new XMLHttpRequest();
    const url = "temp";
    Http.open("POST", url);
    Http.send();
}*/
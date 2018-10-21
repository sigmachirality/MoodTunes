//Define object constants
const player = document.getElementById('player');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const captureButton = document.getElementById('buttonPressed');
const constraints = { video: true };
//var image;

function ShowCam() {
    Webcam.set({
        width: 320,
        height: 240,
        image_format: 'png',
        jpeg_quality: 100
    });
    Webcam.attach('#canvas');
}
window.onload = ShowCam;

//Convert from dataURI to blob
function dataURItoBlob(dataURI) {
    // convert base64/URLEncoded data component to raw binary data held in a string
    var byteString;
    if (dataURI.split(',')[0].indexOf('base64') >= 0)
        byteString = atob(dataURI.split(',')[1]);
    else
        byteString = unescape(dataURI.split(',')[1]);

    // separate out the mime component
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

    // write the bytes of the string to a typed array
    var ia = new Uint8Array(byteString.length);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }

    return new Blob([ia], { type: mimeString });
}

//Hook into button event to display image to canvas
captureButton.addEventListener('click', onButtonClicked);

var blob;
function onButtonClicked(event){
    setTimeout(function(){
        Webcam.snap(function(data_uri) {
            var form = document.getElementById('myForm');
            blob = dataURItoBlob(data_uri);
            var formData = new FormData(form);
            formData.append("file", blob);
            var xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST", "/emotion", false);
            xmlhttp.send(formData);
            document.getElementById('emotion').innerHTML = "<button id='visualize' style='background:none!important; border:none!important; '><code>"+xmlhttp.response+"</code></button>";
            document.getElementById('visualize').addEventListener('click', onVizClicked);
        });
    }, 3000);

    setTimeout(function(){
            var userCode =getUrlVars()['code'];
            var form = document.getElementById('myForm');
            var formData = new FormData(form);
            formData.append("file", blob);
            var xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST", "/playlist?code="+userCode, false);
            xmlhttp.send(formData);
            document.getElementById('playlist').innerHTML = "<code><a href='" + xmlhttp.response+"' style='color:#e83e8c; text-decoration:none;'>Link</a></code>";
    }, 6000);
}

function onVizClicked(event){
    var form = document.getElementById('myForm');
    var formData = new FormData(form);
    formData.append("file", blob);
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", "/visualize", false);
    xmlhttp.send(formData);     
    document.write(xmlhttp.responseText);
}


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

function showVideo() {
    document.getElementById("captureVideo").style.display = "block";
    document.getElementById("hide-on-webcam").style.display = "none";
    document.getElementById("buttonPressed").style.display = "none";
    document.getElementById("captureVideo").style.marginTop = "50px";
    document.getElementById("canvas").style.display ="none";
}

//Get html params from url
function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}


/*//Hook into button event to display image to canvas
captureButton.addEventListener('click', () => {
    //Post imageUrl to server
    Webcam.snap(function(data_uri) {
        var form = document.getElementById('myForm');
        var blob = dataURItoBlob(data_uri)
        var formData = new FormData(form);
        formData.append("file", blob);
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST", "/");
        xmlhttp.send(formData);
    });
});*/
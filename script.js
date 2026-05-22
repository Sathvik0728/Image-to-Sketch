const upload =
document.getElementById("upload");

const originalImage =
document.getElementById("originalImage");

const canvas =
document.getElementById("sketchCanvas");

const ctx =
canvas.getContext("2d");

const intensity =
document.getElementById("intensity");

const downloadBtn =
document.getElementById("downloadBtn");

let uploadedImage = null;

// FIXED SIZE

const MAX_WIDTH = 850;

const MAX_HEIGHT = 500;

// CREATE PENCIL SKETCH

function generateSketch(img){

    let width = img.width;

    let height = img.height;

    // SCALE IMAGE

    const ratio =
    Math.min(
        MAX_WIDTH / width,
        MAX_HEIGHT / height
    );

    width *= ratio;

    height *= ratio;

    canvas.width = width;

    canvas.height = height;

    // TEMP CANVAS

    const tempCanvas =
    document.createElement("canvas");

    tempCanvas.width = width;

    tempCanvas.height = height;

    const tempCtx =
    tempCanvas.getContext("2d");

    // DRAW IMAGE

    tempCtx.drawImage(
        img,
        0,
        0,
        width,
        height
    );

    // GET DATA

    let imageData =
    tempCtx.getImageData(
        0,
        0,
        width,
        height
    );

    let data =
    imageData.data;

    // GRAYSCALE

    for(let i = 0; i < data.length; i += 4){

        let gray =
        0.299 * data[i] +
        0.587 * data[i + 1] +
        0.114 * data[i + 2];

        data[i] = gray;
        data[i + 1] = gray;
        data[i + 2] = gray;
    }

    tempCtx.putImageData(imageData, 0, 0);

    // CREATE INVERTED

    const invertCanvas =
    document.createElement("canvas");

    invertCanvas.width = width;

    invertCanvas.height = height;

    const invertCtx =
    invertCanvas.getContext("2d");

    invertCtx.drawImage(tempCanvas, 0, 0);

    let invertData =
    invertCtx.getImageData(
        0,
        0,
        width,
        height
    );

    let pixels =
    invertData.data;

    // INVERT COLORS

    for(let i = 0; i < pixels.length; i += 4){

        pixels[i] = 255 - pixels[i];

        pixels[i + 1] =
        255 - pixels[i + 1];

        pixels[i + 2] =
        255 - pixels[i + 2];
    }

    invertCtx.putImageData(invertData, 0, 0);

    // BLUR INVERTED IMAGE

    ctx.clearRect(0, 0, width, height);

    ctx.filter =
    `blur(${intensity.value}px)`;

    ctx.drawImage(invertCanvas, 0, 0);

    // GET BLURRED DATA

    let blurData =
    ctx.getImageData(
        0,
        0,
        width,
        height
    );

    let blurPixels =
    blurData.data;

    // GET ORIGINAL GRAY DATA

    let grayData =
    tempCtx.getImageData(
        0,
        0,
        width,
        height
    );

    let grayPixels =
    grayData.data;

    // DODGE BLEND

    for(let i = 0; i < grayPixels.length; i += 4){

        let base =
        grayPixels[i];

        let blend =
        blurPixels[i];

        let result =
        Math.min(
            255,
            (base * 256) /
            (255 - blend + 1)
        );

        grayPixels[i] = result;

        grayPixels[i + 1] = result;

        grayPixels[i + 2] = result;
    }

    // FINAL IMAGE

    ctx.filter = "none";

    ctx.putImageData(grayData, 0, 0);
}

// UPLOAD

upload.addEventListener("change", (e)=>{

    const file =
    e.target.files[0];

    if(!file) return;

    const reader =
    new FileReader();

    reader.onload = function(event){

        originalImage.src =
        event.target.result;

        uploadedImage =
        new Image();

        uploadedImage.src =
        event.target.result;

        uploadedImage.onload =
        ()=>{

            generateSketch(uploadedImage);
        };
    };

    reader.readAsDataURL(file);
});

// INTENSITY

intensity.addEventListener("input", ()=>{

    if(uploadedImage){

        generateSketch(uploadedImage);
    }
});

// DOWNLOAD

downloadBtn.addEventListener("click", ()=>{

    const link =
    document.createElement("a");

    link.download =
    "pencil-sketch.png";

    link.href =
    canvas.toDataURL("image/png");

    link.click();
});
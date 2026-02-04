async function setupFaceApi() {
  await faceapi.nets.tinyFaceDetector.loadFromUri("/static/tryonapp/models");
  await faceapi.nets.faceLandmark68Net.loadFromUri("/static/tryonapp/models");
  console.log("Models loaded");

    // 2. Image Loading and Event Listener Setup:

  const image = document.getElementById("uploaded-image");

  if (image) {
    image.addEventListener("load", () => {
      console.log("Image loaded");
      processImage(image);
    });
    // Manually trigger load event if image is already loaded
    if (image.complete) {
      console.log("Image already loaded");
      processImage(image);
    }
  } else {
    console.log("No image element found 123");
  }
}
// upload the glasses images
const glassesImage = new Image();

// glassesImage.src = "/static/tryon_app/images/glasses.png";
const hiddenInput = document.getElementById("tryon1");
glassesImage.src = hiddenInput.value;
glassesImage.onload = () => console.log("Glasses image loaded");
document.addEventListener("DOMContentLoaded", (event) => {
  const glassesImage = new Image();
  // glassesImage.src = "/static/tryon_app/images/glasses.png";
  const hiddenInput = document.getElementById("tryon1");
  glassesImage.src = hiddenInput.value;
  glassesImage.onload = function () {
    console.log("Glasses image loaded 123");
  };

  // Assuming other initialization code goes here, e.g., event listeners
});
//overlay the glasses onto the image's face
function overlayGlasses(canvas, detections) {
  const context = canvas.getContext("2d");
  context.clearRect(0, 0, canvas.width, canvas.height); // Clear previous drawings

  detections.forEach((detection) => {
    const landmarks = detection.landmarks;
    const leftEye = landmarks.getLeftEye();
    const rightEye = landmarks.getRightEye();

    // Calculate the center point between the eyes
    const centerX = (leftEye[0].x + rightEye[0].x) / 2;
    const centerY = (leftEye[0].y + rightEye[0].y) / 2;

    // Calculate the distance between the eyes
    const eyeDistance = rightEye[0].x - leftEye[0].x;

    // Calculate the width and height of the glasses
    const glassesWidth = eyeDistance * 2.2; // Adjust multiplier as needed
    const glassesHeight =
      (glassesWidth / glassesImage.width) * glassesImage.height;

    // Position the glasses at the center between the eyes, slightly above
    const glassesX = centerX - glassesWidth / 2;
    const glassesY = centerY - (glassesHeight / 2) * 1.2; // Adjust the vertical position as needed

    console.log(
      `Drawing glasses 123 at (${glassesX}, ${glassesY}) with width ${glassesWidth} and height ${glassesHeight}`
    );

    context.drawImage(
      glassesImage,
      glassesX,
      glassesY,
      glassesWidth + 10,
      glassesHeight + 10
    );
  });
}
// Processing the Image:
async function processImage(image) {
  console.log("Processing image");
  const canvas = document.getElementById("overlay-canvas");
  const displaySize = { width: image.width, height: image.height };
  canvas.width = displaySize.width;
  canvas.height = displaySize.height;

  faceapi.matchDimensions(canvas, displaySize);
  const detections = await faceapi
    .detectAllFaces(image, new faceapi.TinyFaceDetectorOptions())
    .withFaceLandmarks();
  console.log("Detections:", detections);

  const resizedDetections = faceapi.resizeResults(detections, displaySize);
  overlayGlasses(canvas, resizedDetections);
}
// Final Initialization:
setupFaceApi();

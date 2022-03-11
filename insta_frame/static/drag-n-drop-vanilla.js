// after https://www.smashingmagazine.com/2018/01/drag-drop-file-uploader-vanilla-js/

const dropArea = document.getElementById("drop-area");

function checkAvailableDragAndDropAPI() {
  var div = document.createElement("div");
  return (
    ("draggable" in div || ("ondragstart" in div && "ondrop" in div)) &&
    "FormData" in window &&
    "FileReader" in window
  );
}

if (checkAvailableDragAndDropAPI()) {
  dropArea.classList.add("has-advanced-upload");
}

dropArea.addEventListener("dragenter", (e) => onDragEnter(dropArea, e));
dropArea.addEventListener("dragleave", (e) => onDragLeave(dropArea, e));
dropArea.addEventListener("dragover", (e) => onDragOver(dropArea, e));
dropArea.addEventListener("drop", (e) => onDrop(dropArea, e));

function onDragEnter(element, event) {
  preventDefaults(event);
  highlight(element);
}
function onDragLeave(element, event) {
  preventDefaults(event);
  unhighlight(element);
}
function onDragOver(element, event) {
  preventDefaults(event);
  highlight(element);
}
function onDrop(element, event) {
  preventDefaults(event);
  unhighlight(element);

  handleDrop(event);
}

function handleDrop(event) {
  const dataTransfer = event.dataTransfer;
  const files = dataTransfer.files;

  handleFiles(files);
}

function handleFiles(files) {
  const file = files.item(0);
  upload(file);
  previewFile(file);
}

function uploadFrom(form) {
  return (file) => {
    if (form.classList.contains("is-uploading")) {
      return;
    }

    form.classList.remove("is-error");
    form.classList.add("is-uploading");

    const formData = new FormData();

    formData.append("file", file);

    fetch(form.action, { method: "Post", body: formData })
      .then((response) => response.json())
      .then((data) => onfulfilled(form, data))
      .catch(onrejected);
  };
}

const upload = uploadFrom(dropArea);

function onfulfilled(form, data) {
  if (data.image) {
    setImage(data.image, "image with 1:1 aspect ratio");
    form.classList.remove("is-uploading");
    form.classList.add("is-success");
  } else {
    window.location.href = form.action.replace("%3F", "");
  }
}

function onrejected(reason) {
  console.log(reason);
}

function preventDefaults(event) {
  event.preventDefault();
  event.stopPropagation();
}

function highlight(element) {
  element.classList.add("is-dragover");
}

function unhighlight(element) {
  element.classList.remove("is-dragover");
}

function onInputChanged(element) {
  const files = element.files;
  handleFiles(files);
}

function previewFile(file) {
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () =>
    setImage(reader.result, `chosen image: ${file.name}`);
}

function setImage(src, alt) {
  const imageElement = document.getElementById("image");
  imageElement.src = src;
  alt && (imageElement.alt = alt);
  imageElement.classList.remove("placeholder-img");
}

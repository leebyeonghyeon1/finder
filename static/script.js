import { searchObject } from "./search.js";

// @ top-bar 상단바
document.getElementById("search-btn").addEventListener("click", function () {
  var query = document.getElementById("search-box").value;
  if (query) {
    searchObject(query);
  } else {
    document.getElementById("status-message").textContent =
      "검색어를 입력하세요.";
  }
}); //: 검색 버튼을 눌렀을 때

document.getElementById("search-box").addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    var query = document.getElementById("search-box").value;
    if (query) {
      searchObject(query);
    } else {
      document.getElementById("status-message").textContent =
        "검색어를 입력하세요.";
    }
  }
}); //: 검색창에서 엔터를 눌렀을 때

document.getElementById('all-btn').addEventListener('click', function () {
  // Clear the search-image-area
  const searchArea = document.getElementById('search-img-area');
  searchArea.innerHTML = '';

  // Fetch all images from the static folder (assuming server returns an array of image filenames)
  fetch('/get_all_images')
    .then(response => response.json())
    .then(data => {
      data.forEach(image => {
        if (image.endsWith('.jpg')) { // Only include .jpg files
          const imgElement = document.createElement('img');
          imgElement.src = `/static/${image}`;
          imgElement.style.maxWidth = '45%';
          imgElement.style.padding = '10px';
          searchArea.appendChild(imgElement);

          // Attach click event listener to each image
          imgElement.addEventListener("click", function () {
            processImageClick(this, searchArea);
          });
        }
      });
    });
});

function processImageClick(clickedImage, searchArea) {
  document.getElementById("status-message").textContent = "검색 중...";
  let itemName = clickedImage.src.split("/").pop().split(".")[0]; // Extract item name from image filename

  // Remove all images except the clicked one
  Array.from(searchArea.children).forEach((img) => {
    if (img !== clickedImage) {
      searchArea.removeChild(img);
    }
  });

  // Send AJAX request to the server
  fetch("/process_image", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ item_name: itemName }),
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("status-message").textContent = "검색 완료";

      const resultArea = document.getElementById("result-img-area");
      const resImgElm = document.createElement("img");
      resImgElm.src = data.image_url;
      resImgElm.alt = itemName;
      resImgElm.style.maxWidth = "90%";
      resImgElm.style.padding = "10px";

      // Clear previous result images
      resultArea.innerHTML = "";

      // Append the new result image
      resultArea.appendChild(resImgElm);
    });
}

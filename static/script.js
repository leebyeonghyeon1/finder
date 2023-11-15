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
  // 검색 이미지 영역 지우기
  const searchArea = document.getElementById('search-img-area');
  
  searchArea.innerHTML = '';
  

  // 정적 폴더에서 모든 이미지 가져오기(서버가 이미지 파일 이름 배열을 반환한다고 가정)
  fetch('/get_all_images')
    .then(response => response.json())
    .then(data => {
      data.forEach(image => {
        if (image.endsWith('.jpg')) { // .jpg 파일만 포함합니다
          const imgElement = document.createElement('img');
          imgElement.src = `/static/${image}`;
          imgElement.style.maxWidth = '45%';
          imgElement.style.padding = '10px';
          searchArea.appendChild(imgElement);

          // 각 이미지에 클릭 이벤트 수신기 첨부
          imgElement.addEventListener("click", function () {
            processImageClick(this, searchArea);
          });
        }
      });
    });
});

function processImageClick(clickedImage, searchArea) {
  document.getElementById("status-message").textContent = "검색 중...";

  let itemName = clickedImage.src.split("/").pop().split(".")[0]; // 이미지 파일 이름에서 항목 이름 추출

  // 클릭한 이미지를 제외한 모든 이미지 제거
  Array.from(searchArea.children).forEach((img) => {
    if (img !== clickedImage) {
      searchArea.removeChild(img);
    }
  });

  // 서버에 AJAX 요청 보내기
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

      // 이전 결과 영상 지우기
      resultArea.innerHTML = "";

      // 새 결과 이미지 추가
      resultArea.appendChild(resImgElm);
    });
}

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

// ~ 사용자가 입력한 검색어로 오브젝트를 검색
function searchObject(query) {
  document.getElementById("status-message").textContent = "검색 중...";

  fetch(`/search?query=${query}`)
    .then((response) => response.json())
    .then((data) => {
      const searchArea = document.getElementById("search-image-area");
      searchArea.innerHTmL = "";
      const resultArea = document.getElementById("result-area");
      resultArea.innerHTML = "";

      if (data.success && data.results.length > 0) {
        data.results.forEach((result) => {
          const imgElement = document.createElement("img");
          imgElement.src = result.image;
          imgElement.alt = result.name;
          imgElement.style.maxWidth = "20%";
          imgElement.style.padding = "10px";

          searchArea.appendChild(imgElement);

          // 이미지 클릭 시 resultArea에 outputImageElement 표시
          imgElement.addEventListener("click", function () {
            // 서버에 AJAX 요청을 보냅니다.
            fetch("/process_image", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ item_name: result.name }),
            })
              .then((response) => response.json())
              .then((data) => {
                // 반환된 이미지 URL을 사용하여 웹 페이지에 이미지를 표시합니다.
                const outputImageElement = document.createElement("img");
                outputImageElement.src = data.image_url;
                outputImageElement.alt = data.name;
                resultArea.appendChild(outputImageElement);
              });
          });
        });
      } else {
        document.getElementById("status-message").textContent =
          "결과를 찾을 수 없습니다.";
      }
    });
}

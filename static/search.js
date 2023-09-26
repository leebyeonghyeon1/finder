// ~ 사용자가 입력한 검색어로 오브젝트를 검색
export function searchObject(query) {
  // Clear previous search results
  const searchArea = document.getElementById("search-img-area");
  searchArea.innerHTML = "";
  const resultArea = document.getElementById("result-img-area");
  resultArea.innerHTML = "";

  document.getElementById("status-message").textContent = "찾고 싶은 상품 이미지를 클릭하세요.";

  fetch(`/search?query=${query}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success && data.results.length > 0) {
        data.results.forEach((result) => {
          const itemImgElm = document.createElement("img");
          itemImgElm.src = result.image;
          itemImgElm.alt = result.name;
          itemImgElm.style.maxWidth = "50%";
          itemImgElm.style.padding = "5px";

          searchArea.appendChild(itemImgElm);

          // 이미지 클릭 시 resultArea에 outputImageElement 표시
          itemImgElm.addEventListener("click", function () {
            document.getElementById("status-message").textContent = "검색 중...";

            let itemName = this.src.split("/").pop().split(".")[0]; // ~이미지의 파일 이름에서 확장자를 제거하고 그 결과를 item_name으로 사용합니다.


            // 지정되지 않은 itemImg는 제거
            Array.from(searchArea.children).forEach((img) => {
              if (img !== this) {
                searchArea.removeChild(img);
              }
            });

            // 서버에 AJAX 요청을 보내기
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


                // 반환된 이미지 URL을 사용하여 웹 페이지에 이미지를 표시
                const resImgElm = document.createElement("img");
                resImgElm.src = data.image_url;
                resImgElm.alt = itemName; // alt 속성에도 item_name 
                resImgElm.style.maxWidth = "90%";
                resImgElm.style.padding = "10px";
                // 기존 이미지 제거
                resultArea.innerHTML = "";
                // resultArea에 이미지를 추가
                resultArea.appendChild(resImgElm);
              });
          });
        });
      } else {
        document.getElementById("status-message").textContent =
          "결과를 찾을 수 없습니다.";
      }
    });
}

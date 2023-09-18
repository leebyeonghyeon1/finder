#seonghan
from flask import Flask, request, jsonify, send_from_directory, url_for
import os
import logging
import send_message

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder=os.path.join(os.getcwd(), "static"),
)

log_file_path = os.path.join(os.getcwd(), "app.log")

# 로거 객체 생성
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# 파일 핸들러 설정
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)

# 스트림 핸들러 설정 (터미널에 출력하기 위함)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# 로깅 포맷 설정
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 파일 핸들러와 스트림 핸들러에 로깅 포맷을 적용
file_handler.setFormatter(log_format)
stream_handler.setFormatter(log_format)

# 핸들러를 로거에 추가
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


# 루트 경로 ("/")에 대한 라우트 추가
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/images/<filename>")
def send_image(filename):
    return send_from_directory("images", filename)

@app.route('/output_img/<filename>')
def output_image(filename):
    return send_from_directory('output_img', filename)


# 오브젝트 검색 함수
def find_objects(query):
    return [item for key, item in objects.items() if query.lower() in key.lower()]


# '/search' 경로에 대한 라우트 설정. GET 메서드를 사용합니다.
@app.route("/search", methods=["GET"])
def search():
    # 사용자의 검색 쿼리를 가져옵니다.
    query = request.args.get("query")

    # find_objects 함수를 사용해 검색 쿼리와 일치하는 오브젝트를 찾습니다.
    results = find_objects(query)

    # 검색된 각 결과에 대해 이미지 URL을 수정합니다.
    for result in results:
        result[
            "image"
        ] = f"/static/{result['name']}.jpg"  # 정적 폴더 내의 경로로 이미지 URL을 업데이트합니다.

    # 검색 결과를 JSON 형식으로 반환합니다.
    return jsonify(success=True, results=results)

# 쿼리 번역 딕셔너리
word_mapping = {
    "신라면 컵" : "Shin Ramyun -cup- 65g",
    "새우탕 컵" : "Shrimp soup noodle -cup- 67g",
    "짜파구리 컵" : "Angry Chapaguri -cup- 108 g",
    "쇠고기 미역국라면 컵" : "beef and seaweed soup -cup- 100g",
    "불닭볶음면 팩" : "Hot Chicken Flavor Ramen 140g",
    "진라면 컵" : "Jin Ramen Spicy -Cup- 65g",
    "진라면 팩" : "Jin Ramen Spicy 120g",
    "참깨라면 컵" : "Chamggae Ramen -cup- 65g",
    "안성탕면 팩" : "Anseongtangmyeon -cup- 125g",
    "짜파게티 컵" : "Chapagetti -cup- 123g"

}

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        # 사용자로부터 전달받은 물품명
        data = request.get_json()
        item_name = data.get('item_name')

        # 전달받은 물품명을 영어로 변경
        item_name = word_mapping.get(item_name, "Unknown_Item")

        # sendmessage 함수를 사용하여 이미지 처리
        send_message.start_AI(item_name)

        # 처리된 이미지의 URL을 반환합니다.
        image_url = url_for('output_image', filename='output.jpg')
        app.logger.info(f"Image processed successfully, URL: {image_url}")
        return jsonify({"image_url": image_url})
    
    except Exception as e:
        app.logger.error(f"Error processing image: {str(e)}")
        return jsonify({"error": "An error occurred while processing the image."}), 500


# 현재 작업 디렉토리 내의 'static' 폴더의 경로를 가져옵니다.
static_folder = os.path.join(os.getcwd(), "static")

# static 폴더 내의 .jpg 파일들을 오브젝트로 로드합니다.
# 각 파일명을 오브젝트의 이름으로, 파일명을 오브젝트의 이미지로 사용합니다.
objects = {
    os.path.splitext(file_name)[0]: {
        "image": file_name,
        "name": os.path.splitext(file_name)[0],
    }
    for file_name in os.listdir(static_folder)
    if os.path.isfile(os.path.join(static_folder, file_name))
    and file_name.endswith(".jpg")
}


if __name__ == "__main__":  # debug: 코드 변경 시 자동으로 서버 재시작
    app.run(host="0.0.0.0", debug=True, port=5000)
    # @실행: [cmd] python app.py

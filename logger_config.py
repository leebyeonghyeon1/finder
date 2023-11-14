import logging
import os
import datetime
from werkzeug.serving import WSGIRequestHandler


def setup_logger():
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
    log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # 파일 핸들러와 스트림 핸들러에 로깅 포맷을 적용
    file_handler.setFormatter(log_format)
    stream_handler.setFormatter(log_format)

    # 핸들러를 로거에 추가
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


class CustomRequestHandler(WSGIRequestHandler):
    def log_request(self, code="-", size="-"):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        client_address = getattr(self, "client_address", "Unknown")[0]
        command = getattr(self, "command", "Unknown")
        path = self.requestline.split()[1]  # 요청 경로 추출

        self.log(
            "info",
            'Client %s - - [%s] "%s %s %s" %s %s',
            client_address,
            current_time,
            command,
            path,
            self.request_version,
            code,
            size,
        )


# 요청 핸들러 설정을 위한 함수
def set_custom_request_handler():
    WSGIRequestHandler.log_request = CustomRequestHandler.log_request

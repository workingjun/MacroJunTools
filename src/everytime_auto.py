import sys

from src.utils.custom_logging import GetLogger
logging_file_path = "src/logs/auto_like.log"
logger = GetLogger("logger_everytime", logging_file_path)

from src.app.everytime.articles import move_to_board
from src.app.everytime.articles import find_starting_point
from src.app.everytime.login import login_everytime
from src.app.everytime.autolike import StartAutoLike
from src.utils.chrome_manager import ChromeDriverManager
from src.utils.file.env_utils import load_env
from selenium.common.exceptions import NoSuchElementException
            
def run_everytime_auto_like(headless):
    global logger

    # .env 파일 및 config.yaml 파일 불러오기
    env_values = load_env()

    # .env에서 민감한 정보 가져오기
    my_id = env_values.get("EVERYTIME_USERNAME")
    my_password = env_values.get("EVERYTIME_PASSWORD")
    
    logger.info("Everytime ID, Password: %s, %s", my_id, my_password)
    
    if not my_id or not my_password:
        logger.error("Everytime ID, Password are missing in .env file!")
        raise
    
    logger.info("Starting Everytime auto-like...")
    
    try:
        manager = ChromeDriverManager()
        manager.start(headless=headless, url="https://everytime.kr/")

        # 크롬이 종료되었을 경우 예외 처리
        if not manager.browser:
            logger.error("Chrome browser failed to start.")
            raise SystemExit("Chrome browser failed to start.")

        login_everytime(manager, my_id, my_password)

        move_to_board(manager, "자유게시판")
        start_article, page_num = find_starting_point(manager, logging_file_path)

        logger.info("Starting from article: %s, page number: %s", start_article, page_num)

        StartAutoLike(manager, start_article, page_num)

    except NoSuchElementException:
        if manager:
            manager.stop()
        logger.info("Exiting program as there are no more elements to process.")
        sys.exit(0)  # 정상 종료
    
    finally:
        if manager:
            manager.stop()
        logger.info("The task is complete.")
        sys.exit(0)  # 정상 종료



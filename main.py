import os
import time
import pyperclip
import pyautogui
import autoit
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 데이터 파일
config = configparser.ConfigParser()

# 데이터 읽기
config.read('config.ini', encoding='utf-8')

# 데이터 파일 만들기
config["system"] = {}
config["system"]["title"] = "제목"
config["system"]["content"] = "내용(줄바꿈)내용"
config["system"]["naver_id"] = "네이버 아이디"
config["system"]["naver_pw"] = "네이버 비밀번호"
config["system"]["naver_url"] = "네이버 카페 주소"
config["system"]["board_number"] = "0"
with open('config.ini', 'w', encoding='utf-8') as configfile:
    config.write(configfile)

# 글쓰기 제목 / 내용
title = config["system"]["title"]
content = config["system"]["content"].replace('(줄바꿈)', "\n")

# 네이버 계정
naver_id = config["system"]["naver_id"]
naver_pw = config["system"]["naver_pw"]
naver_cafe_url = config["system"]["naver_url"]
board_number = int(config["system"]["board_number"])

# 크롬
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(5)
driver.get(naver_cafe_url)

print("[ Automatic Naver Cafe Posting ]")
print("지금부터 자동 게시글 올리기 프로그램을 시작합니다")
print("Made by MIN\n\n\n")

# 로그인
print("로그인 시도중 . . .")
driver.find_element(By.ID, "gnb_login_button").click()
# 네이버 아이디 입력
driver.find_element(By.ID, 'id').click()
pyperclip.copy(naver_id)
driver.find_element(By.ID, 'id').send_keys(Keys.CONTROL, 'v')
# 네이버 패드워드 입력
driver.find_element(By.ID, 'pw').click()
pyperclip.copy(naver_pw)
driver.find_element(By.ID, 'pw').send_keys(Keys.CONTROL, 'v')
# #로그인 버튼 입력
driver.find_element(By.ID, 'log.login').click()
print("로그인 완료 !")

# 글쓰는 페이지 이동
print("글쓰기 시도중 . . .")
driver.find_element(By.CLASS_NAME, 'cafe-write-btn').click()
driver.switch_to.window(driver.window_handles[-1])
time.sleep(2)

# 게시판 선택
print("게시판 선택중 . . .")
board_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[1]/button'
driver.find_element(By.XPATH, board_xpath).click()
driver.find_elements(By.CLASS_NAME, "option")[board_number].click()
time.sleep(1)
pyautogui.press('enter')
print("게시판 선택 완료 !")

# 제목 입력
time.sleep(1)
print("제목 입력중 . . .")
title_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[1]/div[2]/div/textarea'
driver.find_element(By.XPATH, title_xpath).send_keys(title)
print("제목 입력 완료 !")

# 내용 입력
print("내용 입력중 . . .")
driver.find_element(By.CLASS_NAME, "se-canvas-bottom").click()
pyperclip.copy(content)
pyautogui.hotkey('ctrl', 'v')
print("내용 입력 완료 !")

# 사진 업로드
print("사진 업로드중 . . .")
image_class = "se-image-toolbar-button.se-document-toolbar-basic-button.se-text-icon-toolbar-button"
driver.find_element(By.CLASS_NAME, image_class).send_keys(Keys.ENTER)
time.sleep(1)
handle = "[CLASS:#32770; TITLE:열기]"
autoit.win_wait_active("열기", 3)
img_path = os.getcwd() + '\image.png'
autoit.control_send(handle, "Edit1", img_path)
time.sleep(1)
autoit.control_click(handle, "Button1")
time.sleep(1)
print("사진 업로드 완료 !")

# 올리기 버튼 클릭
time.sleep(1)
driver.find_element(
    By.CLASS_NAME, "BaseButton.BaseButton--skinGreen.size_default").click()
print("\n글쓰기 완료 !\n\n")

time.sleep(2)

# 종료
print("프로그램을 정상적으로 마쳤습니다 !")
print("3초후 자동으로 종료됩니다")
time.sleep(3)
driver.quit()

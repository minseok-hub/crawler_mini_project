# 웹크롤러를 이용한 상품조회 서비스

셀리니움(Selenium)과 BeautifulSoup으로 만든 웹크롤러와 Telegram API를 사용하여 간단 쇼핑정보를 확인할 수 있는 프로젝트입니다. 

Anaconda를 설치하여 진행했습니다.

먼저 필요한 모듈을 ```pip```으로 설치합니다.

```requirements.txt```는 다음과 같습니다.

```txt
# webcrawler
bs4
selenium
requests

# For telegram
python-telegram-bot
```

```.ipynb```를 실행하기 전 ```requirements.txt```를 실행해서 환경설정을 해줄 필요가 있습니다.

```bash
pip install -r requirements.txt
```

설치가 끝나면 python  파일을 실행합니다.
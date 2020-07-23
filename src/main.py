import os

from selenium import webdriver
from bs4 import BeautifulSoup
from telegram import Bot
from goods import Goods, goodsALL, goodsDetail, goodsInfo

# Crawler

def movePage(driver, url):
    # url 바로 가기
    driver.get(url)

def clickStock(driver):
    # '제품선택'버튼을 누른다.
    driver.find_element_by_xpath('//*[@id="wrap"]/div/div[2]/div[2]/form/fieldset/div[4]/div[1]/ul/li/ul/li[1]/div/div').click()

def stockChoice(driver, index):
    # index를 통해 제품을 선택한다.
    driver.find_element_by_xpath('/html/body/div[2]/div/ul/li[{}]'.format(index)).click()

def getStockIndices(driver):
    # 제품의 제고 종류를 구하기
    clickStock(driver)
    option = driver.find_elements_by_xpath('/html/body/div[2]/div/ul')[0]
    soup = BeautifulSoup(option.get_attribute('innerHTML'), 'html.parser')
    li = soup.select('li')
    # return에서 +1 을 해준 이유는 이후 getQuantities함수 시행할 for문 조건 때문이다.
    return len(li) + 1

def getQuantities(driver, url):
    # 자세히보기
    # 제품의 제고 종류 갯수를 받아온다.
    movePage(driver, url)
    stock_indices = getStockIndices(driver)
    stock_dictionary = {}
    # '제품선택'이란 칸 때문에 2부터 상품의 제고가 된다. getStockIndices에서 +1을 한 이유이다.
    for index in range(2, stock_indices):
        movePage(driver, url)
        clickStock(driver)
        stockChoice(driver, index) # driver객체와 index를 매개인자로 넘긴다.
        # driver.find_element_by_xpath('/html/body/div[2]/div/ul/li[{}]'.format(index)).click()
        #time.sleep(1)
        stock_name = driver.find_element_by_xpath('/html/body/div[3]/div/ul/li[{}]'.format(index)).get_attribute('innerHTML')
        # driver.find_element_by_xpath('//*[@id="wrap"]/div/div[2]/div[2]/form/fieldset/div[4]/div[1]/ul/li/ul/li[2]/div/div').click()
        #time.sleep(1)
        remain_stocks = driver.find_element_by_xpath('/html/body/div[1]/div/ul')
        #print(remain_stocks.get_attribute('innerHTML'))
        soup = BeautifulSoup(remain_stocks.get_attribute('innerHTML'), 'html.parser')
        stock_dictionary[stock_name] = [stock.text.replace('\xa0', '') for stock in soup.select('li')[1:]] # '사이즈'란 때문
        print(stock_name)
        print(stock_dictionary[stock_name])
        
    return stock_dictionary

# stock_dictionary
def dictionaryGetString(stock_dictionary):
    string = ''
    for key, value in stock_dictionary.items():
        string = string + '[' + key + "]:\n"
        for v in value:
            string = string + '\t' + v + '\n'
    
    return string

#print(string)

if __name__=="__main__":
    # selenium 사용을 위한 webdriver설정!
    chromedriver = os.environ['CHROMEDRIVER']
    driver = webdriver.Chrome(chromedriver)
    driver.implicitly_wait(3)
    url = 'https://smartstore.naver.com/launhing'

    my_token = 'api 토큰'
    driver.get(url)
    # telegram Bot 생성
    bot = Bot(token=my_token)
    last_message = bot.getUpdates()[-1].message
    username = last_message.chat.first_name + "_" + last_message.chat.last_name
    message_id = last_message.message_id
    search_check = False
    detail_check = False
    goods_list = goodsALL(driver)
    print("총 상품 갯수: {}".format(len(goods_list)))
    while True:
        last_message = bot.getUpdates()[-1].message
        # print(last_message)
        if message_id == last_message.message_id:
            continue
        
        # 양쪽 빈칸 제거
        command = last_message.text.strip()
        print(command)
        message_id = last_message.message_id
        chat_id = last_message.chat.id
        if command.lower() in ["시작", "start"]:
            bot.sendMessage(chat_id=chat_id, text="안녕하세요~ {} 님! 무엇을 도와드릴까요?".format(username))
        elif command.lower() in ["검색", "검색하기"]:            
            bot.sendMessage(chat_id=chat_id, text="검색할 상품을 입력해주세요!")
            search_check = True
            detail_check = False
        elif command.lower() in ["자세히", "자세히 보여줘", "자세히 보여줘!"]:
            bot.sendMessage(chat_id=chat_id, text="자세히 볼 상품을 입력해주세요!")
            detail_check = True
            search_check = False
        elif search_check:
            search_check = False
            if command:
                goods_list = goodsInfo(goods_list, command)
            for goods in goods_list:
                bot.sendMessage(chat_id=chat_id, text=str(goods))
            bot.sendMessage(chat_id=chat_id, text="입력하신 \"{}\"관련 상품, 총 {}개를 찾았습니다.".format(command, len(goods_list)))
        elif detail_check:
            detail_check = False
            bot.sendMessage(chat_id=chat_id, text="잠시만 기다려주세용")
            goods = goodsDetail(goods_list, command)
            if goods is None:
                bot.sendMessage(chat_id=chat_id, text="입력하신 \"{}\"상품이 존재하지 않습니다.".format(command))
                continue
                
            goods_link = goods.getGoodsLink()
            print("detail-url: ", goods_link)
            stock_dictionary = getQuantities(driver, goods_link)
            string = dictionaryGetString(stock_dictionary)
            information = str(goods) + string
            print(information)
            bot.sendMessage(chat_id=chat_id, text=information)
        elif command.lower() in ['h', 'help']:
            help_text = "[사용법]\nshopping_bot은 다음과 같은 3가지 기능을 제공합니다.\n1. \"시작\" 또는 \"Start\" 등을 통해서 텔레그램봇을 활성화시킵니다.\n2. \"검색\", \"검색하기\"를 입력하면 검색된 물품 정보를 간력히 출력합니다.\n3. \"자세히\" 또는 \"자세히 보여줘\" 명령을 통해 상품의 제고현황을 알 수 있습니다."
            bot.sendMessage(chat_id=chat_id, text=help_text)
        elif command.lower() in ["종료", "탈출", "그만", "exit", "quit"]:
            bot.sendMessage(chat_id=chat_id, text="그래 우리 그만 대화하자! 안녕~!!")
        else:
            bot.sendMessage(chat_id=chat_id, text="저는 3가지 기능 밖에 제공하지 않습니다!")
    
        # if command.lower() in ["종료", "탈출", "그만", "exit", "quit"]:
        #    break
        
    driver.stop_client()
    driver.close()

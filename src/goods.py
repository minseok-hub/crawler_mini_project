from bs4 import BeautifulSoup

def goodsALL(driver):
    url = 'https://smartstore.naver.com'
    goods_xpath = driver.find_element_by_xpath('//*[@id="content"]/form/div[2]/div')
    soup = BeautifulSoup(goods_xpath.get_attribute('innerHTML'), 'html.parser')
    goods = soup.select('li')
    goods_list = []
    for a_tag in goods:
        link  = a_tag.select('a.area_overview')[0].attrs['href']
        #print([info.text for info in a_tag.select('strong')])
        good_info = [info.text for info in a_tag.select('strong')]
        good_info.append(url + link)
        good = Goods(*good_info)
        #print(good)
        goods_list.append(good)
        
    return goods_list

def goodsInfo(goods_list, goods_name=''):
    # print('"{}" 상품을 검색합니다.!'.format(goods_name))
    return [goods for goods in goods_list if goods_name in goods.getGoodsName()]

def goodsDetail(goods_list, goods_name=''):
    # 자세히 볼 상품 객체 반환
    for goods in goods_list:
        if goods_name in goods.getGoodsName():
            return goods
    return None

class Goods:
    # 상품 정보 클래스
    def __init__(self,
                 goods_name,
                 discounted_price,
                 original_price,
                 discount_rate,
                 goods_link):
        self._goods_name = goods_name
        self._discounted_price = discounted_price
        self._original_price = original_price
        self._discount_rate = discount_rate
        self._goods_link = goods_link
        
    def getGoodsName(self):
        return self._goods_name
    
    def getDiscountedPrice(self):
        return self._discounted_price
    
    def getOriginalPrice(self):
        return self._original_price
    
    def getDiscountRate(self):
        return self._discount_rate
    
    def getGoodsLink(self):
        return self._goods_link
    
    def __str__(self):
        return "************\n상품명: {}\n할인된 가격: {}\n원   가: {}\n할인률: {}\n상품 링크: {}\n************\n".format(
            self._goods_name,
            self._discounted_price,
            self._original_price,
            self._discount_rate,
            self._goods_link
        )
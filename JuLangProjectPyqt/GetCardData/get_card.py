#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@ author: guess
@ effect:
@ Time : 2018/10/17 15:01Referer: http://dayzadmin.qqsgame.com/majiangcs/adminnew/login_new.php
"""

#注意檢查：uuid=%s&gametype=3&timestamp=%s  中的gametype
try:
    import requests
except:
    import os
    os.system("pip install requests")
    import requests

try:
    from bs4 import BeautifulSoup
except:
    import os
    os.system("pip install beautifulsoup4")
    from bs4 import BeautifulSoup


import time,json
from collections import Counter
class GetCard:
    def __init__(self,versions,date, uid,pullOutCardNumber=None):
        self.date = date
        self.uid = uid
        self.versions = versions
        self.pullOutCard = pullOutCardNumber
        self.url = None
        self.params = None
        self.get_card_url = None
        self.cookies = None
        self.handCaed = None
        self.mound_takeOutCard = None
        self.allPlayerHandCard = None
        self.make_card = []
        self.oneLine = None   #牌局列表第一行数据
        self.zhuaMa = None    #抓码数据
        self.dun_card = None  #最后墩上未知的牌数据
        self.valueError = None
        self.get_cookie()

    def get_cookie(self):
        if self.versions == "长沙":
            self.params = {
                "aname": "ceshi_zhaohuabing",
                "apwd": "7cn0fJLDktmjbpKREM",
                "language": "majiangcs",
                                            }
            self.url = 'https://dayzadmin.qqsgame.com/majiangcs/adminnew/login_new.php?ver=majiangcs'
        elif self.versions == "常德":
            self.params = {
                "aname": "ceshi_zhaohuabing",
                "apwd": "7cn0fJLDktmjbpKREM",
                "language": "majiangcd",
                                            }
            self.url = 'https://hyadmin.qqsgame.com/majiangcd/adminnew/login_new.php?ver=majiangcd'
        elif self.versions == "主版本":
            self.params = {
                "aname": "ceshi_zhaohuabing",
                "apwd": "7cn0fJLDktmjbpKREM",
                "language": "majiang",
            }
            self.url = 'https://qsadmin.jiaheyx.com/majiang/adminnew/login_new.php?ver=majiang'

        s = requests.session()
        requests.utils.add_dict_to_cookiejar(s.cookies, self.params)
        s.post(self.url, self.params)
        self.cookies = s.cookies.get_dict()

    def login_platform(self):
        tss = self.date
        id1 = self.uid
        # tm = time.strptime(tss, '%Y-%m-%d %H:%M:%S')
        try:
            timeArray = time.strptime(tss, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            self.valueError = False
            return

        timeStamp = int(time.mktime(timeArray))
        if self.versions == "长沙":
            self.get_card_url = "https://dayzadmin.qqsgame.com/majiangcs/adminnew/userinfo/singlegambling.php?"
        elif self.versions == "常德":
            self.get_card_url = "https://hyadmin.qqsgame.com/majiangcd/adminnew/userinfo/singlegambling.php?"
        elif self.versions == "主版本":
            self.get_card_url = "https://qsadmin.jiaheyx.com/majiang/adminnew/userinfo/singlegambling.php?"

        url = "%suuid=%s&gametype=3&timestamp=%s" % (self.get_card_url, id1, timeStamp)

        request_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/66.0.3359.139 Safari/537.36",
            "Cookie": "aliyungf_tc=%s; acw_tc=%s; PHPSESSID=%s; " % (
                self.cookies["aliyungf_tc"], self.cookies["acw_tc"], self.cookies["PHPSESSID"]),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        }
        s = requests.get(url=url, headers=request_headers)
        if s.status_code != 200:
            raise Exception("网页请求状态码为:", s.status_code)
        html = s.text
        soup = BeautifulSoup(html)
        return soup

    def get_hand_card(self):
        soup = self.login_platform()
        if self.valueError is False:
            return
        elif str(soup) == "<html><body><pre></pre></body></html>":
            return



        handCard = []
        mound_takeOutCard = []
        oneLine = []
        oneLine_sign = True
        #第一步:获取手牌和摸牌数据
        for string in soup.strings:
            if oneLine_sign:       #获取第一行数据
                oneLine.append(string)
                oneLine_sign = False
            defined_list = []
            if "手牌" in str(string):
                if len(str(string)) > 62:
                    """获取手牌数据"""
                    index = string.index("手牌")
                    cards = string[index:][2:-1]
                    defined_list.append(cards)
                    handCard.append(defined_list)
            elif "摸牌" in str(string):
                """获取出的牌数据"""
                mound_takeOutCard.append("%s"% str(string)[-2:])

            elif "扎码个数：" in str(string):
                self.zhuaMa = string[-1] #中文冒号
            elif "扎码个数: " in str(string):
                self.zhuaMa = string[-1] #英文冒号



        self.allPlayerHandCard = handCard
        self.mound_takeOutCard = mound_takeOutCard
        self.oneLine = oneLine
        return handCard,mound_takeOutCard

    def hand_card_order(self):
        '''手牌顺序校验'''
        for i in range(1,len(self.allPlayerHandCard)):
            onePlayerCard = len(self.allPlayerHandCard[0][0])
            if onePlayerCard <  len(self.allPlayerHandCard[i][0]):
                return True
        return


    def playing_method_filtration(self):
        """游戏玩法过滤"""

        allHandCard = []
        try:
            handCard,mound_takeOutCard = self.get_hand_card()
        except TypeError:
            return False


        #字符串牌型转义成列表牌型
        for card in handCard:
            cards = "".join(card).replace(",","")
            for i in range (len(cards)):
                if i %2 == 0:
                    allHandCard.append(cards[i:i+2])
        for card in mound_takeOutCard:
            cards = "".join(card).replace(",","")
            for i in range (len(cards)):
                if i %2 == 0:
                    allHandCard.append(cards[i:i+2])

        self.handCaed = allHandCard
        #刷选是跑胡子还是麻将
        allHandCard_sign = []
        kind = []  #牌型种类
        for i in allHandCard:
            allHandCard_sign.append(i[-1])
        sign = Counter(allHandCard_sign)
        for key in dict(sign).keys():
            kind.append(key)
        card_kind = sorted(kind)
        paohuzi = 2
        if len(card_kind) is paohuzi:
            if card_kind == ['S', 'B'] or card_kind == ['B', 'S']:
                return "paohuzi"

        elif len(card_kind) == 4:
            if card_kind == ['c', 'd', 'h', 's']:
                return "runfast"
            elif card_kind == ['S', 'T', 'W', 'Z']:
                return "HongzhongMajiang"
        else:
            return "majiang"



    def transition_json(self,data):
        '''数据格式转换'''
        j = 1
        all_cards = "{"
        for i in data:
            cards = ""
            cards_v = i[0].split(',')

            for value in cards_v:
                card = value.upper()
                if len(cards) != 0:
                    cards = cards + ","
                cards = cards + "\"" + card + "\""
            all_cards = all_cards + "\"" + str(j) + "\":[" + cards + "]," + "\n"
            j += 1
        all_cards += "}"
        return all_cards


    def zhuai_niao_data(self):
        zhuaMa = self.zhuaMa_data()
        niao_data = []
        if zhuaMa is not None and zhuaMa is not False:
            # 抓鸟数据插入
            for index in range(len(zhuaMa)):
                niao_data.insert(index, zhuaMa[index])
            return niao_data
        else:
            return None


    def output_all_card(self):
        _method = self.playing_method_filtration()  #玩法过滤
        if _method is False: #谨慎删除这条判断
            return False

        if _method == "runfast":
            card_data = self.transition_json(self.allPlayerHandCard)
            return str(card_data)

        else:
            #判断有无抽牌数据
            if self.pullOutCard == 10:
                self.insert_pullOutCard(data=self.handCaed, num=self.pullOutCard, insert_list=self.allPlayerHandCard)
            elif self.pullOutCard == 20:
                self.insert_pullOutCard(data=self.handCaed, num=self.pullOutCard, insert_list=self.allPlayerHandCard)
            elif self.pullOutCard == 40:
                self.insert_pullOutCard(data=self.handCaed, num=self.pullOutCard, insert_list=self.allPlayerHandCard)

            #判断抓鸟数据
            niao_data = self.zhuai_niao_data()
            if not niao_data is None:
                for card in niao_data:
                    self.mound_takeOutCard.append(card)
                c = ",".join(self.mound_takeOutCard)
                self.mound_takeOutCard.clear()
                self.mound_takeOutCard.append(c)
                self.allPlayerHandCard.append(self.mound_takeOutCard)
                newPlayerCard = self.allPlayerHandCard
                card_data = self.transition_json(newPlayerCard)
                return str(card_data)
            else:
                c = ",".join(self.mound_takeOutCard)
                self.mound_takeOutCard.clear()
                self.mound_takeOutCard.append(c)
                self.allPlayerHandCard.append(self.mound_takeOutCard)
                newPlayerCard = self.allPlayerHandCard
                card_data = self.transition_json(newPlayerCard)
                return str(card_data)



    def insert_pullOutCard(self,data,num,insert_list):
        '''插入牌数据'''
        _list = []
        initialization = []

        for i in range(num):
            _list.append(data[0])
        print("长度,",len(_list))
        str_sliceData = ",".join(_list)
        initialization.append(str_sliceData)
        insert_list.insert(0,initialization)



    def draw_card_data(self,add_list,add_number):
        '''抽牌的数据'''
        for i in range(add_number):
            add_list.append(add_list[0])



    def zhuaMa_data(self):
        if self.zhuaMa is None:  #没有抓鸟数据
            return False

        elif int(self.zhuaMa) is 0:
            return False
        else:
            oneLine = json.loads(str(self.oneLine[0]))
            if type(oneLine[-1]) is not list: #抓鸟数据格式为列表
                return "type is not list"
            else:
                return oneLine[-1][1:]         #抓鸟数据


if __name__ == "__main__":

    g = GetCard(versions="长沙",date="2019-04-20 11:08:09",uid="9f2dc1c6-9607-403e-a65b-45d04b339484",pullOutCardNumber=None)
    print(g.output_all_card())

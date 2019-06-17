import requests,json,string


def transition_json(data):
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

class CardData:
    def __init__(self,versions,playbackNumber,phoneNumber="13823720073",passwd="zhaohuabing"):
        self.versions = versions
        self._playbackNumber = playbackNumber
        self._sesskey = ""
        self.cdUrl = "https://changdeqp.qqsgame.com/majiangcd/api/mobile/api.php?api="
        self.mainUrl = "https://mj.qspokerapi0.com/majiang/api/mobile/api.php?api="
        self.csUrl = "https://dayzweb.qqsgame.com/majiangcs/api/mobile/api.php?api="

        self.paramsLogin ={"deviceid":"2018-40-03-13%3a40%3a06783",
                          "type":"1",
                          "method":"Amember.phoneLogin",
                          "openbak":"1",
                          "tel":phoneNumber,
                          "passwd":passwd,
                          "site":"2",
                          "channel":"10001",
                          "gp":"101"}



        self.Login()
    def Login(self):

        if self.versions == "主版本":
            #登录
            login_data = requests.get(self.mainUrl + json.dumps(self.paramsLogin))
            self._sesskey = json.loads(login_data.text)['data']['sesskey']
            #回放码
        elif self.versions == "长沙":
            login_data = requests.get(self.csUrl + json.dumps(self.paramsLogin))
            self._sesskey = json.loads(login_data.text)['data']['sesskey']
        elif self.versions == "常德":
            login_data = requests.get(self.cdUrl + json.dumps(self.paramsLogin))
            self._sesskey = json.loads(login_data.text)['data']['sesskey']

    def cardPlayBack(self):
        false = "false"  # info数据中有个false,需转换下
        self.paramsCardPlayBack = {"id": self._playbackNumber,
                                   "sesskey": self._sesskey,
                                   "method": "Amember.getShareGameRecord",
                               }

        if self.versions == "主版本":
            PlayBack_data = requests.get(self.mainUrl + json.dumps(self.paramsCardPlayBack))
            try:
                info = json.loads(PlayBack_data.text)["data"]["arr"]["info"]
            except TypeError:
                return False
            info_list = list(eval(info))
            data = self._getcard(hand_card=info_list[0],all_info=info_list)
            print(data)
            return data

        elif self.versions == "长沙":
            PlayBack_data = requests.get(self.csUrl + json.dumps(self.paramsCardPlayBack))
            if json.loads(PlayBack_data.text)["svflag"] is 2:
                raise Exception('检查下是否绑定了手机号码')
            try:
                info = json.loads(PlayBack_data.text)["data"]["arr"]["info"]
            except TypeError:
                return False


            info_list = list(eval(info))
            data = self._getcard(hand_card=info_list[0], all_info=info_list)
            print(data)
            return data

        elif self.versions == "常德":
            PlayBack_data = requests.get(self.cdUrl + json.dumps(self.paramsCardPlayBack))
            if json.loads(PlayBack_data.text)["svflag"] is 2:
                raise Exception('检查下是否绑定了手机号码')
            try:
                info = json.loads(PlayBack_data.text)["data"]["arr"]["info"]
            except TypeError:
                return False
            info_list = list(eval(info))
            data = self._getcard(hand_card=info_list[0], all_info=info_list)
            print(data)
            return data

    def _getcard(self,hand_card,all_info):
        hand_card = hand_card
        cardList = []  # 手牌数据
        # 找到手牌
        for i in hand_card:
            if type(i) is dict:
                for cards in i.keys():  # 找出cards
                    if cards == "cards":  # 找到手牌
                        for _cKye, _cValue in i.items():
                            if _cKye == "seatno":
                                index = int(_cValue) - 1
                                cards = i["cards"].strip(string.punctuation)  # 去除末尾的逗号
                                cardList.insert(index, cards)
        add_card = []  # 摸牌的数据
        niao_card = []  # 抓鸟数据
        for i in all_info:
            if type(i) is list:
                if i[0] is 1:  # 玩家操作
                    for _type in i:
                        if _type is 105:
                            for c in i: #找到牌数据，只有牌是字符串形
                                if type(c) is str:
                                    if c[-1] in ["F","W","T","S","Z","B","c","h","s","d"]:
                                        add_card.append(c)
                elif i[0] is 3:  # 抓鸟数据

                    if len(i) > 1:
                        if len(i[1]) < 3:
                            niao_card = i[1:]
        if not len(niao_card) is 0: #抓鸟数据添加
            for i in niao_card:
                add_card.append(i)

        m_card = self.FormatConversion(add_card)
        allCardList = [] #所有牌数据
        for i in cardList: #手牌add
            a = []
            a.append(i)
            allCardList.append(a)

        if m_card != [""]:
            allCardList.append(m_card) #摸牌add
        json_data = transition_json(allCardList)
        return json_data


    def FormatConversion(self,cardData):
        L = []
        return_info = []
        for card in cardData:
            L.append(card)
        c = ",".join(L)
        return_info.append(c)
        return  return_info

#
# a=CardData(versions="主版本",playbackNumber="11")
# print(a.cardPlayBack())
# a=CardData(versions="主版本",playbackNumber="60224")
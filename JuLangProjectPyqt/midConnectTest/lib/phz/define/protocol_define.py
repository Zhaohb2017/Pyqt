#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@ author: Hubery
@ create on: 2018/4/19 16:13
@ file: protocol_define.py
@ site: 
@ purpose: 协议号说明，协议实体定义，以及协议分类
"""

from midConnectTest.lib.phz.define.protocol_entity import *


#   玩法介绍及操作判断
class PlayIntroduction:
    def __init__(self):
        self.Chi_Pai = {"canDo": 0, "function_type": 1}
        self.Peng_Pai = {"canDo": 0, "function_type": 2}
        self.Hu_Pai = {"canDo": 0, "function_type": 9}
        self.Guo_Pai = {"canDo": 0, "function_type": 10}
        self.Chu_Pai = {"canDo": 0, "function_type": 11}
        self.QIMENFANGZI_NUM = 0

    #   修改牌的值
    def changeStr(self, value):
        if 'T' in value:
            value = value.replace('T', '10')
        result = int(value[:len(value) - 2])
        if value[-1] == 'b':
            result += 20
        return result

    #   检查胡息
    def check_hu_xi(self):
        pass

    #   检查七方门子和胡息
    def check_seven_fang_men_zi(self, molding_card_list, hand_card_list):
        #   已打出牌型中门子的数量
        molding_num = 0
        if molding_card_list:
            molding_num = len(molding_card_list)

        #   手牌中坎牌
        shoupai_kanpai = [i for i in hand_card_list if hand_card_list.count(i) == 3]
        for i in shoupai_kanpai:
            if i in hand_card_list:
                hand_card_list.remove(i)
        print(shoupai_kanpai, len(hand_card_list), hand_card_list)
        #   坎牌数目
        shoupai_kanpai_num = len(list(set(shoupai_kanpai)))
        print("shoupai_kanpai_num: %s" % shoupai_kanpai_num)
        print("-----------------------------------------")
        print()
        kanpai_huxi = shoupai_kanpai_num * 3
        #   手牌中绞牌
        _dict = {}
        for i in hand_card_list:
            if i[0] not in _dict:
                _dict[i[0]] = 1
            else:
                _dict[i[0]] += 1

        shoupai_jiaopai = [k for k, v in _dict.items() if v == 3]

        for i in shoupai_jiaopai:
            if i[0] in hand_card_list:
                hand_card_list.remove(i)

        for i in shoupai_jiaopai:
            if i[0] in hand_card_list:
                hand_card_list.remove(i)

        print(shoupai_jiaopai, len(hand_card_list), hand_card_list)

        #   绞牌数目
        shoupai_jiaopai_num = len(shoupai_jiaopai)
        print("shoupai_jiaopai_num: %s" % shoupai_jiaopai_num)
        print("-----------------------------------------")
        print()

        #   手牌对子
        shoupai_duizi = [i for i in hand_card_list if hand_card_list.count(i) == 2]

        #   手牌对子数目
        shoupai_duizi_num = len(list(set(shoupai_duizi)))
        for i in shoupai_duizi:
            if i in hand_card_list:
                hand_card_list.remove(i)
        print(shoupai_duizi, len(hand_card_list), hand_card_list)
        print("shoupai_duizi_num: %s" % shoupai_duizi_num)
        print("-----------------------------------------")
        print()

        #   手牌中连牌数目
        shoupai_lianpai_num = 0

        #   获取手牌中连牌数目
        if len(hand_card_list) >= 3:
            index = 1
            result = 0
            shunzi_list = []
            while index <= len(hand_card_list):
                if index % 3 == 0 and result == 0:
                    shunzi_list.append(hand_card_list[index - 3: index])
                    index += 1

                if index != len(hand_card_list):
                    result += self.changeStr(hand_card_list[index]) - self.changeStr(hand_card_list[index - 1]) - 1
                    index += 1
                else:
                    break

            shoupai_lianpai_num = len(shunzi_list)
            print(shunzi_list, len(hand_card_list), hand_card_list)
            print("shoupai_lianpai_num: %s" % shoupai_lianpai_num)
            print("-----------------------------------------")
            print()

        total_7_menzi = molding_num + shoupai_kanpai_num + shoupai_jiaopai_num + shoupai_duizi_num + shoupai_lianpai_num
        # total_hu_xi = kanpai_huxi
        print("total_7_menzi: %s" % total_7_menzi)
        return total_7_menzi

    #   操作分发
    def do_fun_dispense(self):
        pass

    #   胡牌检查
    def _hupai_fun(self, molding_card_data, hand_cards_list):
        seven_fang_men_zi = self.check_seven_fang_men_zi(molding_card_data, hand_cards_list)
        return seven_fang_men_zi

    #   碰牌检查
    def _pengpai_fun(self):
        pass

    #   出牌检查
    def _chupai_fun(self):
        pass

    #   吃牌检查
    def _chipai_fun(self):
        pass

    #   过牌检查
    def _guopai_fun(self):
        pass

    #   判断做的操作与手上的牌型是否符合，
    #   current_fun_index: 当前操作的类型, can_do_data：能进行操作返回的数据, _cards：牌
    def judge_cards_conform(self, molding_card_data, can_do_data, hand_cards_list):
        last_card = None
        # total_hu_xi = can_do_data['zong_hu_xi']
        seven_fang_men_zi = None
        for i in can_do_data:
            if i == "last_push_card":
                last_card = i[1]
            if i == "is_chu_card":
                self.Chu_Pai["canDo"] = can_do_data[i][1]
            if i == "is_peng_card":
                self.Peng_Pai["canDo"] = can_do_data[i][1]
            if i == "is_chi_card":
                self.Chi_Pai["canDo"] = can_do_data[i][1]
            if i == "is_hu_card":
                self.Hu_Pai["canDo"] = can_do_data[i][1]

        #   胡牌
        if self.Hu_Pai['canDo'] == 1:
            total_hu_xi = 15
            total_7_menzi = self._hupai_fun(molding_card_data, hand_cards_list)
            if total_hu_xi < 15 and total_7_menzi != 7:
                return False, []
            else:
                return True, []

        #   碰牌
        if self.Peng_Pai['canDo'] == 1:
            #   判断手牌中对子与上次出牌相同
            last_card = can_do_data['last_push_card'][1]

            dui_zi = [i for i in hand_cards_list if hand_cards_list.count(i) >= 2]

            if last_card in dui_zi:
                return True, dui_zi
            else:
                return False, dui_zi

        #   出牌
        if self.Chu_Pai['canDo'] == 1:
            last_card = can_do_data['last_push_card'][1]
            #   判断手牌中的单牌
            _dict = {}
            for i in hand_cards_list:
                if i not in _dict:
                    _dict[i] = 1
                else:
                    _dict[i] += 1

            send_card = [k for k, v in _dict.items() if v == 1]

            # 当有单牌的时候,判断单牌是否在顺子里面
            if len(send_card) >= 1:
                #   获取手牌中连牌数目
                shunzi_list = []
                if len(hand_cards_list) >= 3:
                    index = 1
                    result = 0
                    while index <= len(hand_cards_list):
                        if index % 3 == 0 and result == 0:
                            shunzi_list.append(hand_cards_list[index - 3: index])
                            index += 1

                        if index != len(hand_cards_list):
                            result += self.changeStr(hand_cards_list[index]) - self.changeStr(
                                hand_cards_list[index - 1]) - 1
                            index += 1
                        else:
                            break
                #   如果单牌在顺子里面，则去除这个牌在出牌序列
                if len(shunzi_list) > 0:
                    for i in shunzi_list:
                        for j in send_card:
                            if j in i:
                                send_card.remove(j)

            #   没有单牌的时候，拆除一个对子
            else:
                send_card = [k for k, v in _dict.items() if v == 2]
            return True, send_card[0][:2]

        #   吃牌
        if self.Chi_Pai['canDo'] == 1:
            #   判断手牌中有没有符合吃牌规则的牌
            last_card = can_do_data['last_push_card'][1]
            if "T" in last_card:
                last_card = last_card.replace("T", "10")
            print(u"上家打出的牌： %s, 手牌: %s" % (last_card, hand_cards_list))
            chipai_list = []
            for i in hand_cards_list:
                if "T" in i:
                    TEN = i.replace('T', '10')
                    print(u"存在T的数值: %s, TEN: %s" % (i, TEN))
                    if -2 <= int(TEN[: len(TEN) - 2]) - int(last_card[0]) <= 2:
                        chipai_list.append(i)
                else:
                    print(u"非T的数值: %s" % i)
                    if -2 <= int(i[: len(i) - 2]) - int(last_card[0]) <= 2:
                        chipai_list.append(i)

            chipai_list = list(set(chipai_list))
            print("last card: %s, list: %s" % (last_card, chipai_list))
            #   不重复的牌
            _NotRepeatList = []

            for i in chipai_list:
                if i not in _NotRepeatList and len([j for j in _NotRepeatList if i[0] == j[0]]) == 0:
                    _NotRepeatList.append(i)

            _NotRepeatList = list(set(_NotRepeatList))
            if len(_NotRepeatList) < 3:
                print(u"吃牌队列长度不够，不可吃牌..")
                return "guo", []
            else:
                print("-------------------------")
                print(_NotRepeatList)
                for i in _NotRepeatList:
                    if i[0] == last_card[0]:
                        _NotRepeatList.remove(i)
                _NotRepeatList.append(last_card)
                _NotRepeatList.sort()
                print("last card: %s, _NotRepeatList: %s, hand_card：%s" % (last_card, _NotRepeatList, hand_cards_list))
                index = _NotRepeatList.index(last_card)
                real_list = []

                for i in _NotRepeatList:
                    if "T" in i:
                        _NotRepeatList.remove(i)
                        element = "10"+i[1:]
                        _NotRepeatList.append(element)
                print("_NotRepeatList: %s" % _NotRepeatList)
                #   根据上家打的牌来判断这场牌位于自己手牌中的第几张，并判断有没有顺子
                if index != 0 and index != len(_NotRepeatList) - 1:
                    print(u"牌在中间")
                    print(int(_NotRepeatList[index][0]) - int(_NotRepeatList[index - 1][0]))
                    print("======")
                    print(int(_NotRepeatList[index + 1][0]) - int(_NotRepeatList[index][0]))
                    if int(_NotRepeatList[index][0]) - int(_NotRepeatList[index - 1][0]) == int(
                            _NotRepeatList[index + 1][0]) - int(_NotRepeatList[index][0]):
                        print(u"中间牌获取成功")
                        real_list.append(_NotRepeatList[index - 1])
                        real_list.append(_NotRepeatList[index + 1])
                elif index == 0:
                    print(u"牌在初始")
                    if int(_NotRepeatList[index + 1][0]) - int(_NotRepeatList[index][0]) == int(
                            _NotRepeatList[index + 2][0]) - int(_NotRepeatList[index + 1][0]):
                        print(u"头牌获取成功")
                        real_list.append(_NotRepeatList[index + 1])
                        real_list.append(_NotRepeatList[index + 2])

                elif index == len(_NotRepeatList) - 1:
                    print(u"牌在尾部")
                    if int(_NotRepeatList[index][0]) - int(_NotRepeatList[index - 1][0]) == int(
                            _NotRepeatList[index - 1][0]) - int(_NotRepeatList[index - 2][0]):
                        print(u"尾牌获取成功")
                        real_list.append(_NotRepeatList[index - 1])
                        real_list.append(_NotRepeatList[index - 2])
                else:
                    pass
                print(u"吃牌数据： %s" % real_list)

                for i in real_list:
                    if "10" in i:
                        real_list.remove(i)
                        element = 'T'+i[2:]
                        real_list.append(element)

                if len(real_list) >= 2 and len(real_list) % 2 == 0:
                    print("true....")
                    return True, real_list
                else:
                    print("false....")
                    return "guo", []

        #   过牌
        if self.Guo_Pai['canDo'] == 1:
            return True, []

#   协议说明
class DefineProtocol:
    """
        客户端发包CS
    """
    PAO_HU_ZI_CS_LOGIN = 1000  # 登录
    # PAO_HU_ZI_CS_REQUEST_ENTER_ROOM = 1001  # 请求进入房间

    # PAO_HU_ZI_CS_LEAVE_ROOM = 1004  # 离开房间

    # PAO_HU_ZI_CS_REQUEST_READY = 1006   # 请求准备

    PAO_HU_ZI_CS_CREATE_ROOM = 1010  # 创建房间

    PAO_HU_ZI_CS_DISSOLVE_ROOM = 1018  # 解散房间
    PAO_HU_ZI_CS_CHOSE_DISSOLVE_ROOM = 1020  # 选择解散房间
    PAO_HU_ZI_CS_CHECK_IN_CLUB = 1041  # 检查是否在俱乐部里面
    PAO_HU_ZI_CS_GAME_SERVER_TRUSTEESHIP = 1053  # 游戏服托管
    PAO_HU_ZI_CS_MAKE_CARDS_TYPE = 1057  # 测试专用做牌
    PAO_HU_ZI_CS_CREATED_GAME_LIST = 1100  # 已创建的比赛
    PAO_HU_ZI_CS_CLUB_GAME_LIST = 1101  # 所在俱乐部比赛
    PAO_HU_ZI_CS_CHAT_SEND_CONTENT = 2001  # 发聊天内容
    PAO_HU_ZI_CS_CHAT_SEND_CONTENT_WITH_FACE = 2009  # 发表情




    """
        服务器回包SC
    """
    PAO_HU_ZI_SC_LOGIN = 1000  # 登录
    # PAO_HU_ZI_SC_REQUEST_ENTER_ROOM = 1103 # 请求进入房间

    PAO_HU_ZI_SC_ROOM_SNAPSHOT = 1002  # 获取房间所有玩家信息
    # PAO_HU_ZI_SC_DESKTOP_SNAPSHOT = 1003  # 桌面快照

    # PAO_HU_ZI_SC_LEAVE_ROOM = 1004  # 离开房间
    PAO_HU_ZI_SC_ENTER_ROOM_PLAYER_INFO = 1005  # 通知进入房间玩家信息

    PAO_HU_ZI_SC_GAME_START = 1007  # 游戏开始

    #------------------------------------------------------------------
    majiang_paohuzi_on_enter_room = 1103  # 请求进入房间
    majiang_paohuzi_create_room = 1001  # 进入房间
    majiang_paohuzi_join_house = 1004  # 加入进入房间
    majiang_paohuzi_user_info = 1003   # 获取房间所有玩家桌面信息
    majiang_paohuzi_sc_request_ready = 1005  # 请求准备
    majiang_paohuzi_which_player_can_do = 5016  # 广播谁可以做什么操作
    majiang_paohuzi_player_hand_cards = 5002 #广播玩家手上的牌数
    majiang_paohuzi_reconnect = 1006 # 重新连接
    majiang_paohuzi_end_hu = 5018 #最后胡牌
    majiang_paohuzi_now_operation_user = 5003 #广播当前操作玩家
    majiang_paohuzi_game_over = 1013 #房间已解散
    majiang_paohuzi_small_settle_accounts = 5019 #小局结算
    majiang_paohuzi_supplement_card_target_user = 5006 #广播补牌消息给其它玩家
    majiang_paohuzi_broadcast_ti = 5007 #广播提牌操作
    majiang_paohuzi_broadcast_wei = 5008 #广播偎牌操作
    majiang_paohuzi_operation_hu = 5009 #胡牌
    majiang_paohuzi_broadcast_pao = 5010 #广播跑牌操作
    majiang_paohuzi_operation_peng = 5011 # 碰牌
    majiang_paohuzi_operation_chu = 5013 #出牌
    majiang_paohuzi_operation_guo = 5014 #过牌
    majiang_paohuzi_card_region_is_chu = 5015 #广播将展示的牌移到出牌区域
    majiang_paohuzi_create_error_code = 1102  # 创建房间失败的错误码
    majiang_paohuzi_departure_room_data = 1009 #玩家离开房间
    majiang_paohuzi_supplement_card = 5005     #补牌
    majiang_paohuzi_dou_liu_zi = 5022     #逗溜子
    majiang_paohuzi_move_card = 5021      #将牌移到手牌中
    majiang_paohuzi_request_function = 5012  #吃牌返回数据
    majiang_paohuzi_disconnection_reconnect = 5017  # 断线重连桌面数据

    #--------------------------------------------------------------
    majing_big_settle_accounts = 1035 #麻将大局清算
    majiang_pure_WANG = 1080 #服务器广播正王和纯王
    majiang_reconnection = 1063 # 断线重连时
    majiang_fengdong_status = 1092 #封东状态
    majiang_small_settle_accounts = 1031 #麻将小局结算
    majiang_hand_cards = 1034 #广播玩家手上的牌数
    majiang_next_out_card_player = 1021 # 广播下一个出牌玩家
    majiang_ting_card = 1041 #服务器通知是否听牌
    majiang_deal_card = 1020 #服务器发牌
    majiang_who_can_do = 1022 #通知用户做相应的操作
    majiang_out_card = 1023 #用户出牌操作返回数据
    majiang_peng_card = 1024 #碰牌操作返回数据
    majiang_gang_card = 1025 #用户杠牌操作返回数据
    majiang_zi_mo_hu = 1026 #自摸胡操作返回数据
    majiang_cancel_operation = 1027 #取消操作
    majiang_notification_touched_a_card = 1028 #通知玩家摸牌
    majiang_hu_card = 1029 # 胡牌数据
    majiang_chi_card = 1036 #吃牌数据
    majiang_player_supplement_card = 1037 #用户补张
    majiang_notification_Gang_later_operation = 1038 #通知杠后补张操作
    majiang_supplement_gang = 1039 #补杠
    majiang_broadcast_supplement_card = 1040 #广播补牌
    majiang_broadcast_operation_Ningxiang_gang = 1081  #宁乡开王麻将杠牌操作广播
    majiang_HDMY_operation = 1044 #海底漫游
    majiang_zha_niao = 1030     #扎鸟
    majiang_broadcast_get_card = 1033 #广播哪个玩家摸牌
    majiang_broadcast_HDL = 1045 #服务器广播海底牌
    majiang_make_cards_type = 65534 # 测试做牌专用
    majiang_broadcast_mingtang_info = 1050 #广播名堂信息
    majiang_broadcast_mingtang_operation = 1042 #服务器通知起手明堂操作
    majiang_dissolve = 1012 #麻将解散

    #----------------------------------------------------------
    majiang_run_fast_deal_card = 2520    #发牌
    # majiang_run_fast_out_card_player = 1021        #广播下一个出牌玩家
    # majiang_run_fast_who_can_do = 1022             #通知用户做相应的操作
    majiang_run_fast_out_card = 2523                 #出牌
    majiang_run_fast_small_settle_accounts = 2531    #小局结算
    majiang_run_fast_reconnection = 2532             #断线重连
    majiang_run_fast_big_settle_accounts = 2535      #大局结算
    majiang_run_fast_broadcast_bomb = 2536           #服务器广播炸弹结算
    majiang_run_fast_query_last_outcard_info = 2537  #查询上一轮出牌信息
    majiang_run_fast_broadcast_PiaoFen = 1061        #服务器通知客户端飘分
    majiang_run_fast_piaofen_info = 1062             #通知每个玩家飘分情况
    majiang_run_fast_return_piaofen_info = 1063      #断线重连时，返回玩家飘分信息












    PAO_HU_ZI_SC_SEND_CARDS = 5001  # 发牌


    PAO_HU_ZI_SC_TOUCH_CARDS = 5004 # 摸牌

    PAO_HU_ZI_SC_TOTAL_SETTLEMENT = 5020    # 总结算
    PAO_HU_ZI_SC_PLAY_GAME_TIMES = 1017 # 广播当前已玩的局数


    PAO_HU_ZI_SC_DISSOLVE_ROOM = 1008  # 解散房间

    PAO_HU_ZI_SC_STEP_OUT_ROOM = 1019  # 暂离房间
    PAO_HU_ZI_SC_SETTLEMENT = 1026  # 小局结算
    # PAO_HU_ZI_SC_ERROR_TIPS = 1027  # 错误提示

    PAO_HU_ZI_SC_RECONNECTION_SERVER_SEND_CARDS = 1035  # 断线重连后服务器推自己手上的牌

    PAO_HU_ZI_SC_NOT_IN_ROOM = 1043  # 不在房间中，不能进行操作
    PAO_HU_ZI_SC_GAME_SERVER_TRUSTEESHIP = 1053  # 游戏服托管
    PAO_HU_ZI_SC_MAKE_CARDS_TYPE = 1057  # 测试专用做牌
    PAO_HU_ZI_SC_CREATED_GAME_LIST = 1100    # 已创建的比赛
    PAO_HU_ZI_SC_CLUB_GAME_LIST = 1101  # 所在俱乐部比赛
    PAO_HU_ZI_SC_CHANGE_GOLD_COINS = 1086  # 金币改变
    PAO_HU_ZI_SC_SERVER_CLOSE = 1998    # 服务器即将关闭

    # PAO_HU_ZI_SC_RECONNECTION = 5017  # 断线重连桌面数据

    PAO_HU_ZI_SC_COMMON_CHAT = 2002     # 广播公聊
    PAO_HU_ZI_SC_CHAT_SEND_CONTENT = 2001  # 发聊天内容
    PAO_HU_ZI_SC_COMMON_CHAT_WITH_FACE = 2010  # 广播公聊 表情
    PAO_HU_ZI_SC_CHAT_SEND_CONTENT_WITH_FACE = 2009  # 发表情
    PAO_HU_ZI_SC_PLAYER_CHANGE_IDENTITY = 10022     # 玩家改变身份
    PAO_HU_ZI_SC_CHANGE_SERVER = 10080  # 切换服务器
    PAO_HU_ZI_SC_CREATE_ROOM_YIYANG = 2029
    PAO_HU_ZI_SC_CAN_MOTION = 2026



#   根据参数数据类型分类
class ProtocolClassify:
    # 根据每个协议实体中参数数据类型划分，纯int32, 纯int16, 纯int64，含有string四类
    protocol_classify = {"INT32": [DefineProtocol.PAO_HU_ZI_SC_LOGIN, DefineProtocol.majiang_paohuzi_reconnect,
                                   DefineProtocol.PAO_HU_ZI_SC_CHANGE_SERVER, ], "INT16": [],
                         "INT64": [DefineProtocol.PAO_HU_ZI_SC_CHANGE_GOLD_COINS, ],
                         "STRING": [DefineProtocol.majiang_paohuzi_create_room,
                                    DefineProtocol.majiang_paohuzi_on_enter_room, ], }

    #   协议号对应的回包处理函数
    protocol_corresponding_function = {DefineProtocol.PAO_HU_ZI_SC_LOGIN: [SCLogin, "sc_login"],
                                       DefineProtocol.PAO_HU_ZI_SC_CHANGE_GOLD_COINS: [SCGoldCoinsChange,
                                                                                       "sc_gold_coins_change"],

                                       # DefineProtocol.PAO_HU_ZI_SC_RECONNECTION: [SCReconnection, "sc_reconnection"],
                                       DefineProtocol.PAO_HU_ZI_SC_CHANGE_SERVER: [SCChangeServer, "sc_change_server"],
                                       DefineProtocol.majiang_paohuzi_create_room: [SCCreateRoom, "sc_create_room"],
                                       # DefineProtocol.PAO_HU_ZI_SC_LEAVE_ROOM: [SCLeaveRoom, "sc_leave_room"],
                                       DefineProtocol.majiang_paohuzi_join_house: [SCjoinRoom, "sc_join_room"],
                                       DefineProtocol.majiang_paohuzi_user_info: [SCAllUserInfo,"sc_all_userInfo"],
                                       DefineProtocol.majiang_paohuzi_player_hand_cards: [SCPlayerHandCards,"sc_player_hand_cards"],
                                       DefineProtocol.majiang_paohuzi_end_hu: [SCEndHuCard,"sc_end_hu_card"],
                                       DefineProtocol.majiang_paohuzi_now_operation_user: [SCNowOperationUser,"sc_now_operation_user"],
                                       DefineProtocol.majiang_paohuzi_game_over:[SCGameOver,"sc_majiang_game_over"],
                                       DefineProtocol.majiang_paohuzi_small_settle_accounts:[SCSmallSettleAccounts,"sc_small_settle_accounts"],
                                       DefineProtocol.majiang_paohuzi_supplement_card_target_user: [SCSupplementCard,"sc_supplement_card"],
                                       DefineProtocol.majiang_paohuzi_broadcast_ti: [SCBroadcastTi,"sc_broadcast_ti"],
                                       DefineProtocol.majiang_paohuzi_broadcast_wei:[SCBroadcastWei,"sc_broadcast_wei"],
                                       DefineProtocol.majiang_paohuzi_operation_hu: [SCRequestHu,"sc_operation_hu"],
                                       DefineProtocol.majiang_paohuzi_broadcast_pao: [SCBroadcastPao,"sc_broadcast_pao"],
                                       DefineProtocol.majiang_paohuzi_operation_peng: [SCRequestPeng,"sc_operation_peng"],
                                       DefineProtocol.majiang_paohuzi_operation_chu: [SCRequestChu,"sc_paohuzi_operation_chu"],
                                       DefineProtocol.majiang_paohuzi_operation_guo: [SCRequestGuo,"sc_operation_guo"],
                                       DefineProtocol.majiang_paohuzi_card_region_is_chu:[SCCardRegionIsCHU,"sc_card_region_is_chu"],
                                       DefineProtocol.majiang_paohuzi_create_error_code :[SCCreateErrorCode,"sc_create_error_code"],
                                       DefineProtocol.majiang_paohuzi_departure_room_data :[SCRequestDepartureRoom,"sc_departure_room"],
                                       DefineProtocol.majiang_paohuzi_reconnect: [SCReconnect,"sc_reconnect"],
                                       DefineProtocol.majiang_paohuzi_supplement_card: [SCPHZSupplementCard,"sc_paohuzi_supplement"],
                                       DefineProtocol.majiang_paohuzi_dou_liu_zi: [SCPHZDouLiuZi,"sc_paohuzi_dou_liu_zi"],
                                       DefineProtocol.majiang_paohuzi_move_card: [SCPHZMove_Card,"sc_paohuzi_move_card"],
                                       DefineProtocol.majiang_paohuzi_request_function: [SCRequestFunction,
                                                                                      "sc_request_function"],
                                       DefineProtocol.majiang_paohuzi_disconnection_reconnect: [SCMJDisconnectionReconnect,"sc_majiang_disconnection_reconnect"],


                                       DefineProtocol.majiang_dissolve:[SCMajiangDissolve,"sc_majiang_dissolve"],
                                       DefineProtocol.majiang_make_cards_type: [SCMajiangMakeCardsType,"sc_majiang_make_cards_type"],
                                       DefineProtocol.majiang_broadcast_mingtang_info: [SCMajiangBroadcastMingtangInfo,"sc_majiang_mingtang_ingo"],
                                       DefineProtocol.majiang_broadcast_mingtang_operation: [SCMajiangBroadcastMingtangOpreation,"sc_majiang_mingtang_opreation_info"],



                                       DefineProtocol.majing_big_settle_accounts :[SCMajiangBigSettle_accouts,"sc_majiang_big_settle_accounts"],
                                       DefineProtocol.majiang_pure_WANG : [SCMajiangPureWANG,"sc_majiang_pure_wang"],
                                       DefineProtocol.majiang_reconnection : [SCRMajiangReconnection,"sc_majiang_reconnection"],
                                       DefineProtocol.majiang_fengdong_status: [SCMajiangFengDongStatus,"sc_fengdong_status"],
                                       DefineProtocol.majiang_small_settle_accounts: [SCMajiangSmallSettleAccounts,"sc_majiang_small_accounts"],
                                       DefineProtocol.majiang_hand_cards: [SCMajiangHandCards,"sc_hand_cards"],
                                       DefineProtocol.majiang_next_out_card_player: [SCMajiangNextOutCardPlayer,"sc_next_out_card_player"],
                                       DefineProtocol.majiang_ting_card: [SCMajiangTingCard,"sc_ting_card"],
                                       DefineProtocol.majiang_deal_card: [SCMajiangDealCard,"sc_deal_card"],
                                       DefineProtocol.majiang_who_can_do: [SCMajiangWhoCanDo,"sc_majiang_who_can_do"],
                                       DefineProtocol.majiang_out_card: [SCMajiangOutCard,"sc_majiang_out_card"],
                                       DefineProtocol.majiang_peng_card: [SCMajiangPengCard,"sc_majiang_peng_card"],
                                       DefineProtocol.majiang_gang_card: [SCMajiangGangCard,"sc_majiang_gang_card"],
                                       DefineProtocol.majiang_zi_mo_hu: [SCMajiangZiMoHu,"sc_majiang_zi_mo_hu"],
                                       DefineProtocol.majiang_cancel_operation: [SCMajiangCancelOperation,"sc_majiang_cancel_operation"],
                                       DefineProtocol.majiang_notification_touched_a_card: [SCMajiangNotificationTouchedACard,"sc_majiang_notification_touched_a_card"],
                                       DefineProtocol.majiang_hu_card:[SCMajiangHuCard,"sc_majiang_hu_card"],
                                       DefineProtocol.majiang_chi_card: [SCMajiangChiCard,"sc_majiang_chi_card"],
                                       DefineProtocol.majiang_player_supplement_card: [SCMajiangplayerSupplementCard,"sc_majiang_player_supplement_card"],
                                       DefineProtocol.majiang_notification_Gang_later_operation: [SCMajiangNotficationGangLaterOpration,"sc_notification_Gang_later_operation"],
                                       DefineProtocol.majiang_supplement_gang: [SCMajiangSupplementGang,"sc_supplement_gang"],
                                       DefineProtocol.majiang_broadcast_supplement_card: [SCMajiangBroadcastSupplementCard,"sc_broadcast_supplement_card"],
                                       DefineProtocol.majiang_broadcast_operation_Ningxiang_gang: [SCMajiangBroadcastOperationNingxiangGang,"sc_majiang_broadcast_operation_Ningxiang_gang"],
                                       DefineProtocol.majiang_HDMY_operation: [SCMajiangHDMYOperation,"sc_majiang_HDMY_opertion"],
                                       DefineProtocol.majiang_zha_niao: [SCMajiangZhaNiao,"sc_majiang_zhao_niao"],
                                       DefineProtocol.majiang_broadcast_get_card: [SCMajiangBroadcastGetCard,"sc_majiang_broadcast_get_card"],
                                       DefineProtocol.majiang_paohuzi_on_enter_room: [SCMajiangRequestEnterRoom,"sc_majiang_enter_room"],
                                       DefineProtocol.majiang_broadcast_HDL: [SCMajiangBroadcast_HDL,"sc_majiang_broadcast_HDL"],


                                       #------------------------------------------跑得快
                                       DefineProtocol.majiang_run_fast_deal_card: [SCRunFastDealCard,"sc_runfast_deal_card"],
                                       #DefineProtocol.majiang_run_fast_out_card_player: [SCRunFastOutCard_Player,"sc_runfast_out_card_player"],
                                       #DefineProtocol.majiang_run_fast_who_can_do: [SCRunFastWhoCanDo,"sc_runfast_who_can_do"],
                                       DefineProtocol.majiang_run_fast_out_card: [SCRunFastOutCard, "sc_runfast_out_card"],
                                       DefineProtocol.majiang_run_fast_small_settle_accounts: [SCRunFastSmallSettleAccounts,"sc_runfast_small_settle_accounts"],
                                       DefineProtocol.majiang_run_fast_reconnection: [SCRUnFastReconnection,"sc_runfast_reconnection"],
                                       DefineProtocol.majiang_run_fast_big_settle_accounts: [SCRunFastBigSettleAccounts,"sc_runfast_big_settle_accounts"],
                                       DefineProtocol.majiang_run_fast_broadcast_bomb: [SCRunFastBroadcastBomb,"sc_runfast_broadcast_bomb"],
                                       DefineProtocol.majiang_run_fast_query_last_outcard_info: [SCRunFastQueryLastOutcardInfo,"sc_runfast_query_last_outcard_info"],
                                       DefineProtocol.majiang_run_fast_broadcast_PiaoFen: [SCRunFastBroadcast_PiaoFen,"sc_runfast_piaofen"],
                                       DefineProtocol.majiang_run_fast_piaofen_info: [SCRunFastPiaoFenInfo,"sc_runfast_piaofen_info"],
                                       DefineProtocol.majiang_run_fast_return_piaofen_info: [SCRunFastReturnPiaoFenInfo,"sc_runfast_return_piaofen_info"],










                                       DefineProtocol.PAO_HU_ZI_SC_DISSOLVE_ROOM: [SCDissolveRoom, "sc_dissolve_room"],
                                       # DefineProtocol.PAO_HU_ZI_SC_DISSOLVE_ROOM: [SCLeaveRoom, "sc_leave_room"],


                                       DefineProtocol.PAO_HU_ZI_SC_GAME_SERVER_TRUSTEESHIP: [SCTrusteeship,
                                                                                             "sc_trusteeship"],
                                       # DefineProtocol.PAO_HU_ZI_SC_DESKTOP_SNAPSHOT: [SCDesktopSnapshot,
                                       #                                                "sc_desktop_snapshot"],
                                       DefineProtocol.PAO_HU_ZI_SC_ROOM_SNAPSHOT: [SCRoomSnapshot, "sc_room_snapshot"],
                                       DefineProtocol.PAO_HU_ZI_SC_ENTER_ROOM_PLAYER_INFO: [SCEnterRoomPlayerInfo,
                                                                                            "sc_enter_room_player_info"],
                                       DefineProtocol.majiang_paohuzi_sc_request_ready: [SCRequestReady, "sc_request_ready"],
                                       DefineProtocol.PAO_HU_ZI_SC_PLAY_GAME_TIMES: [SCPlayGameTimes,
                                                                                     "sc_play_game_times"],
                                       DefineProtocol.PAO_HU_ZI_SC_NOT_IN_ROOM: [SCNotInRoom, "sc_not_in_room"],
                                       DefineProtocol.PAO_HU_ZI_SC_SERVER_CLOSE: [SCServerClose, "sc_server_close"],

                                       DefineProtocol.PAO_HU_ZI_SC_GAME_START: [SCGameStart, "sc_game_start"],
                                       DefineProtocol.PAO_HU_ZI_SC_SEND_CARDS: [SCSendCards, "sc_send_cards"],
                                       DefineProtocol.PAO_HU_ZI_SC_TOUCH_CARDS: [SCTouchCards, "sc_touch_cards"],
                                       DefineProtocol.majiang_paohuzi_which_player_can_do: [SCPlayerCanDo,
                                                                                         "sc_paohuzi_player_can_do"],


                                       DefineProtocol.PAO_HU_ZI_SC_TOTAL_SETTLEMENT: [SCTotalSettlement,
                                                                                      "sc_total_settlement"],
                                       DefineProtocol.PAO_HU_ZI_SC_COMMON_CHAT: [SCCommonChat, "sc_common_chat"],
                                       # DefineProtocol.PAO_HU_ZI_SC_ERROR_TIPS: [SCErrorTips, "sc_error_tips"],
                                       DefineProtocol.PAO_HU_ZI_CS_CHAT_SEND_CONTENT: [SCChat, "sc_chat"],
                                       DefineProtocol.PAO_HU_ZI_CS_CHAT_SEND_CONTENT_WITH_FACE: [SCChatFace,
                                                                                                 "sc_chat_face"],

                                       DefineProtocol.PAO_HU_ZI_SC_COMMON_CHAT_WITH_FACE: [SCCommonChatWithFace,
                                                                                           "sc_common_chat_with_face"],
                                       DefineProtocol.PAO_HU_ZI_SC_MAKE_CARDS_TYPE: [SCMakeCardsType,
                                                                                     "sc_make_cards_type"],


                                       DefineProtocol.PAO_HU_ZI_SC_CREATED_GAME_LIST: [SCCreatedGameList,
                                                                                       "sc_created_game_lisst"],
                                       DefineProtocol.PAO_HU_ZI_SC_CLUB_GAME_LIST: [SCClubGameList,
                                                                                    "sc_club_game_list"],
                                       DefineProtocol.PAO_HU_ZI_SC_PLAYER_CHANGE_IDENTITY: [SCPlayerChangeIdentity,
                                                                                            "sc_player_change_identity"],
                                       DefineProtocol.PAO_HU_ZI_SC_CREATE_ROOM_YIYANG: [SCCreateRoom_YiYang,
                                                                                        "sc_createRoom_Yiyang"],


                                       }

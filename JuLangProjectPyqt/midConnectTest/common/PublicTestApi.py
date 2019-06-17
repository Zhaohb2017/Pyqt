#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@ author: guess
@ effect: 业务流程
@ Time : 2018/7/18 13:44
"""
from midConnectTest.common.common_api import *
import logging,time

from collections import Counter
from copy import copy
import itertools
path = "../../log"
#logging.NOTSET #filename=path+'/new.log', # filemode='w', #  filename=path+'/new.log',filemode='w',
logging.basicConfig(level=logging.NOTSET,

                    format='%(asctime)s - %(filename)s - %(funcName)s : %(levelname)s  %(message)s')
logger = logging.getLogger(__name__)




class PublicTestApi():
    def __init__(self,version,different="local"):
        super(PublicTestApi,self).__init__()
        self.version = version
        self.different=different
        self.huang_pai = 0  # 荒局数  默认1
        self.user_info = {}  # 座位号信息
        self.all_pai_data = {}  # 所有玩家牌数据
        self.DECLARER_who_can_do_operate = None  # 庄家可以进行的操作
        self.many_users = []  # 所有进入房间的用户
        self.out_card_list= [] #出牌的数据
        self.out_card = None
        self.all_users_maturity_cards = []  # 所有用户成熟的牌型
        self.who_can_do = {}
        self.phz_who_can_do = {} #跑胡子谁能操作
        self.peng_status = None  # 碰牌状态
        self.pao_status = None #跑牌状态
        self.hu_status = "" #跑牌状态
        self.copy_who_can_do = "" #复制谁做什么操作
        self.huang_status = None
        self.majiang_who_can_do = {} # 麻将谁能操作什么
        self.majiang_who_can_do_data = {}  #麻将用户能做什么操作数据
        self.chu_card = ["1S", "1B", "3B", "1S", "1B", "3B"]  #牌数据
        self.pause = False  # self.chu_card 出完
        self.result_list = []

    #   获取当前时间戳
    def get_current_time(self):
        return time.time()

    #   多人登录并检测
    def api_login_more_with_check(self, login_account_list):
        player_list = []
        for i in login_account_list:
            player = CommonApi(mid=i,versions=self.version,different=self.different)
            #   登录
            player.phz_login()
            #   设定开始时间
            startTime = self.get_current_time()
            #   进行登录检测，超过5秒直接失败
            while not player.logined:
                if time.time() - startTime > 5:
                    break
                time.sleep(0.5)
            if player.logined:
                player_list.append(player)
        #   当玩家对象与登录人数一致时，说明登录成功
        if len(player_list) == len(login_account_list):
            logging.info("多人登录成功...")
            if len(login_account_list) is 2:
                for i in range(len(login_account_list)):
                    self.many_users.append(player_list[i])
                return player_list[0], player_list[1]
            elif len(login_account_list) is 3:
                for i in range(len(login_account_list)):
                    self.many_users.append(player_list[i])
                return player_list[0] ,player_list[1], player_list[2]
            elif len(login_account_list) is 4:
                for i in range(len(login_account_list)):
                    self.many_users.append(player_list[i])
                return player_list[0], player_list[1], player_list[2], player_list[3]

            return
        else:

            raise logging.error("多人登录失败...")



    #   创建房间
    def api_create_room_with_check(self, player, create_room_data, isCheck=True):#
        player.phz_create_room(create_room_data)
        if isCheck:
            startTime = self.get_current_time()
            while len(player.sc_create_room_data) is 0:
                if time.time() - startTime > 5:
                    break
                time.sleep(0.1)
        else:
            time.sleep(3)

        if not len(player.sc_create_room_data) is 0:
            logging.info("%s 创建房间成功...,房间号: %s" % (player.user_mid, player.room_id))
            return player.room_id
        else:
            raise Exception("创建房间失败->>%s"%player.room_id)




    #   解散房间
    def api_dissolve_room_with_check(self, player):
        player.qs_dissolve_room()

        startTime = self.get_current_time()
        while not player.dissolve_room_state:
            if time.time() - startTime > 10:
                break
            time.sleep(0.1)

    #   多人申请加入房间
    def api_enter_room_more_with_check(self, player_list, room_id, isCheck=True):
        if type(player_list) is not list:
            raise logging.error("你调用错接口了...此接口是调用多人加入房间的")
        #   结果准备
        result_list = []
        update_dataa = {"room_id": room_id}

        #   循环申请加入房间及判断
        for player in player_list:
            logging.info("玩家: %s加入房间"%player.user_mid)
            player.phz_requests_enter_room(update_dataa)

            result_list.append(player)

        if len(result_list) is len(player_list):
            logging.info("%s个人加入房间成功..." % len(player_list))
            return True
        else:
            return False
            # raise Exception ("%s个人加入房间失败..." % len(result_list))

    #多人准备

    def api_ready_game(self, obj_list, isCheck=True) -> object:
        self.huang_status = False # 玩家准备荒庄状态为false
        result_list = []
        for i in obj_list:
            #   进行准备
            logging.info("玩家: %s 进行准备" % i.user_mid)
            for seatid, user in i.user_info.items():
                # print(i.user_info,"222222222222")
                self.user_info[seatid] = user
            self.result_list = result_list
            i.phz_ready_game()
             # 进行检查
            if isCheck:
                time_1 = 0
                while len(i.request_ready_data) is 0:
                    if time_1 > 10:
                        break
                    time_1 += 1
                    time.sleep(0.5)
                if  not len(i.request_ready_data) is 0:
                    logging.info("玩家准备-->>Success")

        player_cards_dict = {}
        time.sleep(3)
        for player in obj_list:
            player_cards = player.sc_send_cards_data
            player_cards_dict[player.account] = player_cards
        self.all_pai_data = player_cards_dict

    # 校验重复值
    def checkout_repetition(self,value):
        from collections import Counter
        if type(value) is list:
            cou = Counter(value)
            for k, v in dict(cou).items():
                if v >= 2:
                    return True
        else:
            raise Exception("传值错误")
        return





    #玩家请求离开房间
    def api_request_departure_room(self,player):
        player.qs_requests_departure_room()

    #用户创建房间并且用户加入
    def api_createRoom_and_enterRoom(self,player,user,create_room_data,player_list,):#ist,clear_list
        room_id = self.api_create_room_with_check(player, create_room_data)
        self.api_enter_room_more_with_check(player_list, room_id)
        time.sleep(2)
        print("房间ID: ",room_id)
        if user.join_room_status == False:
            # clear_data(instantiation=ist, user_list=clear_list)
            room_id = self.api_create_room_with_check(player, create_room_data)
            self.api_enter_room_more_with_check(player_list, room_id)
            print("房间ID: ", room_id)
        print()



    #   碰牌并校验
    def api_send_card_with_Peng(self, player,card):
        time.sleep(3)

        while len(player.sc_play_can_do_data) is 0:
            time.sleep(0.1)
        xuliehao = player.sc_play_can_do_data['operation_sign'][1][:-1]

        send_card_data = {"operation_number": xuliehao,"peng_card":card[:-1]}

        #  碰牌
        player.qs_request_peng(send_card_data)
        while len(player.player_broadcast_peng) is 0:
            time.sleep(0.002)
        if player.player_broadcast_peng["seat_id"][1] == -1:
            raise Exception("碰牌失败!")
        else:
            logging.info("碰牌成功")





    #   过牌并校验
    def api_send_card_with_Guo(self, player, isCheck=True):
        time.sleep(2)

        xuliehao = player.sc_play_can_do_data['operation_sign'][1][:-1]
        send_card_data = {"operation_number": xuliehao}
        player.qs_request_guo(send_card_data)

        check_result = None
        if isCheck:
            startTime = self.get_current_time()
            while len(player.operation_guo_data) is 0:
                if self.get_current_time() - startTime > 5:
                    break
                time.sleep(0.1)
            if len(player.operation_guo_data) is not 0:
                time.sleep(1)
                check_result = True
        if check_result is not None:
            if player.operation_guo_data["error_code"][1] == 0:
                logging.info("%s : 过牌成功"%player.account)
                return True
            else:
                if player.operation_guo_data["error_code"][1] == -1:
                    raise Exception("过牌失败!--->>%s"%player.operation_guo_data)
        return

    #   吃牌并校验
    def api_send_card_with_Chi(self, player,chi_card,group_card,card_type,card_list,card_list_1=None):
        time.sleep(3)
        send_card_data = None

        xuliehao = player.sc_play_can_do_data['operation_sign'][1][:-1]
        if group_card == 1:
            send_card_data = {"operation_number":xuliehao,"chi_card":chi_card,
                          "group_card":group_card,"card_type":card_type,
                          "card_list":card_list
                          }
        elif group_card == 2:
            send_card_data = {"operation_number": xuliehao, "chi_card": chi_card,
                              "group_card": group_card, "card_type": card_type,
                              "card_list": card_list,"card_type_1":card_type,
                              "card_list_1":card_list_1
                              }
        #  吃牌
        player.phz_send_cards(send_card_data)
        while len(player.sc_request_function_data) is 0 :
            time.sleep(0.02)




    #   胡牌并校验
    def api_send_card_with_Hu(self, player):
        # print("1111",player.account)
        while len(player.sc_play_can_do_data) is 0:
            time.sleep(0.2)

        xuliehao = player.sc_play_can_do_data['operation_sign'][1][:-1]
        send_card_data = {"operation_number": xuliehao}
        #  胡牌
        player.qs_request_hu(send_card_data)
        time.sleep(2)
        if len(player.end_hu_card_data) != 0:
            logging.info("胡牌成功")
        else:
            if len(player.end_hu_card_data) == 0:
                logging.error("胡牌失败!")
            elif len(player.operation_hu_data) !=0:
                logging.error("胡牌失败,%s"%player.operation_hu_data)

    #出牌
    def api_send_card_with_Chu(self, player, card,isCheck=True):
        time.sleep(3)
        xuliehao = player.sc_play_can_do_data['operation_sign'][1][:-1]

        send_card_data = {"operation_number":xuliehao,"chu_card":card}
         #出牌
        player.qs_request_chu(send_card_data)
        #  检查结果
        check_result = None
        if isCheck:
            startTime = self.get_current_time()
            while len(player.operation_chu_data) is 0:
                if self.get_current_time() - startTime > 5:
                    break
                time.sleep(0.1)
            if len(player.operation_chu_data) is not 0:
                time.sleep(1)
                check_result = True
        if check_result is not None:
            error_code = player.operation_chu_data["error_code"][1]["error_code"]
            if error_code < 0:
                raise Exception("出牌:%s 失败!--->>%s" % (card, player.operation_chu_data))
            else:
                logging.info("出牌: %s -->>success" % card)
                self.out_card = card
                return True
        return




    def api_majiang_chu_card(self, player, card ):
        xuliehao = player.majiang_who_can_do_data['operation_number'][1][:-1]
        send_card_data = {"operation_number": xuliehao, "card": card}
        print("发送数据",send_card_data)
        player.qs_majiang_out_card(send_card_data)
        while len(player.majiang_out_card) is 0:
            time.sleep(0.02)
        if player.majiang_out_card['seat_id'][1] == -1 :
            raise Exception("出牌失败 !")
        player.majiang_out_card.clear()

    def api_majiang_peng_card(self, player ):
        xuliehao = player.majiang_who_can_do_data['operation_number'][1][:-1]
        send_card_data = {"operation_number": xuliehao}
        player.qs_majiang_peng_card(send_card_data)

    def api_majiang_gang_card(self, player, card):
        xuliehao = player.majiang_who_can_do_data['operation_number'][1][:-1]
        send_card_data = {"operation_number": xuliehao, "card": card}
        player.qs_majiang_gang_card(send_card_data)


    def api_majiang_supplement_card(self, player, card):
        xuliehao = player.majiang_who_can_do_data['operation_number'][1][:-1]
        send_card_data = {"card": card, "operation_number": xuliehao }
        player.qs_majiang_supplement_card(send_card_data)


    def api_majiang_hu_card(self, player):
        xuliehao = player.majiang_who_can_do_data['operation_number'][1][:-1]
        send_card_data = {"operation_number": xuliehao}
        player.qs_majiang_hu_card(send_card_data)

    def api_majiang_guo_card(self,player):
        xuliehao = player.majiang_who_can_do_data['operation_number'][1][:-1]
        send_card_data = {"operation_number": xuliehao}
        player.qs_majiang_guo_card(send_card_data)
        while len(player.majiang_cancel_data) is 0:
            time.sleep(0.02)
        if player.majiang_cancel_data["error_code"][1] != 0:
            raise Exception("过牌失败! ")



    def api_majiang_auto_operation_card(self,Capable_player,user_list):
        for operation_user , operation_motion in Capable_player.items():
            player = user_list[int(operation_user) - 1]
            if operation_motion == "hu":
                self.api_majiang_hu_card(player=player)

    def api_majiang_mingtang_opreation(self,player,sign,mingtang_type):
        mingtang_opreation_data = {"operation_number":sign,"mingtang_type":mingtang_type}
        player.majiang_mingtang_opreation(mingtang_opreation_data)



    def api_runfast_out_card(self,player,card_num,out_card):
        time.sleep(2)
        if len(player.majiang_who_can_do_data) is 0:
            time.sleep(5)
        serial_number = player.majiang_who_can_do_data['operation_number'][1][:-1]
        send_data = {"operation_number":serial_number,"outcard_num":card_num,"out_card":out_card}

        player.runfast_player_out_card(send_data)

    def runfast_card_data_checkout(self,data):
        card = Counter(data)
        for k,v in card.items():
            if v != 1:
                print("runfast_card_data_checkout---->>",data)
                return k
        return True

    def api_piao_score_operation(self,user_list,piao_score):
        for user in user_list:
            time.sleep(1)
            operation_number = user.piao_score_data['operation_number'][1][:-1]
            send_data = {"piao_Score":piao_score,"operation_Number":operation_number}
            user.runfast_piao_score(send_data)


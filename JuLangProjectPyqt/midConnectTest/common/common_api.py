#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@ author: Hubery
@ create on: 2018/4/26 14:47
@ file: common_api.py
@ site: 
@ purpose: 
"""
import requests
import json,os
import yaml
import time
from midConnectTest.lib.phz.net.connecter import *
from midConnectTest.lib.phz.net.net_unpack import *
import logging


Normal_Test_File_PATH = "../../../../../conf/phz/phz.yml"
AutoTest_File_PATH = "../../conf/phz/phz.yml" #"../../conf/phz/phz.yml"


isAutoTest = True
print("isAutoTest: %s" % isAutoTest)

def get_conf_data():
    # local = os.getcwd()
    _File_PATH = "midConnectTest/conf/majiang/majiang.yml"
    _file_data = open(_File_PATH, 'r', encoding='utf-8')
    conf_data = yaml.load(_file_data)
    _file_data.close()
    return conf_data

def helper_print(account, function_name, protocol_number, data, print_state = False):
    if print_state:
        print("account: %s, protocol_number: %s, %s :" % (
            account, protocol_number, time.strftime("%Y-%m-%d %X", time.localtime())))
        print("%s: %s" % (function_name, data))

class CommonApi:
    def __init__(self, mid,versions,different="local"):
        self.touch_card = ''
        self.sc_club_game_list_data = {}
        self.account = None
        self.versions = versions
        self.different = different
        self.confData = get_conf_data()
        if self.different =="local":
            self.ip = self.confData['server_ip']

            if self.versions == "master":
                self.port = self.confData['server_port_master']
            elif self.versions == "ChangSha":
                self.port = self.confData['server_port_changsha']
            elif self.versions == "ChangDe":
                self.port = self.confData['server_port_changde']
        else:
            if self.different =="test":
                self.ip = self.confData['test_server_ip']
                if self.versions == "master":
                    self.port = self.confData['test_server_port_master']
                elif self.versions == "ChangSha":
                    self.port = self.confData['server_port_changsha']
                elif self.versions == "ChangDe":
                    self.port = self.confData['server_port_changde']


        self.sesskey = None             # 登录唯一标识
        self.user_mid = mid            # 用户编号
        self.user_gp = None             # 用户组
        self.room_id = None             # 创建房间得到的房间ID
        self.user_clubID = None         # 俱乐部ID
        self.conn = None                # 连接器对象
        self.user_current_gold = None   # 用户当前金币数量
        self.last_room_id = None        # 断线重连之前的房间ID
        self.current_fun_index = None   # 操作序列号
        self.can_do_data = None         # 可以做什么操作的数据
        self.current_fun_data = None    # 当前操作返回的结果，包括胡息,座位号,牌内容
        self.total_hu_xi = None         # 总胡息
        self.total_7_men_zi = None      # 七方门子总数
        self.molding_card_list = []     # 已出牌牌型
        self.hand_cards_list = None     # 手牌
        self.logined = False            # 是否登录
        self.isEnterRoom = False        # 是否进入房间了
        self.seat_id = None             # 座位号
        self.get_room_state = False     # 获取房间快照信息
        self.dissolve_room_state = False    # 解散房间标志
        self.isNotMyPart = False        # 广播消息不接收非自身信息
        self.game_start_state = False   # 游戏开始标志
        self.game_over = False          # 小局结束
        self.current_rounds = False     # 判定是谁操作的轮次
        self.in_the_room = False        # 不在房间中
        self.isAgree = False            # 设置解散房间同意状态
        self.last_push_card = None      # 上个玩家出的牌
        self.remain_card = None         #荒牌状态
        self.create_error = None

        self.reconnect_status = False   # 重连状态
        self.sc_now_operation_player = None  #当前操作用户
        self.room_dissolve_status = False    #解散房间状态

        self.join_house_status = False        #加入房间状态
        self.create_room_join_room_status = False #创建房间进入房间状态
        self.operation_sign = None   #操作码
        self.operation_chu_data = {}  #出牌数据
        self.operation_guo_data = {}  # 过牌数据
        self.peng_card = None   # 碰牌数据
        self.operation_hu_data = {} #胡牌数据
        self.player_broadcast_ti = {} # 玩家自动提牌数据
        self.player_broadcast_wei = {} #玩家自动偎牌数据
        self.player_broadcast_pao = {} #玩家自动跑牌数据
        self.player_broadcast_peng = {} #玩家自动碰牌数据
        self.small_settle_accounts_data = {} #小局结算数据
        self.total_settlement_data = {} #大局结算数据
        self.end_hu_card_data = {} #最后胡牌
        self.departure_room_data = {} #离开房间返回数据
        self.is_join_hand_card = None #加入手牌
        self.mo_card = None   #摸牌
        self.chi_card = None  #吃的牌
        self.player_hand_cards = []        #玩家手上的牌
        ##################################################################################
        self.majiang_big_settle_accounts_data = {} #麻将大局结算数据
        self.majiang_pure_wang_data = {} #服务器广播正王和纯王
        self.majiang_small_accounts_data = {} #麻将小局结算数据
        self.majiang_who_can_do_data = {}     #麻将谁能做什么操作data
        self.majiang_who_can_do_operate = {}  #麻将用户能做什么操作
        self.majiang_deal_card_data = {}      #发牌回包数据
        self.majiang_player_cards = {}        #用戶牌數據
        self.majiang_seat_id = None           #可以做操作用户
        self.majiang_mo_card_data = {} #摸牌数据
        self.majiang_out_card = {}     #出牌数据
        self.majiang_cancel_data = {}  #取消数据
        self.majiang_dun_card_zero = None  #墩剩余牌数量
        self.majiang_HDMY = None           #海底漫游
        self.majiang_HDMY_operation_data = {}  #海底漫游操作码
        self.majiang_next_out_card_player = None  #下一个玩家出牌
        self.majiang_dun_card_num = None          #麻將噸上的牌數量
        self.mingtang_opreation = {}              #起手名堂操作
        self.mingtang_status = False              #起手名堂操作状态
        self.mingtang_seatid = None               #名堂操作座位号
        self.room_null = True                     #找不到房间号
        self.join_room_status = None              #加入房间状态


        #   data recv
        self.sc_login_data = {}         # 登录回包数据
        self.sc_change_server_data = {} # 改变服务器回包数据
        self.sc_join_room_data = {}     # 玩家进入房间
        self.sc_chose_dissolve_room_data = {}   # 选择解散房间回包数据
        self.sc_common_chat_data = {}   # 聊天回包数据
        self.sc_create_room_data = {}   # 创建私人房间回包
        self.sc_desktop_snapshot_data = {}  # 桌面快照回包
        self.sc_dissolve_room_data = {} # 解散房间回包数据
        self.sc_enter_room_data = {}    # 进入房间回包数据
        self.sc_error_tips_data = {}    # 错误信息回包
        self.sc_game_start_data = {}    # 游戏开始回包
        self.sc_gold_coins_change_data = {} # 金币改变回包
        self.sc_leave_room_data = {}    # 离开房间回包数据

        self.sc_play_can_do_data = {}   # 能进行什么操作回包
        self.sc_server_close_data = {}  # 服务器即将关闭回包
        self.sc_not_in_room_data = {}   # 不在房间里回包数据
        self.sc_trusteeship_data = {}   # 托管回包
        self.sc_total_settlement_data = {}  # 总结算数据回包
        self.sc_settlement_data = {}    # 小局结算回包数据
        self.sc_request_function_data = {}  # 请求操作回包数据
        self.sc_touch_cards_data = {}   # 摸牌回包数据
        self.sc_send_cards_data = {}    # 发牌数据回包
        self.request_ready_data = {}    # 准备回包数据
        self.sc_play_game_time_data = {}    # 玩过几局游戏回包
        self.sc_room_snapshot_data = {} # 房间快照回包
        self.sc_enter_room_player_info_data = {}    # 进入房间后玩家信息回包
        self.sc_reconnection_data = {}  # 断线重连数据
        self.sc_send_gift_data = {}     # 发送道具回包数据
        self.sc_chat_face_data = {}     # 发送表情回包数据
        self.sc_chat_data = {}          # 发送聊天内容回包数据
        self.sc_common_chat_data_with_chat = {} # 广播公聊表情回包数据
        self.sc_make_cards_type_data = {}   # 做牌回包效果
        self.sc_jingweidu_data = {}     # 经纬度回包
        self.sc_created_game_list_data = {}  # 已创建的比赛回包
        self.sc_reconnection_server_send_cards_data = {}    # 断线重连后服务器推给自己的牌的回包
        self.sc_player_change_identity_data = {}    #   玩家改变身份回包数据
        self.sc_jiatou ={} #加拓
        self.sc_datou_data ={} #打坨
        self.sc_create_room_yiyang_data = {} # 益阳创建房间回包数据
        self.sc_play_can_do_yiyang_data = {} #益阳返回可操作的数据
        self.who_can_do_operate = {}  # 谁可以进行什么操作
        self.mopai_list = [] #摸牌的列表
        self.remain_card_num = None # 剩余多少牌
        self.user_info = {}    #房间用户信息
        #==========================跑得快
        self.runfast_len_card = None
        self.runfast_card_list = []
        self.piao_score_data = []

    #   注册用户
    def phz_get_sseskey(self):
        get_sesskey_data = {'method': 'Amember.login', 'sitemid': self.account, 'site': self.confData['site_id'],
                            'channel': self.confData['channel_id'], 'gp': self.confData['gp_id'], 'pass': ''}

        try:
            #   请求访问
            url = None
            if self.different == "local":
                if self.versions == "master":
                    url = self.confData['php_base_url_master']
                elif self.versions == "ChangSha":
                    url = self.confData['php_base_url_changsha']
                else:
                    url = self.confData['php_base_url_changde']
            else:
                if self.different == "test":
                    if self.versions == "master":
                        url = self.confData['test_php_base_url_master']
                    elif self.versions == "ChangSha":
                        url = self.confData['test_php_base_url_changsha']
                    else:
                        url = self.confData['test_php_base_url_changde']


            call_get_sesskey_data = requests.get(url + json.dumps(get_sesskey_data))
            if call_get_sesskey_data.status_code != 200:
                raise print("PHP connection fail")
            self.sesskey = json.loads(call_get_sesskey_data.text)['data']['sesskey']

            if self.sesskey is None:
                raise print("get sesskey error...")
        except Exception as e:
            raise e

    #   加载用户信息
    def phz_load_user_info(self):
        if self.sesskey is None:
            return
        #	获取用户数据
        get_user_data = {'method': 'Amember.load', 'sesskey': self.sesskey}
        try:
            #   请求访问
            url = None
            if self.different == "local":
                if self.versions == "master":
                    url = self.confData['php_base_url_master']
                elif self.versions == "ChangSha":
                    url = self.confData['php_base_url_changsha']
                else:
                    url = self.confData['php_base_url_changde']
            else:
                if self.different == "test":
                    if self.versions == "master":
                        url = self.confData['test_php_base_url_master']
                    elif self.versions == "ChangSha":
                        url = self.confData['test_php_base_url_changsha']
                    else:
                        url = self.confData['test_php_base_url_changde']

            call_get_user_data = requests.get(url + json.dumps(get_user_data))
            user_data = json.loads(call_get_user_data.text)

            self.user_mid, self.user_gp = user_data['data']['aUser']['mid'], user_data['data']['aUser']['gp']
            print("玩家信息mid: %s" % self.user_mid)

            if self.user_mid is None and self.user_gp is None:
                raise print("get user data error... user_mid: %s, user_gp: %s" % (self.user_mid, self.user_gp))
            return user_data['data']['aUser']['mid']
        except Exception as e:
            raise e

    #   获取用户俱乐部ID
    def phz_get_user_clubId(self):
        url = self.confData['php_get_user_clubId'] % self.user_mid
        try:
            #	请求访问
            call_get_user_data = requests.get(url)
            user_gold_data = json.loads(call_get_user_data.text)
            if user_gold_data['svflag'] is 1:
                self.user_clubID = user_gold_data['data']
                return self.user_clubID
            else:
                return None
        except Exception as e:
            raise e

    #   查询用户当前金币数额
    def phz_query_user_gold(self):
        url = self.confData['php_query_gold_url'] % self.user_mid
        try:
            #	请求访问
            call_get_user_data = requests.get(url)
            user_gold_data = json.loads(call_get_user_data.text)
            self.user_current_gold = user_gold_data['data']
            return self.user_current_gold
        except Exception as e:
            raise e

    #   修改用户金币数额
    def phz_update_user_gold(self,user_mid, update_gold):
        url = self.confData['php_update_gold_url'] % (user_mid, update_gold)
        print("请求增加金币url:",url)
        try:
            #	请求访问
            call_get_user_data = requests.get(url)
            print("增加金币返回数据",call_get_user_data.text)
            # user_gold_data = json.loads(call_get_user_data.text)
            # self.user_current_gold = user_gold_data['data']
            # return self.user_current_gold
        except Exception as e:
            raise e

    #   获取代理商固定玩法和自动开房值
    def phz_get_agent_wanfa_value(self):
        clubID = self.phz_get_user_clubId()
        if len(clubID) <= 0:
            return False
        #	获取用户数据
        clubplay = "3,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,%s,0,club,0,0,0" % clubID[0]
        agent_data  = {"method": "Aactive.saveClubPlays",
             "sesskey": self.sesskey, "clubid": clubID[0],
             "clubplays": clubplay, "type": 0}
        try:
            #	请求访问
            call_get_user_data = requests.get(self.confData['php_cache_wanfa_url'] + json.dumps(agent_data))
            agent_data = json.loads(call_get_user_data.text)
            if agent_data['svflag'] == 1:
                return True
            else:
                return False
        except Exception as e:
            raise e

    #   登录
    def phz_login(self, _CONDICTION= None):
        # self.phz_get_sseskey()
        user_mid=self.phz_load_user_info()
        self.qs_connect()


    #   创建房间
    def phz_create_room(self, update_data):
        print("重连状态--%s"%self.reconnect_status)
        if self.reconnect_status:
            print("房间重连-----解散房间")
            self.qs_dissolve_room()
            time.sleep(5)
            print("解散房间状态: %s"%self.room_dissolve_status)
            if self.room_dissolve_status:
                self.qs_create_room(update_data)
        else:
            self.qs_create_room(update_data)




    #   申请进入房间
    def phz_requests_enter_room(self, update_data):
        self.qs_enter_room(update_data)
        # while not self.isEnterRoom:
        #     time.sleep(0.01)

    #   准备游戏
    def phz_ready_game(self):
        self.qs_request_ready()
        time.sleep(2)
        self.remain_card = False  # 荒牌状态

    #   发聊天内容
    def phz_chat_content(self, update_data):
        self.qs_chat(update_data)

    #   发聊天表情
    def phz_cha_content_with_face(self, update_data):
        self.qs_chat_face(update_data)

    #   发互动道具
    def phz_send_gift(self, update_data):
        self.qs_send_gift(update_data)


    #   开始打牌
    def phz_send_cards(self, update_data):
        #   当到我的轮次进行出牌
        # if self.current_rounds:
        #     # logging.info("当前轮次是: %s" % self.account)
        self.qs_request_function(update_data)

    #   做牌接口
    def majiang_make_cards(self, update_data):
        real_data = {"cards_list": update_data}
        # for k, v in update_data.items():
        #     real_data["cards_list"] += v

        # if len(list(real_data["cards_list"].replace(",", ""))) is not 160:
        #     print("---> 输出的牌型有误，请重新检查后再次输入...")
        #     return

        self.qs_make_cards_type(real_data)

    def qs_connect(self):
        print("socket_Connected is build...")
        print("connect ip is : %s, port: %s" % (self.ip, self.port))
        self.conn = Connecter(self.ip, self.port, self.qs_protocol, self.on_connect_server)
        self.conn.async_connect()



    #   连接成功回调
    def on_connect_server(self):
        print('socket_Connected is success..')
        print("-----------------------------------------------------")

        self.qs_login(self.user_mid, self.user_gp)

    #   发送数据到TCP服务器
    def qs_send_data(self, data):
        self.conn.send_protocol(data)

    #   关闭连接
    def connect_close(self):
        self.conn.connection_close()
        loop_close()

    #   数据处理
    def qs_protocol(self, protocol_num, data):
        p_list = [8001,9999,1087,1105,1130]
        if protocol_num in p_list :
            return


        # 处理包体数据，拿到明文数据，传递给各回包函数中处理
        data_list = ProtocolClassify.protocol_corresponding_function[protocol_num]
        # print("qs_protocol_函数,",protocol_num)
        protocol_entity, funcName = data_list[0], data_list[1]
        real_data = None
        real_data = UnPackData().unpack_data(protocol_num, protocol_entity, data)
        #   如果当前解包数据是无的话，返回
        #         # if real_data is None:
        #                 #     return
        #   获取当前类的方法函数
        class_method = self.__class__.__dict__.get(funcName)
        #   协议处理
        if class_method:
            # 未登录状态在game server中执行登录前置要求
            class_method(self, funcName, protocol_num, real_data)
        else:
            print("it has no function..")

    #   登录
    def qs_login(self, mid, gp):
        update_data = {"mid": mid, "gp": 101}
        print(update_data)
        cs_login_data = CSLogin(update_data)
        self.qs_send_data(cs_login_data.real_data)

    #   登录回包
    def sc_login(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_login_data = data
        if data["error_code"][1] == 0:
            self.logined = True
        if not self.logined:
            return
    # 玩家进入房间，广播该玩家信息
    def sc_join_room(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        # print("%s进入房间，广播该玩家信息-->%s"%(self.account,data))
        self.sc_join_room_data = data
        if len(data) != 0:
            self.join_house_status = True
            self.get_room_state = True

    # #   断线重连
    # def sc_reconnection(self, funcName, protocol_num, data):
    #     # print(self.account, "断线重连", funcName, data)
    #     helper_print(self.account, funcName, protocol_num, data)
    #     # self.sc_reconnection_data = data
    #     # if data['room_id'][1] != 0:
    #     #     self.last_room_id = data['room_id'][1]
    #     #     self.in_the_room = True

    #   修改服务器
    def sc_change_server(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_change_server_data = data

    #   金币
    def sc_gold_coins_change(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_gold_coins_change_data = data

    #   创建私人房间
    def qs_create_room(self, update_data):
        cs_create_room_data = CSCreateRoom(data=update_data)
        self.qs_send_data(cs_create_room_data.real_data)



    #   创建房间回包
    def sc_create_room(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_create_room_data = data
        if not len(data) is 0:
            if len(self.user_info) != 0:
                self.user_info.clear()
            self.user_info[data['seat_id'][1]] = self.account
            self.room_id = data['room_id'][1]
            print("玩家 %s 进入房间: %s"%(data['seat_id'][1],self.room_id))
            self.create_room_join_room_status = True



    #   申请进入房间
    def qs_enter_room(self, update_data):
        # update_data = {"room_id": room_id}
        cs_enter_room_data = CSRequestEnterRoom(update_data)
        self.qs_send_data(cs_enter_room_data.real_data)

    #   请求进入房间回包
    def sc_majiang_enter_room(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)
        if data["error_code"][1] == -1102:
            self.join_room_status = False
            logging.error(" %s: 找不到该房间号"%self.account)


    #  手里的牌
    def sc_player_hand_cards(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        seat_id = data["seat_id"][1]
        hand_cards_num = data["hand_cards_num"][1]
        logging.info(" %s: 座位号,手里的牌: %s 张"%(seat_id,hand_cards_num))

    # 房间已解散
    def sc_majiang_game_over(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        if not len(data) is 0:
            print("房间已解散!")
            self.room_dissolve_status = True

    #玩家请求离开房间
    def qs_requests_departure_room(self):
        cs_departure_room_data = CSRequestDepartureRoom()
        self.qs_send_data(cs_departure_room_data.real_data)

    #玩家离开房间
    def sc_departure_room(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.departure_room_data = data
        print("%s玩家离开房间--->>%s"%(self.account,data))



    # #   请求玩家信息
    # def qs_request_query_info(self):
    #     cs_request_info = CSRequestQueryInfo()
    #     self.qs_send_data(cs_request_info.real_data)

    #   桌面快照回包
    def sc_desktop_snapshot(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_desktop_snapshot_data = data

    #   获取房间所有玩家信息
    def sc_room_snapshot(self, funcName, protocol_num, data):
        helper_print(self.account,funcName ,protocol_num,data)
        # print("获取房间所有玩家信息-->>%s"%data)
        self.sc_room_snapshot_data = data
        # self.get_room_state = True

    #   广播已玩的游戏局数
    def sc_play_game_times(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_play_game_time_data = data

    #   服务器广播进入房间的玩家信息
    def sc_enter_room_player_info(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_enter_room_player_info_data = data

    #   发起准备
    def qs_request_ready(self):
        cs_request_ready_data = CSRequestReady()
        self.qs_send_data(cs_request_ready_data.real_data)


    # 发起胡牌
    def qs_request_hu(self,updata):
        cs_request_hu = CSRequestHu(updata)
        self.qs_send_data(cs_request_hu.real_data)

    # 胡牌操作返回包
    def sc_operation_hu(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)
        self.operation_hu_data = data

    #  发起碰牌
    def qs_request_peng(self,updata):
        cs_request_peng = CSRequestPeng(updata)
        self.qs_send_data(cs_request_peng.real_data)

    # 碰牌回包数据
    def sc_operation_peng(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.player_broadcast_peng = data


    # 发起出牌
    def paohuzi_request_chu(self,updata):
        cs_request_chu = CSRequestChu(updata)
        self.qs_send_data(cs_request_chu.real_data)
    #出牌回包数据
    def sc_paohuzi_operation_chu(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.operation_chu_data = data

    #发起过牌
    def qs_request_guo(self,updata):
        cs_request_guo = CSRequestGuo(updata)
        self.qs_send_data(cs_request_guo.real_data)
    #过牌回包数据
    def sc_operation_guo(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.operation_guo_data = data
    #创建房间失败的错误码
    def sc_create_error_code(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        if data['error_code'][1] == -1100:
            print("房间不足!")
            self.create_error = "房间不足"
        elif data['error_code'][1] == -1101:
            print("%s金币不足!"%self.user_mid)
            self.create_error = "金币不足"







    #广播将展示的牌移到出牌区域
    def sc_card_region_is_chu(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.show_card_region = data['card'][1]


    #   准备回包
    def sc_request_ready(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.request_ready_data = data
        # print("%s:准备返回数据%s"%(self.account,data))

    #小局结算
    def sc_small_settle_accounts(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.small_settle_accounts_data = data


    #广播补牌消息给其它玩家
    def sc_supplement_card(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)

    #广播提牌操作
    def sc_broadcast_ti(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.player_broadcast_ti = data
        logging.info("有玩家提牌")
    #广播偎牌操作
    def sc_broadcast_wei(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.player_broadcast_wei = data
        logging.info("有玩家偎牌")

    #广播跑牌
    def sc_broadcast_pao(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.player_broadcast_pao = data
        logging.info("有玩家跑牌")



    #   游戏开始
    def sc_game_start(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.game_start_state = True
        self.sc_game_start_data = data
        # print("游戏开始包返回数据",data)

    #   发牌回包
    def sc_send_cards(self, funcName, protocol_num, data):
        helper_print(self.user_mid, funcName, protocol_num, data)
        self.player_hand_cards = data['card_'][1]
        logging.info("%s :%s"%(self.user_mid,self.player_hand_cards))



    #最后胡牌
    def sc_end_hu_card(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.end_hu_card_data = data




    #   摸牌回包
    def sc_touch_cards(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.mo_card_seat_id = data['seat_id'][1]
        self.mo_card = data['touch_card'][1]
        self.dun_card_num = data['dun_card_num'][1]
        self.is_join_hand_card = data['is_join_hand_card'][1]
        self.hand_card_num = data['hand_card_num'][1]
        self.is_wei = data['is_wei'][1]

        logging.info(" %s:座位号,摸到的牌是: %s,加入到了手中了: %s(0否 1是),玩家有: %s张牌,是否偎牌: %s(0否 1是)"
                     %(self.mo_card_seat_id,self.mo_card[:-1],self.is_join_hand_card,self.hand_card_num,self.is_wei))
        logging.info(" 墩上牌数余: %s张"%self.dun_card_num)
        if self.dun_card_num == 0:
            self.remain_card = True
        time.sleep(2)


    #   广播谁可以做什么操作
    def sc_paohuzi_player_can_do(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.current_rounds = True
        self.sc_play_can_do_data = data
        seat_id = data["seat_id"][1]
        operation_num = data["operation_num"][1]
        operation_num_info = data["operation_num_info"][1]
        operation_sign = data["operation_sign"][1]
        operation_type = []
        who_can_do_operate = {}
        logging.info("%s operation_numbers: %s"%(self.user_mid,operation_num_info))
            
        # if operation_num != 0:
        #     for key,value in operation_num_info.items():
        #
        #         if key[:14] == "operation_type":
        #             postfix = key[-1]
        #             operation_type.append(value)
        #             if value == 100:
        #                 who_can_do_operate[seat_id] = "chu"
        #                 logging.info("%s :座位号可以进行 '出' 牌操作"%seat_id)
        #             if value == 101:
        #                 who_can_do_operate[seat_id] = "ti"
        #                 logging.info("%s :座位号可以进行 '提' 牌操作" % seat_id)
        #             if value == 102:
        #                 who_can_do_operate[seat_id] = "wei"
        #                 logging.info("%s :座位号可以进行 '偎' 牌操作" % seat_id)
        #             if value == 103:
        #                 who_can_do_operate[seat_id] = "hu"
        #                 logging.info("%s :座位号可以进行 '胡' 牌操作" % seat_id)
        #             if value == 104:
        #                 who_can_do_operate[seat_id] = "pao"
        #                 logging.info("%s :座位号可以进行 '跑' 牌操作" % seat_id)
        #             if value == 105:
        #                 who_can_do_operate[seat_id] = "peng"
        #                 self.peng_card = operation_num_info["card_%s"%postfix]
        #                 logging.info("%s :座位号可以进行 '碰' 牌操作,牌: %s" % (seat_id,self.peng_card))
        #             if value == 106:
        #                 who_can_do_operate[seat_id] = "chi"
        #                 self.chi_card = operation_num_info["card_%s" % postfix]
        #                 logging.info("%s :座位号可以进行 '吃' 牌操作" % seat_id)
        #             if value == 107:
        #                 who_can_do_operate[seat_id] = "guo"
        #                 logging.info("%s :座位号可以进行 '过' 牌操作" % seat_id)
        #             if value == 108:
        #                 who_can_do_operate[seat_id] = "mo"
        #                 logging.info("%s :座位号可以进行 '摸' 牌操作" % seat_id)
        #             if value == 109:
        #                 who_can_do_operate[seat_id] = "zhe"
        #                 logging.info("%s :座位号可以进行 '啫' 牌操作" % seat_id)

        self.operation_user = seat_id
        self.operation_type = operation_type
        self.operation_sign = operation_sign
        self.who_can_do_operate = who_can_do_operate


    #   请求操作
    def qs_request_function(self, update_data):
        cs_request_function_data = CSRequestFunction(update_data)
        self.qs_send_data(cs_request_function_data.real_data)
        if self.seat_id == 2:
            pass
            # print("cs_request_function_data.real_data")

    #   请求操作回包
    def sc_request_function(self, funcName, protocol_num, data):
        self.sc_request_function_data = data
        helper_print(self.account, funcName, protocol_num, data)
        # if self.seat_id is data['seat_id'][1]:
        #     #   轮次结束
        #     self.current_rounds = False

    def sc_now_operation_user(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        # print("当前用户操作数据-->>%s"%data)
        self.sc_now_operation_player = data['seat_id'][1]


    #   错误提示
    def sc_error_tips(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_error_tips_data = data

    #   小局结算
    def sc_settlement(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)#True
        self.sc_settlement_data = data
        self.game_over = True

    #   大局结算
    def sc_total_settlement(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.total_settlement_data = data
        # print("总结算-->%s"%data)
        self.game_over = True
        self.sc_total_settlement_data = data

    #   请求离开房间
    def qs_leave_room(self):
        cs_leave_room_data = CSLeaveRoom()
        self.qs_send_data(cs_leave_room_data.real_data)

    #   离开房间回包
    def sc_leave_room(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_leave_room_data = data
        if data['error_code'][1] == -17:
            self.dissolve_room_state = True



    #   房主发出解散房间
    def qs_dissolve_room(self):
        cs_dissolve_room_data = CSDissolveRoom()
        self.qs_send_data(cs_dissolve_room_data.real_data)

    #   解散房间回包
    def sc_dissolve_room(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_dissolve_room_data = data
        if data["error_code"][1]==0:
            logging.info(" %s:号发起解散房间"%data['seat_id'][1])
        if self.account != self.user_mid:
            if not self.isAgree:
                #   发起同意
                self.qs_chose_dissolve_room()
                self.isAgree = True
                time.sleep(2)

    #   选择是否解散房间
    def qs_chose_dissolve_room(self):
        cs_chose_dissolve_data = CSChoseDissolveRoom()
        self.qs_send_data(cs_chose_dissolve_data.real_data)



    #   游戏服托管
    def qs_trusteeship(self):
        cs_trusteeship_data = CSTrusteeship()
        self.qs_send_data(cs_trusteeship_data.real_data)

    #   托管回包
    def sc_trusteeship(self, funcName, protocol_num, data):
        self.sc_trusteeship_data = data
        helper_print(self.account, funcName, protocol_num, data)

    #   发送聊天内容
    def qs_chat(self, update_data):
        cs_chat_content = CSChat(update_data)
        self.qs_send_data(cs_chat_content.real_data)

    #   发送聊天内容回包
    def sc_chat(self, funcName, protocol_num, data):
        self.sc_chat_data = data
        helper_print(self.account, funcName, protocol_num, data)


    #   发送聊天表情
    def qs_chat_face(self, update_data):
        cs_chat_face = CSChatFace(update_data)
        self.qs_send_data(cs_chat_face.real_data)

    #   发送聊天表情
    def sc_chat_face(self, funcName, protocol_num, data):
        self.sc_chat_face_data = data
        helper_print(self.account, funcName, protocol_num, data)

    #   互送道具
    def qs_send_gift(self, update_data):
        cs_send_gift = CSSendGift(update_data)
        self.qs_send_data(cs_send_gift.real_data)

    #   互送道具回包
    def sc_send_gift(self, funcName, protocol_num, data):
        self.sc_send_gift_data = data
        helper_print(self.account, funcName, protocol_num, data)

    #   不在房间中，无法进行房间的操作
    def sc_not_in_room(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_not_in_room_data = data
        self.in_the_room = False

    #   广播公聊
    def sc_common_chat(self, funcName, protocol_num, data):
        self.sc_common_chat_data = data
        helper_print(self.account, funcName, protocol_num, data)

    #   广播公聊 表情
    def sc_common_chat_with_face(self, funcName, protocol_num, data):
        self.sc_common_chat_data_with_chat = data
        helper_print(self.account, funcName, protocol_num, data, True)

    #   服务器即将关闭
    def sc_server_close(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_server_close_data = data


    #   做牌，测试专用
    def qs_make_cards_type(self, update_data):
        # print("发送的牌", update_data)
        cs_cards_type = CSMakeCardsType(update_data)

        # print("做牌数据: %s" % cs_cards_type.real_data)
        self.qs_send_data(cs_cards_type.real_data)


    #   做牌回包
    def sc_make_cards_type(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_make_cards_type_data = data

    #   重连后服务器推给自己的牌
    def sc_reconnection_server_send_cards(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_reconnection_server_send_cards_data = data


    # 重连接
    def sc_reconnect(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.reconnect_status = True
        print("座位号: %s 重连" % data['seat_id'][1])



    #   请求经纬度
    def qs_request_jingweidu(self, update_data):
        cs_jingweidu_data = CSJingWeiDu(update_data)
        self.qs_send_data(cs_jingweidu_data.real_data)

    #   经纬度回包
    def sc_jingweidu(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_jingweidu_data = data

    #   请求已创建的比赛回包
    def qs_created_game_list(self):
        cs_created_game_list_data = CSCreatedGameList()
        self.qs_send_data(cs_created_game_list_data.real_data)

    #   已创建的比赛回包
    def sc_created_game_list(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_created_game_list_data = data

    #   请求所在俱乐部的比赛回包
    def qs_club_game_list(self):
        cs_club_game_list_data = CSClubGameList()
        self.qs_send_data(cs_club_game_list_data.real_data)

    #   所在俱乐部比赛的回包
    def sc_club_game_list(self, funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.sc_club_game_list_data = data


    #湖南麻将用户出牌操作
    def qs_majiang_out_card(self,updata):
        cs_out_card_data = CSMajiangOutCard(updata)
        self.qs_send_data(cs_out_card_data.real_data)
    #湖南麻将用户碰牌操作
    def qs_majiang_peng_card(self,updata):
        cs_peng_card_data = CSMajiangPengCard(updata)
        self.qs_send_data(cs_peng_card_data.real_data)
    # 用户吃牌
    def qs_majiang_chi_card(self,updata):
        cs_chi_card_data = CSMajiangChiCard(updata)
        self.qs_send_data(cs_chi_card_data.real_data)
    #用戶杠牌
    def qs_majiang_gang_card(self,updata):
        cs_gang_card_data = CSMajiangGangCard(updata)
        self.qs_send_data(cs_gang_card_data.real_data)

    #用户补张
    def qs_majiang_supplement_card(self,updata):
        cs_supplement_card_data = CSMajiangSupplementCard(updata)
        self.qs_send_data(cs_supplement_card_data.real_data)
    #麻将胡
    def qs_majiang_hu_card(self,updata):
        cs_hu_card_data = CSMajiangHuOpertion(updata)
        self.qs_send_data(cs_hu_card_data.real_data)
    #麻将过牌
    def qs_majiang_guo_card(self,updata):
        cs_guo_card_data = CSMajiangCancelOperation(updata)
        self.qs_send_data(cs_guo_card_data.real_data)

    #海底漫游
    def qs_majiang_HDMY(self,updata):
        cs_HDMY_data = CSMajiangHDMYOperation(updata)
        self.qs_send_data(cs_HDMY_data.real_data)
    #服务器广播海底牌
    def sc_majiang_broadcast_HDL(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        HDL_data = data
        if not len(HDL_data) is 0:
            self.game_over = True



    #麻将大局结算
    def sc_majiang_big_settle_accounts(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.majiang_big_settle_accounts_data = data
    #服务器广播正王和纯王
    def sc_majiang_pure_wang(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data ,True)
        self.majiang_pure_wang_data = data
    #断线重连时
    def sc_majiang_reconnection(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        print("用户重连")
    #服务器通知封东状态
    def sc_fengdong_status(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data ,True)
    #麻将小局结算
    def sc_majiang_small_accounts(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.majiang_small_accounts_data = data
    #广播玩家手上的牌
    def sc_hand_cards(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        logging.info("座位号: %s 手里的牌数量: %s"%(data['seat_id'][1],data['hand_cards_num'][1]))
    #广播下一个出牌玩家
    def sc_next_out_card_player(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        logging.info("下一个出牌玩家座位号: %s"%data['seat_id'][1])
        self.majiang_next_out_card_player = data['seat_id'][1]

    # 服务器通知是否听牌
    def sc_ting_card(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data ,True)
        logging.info("%s:是否听牌(%s) "%(self.account,data["is_ting_card"][1]))

    #服务器通知发牌
    def sc_deal_card(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.majiang_deal_card_data = data
        self.sc_send_cards_data = data["cards_num_info"][1]['card']
        logging.info("%s - 服务器发牌 %s张: %s"%(self.account,data['cards_num'][1],data['cards_num_info'][1]['card']))



    #麻将出牌返回数据
    def sc_majiang_out_card(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)
        self.majiang_out_card = data

    # 麻将碰牌返回数据
    def sc_majiang_peng_card(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)

    #麻将杠牌返回数据
    def sc_majiang_gang_card(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)

    #麻将自摸胡操作
    def sc_majiang_zi_mo_hu(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        seat_id = data['seat_id'][1]
        hand_card_num = data["hand_card_num"][1]
        hand_cards = data["hand_cards"][1]['card']
        hu_card = data["hu_card"][1]
        logging.info("座位号: %s ,手里牌数: %s ,所有牌: %s, 胡的牌: %s"%(seat_id,hand_card_num,hand_cards,hu_card))
    #取消操作
    def sc_majiang_cancel_operation(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.majiang_cancel_data = data
    #通知玩家摸牌
    def sc_majiang_notification_touched_a_card(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.majiang_mo_card_data = data
        if data['dun_card_num'][1] == 1:
            self.majiang_HDMY = True

    # 胡牌
    def sc_majiang_hu_card(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)

    #吃牌操作返回数据
    def sc_majiang_chi_card(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)
    #用户补张
    def sc_majiang_player_supplement_card(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)

    #通知杠后补张操作
    def sc_notification_Gang_later_operation(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)

    # 补杠操作
    def sc_supplement_gang(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)

    #广播补牌
    def sc_broadcast_supplement_card(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)

    #宁乡开王麻将杠牌操作广播
    def sc_majiang_broadcast_operation_Ningxiang_gang(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)

    #麻将用户能做什么操作
    def sc_majiang_who_can_do(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)
        self.current_rounds = True
        self.majiang_who_can_do_data = data
        seat_id = data['seat_id'][1]
        majiang_who_can_do_operate = {}
        for i in data['operation_num_info'][1]:
            if i == 100:
                majiang_who_can_do_operate[seat_id] = "chu"
                logging.info("座位号: %s 可以出牌"%seat_id)
            elif i == 101:
                majiang_who_can_do_operate[seat_id] = "peng"
                logging.info("座位号: %s 可以碰牌" % seat_id)
            elif i == 102:
                majiang_who_can_do_operate[seat_id] = "gang"
                logging.info("座位号: %s 可以杠牌" % seat_id)
            elif i == 103:
                majiang_who_can_do_operate[seat_id] = "hu"
                logging.info("座位号: %s 可以胡牌" % seat_id)
            elif i == 104:
                majiang_who_can_do_operate[seat_id] = "guo"
                logging.info("座位号: %s 可以过牌" % seat_id)
            elif i == 105:
                majiang_who_can_do_operate[seat_id] = "mo"
                logging.info("座位号: %s 可以摸牌" % seat_id)
            elif i == 106:
                majiang_who_can_do_operate[seat_id] = "chi"
                logging.info("座位号: %s 可以吃牌" % seat_id)
            elif i == 107:
                majiang_who_can_do_operate[seat_id] = "bu"
                logging.info("座位号: %s 可以补张" % seat_id)
        self.majiang_seat_id = seat_id
        self.majiang_who_can_do_operate = majiang_who_can_do_operate

    def sc_majiang_HDMY_opertion(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)
        self.majiang_HDMY = True
        self.majiang_HDMY_operation_data = data

    #扎鳥
    def sc_majiang_zhao_niao(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        # print("玩家扎鸟")

    #广博哪个玩家摸牌
    def sc_majiang_broadcast_get_card(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)
        if data["dun_cards_num"][1] == 0:
            self.majiang_dun_card_zero = True
        elif data["dun_cards_num"][1] == 1:
            self.majiang_HDMY = True
        self.majiang_dun_card_num = data["dun_cards_num"][1]
        logging.info("座位号: %s 摸牌, 墩上牌数: %s"%(data["seat_id"][1],data["dun_cards_num"][1]))

    # 跑胡子补牌
    def sc_paohuzi_supplement(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)

    #逗溜子
    def sc_paohuzi_dou_liu_zi(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)



    #湖南麻将做牌
    def sc_majiang_make_cards_type(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)

    #将牌移到手牌中
    def sc_paohuzi_move_card(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        logging.info("座位号: %s 移动到手牌: %s"%(data['seat_id'][1],data['card'][1]))
    #广播名堂信息
    def sc_majiang_mingtang_ingo(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        data_info = data
        print("座位号: %s ,广播名堂类型: %s"%(data_info['seat_id'][1],data_info['mingtang_num_info'][1]))
    #服务器通知起手明堂操作
    def sc_majiang_mingtang_opreation_info(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)
        self.mingtang_opreation = data
        self.mingtang_status = True
        self.mingtang_seatid = data['seat_id'][1]
        logging.info("起手名堂操作座位号玩家: %s"%(data['seat_id'][1]))

    #投票解散
    def sc_majiang_dissolve(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        if data['error_code'][1] == -1:
            raise logging.error("解散房间失败,非法操作")
        elif data['error_code'][1] == -2:
            raise logging.error("解散房间失败,已投票")
        else:
            logging.info("解散房间成功!")


    #名堂操作
    def majiang_mingtang_opreation(self,update_data):
        cs_send_mingtang_opreation_data = CSMajiangMingtangOpreation(update_data)
        self.qs_send_data(cs_send_mingtang_opreation_data.real_data)

    #飘分操作
    def runfast_piao_score(self,update_data):
        sc_send_piao_score = CSRunFastPiaoScore(update_data)
        self.qs_send_data(sc_send_piao_score.real_data)


    def sc_majiang_disconnection_reconnect(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        logging.info(" %s: 座位号,断线重连桌面数据"%data['seatID'][1])



    #---------------------------------------------------------------------跑得快
    #发牌
    def sc_runfast_deal_card(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)
        self.runfast_dea_card_data = data
        self.runfast_card_list = data['card_num_info'][1]
        self.runfast_len_card = len(self.runfast_card_list)


    #广播下一个出牌玩家
    def sc_runfast_out_card_player(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)


    #通知用户做相应的操作
    def sc_runfast_who_can_do(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)
    #出牌
    def runfast_player_out_card(self,update_data):
        runfast_out_card_data = CSRunFastOutCard(update_data)
        self.qs_send_data(runfast_out_card_data.real_data)
    #过牌
    def runfast_player_guo_card(self,update_data):
        runfast_guo_card_data = CSRunFastGuoCard(update_data)
        self.qs_send_data(runfast_guo_card_data.real_data)

    #小局结算
    def sc_runfast_small_settle_accounts(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        logging.info("跑胡子小局结算")

    #断线重连
    def sc_runfast_reconnection(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)
        self.reconnect_status = True
        logging.info("跑得快, %s 号玩家重连"%data["seatid"][1])

    #大局结算
    def sc_runfast_big_settle_accounts(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        logging.info("跑胡子大局结算")

    #服务器广播炸弹结算
    def sc_runfast_broadcast_bomb(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)

    #查询上一轮出牌信息
    def sc_runfast_query_last_outcard_info(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)

    #服务器通知客户端飘分
    def sc_runfast_piaofen(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        self.piao_score_data = data

    #通知每个玩家飘分情况
    def sc_runfast_piaofen_info(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data)
        logging.info("%s 玩家选择---->>%s飘分" % (data['seat_id'][1], data['piaofen_score'][1]))


    #断线重连时，返回玩家飘分信息
    def sc_runfast_return_piaofen_info(self,funcName, protocol_num, data):
        helper_print(self.account, funcName, protocol_num, data,True)

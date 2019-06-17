#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@ author: Hubery
@ create on: 2018/6/19 13:44
@ file: protocol_entity.py
@ site: 
@ purpose: 协议实体
"""
from midConnectTest.lib.phz.net.net_package import *
# from lib.phz.define.protocol_define import *



class Encrypt2ParseData:
    def __init__(self, update_data, method=None):
        self.update_data = update_data
        self.method = method

    #   Update protocol data and perform different processing of data according to requirements.
    def get_update_data(self):
        if self.method == "pack":
            return self.pack_data()
        elif self.method == "unpack":
            return self.unpack_data()
        else:
            return None

    #   pack data
    def pack_data(self):
        package = net_package(self.update_data["protocol_num"][1])

        if len(self.update_data) > 0:
            for k, v in self.update_data.items():
                # print(k,v)
                if k != "protocol_num":
                    if v[0] == "INT32":
                        package.write_int32(v[1])
                    elif v[0] == "INT64":
                        package.write_int32(v[1])
                    elif v[0] == "INT16":
                        package.write_int16(v[1])
                    elif v[0] == "STRING":
                        if self.update_data["protocol_num"][1] == 5012:
                            if type(v[1]) == list:
                                for i in v[1]:
                                    # print(u"构造多张牌的数据: %s" % i)
                                    package.write_string(
                                        i[: len(i) - 1])  # print(u"数据组建：%s %s" % (package.int32data, package.data))
                            else:
                                # print(u"单张出牌操作数据: %s" % str(v[1]))
                                package.write_string(str(v[1]))
                        elif self.update_data["protocol_num"][1] ==2523:
                            if type(v[1]) == list:
                                for i in v[1]:
                                    package.write_string(
                                        i[: len(i) - 1])
                            else:
                                package.write_string(str(v[1]))


                        else:
                            package.write_string(str(v[1]))
        # print("package.encode: %s" % package.encode())
        return package.encode()

    #   unpack data
    def unpack_data(self):
        pass


#   Update protocol data.
class CommonUtils2UpdateData:
    def __init__(self, original_data, original_data_keys_list, update_data, method):
        self.original_data = original_data
        self.original_data_keys_list = original_data_keys_list
        self.data = update_data
        self.method = method

    def update_data(self):
        if len(self.data) > 0:
            for k, v in self.data.items():
                if k in self.original_data_keys_list:
                    self.original_data[k][1] = v

        # if self.original_data["protocol_num"][1] == 65534:
            # print("data: %s" % self.original_data)
        ud = Encrypt2ParseData(self.original_data, self.method)
        return ud.get_update_data()


#   common api to call update data
class CallUpdateApi:
    def __init__(self, original_data, original_data_keys_list, update_data, method):
        self.original_data = original_data
        self.original_data_keys_list = original_data_keys_list
        self.update_data = update_data
        self.method = method
        self.real_data = None
        self.get_real_data()

    def get_real_data(self):
        cu = CommonUtils2UpdateData(self.original_data, self.original_data_keys_list, self.update_data, self.method)
        self.real_data = cu.update_data()


#   login entity --> CS
class CSLogin:
    def __init__(self, data={}):
        self.cs_login_entity = {"protocol_num": ["INT32", 1000], "mid": ["INT32", 0], "unused": ["STRING", "login"],
                                "gp": ["INT32", 101], "sid": ["INT32", 1400]} #1500
        self.cs_keys_list = self.cs_login_entity.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_login_entity, self.cs_keys_list, self.update_data, self.method).real_data


#   login entity --> SC
class SCLogin:
    def __init__(self, data={}):
        self.sc_entity_data = {"error_code": ["INT32", 0],
                               }
        self.sc_login_keys_list = self.sc_entity_data.keys()
        self.update_data = data
        self.method = "unpack"


#   gold coins change entity --> SC
class SCGoldCoinsChange:
    def __init__(self):
        self.sc_entity_data = {}

#
# class SCReconnection:
#     def __init__(self):
#         self.sc_entity_data = {
#             "seat_id": ["INT32", 0],
#         }

class SCReconnect:
    def __init__(self):
        self.sc_entity_data = {
            "seat_id": ["INT32", 0],
        }


class SCChangeServer:
    def __init__(self):
        self.sc_entity_data = {}

class CSJiaTou:
    def __init__(self,data={}):
        self.cs_jiatou_data = {
            "protocol_num": ["INT32", 1036],
            "jiatou": ["INT32", 1]
        }
        self.cs_keys_list = self.cs_jiatou_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_jiatou_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data

class SCJiaTou:
    def __init__(self,data={}):
        self.sc_entity_data = {"error_code": ["INT32", 0],
            "Seatid": ["INT32", 0],
            "jiatou":["INT32", 0]}

        self.sc_jiatou = self.sc_entity_data.keys()
        self.update_data = data
        self.method = "unpack"


class CSCreateRoom_YiYang:
    def __init__(self,data={}):
        self.cs_create_room_entity = {"protocol_num": ["INT32", 2029],
                                      "gameBaoLiuZi": ["INT16", 1],
                                      "gameRoomType": ["STRING", "20"],
                                      "gamePaiJu": ["INT32", 0],
                                      "gameCiShu": ["INT32", 6],
                                      "gameWanFa": ["INT16", 0],
                                      "gamePlayer": ["INT32", 0],
                                      "gameFengDing": ["INT32", 100],
                                      "gameMinHuXi": ["INT32", 6],
                                      "gameClubId": ["INT32", 0],
                                      "gameVip": ["INT32", 0],
                                      "gameClubName": ["STRING", "tt"],
                                      "gameMoShi": ["INT32", 0],
                                      "gameParamIndex": ["INT32", 0],
                                      "gameTag": ["INT32", 0]

                                      }
        self.cs_keys_list = self.cs_create_room_entity.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_create_room_entity, self.cs_keys_list, self.update_data,
                                       self.method).real_data

class SCCreateRoom_YiYang:
    def __init__(self, data={}):

        self.sc_entity_data ={
            "BaoLiuZi":["INT16", 0],
            "error_code": ["INT32", 0],
            "gameRoomid": ["INT32", 0],
            "gameRoomType": ["STRING", 0],
            "gamePaiJu": ["INT32", 0],
            "gameJuShu": ["INT32", 0],
            "gameWanFa": ["INT16", 0],
            "gameRenShu": ["INT32", 0],
            "gameFengDing": ["INT32", 0],
            "gameMinHuXi": ["INT32", 0],
            "gameClubId": ["INT32", 0],
            "gameVip": ["INT32", 0],
            "gameClubName": ["STRING", ""]
        }

        self.sc_login_keys_list = self.sc_entity_data.keys()
        self.update_data = data
        self.method = "unpack"




#   create room entity -->CS
class CSCreateRoom:
    def __init__(self,data={}):
        self.cs_create_room_entity = {"protocol_num": ["INT32", 1102], "gameRoomType": ["STRING", ""],
                                      "gameCishu": ["INT32", 0],
                                      "gamePlayer": ["INT32", 3],   "gameWanFa": ["INT32", 0],
                                      "gameXuanXiang": ["INT32", 0],"gameZhama": ["INT32", 0],
                                      "gameDaiKaiFang": ["INT32", 0],"gameClubId": ["INT32", 0],
                                      "gameClubName": ["STRING", "tt"],
                                      "gameVip": ["INT32", 0],
                                      }

        self.cs_keys_list = self.cs_create_room_entity.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_create_room_entity, self.cs_keys_list, self.update_data,
                                       self.method).real_data


#   create room -->SC
class SCCreateRoom:
    def __init__(self, data={}):

        self.sc_entity_data = {"seat_id": ["INT32", 0],"room_id":["INT32", 0],"scene_type":["STRING", ""]}
        self.sc_login_keys_list = self.sc_entity_data.keys()
        self.update_data = data
        self.method = "unpack"


#   leave room -->CS
class CSLeaveRoom:
    def __init__(self, data={}):
        self.cs_leave_room_data = {"protocol_num": ["INT32", 1004]}
        self.cs_keys_list = self.cs_leave_room_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_leave_room_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data


#   leave room -->SC
class SCLeaveRoom:
    def __init__(self):
        self.sc_entity_data = {"mid": ["INT32", 00], "error_code": ["INT32", 99]}


#   dissolve room -->CS
class CSDissolveRoom:
    def __init__(self, data={}):
        self.cs_dissolve_room_data = {"protocol_num": ["INT32", 1008]}
        self.cs_keys_list = self.cs_dissolve_room_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_dissolve_room_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data


#   dissolve room --> SC: have not this entity
class SCDissolveRoom:
    def __init__(self):
        self.sc_entity_data = {"error_code": ["INT32", 99], "seat_id": ["INT32", 0],"time":["INT32", 0],
                               "user_num": ["INT32", 0],
                               "user_num_info": ["INT32",{"_seat_id":["INT32", 0],"isAgree":["INT32", 0]}],
                                }

#
class SCMajiangDissolve:
    def __init__(self):
        self.sc_entity_data = {"error_code": ["INT32", 99]}


#   chose dissolve room -->CS
class CSChoseDissolveRoom:
    def __init__(self, data={}):
        self.cs_chose_dissolve_room_data = {"protocol_num": ["INT32", 1012], "option": ["INT32", 1]}
        self.cs_keys_list = self.cs_chose_dissolve_room_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_chose_dissolve_room_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data




class SCjoinRoom:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0],"play_ip": ["STRING", ""],"play_id": ["INT32", 0],
                               "gp": ["INT32", 0],"sex": ["INT32", 0],"name": ["STRING", ""],
                               "icon": ["STRING", ""],"city": ["STRING", ""],"gps":["STRING", ""],"glob":["INT32", 0],

                               "play_score":["INT32", 0]
                               }



class SCAllUserInfo:
    def __init__(self):
        self.sc_entity_data = {

                               }





class CSRequestEnterRoom:
    def __init__(self, data={}):
        self.cs_request_enter_data = {"protocol_num": ["INT32", 1103], "room_id": ["INT32", 0],
                                      "club_id": ["INT32", 0]
                                      }
        self.cs_keys_list = self.cs_request_enter_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_request_enter_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data

#   request enter room --> SC
class SCMajiangRequestEnterRoom:
    def __init__(self):
        self.sc_entity_data = {"error_code": ["INT32", 0]

                               }

#   request query player and room info  -->CS
class CSRequestDepartureRoom:
    def __init__(self, data={}):
        self.cs_request_departure_room = {"protocol_num": ["INT32", 1009]}
        self.cs_keys_list = self.cs_request_departure_room.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_request_departure_room, self.cs_keys_list, self.update_data,
                                       self.method).real_data

#   request query player and room info  -->SC
class SCRequestDepartureRoom:
    def __init__(self):
        self.sc_entity_data = {"error_code":["INT32", 99],"seat_id":["INT32", 99]}


#   desktop snapshot --> SC
class SCDesktopSnapshot:
    def __init__(self):
        self.sc_entity_data = {"room_num": ["INT32", 0], "room_type": ["STRING", ""], "total_times": ["INT32", 0],
                               "banker_seat_id": ["INT32", 0], "current_player_seat_id": ["INT32", 0],
                               "current_card": ["STRING", ""], "current_send_card_seat_id": ["INT32", 0],
                               "hupai_type": ["INT32", 0], "player_num": ["INT32", 0], "player_info": ["INT32", {
                "seat_id": ["INT32", 0], "mid": ["INT32", 0], "zanli": ["INT32", 0], "isready": ["INT32", 0],
                "huxi": ["INT32", 0], "send_card_num": ["INT32", 0], "_card_list": ["STRING", ""],
                "molding_card": ["INT32", 0], "_card_type_list": ["INT32", {"shoupai_type": ["INT32", 0],
                                                                            "card_num": ["INT32", 0],
                                                                            "_card": ["STRING", ""], }]}],
                               "homer_seat_id": ["INT32", 0], "game_start_type": ["INT32", 0],
                               "player_number": ["INT32", 0],
                               "_player": ["INT32", {"seat_id": ["INT32", 0], "jiatuo_daniao": ["STRING", ""]}]}


#   room snapshot   -->SC
class SCRoomSnapshot:
    def __init__(self):
        self.sc_entity_data = {
                                "house_owner":['INT32', 0], "room_status":['INT32', 0],
                                "play_finish_num":['INT32', 0],"sum_jushu":['INT32', 0],
                                                                "players": ['INT32', 0],
                                                                "_player_info": ["INT32",
                                                                         {"seat_id": ['INT32', 0], "IP": ['string', ""],
                                                                          "player_id":['INT32', 0], "gp":['INT32', 0],
                                                                          "sex": ['INT32', 0],"name": ["STRING", ""],
                                                                          "icon": ["STRING", ""],"city": ["STRING", ""],
                                                                          "json":["INT32",{
                                                                              "gps": ["STRING", ""],
                                                                              "glob": ['INT32', 0],
                                                                              "quit_time":['INT32', 0]
                                                                          }]
                                                                          }],

                                "banker_seat":["INT32", 0],"seat_num":["INT32", 0]
                               }

#   enter room player info -->SC
class SCEnterRoomPlayerInfo:
    def __init__(self):
        self.sc_entity_data = {"mid": ["INT32", 0], "sex": ["INT32", 0], "name": ["STRING", 0], "icon": ["STRING", 0],
                               "vip": ["INT32", 0], "gold": ["INT32", 0], "jifen": ["INT32", 0],
                               "seat_id": ["INT32", 0], "ip": ["STRING", 0], "jingweidu": ["STRING", 0],
                               "huxi": ["INT32", 0], "time": ["INT32", 0], "home_owner": ["INT32", 0]}


class SCPlayGameTimes:
    def __init__(self):
        self.sc_entity_data = {"has_been_play_times": ["INT32", 0]}

#   request ready -->CS
class CSRequestReady:
    def __init__(self, data={}):
        self.cs_request_ready_data = {"protocol_num": ["INT32", 1005]}
        self.cs_keys_list = self.cs_request_ready_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_request_ready_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data

class SCRequestReady:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0]}


# 胡牌
class CSRequestHu:
    def __init__(self, data={}):
        self.cs_request_hu_data = {"protocol_num": ["INT32", 5009],"operation_number": ["STRING", ""]}
        self.cs_keys_list = self.cs_request_hu_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_request_hu_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data
class SCRequestHu:
    def __init__(self):
        self.sc_entity_data = {"error_code": ["INT32", 100]}

# 碰牌
class CSRequestPeng:
    def __init__(self, data={}):
        self.cs_request_peng_data = {"protocol_num": ["INT32", 5011],"operation_number": ["STRING", ""],"peng_card":["STRING", ""]}
        self.cs_keys_list = self.cs_request_peng_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_request_peng_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data
class SCRequestPeng:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0],"goal_seat_id":["INT32", 0],"peng_operation":["INT32", 0],"card":["STRING", ""],
                               "operation_scope":["INT32", 100],"sum_hu_xi":["INT32", 0]
                               }
# 出牌
class CSRequestChu:
    def __init__(self, data={}):
        self.cs_request_chu_data = {"protocol_num": ["INT32", 5013],"operation_number": ["STRING", ""],"chu_card":["STRING", ""]}
        self.cs_keys_list = self.cs_request_chu_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_request_chu_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data

class SCRequestChu:
    def __init__(self):
        self.sc_entity_data = {"error_code": ["INT32", 100],"seat_id":["INT32", 100],"chu_card":["STRING", ""]}

#  过牌
class CSRequestGuo:
    def __init__(self, data={}):
        self.cs_request_guo_data = {"protocol_num": ["INT32", 5014],"operation_number": ["STRING", ""]}
        self.cs_keys_list = self.cs_request_guo_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_request_guo_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data

class SCRequestGuo:
    def __init__(self):
        self.sc_entity_data = {"error_code": ["INT32", 100]}




#   trusteeship --> CS
class CSTrusteeship:
    def __init__(self, data={}):
        self.cs_trusteeship_data = {"protocol_num": ["INT32", 1053]}
        self.cs_keys_list = self.cs_trusteeship_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_trusteeship_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data
#   trusteeship --> SC
class SCTrusteeship:
    def __init__(self):
        self.sc_entity_data = {"seat_number": ["INT32", 0], "is_trusteeship": ["INT32", 0]}

#   game start -->SC
class SCGameStart:
    def __init__(self):
        self.sc_entity_data = {"error_code": ["INT32", 0], "playing_jushu": ["INT32", 0]}

#   send card -->SC
class SCSendCards:
    def __init__(self):
        self.sc_entity_data = {"card_num": ["INT32", 0], "card_": ["STRING", ""],"Dun_card_num": ["INT32", 0]}


class SCNowOperationUser:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0]}




class SCEndHuCard:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0], "hu_card": ["STRING", ""], "player_num": ["INT32", 0],
                          "player_num_info": ["INT32", {
                              "_seat_id": ["INT32", 99], "hu_xi": ["INT32", 0], "pao_hu": ["INT32", 0],
                              "cards_num": ["INT32", 0], "cards_num_info": ["INT32", {"card": ["STRING", ""]}]}],
                          "dun_cards_num": ["INT32", 0], "dun_cards_num_info": ["INT32", {"card": ["STRING", ""]}],
                          "time": ["INT32", 0],
                          "hand_group_num": ["INT32", 0], "hand_group_num_info": ["INT32", {"card_type": ["INT32", 0],
                                                                                            "card_group_num": ["INT32",
                                                                                                               0],
                                                                                            "card_group_num_info": [
                                                                                                "INT32", {
                                                                                                    "card": ["STRING",
                                                                                                             ""]}]}],

                          "max_mingtang_number": ["STRING", ""]
                          }


class SCGameOver:
    def __init__(self):
        self.sc_entity_data = {
            "room_id": ["INT32", 0],
            "room_type": ["STRING", ""],
            "dissolve_type": ["INT32", 0]
        }

class SCCreateErrorCode:
    def __init__(self):
        self.sc_entity_data = {
            "error_code": ["INT32", 0],

        }



#小局结算
class SCSmallSettleAccounts:
    def __init__(self):
        self.sc_entity_data = {
            "banker": ["INT32", 0],
            "next_banker": ["INT32", 0],
            "number_of_remain_": ["INT32", 99],
            "hu_player_id": ["INT32", 99],
            "hu_type": ["INT32", 99],
            "hu_card": ["STRING", ""],
            "player_sum": ["INT32", 0],
            "player_sum_info":["INT32",{"seat_id":["INT32", 99], "mid":["INT32", 99],"name":["STRING", ""],"icon":["STRING", ""],
                                        "this_score":["INT32", 0],"user_sum_score":["INT64", 0],"card_group_num":["INT32", 0],
                                         "card_group_num_info":["INT32",{"card_type":["INT32", 0],
                                                                        "score":["INT32", 0],
                                                                        "is_hu_card":["INT32", 0],
                                                                        "cards_sum":["INT32", 0],
                                                                        "cards_sum_info":["INT32", {"card_":["STRING", ""]}],

                                                                        }],
                                        "ming_tang_num":["INT32", 0],
                                        "ming_tang_num_info": ["INT32", {"ming_tang_type":["INT32", 0],"score_type":["INT32", 0],"value":["INT32", 0]}],
                                        }],
            "dun_sum":["INT32", 0],
            "dun_sum_info": ["INT32", {"dun_card":["STRING", ""]}],
            "json":["STRING", ""],
            "this_liu_score_sum_info": ["INT32", {"this_liu_score":["INT32", 0]}]

        }


#广播补牌消息给其它玩家
class SCSupplementCard:
    def __init__(self):
        self.sc_entity_data = {
            "seat_id": ["INT32", 0],
            "hande_card": ["INT32", 0],
            "dun_card_num": ["INT32", 0]
        }
# 广播提牌操作
class SCBroadcastTi:
    def __init__(self):
        self.sc_entity_data = {
            "seat_id": ["INT32", 0],
            "card_type": ["INT32", 0],
            "card": ["STRING", ""],
            "operation_scope":["INT32", 0],
            "sum_hu_xi": ["INT32", 0]
        }

#广播偎牌操作
class SCBroadcastWei:
    def __init__(self):
        self.sc_entity_data = {
            "seat_id": ["INT32", 0],
            "card_type": ["INT32", 0],
            "card": ["STRING", ""],
            "operation_scope":["INT32", 0],
            "sum_hu_xi": ["INT32", 0]
        }


#广播跑牌操作
class SCBroadcastPao:
    def __init__(self):
        self.sc_entity_data = {
            "seat_id": ["INT32", 0],
            "goal_seat_id": ["INT32", 0],
            "card_type": ["INT32", 0],
            "card": ["STRING", ""],
            "operation_scope":["INT32", 0],
            "sum_hu_xi": ["INT32", 0]
        }

#广播将展示的牌移到出牌区域
class SCCardRegionIsCHU:
    def __init__(self):
        self.sc_entity_data = {
            "seat_id": ["INT32", 0],
            "card": ["STRING", ""]
        }








#   touch cards -->SC
class SCTouchCards:
    def __init__(self):
        self.sc_entity_data = {
            "seat_id": ["INT32", 0],
            "touch_card": ["STRING", ""],
            "dun_card_num": ["INT32", 0],
            "is_join_hand_card":["INT32", 0],
            "hand_card_num": ["INT32", 0],
            "is_wei": ["INT32", 0]
        }





#   player can do -->SC
class SCPlayerCanDo:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0],
                               "operation_num": ["INT32", 0],
                               "operation_num_info": ["INT32",{
                                                               "operation_type": ["INT32", 0],
                                                               "card": ["STRING", ""]
                                                        }],
                               "operation_sign": ["STRING", ""]}

class SCPlayerHandCards:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0],
                               "hand_cards_num": ["INT32", 0],
                               "Dun_cards_num":["INT32", 0],
                               }



class CSRequestFunction:
    def __init__(self, data={}):
        if data["group_card"] == 1:
            self.cs_request_function_data = {"protocol_num": ["INT32", 5012], "operation_number": ["STRING", ""],
                                             "chi_card": ["STRING", ""], "group_card": ["INT32", 0],
                                             "card_type": ["INT32", 0],"card_num": ["INT32", 3],"card_list":["STRING", ""]}
                                            #group_card_牌组的个数   #card_type_牌型(1有息2无息)
        if data["group_card"] == 2:
            self.cs_request_function_data = {"protocol_num": ["INT32", 5012], "operation_number": ["STRING", ""],
                                             "chi_card": ["STRING", ""], "group_card": ["INT32", 0],
                                             "card_type": ["INT32", 0], "card_num": ["INT32", 3],
                                             "card_list": ["STRING", ""],
                                             "card_type_1": ["INT32", 0], "card_num_1": ["INT32", 3],
                                             "card_list_1": ["STRING", ""]}

        self.cs_keys_list = self.cs_request_function_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_request_function_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data

class SCRequestFunction:
    def __init__(self):
        self.sc_entity_data = {"error_code": ["INT32", 100]}
        # "seat_id": ["INT32", -100], "zong_hu_xi": ["INT32", 0],
        # "do_function": ["INT32", 0], "card_num": ["INT32", 0], "_card": ["STRING", ""],
        # "player_num": ["INT32", 0], "_player": ["INT32", {"seat_id": ["INT32", 0],
        #                                                   "fen_shu": ["INT32", 0],
        #                                                   "zong_fen": ["INT32", 0]}],
        # "game_type": ["INT32", 0], "an_pai_hu_xi": ["INT32", 0]}


class SCErrorTips:
    def __init__(self):
        self.sc_entity_data = {"error_code": ["INT32", 0], "card": ["STRING", ""]}
#麻将大局结算
class SCMajiangBigSettle_accouts:
    def __init__(self):
        self.sc_entity_data = {"house_owner": ["INT32", 0], "players": ["INT32", 0],
                                                             "players_info":  ["INT32", {
                                                                 "player_seat_id":["INT32", 0],
                                                                 "uid":["INT32", 0],
                                                                 "player_name":["STRING", ""],
                                                                 "player_icon":["STRING", ""],
                                                                 "big_zimo_num":["INT32", 0],
                                                                 "small_zimo_num": ["INT32", 0],
                                                                 "big_dianpao_num": ["INT32", 0],
                                                                 "small_dianpao_num": ["INT32", 0],
                                                                 "big_jiepao_num": ["INT32", 0],
                                                                 "small_jiepao_num": ["INT32", 0],
                                                                 "xxxxxxxxx": ["INT32", 0],
                                                                 "score": ["INT32", 0],
                                                             }],
                               }



# 服务器广播正王和纯王
class SCMajiangPureWANG:
    def __init__(self):
        self.sc_entity_data = {"zheng_wang": ["STRING", ""], "chun_wang_num": ["INT32",99],
                                                             "chun_wang_num_info":  ["INT32", {
                                                             "chun_wang":["STRING", ""],
                                                             }]
                               }
#断线重连时
class SCRMajiangReconnection:
    def __init__(self):
        self.sc_entity_data = {"players": ["INT32", 0],
                               "players_info": ["INT32", {
                                   "seat_id":["INT32", 0],
                                   "player_score": ["INT32", 0],
                               }]}

#服务器通知封东状态
class SCMajiangFengDongStatus:
    def __init__(self):
        self.sc_entity_data = {"players": ["INT32", 0],
                               "players_info": ["INT32", {
                                   "seat_id":["INT32", 0],
                                   "fengdong_status": ["INT32", 0],
                               }]}

#断线重连桌面数据
class SCMJDisconnectionReconnect:
    def __init__(self):
        self.sc_entity_data = {"seatID": ["INT32", 0]}




#麻将小局结算
class SCMajiangSmallSettleAccounts:
    def __init__(self):
        self.sc_entity_data = {
            "banker": ["INT32", 0],
            "hu_player_id": ["INT32", 99],
            "number_of_remain_": ["INT32", 99],
            "hu_type": ["INT32", 99],
            "hu_card": ["STRING", ""],
            "hu_player_sum": ["INT32", 0],
            "hu_player_sum_info": ["INT32", {"seat_id": ["INT32", 99]}],
            "players_num": ["INT32", 0],
            "players_num_info": ["INT32",
                 {
                "seat_id":["INT32", 99],
                "uid":["INT32", 99],
                "name":["STRING", ""],
                "score":["INT32", 99],
                "player_sum_score":["INT64", 0],
                "group_num":["INT32", 0],
                "group_num_info":["INT32", {
                    "cardname":["STRING", ""],
                    "card_group_type":["INT32", 0]
                                                }],

                "hand_card_num":["INT32", 0],
                "hand_card_num_info":["INT32", {"card":["STRING", ""]}],
                "ming_tang_num":["INT32", 0],
                "ming_tang_num_info":["INT32", {
                        "mingtang_type":["INT32", 0],
                        "mingtang_number":["INT32", 0]
                    }],

            }],
            "zha_niao_num": ["INT32", 0],
            "zha_niao_num_info": ["INT32", {"card": ["STRING", ""]}],
            "RoomData": ["STRING", ""],
            "dun_cards": ["STRING", ""],
            "zhong_ma_players": ["INT32", 0],
            "zhong_ma_players_info": ["INT32", {
                "seat_id": ["INT32", 0],
                "zhong_ma_cards": ["INT32", 0],
                "zhong_ma_cards_info": ["INT32", {"card": ["STRING", ""]}],
            }]
                               }

#广播玩家手上的牌数
class SCMajiangHandCards:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0],
                               "hand_cards_num":["INT32", 0],
                               "dun_cards_num":["INT32", 0],
                               }
#麻将广播名堂信息
class SCMajiangBroadcastMingtangInfo:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0],
                               "mingtang_num":["INT32", 0],
                               "mingtang_num_info":["INT32", {"mingtang_type": ["INT32", 99]}]
                               }


class SCMajiangBroadcastMingtangOpreation:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0],
                               "operation_num":["INT32", 0],
                               "operation_num_info":["INT32", {"mingtang_type": ["INT32", 99]}],
                               "operation_sign":["STRING", ""]
                               }


#名堂操作
class CSMajiangMingtangOpreation:
    def __init__(self, data):
        self.cs_chat_data = {"protocol_num": ["INT32", 1043], "operation_number": ["STRING", ""],"mingtang_type": ["INT32", 99]}
        self.cs_keys_list = self.cs_chat_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_chat_data, self.cs_keys_list, self.update_data, self.method).real_data







# # 测试做牌
# class CSMajiangMakeCardsType:
#     def __init__(self, data={}):
#         self.cs_make_cards_type_data = {"protocol_num": ["INT16", 65534], "cards_list": ["STRING", ""]}
#         self.cs_keys_list = self.cs_make_cards_type_data.keys()
#         self.update_data = data
#         self.method = "pack"
#         self.real_data = CallUpdateApi(self.cs_make_cards_type_data, self.cs_keys_list, self.update_data,
#                                        self.method).real_data



# 测试做牌
class SCMajiangMakeCardsType:
    pass








#广播下一个出牌玩家
class SCMajiangNextOutCardPlayer:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0]}

#服务器通知是否听牌
class SCMajiangTingCard:
    def __init__(self):
        self.sc_entity_data = {"is_ting_card": ["INT32", 0]}


#发牌
class SCMajiangDealCard:
    def __init__(self):
        self.sc_entity_data = {"cards_num": ["INT32", 0],
                               "cards_num_info": ["INT32", {"card":["STRING", ""]}],
                               "dun_cards_num":["INT32", 0]

                               }


#通知用户做相应的操作
class SCMajiangWhoCanDo:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0],
                               "operation_num":["INT32", 0],
                               "operation_num_info":["INT32", []],
                               "operation_number":["STRING", ""]
                               }

#用户出牌操作
class CSMajiangOutCard:
    def __init__(self, data):
        self.cs_chat_data = {"protocol_num": ["INT32", 1023], "card": ["STRING", ""], "operation_number": ["STRING", ""]}
        self.cs_keys_list = self.cs_chat_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_chat_data, self.cs_keys_list, self.update_data, self.method).real_data



#用户出牌操作返回数据
class SCMajiangOutCard:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0],"card": ["STRING", ""]}


#用户碰牌操作
class CSMajiangPengCard:
    def __init__(self, data):
        self.cs_chat_data = {"protocol_num": ["INT32", 1024], "operation_number": ["STRING", ""]}
        self.cs_keys_list = self.cs_chat_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_chat_data, self.cs_keys_list, self.update_data, self.method).real_data


#湖南麻将碰牌返回数据
class SCMajiangPengCard:
    def __init__(self):
        self.sc_entity_data = {"peng_card_seat_id": ["INT32", 0],"out_card_seat_id": ["INT32", 0],"card": ["STRING", ""]}


#湖南麻将杠牌操作
class CSMajiangGangCard:
    def __init__(self, data):
        self.cs_chat_data = {"protocol_num": ["INT32", 1025], "card": ["STRING", ""],"operation_number": ["STRING", ""]}
        self.cs_keys_list = self.cs_chat_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_chat_data, self.cs_keys_list, self.update_data, self.method).real_data



# 湖南麻将杠牌操作返回数据
class SCMajiangGangCard:
    def __init__(self):
        self.sc_entity_data = {"gang_card_seat_id": ["INT32", 0],"gang_card_type": ["INT32", 0],"gang_target_player": ["INT32", 0],"card": ["STRING", ""]}



# 湖南麻将自摸胡操作返回数据
class SCMajiangZiMoHu:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0],
                               "hand_card_num": ["INT32", 0],
                               "hand_cards": ["INT32", {"card":["STRING", ""]}],

                               "hu_card": ["STRING", ""]}

#取消操作
class CSMajiangCancelOperation:
    def __init__(self, data):
        self.cs_chat_data = {"protocol_num": ["INT32", 1027],"operation_number": ["STRING", ""]}
        self.cs_keys_list = self.cs_chat_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_chat_data, self.cs_keys_list, self.update_data, self.method).real_data

#将牌移到手牌中
class SCPHZMove_Card:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 99],"card": ["STRING", ""]}


#取消操作返回数据
class SCMajiangCancelOperation:
    def __init__(self):
        self.sc_entity_data = {"error_code": ["INT32", 99]}

#通知玩家摸牌
class SCMajiangNotificationTouchedACard:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0],"card": ["STRING", ""],"dun_card_num": ["INT32", 0]}
#胡牌/抢杠胡/点炮胡
class SCMajiangHuCard:
    def __init__(self):
        self.sc_entity_data = {"jie_pao_seat_id": ["INT32", 0],
                               "dian_pao_seat_id": ["INT32", 0],
                               "hu_card": ["STRING", ""],
                               "hand_card_num": ["INT32", 0],
                               "hand_cards":["INT32", {"card": ["STRING", ""]}]
                               }
# 吃牌请求
class CSMajiangChiCard:
    def __init__(self, data):
        self.cs_chat_data = {"protocol_num": ["INT32", 1036],"card": ["STRING", ""],"operation_number": ["STRING", ""]}
        self.cs_keys_list = self.cs_chat_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_chat_data, self.cs_keys_list, self.update_data, self.method).real_data




# 吃牌操作数据
class SCMajiangChiCard:
    def __init__(self):
        self.sc_entity_data = {"chi_seat_id": ["INT32", 0],
                               "card":["STRING", ""],
                               "out_card_seat_id":["INT32", 0],
                               "_card":["STRING", ""]

                               }

#  用户补张
class CSMajiangSupplementCard:
    def __init__(self, data):
        self.cs_chat_data = {"protocol_num": ["INT32", 1037],"card": ["STRING", ""],"operation_number": ["STRING", ""]}
        self.cs_keys_list = self.cs_chat_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_chat_data, self.cs_keys_list, self.update_data, self.method).real_data


#补张返回数据
class SCMajiangplayerSupplementCard:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0],
                               "supplementCard_type": ["INT32", 0],
                               "out_card_seat_id":["INT32", 0],
                               "_card":["STRING", ""]
                               }


#通知杠后补张操作
class SCMajiangNotficationGangLaterOpration:
    def __init__(self):
        self.sc_entity_data = {"operation_number": ["INT32", 0],
                               "gang_player_seat_id": ["INT32", 0],
                               "gang_card":["STRING", ""],
                               "operation_num":["INT32", 0],
                               "operation_num_info":["INT32", {"card":["STRING", ""],
                                                               "_operation_num":["INT32", 0],
                                                               "_operation_info":["INT32", {"operation_type":["INT32", 0]}],
                                                               }]
                               }


# 补杠操作
class CSMajiangSupplementGang:
    def __init__(self, data):
        self.cs_chat_data = {"protocol_num": ["INT32", 1039],"operation_type": ["INT32", 0],"card": ["STRING", ""],
                             "operation_number": ["STRING", ""],"chi_card":["STRING", ""]}

        self.cs_keys_list = self.cs_chat_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_chat_data, self.cs_keys_list, self.update_data, self.method).real_data


class SCMajiangSupplementGang:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0],
                               "supplement_card_num":["INT32", 0],
                               "supplement_card_num_info":["INT32", {"card":["STRING", ""]}],
                               "dun_card_num":["INT32", 0]
                               }
#胡牌
class CSMajiangHuOpertion:
    def __init__(self, data):
        self.cs_chat_data = {"protocol_num": ["INT32", 1026],"operation_number": ["STRING", ""]}

        self.cs_keys_list = self.cs_chat_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_chat_data, self.cs_keys_list, self.update_data, self.method).real_data


#海底漫游
class CSMajiangHDMYOperation:
    def __init__(self, data):
        self.cs_chat_data = {"protocol_num": ["INT32", 1044],"operation_type":["INT32", 0],"operation_number": ["STRING", ""]}
        self.cs_keys_list = self.cs_chat_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_chat_data, self.cs_keys_list, self.update_data, self.method).real_data


#海底漫游
class SCMajiangHDMYOperation:
    def __init__(self):
        self.sc_entity_data = {"operation_info": ["STRING", ""]}

#服务器广播海底牌
class SCMajiangBroadcast_HDL:
    def __init__(self):
        self.sc_entity_data = {"card": ["STRING", ""]}


#扎鳥
class SCMajiangZhaNiao:
    def __init__(self):
        self.sc_entity_data = {"zhong_ma_players": ["INT32", 0],
                               "zhong_ma_players_info":["INT32", {
                                   "seat_id":["INT32", 0],
                                   "zhong_ma_num":["INT32", 0],
                                   "zhong_ma_card_list":["STRING", ""]
                               }]
                               }
#补牌
class SCPHZSupplementCard:
    def __init__(self):
        self.sc_entity_data = {"card": ["STRING", ""],"dun_cards_num":["INT32", 0]}



#逗溜子
class SCPHZDouLiuZi:
    def __init__(self):
        self.sc_entity_data = {"liu_score": ["INT32", 0],"players_num":["INT32", 0],"players_info":["INT32", {
                                                                                                        "seat_id":["INT32", 0],
                                                                                                        "this_liu_score":["INT32", 0],
                                                                                                        "player_score": ["INT32", 0]
        }]}







#广播补牌
class SCMajiangBroadcastSupplementCard:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0],
                               "operation_type":["INT32", 0],
                               "card":["STRING", ""],
                               "gang_player_seat_id":["INT32", 0]
                               }
class SCMajiangBroadcastOperationNingxiangGang:
    def __init__(self):
        self.sc_entity_data = {"dice_value": ["INT32", 0],
                               "cards_num":["INT32", 0],
                               "gang_num":["STRING", ""],
                               "gang_num_info":["INT32", {"card":["STRING", ""]}]
                               }



class SCMajiangBroadcastGetCard:
    def __init__(self):
        self.sc_entity_data = {"seat_id": ["INT32", 0],
                               "dun_cards_num":["INT32", 0],
                               }







#   not in room -->SC
class SCNotInRoom:
    def __init__(self):
        self.sc_entity_data = {"error_code": ["INT16", 0]}

#   server close -> SC
class SCServerClose:
    def __init__(self):
        self.sc_entity_data = {"error_code": ["INT32", 0]}

#   total settlement
class SCTotalSettlement:
    def __init__(self):
        self.sc_entity_data = {
            "house_owner": ["INT32", 0],
            "players_num": ["INT32", 0],
            "players_num_info":["INT32",{
                                        "seat_id":["INT32", 0],
                                        "mid":["INT32", 0],
                                        "name":["STRING", ""],
                                        "icon":["STRING", ""],
                                        "hu_num":["INT32", 0],
                                        "zi_mo_num":["INT32", 0],
                                        "dian_pao_num":["INT32", 0],
                                        "ti_card":["INT32", 0],
                                        "pao_num":["INT32", 0],
                                        "sum_score": ["INT64", 0],
                                        }],
            "json":["STRING", ""]

        }

#   common chat
class SCCommonChat:
    def __init__(self):
        self.sc_entity_data = {"chat_type": ["INT32", 0], "mid": ["INT32", 0], "name": ["STRING", ""],
                               "msg": ["STRING", ""], "seat_id": ["INT32", 0]}


class CSChat:
    def __init__(self, data):
        self.cs_chat_data = {"protocol_num": ["INT32", 2001], "msg": ["STRING", ""], "type": ["INT32", 0]}
        self.cs_keys_list = self.cs_chat_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_chat_data, self.cs_keys_list, self.update_data, self.method).real_data


class SCChat:
    def __init__(self):
        self.sc_entity_data = {"error_code": ["INT32", 0], "type": ["INT32", -100], "seat_id": ["INT32", 0]}


class CSChatFace:
    def __init__(self, data):
        self.cs_chat_face_data = {"protocol_num": ["INT32", 2009], "msg": ["STRING", ""], "type": ["INT32", 0]}
        self.cs_keys_list = self.cs_chat_face_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_chat_face_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data

class SCChatFace:
    def __init__(self):
        self.sc_entity_data = {"error_code": ["INT32", -100], "type": ["INT32", -100], "seat_id": ["INT32", 0]}


class CSSendGift:
    def __init__(self, data):
        self.cs_send_gift_data = {"protocol_num": ["INT32", 1042], "recv_id": ["INT32", 0], "props": ["STRING", ""]}
        self.cs_keys_list = self.cs_send_gift_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_send_gift_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data

class SCSendGift:
    def __init__(self):
        self.sc_entity_data = {"error_code": ["INT32", -100], "send_mid": ["INT32", 0], "recv_mid": ["INT32", 0],
                               "props": ["STRING", ""]}


class SCCommonChatWithFace:
    def __init__(self):
        self.sc_entity_data = {"type": ["INT32", -100], "mid": ["INT32", -100], "name": ["STRING", ""], "msg": ["STRING", ""]}


class CSMakeCardsType:
    def __init__(self, data):
        self.cs_make_cards_type_data = {"protocol_num": ["INT16", 65534], "cards_list": ["STRING", ""]}
        self.cs_keys_list = self.cs_make_cards_type_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_make_cards_type_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data


class SCMakeCardsType:
    def __init__(self):
        self.sc_entity_data = {"error_code": ["INT32", -100]}


class SCReconnectionServerSendCards:
    def __init__(self):
        self.sc_entity_data = {"dipai_num": ["INT32", -100], "_cards": ["STRING", ""]}


class CSJingWeiDu:
    def __init__(self, data):
        self.cs_jingweidu_data = {"protocol_num": ["INT32", 1028], "jingweidu": ["STRING", ""],
                                  "isrefresh": ["INT32", 99]}
        self.cs_keys_list = self.cs_jingweidu_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_jingweidu_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data

class SCJingWeiDu:
    def __init__(self):
        self.sc_entity_data = {"players": ["INT32", -100],
                               "players_info": ["INT32", {"seat_id": ["INT32", 0], "jingweidu": ["STRING", ""]}]}


class CSCreatedGameList:
    def __init__(self, data):
        self.cs_created_game_list_data = {"protocol_num": ["INT32", 1100]}
        self.cs_keys_list = self.cs_created_game_list_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_created_game_list_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data


class SCCreatedGameList:
    def __init__(self):
        self.sc_entity_data = {"list_num": ["INT32", 0], "list_info": ["INT32", {"game_index": ["INT32", 0],
                                                                                 "club_id": ["INT32", 0],
                                                                                 "club_name": ["STRING", ""],
                                                                                 "room_type": ["STRING", ""],
                                                                                 "wanfa": ["INT32", 0],
                                                                                 "difen": ["INT32", 0],
                                                                                 "room_players": ["INT32", 0],
                                                                                 "total_players": ["INT32", 0],
                                                                                 "real_players": ["INT32", 0],
                                                                                 "rounds_num": ["INT32", 0],
                                                                                 "innings": ["INT32", 0],
                                                                                 "format": ["INT32", 0],
                                                                                 "state": ["INT32", 0],
                                                                                 "distance_close_time": ["INT32", 0],
                                                                                 "uuid": ["STRING", ""], }

                                                                       ]}


class CSClubGameList:
    def __init__(self, data):
        self.cs_club_game_list_data = {"protocol_num": ["INT32", 1101]}
        self.cs_keys_list = self.cs_club_game_list_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_club_game_list_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data


class SCClubGameList:
    def __init__(self):
        self.sc_entity_data = {"list_num": ["INT32", 0], "list_info": ["INT32", {"club_icon": ["STRING", ""],
                                                                                 "club_name": ["STRING", ""],
                                                                                 "club_id": ["INT32", 0],
                                                                                 "game_index": ["INT32", 0],
                                                                                 "room_type": ["STRING", ""],
                                                                                 "wanfa": ["INT32", 0],
                                                                                 "difen": ["INT32", 0],
                                                                                 "room_players": ["INT32", 0],
                                                                                 "total_players": ["INT32", 0],
                                                                                 "real_players": ["INT32", 0],
                                                                                 "rounds_num": ["INT32", 0],
                                                                                 "innings": ["INT32", 0],
                                                                                 "format": ["INT32", 0],
                                                                                 "state": ["INT32", 0],
                                                                                 "distance_close_time": ["INT32", 0],
                                                                                 "uuid": ["STRING", ""], }

                                                                       ]}


class SCPlayerChangeIdentity:
    def __init__(self):
        self.sc_entity_data = {"status": ["INT32", -100]}






class SCplayerChangeIdentity:
    def __init__(self):
        self.sc_entity_data = {
            "status": ["INT32", -100]
        }
class SCDaTou:
    def __init__(self):
        self.sc_entity_data ={
            "datou":[["INT32", 0]]
        }

#----------------------------------------------跑得快
#发牌
class SCRunFastDealCard:
    def __init__(self):
        self.sc_entity_data = {
            "card_num": ["INT32", -100],
            "card_num_info":["INT32",{"uuid": ["STRING", ""]}]
        }

#广播下一个出牌玩家
class SCRunFastOutCard_Player:
    def __init__(self):
        self.sc_entity_data ={
            "seatid":["INT32", 0]
        }

#通知用户做相应的操作
class SCRunFastWhoCanDo:
    def __init__(self):
        self.sc_entity_data ={
            "seatid":["INT32", 0],
            "operation_num":["INT32", 0],
            "operation_num_info":["INT32", {"operation_type":["INT32",0]}],
            "operation_sign":["STRING", ""]
        }

#出牌
class SCRunFastOutCard:
    def __init__(self):
        self.sc_entity_data ={
            "seatid":["INT32", 0],
            "hand_card_num":["INT32", 0],
            "out_card_num":["INT32", 0],
            "out_card_num_info":["INT32", {"card":["STRING", ""]}],
            "whether_auto_outcard":["INT32", 0],
        }

class CSRunFastOutCard:
    def __init__(self, data):
        self.cs_club_game_list_data = {"protocol_num": ["INT32", 2523],"operation_number":["STRING", ""],"outcard_num":["INT32", 0],"out_card":["STRING", []]}
        self.cs_keys_list = self.cs_club_game_list_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_club_game_list_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data

#过牌
class CSRunFastGuoCard:
    def __init__(self, data):
        self.cs_club_game_list_data = {"protocol_num": ["INT32", 1027]}
        self.cs_keys_list = self.cs_club_game_list_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_club_game_list_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data

#飘分
class CSRunFastPiaoScore:
    def __init__(self, data):
        self.cs_club_game_list_data = {"protocol_num": ["INT32", 1062],"piao_Score":["INT32", 0],"operation_Number":["STRING", ""]}
        self.cs_keys_list = self.cs_club_game_list_data.keys()
        self.update_data = data
        self.method = "pack"
        self.real_data = CallUpdateApi(self.cs_club_game_list_data, self.cs_keys_list, self.update_data,
                                       self.method).real_data




#跑的快小局结算
class SCRunFastSmallSettleAccounts:
    def __init__(self):
        self.sc_entity_data ={
            "winner_seatid":["INT32", 0],
            "remain_num":["INT32", 0],
            "player_num":["INT32", 0],
            "player_sum_info":["INT32",{
                                        "seatid":["INT32", 0],
                                        "uid":["INT32", 0],
                                        "name":["STRING", ""],
                                        "icou":["STRING", ""],
                                        "bomb_num":["INT32", 0],
                                        "this_is_score": ["INT32", 0],
                                        "player_score": ["INT64", 0],
                                        "ChunTian": ["INT32", 0],
                                        "PiaoFei_score":["INT32", 0],
                                        "out_card_num":["INT32", 0],
                                        "out_card_num_info": ["INT32", {
                                                                        "card_type":["INT32", 0],
                                                                        "card_num": ["INT32", 0],
                                                                        "card_list":["INT32", {"card":["STRING", ""]}],
                                                                         }],
                                        "hand_card_num":["INT32", 0],
                                        "hand_card_list":["INT32", {"card":["STRING", ""]}],
                                        "String":["STRING", ""],
                                            }],
            "json":["STRING", ""],
            "transfer_card":["STRING", ""],
            "red_ten_seatID":["INT32", 0],
            "red_nine_seatID": ["INT32", 0],

        }


#短綫重連
class SCRUnFastReconnection:
    def __init__(self):
        self.sc_entity_data ={
            "seatid":["INT32", 0]}


#大局结算
class SCRunFastBigSettleAccounts:
    def __init__(self):
        self.sc_entity_data = {"seatid": ["INT32", 0],
                               "players": ["INT32", 0],
                               "players_info": ["INT32", {
                                   "player_seat_id": ["INT32", 0],
                                   "uid": ["INT32", 0],
                                   "player_name": ["STRING", ""],
                                   "player_icon": ["STRING", ""],
                                   "player_sum_score": ["INT64", 0],
                                   "bomb_num": ["INT32", 0],
                                   "win_num": ["INT32", 0],
                                   "lost_num": ["INT32", 0],
                                   "small_max_score": ["INT32", 0],
                                                            }],
                               "json":["STRING", ""],
                               "double_score_seatid":["STRING", ""]
                               }

#服务器广播炸弹结算
class SCRunFastBroadcastBomb:
    def __init__(self):
        self.sc_entity_data = {
                               "players": ["INT32", 0],
                               "players_info": ["INT32", {
                                                "player_seat_id": ["INT32", 0],
                                                "bomb_score": ["INT32", 0],
                                                "player_sum_score": ["INT32", 0]
                               }]


        }


#查询上一轮出牌信息
class SCRunFastQueryLastOutcardInfo:
    def __init__(self):
        self.sc_entity_data = {
                               "players": ["INT32", 0],
                               "players_info": ["INT32", {
                                                "player_seat_id": ["INT32", 0],
                                                "last_out_card_num": ["INT32", 0],
                                                "last_out_card_num_info": ["INT32", {"card":["STRING", ""]}]
                               }]
        }

#服务器通知客户端飘分
class SCRunFastBroadcast_PiaoFen:
    def __init__(self):
        self.sc_entity_data = {
                               "operation_number": ["STRING", ""]}

#通知每个玩家飘分情况
class SCRunFastPiaoFenInfo:
    def __init__(self):
        self.sc_entity_data = {
                                "seat_id": ["INT32", 0],
                                "piaofen_score":["INT32", 0]

        }



#断线重连时，返回玩家飘分信息
class SCRunFastReturnPiaoFenInfo:
    def __init__(self):
        self.sc_entity_data = {
                                "player_num": ["INT32", 0],
                                "player_num_info":["INT32", {
                                                    "seat_id":["INT32", 0],
                                                    "piaofen": ["INT32", 0],
                                }]

        }










#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@ author: Hubery
@ create on: 2018/4/19 17:10
@ file: net_unpack.py
@ site: 
@ purpose: 根据不同的协议，进行协议分类解包
"""
import struct
from midConnectTest.lib.phz.define.protocol_entity import *
from midConnectTest.lib.phz.define.protocol_define import *

class UnPackData:
    #   初始化协议号及包体数据
    def __init__(self):
        self.current_index = 0
        self.result = None
        self.normal_entity_list = [1000, 1001,1004,1005,1006,1007,1009,1010,1012, 1013, 1014, 1016,1017, 1043, 1053, 1047, 1057, 1086,
                                   1021,1023,1024,1025,65534,1027,1028,1033,1034,1036,1037,1039,1041,1103,1044,1045,1102,
                                   5002,5003,5004,5005,5006,5007,5008,5009,5010,5011,5012,5014,5015,5017,5021,2010, 10080,9999,
                                   1021,2532,1061,1062,

                                   ]

    def get_protocol_classify(self, protocol_num):
        classify_list = ProtocolClassify.protocol_classify
        classify = None
        #   拿到协议所属分类
        for key, value in classify_list.items():
            for i in range(len(value)):
                if classify is None:
                    if protocol_num == value[i]:
                        classify = key
                        break
        if classify is not None:
            return classify
        else:
            return None

    def read_int16(self, data):
        value = struct.unpack("<h", data[0: 2])[0]
        return value

    def read_int32(self, data):
        value = struct.unpack("<i", data[0: 4])[0]
        return value

    def read_int64(self, data):
        value = struct.unpack("<q", data[0: 8])[0]
        return value

    def read_string(self, size, data):
        fmt = "<%ds" % size
        value = struct.unpack(fmt, data)[0]
        return value.decode("utf-8")

    def read_string1(self, data):
        size = self.read_int32()
        fmt = "<%ds" % size
        value = struct.unpack(fmt, self.body[self.cur_read_pos:self.cur_read_pos + struct.calcsize(fmt)])[0]
        return value

    def unpack_data(self, protocol_num, protocol_entity, data):
        need_parse_data = data
        entity = protocol_entity()
        entity_data = entity.sc_entity_data
        current_index = 0
        if protocol_num in self.normal_entity_list:
            # print("000000000000",protocol_num)
            for i in entity_data:
                if len(need_parse_data) <= 0 or len(need_parse_data) - current_index <= 0:
                    break
                if entity_data[i][0] == "INT32":
                    if len(need_parse_data) - current_index < 4:
                        break
                    entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                    current_index += 4
                elif entity_data[i][0] == "INT16":
                    if len(need_parse_data) - current_index < 2:
                        break
                    entity_data[i][1] = self.read_int16(need_parse_data[current_index: (current_index + 2)])
                    current_index += 2
                elif entity_data[i][0] == "INT64":
                    if len(need_parse_data) - current_index < 8:
                        break
                    entity_data[i][1] = self.read_int64(need_parse_data[current_index: (current_index + 8)])
                    current_index += 8
                else:
                    size = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                    current_index += 4
                    entity_data[i][1] = self.read_string(size, need_parse_data[current_index: current_index + size])
                    current_index += size

        else:
            if protocol_num == 1002:    # 房间快照
                for i in entity_data:
                    if i == "house_owner":
                        house_owner = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = house_owner
                    if i == "room_status":
                        room_status = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = room_status

                    if i == "sum_jushu":
                        sum_jushu = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = sum_jushu
                    if i == "players":
                        players = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = players
                    if i == "play_finish_num":
                        play_finish_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = play_finish_num




            if protocol_num == 5019:
                self.user_id = None
                for i in entity_data:
                    if i == "banker":
                        banker = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        # print("庄家座位号--->%s"%banker)
                        entity_data[i][1] = banker
                    elif i == "next_banker":
                        next_banker = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        # print("下个庄家的座位号--->>%s"%next_banker)
                        entity_data[i][1] = next_banker
                    elif i == "number_of_remain_":
                        number_of_remain_ = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        # print("还剩下多少局----->>%s"%number_of_remain_)
                        entity_data[i][1] = number_of_remain_

                    elif i == "hu_player_id":
                        hu_player_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        self.user_id = hu_player_id
                        # print("胡牌人的----->>id%s"%hu_player_id)
                        entity_data[i][1] = hu_player_id

                    elif i == "hu_type":
                        hu_type = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        # print("胡牌的类型----->>%s"%hu_type)
                        entity_data[i][1] = hu_type
                    elif i == "hu_card":
                        name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        card = self.read_string(name_len, need_parse_data[current_index: current_index + name_len])
                        current_index += name_len
                        # print("胡的牌------>>%s"%card)
                        entity_data[i][1] = card

                    elif i == "player_sum":
                        player_sum = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4

                        entity_data[i][1] = player_sum

                    elif i == "player_sum_info":
                        num = entity_data['player_sum'][1]
                        if num == 0:
                            break
                        info_data = {}
                        # print("玩家人数----->>%s" % num)
                        for k in range(num):
                            seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            mid = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            name = self.read_string(name_len, need_parse_data[current_index: current_index + name_len])
                            current_index += name_len

                            icon_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            icon = self.read_string(icon_len, need_parse_data[current_index: current_index + icon_len])
                            current_index += icon_len

                            this_score = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            user_sum_score = self.read_int64(need_parse_data[current_index: (current_index + 8)])
                            current_index += 8

                            # print(seat_id ,"玩家座位号")
                            # print(mid, "mid")
                            # print(name, "name")
                            # print(icon, "icon")
                            # print(this_score, "当局分数")
                            # print(user_sum_score,"座位总分数")

                            key_1 = "seat_id_%s" % k
                            key_2 = "mid_%s" % k
                            key_3 = "name_%s"% k
                            key_4 = "icon_%s"% k
                            key_5 = "this_score_%s"% k
                            key_6 = "user_sum_score_%s"% k
                            key_7 = "card_group_num_info_%s"% k
                            key_8 = "ming_tang_num_info_%s" % k

                            info_data[key_1] = seat_id
                            info_data[key_2] = mid
                            info_data[key_3] = name
                            info_data[key_4] = icon
                            info_data[key_5] = this_score
                            info_data[key_6] = user_sum_score

                            card_group_dict = {}
                            if seat_id == self.user_id:
                                card_group_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4
                                # print("牌组的个数---->>>%s"%card_group_num)
                                for j in range(card_group_num):
                                    print( )
                                    card_type = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                    current_index += 4
                                    # print("类型---->>%s"%card_type)
                                    score = self.read_int32(need_parse_data[current_index: (current_index +4)])
                                    current_index += 4
                                    # print("分值---->>%s" % score)
                                    is_hu_card = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                    current_index += 4
                                    # print("是否胡牌---->>%s" % is_hu_card)
                                    cards_sum = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                    current_index += 4
                                    card_list_1 = []
                                    # print("牌数---->>%s" % cards_sum)
                                    for k1 in range(cards_sum):
                                        name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                        current_index += 4
                                        card = self.read_string(name_len, need_parse_data[current_index: current_index + name_len])
                                        current_index += name_len
                                        card_list_1.append(card)
                                    # print("牌列表--->>%s"%card_list_1)
                                    key_card_group_1 = "card_type_%s"% j
                                    key_card_group_2 = "score_%s" % j
                                    key_card_group_3 = "is_hu_card_%s" % j
                                    key_card_group_4 = "cards_sum_%s" % j
                                    key_card_group_5 = "card_list_1%s" % j

                                    card_group_dict[key_card_group_1] = card_type
                                    card_group_dict[key_card_group_2] = score
                                    card_group_dict[key_card_group_3] = is_hu_card
                                    card_group_dict[key_card_group_4] = cards_sum
                                    card_group_dict[key_card_group_5] = card_list_1
                                info_data[key_7] = card_group_dict


                                ming_tang_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4
                                # print("名堂个数------>>%s"%ming_tang_num)
                                mingtang_dict = {}
                                if int(ming_tang_num) > 0:
                                    for mingtang in range(ming_tang_num):
                                        ming_tang_type = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                        current_index += 4
                                        # print("名堂类型------>>%s" % ming_tang_type)
                                        score_type = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                        current_index += 4
                                        # print("分数类型------>>%s" % score_type)
                                        value = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                        current_index += 4
                                        # print("值------>>%s" % value)
                                        key_mingtang_1 = "ming_tang_type_%s" % mingtang
                                        key_mingtang_2 = "score_type_%s" % score_type
                                        key_mingtang_3 = "value_%s" % value
                                        mingtang_dict[key_mingtang_1] = ming_tang_type
                                        mingtang_dict[key_mingtang_2] = score_type
                                        mingtang_dict[key_mingtang_3] = value
                                info_data[key_8] = mingtang_dict
                        entity_data[i][1] = info_data
                    elif i == "dun_sum":
                        dun_sum = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = dun_sum
                        # print("墩上的牌数------>>%s"%dun_sum)

                    elif i == "dun_sum_info":
                        num_1 = entity_data['dun_sum'][1]
                        if num_1 == 0:
                            break
                        info_data_3 = []
                        for i in range(num_1):
                            name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            dun_card= self.read_string(name_len, need_parse_data[current_index: current_index + name_len])
                            current_index += name_len
                            info_data_3.append(dun_card)
                        entity_data["dun_sum_info"][1]["dun_card"] = info_data_3
                        # entity_data[i][1] =

                    elif i =="json":
                        name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        json = self.read_string(name_len, need_parse_data[current_index: current_index + name_len])
                        current_index += name_len
                        entity_data[i][1] = json



            elif protocol_num == 1042:
                for i in entity_data:
                    if i == "operation_num_info":
                        num = entity_data['operation_num'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            mingtang = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            key_1 = "mingtang_%s" % k
                            info_data[key_1] = mingtang
                        entity_data[i][1] = info_data
                    else:
                        if entity_data[i][0] == "INT32":
                            if len(need_parse_data) - current_index < 4:
                                break
                            entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                        else:
                            if entity_data[i][0] == "STRING":
                                size = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4
                                if len(need_parse_data[current_index: current_index + size]) < 1:
                                    break
                                entity_data[i][1] = self.read_string(size,need_parse_data[current_index:current_index + size])
                                current_index += size



            if protocol_num == 5013:
                for i in entity_data:
                    info_data = {}
                    error = None
                    if i == "error_code":
                        error_code = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        error = error_code

                        if error < 0:
                            info_data["error_code"] = error_code
                            entity_data[i][1] = info_data
                            break
                    # print(error,"111111111111111111111111111")
                    if error != -1 and error is not None:
                        seat_id_1 = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        info_data["error_code"] = error
                        info_data["seat_id"] = seat_id_1
                    entity_data[i][1] = info_data


            if protocol_num == 5020:
                    for i in entity_data:
                        if i == "players_num_info":
                            num = entity_data['players_num'][1]
                            if num == 0:
                                break
                            info_data = {}
                            for k in range(num):
                                seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4

                                mid = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4

                                name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4

                                name = self.read_string(name_len, need_parse_data[current_index: current_index + name_len])
                                current_index += name_len

                                icon_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4

                                icon = self.read_string(icon_len, need_parse_data[current_index: current_index + icon_len])
                                current_index += icon_len

                                hu_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4

                                zi_mo_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4

                                dian_pao_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4

                                ti_card = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4

                                pao_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4

                                sum_score = self.read_int64(need_parse_data[current_index: (current_index + 8)])
                                current_index += 8

                                key_1 = "seat_id_%s" % k
                                key_2 = "mid_%s" % k
                                key_3 = "name_%s" % k
                                key_4 = "icon_%s" % k
                                key_5 = "hu_num_%s" % k
                                key_6 = "zi_mo_num_%s" % k
                                key_7 = "dian_pao_num_%s" % k
                                key_8 = "ti_card_%s" % k
                                key_9 = "pao_num_%s"% k
                                key_10 = "sum_score_%s"% k

                                info_data[key_1] = seat_id
                                info_data[key_2] = mid
                                info_data[key_3] = name
                                info_data[key_4] = icon
                                info_data[key_5] = hu_num
                                info_data[key_6] = zi_mo_num
                                info_data[key_7] = dian_pao_num
                                info_data[key_8] = ti_card
                                info_data[key_9] = pao_num
                                info_data[key_10] = sum_score
                            entity_data[i][1] = info_data

                        else:
                            if entity_data[i][0] == "INT32":
                                if len(need_parse_data) - current_index < 4:
                                    break
                                entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4
                            else:
                                if entity_data[i][0] == "STRING":
                                    size = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                    current_index += 4
                                    if len(need_parse_data[current_index: current_index + size]) < 1:
                                        break
                                    # print("剩余字符111", need_parse_data[current_index: current_index + size])
                                    entity_data[i][1] = self.read_string(size,need_parse_data[current_index:
                        current_index + size])
                                    current_index += size

            elif protocol_num == 5022:
                for i in entity_data:
                    if i == "players_info":
                        num = entity_data['players_num'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            this_liu_score = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            player_score = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            key_1 = "seat_id_%s" % k
                            key_2 = "this_liu_score_%s" % k
                            key_3 = "player_score_%s" % k
                            info_data[key_1] = seat_id
                            info_data[key_2] = this_liu_score
                            info_data[key_3] = player_score
                        entity_data[i][1] = info_data
                    else:
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4








            elif protocol_num == 1008:
                for i in entity_data:
                    if i == "user_num_info":
                        num = entity_data['user_num'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            _seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            isAgree = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            key_1 = "_seat_id_%s" % k
                            key_2 = "isAgree_%s" % k

                            info_data[key_1] = _seat_id
                            info_data[key_2] = isAgree
                        entity_data[i][1] = info_data
                    else:
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4



            elif protocol_num == 5016:  # 通知用户做相应的操作
                for i in entity_data:
                    if i == "operation_num_info":
                        num = entity_data['operation_num'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            operation_type = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            card_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            # print("card长度: %s"%card_len )
                            # print("data数据 %s"%need_parse_data[current_index: current_index + card_len],"current_index长度",current_index,"current_index + card_len",current_index + card_len)
                            card = self.read_string(card_len, need_parse_data[current_index: current_index + card_len])
                            current_index += card_len

                            key_1 = "operation_type_%s" % k
                            key_2 = "card_%s" % k

                            info_data[key_1] = operation_type
                            info_data[key_2] = card
                        entity_data[i][1] = info_data
                    else:
                        if entity_data[i][0] == "INT32":
                            if len(need_parse_data) - current_index < 4:
                                break
                            entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                        else:
                            size = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            if len(need_parse_data[current_index: current_index + size]) < 1:
                                break
                            # print("剩余字符111", need_parse_data[current_index: current_index + size])
                            entity_data[i][1] = self.read_string(size,need_parse_data[current_index: current_index + size])
                            current_index += size

            elif protocol_num == 1020:
                for i in entity_data:
                    if i == "cards_num_info":
                        num = entity_data['cards_num'][1]
                        if num == 0:
                            break
                        info_data = {}
                        card_list = []
                        for k in range(num):
                            name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            card = self.read_string(name_len, need_parse_data[current_index: current_index + name_len])
                            current_index += name_len
                            card_list.append(card)
                        info_data["card"] = card_list
                        entity_data[i][1] = info_data
                    else:
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4




            elif protocol_num == 5001:
                for i in entity_data:
                    if i == "card_":
                        num = entity_data['card_num'][1]
                        if num == 0:
                            break
                        cards = []
                        for k in range(num):
                            name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            card_ = self.read_string(name_len, need_parse_data[current_index: current_index + name_len])
                            current_index += name_len
                            cards.append(card_)
                        entity_data[i][1] = cards

                    else:
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4

            elif protocol_num == 5018:
                for i in entity_data:
                    if i == "seat_id":
                        seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = seat_id
                    elif i == "hu_card":
                        name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        hu_card = self.read_string(name_len, need_parse_data[current_index: current_index + name_len])
                        current_index += name_len
                        entity_data[i][1] = hu_card

                    elif i == "player_num":
                        player_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = player_num


                    elif i == "player_num_info":
                        num = entity_data['player_num'][1]
                        # print(num,"人数多少")
                        # print("胡牌人座位号,%s"%entity_data['seat_id'][1])
                        # print("胡牌人牌,%s" % entity_data['hu_card'][1])
                        if num == 0:
                            break
                        info_data = {}
                        card_dict = {}
                        for k in range(num):
                            _seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            # print("座位号--",_seat_id)
                            hu_xi = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            # print("胡息", hu_xi)
                            pao_hu = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            # print("是否跑胡", pao_hu)
                            cards_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            card_list = []
                            for card_ in range(cards_num):
                                name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4
                                card = self.read_string(name_len,need_parse_data[current_index: current_index + name_len])
                                current_index += name_len
                                card_list.append(card)
                            # print("胡牌的牌---%s"%card_list)
                            key_1 = "_seat_id_%s" % k
                            key_2 = "hu_xi_%s" % k
                            key_3 = "pao_hu_%s" % k
                            key_4 = "cards_num_%s" % k
                            key_6 = "cards_num_info_%s"% k

                            info_data[key_1] = _seat_id
                            info_data[key_2] = hu_xi
                            info_data[key_3] = pao_hu
                            info_data[key_4] = cards_num
                            info_data[key_6] = card_list
                        entity_data[i][1] = info_data
                    elif i == "dun_cards_num":
                        dun_cards_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = dun_cards_num



                    elif i == "dun_cards_num_info":
                        num = entity_data['dun_cards_num'][1]
                        if num == 0:
                            break
                        cards_1 = []
                        for k in range(num):
                            name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            card_ = self.read_string(name_len, need_parse_data[current_index: current_index + name_len])
                            current_index += name_len
                            cards_1.append(card_)
                        # print("墩上面的牌数%s"%cards_1)
                        entity_data[i][1] = cards_1

                    elif i == "time":
                        time = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = time

                    elif i == "hand_group_num":
                        if len(need_parse_data) - current_index < 4:
                            break
                        hand_group_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = hand_group_num


                    elif i == "hand_group_num_info":
                        # print("----------------------------")
                        num = entity_data['hand_group_num'][1]
                        # print("手牌牌组数目--->>%s"%num)
                        if num == 0:
                            break
                        info_data_2 = {}
                        for k in range(num):
                            card_type = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            # print("牌组类型--%s"%card_type)
                            card_group_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            # print("该牌组牌数--%s"%card_group_num)
                            key_1 = "card_type_%s" % k
                            key_2 = "card_group_num_%s" % k
                            key_3 = "card_group_num_info_%s" % k
                            card_list = []
                            for i in range(card_group_num):
                                name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4
                                card = self.read_string(name_len, need_parse_data[current_index: current_index + name_len])
                                current_index += name_len
                                card_list.append(card)
                            info_data_2[key_1] = card_type
                            info_data_2[key_2] = card_group_num
                            info_data_2[key_3] = card_list

                        entity_data["hand_group_num_info"][1] = info_data_2






            elif protocol_num == 1011:  # 发牌
                range_num = 0
                for i in entity_data:
                    if entity_data[i][0] == "INT32":
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        range_num = entity_data[i][1]
                        current_index += 4
                    else:
                        card_list = []
                        for j in range(range_num):
                            size = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            card = self.read_string(size, need_parse_data[current_index: current_index + size])
                            card_list.append(card)
                            current_index += size
                        entity_data[i][1] = card_list

            # elif protocol_num == 1012:  # 请求操作返回
            #     # print("1012: %s" % data)
            #     for i in entity_data:
            #         if entity_data["card_num"][1] != 0:
            #             if i == "_card":
            #                 card_list = []
            #                 for x in range(entity_data["card_num"][1]):
            #                     size = self.read_int32(need_parse_data[current_index: (current_index + 4)])
            #                     current_index += 4
            #                     card = self.read_string(size, need_parse_data[current_index: current_index + size])
            #                     card_list.append(card)
            #                     current_index += size
            #                 entity_data['_card'][1] = card_list
            #
            #         if i == "_player":
            #             player_list = {}
            #             if entity_data["player_num"][1] == 0:
            #                 break
            #             for j in range(entity_data["player_num"][1]):
            #                 seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
            #                 current_index += 4
            #
            #                 fen_shu = self.read_int32(need_parse_data[current_index: (current_index + 4)])
            #                 current_index += 4
            #
            #                 zong_fen = self.read_int32(need_parse_data[current_index: (current_index + 4)])
            #                 current_index += 4
            #
            #                 key_1 = "seat_id_%s" % j
            #                 key_2 = "fen_shu_%s" % j
            #                 key_3 = "zong_fen_%s" % j
            #
            #                 player_list[key_1] = seat_id
            #                 player_list[key_2] = fen_shu
            #                 player_list[key_3] = zong_fen
            #             entity_data[i][1] = player_list
            #
            #         if entity_data[i][0] == "INT32":
            #             if len(need_parse_data) - current_index < 4:
            #                 break
            #             entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
            #             if i == 'error_code':
            #                 if entity_data[i][1] == -20:
            #                     break
            #             current_index += 4

            elif protocol_num == 1035:  # 麻将大局结算
                for i in entity_data:
                    if i == "players_info":
                        num = entity_data['players'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            uid = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            name = self.read_string(name_len, need_parse_data[current_index: current_index + name_len])
                            current_index += name_len

                            icon_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            icon = self.read_string(icon_len, need_parse_data[current_index: current_index + icon_len])
                            current_index += icon_len

                            big_zimo_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            small_zimo_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            big_dianpao_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            small_dianpao_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            big_jiepao_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            small_jiepao_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            xxxxxxxx = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            score = self.read_int64(need_parse_data[current_index: (current_index + 8)])
                            current_index += 8

                            key_1 = "seat_id_ %s" % k
                            key_2 = "uid_ %s" % k
                            key_3 = "name_ %s" % k
                            key_4 = "icon_ %s" % k
                            key_5 = "big_zimo_num_ %s" % k
                            key_6 = "small_zimo_num_ %s" % k
                            key_7 = "big_dianpao_num_ %s" % k
                            key_8 = "small_dianpao_num_ %s" % k
                            key_9 = "big_jiepao_num_ %s"% k
                            key_10 = "small_jiepao_num_ %s" % k
                            key_11 = "xxxxxxxx_ %s" % k
                            key_12 = "score_ %s" % k

                            info_data[key_1] = seat_id
                            info_data[key_2] = uid
                            info_data[key_3] = name
                            info_data[key_4] = icon
                            info_data[key_5] = big_zimo_num
                            info_data[key_6] = small_zimo_num
                            info_data[key_7] = big_dianpao_num
                            info_data[key_8] = small_dianpao_num
                            info_data[key_9] = big_jiepao_num
                            info_data[key_10] = small_jiepao_num
                            info_data[key_11] = xxxxxxxx
                            info_data[key_12] = score


                        entity_data[i][1] = info_data

                    else:
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4



            elif protocol_num == 1080: #服务器广播正王和纯王
                for i in entity_data:
                    if i == "zheng_wang":
                        zhengwang_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        zhengwang = self.read_string(zhengwang_len, need_parse_data[current_index: current_index + zhengwang_len])
                        current_index += zhengwang_len
                        entity_data[i][1] = zhengwang

                    elif i == "chun_wang_num_info":
                        num = entity_data['chun_wang_num'][1]

                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            icon_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            chun_wang = self.read_string(icon_len, need_parse_data[current_index: current_index + icon_len])
                            current_index += icon_len

                            key_1 = "chun_wang_%s" % k

                            info_data[key_1] = chun_wang
                        entity_data[i][1] = info_data
                    else:
                        if entity_data[i][0] == "INT32":
                            if len(need_parse_data) - current_index < 4:
                                break
                            entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                        else:
                            size = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            if len(need_parse_data[current_index: current_index + size]) < 1:
                                break
                            entity_data[i][1] = self.read_string(size,need_parse_data[current_index: current_index + size])
                            current_index += size





            elif protocol_num == 1063:
                for i in entity_data:
                    if i == "players_info":
                        num = entity_data['players'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            player_score = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            key_1 = "seat_id_ %s" % k
                            key_2 = "player_score_ %s" % k

                            info_data[key_1] = seat_id
                            info_data[key_2] = player_score

                        entity_data[i][1] = info_data

                    else:
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4

            elif protocol_num == 1092: #服务器通知封东状态
                for i in entity_data:
                    if i == "players_info":
                        num = entity_data['players'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            fengdong_status = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            key_1 = "seat_id_ %s" % k
                            key_2 = "fengdong_status_ %s" % k
                            info_data[key_1] = seat_id
                            info_data[key_2] = fengdong_status
                        entity_data[i][1] = info_data

                    else:
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4

            elif protocol_num == 1031:
                for i in entity_data:
                    if i == "banker":
                        banker = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = banker
                    elif i == "hu_player_id":
                        hu_player_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = hu_player_id
                    elif i == "number_of_remain_":
                        number_of_remain_ = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = number_of_remain_
                    elif i == "hu_type":
                        hu_type = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = hu_type
                    elif i == "hu_card":
                        hu_card_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4

                        hu_card = self.read_string(hu_card_len,need_parse_data[current_index: current_index +hu_card_len])
                        current_index += hu_card_len
                        entity_data[i][1] = hu_card
                    elif i == "hu_player_sum":
                        hu_player_sum = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = hu_player_sum

                    elif i == "hu_player_sum_info":
                        num = entity_data['hu_player_sum'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            key_1 = "seat_id_ %s"% k
                            info_data[key_1] = seat_id
                        entity_data[i][1] = info_data
                    elif i == "players_num":
                        players_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = players_num

                    elif i == "players_num_info":
                        num = entity_data['players_num'][1]

                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            uid = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            userName_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            name = self.read_string(userName_len,need_parse_data[current_index: current_index + userName_len])
                            current_index += userName_len

                            score = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            player_sum_score = self.read_int64(need_parse_data[current_index: (current_index + 8)])
                            current_index += 8

                            group_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4


                            group_num_info = []
                            group_num_info_dict = {}
                            if group_num != 0:
                                for j in range(group_num):
                                    cardname_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                    current_index += 4
                                    cardname = self.read_string(cardname_len,need_parse_data[current_index: current_index + cardname_len])
                                    current_index += cardname_len

                                    card_group_type = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                    current_index += 4

                                    key_group_1 = "cardname_%s"% j
                                    key_group_2 = "card_group_type_%s" % j
                                    group_num_info_dict[key_group_1] = cardname
                                    group_num_info_dict[key_group_2] = card_group_type

                                group_num_info.append(group_num_info_dict)

                            hand_card_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            han_card_info = []
                            for hand in range(hand_card_num):
                                card_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4

                                card = self.read_string(card_len, need_parse_data[current_index: current_index + card_len])
                                current_index += card_len
                                han_card_info.append(card)

                            ming_tang_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4


                            ming_tang_num_info = {}  #名堂info
                            if  int(ming_tang_num) != 0:
                                for mingtang in range(ming_tang_num):
                                    mingtang_type = self.read_int32(need_parse_data[current_index: (current_index +4)])
                                    current_index += 4
                                    mingtang_number = self.read_int32(need_parse_data[current_index: (current_index +4)])
                                    current_index += 4

                                    key_mingtang_1 = "mingtang_type_%s"% mingtang
                                    key_mingtang_2 = "mingtang_number_%s" % mingtang

                                    ming_tang_num_info[key_mingtang_1] = mingtang_type
                                    ming_tang_num_info[key_mingtang_2] = mingtang_number





                            key_1 = "seat_id_%s"% k
                            key_2 = "uid_ %s"% k
                            key_3 = "name_ %s" % k
                            key_4 = "score_ %s" % k
                            key_5 = "player_sum_score_ %s" % k
                            key_6 = "group_num_ %s" % k
                            key_7 = "group_num_info_%s" % k
                            key_8 = "hand_card_num_%s" % k
                            key_9 = "hand_card_num_info_%s" % k
                            key_10 = "ming_tang_num_%s" % k
                            key_11 = "ming_tang_num_info_%s" % k

                            info_data[key_1] = seat_id
                            info_data[key_2] = uid
                            info_data[key_3] = name
                            info_data[key_4] = score
                            info_data[key_5] = player_sum_score
                            info_data[key_6] = group_num
                            info_data[key_7] = group_num_info
                            info_data[key_8] = hand_card_num
                            info_data[key_9] = han_card_info
                            info_data[key_10] = ming_tang_num
                            info_data[key_11] = ming_tang_num_info

                        entity_data[i][1] = info_data
                    elif i == "zha_niao_num":
                        zha_niao_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = zha_niao_num
                    elif i == "zha_niao_num_info":
                        num = entity_data['zha_niao_num'][1]
                        if num == 0:
                            break
                        info_data = []
                        for k in range(num):
                            cards_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            card = self.read_string(cards_len, need_parse_data[current_index:current_index + cards_len])
                            current_index += cards_len
                            info_data.append(card )
                        entity_data[i][1] = info_data
                    elif i == "RoomData":
                        RoomData_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4

                        RoomData = self.read_string(RoomData_len,need_parse_data[current_index: current_index + RoomData_len])
                        current_index += RoomData_len
                        entity_data[i][1] = RoomData
                    elif i == "dun_cards":
                        dun_cards_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        dun_cards = self.read_string(dun_cards_len,need_parse_data[current_index: current_index + dun_cards_len])

                        current_index += dun_cards_len
                        entity_data[i][1] = dun_cards
                        #判断
                        if len(need_parse_data[current_index: current_index + dun_cards_len]) < 1:
                            break


                    elif i == "zhong_ma_players":

                        zhong_ma_players = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
                        entity_data[i][1] = zhong_ma_players

                    elif i == "zhong_ma_players_info":
                        num = entity_data['zhong_ma_players'][1]
                        if num == 0:
                            break
                        info_data = {}

                        for k in range(num):
                            seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            zhong_ma_cards = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            zhong_ma_cards_info = []
                            if int(zhong_ma_cards) != 0:
                                for zhong in range(zhong_ma_cards):
                                    cards_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                    current_index += 4
                                    cards = self.read_string(cards_len, need_parse_data[current_index: current_index +cards_len])

                                    current_index += cards_len
                                    zhong_ma_cards_info.append(cards)

                            key_zhong_ma_1 = "seat_id_%s" % k
                            key_zhong_ma_2 = "zhong_ma_cards_%s" % k
                            key_zhong_ma_3 = "zhong_ma_cards_info_%s" % k
                            info_data[key_zhong_ma_1] = seat_id
                            info_data[key_zhong_ma_2] = zhong_ma_cards
                            info_data[key_zhong_ma_3] = zhong_ma_cards_info
                        entity_data[i][1] = info_data



            elif protocol_num == 1050:
                for i in entity_data:
                    if i == "mingtang_num_info":
                        num = entity_data['mingtang_num'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            mingtang_type = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            key = "mingtang_%s" % k
                            info_data[key] = mingtang_type
                        entity_data[i][1] = info_data
                    else:
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4









            elif protocol_num == 1040:
                for i in entity_data:
                    if i == "supplement_card_num_info":
                        num = entity_data['supplement_card_num'][1]
                        if num == 0:
                            break
                        info_data = {}
                        info_data_list = []
                        for k in range(num):
                            cards_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            cards = self.read_string(cards_len,need_parse_data[current_index: current_index + cards_len])
                            current_index += cards_len
                            info_data_list.append(cards)
                        info_data["card"] = info_data_list

                        entity_data[i][1] = info_data

                    else:
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4


            elif protocol_num == 1081:
                for i in entity_data:
                    if i == "gang_num_info":
                        num = entity_data['gang_num'][1]
                        if num == 0:
                            break
                        info_data = []
                        for k in range(num):
                            cards_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            cards = self.read_string(cards_len,
                                                     need_parse_data[current_index: current_index + cards_len])
                            current_index += cards_len
                            info_data.append(cards)
                        entity_data[i][1]["card"] = info_data





            elif protocol_num == 1018:  # 解散房间
                for i in entity_data:
                    if entity_data[i][0] == "INT32":
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        if i == 'error_code':
                            if entity_data[i][1] == -20:
                                break
                        current_index += 4

                    if entity_data[i][0] == "STRING":
                        size = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4

                        entity_data[i][1] = self.read_string(size, need_parse_data[current_index: current_index + size])
                        current_index += size

                    if i == '_seat_id':
                        isContinue = True
                        seat_id_list = []
                        for j in range(entity_data['agree_player'][1]):
                            if len(need_parse_data) - current_index < 4:
                                isContinue = False
                                break
                            seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            seat_id_list.append(seat_id)
                        if isContinue:
                            entity['_seat_id'][1] = seat_id_list

            elif protocol_num == 1026:
                for i in entity_data:
                    if i == "hand_cards":
                        num = entity_data['hand_card_num'][1]
                        if num == 0:
                            break
                        info_data_dict = {}
                        info_data = []
                        for j in range(num):
                            cards_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            card = self.read_string(cards_len,need_parse_data[current_index: current_index + cards_len])
                            current_index += cards_len
                            info_data.append(card)
                        info_data_dict["card"] = info_data
                        entity_data[i][1] = info_data_dict


                    else:
                        if entity_data[i][0] == "INT32":
                            if len(need_parse_data) - current_index < 4:
                                break
                            entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                        else:
                            size = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            if len(need_parse_data[current_index: current_index + size]) < 1:
                                break
                            entity_data[i][1] = self.read_string(size,need_parse_data[current_index: current_index + size])
                            current_index += size

            elif protocol_num == 1029:
                for i in entity_data:
                    if i == "hand_card":
                        num = entity_data['hand_card_num'][1]
                        if num == 0:
                            break
                        info_data = {}
                        info_data_list = []
                        for k in range(num):
                            cards_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            card = self.read_string(cards_len,need_parse_data[current_index: current_index + cards_len])
                            current_index += cards_len
                            info_data_list.append(card)
                        info_data["card"] = info_data_list
                        entity_data[i][1] = info_data

                    else:
                        if entity_data[i][0] == "INT32":
                            if len(need_parse_data) - current_index < 4:
                                break
                            entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                        else:
                            size = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            if len(need_parse_data[current_index: current_index + size]) < 1:
                                break
                            entity_data[i][1] = self.read_string(size,need_parse_data[current_index: current_index + size])
                            current_index += size




            elif protocol_num == 1022:
                for i in entity_data:
                    if i == "operation_num_info":
                        num = entity_data['operation_num'][1]
                        if num == 0:
                            break
                        info_data = []
                        for j in range(num):
                            operation_type = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            info_data.append(operation_type)
                        entity_data[i][1] =  info_data

                    else:
                        if entity_data[i][0] == "INT32":
                            if len(need_parse_data) - current_index < 4:
                                break
                            entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                        else:
                            size = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            if len(need_parse_data[current_index: current_index + size]) < 1:
                                break
                            entity_data[i][1] = self.read_string(size, need_parse_data[current_index: current_index + size])
                            current_index += size

            elif protocol_num == 1038:
                for i in entity_data:
                    if i == "operation_num_info":
                        num = entity_data['operation_num'][1]
                        if num == 0:
                            break
                        info_data = {}

                        for k in range(num):
                            cards_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            card = self.read_string(cards_len,need_parse_data[current_index: current_index + cards_len])
                            current_index += cards_len

                            _operation_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            operation_type_list = []
                            for _num in range(_operation_num):
                                operation_type = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4
                                operation_type_list.append(operation_type)


                            key_1 = "card_%s"% k
                            key_2 = "_operation_num_%s"% k
                            key_3 = "_operation_info%s"% k

                            info_data[key_1] = card
                            info_data[key_2] = _operation_num
                            info_data[key_3] = operation_type_list
                        entity_data[i][1] =  info_data

                    else:
                        if entity_data[i][0] == "INT32":
                            if len(need_parse_data) - current_index < 4:
                                break
                            entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                        else:
                            size = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            if len(need_parse_data[current_index: current_index + size]) < 1:
                                break
                            entity_data[i][1] = self.read_string(size, need_parse_data[current_index: current_index + size])
                            current_index += size


            elif protocol_num == 1030:
                for i in entity_data:
                    if i == "zhong_ma_players_info":
                        num = entity_data['zhong_ma_players'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            zhong_ma_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            zhong_ma_list = []
                            for _ma in range(zhong_ma_num):
                                cards_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4
                                card = self.read_string(cards_len,need_parse_data[current_index: current_index + cards_len])
                                current_index += cards_len
                                zhong_ma_list.append(card)

                            key_1 = "seat_id_%s"% k
                            key_2 = "zhong_ma_num_%s"% k
                            key_3 = "zhong_ma_card_list_%s"% k

                            info_data[key_1] = seat_id
                            info_data[key_2] = zhong_ma_num
                            info_data[key_3] = zhong_ma_list
                        entity_data[i][1] = info_data

                    else:
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4




            elif protocol_num == 1100:  # 已创建的比赛
                for i in entity_data:
                    if i == "list_info":
                        num = entity_data['list_num'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            game_index = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            club_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            club_name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            club_name = self.read_string(club_name_len,
                                                         need_parse_data[current_index: current_index + club_name_len])
                            current_index += club_name_len

                            room_type_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            room_type = self.read_string(room_type_len,
                                                         need_parse_data[current_index: current_index + room_type_len])
                            current_index += room_type_len

                            wanfa = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            difen = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            room_players = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            total_players = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            real_players = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            rounds_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            innings = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            format = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            state = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            distance_close_time = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            uuid_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            uuid = self.read_string(uuid_len, need_parse_data[current_index: current_index + uuid_len])
                            current_index += uuid_len

                            key_1 = "game_index_%s" % k
                            key_2 = "club_id_%s" % k
                            key_3 = "club_name_%s" % k
                            key_4 = "room_type_%s" % k
                            key_5 = "wanfa_%s" % k
                            key_6 = "difen_%s" % k
                            key_7 = "room_players_%s" % k
                            key_8 = "total_players_%s" % k
                            key_9 = "real_players_%s" % k
                            key_10 = "rounds_num_%s" % k
                            key_11 = "innings_%s" % k
                            key_12 = "format_%s" % k
                            key_13 = "state_%s" % k
                            key_14 = "distance_close_time_%s" % k
                            key_15 = "uuid_%s" % k

                            info_data[key_1] = game_index
                            info_data[key_2] = club_id
                            info_data[key_3] = club_name
                            info_data[key_4] = room_type
                            info_data[key_5] = wanfa
                            info_data[key_6] = difen
                            info_data[key_7] = room_players
                            info_data[key_8] = total_players
                            info_data[key_9] = real_players
                            info_data[key_10] = rounds_num
                            info_data[key_11] = innings
                            info_data[key_12] = format
                            info_data[key_13] = state
                            info_data[key_14] = distance_close_time
                            info_data[key_15] = uuid
                        entity_data[i][1] = info_data

                    else:
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4

            elif protocol_num == 1101:  # 所在俱乐部比赛
                for i in entity_data:
                    if i == "list_info":
                        num = entity_data['list_num'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            club_icon_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            club_icon = self.read_string(club_icon_len,
                                                         need_parse_data[current_index: current_index + club_icon_len])
                            current_index += club_icon_len

                            club_name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            club_name = self.read_string(club_name_len,
                                                         need_parse_data[current_index: current_index + club_name_len])
                            current_index += club_name_len

                            club_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            game_index = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            room_type_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            room_type = self.read_string(room_type_len,
                                                         need_parse_data[current_index: current_index + room_type_len])
                            current_index += room_type_len

                            wanfa = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            difen = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            room_players = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            total_players = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            real_players = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            rounds_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            innings = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            format = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            state = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            distance_close_time = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            uuid_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            uuid = self.read_string(uuid_len, need_parse_data[current_index: current_index + uuid_len])
                            current_index += uuid_len

                            key_1 = "club_icon_%s" % k
                            key_2 = "club_name_%s" % k
                            key_3 = "club_id_%s" % k
                            key_4 = "game_index_%s" % k
                            key_5 = "room_type_%s" % k
                            key_6 = "wanfa_%s" % k
                            key_7 = "difen_%s" % k
                            key_8 = "room_players_%s" % k
                            key_9 = "total_players_%s" % k
                            key_10 = "real_players_%s" % k
                            key_11 = "rounds_num_%s" % k
                            key_12 = "innings_%s" % k
                            key_13 = "format_%s" % k
                            key_14 = "state_%s" % k
                            key_15 = "distance_close_time_%s" % k
                            key_16 = "uuid_%s" % k

                            info_data[key_1] = club_icon
                            info_data[key_2] = club_name
                            info_data[key_3] = club_id
                            info_data[key_4] = game_index
                            info_data[key_5] = room_type
                            info_data[key_6] = wanfa
                            info_data[key_7] = difen
                            info_data[key_8] = room_players
                            info_data[key_9] = total_players
                            info_data[key_10] = real_players
                            info_data[key_11] = rounds_num
                            info_data[key_12] = innings
                            info_data[key_13] = format
                            info_data[key_14] = state
                            info_data[key_15] = distance_close_time
                            info_data[key_16] = uuid
                        entity_data[i][1] = info_data

                    else:
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4
            #-------------------------------------------------跑得快
            elif protocol_num == 2520:  # 发牌
                for i in entity_data:
                    if i == "card_num_info":
                        num = entity_data['card_num'][1]
                        if num == 0:
                            break
                        info_data = []
                        for k in range(num):
                            uuid_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            card = self.read_string(uuid_len, need_parse_data[current_index: current_index + uuid_len])
                            current_index += uuid_len
                            info_data.append(card)
                        entity_data[i][1] = info_data

                    else:
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4

            elif protocol_num == 1022:  # 发牌
                for i in entity_data:
                    if i == "operation_num_info":
                        num = entity_data['operation_num'][1]
                        if num == 0:
                            break
                        info_data = []
                        for k in range(num):
                            operation_type = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            info_data.append(operation_type)
                        entity_data[i][1] = info_data

                    else:
                        if entity_data[i][0] == "INT32":
                            if len(need_parse_data) - current_index < 4:
                                break
                            entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                        else:
                            size = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            if len(need_parse_data[current_index: current_index + size]) < 1:
                                break
                            entity_data[i][1] = self.read_string(size, need_parse_data[current_index: current_index + size])
                            current_index += size



            elif protocol_num == 2523:  # 出牌
                for i in entity_data:
                    if i == "out_card_num_info":
                        num = entity_data['out_card_num'][1]
                        if num == 0:
                            break
                        info_data = []
                        for k in range(num):
                            operation_type = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            info_data.append(operation_type)
                        entity_data[i][1] = info_data

                    else:
                        if entity_data[i][0] == "INT32":
                            if len(need_parse_data) - current_index < 4:
                                break
                            entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                        else:
                            size = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            if len(need_parse_data[current_index: current_index + size]) < 1:
                                break
                            entity_data[i][1] = self.read_string(size,
                                                                 need_parse_data[current_index: current_index + size])
                            current_index += size


            elif protocol_num == 2531:  # 小局结算
                for i in entity_data:
                    if i == "player_sum_info":
                        num = entity_data['player_num'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            seatid = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            uid = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            name = self.read_string(name_len, need_parse_data[current_index: current_index + name_len])
                            current_index += name_len

                            icou_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            icou = self.read_string(icou_len, need_parse_data[current_index: current_index + icou_len])
                            current_index += icou_len

                            bomb_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            this_is_score = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            player_score = self.read_int64(need_parse_data[current_index: (current_index + 8)])
                            current_index += 8

                            ChunTian = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            PiaoFei_score = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            out_card_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            out_card_num_info = {}
                            for i in range(out_card_num):
                                card_type = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4

                                card_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4

                                card_list = []
                                for i in range(card_num):
                                    icou_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                    current_index += 4
                                    card = self.read_string(icou_len,need_parse_data[current_index: current_index + icou_len])
                                    current_index += icou_len
                                    card_list.append(card)

                                key_1 = "card_type_%s"% i
                                key_2 = "card_num_%s" % i
                                key_3 = "card_list_%s" % i

                                out_card_num_info[key_1] = card_type
                                out_card_num_info[key_2] = card_num
                                out_card_num_info[key_3] = card_list

                            hand_card_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            hand_card_list = []

                            for card_num in range(hand_card_num):
                                card_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4
                                card = self.read_string(card_len,need_parse_data[current_index: current_index + card_len])
                                current_index += card_len

                                hand_card_list.append(card)

                            String_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            print(need_parse_data[current_index: current_index + String_len])

                            String = self.read_string(String_len, need_parse_data[current_index: current_index + String_len])
                            current_index += String_len


                            key_1 = "seatid_ %s" % k
                            key_2 = "uid_ %s" % k
                            key_3 = "name_ %s" % k
                            key_4 = "icou_ %s" % k
                            key_5 = "bomb_num_ %s" % k
                            key_6 = "this_is_score_ %s" % k
                            key_7 = "player_score_ %s" % k
                            key_8 = "ChunTian_ %s" % k
                            key_9 = "PiaoFei_score_ %s" % k
                            key_10 = "out_card_num_ %s" % k
                            key_11 = "out_card_num_info_ %s" % k
                            key_12 = "hand_card_num_ %s" % k
                            key_13 = "hand_card_list_ %s" % k
                            key_14 = "String_ %s" % k

                            info_data[key_1] = seatid
                            info_data[key_2] = uid
                            info_data[key_3] = name
                            info_data[key_4] = icou
                            info_data[key_5] = bomb_num
                            info_data[key_6] = this_is_score
                            info_data[key_7] = player_score
                            info_data[key_8] = ChunTian
                            info_data[key_9] = PiaoFei_score
                            info_data[key_10] = out_card_num
                            info_data[key_11] = out_card_num_info
                            info_data[key_12] = hand_card_num
                            info_data[key_13] = hand_card_list
                            info_data[key_14] = String

                        entity_data[i][1] = info_data

                    else:
                        if entity_data[i][0] == "INT32":
                            if len(need_parse_data) - current_index < 4:
                                break
                            entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                        else:
                            size = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            if len(need_parse_data[current_index: current_index + size]) < 1:
                                break
                            entity_data[i][1] = self.read_string(size,
                                                                 need_parse_data[current_index: current_index + size])
                            current_index += size


            elif protocol_num == 2535:  # 跑得快大局结算
                for i in entity_data:
                    if i == "players_info":
                        num = entity_data['players'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            uid = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            name_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            name = self.read_string(name_len, need_parse_data[current_index: current_index + name_len])
                            current_index += name_len

                            icon_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            icon = self.read_string(icon_len, need_parse_data[current_index: current_index + icon_len])
                            current_index += icon_len

                            score = self.read_int64(need_parse_data[current_index: (current_index + 8)])
                            current_index += 8

                            bomb_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            win_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            lost_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            small_max_score = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            key_1 = "seat_id_ %s" % k
                            key_2 = "uid_ %s" % k
                            key_3 = "player_name_ %s" % k
                            key_4 = "player_icon_ %s" % k
                            key_5 = "player_sum_score_ %s" % k
                            key_6 = "bomb_num_ %s" % k
                            key_7 = "win_num_ %s" % k
                            key_8 = "lost_num_ %s" % k
                            key_9 = "small_max_score_ %s"% k

                            info_data[key_1] = seat_id
                            info_data[key_2] = uid
                            info_data[key_3] = name
                            info_data[key_4] = icon
                            info_data[key_5] = score
                            info_data[key_6] = bomb_num
                            info_data[key_7] = win_num
                            info_data[key_8] = lost_num
                            info_data[key_9] = small_max_score

                        entity_data[i][1] = info_data
                    else:
                        if entity_data[i][0] == "INT32":
                            if len(need_parse_data) - current_index < 4:
                                break
                            entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                        else:
                            size = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            if len(need_parse_data[current_index: current_index + size]) < 1:
                                break
                            entity_data[i][1] = self.read_string(size,need_parse_data[current_index: current_index + size])

                            current_index += size
            elif protocol_num == 2536:
                for i in entity_data:
                    if i == "players_info":
                        num = entity_data['players'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            player_seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            bomb_score = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            player_sum_score = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            key_1 = "player_seat_id_ %s" % k
                            key_2 = "bomb_score_ %s" % k
                            key_3 = "player_sum_score_ %s" % k
                            info_data[key_1] = player_seat_id
                            info_data[key_2] = bomb_score
                            info_data[key_3] = player_sum_score
                        entity_data[i][1] = info_data
                    else:
                        if entity_data[i][0] == "INT32":
                            if len(need_parse_data) - current_index < 4:
                                break
                            entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4


            elif protocol_num == 2537:
                for i in entity_data:
                    if i == "players_info":
                        num = entity_data['players'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            player_seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            last_out_card_num = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            last_out_card_num_info = []
                            for i in range(last_out_card_num):
                                icon_len = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                                current_index += 4
                                card = self.read_string(icon_len,need_parse_data[current_index: current_index + icon_len])
                                current_index += icon_len
                                last_out_card_num_info.append(card)

                            key_1 = "player_seat_id_ %s" % k
                            key_2 = "last_out_card_num_ %s" % k
                            key_3 = "last_out_card_num_info_ %s" % k
                            info_data[key_1] = player_seat_id
                            info_data[key_2] = last_out_card_num
                            info_data[key_3] = last_out_card_num_info
                        entity_data[i][1] = info_data

                    else:
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4


            elif protocol_num == 1063:
                for i in entity_data:
                    if i == "player_num_info":
                        num = entity_data['player_num'][1]
                        if num == 0:
                            break
                        info_data = {}
                        for k in range(num):
                            seat_id = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4

                            piaofen = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                            current_index += 4
                            key_1 = "seat_id_ %s" % k
                            key_2 = "piaofen_ %s" % k
                            info_data[key_1] = seat_id
                            info_data[key_2] = piaofen

                        entity_data[i][1] = info_data

                    else:
                        if len(need_parse_data) - current_index < 4:
                            break
                        entity_data[i][1] = self.read_int32(need_parse_data[current_index: (current_index + 4)])
                        current_index += 4

        self.result = entity_data
        return entity_data

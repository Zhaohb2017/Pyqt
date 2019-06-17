#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@ author: guess
@ effect:
@ Time : 2018/9/27 15:26
"""

from midConnectTest.common.common_api import *
import logging,time


class PublicTestApi():
    def __init__(self,version,different="local"):
        super(PublicTestApi,self).__init__()
        self.version = version
        self.different=different
        self.many_users = []  # 所有进入房间的用户

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
            print("多人登录成功...")
            return player_list
        else:
            return False

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
            print("%s 创建房间成功...,房间号: %s" % (player.user_mid, player.room_id))
            return player.room_id
        else:
            return False


    #   多人申请加入房间
    def api_enter_room_more_with_check(self, player_list, room_id):
        if type(player_list) is not list:
            raise logging.error("你调用错接口了...此接口是调用多人加入房间的")
        #   结果准备
        result_list = []
        update_dataa = {"room_id": room_id}

        #   循环申请加入房间及判断
        for player in player_list:
            print("玩家: %s 加入房间"%player.user_mid)
            player.phz_requests_enter_room(update_dataa)

            print()


            result_list.append(player)

        if len(result_list) is len(player_list):
            print("%s个人加入房间成功..." % len(player_list))
            return True
        else:
            raise False


    def enter_room_and_ready(self,mid_list,room_type,games_number
                                 ,options,people_number,zhua_niao
                                 ,wanfa

                             ):
        login_users = self.api_login_more_with_check(login_account_list=mid_list) #登录状态
        if login_users is False:
            return "登录失败"
        else:
            create_room_data = {"gameRoomType": room_type, "gameCishu": games_number, "gameXuanXiang": options, "gamePlayer": people_number,
                                "gameZhama": zhua_niao, "gameWanFa": wanfa}
            room_id = self.api_create_room_with_check(login_users[0],create_room_data)

            if room_id is False:
                return login_users[0].create_error #错误信息
            else:
                enter_room = self.api_enter_room_more_with_check(player_list=login_users, room_id=room_id)
                print("enter_room: %s"%enter_room)
                for i in login_users:
                    print("玩家加入房间状态: %s" % i.join_room_status)
                    if i.join_room_status is False: #判断玩家是否加入房间
                        return "找不到房间号,请再次创建"

                if enter_room:
                    return "加入房间成功"
                else:
                    return "加入房间失败"





if __name__ == "__main__":
    p = PublicTestApi(version="ChangSha")
    s = p.enter_room_and_ready(mid_list=[50080,50161],room_type="105",
                               games_number = 8,options = 268614655,people_number = 3,
                               zhua_niao = 0,wanfa=135168
                               )
    print(s)









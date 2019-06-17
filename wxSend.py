# 导入模块
from wxpy import *
# 初始化机器人，扫码登陆
bot = Bot('bot.pkl')


def valid_msg(msg):
    return "发财" in msg.text.lower()


def invite(user):
    group = bot.groups().search('"www体验区"')
    group[0].add_members(user,use_invitation=True)


@bot.register(msg_types=FRIENDS)
def new_friends(msg):
    user = msg.card.accept()
    if valid_msg(msg):
        invite(user)
    else:
        user.send("hello {}, 找密码去吧".format(user.name))


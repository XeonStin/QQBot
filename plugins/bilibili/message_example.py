# 链接卡片形式，群发会被风控无法发送，私发可以
message = f"[CQ:share,url=https://live.bilibili.com/{ room_id },title={ user_information['info']['uname'] } 开播了,content={ room_status['title'] },image={ room_status['user_cover'] }]"

# XML 卡片，群发会被风控无法发送，私发可以
message_XML = '[CQ:xml,data=' + escape(f'''<?xml version='1.0' encoding='UTF-8' standalone='yes'?><msg templateID='123' url='https://live.bilibili.com/{ room_id }' serviceID='1' action='web' actionData='' a_actionData='' i_actionData='' brief='开播提醒' flag='0'><item layout='2'><picture cover='{ room_status['user_cover'] }'/><title>{ user_information['info']['uname'] }</title><summary>{ room_status['title'] }</summary></item><source url='' icon='' name='botbot' appid='0' action='' actionData='' a_actionData='' i_actionData=''/></msg>''') + ']'

# 文字+链接+图片形式，群发会被风控无法发送，私发可以

message_with_img = escape(f"\
{ user_information['info']['uname'] } 开播了：{ room_status['title'] }\n\
https://live.bilibili.com/{ room_id }\n\
[CQ:image,file={ room_status['user_cover'] },type=show]")

# 文字+链接形式，群发会被风控无法发送，私发可以
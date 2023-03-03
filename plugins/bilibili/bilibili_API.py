import requests
import json


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'}


async def get_room_status(room_id: str):
    payload = {'room_id': room_id}
    res = requests.get('https://api.live.bilibili.com/room/v1/Room/get_info', headers=headers, params=payload)
    res.encoding = 'utf-8'
    room_status = json.loads(res.text)['data']
    # logger.info('status: ' + str(room_status))
    return room_status


async def get_user_information(uid: str):
    payload = {'uid': uid}
    res = requests.get('https://api.live.bilibili.com/live_user/v1/Master/info', headers=headers, params=payload)
    res.encoding = 'utf-8'
    user_information = json.loads(res.text)['data']
    # logger.info('status: ' + str(room_status))
    return user_information

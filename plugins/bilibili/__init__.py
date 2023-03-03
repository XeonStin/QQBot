import datetime
from typing import List

from aiocqhttp.message import escape

import nonebot
from nonebot import on_command, CommandSession
from nonebot.log import logger

from .bilibili_API import get_room_status, get_user_information
from .routing_config import routing_table


LOOKUP_INTERVAL_SECOND = 60
NEW_ROOM_THRESHOLD_SECOND = LOOKUP_INTERVAL_SECOND + 6


@nonebot.scheduler.scheduled_job('interval', seconds=LOOKUP_INTERVAL_SECOND, start_date=datetime.datetime.now() + datetime.timedelta(seconds=5))
async def check_new_rooms():
    bot = nonebot.get_bot()
    for routing in routing_table:
        room_id   = routing['room_id']
        message = await check_room(room_id, LOOKUP_INTERVAL_SECOND)

        if message != '':
            user_ids  = routing['user_ids']
            group_ids = routing['group_ids']

            for user_id in user_ids:
                await bot.send_private_msg(user_id=user_id, message=message)

            for group_id in group_ids:
                await bot.send_group_msg(group_id=group_id, message=message)


@on_command('check_room')
async def _(session: CommandSession):
    room_id = session.current_arg_text.strip()
    message = await check_room(room_id, 0)
    if message != '':
        await session.send(message)
    else:
        await session.send(escape('主播在摸鱼捏'))


async def check_room(room_id: str, new_room_threshold: int) -> str:
    logger.info(f'Checking for room {room_id}')
    message = ''

    room_status = await get_room_status(room_id)
    if room_status['live_status'] == 1:
        # 正在直播
        start_time = datetime.datetime.strptime(room_status['live_time'], '%Y-%m-%d %H:%M:%S')
        now_time = datetime.datetime.now()
        duration = now_time - start_time
        logger.info(room_id + ' duration: ' + str(duration.seconds) + ' s')
        
        if duration.seconds < new_room_threshold or new_room_threshold == 0:
            # 刚开播
            user_information = await get_user_information(str(room_status['uid']))

            message = escape(f"\
{ user_information['info']['uname'] } 开播了：{ room_status['title'] }\n\
https://live.bilibili.com/{ room_id }")
    
    return message

from nonebot.default_config import *

HOST = '127.0.0.1'  # 对应 CQHTTP 设置
PORT = 8848         # 同上

DEBUG = False       # 调试模式

NICKNAME = 'bot'

SUPERUSERS = {123456789}    # 超级用户：一般用自己的 QQ 号
COMMAND_START = {'/'}       # 指令前缀

DEFAULT_COMMAND_PERMISSION = lambda s: s.is_superuser   # 默认权限：仅允许超级用户

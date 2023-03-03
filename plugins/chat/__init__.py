from typing import Dict

from aiocqhttp.message import escape

from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import render_expression
from nonebot.log import logger

from .ChatGPT_API import ChatGPTConversation
from .permission_checker import simple_allow_list
from .sensitive_config import sensitive_words, user_whitelist, group_whitelist


usage_permission = simple_allow_list(user_ids=user_whitelist, group_ids=group_whitelist)


EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～'
)

EXPR_NO_COMMENT = (
    '刚才我很想啊，就我每次碰到你们，我就想到 — — 中国有句话叫“闷声发大财”。', 
    '明白这个意思吗？！ 你们呀，不要想喜欢，然后弄个大新闻！', 
    '你们啊，Naive Naive。你们呀……I Am Angry，我跟你讲，你们这样子那不行的。我今天算得罪了你们一下。', 
    '我就什么话也不说 — — 这是最好的！ 但是我想我见到你们这样热情呀，一句话不说也不好。 所以刚才你一定要…… 在宣传上将来如果你们报道上有偏差，你们要负责！', 
    '你们有一个好，全世界跑到什么地方，你们比其他的西方记者跑得还快，但是问来问去的问题呀，都too simple, 啊，sometimes naive！懂了没啊？！', 
    '刚才你们问我呀，我可以回答你一句“无可奉告”。弄得你们也不高兴，那怎么办？！', 
    '还是要提高自己的姿势水平。识得唔识得呀？'
)


def get_conversation_id(session: CommandSession):
    if 'group_id' in session.event:
        conversation_id = session.event['group_id']
    else: 
        conversation_id = session.event['user_id']

    conversation_id = str(conversation_id)
    return conversation_id


# 指令部分

conversations: Dict[str, ChatGPTConversation] = {}

@on_command('ChatGPT', aliases='chat')
async def _(session: CommandSession):
    message = session.state.get('message')
    if message == None:
        message = session.current_arg_text.strip()
    
    logger.info(f'ChatGPT: Entering command session with: {message}')

    message_id = session.event['message_id']
    user_id = session.event['user_id']
    reply_header = f'[CQ:reply,id={message_id}][CQ:at,qq={user_id}] [CQ:at,qq={user_id}]'

    if 'group_id' not in session.event:
        reply_header = ''

    conversation_id = get_conversation_id(session)
    if conversation_id not in conversations:
        conversations[conversation_id] = ChatGPTConversation()
    
    reply = await conversations[conversation_id].ask(message)

    if reply:
        # 判断敏感词
        for word in sensitive_words:
            if word in reply:
                conversations[conversation_id].withdraw()
                await session.send(reply_header + render_expression(EXPR_NO_COMMENT))
                return 
            
        # 如果调用 GPT 成功，得到了回复，则转义之后发送给用户
        # 转义会把消息中的某些特殊字符做转换，避免将它们理解为 CQ 码
        await session.send(reply_header + escape(reply))
    else:
        # 如果调用失败，或者它返回的内容我们目前处理不了，发送无法获取 GPT 回复时的「表达」
        # 这里的 render_expression() 函数会将一个「表达」渲染成一个字符串消息
        logger.warning('ChatGPT: Reply is None')
        await session.send(reply_header + render_expression(EXPR_DONT_UNDERSTAND))


@on_command('ChatGPT_clear', aliases='clear')
async def _(session: CommandSession):
    conversation_id = get_conversation_id(session)
    if conversation_id in conversations:
        conversations.pop(conversation_id)

    logger.info(f'ChatGPT: History cleared for: {conversation_id}')
    await session.send(escape('Conversation history cleared'))


@on_command('ChatGPT_get_history', aliases='history')
async def _(session: CommandSession):
    conversation_id = get_conversation_id(session)
    if conversation_id in conversations:
        await session.send(escape(str(conversations[conversation_id].history_messages)))
    else:
        await session.send(escape('当前会话无内容'))


@on_command('no_comment')
async def _(session: CommandSession):
    message_id = session.event['message_id']
    user_id = session.event['user_id']
    reply_header = f'[CQ:reply,id={message_id}][CQ:at,qq={user_id}] [CQ:at,qq={user_id}]'
    await session.send(reply_header + render_expression(EXPR_NO_COMMENT))


@on_command('好好好')
async def _(session: CommandSession):
    await session.send(escape('好好好'))

    
@on_command('fsndl')
async def _(session: CommandSession):
    await session.send(escape('fsndlfsndlfsndl'))


# 自然语言处理部分

@on_natural_language(keywords=sensitive_words, permission=usage_permission)
async def _(session: NLPSession):
    return IntentCommand(90.0, 'no_comment')


@on_natural_language(keywords={'好好好'}, permission=lambda sender: sender.is_superuser, only_to_me=False)
async def _(session: NLPSession):
    return IntentCommand(90.0, '好好好')


@on_natural_language(keywords={'fsndl'}, permission=lambda sender: sender.is_superuser, only_to_me=False)
async def _(session: NLPSession):
    return IntentCommand(90.0, 'fsndl')


@on_natural_language(permission=usage_permission, only_short_message=False)
async def _(session: NLPSession):
    # 以置信度 60.0 返回
    # 确保任何消息都在且仅在其它自然语言处理器无法理解的时候使用 GPT 命令
    text = session.msg_text
    return IntentCommand(60.0, 'ChatGPT', args={'message': text})

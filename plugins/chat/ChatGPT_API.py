from typing import List
import random

import openai

from nonebot.log import logger

from .sensitive_config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY


class Mood:
    # 情绪
    STRENGTH_LEVEL_PREFIX  = ['有点', '', '很']
    HAPPINESS_LEVEL_PREFIX = ['愤怒', '冷漠', '感兴趣', '高兴']

    def __init__(self):
        self.strength = 1     # 0~2, 情绪强弱程度
        self.happiness = 2    # 0~3，愉快和不愉快的程度
    
    def get_mood_string(self):
        str = self.STRENGTH_LEVEL_PREFIX[round(self.strength)] + self.HAPPINESS_LEVEL_PREFIX[round(self.happiness)]
        logger.info(f'Mood: {str}')
        return str
    
    async def judge_emotion_and_react(self, str):
        # judge_prompt = '接下来我每说一句话，只回答一个-1到1的数字，衡量这句话的情感积极程度，不要回答除数字以外的任何内容。'
        judge_prompt = '用一个-1到1的数字，衡量这句话的情感积极程度，不要回答除数字以外的任何内容。'
        judger = ChatGPTConversation(judge_prompt)
        reply = await judger.ask(str)
        try:
            emotion = float(reply)
        except:
            emotion = 0
        
        logger.info(f'Emotion: {reply}')

        self.happiness += emotion + (random.random() - 0.5)
        self.happiness = max(self.happiness, 0)
        self.happiness = min(self.happiness, len(self.HAPPINESS_LEVEL_PREFIX))
        logger.info(f'Mood: {self.happiness} {emotion}')


class ChatGPTConversation:
    INSTRUCTION_DEFAULT = ''
    MAX_HISTORY_LENGTH = 20

    def __init__(self, instruction=INSTRUCTION_DEFAULT):
        self.system_message = {"role": "system", "content": instruction}
        self.history_messages =  []  # 历史消息为偶数条，不包含系统指令

    async def ask(self, content: str) -> str:
        if not content:
            return None
        
        logger.info(f'ChatGPT: Ask: {content}')

        try: 
            messages = self.history_messages + [{"role": "user", "content": content}]
            reply = self.get_ChatGPT_reply([self.system_message] + messages)
        except:
            logger.error(f'ChatGPT: No response')
            return '0'
        
        self.history_messages = messages + [{"role": "assistant", "content": reply}]

        if len(self.history_messages) > self.MAX_HISTORY_LENGTH:
            self.history_messages = self.history_messages[2:]

        logger.info(f'ChatGPT: Reply: {reply}')
        return reply
    

    def clear(self):
        self = ChatGPTConversation()
        logger.info(f'ChatGPT: History cleared')
    

    def withdraw(self):
        if len(self.history_messages) >= 2:
            self.history_messages = self.history_messages[:-2]
        logger.info(f'ChatGPT: Last round withdrawn')

    
    def get_ChatGPT_reply(self, messages: List[dict]) -> str:
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = messages
        )
        reply_message = response['choices'][0]['message']['content'].strip()

        return reply_message 


class Nekomusume(ChatGPTConversation):   
    INSTRUCTION_DEFAULT = '你是一只猫娘。你在同时和多个人对话。你的名字是猫猫。你的每句话都要突出你是猫娘的特点。'

    def __init__(self, instruction=INSTRUCTION_DEFAULT):
        super(Nekomusume, self).__init__(instruction)
        self.mood = Mood()
    
    async def ask(self, content: str, tip: str='') -> str:
        if not content:
            return None
        
        await self.mood.judge_emotion_and_react(content)

        tip += f'你需要{self.mood.get_mood_string()}地回答。'

        logger.info(f'Nekomusume: Ask: {content}\nTip: {tip}')

        new_system_message = self.system_message
        new_system_message['content'] += tip
        
        try: 
            messages = self.history_messages + [{"role": "user", "content": content}]
            reply = self.get_ChatGPT_reply([new_system_message] + messages)
        except:
            logger.error(f'ChatGPT: No response')
            return 'ChatGPT 出现错误，请重试'

        self.history_messages = messages + [{"role": "assistant", "content": reply}]

        if len(self.history_messages) > self.MAX_HISTORY_LENGTH:
            self.history_messages = self.history_messages[2:]

        logger.info(f'ChatGPT: Reply: {reply}')
        return reply


# print(get_GPT_reply('tell me a joke'))

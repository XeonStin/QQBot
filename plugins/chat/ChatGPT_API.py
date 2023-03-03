from typing import List

import openai

from nonebot.log import logger

from .sensitive_config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY


class ChatGPTConversation:
    INSTRUCTION_DEFAULT = "You are a helpful assistant."
    MAX_HISTORY_LENGTH = 10


    def __init__(self):
        # self.history_messages =  [{"role": "system", "content": instruction}]
        self.history_messages =  []
    

    async def ask(self, content: str):
        logger.info(f'ChatGPT: Ask: {content}')
        if not content:
            return None
        
        try: 
            messages = self.history_messages + [{"role": "user", "content": content}]
            reply = await self.get_ChatGPT_reply(messages)
        except:
            logger.error(f'ChatGPT: No response')
            return 'ChatGPT 出现错误，请重试'
        
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


    async def get_ChatGPT_reply(self, messages: List[dict]):
        response = await openai.ChatCompletion.acreate(
            model = "gpt-3.5-turbo",
            messages = messages,
            request_timeout = 5
        )
        reply_message = response['choices'][0]['message']['content'].strip()

        return reply_message 


# print(get_GPT_reply('tell me a joke'))

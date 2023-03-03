# QQBot

基于 NoneBot 的 QQ 机器人，可以：

* 调用 OpenAI 提供的 ChatGPT API 聊天

* 在特定 bilibili 主播开播时发送开播通知

## 使用方法

1. 按照 [NoneBot 指南](https://docs.nonebot.dev/guide/installation.html) 配置 CQHTTP

1. 将 `./config_example.py` 重命名为 `config.py` 并修改

    `HOST`, `PORT` 按照 CQHTTP 对应修改

    添加 `SUPERUSERS`

1. 将 `./plugins/chat/sensitive_config_example.py` 重命名为 `sensitive_config.py` 并修改

    `OPENAI_API_KEY` 填写从 [Open AI](https://platform.openai.com/account/api-keys) 获取的 API Key
    
    添加 `user_whitelist`, `group_whitelist`

1. 将 `./plugins/bilibili/routing_config_example.py` 重命名为 `routing_config.py` 并修改

    填写 `room_id`、`user_ids`、`group_ids`

1. 其他定制需求修改可参照 [NoneBot 文档](https://docs.nonebot.dev/guide/)

1. 运行 CQHTTP

1. 运行 `./bot.py`，bot 上线

1. 私聊 bot 或在群里 @bot 即可使用

## 具体模块

### chat

### bilibili

---

By Xeon Stin

XeonStin@126.com

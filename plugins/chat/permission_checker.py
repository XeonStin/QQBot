from typing import Container

from nonebot.permission import SenderRoles
from nonebot.typing import PermissionPolicy_T


def simple_allow_list(*, user_ids: Container[int] = ...,
                      group_ids: Container[int] = ...,
                      reverse: bool = False) -> PermissionPolicy_T:
    """
    产生一个对应着白名单的权限检查策略。新的权限检查策略只有在发送者的 QQ 号来自于 `user_ids` 或者群组属于 `group_ids` 时才会返回 `True`。
    推荐使用者查看此函数的实现并尝试书写自己的权限检查器。
    参数:
        user_ids {version}`1.8.2+`: 要加入白名单的 QQ 号们，默认为空
        group_ids {version}`1.8.2+`: 要加入白名单的群号们，默认为空
        reverse: 如果为真，则返回值变为黑名单
    返回:
        PermissionPolicy_T: 新的权限检查策略
    用法:
        ```python
        bans_list = simple_allow_list(group_ids={ 123456789, 987654321 }, reverse=True)
        # bans_list(987654321) -> False
        # bans_list(987654322) -> True
        @nonebot.on_command('签到', permission=bans_list)
        async def _(session: CommandSession):
            # 只有不是这两个群的时候才会执行
            ...
        ```
    """
    user_ids = user_ids if user_ids is not ... else set()
    group_ids = group_ids if group_ids is not ... else set()

    def checker(sender: SenderRoles) -> bool:
        is_in = sender.sent_by(user_ids) or sender.from_group(group_ids)
        return not is_in if reverse else is_in

    return checker

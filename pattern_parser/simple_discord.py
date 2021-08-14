import discord
from discord.abc import Messageable
from discord.guild import Guild
from discord.member import Member
from discord.role import Role

LATEST_MEMBER_ID = -1
LATEST_GUILD_ID = -1


class SimpleMember:
    def __init__(self, roles: dict[int, bool], is_bot: bool = False):
        global LATEST_MEMBER_ID
        if not isinstance(roles, dict):
            raise ValueError

        if not isinstance(is_bot, bool):
            raise ValueError

        for key, value in roles.items():
            if not isinstance(key, int):
                raise ValueError
            if not isinstance(value, bool):
                raise ValueError
        if not roles:
            raise ValueError

        self.__roles = roles
        self.__is_bot = is_bot
        self.__id = LATEST_MEMBER_ID + 1
        self.__name = f"simple_user_{self.__id}"
        LATEST_MEMBER_ID = self.__id

    def name(self) -> str:
        return self.__name

    def roles(self) -> dict[int, bool]:
        return self.__roles

    def id(self) -> int:
        return self.__id

    def is_bot(self) -> bool:
        return self.__is_bot


class SimpleGuild:

    def __init__(self, members: list[SimpleMember] = None, roles: list[int] = None, everyone_role: int = None):
        global LATEST_GUILD_ID
        if members is None:
            members = [
                SimpleMember(
                    {
                        1: False,
                        2: True,
                        3: False,
                        4: True,
                        5: False,
                        6: True,
                        7: False,
                        8: True,
                        9: False,
                        10: True
                    }
                ),
                SimpleMember(
                    {
                        1: False,
                        2: False,
                        3: False,
                        4: False,
                        5: False,
                        6: False,
                        7: False,
                        8: False,
                        9: False,
                        10: False
                    }, True
                ),
                SimpleMember(
                    {
                        1: True,
                        2: True,
                        3: True,
                        4: False,
                        5: True,
                        6: True,
                        7: False,
                        8: False,
                        9: True,
                        10: False
                    }, True
                ),
                SimpleMember(
                    {
                        1: True,
                        2: True,
                        3: False,
                        4: False,
                        5: False,
                        6: False,
                        7: True,
                        8: False,
                        9: False,
                        10: True
                    }
                ),
                SimpleMember(
                    {
                        1: True,
                        2: False,
                        3: False,
                        4: True,
                        5: False,
                        6: False,
                        7: True,
                        8: False,
                        9: False,
                        10: False
                    }, True
                ),
                SimpleMember(
                    {
                        1: True,
                        2: True,
                        3: True,
                        4: False,
                        5: False,
                        6: False,
                        7: False,
                        8: False,
                        9: False,
                        10: False
                    }
                )

            ]

        if roles is None:
            roles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        if everyone_role is None:
            everyone_role = roles[0]

        if not isinstance(roles, list):
            raise ValueError
        for role in roles:
            if not isinstance(role, int):
                raise ValueError
        if not roles:
            raise ValueError

        if not isinstance(everyone_role, int):
            raise ValueError
        everyone_role_is_in_guild = False
        for role in roles:
            if role == everyone_role:
                everyone_role_is_in_guild = True
                break
        if not everyone_role_is_in_guild:
            raise ValueError

        if not isinstance(members, list):
            raise ValueError

        roles.sort()
        for member in members:
            if not isinstance(member, SimpleMember):
                raise ValueError
            keys_as_list = []
            for key in member.roles():
                keys_as_list.append(key)
            keys_as_list.sort()
            if roles != keys_as_list:
                raise ValueError

        self.__roles = roles
        self.__everyone_role = everyone_role
        self.__id = LATEST_GUILD_ID + 1
        self.__name = f"simple_guild_{self.__id}"
        self.__members = members
        LATEST_GUILD_ID = self.__id

    def roles(self) -> list[int]:
        return self.__roles

    def everyone_role(self) -> int:
        return self.__everyone_role

    def id(self) -> int:
        return self.__id

    def name(self) -> str:
        return self.__name

    def members(self) -> list[SimpleMember]:
        return self.__members

    def get_result(self, pattern) -> int:
        result = 0
        for member in self.__members:
            result += pattern.user_applies(member)
        return result


class SimpleMessage:

    def __init__(self, content: str = None, *, tts: bool = False, embed: discord.Embed = None, file: discord.File = None, files: list[discord.File] = None, delete_after: float = None, nonce: int = None, allowed_mentions: discord.AllowedMentions = None, reference: discord.Message = None, mention_author: bool = None) -> None:

        self.__content = content
        self.__tts = tts
        self.__embed = embed
        self.__file = file
        self.__files = files
        self.__delete_after = delete_after
        self.__nonce = nonce
        self.__allowed_mentions = allowed_mentions
        self.__reference = reference
        self.__mention_author = mention_author

    async def send_contents(self, target: Messageable) -> None:
        await target.send(content=self.__content, tts=self.__tts, embed=self.__embed, file=self.__file, files=self.__files, delete_after=self.__delete_after, nonce=self.__nonce, allowed_mentions=self.__allowed_mentions, reference=self.__reference, mention_author=self.__mention_author)


def create_simple_guild(guild: Guild) -> SimpleGuild:
    simple_members: list[SimpleMember] = []
    member: Member
    for member in guild.members:
        simple_members.append(create_simple_member(member))

    return SimpleGuild(simple_members, [role.id for role in guild.roles], guild.default_role.id)


def create_simple_member(member: Member) -> SimpleMember:
    role: Role
    member_roles: dict[int, bool] = {}
    for role in member.guild.roles:
        member_roles[role.id] = False
    for role in member.roles:
        member_roles[role.id] = True
    return SimpleMember(member_roles, member.bot)

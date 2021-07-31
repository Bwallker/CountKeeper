from abc import ABC
import os
import json
from typing import Union

from discord.channel import TextChannel, VoiceChannel
from discord.role import Role
from patterns.pattern_error import PatternError
from patterns.component import AdvancedComponent, Component, SimpleComponent
from patterns.operators import Operator
import counting_channels
import importlib.util
from logs.log import print
from inspect import isclass, getmembers, signature
import discord
PATH_TO_CHANNEL_FILES = os.getcwd()
PATH_TO_CHANNEL_FILES += "/count_keeper_data/channels"
PATH_TO_OPERATORS_AND_COMPONENTS = os.getcwd() + "/patterns"


class UnknownPatternInJsonFile(PatternError):
    """
        Raised if the contents of a json file is not a component or operators
    """


ALL_COMPONENTS: dict[str, Component]
ALL_OPERATORS: dict[str, Operator]


def gather_all_operators_and_components(path: str = PATH_TO_OPERATORS_AND_COMPONENTS) -> tuple[dict[str, Component], dict[str, Operator]]:
    new_all_components: dict[str, Component] = {}
    new_all_operators: dict[str, Operator] = {}
    for filename in os.listdir(path):
        new_path = path + f"/{filename}"
        if os.path.isdir(new_path):
            dir_all_components, dir_all_operators = gather_all_operators_and_components(
                new_path)
            new_all_components.update(dir_all_components)
            new_all_operators.update(dir_all_operators)
        elif filename.endswith(".py"):
            path_dir = f"{path}/{filename}"
            name = f"patterns.{filename[:-3]}"
            spec = importlib.util.spec_from_file_location(name, path_dir)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name, value in getmembers(module):

                if isclass(value):
                    number_of_args = len(signature(value.__init__).parameters)
                    number_of_args -= 1
                    args_as_list = []
                    for i in range(number_of_args):
                        args_as_list.append("None")
                    args_as_tuple = tuple(args_as_list)
                    try:
                        instance = value()
                    except Exception:
                        continue
                    key = type(instance).__name__

                    if isinstance(instance, Operator):
                        new_all_operators[key] = value
                    elif isinstance(instance, Component):
                        new_all_components[key] = value
    return new_all_components, new_all_operators


def write_to_file(component: Component, guild_id: int, channel_id: int, path_to_channels: str = PATH_TO_CHANNEL_FILES) -> str:
    path_to_guild = path_to_channels + f"/{guild_id}"
    try:
        os.mkdir(path_to_guild)
    except FileExistsError:
        print(f"{path_to_guild} already exists.")
    path_to_file = path_to_guild + f"/{channel_id}.json"

    with open(path_to_file, 'w') as channel_file:
        json.dump(component.__dict__(), channel_file, indent=4)
    return path_to_file


def read_from_file(guild_id: int, channel_id: int, path_to_channels: str = PATH_TO_CHANNEL_FILES) -> Component:
    path_to_file = path_to_channels + f"/{guild_id}/{channel_id}.json"
    with open(path_to_file, 'r') as channel_file:
        data = json.load(channel_file)
    return from_dict(data)


def from_dict(as_dict: dict) -> Union[Component, Operator]:
    global ALL_COMPONENTS, ALL_OPERATORS
    class_name = as_dict['type']
    if class_name in ALL_COMPONENTS:
        target_class = ALL_COMPONENTS[class_name]
    elif class_name in ALL_OPERATORS:
        target_class = ALL_OPERATORS[class_name]
    else:
        raise UnknownPatternInJsonFile
    instance = target_class()
    try:
        annotations = instance.__annotations__
        print(annotations)
    except AttributeError:
        return instance
    for annotation in annotations:
        type_of_annotation = annotations[annotation]
        value = as_dict[annotation]
        if type_of_annotation == dict or type(value) != dict:
            setattr(instance, annotation, value)
        else:
            setattr(instance, annotation, from_dict(value))
    return instance

def create_component(pattern: str, role_ids_in_guild: list[int], everyone_role_id: int, guild_id: int, channel_id: int) -> tuple[str, discord.File]:
    try:
        operators = counting_channels.operators
        component = counting_channels.pattern_constructor(
        pattern, role_ids_in_guild, operators, everyone_role_id)
        path_to_file = write_to_file(component, guild_id, channel_id)
        return "Pattern parsed successfully!\n\nPattern was: {pattern}\n\n", discord.File(fp=path_to_file, filename=f"{channel_id}.json")
    except PatternError as e:
        return e.__str__(), None


def update_channels(guild: discord.Guild) -> dict[int, int]:
    """
        Updates all the counting channels in a guild
    """
    user_roles: list[dict[int, bool]] = []
    member: discord.Member
    for member in guild.members:
        member_roles: dict[int, bool] = {}
        role: Role
        for role in guild.roles:
            member_roles[role.id] = False
        for role in member.roles:
            member_roles[role.id] = True
        user_roles.append(member_roles)
    text_channel: TextChannel = guild.text_channels[0]
    text_channel.send()
    channel: VoiceChannel
    for channel in guild.voice_channels:
        try:
            component = read_from_file(guild.id, channel.id)
        except FileNotFoundError:
            continue
        number_of_members_who_apply = 0
        for member_roles in user_roles:
            number_of_members_who_apply += component.user_applies(member_roles)
        counting_channels.update_channel(
            channel, number_of_members_who_apply, guild)


def init():
    global ALL_COMPONENTS, ALL_OPERATORS
    ALL_COMPONENTS, ALL_OPERATORS = gather_all_operators_and_components()

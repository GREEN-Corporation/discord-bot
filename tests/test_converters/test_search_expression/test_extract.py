from typing import List, Type

import pytest
from discord.ext import commands

from bot.converters import SearchExpression
from bot.data import ChannelGroup, DiscordObjectsGroup, UserGroup
from bot.exceptions import SearchExpressionNotFound


@pytest.mark.parametrize(
	"argument, compare_data_group",
	[
		("usr:*", [UserGroup]),
		("usr", [UserGroup]),
		("ch", [ChannelGroup]),
		("ch+usr", [ChannelGroup, UserGroup]),
		("usr+ch:*", [UserGroup, ChannelGroup])
	]
)
@pytest.mark.asyncio
async def test_good_extractDataGroup(
	bot: commands.Bot,
	discordContext: commands.Context,
	argument: str,
	compare_data_group: List[Type[DiscordObjectsGroup]]
) -> None:
	a = SearchExpression()
	a.ctx = discordContext
	a.string = argument.split(":")
	a._extractDataGroup()
	for ind in range(0, len(a.data_groups)):
		assert isinstance(a.data_groups[ind], compare_data_group[ind])

@pytest.mark.parametrize(
	"argument",
	[
		"grp",
		"usrg",
		"wertch:*",
		"werwchesdf"
	]
)
@pytest.mark.asyncio
async def test_bad_extractDataGroup(
	bot: commands.Bot,
	discordContext: commands.Context,
	argument: str,
) -> None:
	a = SearchExpression()
	a.ctx = discordContext
	a.string = argument.split(":")
	a.argument = argument
	with pytest.raises(SearchExpressionNotFound):
		a._extractDataGroup()
from typing import Any, Dict

import discord.ext.test as dpytest
import psycopg
import pytest
from discord.ext import commands

from bot.utils import Case, MockLocator, getDiscordMemberID

from .bad_cases import (  # empty_case
	case_without_one_required_params,
	case_without_two_required_params
)
from .coincidence_cases import (
	case_for_coincidence_0_1,
	case_for_coincidence_0_2,
	case_for_coincidence_1_1,
	case_for_coincidence_1_2,
	case_for_coincidence_2_1,
	case_for_coincidence_2_2,
	case_for_coincidence_3_1,
	case_for_coincidence_3_2,
	case_for_coincidence_4_1,
	case_for_coincidence_4_2,
	case_for_coincidence_5_1,
	case_for_coincidence_5_2,
	error_fragments_0,
	error_fragments_1,
	error_fragments_2,
	error_fragments_3,
	error_fragments_4,
	error_fragments_5
)
from .good_cases import (
	case_with_all_channels_and_users_exprs,
	case_with_all_channels_exprs,
	case_with_all_users_exprs,
	compared_objects_for_all_channels_and_users_exprs,
	compared_objects_for_all_channels_exprs,
	compared_objects_for_all_users_exprs,
	default_case,
	default_case_with_other_target_name,
	default_case_with_several_users
)


@pytest.mark.parametrize(
	"case",
	[default_case, default_case_with_several_users,
	default_case_with_other_target_name]
)
@pytest.mark.doDelayedExpression
@pytest.mark.asyncio
async def test_good_log_create_with_flags(
	db: psycopg.AsyncConnection[Any],
	mockLocator: MockLocator,
	case: Case
) -> None:
	await dpytest.message(case.getMessageStringWith("sudo log 1",
		getDiscordMemberID))
	assert dpytest.verify().message().content("Цель добавлена успешно.")
	async with db.cursor() as acur:
		await acur.execute(
			"SELECT * FROM target"
		)
		for row in await acur.fetchall():
			assert row == (row[0], str(mockLocator.guild.id),
				case["target"], case["act"], case["d_in"],
				*list(case["flags"].values()))

@pytest.mark.asyncio
async def test_good_log_create_without_flags(
	db: psycopg.AsyncConnection[Any],
	mockLocator: MockLocator
) -> None:
	parts = []
	parts.append("sudo log 1")
	parts.append(str(mockLocator.members[0].id))
	parts.append("23")
	parts.append(str(mockLocator.members[1].id))
	await dpytest.message(" ".join(parts))
	assert dpytest.verify().message().content("Цель добавлена успешно.")
	async with db.cursor() as acur:
		await acur.execute(
			"SELECT * FROM target"
		)
		for row in await acur.fetchall():
			flags_values = [None, 0, None, None]
			assert row == (row[0], str(mockLocator.guild.id),
				[mockLocator.members[0]], '23', [mockLocator.members[1]],
				*flags_values)

@pytest.mark.asyncio
async def test_log_without_subcommand() -> None:
	await dpytest.message("sudo log")
	assert dpytest.verify().message().content(
		"Убедитесь, что вы указали подкоманду.")

@pytest.mark.doDelayedExpression
@pytest.mark.parametrize(
	"case, missing_params",
	[
		(case_without_two_required_params, "act"),
		(case_without_one_required_params, "d_in"),
		# (empty_case, "target") # TODO improved in discord.py
	]
)
@pytest.mark.asyncio
async def test_log_without_require_params(
	case: Case,
	missing_params: str
) -> None:
	with pytest.raises(commands.MissingRequiredArgument):
		await dpytest.message(case.getMessageStringWith("sudo log 1"))
	assert dpytest.verify().message().content(f"Убедитесь, что вы указали "
		f"все обязательные параметры. Не найденный параметр: "
		f"{missing_params}")

"""
https://github.com/GREEN-Corporation/discord-bot/issues/79
"""
# @pytest.mark.doDelayedExpression
# @pytest.mark.parametrize(
# 	"case, unhandle_message_part",
# 	[(case_without_explicit_flag, "barhatniy_tyagi")]
# )
# @pytest.mark.asyncio
# async def test_log_bad_flag(
# 	case: Case,
# 	unhandle_message_part: str
# ) -> None:
# 	with pytest.raises(commands.CommandInvokeError):
# 		await dpytest.message(case.getMessageStringWith("sudo log 1"))
# 	assert dpytest.verify().message().content("Убедитесь, что вы "
# 		"указали флаги явно, либо указали корректные данные."
# 		f" Необработанная часть сообщения: {unhandle_message_part}")

# @pytest.mark.asyncio
# async def test_log_bad_parameters() -> None:
# 	with pytest.raises(commands.CommandInvokeError):
# 		incorrect_id = 1107606170375565372
# 		await dpytest.message("sudo log 1 336420570449051649 43 "
# 		f"{incorrect_id}")
# 	assert dpytest.verify().message().content("Убедитесь, что вы указали "
# 		"флаги явно, либо указали корректные данные. "
# 		"Необработанная часть сообщения: 1107606170375565372")

@pytest.mark.asyncio
async def test_log_1_with_mention(mockLocator: MockLocator) -> None:
	await dpytest.message(f"sudo log 1 <@{mockLocator.members[0].id}> 23"
		f" <@{mockLocator.members[1].id}>")
	assert dpytest.verify().message().content("Цель добавлена успешно.")

@pytest.mark.doDelayedExpression
@pytest.mark.parametrize(
	"case, compared_case, error_part",
	[
		(case_for_coincidence_0_1, case_for_coincidence_0_2,
		error_fragments_0),
		(case_for_coincidence_1_1, case_for_coincidence_1_2,
		error_fragments_1),
		(case_for_coincidence_2_1, case_for_coincidence_2_2,
		error_fragments_2),
		(case_for_coincidence_3_1, case_for_coincidence_3_2,
		error_fragments_3),
		(case_for_coincidence_4_1, case_for_coincidence_4_2,
		error_fragments_4),
		(case_for_coincidence_5_1, case_for_coincidence_5_2,
		error_fragments_5)
	],
)
@pytest.mark.asyncio
async def test_coincidence_targets(
	case: Case,
	compared_case: Case,
	error_part: Dict[str, Any]
) -> None:

	await dpytest.message(case.getMessageStringWith(
		"sudo log 1"))
	dpytest.get_message()

	await dpytest.message(compared_case.getMessageStringWith(
		"sudo log 1"))
	bot_reply = dpytest.get_message().content
	coincidence_error_message_part = (f"({error_part['name']}). "
		f"Совпадающие элементы: "
		f"{', '.join(map(str, error_part['coincidence_elems']))}")
	assert coincidence_error_message_part in bot_reply

@pytest.mark.doDelayedExpression
@pytest.mark.parametrize(
	"case, compared_objects",
	[
		(
			case_with_all_users_exprs, compared_objects_for_all_users_exprs
		),
		(
			case_with_all_channels_and_users_exprs,
			compared_objects_for_all_channels_and_users_exprs
		),
		(
			case_with_all_channels_exprs, compared_objects_for_all_channels_exprs
		)
	]
)
@pytest.mark.asyncio
async def test_log_1_good_expression(
	db: psycopg.AsyncConnection[Any],
	case: Case,
	compared_objects: Case,
	mockLocator: MockLocator,
) -> None:
	await dpytest.message(f"sudo log 1 {case['target']} 23"
		f" {case['d_in']}")
	assert dpytest.verify().message().content("Цель добавлена успешно.")
	async with db.cursor() as acur:
		await acur.execute(
			"SELECT * FROM target"
		)
		for row in await acur.fetchall():
			flags_values = [None, 0, None, None]
			assert row == (row[0], str(mockLocator.guild.id),
				compared_objects["target"], '23', compared_objects["d_in"],
				*flags_values)

@pytest.mark.parametrize(
	"exp1, exp2, missing_params",
	[
		# ( # improved in discord.py library
		# 	"fger", "erert", "target",
		# ),
		(
			"usr:*", "*df", "d_in"
		)
	]
)
@pytest.mark.asyncio
async def test_log_1_bad_expression(
	exp1: str,
	exp2: str,
	missing_params: str
) -> None:
	with pytest.raises(commands.CommandError):
		await dpytest.message(f"sudo log 1 {exp1} 23"
			f" {exp2}")
	assert dpytest.verify().message().content(f"Убедитесь, что вы указали все"
		f" обязательные параметры. Не найденный параметр: {missing_params}")

"""
https://github.com/Debianov/vtc-bot/issues/72
"""
# @pytest.mark.asyncio
# async def test_log_double_entry_call(
# 	db: psycopg.AsyncConnection[Any],
# 	mockLocator: MockLocator
# ) -> None:
# 	parts = []
# 	parts.append("sudo log 1")
# 	parts.append(str(mockLocator.members[0].id))
# 	parts.append("23")
# 	parts.append(str(mockLocator.members[1].id))
# 	parts.extend(parts)
# 	await dpytest.message(" ".join(parts))
# 	assert dpytest.verify().message().content("Цель добавлена успешно.")
# 	async with db.cursor() as acur:
# 		await acur.execute(
# 			"SELECT * FROM target"
# 		)
# 		row_count = 0
# 		for row in await acur.fetchall():
# 			row_count += 1
# 			flags_values = [None, 0, None, None]
# 			assert row == ("0", str(mockLocator.guild.id),
# 				[mockLocator.members[0]], '23', [mockLocator.members[1]],
# 				*flags_values)
# 		if row_count <= 1:
# 			raise AssertionError
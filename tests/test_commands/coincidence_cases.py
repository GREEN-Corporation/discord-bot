from typing import Any, Union

import discord

from bot.utils import (
	Case,
	DelayedExpression,
	DictMessagePart,
	ElemFormater,
	ListMessagePart,
	StringMessagePart,
	default_format
)


def getDiscordMemberObject(arg: Any) -> Union[str, Any]:
    if isinstance(arg, discord.Member):
        return str(arg.id)
    else:
        return arg


format_for_getting_ds_id = ElemFormater(getDiscordMemberObject)

case_for_coincidence_0_1 = Case(
    target=[DelayedExpression('mockLocator.members[0]')],
    act="26",
    d_in=[DelayedExpression('mockLocator.members[1]')],
    flags={"-name": "Aboba"}
)

case_for_coincidence_0_2 = Case(
    target=[DelayedExpression('mockLocator.members[0]')],
    act="26",
    d_in=[DelayedExpression('mockLocator.members[1]')],
    flags={"-name": "Aboba"}
)

error_fragments_0 = {"id": "0", "name": "Aboba", "coincidence_elems": [
    DelayedExpression('mockLocator.members[0].id'), "26",
    DelayedExpression('mockLocator.members[1].id'), "Aboba"]}

case_for_coincidence_1_1 = Case(
    target=[DelayedExpression('mockLocator.members[0]')],
    act="26",
    d_in=[DelayedExpression('mockLocator.members[1]')],
    flags=DictMessagePart(default_format, {"-name": "Aboba"})
)

case_for_coincidence_1_2 = Case(
    target=ListMessagePart(format_for_getting_ds_id,
                           DelayedExpression('mockLocator.members[2]')),
    act=StringMessagePart("26"),
    d_in=ListMessagePart(format_for_getting_ds_id,
                         DelayedExpression('mockLocator.members[1]')),
    flags=DictMessagePart(default_format, {"-name": "Aboba"})
)

case_for_coincidence_2_1 = Case(
    target=ListMessagePart(format_for_getting_ds_id,
                           DelayedExpression('mockLocator.members[0]'),
                           DelayedExpression('mockLocator.members[1]')),
    act=StringMessagePart("26"),
    d_in=ListMessagePart(format_for_getting_ds_id,
                         DelayedExpression('mockLocator.members[2]'),
                         DelayedExpression('mockLocator.members[3]')),
    flags=DictMessagePart(default_format, {"-name": "Aboba"})
)

case_for_coincidence_2_2 = Case(
    target=ListMessagePart(format_for_getting_ds_id,
                           DelayedExpression('mockLocator.members[0]'),
                           DelayedExpression('mockLocator.members[1]')),
    act=StringMessagePart("26"),
    d_in=ListMessagePart(format_for_getting_ds_id,
                         DelayedExpression('mockLocator.members[2]')),
    flags=DictMessagePart(default_format, {"-name": "Aboba"})
)


case_for_coincidence_3_1 = Case(
    target=ListMessagePart(format_for_getting_ds_id,
                           DelayedExpression('mockLocator.members[0]')),
    act=StringMessagePart("26"),
    d_in=ListMessagePart(format_for_getting_ds_id,
                         DelayedExpression('mockLocator.members[1]')),
    flags=DictMessagePart(default_format, {"-name": "Aboba"})
)

case_for_coincidence_3_2 = Case(
    target=ListMessagePart(format_for_getting_ds_id,
                           DelayedExpression('mockLocator.members[2]')),
    act=StringMessagePart("8"),
    d_in=ListMessagePart(format_for_getting_ds_id,
                         DelayedExpression('mockLocator.members[3]')),
    flags=DictMessagePart(default_format, {"-name": "Aboba"})
)

case_for_coincidence_4_1 = Case(
    target=ListMessagePart(format_for_getting_ds_id,
                           DelayedExpression('mockLocator.members[0]')),
    act=StringMessagePart("26"),
    d_in=ListMessagePart(format_for_getting_ds_id,
                         DelayedExpression('mockLocator.members[1]')),
    flags=DictMessagePart(default_format, {"-name": "Aboba"})
)

case_for_coincidence_4_2 = Case(
    target=ListMessagePart(format_for_getting_ds_id,
                           DelayedExpression('mockLocator.members[0]')),
    act=StringMessagePart("26"),
    d_in=ListMessagePart(format_for_getting_ds_id,
                         DelayedExpression('mockLocator.members[1]')),
    flags=DictMessagePart(default_format, {"-name": "aboba"})
)

case_for_coincidence_5_1 = Case(
    target=ListMessagePart(format_for_getting_ds_id,
                           DelayedExpression('mockLocator.members[0]')),
    act=StringMessagePart("26"),
    d_in=ListMessagePart(format_for_getting_ds_id,
                         DelayedExpression('mockLocator.members[1]')),
    flags=DictMessagePart(default_format, {"-name": "Aboba"})
)

case_for_coincidence_5_2 = Case(
    target=ListMessagePart(format_for_getting_ds_id,
                           DelayedExpression('mockLocator.members[0]')),
    act=StringMessagePart("26"),
    d_in=ListMessagePart(format_for_getting_ds_id,
                         DelayedExpression('mockLocator.members[1]')),
    flags=DictMessagePart(default_format, {"-name": ""})
)
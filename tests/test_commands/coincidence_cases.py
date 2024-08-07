from typing import Any, Union

import discord

from bot.utils import Case, DelayedExpression


def getDiscordMemberObject(arg: Any) -> Union[str, Any]:
    if isinstance(arg, discord.Member):
        return str(arg.id)
    else:
        return arg

case_for_coincidence_0_1 = Case(
    target=[DelayedExpression('mockLocator.members[0].id')],
    act="26",
    d_in=[DelayedExpression('mockLocator.members[1].id')],
    flags={"-name": "Aboba"}
)

case_for_coincidence_0_2 = Case(
    target=[DelayedExpression('mockLocator.members[0].id')],
    act="26",
    d_in=[DelayedExpression('mockLocator.members[1].id')],
    flags={"-name": "Aboba"}
)

error_fragments_0 = {"name": "Aboba", "coincidence_elems": [
    DelayedExpression('mockLocator.members[0].id'), "26",
    DelayedExpression('mockLocator.members[1].id'), "Aboba"]}

case_for_coincidence_1_1 = Case(
    target=[DelayedExpression('mockLocator.members[0].id')],
    act="26",
    d_in=[DelayedExpression('mockLocator.members[1].id')],
    flags={"-name": "Aboba"}
)

case_for_coincidence_1_2 = Case(
    target=[DelayedExpression('mockLocator.members[2].id')],
    act="26",
    d_in=[DelayedExpression('mockLocator.members[1].id')],
    flags={"-name": "Aboba"}
)

error_fragments_1 = {"name": "Aboba", "coincidence_elems": ["26",
    DelayedExpression('mockLocator.members[1].id'), "Aboba"]}

case_for_coincidence_2_1 = Case(
    target=[DelayedExpression('mockLocator.members[0].id'),
            DelayedExpression('mockLocator.members[1].id')],
    act="26",
    d_in=[DelayedExpression('mockLocator.members[2].id'),
          DelayedExpression('mockLocator.members[3].id')],
    flags={"-name": "Aboba"}
)

case_for_coincidence_2_2 = Case(
    target=[DelayedExpression('mockLocator.members[0].id'),
            DelayedExpression('mockLocator.members[1].id')],
    act="26",
    d_in=[DelayedExpression('mockLocator.members[2].id')],
    flags={"-name": "Aboba"}
)

error_fragments_2 = {"name": "Aboba", "coincidence_elems": [
    DelayedExpression('mockLocator.members[0].id'),
    DelayedExpression('mockLocator.members[1].id'), "26",
    DelayedExpression('mockLocator.members[2].id'), "Aboba"]}

case_for_coincidence_3_1 = Case(
    target=[DelayedExpression('mockLocator.members[0].id')],
    act="26",
    d_in=[DelayedExpression('mockLocator.members[1].id')],
    flags={"-name": "Aboba"}
)

case_for_coincidence_3_2 = Case(
    target=[DelayedExpression('mockLocator.members[2].id')],
    act="8",
    d_in=[DelayedExpression('mockLocator.members[3].id')],
    flags={"-name": "Aboba"}
)

error_fragments_3 = {"name": "Aboba", "coincidence_elems": [
    "Aboba"]}

case_for_coincidence_4_1 = Case(
    target=[DelayedExpression('mockLocator.members[0].id')],
    act="26",
    d_in=[DelayedExpression('mockLocator.members[1].id')],
    flags={"-name": "Aboba"}
)

case_for_coincidence_4_2 = Case(
    target=[DelayedExpression('mockLocator.members[0].id')],
    act="26",
    d_in=[DelayedExpression('mockLocator.members[1].id')],
    flags={"-name": "aboba"}
)

error_fragments_4 = {"name": "Aboba", "coincidence_elems": [
    DelayedExpression('mockLocator.members[0].id'), "26",
    DelayedExpression('mockLocator.members[1].id')]}

case_for_coincidence_5_1 = Case(
    target=[DelayedExpression('mockLocator.members[0].id')],
    act="26",
    d_in=[DelayedExpression('mockLocator.members[1].id')],
    flags={"-name": "Aboba"}
)

case_for_coincidence_5_2 = Case(
    target=[DelayedExpression('mockLocator.members[0].id')],
    act="26",
    d_in=[DelayedExpression('mockLocator.members[1].id')],
    flags={"-name": ""}
)

error_fragments_5 = {"name": "Aboba", "coincidence_elems": [
    DelayedExpression('mockLocator.members[0].id'), "26",
    DelayedExpression('mockLocator.members[1].id')]}

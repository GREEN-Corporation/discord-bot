import asyncio
import pathlib
import sys
from typing import Any, AsyncGenerator, Dict, Generator, List, Tuple

import discord
import discord.ext.test as dpytest
import pytest
import pytest_asyncio
from discord.ext import commands

from bot.utils import DelayedExpression, DelayedExpressionReplacer, isIterable

root = pathlib.Path.cwd()

sys.path.append(str(root))

from bot.help import BotHelpCommand  # flake8: noqa: I005
from bot.main import BotConstructor  # flake8: noqa: I005
from bot.utils import Case, DelayedExprsEvaluator

# flake8: noqa: I005
pytest_plugins = ('pytest_asyncio',)

@pytest.fixture(scope="package")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
	loop = asyncio.get_event_loop()
	yield loop
	loop.close()

@pytest_asyncio.fixture(autouse=True)
async def cleanUp() -> AsyncGenerator[None, None]:
	yield
	await dpytest.empty_queue()

def pytest_pyfunc_call(pyfuncitem: pytest.Function) -> None:
	"""
	 The `pytest.mark.doDelayedExpression` implementation.
	 Iter all args that passing to a test function, find and executed all
	 `delayedExpression`s. The results of execution are writed in the same
	 place (`DelayedExpressionReplacer` for more info).
	 If object isn't iterable it is passed.
	"""
	if pyfuncitem.get_closest_marker("doDelayedExpression"):
		params_from_func = pyfuncitem.callspec.params
		params_and_fixtures = pyfuncitem.funcargs
		params_with_case = filterIterableParameters(params_from_func)
		fixtures = filterFixtures(params_and_fixtures, params_with_case)
		for _, maybe_case in params_with_case.items():
			DelayedExpressionReplacer(
				maybe_case,
				fixtures
			).go()

def filterIterableParameters(
	params_from_func: Dict[str, object]
) -> Dict[str, Case]:
	params_with_case: Dict[str, Case] = {}
	for (param, object) in params_from_func.items():
		if isIterable(object):
			params_with_case[param] = object
		else:
			print("filterIterableParameters", "The object is not iterable. "
			"Skipped to checking by fixture.")
	return params_with_case


def filterFixtures(
	params_and_fixtures: Dict[str, Any],
	params_with_case: Dict[str, Case]
) -> Dict[str, Any]:
	fixtures: Dict[str, Case] = params_and_fixtures.copy()
	for param_key in params_with_case.keys():
		fixtures.pop(param_key)
	return fixtures
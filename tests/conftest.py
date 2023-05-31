from discord.ext import commands
import discord.ext.test as dpytest
import discord
import sys
import asyncio
import pathlib
import pytest
import pytest_asyncio

root = pathlib.Path.cwd()

sys.path.append(str(root))

from bot.main import bot

pytest_plugins = ('pytest_asyncio',)

@pytest.fixture(scope="package")
def event_loop() -> None:
	loop = asyncio.get_event_loop()
	yield loop
	loop.close()

@pytest_asyncio.fixture(scope="package", autouse=True, name="bot")
async def botInit() -> commands.Bot:
	await bot._async_setup_hook()
	dpytest.configure(bot, num_members=6)
	config = dpytest.get_config()
	pytest.test_guild = config.guilds[0]
	pytest.test_channel = config.channels[0]
	for (ind, member) in enumerate(config.members):
		setattr(pytest, f"test_member{ind}", member)
	return bot

@pytest_asyncio.fixture(autouse=True)
async def cleanUp() -> None:
	yield
	await dpytest.empty_queue()
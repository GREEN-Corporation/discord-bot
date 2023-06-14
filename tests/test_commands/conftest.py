import discord
import pytest
import pytest_asyncio
import psycopg
import asyncio
from typing import Optional, Any
import sys
import pathlib
import discord.ext.test as dpytest

root = pathlib.Path.cwd()

sys.path.append(str(root))

from bot.main import DBConnector, BotConstructor, DBConnFactory
from bot.help import BotHelpCommand

@pytest.mark.asyncio
@pytest_asyncio.fixture(scope="package", autouse=True, name="db")
async def setupDB() -> Optional[psycopg.AsyncConnection[Any]]:
	loop = asyncio.get_event_loop()
	with open("test_db_secret.sec") as file:
		future_dbconn = await DBConnFactory(dbname=file.readline(), dbuser=file.readline())
	return future_dbconn

@pytest_asyncio.fixture(scope="package", autouse=True, name="bot")
async def botInit(db: Optional[psycopg.AsyncConnection[Any]]) -> 'commands.Bot':
	intents = discord.Intents.all()
	VCSBot = BotConstructor(
		dbconn=db,
		command_prefix="sudo ",
		intents=intents,
		help_command=BotHelpCommand(),
	)
	await VCSBot._async_setup_hook()
	await VCSBot.prepare()
	dpytest.configure(VCSBot, num_members=6)
	config = dpytest.get_config()
	pytest.test_guild = config.guilds[0]
	pytest.test_channel = config.channels[0]
	for (ind, member) in enumerate(config.members):
		setattr(pytest, f"test_member{ind}", member)
		intents = discord.Intents.all()
	return VCSBot

@pytest.mark.asyncio
@pytest_asyncio.fixture(scope="package", autouse=True)
async def createTargetTable(db) -> None:
	async with db.cursor() as acur:
		await acur.execute(
			"""CREATE TABLE public.target (
			id bigint,
			context_id bigint,
			target bigint[],
			act text,
			d_in bigint[],
			name text,
			priority integer,
			output text,
			other text
			);"""
		)
		yield
		await acur.execute(
			"""
			DROP TABLE target;
			"""
		)

@pytest.mark.asyncio
@pytest_asyncio.fixture(scope="function", autouse=True)
async def deleteTargetTable(db) -> None:
	yield
	async with db.cursor() as acur:
		await acur.execute(
			"DELETE FROM target;"
		)
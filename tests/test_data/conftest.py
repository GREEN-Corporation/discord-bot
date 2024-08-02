
import discord
import discord.ext.test as dpytest
import pytest
import pytest_asyncio
from discord.ext import commands

from bot.help import BotHelpCommand
from bot.main import BotConstructor, _setup_i18n
from bot.utils import ContextProvider, MockLocator


@pytest_asyncio.fixture(scope="package", autouse=True, name="bot")
async def botInit() -> commands.Bot:
	intents = discord.Intents.all()
	i18n_translator = _setup_i18n()
	VCSBot = BotConstructor(
		context_provider=ContextProvider(),
		command_prefix="",
		intents=intents,
		help_command=BotHelpCommand(),
		i18n_translator=i18n_translator
	)
	await VCSBot._async_setup_hook()
	await VCSBot.prepare()
	dpytest.configure(VCSBot, num_members=6)
	return VCSBot

@pytest.fixture(scope="package", autouse=True, name="mockLocator")
def initLocator() -> MockLocator:
	config = dpytest.get_config()
	locator = MockLocator(
		guild=config.guilds[0],
		channel=config.channels[0],
		members=list(config.guilds[0].members)
	)
	return locator

@pytest_asyncio.fixture(scope="package", autouse=True, name="discordContext")
async def createDiscordContext(bot: commands.Bot) -> commands.Context:
	message = await dpytest.message("help")
	current_ctx = await bot.get_context(message)
	return current_ctx
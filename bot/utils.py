import builtins
import os
from typing import (
	Any,
	Callable,
	Dict,
	Iterable,
	List,
	Optional,
	Tuple,
	Type,
	TypeVar,
	Union
)

import discord
import discord.abc
from discord.ext import commands

from bot.data import DiscordObjectsGroup


class ContextProvider:
	"""
	The locator for receiving and passing a context (discord.Guild).
	"""

	def __init__(self) -> None:
		self.context: Optional[discord.Guild] = None

	def updateContext(self, context: discord.Guild | None) -> None:
		self.context = context

	def getContext(self) -> Optional[discord.Guild]:
		return self.context


class MockLocator:
	"""
	The class for receiving and passing mock-objects as Discord-objects.
	"""

	def __init__(
		self,
		guild: discord.Guild,
		channel: discord.abc.GuildChannel,
		members: List[discord.Member]
	) -> None:
		self.guild = guild
		self.channel = channel
		self.members = members

def getEnvIfExist(*env_names: str) -> Union[List[str], None]:
	"""
	This function checks the environment variables and returns their values
	in the same order as they were passed.
	"""
	saved_data: List[str] = []
	for env in env_names:
		if not (result := os.getenv(env)):
			return None
		else:
			saved_data.append(result)
	return saved_data


def removeNesting(instance: List[Any]) -> List[Any]:
	"""
		The function for removing nesting.
	"""
	for elem in instance:
		if isinstance(elem, list):
			tmp = elem
			instance.remove(tmp)
			instance.extend(tmp)
	return instance


def createDiscordObjectsGroupInstance(
	instance_list: List[Type[DiscordObjectsGroup]],
	discord_context: commands.Context
) -> List[DiscordObjectsGroup]:
	result: List[DiscordObjectsGroup] = []
	for instance in instance_list:
		result.append(instance(discord_context))
	return result


T = TypeVar("T")


class DelayedExpression:
	"""
	The reason of why this class was written is an overwhelming developer\
	desire of to have human-readable expressions under the\
	`pytest.mark.parametrize <https://docs.pytest.org/en/7.1.x/how-to/param\
	etrize.html>`_ decorators that is impossible without implementing\
	something like this.
	"""

	def __init__(self, expression: str):
		self.expression = expression

	def eval(self, fixtures: Any) -> Any:
		self._setGlobalVarsInLocals(locals(), fixtures)
		return eval(self.expression)

	def _setGlobalVarsInLocals(
		self,
		locals: Dict[str, Any],
		fixtures: Any
	) -> Dict[str, Any]:
		"""
		Func sets a local variable in a func that called it.
		"""
		for (key, value) in fixtures.items():
			locals[key] = value
		return locals

	@staticmethod
	def isMine(check_instance: Any) -> bool:
		"""
		The load == implement for a purpose that isinstance for an
		instance check don't work due a python
		`features <https://bugs.python.org/issue7555>`_.
		"""
		return (hasattr(check_instance, "expression") and
				hasattr(check_instance, "eval_expression"))

class Case(dict):
	"""
	The class for storing and passing args to test funcs.
	Access to class attributes is any call to `__getitem__`.
	"""

	def __init__(self, **kwargs: Any) -> None:
		"""
		Args:
			**kwargs (dict[str, Any])
		"""
		self.message_string: List[str] = []
		self.update(**kwargs)

	def getMessageStringWith(
		self,
		cmd: str,
		format_func: Callable[[Any], Any] = lambda x: x
	) -> str:
		"""
		Returns the string for use in user messages.

		Args:
			format_func(Callable[[Any], Any]: should to check an object type
			and get any necessary attrs.
		"""
		if not self.message_string:
			self.message_string.append(cmd)
			for elem in self.values():
				match type(elem):
					case builtins.list:
						for inner_elem in elem:
							self._addInMessageStringList(format_func(inner_elem))
					case builtins.dict:
						for key, value in elem.items():
							if bool(value):
								self._addInMessageStringList(format_func(key))
								self._addInMessageStringList(format_func(value))
					case _:
						self._addInMessageStringList(elem)
		return " ".join(self.message_string) # anchor: duplicate

	def _addInMessageStringList(self, elem: Any):
		"""
		Checks that elems of a :class:`Case` instance is evaluated by
		:class:`DelayedExprsEvaluator`.
		"""
		match type(elem):
			case builtins.int:
				self.message_string.append(str(elem))
			case builtins.str:
				self.message_string.append(elem)
			case _:
				raise TypeError("elem isn't str or int. Message string formation isn't "
								"possible.")

class DelayedExpressionReplacer:
	"""
	This class for replacing elements in nested storages on the element
	of a `fixtures <https://docs.pytest.org/en/7.1.x/how-to/fixtures.html>`_
	namespace (respectively).
	"""
	def __init__(
		self,
		target: Iterable,
		fixtures: Any
	):
		self.target = target
		self.current_target = target
		self.last_storage = target
		self.fixtures = fixtures
		self.last_mutable_storage: Union[Dict[str, Any], List[Any], None] \
			= None
		self.class_to_change = DelayedExpression
		self.item: Union[str, int] = ""
		self.immutable_storages_chain: List[Tuple[Any, ...]] = []
		self.item_to_access_immutable_storage: Union[str, int, None] = None

	def go(self) -> None:
		if not isinstance(self.current_target, self.class_to_change):
			previous_storage = self._setLastStorage(self.current_target)
			if (isinstance(self.current_target, dict) or
					isinstance(self.current_target, list)):
				self.last_mutable_storage = self.current_target
				self.immutable_storages_chain.clear()
				if isinstance(self.current_target, dict):
					for key, value in self.current_target.items():
						self.current_target = value
						self.item = key
						self.go()
				else:
					for ind, value in enumerate(self.current_target):
						self.current_target = value
						self.item = ind
						self.go()
			elif isinstance(self.current_target, tuple):
				self.immutable_storages_chain.append((self.current_target, self.item))
				self._addItemForAccessImmutableStorage(previous_storage)
				for ind, value in enumerate(self.current_target):
					self.current_target = value
					self.item = ind
					self.go()
				self.immutable_storages_chain.pop() if (
					self.immutable_storages_chain) else False
			self.last_storage = previous_storage
		else:
			delayed_expr = self.current_target
			evaled_expr = delayed_expr.eval(self.fixtures)
			self._insert(evaled_expr)

	def _setLastStorage(self, target: Any) -> Any:
		"""
			Set `self.last_storage` and return an old attr value needed
			to restore an `self.last_storage` attr after exiting from a
			next recursive layer.
		"""
		previous_storage = self.last_storage
		self.last_storage = target
		return previous_storage

	def _addItemForAccessImmutableStorage(self, previous_storage: Any) -> None:
		"""
		A func writes `self.item` to `item_to_access_immutable_storage`.
		`self.item_to_access_immutable_storage` stores `self.item` to access
		immutable storage from last mutable storage. If `previous_storage`
		is immutable storage `self.item` it doesn't save in
		`self.item_to_access_immutable_storage`.

		```
		{'key': ("test", "test2", ["test3", "test4",
		("test5", object_to_update1, (object_to_update2, "test6"))])}
		A path to object_to_update1: item = 2 from first tuple => item =
		2 from first list.
		```
		If `item_to_access_immutable_storage` is sets from an item that
		describes a position access to immutable storage
		from other immutable storage, it's not allowed (we won't be able
		"to write" anything in an immutable storage).
		```
		{'key': ("test", "test2", ["test3", "test4", ("test5",
		object_to_update1, (object_to_update2, "test6"))])}
		A wrong path to object_to_update2: item = 2 from first tuple =>
		item = 2 from first list => item = 2 from second tuple.
		A true path to object_to_update2: item = 2 from first tuple =>
		item = 2 from first list because first list is last mutable storage.
		```
		"""
		if isinstance(previous_storage, dict) or isinstance(previous_storage, list):
			self.item_to_access_immutable_storage = self.item

	def _insert(self, object_to_insert: Any):
		if isinstance(self.last_storage, tuple) and isinstance(self.item, int):
			self.last_storage = insertInTuple(self.last_storage,
				object_to_insert, self.item)
			self._updateImmutableChain(self.last_storage,
				self.immutable_storages_chain)
			if ((isinstance(self.last_mutable_storage, dict) and
			isinstance(self.item_to_access_immutable_storage, str)) or
			(isinstance(self.last_mutable_storage, list) and
			isinstance(self.item_to_access_immutable_storage, int))):
				self.last_mutable_storage[self. # type: ignore
				item_to_access_immutable_storage] = (self.
				immutable_storages_chain[0][0])
			else:
				raise TypeError("Unexpected type at assignment.")
		else:
			mutable_storage = self.last_storage # type: ignore
			mutable_storage[self.item] = object_to_insert # type: ignore

	def _updateImmutableChain(
		self,
		storage_to_update: Tuple[Any],
		immutable_storages_chain: List[Tuple[Any, ...]]
	) -> None:
		"""
		An updateImmutableChain func updates the entire chain starting with
		first elements.
		"""
		immutable_storages_chain.reverse()
		for ind in range(0, len(immutable_storages_chain)):
			item_to_next_storage = immutable_storages_chain[ind][1]
			if ind == 0:
				immutable_storages_chain[ind] = (storage_to_update, item_to_next_storage)
			else:
				current_storage = immutable_storages_chain[ind][0]
				previous_storage = immutable_storages_chain[ind - 1][0]
				item_to_current_storage = immutable_storages_chain[ind - 1][1]
				current_storage = insertInTuple(
					current_storage,
					previous_storage,
					item_to_current_storage
				)
				immutable_storages_chain[ind] = (current_storage, item_to_next_storage)
		immutable_storages_chain.reverse()

def insertInTuple(
	old_tuple: Tuple[Any],
	element_to_insert: Any,
	ind_to_insert: int
) -> Tuple[Any]:
	new_tuple: Tuple[Any, ...] = tuple()
	if not isinstance(ind_to_insert, int):
		raise Exception
	for (ind, elem) in enumerate(old_tuple):
		if ind == ind_to_insert:
			new_tuple += (element_to_insert,)
		else:
			new_tuple += (elem,)
	if element_to_insert not in new_tuple:
		raise Exception
	return new_tuple

def isIterable(obj: Any) -> bool:
	try:
		iter(obj)
	except TypeError:
		return False
	else:
		return True

def getDiscordMemberID(obj: Any) -> Any:
	if hasattr(obj, "id"):
		return obj.id
	else:
		print("getDiscordMemberID", f"the id attr hasn't been found in {obj}. Skip.")
		return obj
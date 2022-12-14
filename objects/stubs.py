from typing import Final

class Text:

	def __init__(self, text: str) -> None:
		self.text = text
		self.processText()
		self.checkText()

	def __repr__(self):
		return self.getText()

	def getText(self) -> str:
		return self.text

	def processText(self) -> None:
		pass

class StrOrIntText(Text):

	def checkText(self) -> None:
		if not self.text.isprintable():
			raise Exception # TODO

class IntText(Text):

	def checkText(self) -> None:
		if not self.text.isdigit():
			raise Exception()

class MentionText(Text):
	
	LEFT_BRACKET: Final = "<"
	RIGHT_BRACKET: Final = ">"

	def checkText(self) -> None:
		if not self.text.startswith(self.INDICATOR):
			raise Exception # TODO
		if not self.text[1:].isdigit():
			raise Exception

	def processText(self) -> None:
		self.text = self.text.removeprefix(self.LEFT_BRACKET)
		self.text = self.text.removesuffix(self.RIGHT_BRACKET)

class ChannelMentionText(MentionText): 

	INDICATOR: Final = "#"

class UserMentionText(MentionText):

	INDICATOR: Final = "@"
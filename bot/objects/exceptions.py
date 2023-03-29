from typing import Tuple
from string import ascii_letters

class Error(Exception):
	
	def __init__(self, error_text: str) -> None:
		self.error_text = error_text

	def getText(self) -> str:
		return self.error_text

class UndefinedError(Error):
	
	def __init__(self) -> None:
		self.error_text = ("При выполнении операции произошла"
		" неопределённая/серверная ошибка.\nПожалуйста,"
		" повторите попытку позже. + \n\nЕсли ошибка повторяется,"
		" обратитесь в [тех. поддержку](//сайт тех. поддержки VCS//),"
		" предоставив системную информацию ниже.")

class ParameterError(Error):

	def __init__(self, parameter_name: str) -> None:
		super().__init__("")
		self.parameter_name = parameter_name
		self.processParameterName()

	def getText(self) -> str:
		return self.error_text

	def getParameterName(self) -> str:
		return self.parameter_name

	def processParameterName(self) -> None:
		if self.parameter_name.startswith("d_"):
			self.parameter_name = self.parameter_name.removeprefix("d_")

class DeterminingParameterError(ParameterError):
	
	def __init__(self, parameter_name: str) -> None:
		super().__init__(parameter_name) #? странная херня: как-то раз по
		# невнимательности оставил super без () — так никаких исключений даже не
		# возбудилось. Воспроизводил в отдельном файле данный класс и суперкласс
		# Error — всё возбуждается, хотя здесь нету никакх excep-шенов, которые всё
		# перехватывают. Чё за приколы?
		self.error_text = ("Убедитесь, что вы указали все обязательные аргументы"
		", либо указали параметры явно. Не найденные параметры: {}").\
		format(self.parameter_name) # TODO embedded

class ActParameterError(ParameterError):

	def __init__(self, parameter_name: str) -> None:
		super().__init__(parameter_name)
		self.error_text = "Убедитесь, что вы указали знак действия в параметре {}".\
		format(self.parameter_name) # TODO embedded

class UnmatchingParameterTypeError(ParameterError):

	def __init__(self, arg: str, parameter_name: str, expect_parameter_types: Tuple['Text']): # TODO было бы не плохо уточнить, что речь
		# идёт о parameter и parameter_type, сделав это через аннотации.
		super().__init__(parameter_name)
		self.arg = arg
		self.error_text = ""
		self.expect_parameter_types: Tuple['Text'] = expect_parameter_types

	def getText(self) -> str:
		if not self.error_text:
			self.createErrorText()
		return self.error_text

	def createErrorText(self) -> None:
		# TODO нормальный вывод типов.
		self.error_text = ("Значение \"{}\" не соответствует типам: {} в параметре \"{}\". Пажалуста,"
		"измените значение параметра, либо укажите параметр явно.").format(self.arg, self.expect_parameter_types, self.parameter_name)

class Signal(Exception):
	pass

class WrongTextTypeSignal(Signal):
	pass

class WrongActSignal(Signal):
	pass
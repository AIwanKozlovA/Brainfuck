from lxml import etree
from lxml import *

# Определяем список команд Brainfuck
BF_COMMANDS = "><+-.,[]"

# Класс узла дерева разбора
u = 0
class Node:
  def __init__(self, type, value=None, children=None):
    self.type = type
    self.value = value
    self.children = children or []

  def to_xml(self):
    global u
    u+=1
    # print(u)
    node = etree.Element(self.type)
    if self.value is not None:
      node.text = str(self.value)
    for child in self.children:
    	if child != None:
            node.append(child.to_xml())
    return node
u = 0
# Класс парсера Brainfuck
class Parser:
  def __init__(self, code):
    self.code = code

  # Возвращает следующий символ без перемещения указателя
  def peek(self):
    if self.index >= len(self.code):
      return None
    return self.code[self.index]

  # Возвращает следующий символ и перемещает указатель
  def get(self):
    if self.index >= len(self.code):
      return None
    c = self.code[self.index]
    self.index += 1
    return c

  # Обрабатывает команду на инкремент значения в текущей ячейке памяти
  def parse_inc(self):
    return Node("inc")

  # Обрабатывает команду на декремент значения в текущей ячейке памяти
  def parse_dec(self):
    return Node("dec")

  # Обрабатывает команду на сдвиг указателя текущей ячейки памяти вправо
  def parse_right(self):
    return Node("right")

  # Обрабатывает команду на сдвиг указателя текущей ячейки памяти влево
  def parse_left(self):
    return Node("left")

  # Обрабатывает команду на вывод значения в текущей ячейке памяти
  def parse_out(self):
    return Node("out")

  # Обрабатывает команду на ввод значения в текущую ячейку памяти
  def parse_in(self):
    return Node("in")

  # Обрабатывает команду на начало цикла
  def parse_loop(self):
    node = Node("loop")
    self.get() # пропускаем '['
    while self.peek() != ']':
      node.children.append(self.parse_command())
    self.get() # пропускаем ']'
    return node

  # Обрабатывает одну команду Brainfuck и возвращает соответствующий узел AST
  def parse_command(self):
    c = self.get()
    if c is None:
      return None
    elif c == ">":
      return self.parse_right()
    elif c == "<":
      return self.parse_left()
    elif c == "+":
      return self.parse_inc()
    elif c == "-":
      return self.parse_dec()
    elif c == ".":
      return self.parse_out()
    elif c == ",":
      return self.parse_in()
    elif c == "[":
      return self.parse_loop()

  # Строит AST для всей программы
  def parse(self):
    node = Node("program")
    while self.peek() is not None:
      node.children.append(self.parse_command())
    return node

  # Запускает парсер
  def run(self):
    self.index = 0
    return self.parse()

# Читаем код Brainfuck из файла input.bf
with open("input.bf", "r") as f:
  code = f.read()
# print(len(code))
# Строим AST с использованием парсера
parser = Parser(code)
ast = parser.run()
# print(type(ast))
# Сохраняем AST в файле формата XML
root = ast.to_xml()
tree = etree.ElementTree(root)
with open("output.xml", "wb") as f:
  f.write(etree.tostring(tree, pretty_print=True))

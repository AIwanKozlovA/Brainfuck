import xml.etree.ElementTree as ET

"""
Функция: generate_ast

Описание: Преобразует код Brainfuck в абстрактное синтаксическое дерево (AST).

Аргументы:
- code: строка с кодом Brainfuck.

Возвращаемое значение: Строка, представляющая AST в формате XML.

Логика работы:
1. Инициализируется указатель ptr в 0 и AST-дерево ast_root.
2. Пока указатель ptr не выходит за границы строки code:
   a. Если текущий символ в строке code - ">", то в AST добавляется элемент "t_SHIFT_RIGHT".
   b. Если текущий символ в строке code - "<", то в AST добавляется элемент "t_SHIFT_LEFT".
   c. Если текущий символ в строке code - "+", то в AST добавляется элемент "t_INCREASE".
   d. Если текущий символ в строке code - "-", то в AST добавляется элемент "t_DECREASE".
   e. Если текущий символ в строке code - ".", то в AST добавляется элемент "t_OUTPUT".
   f. Если текущий символ в строке code - ",", то в AST добавляется элемент "t_INPUT".
   g. Если текущий символ в строке code - "[", то в AST добавляется элемент "t_LOOP".
      i. Указатель ptr увеличивается на 1.
      ii. Пока указатель ptr не выходит за границы строки code и текущий символ не является "]", выполняется следующее:
          1. Если текущий символ в строке code - ">", то в элемент "t_LOOP" добавляется элемент "t_SHIFT_RIGHT".
          2. Если текущий символ в строке code - "<", то в элемент "t_LOOP" добавляется элемент "t_SHIFT_LEFT".
          3. Если текущий символ в строке code - "+", то в элемент "t_LOOP" добавляется элемент "t_INCREASE".
          4. Если текущий символ в строке code - "-", то в элемент "t_LOOP" добавляется элемент "t_DECREASE".
          5. Если текущий символ в строке code - ".", то в элемент "t_LOOP" добавляется элемент "t_OUTPUT".
          6. Если текущий символ в строке code - ",", то в элемент "t_LOOP" добавляется элемент "t_INPUT".
          7. Если текущий символ в строке code - "[", то вызывается функция generate_nested_loop, которая возвращает вложенное AST-дерево и новое значение указателя ptr.
          8. Указатель ptr увеличивается на 1.
3. Указатель ptr увеличивается на 1.
4. Возвращается AST-дерево ast_root в формате XML.

"""
def generate_ast(code):
    ptr = 0
    ast_root = ET.Element("program")
    while ptr < len(code):
        if code[ptr] == ">":
            ast_root.append(ET.Element("t_SHIFT_RIGHT"))
        elif code[ptr] == "<":
            ast_root.append(ET.Element("t_SHIFT_LEFT"))
        elif code[ptr] == "+":
            ast_root.append(ET.Element("t_INCREASE"))
        elif code[ptr] == "-":
            ast_root.append(ET.Element("t_DECREASE"))
        elif code[ptr] == ".":
            ast_root.append(ET.Element("t_OUTPUT"))
        elif code[ptr] == ",":
            ast_root.append(ET.Element("t_INPUT"))
        elif code[ptr] == "[":
            loop = ET.Element("t_LOOP")
            ast_root.append(loop)
            ptr += 1
            while ptr < len(code) and code[ptr] != "]":
                if code[ptr] == ">":
                    loop.append(ET.Element("t_SHIFT_RIGHT"))
                elif code[ptr] == "<":
                    loop.append(ET.Element("t_SHIFT_LEFT"))
                elif code[ptr] == "+":
                    loop.append(ET.Element("t_INCREASE"))
                elif code[ptr] == "-":
                    loop.append(ET.Element("t_DECREASE"))
                elif code[ptr] == ".":
                    loop.append(ET.Element("t_OUTPUT"))
                elif code[ptr] == ",":
                    loop.append(ET.Element("t_INPUT"))
                elif code[ptr] == "[":
                    nested_loop, ptr = generate_nested_loop(code, ptr)
                    loop.append(nested_loop)
                ptr += 1
        ptr += 1

    #Форматируем дерево
    tree = ET.ElementTree(ast_root)
    ET.indent(tree, '\t')
   #Записываем дерево в файл output.xml
    tree.write("output.xml", encoding="utf-8", xml_declaration=True)
    retur ET.tostring(ast_root, encoding="unicode")


"""
Функция: generate_nested_loop

Описание: Генерирует вложенное AST-дерево для элемента "t_LOOP" внутри главного AST-дерева.

Аргументы:
- code: строка с кодом Brainfuck.
- ptr: текущее значение указателя.

Возвращаемое значение: Кортеж из элемента "t_LOOP" вложенного AST-дерева и нового значения указателя ptr.

Логика работы:
1. Инициализируется элемент "t_LOOP" вложенного AST-дерева loop и указатель ptr увеличивается на 1.
2. Пока указатель ptr не выходит за границы строки code и текущий символ не является "]", выполняется следующее:
   a. Если текущий символ в строке code - ">", то в элемент "t_LOOP" добавляется элемент "t_SHIFT_RIGHT".
   b. Если текущий символ в строке code - "<", то в элемент "t_LOOP" добавляется элемент "t_SHIFT_LEFT".
   c. Если текущий символ в строке code - "+", то в элемент "t_LOOP" добавляется элемент "t_INCREASE".
   d. Если текущий символ в строке code - "-", то в элемент "t_LOOP" добавляется элемент "t_DECREASE".
   e. Если текущий символ в строке code - ".", то в элемент "t_LOOP" добавляется элемент "t_OUTPUT".
   f. Если текущий символ в строке code - ",", то в элемент "t_LOOP" добавляется элемент "t_INPUT".
   g. Если текущий символ в строке code - "[", то вызывается функция generate_nested_loop, которая возвращает вложенное AST-дерево и новое значение указателя ptr, и это вложенное AST добавляется в элемент "t_LOOP".
   h. Указатель ptr увеличивается на 1.
3. Возвращается кортеж из элемента "t_LOOP" вложенного AST-дерева и нового значения указателя ptr.
"""
def generate_nested_loop(code, ptr):
    loop = ET.Element("t_LOOP")
    ptr += 1
    while ptr < len(code) and code[ptr] != "]":
        if code[ptr] == ">":
            loop.append(ET.Element("t_SHIFT_RIGHT"))
        elif code[ptr] == "<":
            loop.append(ET.Element("t_SHIFT_LEFT"))
        elif code[ptr] == "+":
            loop.append(ET.Element("t_INCREASE"))
        elif code[ptr] == "-":
            loop.append(ET.Element("t_DECREASE"))
        elif code[ptr] == ".":
            loop.append(ET.Element("t_OUTPUT"))
        elif code[ptr] == ",":
            loop.append(ET.Element("t_INPUT"))
        elif code[ptr] == "[":
            nested_loop, ptr = generate_nested_loop(code, ptr)
            loop.append(nested_loop)
        ptr += 1
    return loop, ptr


def main():
    code = ""
    with open(input("Введите путь к файлу с расширенем .bf\n"), "r") as file:
        code = file.read()
    #code = "--[++--]++"
    ast = generate_ast(code)
    print(ast)

if __name__ == "__main__":
    main()

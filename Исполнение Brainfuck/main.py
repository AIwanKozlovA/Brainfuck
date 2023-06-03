sim = '><+-.,[]'


"""
Функция: clear_code

Описание: Функция очищает код,  от символов, которые не используются в языке brainfuck

Аргументы:
- code: строка с кодом Brainfuck.
"""
def clear_code(code): # очищает код от лишнего
    return ''.join(c for c in code if c in sim)
   
    
"""
Функция: ras_on_blocks

Описание: Позволяет определить начало и конец каждого цикла Brainfuck

Аргументы:
- code: строка с кодом Brainfuck.
"""  

 
def ras_on_blocks(code): # разделяем код на блоки
    otkr = []
    blocki = {}
    for i in range(len(code)):
        if code[i] == '[':
            otkr.append(i)
        elif code[i] == ']':
            blocki[i] = otkr[-1]
            blocki[otkr.pop()] = i
    return blocki


"""
Функция: launch_brainfuck

Описание: функция, выполняющая интерпретацию языка программирования Brainfuck

Аргументы:
- code: строка с кодом Brainfuck.
""" 


def launch_brainfuck(code): # запуск кода
    code = clear_code(code)
    x = i = 0
    bf = {0: 0}
    blocks = ras_on_blocks(code)
    dl = len(code)
    while i < dl:
        sym = code[i]
        if sym == sim[0]:
            x += 1
            bf.setdefault(x, 0)
        elif sym == sim[1]:
            x -= 1
        elif sym == sim[2]:
            bf[x] += 1
        elif sym == sim[3]:
            bf[x] -= 1
        elif sym == sim[4]:
            print(chr(bf[x]), end='')
        elif sym == sim[5]:
            bf[x] = int(input('Введите: '))
        elif sym == sim[6]:
            if not bf[x]: i = blocks[i]
        elif sym == sim[7]:
            if bf[x]: 
            	i = blocks[i]
        i += 1
        
        
def main():
	file = open("code.bf", "r")
	code = file.read()
	launch_brainfuck(code)
	
	
if __name__ == "__main__":
    main()

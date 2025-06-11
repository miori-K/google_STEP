#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_mult(line, index):
    token = {'type': 'MULT'}
    return token, index + 1

def read_divi(line, index):
    token = {'type': 'DIVI'}
    return token, index + 1

def read_open(line,index):
    token = {'type': 'OPEN'}
    return token, index + 1

def read_close(line,index):
    token = {'type': 'CLOSE'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_mult(line, index)
        elif line[index] == '/':
            (token, index) = read_divi(line, index)
        elif line[index] == '(':
            (token, index) = read_open(line, index)
        elif line[index] == ')':
            (token, index) = read_close(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def evaluate(tokens): #メインの計算（）に対応
    index = 0
    stack = []

    while index < len(tokens):
        if tokens[index]['type'] == 'OPEN':
            stack.append(index) #(を保存
            index += 1
        elif tokens[index]['type'] == 'CLOSE':
            if stack == []:
                break
            else:
                open_index = stack.pop()#最後に入れた(を取り出す
                close_index = index
                inner_tokens = tokens[open_index +1 :close_index] #(は含めない
                value = evaluate(inner_tokens) #再帰呼び出し
                tokens[open_index:close_index+1] = [{'type': 'NUMBER', 'number': value}]#()部分を書き換えてtoken列を変更
                index = 0 #初めに戻る
        else:
            index += 1

    tokens = multdivi(tokens)
    return plusminus(tokens)

def multdivi(tokens): #掛け算、割り算を計算
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 0

    while index < len(tokens):
        if tokens[index]['type'] == 'MULT':
            result =tokens[index-1]['number']*tokens[index+1]['number']
            tokens[index-1:index+2] =  [{'type': 'NUMBER', 'number': result}]
            index -= 1
        elif tokens[index]['type'] == 'DIVI':
            result =tokens[index-1]['number']/tokens[index+1]['number']
            tokens[index-1:index+2] =  [{'type': 'NUMBER', 'number': result}]
            index -= 1
        index += 1

    return tokens

def plusminus(tokens): #足し算、引き算を計算
    answer = 0
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
        index += 1
    return answer

def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("9/2+4.0")
    test("2.5+5*10")
    test("4-8*0")
    test("6/3*3")
    test("3*(9-3)")
    test("((8+2)-7)*2")
    test("2+(9-3)*4/(5-3)+((8-4)/2)")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    print("answer = %f\n" % actual_answer)

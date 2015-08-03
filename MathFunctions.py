from decimal import Decimal
import math

functions = ["sin", "cos", "tan", "sqrt", "abs", "factorial", "pi"]

def factorial(x):
    count = 1
    result = 1

    while count <= x:
        result *= count
        count += 1

    return result

# <summary>
# -n: The number to compute the square root of (int), must be > 0
# -precision:
# </summary>
def sqrt(n, precision = 5):
    return math.sqrt(n)

    base = 0
    isPerfectSquare = False
    result = 0.0

    if n < 0:
        return -1
    elif n == 0:
        return 0

    # Find the number that, when squared is less than n
    # If a number squared = n, print that number

    for i in range(n):
        if i * i < n:
            base = i
        elif i * i == n:
            isPerfectSquare = True
            base = i
            break
        elif i * i > n:
            break

    if isPerfectSquare:
        return base
    else:
        start = (n - base * base) * 100
        factor = base + base % 10
        tmpFactor = factor

        result += base

        for i in range(precision):
            if i > 0:
                # Double the last digit
                factor += factor % 10;

            # Find the number that, when appending another digit to
            # factor, times that digit is less than start
            for j in range(10):
                tmpFactor = 10 * factor + j;

                if tmpFactor * j > start:
                    factor = factor * 10 + (j - 1)

                    result = appendDigit(result, j - 1, 0 - (i + 1))
                    start = (start - (factor * (j - 1))) * 100
                    break

    return result

def appendDigit(n, digit, place):
    n += (10 ** place) * digit
    return n;

def sin(x, precision = 5):
    return math.sin(x)
    # answer = 0

    # for n in range(1, precision):
    #     answer += (((-1.0) ** n) * (x ** (2 * n + 1))) / factorial(2 * n + 1)

    # return answer

def cos(x, precision = 5):
    return math.cos(x)

def tan(x):
    return math.tan(x)

def abs(x):
    if x >= 0:
        return x
    else:
        return -x

def shuntingYard(expression):
    operatorStack = []
    numCount = 0
    count = 0
    unaryMinus = False
    outputStr = ""
    found_func = False

    expression = expression.replace(" ", "")
    expression = expression.replace("pi", '(' + str(math.pi) + ')')

    # Loop through characters
    while count < len(expression):
        start = count

        # Loop through functions to see if there's
        # a function at the current spot
        for i in functions:
            found = False
            count = start

            # Check if a function is entered
            if expression[count:count + len(i)] == i:
                # push the function onto the stack
                operatorStack.append(i)

                # advance position to after the function
                count += len(i)
                found_func = True
                break

        if count >= len(expression):
            break

        while isNum(expression[count]):
            # if a unary minus was intended,
            # append a - to the output string
            if unaryMinus and count == start:
                outputStr += '-'
                unaryMinus = False

            # add the digit to the output
            outputStr += expression[count]

            # advance 1 further in the string
            count += 1

            if count >= len(expression):
                break

            # check if a decimal is in the string
            # if so, append it to the output
            if expression[count] == '.':
                outputStr += '.'
                count += 1

        if count >= len(expression):
            break

        # Add operator to operator list according to precedence
        if isOp(expression[count]):

            # Check if the '-' is being used has a negative sign.
            # This could happen in a few cases:
            # 1. - is the first character in the string
            # 2. ( precedes a -
            # 3. - follows another operator
            if expression[count] == '-' and (count - 1 < 0 or isOp(expression[count - 1]) or expression[count - 1] == '(' or precedesFunc(expression, count)):
                if count + 1 < len(expression):

                    # If the unary minus is used before an open
                    # parenthesis, then append -1* before it
                    if expression[count + 1] == '(' or precedesFunc(expression, count):
                        expression = expression[:count] + "-1*" + expression[count + 1:]

                unaryMinus = True
            else:
                outputStr += " "

                # get the precedence of the current operator
                opPrec = getPrecedence(expression[count])

                if len(operatorStack) >= 1:
                    if opPrec == getPrecedence(operatorStack[-1]):
                        if expression[count] != '^':
                            outputStr += operatorStack[-1] + " "

                            # Pop back
                            operatorStack = operatorStack[:-1]
                    elif opPrec < getPrecedence(operatorStack[-1]):
                        outputStr += operatorStack[-1] + " "
                        operatorStack = operatorStack[:-1]

                # push the found operator onto the stack
                operatorStack.append(expression[count])

            count += 1

        # break if the count is >= the length of the expression
        if count >= len(expression):
            break

        if expression[count] == '(':

            # Check if a number is used before a parenthesis
            # (implied multiplication)
            # If so, inserts * before the parenthesis
            if isNum(expression[count - 1]) and count - 1 >= 0:
                expression = expression[:count] + "*" + expression[count:]
                continue
            else:
                # push the open parenthesis onto the stack
                operatorStack.append('(')
            # index = len(operatorStack) - 1

            count += 1

        if expression[count] == ')':

            # pop everything off the stack until, and including
            # when ( is on the top of the stack
            while 1:
                if operatorStack[-1] == '(':
                    operatorStack = operatorStack[:-1]
                    break

                # append the operator to the output string
                outputStr += " " + operatorStack[-1]
                operatorStack = operatorStack[:-1]

            # if the closed parenthesis belonged to a function,
            # pop the function off the stack and add it to the
            # output string
            if found_func:
                if operatorStack[-1] != '(':
                    outputStr += " " + operatorStack[-1]
                    operatorStack = operatorStack[:-1]
                    found_func = False

            # move one character further in the string
            count += 1

    # a counter for the index of the last
    # operator in the operator stack
    count2 = len(operatorStack) - 1

    # Append operators from the stack to
    # the string starting from the top
    while count2 >= 0:
        outputStr += " " + operatorStack[count2]
        count2 -= 1

    return outputStr

def solveShuntingExpression(expression):
    answer = Decimal(0.0)
    operands = expression.split(" ")
    count = 0
    numStack = []
    i = 0

    if len(operands) == 1 and not '(' in operands[0]:
        return operands[0]

    count = 0

    while count < len(operands):
        result = 0.0

        if not isOp(operands[count]):
            is_func = False

            for i in functions:
                if operands[count] == i:
                    is_func = True
                    v = numStack[-1]
                    numStack = numStack[:-1]
                    numStack.append(doFunction(i, v))

            if not is_func:
                numStack.append(float(operands[count]))
        else:
            result = performOp(operands[count], Decimal(numStack[-2]), Decimal(numStack[-1]))
            numStack = numStack[:-2]
            numStack.append(result)

            answer = result

        count += 1

    if len(numStack) == 1:
        answer = numStack[0]

    return str(answer)

def doFunction(func, x, precision = 5):
    if func == "sin":
       return sin(x, precision)
    if func == "sqrt":
       return sqrt(int(x), precision)
    if func == "factorial":
        return factorial(x)
    if func == "abs":
        return abs(x)
    if func == "cos":
        return cos(x)
    if func == "tan":
        return tan(x)

# ------------------- Helper functions for Shunting Yard ----------------
def performOp(op, a, b):

        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '/':
            if b != 0:
                return a / b
            else:
                return "Error: division by zero."
        elif op == '*':
            return a * b
        elif op == '^':
            return a ** b

def isNum(char):
    return char in "1234567890"

def isOp(char):
    return char in "+-*/^"

# Returns true if the character at position |i| 
# in the string |expression| precedes the name of a
# function.
def precedesFunc(expression, i):
    for func in functions:
        l = len(func)

        if expression[i + 1:i + 1 + l] == func:
            return True
    return False

def getPrecedence(op):
    if op == '^':
        return 3
    if op == '*' or op == '/':
        return 2
    if op == '+' or op == '-':
        return 1
# -----------------------------------------------------------------------

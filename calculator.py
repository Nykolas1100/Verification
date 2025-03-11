import abc
from Combinator import *

class Expr(abc.ABC):
    def evaluate(self):
        ...

class num(Expr):
    def __init__(self, number: int):
        self.val = number
    def evaluate(self):
        return self
    def __str__(self):
        return str(self.val)
    
class plus(Expr):
    def __init__(self, exprLeft: Expr, exprRight: Expr):
        self.left = exprLeft
        self.right = exprRight
    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return num(left.val + right.val)
    def __str__(self):
        return f"({self.left}) + ({self.right})"
    
class minus(Expr):
    def __init__(self, exprLeft: Expr, exprRight: Expr):
        self.left = exprLeft
        self.right = exprRight
    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return num(left.val - right.val)
    def __str__(self):
        return f"({self.left}) - ({self.right})"
    
class boolean(Expr):
    def __init__(self, value: bool):
        self.val = value
    
    def evaluate(self):
        return self
    
    def __str__(self):
        return "True" if self.val else "False"

class equal(Expr):
    def __init__(self, exprLeft: Expr, exprRight: Expr):
        self.left = exprLeft
        self.right = exprRight
    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if left.val == right.val:
            return num(right.val)
        return boolean(False)
        # return self.left.evaluate()==self.right.evaluate()
    def __str__(self):
        return f"({self.left}) = ({self.right})"
    
def combining(left: Expr, middle: str, right: Expr):
    # print("combining: " + str(left) + " " + str(middle) + " " + str(right))
    match middle:
        case "+":
            return plus(left, right)
        case "-":
            return minus(left, right)
        case "=":
            return equal(left, right)
        
def helper(left: Expr, rest: Expr):
    for _, right in rest:
        left = equal(left, right)
    return left

(expr, exprImpl) = recparser()

digit = pchar('0') | pchar('1') | pchar('2') | pchar('3') | pchar('4') | pchar('5') | pchar('6') | pchar('7') | pchar('8') | pchar('9')
addition = pchar('+')
subtraction = pchar('-')
equality = pchar('=')
lparen = pchar('(')
rparen = pchar(')')

# parse arbitrary length number
n: Parser[Expr] = (pmany1(digit) > (lambda digits: num(int("".join(digits))))) ^ "n"

paren: Parser[Expr] = pbetween(lparen, expr, rparen) ^ "paren"

# pseq(equality, expr) | 

suffix: Parser[Expr] = (pseq(addition, expr) | pseq(subtraction, expr)) ^ "suffix"

prefix: Parser[Expr] = ((pseq(n, suffix) > (lambda parsed: combining(parsed[0], parsed[1][0], parsed[1][1]) if parsed[1] else parsed[0])) | n) ^ "prefix"

exprImpl[0] = ((pseq(paren, suffix) > (lambda parsed: combining(parsed[0], parsed[1][0], parsed[1][1]) if parsed[1] else parsed[0])) | paren | prefix) ^ "expr"

# grammar: Parser[Expr] = pleft(expr, peof()) ^ "grammar"

# equation: Parser[Expr] = (((pseq(pleft(expr, equality), expr))) > (lambda parsed: combining(parsed[0], "=", parsed[1]))) | expr ^ "equation"

equations: Parser[Expr] = ((pseq(expr, pmany1(pseq(equality, expr)))) > (lambda parsed: helper(parsed[0], parsed[1]))) | expr ^ "equation"

grammar: Parser[Expr] = pleft(equations, peof()) ^ "grammar"

# # parse left and right of addition
# p: Parser[Expr] = (pseq(n, pright(addition, n)) > (lambda parsed: plus(parsed[0], parsed[1]))) ^ "p"

# # parse left and right of subtraction
# m: Parser[Expr] = (pseq(n, pright(subtraction, n)) > (lambda parsed: minus(parsed[0], parsed[1]))) ^ "m"

# # parse left and right of equality
# e: Parser[Expr] = (pseq(n, pright(equality, n)) > (lambda parsed: equal(parsed[0], parsed[1]))) ^ "e"

def balanced(expression):
    match expression:
        case num():
            return True
        case plus() | minus() | equal():
            if expression.left == None or expression.right == None:
                return False
            return balanced(expression.left) and balanced(expression.right)
        case _:
            print("Input must be of type Expr")
            return False
        
def isEquation(expression):
    def count(e):
        match e:
            case num():
                return 0
            case plus() | minus():
                return 0 + count(e.left) + count(e.right)
            case equal():
                return 1 + count(e.left) + count(e.right)
            case _:
                return 0
    # print("count = " + str(count(expression)))
    return count(expression) == 1

def isEqual(expression):
    return expression.evaluate()
    
def main():
    # one = num(1)
    # two = num(2)
    # print(one.evaluate())
    # print(plus(one, two).evaluate())
    # print(balanced(minus(minus(num(3), num(2)), num(4))))
    # print(isEquation(minus(minus(num(3), num(2)), num(4))))
    # print(isEquation(equal(minus(num(3), num(2)), num(4))))
    # print(isEqual(equal(minus(num(3), num(2)), num(4))))
    # print(isEqual(equal(minus(num(6), num(2)), num(4))))
    # equals = equal(1, equal(1, 1))
    # print(equals)
    # print(isEquation(equals))
    user = input("Enter your code: ")
    code = grammar(Input(user, is_debug = False)).result
    print(code)
    if not(balanced(code)):
        print("equation unbalanced")
        return
    if not(isEquation(code)):
        print("code is not an equation")
    if not(isEqual(code)):
        print("the equation is false")
        return
    print(code.evaluate())
    # input0 = Input("(33)", is_debug = False)
    # ast_maybe: Outcome[Expr] = grammar(input0)
    # print(ast_maybe)
    # input1 = Input("1+2", is_debug = False)
    # ast_maybe: Outcome[Expr] = grammar(input1)
    # print(ast_maybe)
    # input2 = Input("(1-2)", is_debug = False)
    # ast_maybe: Outcome[Expr] = grammar(input2)
    # print(ast_maybe)
    # input3 = Input("(1-2)+4", is_debug = False)
    # ast_maybe: Outcome[Expr] = grammar(input3)
    # print(ast_maybe)
    # input4 = Input("1+1+1+1", is_debug = False)
    # ast_maybe: Outcome[Expr] = grammar(input4)
    # print(ast_maybe)
    # print(type(grammar(input0).result))
    # print(balanced(grammar(input4).result))

if __name__=="__main__":
    main()

# Return an expr to create a closed language - dynamic type checks for each data type
# Add unit tests!
# Move events from today to tomorrow
# Data structure with partial programs
# Prevent hallucination of missing values
# Parse calendar language
# Watermark with whitespace - different types - ID
# Fingerprint prompt
# Matt Frederickson
# Start with hard then consider soft constraints
# Responsibility of language versus the verifier
# Fuzz test - random input explosion
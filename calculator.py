import abc

class Expr(abc.ABC):
    def evaluate(self):
        ...

class num(Expr):
    def __init__(self, number):
        self.val = number
    def evaluate(self):
        return self.val
    
class plus(Expr):
    def __init__(self, exprLeft, exprRight):
        self.left = exprLeft
        self.right = exprRight
    def evaluate(self):
        return self.left.evaluate()+self.right.evaluate()
    
class minus(Expr):
    def __init__(self, exprLeft, exprRight):
        self.left = exprLeft
        self.right = exprRight
    def evaluate(self):
        return self.left.evaluate()-self.right.evaluate()

class equal(Expr):
    def __init__(self, exprLeft, exprRight):
        self.left = exprLeft
        self.right = exprRight
    def evaluate(self):
        return self.left.evaluate()==self.right.evaluate()
    
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
    code = input("Enter your code: ")
    if not(balanced(eval(code))):
        print("equation unbalanced")
        return
    if not(isEquation(eval(code))):
        print("code is not an equation")
    if not(isEqual(eval(code))):
        print("the equation is false")
        return
    print((eval(code).evaluate()))

if __name__=="__main__":
    main()
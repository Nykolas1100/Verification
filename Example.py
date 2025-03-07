from abc import ABC, abstractmethod
from Combinator import *

# a varition on the example we did together
# define a "AST" interface
class Expr(ABC):
    @abstractmethod
    def eval(self):
        pass

# a concrete AST node
class FThing(Expr):
    def eval(self):
        print("peanut butter")
        
    # Python equivalent to Java's toString
    def __str__(self):
        return "F"

# another concrete AST node
class OThing(Expr):
    def eval(self):
        print("jelly")
        
    def __str__(self):
        return "O"

# yet another concrete AST node
class Sequence(Expr):
    exprs: List[Expr] = []

    # we need a constructor here because we want
    # to pass Sequence a list of expressions when
    # we make the node
    def __init__(self, exprs: List[Expr]):
        self.exprs = exprs

    def eval(self):
        # get all of the expressions and run them
        for e in self.exprs:
            e.eval()
            
    def __str__(self):
        return "[" + ", ".join(map(lambda e: str(e), self.exprs)) + "]"

# make an input
i = Input("fooooo")

# make a parser;
# Note that I explicitly tell Python that these are Expr parsers, otherwise
# it will infer their types as Parser[OThing] or Parser[FThing] and then
# when I try to make a list it gets upset because it can't figure out that
# OThing and FThing are just Expr and that the list should be List[Expr].
# Alternatively, just don't use type annotations and Python will do whatever.
f: Parser[Expr] = pchar('f') > (lambda _: FThing())
o: Parser[Expr] = pchar('o') > (lambda _: OThing())
p: Parser[Expr] = (f + pmany1(o)) > (lambda tup: Sequence([tup[0]] + tup[1] ))

#   example of f above with debug output
# f: Parser[Expr] = (pchar('f') > (lambda _: FThing()) ^ "fthing")
#   uncomment and then enable debugging when constructing Input
# i = Input("fooooo", is_debug = True)

# run the parser on the input
ast_maybe: Outcome[Expr] = p(i)

# print the resulting AST
print(ast_maybe)

# RUN the AST if the input made sense
match ast_maybe:
    case Success(ast,_):
        ast.eval()
    case Failure(_,_):
        print("Did not parse!")

# handy dandy operator overloads:
# + is pseq
# > is pfun (aka |>> in F#)
# | is alt (aka <|> in F#)
# ^ is pdebug (aka <!> in F#)
# << is pleft
# >> is pright
# you can just use the function names, though, if you don't like the overloads
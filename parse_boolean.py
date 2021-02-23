from boolean import BooleanAlgebra, Symbol

a = BooleanAlgebra()

expr1 = a.parse("(cristina and lopes) and acm and computers")
symbols = expr1.get_symbols()

print(expr1)

'''
- make BooleanAlgebra() object
- lowercase the expression (query) before parsing
- parse the expression 
- call simplify on expression object
- recursively traverse 
    - Base case: if every arg is of type Symbol, return result of arg
        otherwise, go deeper
        if in an AND, get intersection of args
        if in an OR, merge results of args
        if in NOT, get everything NOT in args
            given: a NOT b
            check every term in other args, to see if its not inside NOTed arg
        if no other args, check index
'''
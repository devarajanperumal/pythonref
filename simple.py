# simple.py

x = 42

def spam():
    print('x is', x)

def run():
    print('calling spam')
    spam()

print('simple namespace',__name__)
run()
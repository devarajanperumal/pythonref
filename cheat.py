#!/usr/bin/env python3
# cheat.py

"""David Beazley
1) To change script into executable: 
-Pound Bang or shebang will use whatever python executable appears first in the user's environment variable $PATH.
-chmod +x commandline.py

more on environment:
-Environment Variables are key-value pairs.
-local(only that shell)
#FILE=”output.txt”
#echo $FILE
output.txt
-global(the shell and all children)
#export FILE=”output.txt”
#echo $FILE
output.txt
-alternate set(local) and setenv(global)
-view environment variables: printenv, env, set

2) Debug
-run in interactive mode: python -i file.py
>>> import pdb
>>> pdb.pm()
>>> list

"""

import sys
import csv
import itertools
import json
import portie
from abc import ABC, abstractclassmethod

def commandline():
    if len(sys.argv) != 3:
        raise SystemExit('Usage interpreter.py arg1 arg2')
    print('arg1:{} arg2:{}'.format(sys.argv[1], sys.argv[2]))

def printing():
    out = 'python-version'
    print(out, sys.version_info[0], end='\t')    # multiple args, kwargs: sep=' ',end='\n',file=sys.stdout
    print(out, sys.version_info[0], sep='-')

def writefile():
    with open('Data/simple.txt', 'w') as f:
        print('Printing to a file using print', file=f)
        f.write('Printing to a file using write\n')
        lines = ['line 1\n', 'line 2\n', 'line 3\n']
        f.writelines(lines)

def setbreakpoint():
    loop = 10
    while loop > 0:
        loop -= 1
        import pdb; pdb.set_trace()         # set breakpoint
    # (Pdb) loop=3                          # change something
    # (Pdb) pdb.set_trace = lambda: None    # remove breakpoint
    # (Pdb) continue

def readfile():
    '''Any read pushes the pointer to the next line
    '''
    print('using read():')
    with open('Data/portfolio.csv', 'r') as f:
        data = f.read()       # into 1 string
        print(data)
    print('\nusing readlines()')
    with open('Data/missing.csv', 'r') as f:
        data = f.readlines()    # into 1 list    
        print(data)
    print('\nreading line by line')
    with open('Data/portfolio2.csv', 'r') as f:
        headers = next(f)       # skip 1 line
        print(headers)
        for line in f:
            print(line)
    print('\nreading line by line and add line no')
    with open('Data/portfolio2.csv', 'r') as f:
        for lineno, line in enumerate(f, start=1):
            print('lineno:', lineno, 'line:', line)
    print('\nusing csv.reader()')
    with open('Data/portfolio3.csv', 'r') as f:
        rows = csv.reader(f)
        header = next(rows)
        print(header)
        for row in rows:
            print(row)

def stringops():
    line = ' "AA","2007-06-11",100,32.20\n'
    parts = line.strip().split(',')
    joined = '-'.join(parts)
    print(joined)
    parts[0], parts[1]  = parts[0].strip('"'), parts[1].strip('"')
    parts[2], parts[3] = int(parts[2]), float(parts[3])
    print(parts)
    data = [(16,48000,3909.9875555478193), (17,51000,926.2791703626017), (18,48930.13866690578,0)]
    for month, paid, principal in data:
        # print(month, paid, principal)
        # print('{:<5d}   {:<10.2f}  {:<10.2f}'.format(month, paid, principal))
        print('{:<{}d}   {:<{}.2f}  {:<{}.2f}'.format(month, 5, paid, 10, principal, 10))

def funcoptional(arg1, arg2, *, option='default'):
    '''option can only be provided with keywords
    '''
    print('arg1:', arg1)
    print('arg2:', arg2)
    print('option:', option)

def funckwonly(*, arg, option='default'):
    '''all must be keywords. Zero positional.
    '''
    print('arg:', arg)
    print('option:', option)

def argskwargs(arg, *args, **kwargs):
    '''
    At lease 1 positional argument, arg
    '''
    print('arg:', arg)
    print('args:', args, 'type:', type(args))
    print('kwargs', kwargs)

def read_portfolios(filename, *, error='warn'):
    if error not in {'silent', 'raise', 'warn'}:
        raise ValueError("error must be 'silent', 'raise' or 'warn'(default)")
    portfolios = []
    with open(filename, 'r') as f:
        _ = next(f) # skips header
        rows = csv.reader(f)
        for rowno, row in enumerate(rows):
            try:
                row[2] = int(row[2])
                row[3] = float(row[3])
            except ValueError as err:
                if error=='warn':
                    print(f'{rowno}: {row} --> {err}')
                elif error=='silent':
                    pass
                else:
                    raise
                continue
            portfolios.append({
                    'name':row[0],
                    'date': row[1],
                    'shares': row[2],
                    'price': row[3]
                })
    return portfolios    

def sum_listcomp(portfolios):
    return sum([portfolio['shares']*portfolio['price'] for portfolio in portfolios])

def if_listcomp(portfolios):
    return [portfolio for portfolio in portfolios if portfolio['shares']>100]

def setcomp(portfolios):
    return {portfolio['name'] for portfolio in portfolios}

def dict_from_zip(names, pricesdata):
    prices = pricesdata.split()
    return {name:float(price) for name,price in zip(names,prices)}

def sorting(portfolios):
    # portfolios.sort(key= lambda x: x[0])
    return sorted(portfolios, key= lambda x: x['name'])

def min_max(portfolios):
    minimum_price = min(portfolios, key=lambda x: x['price'])
    maximum_price = max(portfolios, key=lambda x: x['price'])
    return minimum_price, maximum_price

def grouping(portfolios):
    grouped = itertools.groupby(sorting(portfolios), key=lambda x: x['name']) # groupby needs sorting using the same key
    grouped_dict = {}
    for name, items in grouped:
        if name not in grouped_dict: # checking for key in dictionary
            grouped_dict[name] = []
        for item in items:
            grouped_dict[name].append(item)
    return grouped_dict

def grouping_super(portfolios):
    return {name:[item for item in items] for name, items in itertools.groupby(sorting(portfolios), key=lambda x: x['name'])}

def converting(portfolios):
    return json.dumps(portfolios)

def about_import():
    '''import statetment will execute the module
    from <module> import <something> will also execute the entire module
    Python looks for module to import in dirs in sys.path. We can append a new path
    >>> import sys
    >>> sys.path
    ['', '/Library/Frameworks/Python.framework/Versions/3.7/lib/python37.zip', '/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7', '/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/lib-dynload', '/Users/devarajanperumal/pythonref/env/lib/python3.7/site-packages']
    >>> sys.path.append('..')
    Or we can set temp environment var and run Python
    (env) Devarajans-MacBook-Pro:temp devarajanperumal$ env PYTHONPATH=.. python
    '''
    print('about_import namespace', __name__)
    # import simple
    from simple import run # this will execute the module also

class CheatTemplate(ABC):
    @abstractclassmethod
    def cheat_method(self):
        pass

class CheatClass(CheatTemplate):
    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2
    
    def cheat_method(self):
        print(self.attr1, self.attr2)

    @classmethod
    def from_string(cls, s): # cls helps by not hardcoding the class name. So child classes can use this method
        attrs = s.split('-')
        return cls(attrs[0], attrs[1]) # this is equal to CheatClass(attr1, attr2)

    # >>> c.__dict__
    # {'attr1': 'a1', 'attr2': 'a2'}
    # >>> c.__class__
    # <class '__main__.CheatClass'>
    # >>> type(c)
    # <class '__main__.CheatClass'>
    # >>> CheatClass.__dict__
    # mappingproxy({'__module__': '__main__', '__init__': <function CheatClass.__init__ at 0x101ec20d0>, 'cheat_method': <function CheatClass.cheat_method at 0x101ec2158>, 'from_string': <classmethod object at 0x101e4c390>, '__doc__': None, '__abstractmethods__': frozenset(), '_abc_impl': <_abc_data object at 0x101e69060>})

def getsetdel_attr():
    cheatobj = CheatClass('attr1', 'attr2')
    #methods also use get, set, del machinery
    f = cheatobj.cheat_method
    print(f())
    setattr(cheatobj, 'attr2', 'new')
    print(getattr(cheatobj, 'attr2'))
    c = CheatClass.from_string('str1-str2')
    print(c.cheat_method())

class ChildCheat(CheatClass):
    def __init__(self, attr1, attr2, attr3): # extra attribute
        self.attr3 = attr3
        super().__init__(attr1, attr2)

    def cheat_method(self):
        print('child method')
        super().cheat_method()

class ChildMixin:
    def cheat_method(self):
        print('mixin method')
        super().cheat_method()

class Child2Cheat(ChildMixin, CheatClass):
    '''
    To see Method Resolution order, help(Child2Cheat)
    Child2Cheat.__mro__
    '''
    pass

def check_instance(obj):
    if not isinstance(obj, CheatClass):
        raise TypeError('must be CheatClass')

class CheatRepr(CheatClass):
    def __init__(self, attr1, attr2):
        super().__init__(attr1, attr2)
        self.list_ = [self.attr1, self.attr2]

    def __repr__(self):
        return 'CheatClass({},{})'.format(self.attr1, self.attr2)

    def __str__(self):
        return 'Sample class with attributes'

    def __getitem__(self, n):
        if isinstance(n, str):
            return getattr(self, n)
        return self.list_[n]

    def __len__(self):
        return len(self.list_)

    def __iter__(self):
        return self.list_.__iter__()
    # >>> obj
    # CheatClass(a1,a2)
    # >>> print(obj)
    # Sample class with attributes
    # >>> repr(obj)
    # 'CheatClass(a1,a2)'

class AltIter:
    def __init__(self, max):
        self.max = max

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.max:
            result = self.n
            self.n += 1
            return result
        raise StopIteration
    # What happens in a for loop
    # iter_obj = iter(iterable)     # create an iterator object from that iterable
    # while True:                   # infinite loop
    #     try:
    #         element = next(iter_obj)      # get the next item
    #         # do something with element
    #     except StopIteration:
    #         break                         # if StopIteration is raised, break from loop
        
class WithManager:
    def __enter__(self):
        print('entering')
        return 'some value'
    
    def __exit__(self, ty, val, tb):
        print('exiting')
        print('ty:', ty)
        print('val:', val)
        print('tb:' ,tb)

class PropertyAttr:

    def __init__(self, val):
        self.val = val #this calls @val.setter

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, newval):
        if not isinstance(newval, str):
            raise TypeError('Expecting a string')
        self._val = newval

    @val.deleter
    def val(self):
        del self._val

class AltProperty:

    def __init__(self, val=None):
        self.val = val

    def get_value(self):
        return self._val
    
    def set_value(self, newval):
        if not isinstance(newval, str):
            raise TypeError('Expecting a string')
        self._val = newval

    val = property(fget=get_value, fset=set_value, doc='I am val')
    # >>> AltProperty.val.__doc__
    # 'I am val'

    # >>> a = AltProperty('a')
    # >>> a.val
    # 'a'
    # how a.val works
    # >>> a.__class__.__dict__['val']
    # <property object at 0x102e35778>
    # >>> property = _
    # >>> hasattr(property, '__get__')
    # True
    # >>> property.__get__(a)
    # 'a'

    # how a.val = newval works
    # >>> a.__class__.__dict__['val']
    # <property object at 0x102e35778>
    # >>> prop = _
    # >>> hasattr(prop, '__set__')
    # True
    # >>> prop.__set__(a, 'b')
    # >>> a.val
    # 'b'

class MyInt:
    '''
    A descriptor is an object that impliments __get__, __set__ and __delete__.
    Property object impliments all thus it is a data descriptor. If only __get__ implimented it is non data descriptor
    '''
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        return instance.__dict__[self.name]
    
    def __set__(self, instance, val):
        if not isinstance(val, int):
            raise TypeError('Expected int')
        instance.__dict__[self.name] = val

class Point:
    x = MyInt('x')
    y = MyInt('y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

class InterceptGet:
    def __getattribute__(self, name):
        return 'Getting {}'.format(name)

class InterceptSet:
    def __setattr__(self, name, val):
        if name not in {'x', 'y', 'z'}:
            raise AttributeError('Attributes only allowed to be x, y or z')
        super().__setattr__(name,val)
    # >>> i = InterceptSet()
    # >>> i.z = 1
    # >>> i.z
    # 1
    # >>> i.a = 2
    # Traceback (most recent call last):
    # File "<stdin>", line 1, in <module>
    # File "/Users/devarajanperumal/pythonref/cheat.py", line 420, in __setattr__
    #     raise AttributeError('Attributes only allowed to be x, y or z')
    # AttributeError: Attributes only allowed to be x, y or z

class MissingAttr:
    '''
    __getattr__ is called when the attribute called is missing
    '''
    def __getattr__(self, name):
        return 'getting {}'.format(name)

    # >>> m = MissingAttr()
    # >>> m.x = 1
    # >>> m.x
    # 1
    # >>> m.y
    # 'getting y'
    # >>> m.__getattribute__('x')
    # 1
    # >>> m.__setattr__('x', 2)
    # >>> m.x
    # 2
    # >>> m.__delattr__('x')
    # >>> m.x
    # 'getting x'

class ListProxy:
    def __init__(self, *args):
        self.list_ = list(args)

    def __getattr__(self, name):
        return self.list_.__getattribute__(name)
    
    def __repr__(self):
        return str(self.list_)
    # >>> l = ListProxy(1,2,3)
    # >>> l.append(4)
    # >>> l
    # [1, 2, 3, 4]

import time

def delayed_eval(sec, func):
    time.sleep(sec)
    func()

def add_func(x,y):
    def add():
        print('{} + {} = {}'.format(x, y, x+y))
    return add
    # >>> myfunc = cheat.add_func(1, 2)
    # >>> cheat.delayed_eval(5, myfunc)
    # 1 + 2 = 3

def typed_prop(name, expected_type):
    '''
    We will create a function that will generate functions like def val1() and def val2() below:
    class PropertyAttr:

        def __init__(self, val1, val2):
            self.val1 = val1 #this calls @val.setter
            self.val2 = val2

        @property
        def val1(self):
            return self._val1

        @val1.setter
        def val1(self, newval):
            if not isinstance(newval, str):
                raise TypeError('Expecting a string')
            self._val1 = newval
        
        @property
        def val2(self):
            return self._val2

        @val2.setter
        def val2(self, newval):
            if not isinstance(newval, int):
                raise TypeError('Expecting a integer')
            self._val2 = newval
    '''
    private_name =  '_' + name

    @property
    def prop(self):
        return getattr(self, private_name)
    
    @prop.setter
    def prop(self, newval):
        if not isinstance(newval, expected_type):
            raise TypeError('Expecting {}'.format(expected_type))
        setattr(self, private_name, newval)
        
    return prop

class NewProp:
    val1 = typed_prop('val1', str)
    val2 = typed_prop('val2', int)

    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2

from functools import wraps

def logged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Calling', func.__name__)
        func(*args, **kwargs)
    return wrapper

def format(fmt):
    def logged(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(fmt.format(func=func))
            func(*args, **kwargs)
        return wrapper
    return logged

@logged
def add(x, y):
    print('{} + {} = {}'.format(x, y, x+y))

@format('CALLING {func.__name__}')
def addnew(x, y):
    print('{} + {} = {}'.format(x, y, x+y))

def logmethod(cls):
    for key,value in vars(cls).items():
        if callable(value):
            setattr(cls, key, logged(value))
    return cls

@logmethod
class Testing:
    def __init__(self, val):
        self.val = val
    def yow(self):
        print('yow!')
    def grok(self):
        print('grok')

if __name__ == '__main__':
    # commandline()
    # printing()
    # stringformatting()
    # writefile()
    # setbreakpoint()
    # readfile()
    # stringops()
    # funcoptional('arg1', 'arg2', 'option')              # TypeError: funcoptional() takes 2 positional arguments but 3 were given
    # funcoptional('arg1', 'arg2', option='option')       # Correct behavior
    # funcoptional('arg1', 'arg2')                        # Correct behavior
    # funcoptional(arg2='arg2', arg1='arg1')              # Correct behavior
    # funcoptional('arg2', arg1='arg1')                   # TypeError: funcoptional() got multiple values for argument 'arg1'
    # funcoptional(arg2='arg2', 'arg1')                   # SyntaxError: positional argument follows keyword argument
    # funckwonly()                                        # TypeError: funckwonly() missing 1 required keyword-only argument: 'arg'
    # funckwonly('arg', 'option')                         # TypeError: funckwonly() takes 0 positional arguments but 2 were given
    # funckwonly(arg='arg', option='option')              # Correct
    # funckwonly(arg='arg')                               # Correct
    # argskwargs()        # TypeError: argskwargs() missing 1 required positional argument: 'arg'
    # argskwargs('arg1', 'arg2', 'arg3', 'arg4')  # arg: arg1 args: ('arg2', 'arg3', 'arg4') type: <class 'tuple'> kwargs {}
    # portfolios = read_portfolios('Data/missing.csv')
    # totalinvest = sum_listcomp(portfolios)
    # more100 = if_listcomp(portfolios)
    # names = setcomp(portfolios)
    # data = b'72.51\n9.27\n153.24\n30.11\n'
    # currentprice = dict_from_zip(names, data)
    # minprice, maxprice = min_max(portfolios)
    # groupedbyname = grouping_super(portfolios)
    # jsonstring = converting(portfolios)
    # about_import()
    # portfolios = portie.read_csv('Data/missing.csv', [str, str, int, float])
    pass

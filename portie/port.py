# port.py
from . import reader

def read_portfolios(filename, *, error='warn'):
    return reader.read_csv(filename, [str, str, int, float], error=error)

if __name__=='__main__':
    portfolio = read_portfolios('../Data/portfolio.csv')
    total = 0.0
    for holding in portfolio:
        total += holding['shares'] * holding['price']
    print('total is', total)

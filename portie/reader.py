# reader.py

import csv

def read_csv(filename, types, *, error='warn'):
    '''
    Read a csv with type conversion into list of dictionary
    '''
    if error not in {'silent', 'raise', 'warn'}:
        raise ValueError("error must be 'silent', 'raise' or 'warn'(default)")
    portfolios = []
    with open(filename, 'r') as f:
        rows = csv.reader(f)
        header = next(rows)
        for rowno, row in enumerate(rows, start=1):
            try:
                row = [func(value) for func, value in zip(types, row)]
            except ValueError as err:
                if error=='warn':
                    print(f'{rowno}: {row} --> {err}')
                elif error=='silent':
                    pass
                else:
                    raise
                continue
            portfolios.append(dict(zip(header,row)))
    return portfolios    
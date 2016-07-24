import pickle
import doctest

def int2str(i, length):
    """
    >>> int2str(1211,6)
    '001211'
    """
    res = str(i)
    return '0'*(length - len(res)) + res

def postal2fips(pc):
    """
    Takes a 2-letter postal state code and returns a 2-digit FIPS code for that state
    Input: 2-letter state postal code
    Returns: 2-digit state FIPS code (as str)
    >>> postal2fips('AL')
    '01'
    """
    with open('pkl/postal2fips.pkl', 'rb') as fh:
        p2f = pickle.load(fh)
        return p2f[pc]
    
def fips2postal(fips):
    """
    Takes 2-digit state FIPS code and returns the 2-letter state postal code
    Input: 2-digit state FIPS code
    Returns: 2-letter state postal code
    >>> fips2postal('01')
    'AL'
    """
    if type(fips)==int:
        fips = int2str(fips, 2)
    with open('pkl/fips2postal.pkl', 'rb') as fh:
        f2p = pickle.load(fh)
        return f2p[fips]
    
def fips2county(fips):
    """
    Input: 5-digit FIPS code (can also take int)
    Returns: tuple of state and county name
    >>> fips2county('16079')
    ('ID', 'Shoshone County')
    >>> fips2county(1001)
    ('AL', 'Autauga County')
    """
    if type(fips)==int:
        fips = int2str(fips, 5)
    with open('pkl/fips2county.pkl', 'rb') as fh:
        f2c = pickle.load(fh)
        return f2c[fips]

if __name__ == '__main__':
    doctest.testmod()
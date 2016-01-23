# -*- coding: utf-8 -*-
"""

"""
import sys

res = {'03': 'F', '05': 'B'}
for i in range(1, 100):
    pp = ''.join([res.get('{}{}'.format((i % ii), ii), '') for ii in [3, 5]])
    print(pp or i)


# or
print('*' * 80)
if sys.version_info[0] > 2:
    for i in range(1, 100):
        pp = ''.join([res.get('{}{}'.format((i % ii), ii), '') for ii in [3, 5]])
        print(next(filter(None, [pp, i])))
else:
    for i in range(1, 100):
        pp = ''.join([res.get('{}{}'.format((i % ii), ii), '') for ii in [3, 5]])
        print(filter(None, [pp, i])[0])

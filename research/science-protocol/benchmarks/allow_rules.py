import re
src = open('typecheck.py').read()
# allow $vars inside rule (==>) atoms, but keep rejecting them in ground (--> atoms
old = """    for a in args:
        if isinstance(a, str) and a.startswith('$'):"""
new = """    rule = pred == '==>'
    for a in args:
        if isinstance(a, str) and a.startswith('$') and not rule:"""
assert old in src
src = src.replace(old, new)
open('typecheck.py','w').write(src)

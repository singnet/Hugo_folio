import json, glob, re

def balanced(s):
    d=0
    for ch in s:
        if ch=='(': d+=1
        elif ch==')':
            d-=1
            if d<0: return False
    return d==0

def fix(atom):
    a=atom.strip()
    if 'stv' not in a or a.startswith('(-->') or a.startswith('(==>') :
        # candidate atoms without stv: just strip stray extra parens
        return a
    m=re.search(r'\(stv\s+([\d.]+)\s+([\d.]+)\)', a)
    if not m: return a
    pat=a[:m.start()].strip()
    pat=pat.lstrip('(|-').strip()
    # pat now like ((--> x y)) or ((--> x y) possibly unbalanced
    while pat.endswith(')') and not balanced(pat):
        pat=pat[:-1]
    # ensure pat is ((...))
    if not (pat.startswith('((') and pat.endswith('))') and balanced(pat)):
        # try to wrap: inner content
        inner=pat.strip('()').strip()
        while not balanced(inner):
            inner=inner[:-1]
        pat='((%s))' % inner
    return '(|- %s (stv %s %s))' % (pat, m.group(1), m.group(2))

for f in sorted(glob.glob('fixtures/sample_*.jsonl')):
    data=json.load(open(f))
    for c in data['claims']:
        old=c.get('metta_atom')
        if old:
            new=fix(old)
            c['metta_atom']=new
            if not balanced(new):
                print('STILL UNBALANCED', f, c['claim_id'], new)
    json.dump(data, open(f,'w'), indent=1)
    print(f, 'done')

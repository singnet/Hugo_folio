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
    # stv buried inside pattern: (|- ((PAT (stv s c))))  or missing outer close
    m=re.match(r'^\(\|-\s*\(\((.*)\s*\(stv ([\d.]+) ([\d.]+)\)\)\)?\s*$', a)
    if m:
        return '(|- ((%s) (stv %s %s)))' % (m.group(1).strip(), m.group(2), m.group(3))
    m=re.match(r'^\(\|-\s*\((.*)\)\s*\(stv\s+([\d.]+)\s+([\d.]+)\)\)\s*$', a)
    if m:
        return '(|- ((%s) (stv %s %s)))' % (m.group(1).strip(), m.group(2), m.group(3))
    return a

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

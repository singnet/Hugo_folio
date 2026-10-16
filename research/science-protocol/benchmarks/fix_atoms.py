import json, re, glob

def balanced(s):
    d = 0
    for ch in s:
        if ch == '(':
            d += 1
        elif ch == ')':
            d -= 1
        if d < 0:
            return False
    return d == 0

def fix(atom):
    if not atom:
        return atom
    a = atom.strip()
    # nested PAT form: (|- ((PAT)) (stv s c))
    m = re.match(r'^\(\|-\s*\(\((.*)\)\)\s*\(stv\s+([\d.]+)\s+([\d.]+)\)\)$', a)
    if m:
        return '(|- ((%s) (stv %s %s)))' % (m.group(1).strip(), m.group(2), m.group(3))
    # missing final paren: (|- ((PAT) (stv s c)
    m = re.match(r'^\(\|-\s*\(\((.*)\)\s*\(stv\s+([\d.]+)\s+([\d.]+)\)\)$', a)
    if m:
        return '(|- ((%s) (stv %s %s)))' % (m.group(1).strip(), m.group(2), m.group(3))
    return a

for f in sorted(glob.glob('fixtures/sample_*.jsonl')):
    data = json.load(open(f))
    fixed = []
    for c in data['claims']:
        old = c.get('metta_atom')
        new = fix(old) if old else old
        if new and new != old:
            fixed.append((c['claim_id'], old, new))
        c['metta_atom'] = new
        if new and not balanced(new):
            print('STILL UNBALANCED', f, c['claim_id'], new)
    json.dump(data, open(f, 'w'), indent=1)
    print(f, 'fixed:', len(fixed))
    for cid, o, n in fixed:
        print(' ', cid, '->', n)
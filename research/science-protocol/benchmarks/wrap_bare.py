import json, glob, re
for f in sorted(glob.glob('fixtures/sample_*.jsonl')):
    data = json.load(open(f))
    for c in data['claims']:
        a = c.get('metta_atom')
        if not a: continue
        a = a.strip()
        if a.startswith('(|-'): continue
        if a.startswith('(and '):
            parts = re.findall(r'\((\S+)\s+(\S+)\)', a)
            conj = '-and-'.join(p[1] for p in parts)
            head = parts[0][0]
            a = '(--> %s %s)' % (head, conj)
        m = re.match(r'^\((\S+)\s+(\S+)\s+(\S+)\)$', a)
        if m:
            stv = c.get('stv') or '1.0 0.9'
            if isinstance(stv, list): stv = '%s %s' % tuple(stv)
            c['metta_atom'] = '(|- ((%s %s %s) (stv %s)))' % (m.group(1), m.group(2), m.group(3), stv)
    json.dump(data, open(f, 'w'), indent=1)
    print(f, 'done')
